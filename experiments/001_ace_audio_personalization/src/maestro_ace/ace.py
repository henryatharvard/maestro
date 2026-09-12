"""Thin integration with an independently installed, revision-pinned ACE-Step checkout."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from .config import Config
from .io import file_hash, write_json


def check_ace_checkout(path: Path, cfg: Config) -> str:
    path = path.resolve()
    if not (path / "train.py").is_file() or not (path / "acestep/inference.py").is_file():
        raise FileNotFoundError(f"Not an ACE-Step checkout: {path}")
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True,
                            check=True)
    revision = result.stdout.strip()
    if revision != cfg.runtime.ace_revision:
        raise ValueError(f"ACE revision mismatch: need {cfg.runtime.ace_revision}, got {revision}")
    return revision


def check_checkpoint_dir(path: Path, cfg: Config) -> None:
    variant = {
        "base": "acestep-v15-base", "sft": "acestep-v15-sft",
        "turbo": "acestep-v15-turbo", "xl_base": "acestep-v15-xl-base",
        "xl_sft": "acestep-v15-xl-sft", "xl_turbo": "acestep-v15-xl-turbo",
    }[cfg.runtime.variant]
    for item in (variant, "vae", "Qwen3-Embedding-0.6B"):
        if not (path / item).is_dir():
            raise FileNotFoundError(f"ACE checkpoint component missing: {path / item}")


def preprocess(ace_root: Path, checkpoint_dir: Path, cfg: Config,
               dataset_json: Path, output: Path) -> dict:
    check_ace_checkout(ace_root, cfg)
    check_checkpoint_dir(checkpoint_dir, cfg)
    from acestep.training_v2.preprocess import preprocess_audio_files

    result = preprocess_audio_files(
        audio_dir=None, dataset_json=str(dataset_json.resolve()),
        output_dir=str(output.resolve()), checkpoint_dir=str(checkpoint_dir.resolve()),
        variant=cfg.runtime.variant, max_duration=cfg.data.max_seconds,
        device=cfg.runtime.device, precision=cfg.runtime.precision,
    )
    expected = len(json.loads(dataset_json.read_text())["samples"])
    actual = len(list(output.glob("*.pt"))) - len(list(output.glob("*.tmp.pt")))
    if result["failed"] or actual != expected:
        raise RuntimeError(f"ACE preprocessing incomplete: {result}, expected {expected}, found {actual}")
    return result


def load_model(checkpoint_dir: Path, cfg: Config, adapter: Path | None = None,
               preference: bool = False):
    from acestep.training_v2.model_loader import load_decoder_for_training

    model = load_decoder_for_training(str(checkpoint_dir), cfg.runtime.variant,
                                      cfg.runtime.device, cfg.runtime.precision)
    if adapter:
        from peft import PeftModel

        model.decoder = PeftModel.from_pretrained(model.decoder, str(adapter),
                                                adapter_name="default", is_trainable=True)
        if preference:
            model.decoder.load_adapter(str(adapter), adapter_name="reference", is_trainable=False)
            model.decoder.set_adapter("default")
        for name, param in model.named_parameters():
            param.requires_grad = "lora_" in name and ".default." in name
    else:
        from acestep.training.configs import LoRAConfig
        from acestep.training.lora_injection import inject_lora_into_dit

        model, _ = inject_lora_into_dit(model, LoRAConfig(
            r=cfg.lora.rank, alpha=cfg.lora.alpha, dropout=cfg.lora.dropout,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        ))
    model.train()
    return model


def save_adapter(model, output: Path, cfg: Config, extra: dict) -> None:
    adapter = output / "adapter"
    adapter.mkdir(parents=True, exist_ok=True)
    selected = ["default"] if "default" in model.decoder.peft_config else None
    model.decoder.save_pretrained(str(adapter), safe_serialization=True,
                                  selected_adapters=selected)
    write_json(output / "provenance.json", {
        "ace_revision": cfg.runtime.ace_revision, "variant": cfg.runtime.variant,
        "adapter_sha256": {p.name: file_hash(p) for p in adapter.iterdir() if p.is_file()},
        **extra,
    })


def use_ace_python(ace_root: Path) -> None:
    """Use the installed checkout package, including its model code, without vendoring weights."""
    if str(ace_root) not in sys.path:
        sys.path.insert(0, str(ace_root))
