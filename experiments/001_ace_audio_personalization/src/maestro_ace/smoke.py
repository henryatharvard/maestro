"""Full local wiring smoke. Synthetic audio/tensors/model are NOT an ACE quality test."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import soundfile as sf
import torch
from torch import nn

from .config import ROOT, Config
from .data import prepare
from .generate import generate
from .io import read_jsonl, write_json, write_jsonl
from .preferences import make_ai_pairs, make_human_pairs, make_preprocess_manifest
from .report import report
from .train import run_preference, run_sft


class TinyDecoder(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.base = nn.Linear(64, 64, bias=False)
        self.condition = nn.Linear(16, 64, bias=False)
        self.lora_A = nn.ModuleDict({name: nn.Linear(64, 4, bias=False)
                                     for name in ("default", "reference")})
        self.lora_B = nn.ModuleDict({name: nn.Linear(4, 64, bias=False)
                                     for name in ("default", "reference")})
        self.peft_config = {"default": {}}
        self.active_adapter = "default"
        for parameter in self.base.parameters():
            parameter.requires_grad_(False)
        for parameter in self.condition.parameters():
            parameter.requires_grad_(False)
        for parameter in self.lora_A.reference.parameters():
            parameter.requires_grad_(False)
        for parameter in self.lora_B.reference.parameters():
            parameter.requires_grad_(False)

    def set_adapter(self, name: str) -> None:
        if name not in ("default", "reference"):
            raise ValueError(name)
        self.active_adapter = name

    def forward(self, *, hidden_states, timestep, timestep_r, attention_mask,
                encoder_hidden_states, encoder_attention_mask, context_latents):
        del timestep_r, attention_mask, context_latents
        condition = (encoder_hidden_states * encoder_attention_mask[:, :, None]).mean(dim=1)
        adapter = self.active_adapter
        predicted = (self.base(hidden_states) +
                     self.lora_B[adapter](self.lora_A[adapter](hidden_states)) +
                     self.condition(condition)[:, None, :] + timestep[:, None, None])
        return (predicted,)

    def save_pretrained(self, directory: str, *, safe_serialization: bool,
                        selected_adapters: list[str] | None) -> None:
        del safe_serialization, selected_adapters
        target = Path(directory)
        write_json(target / "adapter_config.json", {"backend": "tiny-smoke-only"})
        torch.save({"lora_A": self.lora_A.default.state_dict(),
                    "lora_B": self.lora_B.default.state_dict()}, target / "smoke_weights.pt")


class TinyModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.decoder = TinyDecoder()
        self.config = SimpleNamespace(timestep_mu=-0.4, timestep_sigma=1.0)
        self.register_buffer("null_condition_emb", torch.zeros(1, 1, 16))


def _tiny_loader(checkpoint_dir: Path, cfg: Config, adapter: Path | None = None,
                 preference: bool = False) -> TinyModel:
    del checkpoint_dir, cfg
    torch.manual_seed(1234)
    model = TinyModel()
    if adapter is not None:
        state = torch.load(adapter / "smoke_weights.pt", map_location="cpu", weights_only=True)
        model.decoder.lora_A.default.load_state_dict(state["lora_A"])
        model.decoder.lora_B.default.load_state_dict(state["lora_B"])
        if preference:
            model.decoder.lora_A.reference.load_state_dict(state["lora_A"])
            model.decoder.lora_B.reference.load_state_dict(state["lora_B"])
    return model


def _tone(path: Path, *, amplitude: float, frequency: float, seconds: float = 10.0) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = int(48000 * seconds)
    time = np.arange(frames, dtype=np.float32) / 48000
    sf.write(path, amplitude * np.sin(2 * np.pi * frequency * time), 48000,
             format="FLAC", subtype="PCM_16")


def _seed_inputs(root: Path) -> None:
    records = []
    for index, instrument in enumerate(("piano", "violin")):
        name = f"own-{instrument}"
        _tone(root / "data" / f"{name}.flac", amplitude=0.15,
              frequency=220 + index * 110)
        records.append({"id": name, "composition_id": name,
                        "audio_path": f"data/{name}.flac",
                        "caption": f"Original expressive {instrument} melody, recorded for the smoke test",
                        "instruments": [instrument], "provenance": "synthetic smoke audio"})
    write_jsonl(root / "data/recordings.jsonl", records)
    for split, count in (("feedback", 2), ("eval", 1)):
        prompts = [{"id": f"{split}-{index}",
                    "caption": f"Original instrumental {split} arrangement number {index} for piano and violin",
                    "duration": 10.0} for index in range(count)]
        write_jsonl(root / "prompts" / f"{split}.jsonl", prompts)


def _fake_preprocess(manifest: Path, output: Path) -> int:
    samples = json.loads(manifest.read_text())["samples"]
    output.mkdir(parents=True, exist_ok=True)
    for sample in samples:
        ident = Path(sample["audio_path"]).stem
        rng = np.random.default_rng(sum(map(ord, ident)))
        row = {"target_latents": torch.tensor(rng.normal(size=(8, 64)), dtype=torch.float32),
               "attention_mask": torch.ones(8),
               "encoder_hidden_states": torch.tensor(rng.normal(size=(4, 16)), dtype=torch.float32),
               "encoder_attention_mask": torch.ones(4),
               "context_latents": torch.zeros(8, 65),
               "metadata": {"id": ident, "backend": "synthetic-smoke"}}
        torch.save(row, output / f"{ident}.pt")
    return len(samples)


def _fake_renderer(stage: str):
    def render(prompt: dict, seed: int, target: Path) -> None:
        amplitude = 0.11 + 0.03 * (seed % 2) + 0.005 * ("base", "sft", "human", "ai").index(stage)
        frequency = 220 + 30 * (seed % 2) + 10 * len(prompt["id"])
        _tone(target, amplitude=amplitude, frequency=frequency)

    return render


def _energy_score(path: Path, caption: str) -> float:
    del caption
    audio, sample_rate = sf.read(path, dtype="float32")
    assert sample_rate == 48000
    return float(np.sqrt(np.mean(np.square(audio))))


def run_smoke(config: Config) -> dict:
    """Exercise all stage orchestration while clearly excluding ACE weights and CLAP."""
    torch.set_num_threads(2)
    smoke_root = ROOT / "artifacts" / "smoke"
    smoke_root.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="run-", dir=smoke_root))
    cfg = config.model_copy(update={
        "runtime": config.runtime.model_copy(update={"device": "cpu", "precision": "fp32"}),
        "sft": config.sft.model_copy(update={"steps": 1, "gradient_accumulation": 1,
                                               "save_every": 1, "validation_samples": 1}),
        "preference": config.preference.model_copy(update={"steps": 1,
            "gradient_accumulation": 1, "save_every": 1}),
        "generation": config.generation.model_copy(update={"seeds": [101, 202]}),
    })
    artifacts = root / "artifacts"
    _seed_inputs(root)
    prepared = prepare(root, cfg, artifacts / "prepared")
    write_json(artifacts / "prepared/summary.json", prepared)
    assert prepared["train"] == 1 and prepared["validation"] == 1
    for split in ("train", "validation"):
        assert _fake_preprocess(artifacts / "prepared" / f"{split}.json",
                                artifacts / "tensors" / split) == 1
    sft_output = artifacts / "checkpoints/sft"
    run_sft(root, cfg, artifacts / "tensors/train", artifacts / "tensors/validation",
            sft_output, model_loader=_tiny_loader)
    sft_adapter = sft_output / "final/adapter"
    feedback_file = artifacts / "generations/feedback/sft/candidates.jsonl"
    feedback = generate(root, root, root, cfg, "sft", sft_adapter, "feedback",
                        feedback_file.parent, renderer=_fake_renderer("sft"))
    assert len(feedback) == 4
    ballots = [{"prompt_id": prompt, "chosen": f"{prompt}-202",
                "rejected": f"{prompt}-101", "reviewer": "smoke-runner",
                "reason": "synthetic preference for wiring test"}
               for prompt in ("feedback-0", "feedback-1")]
    ballot_file = root / "ballots.jsonl"
    write_jsonl(ballot_file, ballots)
    human_root = artifacts / "preferences/human"
    ai_root = artifacts / "preferences/ai"
    human_pairs = make_human_pairs(feedback_file, ballot_file, human_root / "pairs.jsonl")
    ai_pairs = make_ai_pairs(feedback_file, ai_root / "pairs.jsonl", cfg,
                             scorer=_energy_score)
    assert len(human_pairs) == len(ai_pairs) == 2
    for source, pair_root in (("human", human_root), ("ai", ai_root)):
        assert make_preprocess_manifest(feedback_file, pair_root / "pairs.jsonl",
                                        pair_root / "ace_samples.json") == 4
        assert _fake_preprocess(pair_root / "ace_samples.json", pair_root / "tensors") == 4
        run_preference(root, cfg, sft_adapter, pair_root / "pairs.jsonl",
                       pair_root / "tensors", artifacts / "checkpoints" / source,
                       model_loader=_tiny_loader)
    for stage in ("base", "sft", "human", "ai"):
        adapter = None if stage == "base" else artifacts / "checkpoints" / stage / "final/adapter"
        assert len(generate(root, root, root, cfg, stage, adapter, "eval",
                            artifacts / "generations/eval" / stage,
                            renderer=_fake_renderer(stage))) == 2
    summary = report(root, cfg, artifacts)
    assert summary["matched_cases"] == summary["complete_base_sft_pairs"] == 2
    assert all(len(row["clips"]) == 4 for row in read_jsonl(artifacts / "reports/eval_listening.jsonl"))
    result = {"status": "passed", "backend": "synthetic CPU stand-ins; no ACE/CLAP weights",
              "root": str(root), "prepared": prepared,
              "sft_steps": 1, "human_preference_steps": 1, "ai_preference_steps": 1,
              "feedback_candidates": len(feedback), "human_pairs": len(human_pairs),
              "ai_pairs": len(ai_pairs), "matched_eval_cases": summary["matched_cases"]}
    write_json(root / "smoke_result.json", result)
    return result
