"""GPU training loops; use ACE's own preprocessing and model/LoRA components."""

from __future__ import annotations

import random
from pathlib import Path

import torch

from .ace import load_model, save_adapter
from .config import Config
from .flow import flow_mse, preference_objective
from .io import read_jsonl, write_json, write_jsonl


def load_tensor(path: Path) -> dict:
    # Tensors were produced by our pinned ACE preprocessing stage.
    row = torch.load(path, map_location="cpu", weights_only=True)
    required = {"target_latents", "attention_mask", "encoder_hidden_states",
                "encoder_attention_mask", "context_latents"}
    if not required <= row.keys():
        raise ValueError(f"Incomplete ACE tensor: {path}")
    # Training consumes one example at a time. This is the single-item equivalent
    # of ACE's collate_preprocessed_batch, without importing torchaudio/Lightning.
    return {key: value.unsqueeze(0) for key, value in row.items()
            if key in required} | {"metadata": [row.get("metadata", {})]}


def _train_loop(model, cfg: Config, steps: int, learning_rate: float, accumulation: int,
                save_every: int, output: Path, examples: list, objective, stage: str) -> None:
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                                  lr=learning_rate)
    rng = random.Random(cfg.seed)
    records = []
    model.train()
    optimizer.zero_grad(set_to_none=True)
    for step in range(1, steps + 1):
        for _ in range(accumulation):
            example = rng.choice(examples)
            loss, extra = objective(example)
            if not torch.isfinite(loss):
                raise FloatingPointError(f"Non-finite {stage} loss at step {step}")
            (loss / accumulation).backward()
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        record = {"step": step, "loss": float(loss.detach()), **extra}
        records.append(record)
        if step == 1 or step % 10 == 0:
            print(f"{stage} step {step}/{steps}: {record['loss']:.5f}", flush=True)
        if step % save_every == 0 or step == steps:
            save_adapter(model, output / f"step-{step:06d}", cfg,
                         {"stage": stage, "step": step})
            write_jsonl(output / "metrics.jsonl", records)
    save_adapter(model, output / "final", cfg, {"stage": stage, "step": steps})


def _validation(model, paths: list[Path], cfg: Config) -> dict:
    if not paths:
        raise ValueError("No validation tensors")
    was_training = model.training
    model.eval()
    torch.manual_seed(cfg.seed)
    losses = []
    with torch.no_grad():
        for path in paths[:cfg.sft.validation_samples]:
            losses.append(float(flow_mse(model, load_tensor(path)).mean()))
    model.train(was_training)
    return {"mean_flow_mse": sum(losses) / len(losses), "samples": len(losses)}


def run_sft(checkpoint_dir: Path, cfg: Config, tensors: Path,
            validation_tensors: Path, output: Path, *, model_loader=load_model) -> None:
    if (output / "final/adapter/adapter_config.json").exists():
        raise FileExistsError(f"SFT final adapter already exists: {output}")
    paths = sorted(tensors.glob("*.pt"))
    paths = [p for p in paths if not p.name.endswith(".tmp.pt")]
    if not paths:
        raise ValueError("No preprocessed training tensors")
    validation_paths = sorted(validation_tensors.glob("*.pt"))
    validation_paths = [p for p in validation_paths if not p.name.endswith(".tmp.pt")]
    model = model_loader(checkpoint_dir, cfg)
    baseline = _validation(model, validation_paths, cfg)

    def objective(path):
        batch = load_tensor(path)
        device = cfg.runtime.device
        with torch.autocast(device_type=device, dtype=torch.bfloat16,
                            enabled=device == "cuda" and cfg.runtime.precision == "bf16"):
            loss = flow_mse(model, batch, cfg_dropout=cfg.sft.cfg_dropout).mean()
        return loss, {}

    _train_loop(model, cfg, cfg.sft.steps, cfg.sft.learning_rate,
                cfg.sft.gradient_accumulation, cfg.sft.save_every, output, paths,
                objective, "sft")
    after = _validation(model, validation_paths, cfg)
    write_json(output / "validation.json", {"before": baseline, "after": after})


def run_preference(checkpoint_dir: Path, cfg: Config, sft_adapter: Path,
                   pairs_file: Path, tensors: Path, output: Path, *, model_loader=load_model) -> None:
    if (output / "final/adapter/adapter_config.json").exists():
        raise FileExistsError(f"Preference final adapter already exists: {output}")
    pairs = read_jsonl(pairs_file)
    if not all(p.get("chosen") and p.get("rejected") for p in pairs):
        raise ValueError("Each preference pair needs chosen and rejected IDs")
    model = model_loader(checkpoint_dir, cfg, sft_adapter, preference=True)
    known = set()
    for pair in pairs:
        for key in ("chosen", "rejected"):
            if pair[key] not in known:
                if not (tensors / f"{pair[key]}.pt").is_file():
                    raise FileNotFoundError(f"Missing preference tensor: {pair[key]}")
                known.add(pair[key])

    def objective(pair):
        chosen = load_tensor(tensors / f"{pair['chosen']}.pt")
        rejected = load_tensor(tensors / f"{pair['rejected']}.pt")
        with torch.autocast(device_type=cfg.runtime.device, dtype=torch.bfloat16,
                            enabled=cfg.runtime.device == "cuda" and cfg.runtime.precision == "bf16"):
            return preference_objective(model, chosen, rejected,
                                        cfg.preference.beta, cfg.preference.sft_anchor)

    _train_loop(model, cfg, cfg.preference.steps, cfg.preference.learning_rate,
                cfg.preference.gradient_accumulation, cfg.preference.save_every,
                output, pairs, objective, "preference")
