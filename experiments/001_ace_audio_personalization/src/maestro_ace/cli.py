"""Experiment-scoped, explicit stage runner. No hidden downloads or GPU work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import ROOT, load_config
from .io import write_json


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="maestro-ace")
    p.add_argument("--config", type=Path, default=ROOT / "configs/piano_violin.toml")
    p.add_argument("--ace-root", type=Path, help="Pinned ACE-Step 1.5 checkout (GPU stages)")
    p.add_argument("--checkpoints", type=Path, help="ACE checkpoint directory (GPU stages)")
    sub = p.add_subparsers(dest="stage", required=True)
    sub.add_parser("doctor", help="Show environment, config and stage readiness")
    sub.add_parser("smoke", help="Run every stage locally with synthetic data and a tiny CPU model")
    sub.add_parser("prepare", help="Validate recordings and freeze composition-level split")
    sub.add_parser("preprocess", help="ACE preprocessing for SFT train and validation")
    sub.add_parser("sft", help="Train LoRA with ACE flow-matching loss")
    g = sub.add_parser("generate", help="Generate frozen prompts and seeded candidates")
    g.add_argument("--split", choices=["feedback", "eval"], required=True)
    g.add_argument("--model", choices=["base", "sft", "human", "ai"], required=True)
    rank = sub.add_parser("rank", help="Create human or CLAP preference pairs")
    rank.add_argument("--source", choices=["human", "ai"], required=True)
    rank.add_argument("--ballots", type=Path, help="Required for human ranking")
    pp = sub.add_parser("preprocess-pairs", help="ACE preprocessing for ranked candidates")
    pp.add_argument("--source", choices=["human", "ai"], required=True)
    tr = sub.add_parser("preference", help="Train experimental offline flow-DPO adapter")
    tr.add_argument("--source", choices=["human", "ai"], required=True)
    sub.add_parser("report", help="Build a matched-seed blind listening index")
    return p


def _require_gpu_args(args, cfg):
    if not args.ace_root or not args.checkpoints:
        raise ValueError("GPU stages require --ace-root and --checkpoints")
    from .ace import check_ace_checkout, check_checkpoint_dir, use_ace_python

    revision = check_ace_checkout(args.ace_root, cfg)
    check_checkpoint_dir(args.checkpoints, cfg)
    use_ace_python(args.ace_root.resolve())
    import torch

    if cfg.runtime.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but PyTorch cannot see a CUDA GPU")
    print(f"ACE {revision[:12]} | torch {torch.__version__} | {cfg.runtime.device}")


def _prepared(artifacts: Path) -> Path:
    folder = artifacts / "prepared"
    if not (folder / "train.json").is_file():
        raise FileNotFoundError("Run prepare first")
    return folder


def _adapter(artifacts: Path, name: str) -> Path:
    path = artifacts / "checkpoints" / name / "final" / "adapter"
    if not (path / "adapter_config.json").is_file():
        raise FileNotFoundError(f"Adapter missing: {path}")
    return path


def main() -> None:
    args = parser().parse_args()
    cfg = load_config(args.config.resolve())
    root = ROOT
    artifacts = root / "artifacts"
    stage = args.stage
    if stage == "smoke":
        from .smoke import run_smoke

        print(json.dumps(run_smoke(cfg), indent=2))
        return
    if stage == "doctor":
        from .data import load_prompts

        prompts = load_prompts(root, cfg)
        status = {"experiment": root.name, "config": str(args.config.resolve()),
                  "ace_revision": cfg.runtime.ace_revision,
                  "recordings_manifest": (root / cfg.data.manifest).is_file(),
                  "prepared": (artifacts / "prepared/train.json").is_file(),
                  "sft_adapter": (artifacts / "checkpoints/sft/final/adapter/adapter_config.json").is_file(),
                  "feedback_prompts": len(prompts["feedback"]), "eval_prompts": len(prompts["eval"]),
                  "ace_root": str(args.ace_root) if args.ace_root else None,
                  "checkpoints": str(args.checkpoints) if args.checkpoints else None}
        print(json.dumps(status, indent=2))
        return
    if stage == "prepare":
        from .data import prepare

        result = prepare(root, cfg, artifacts / "prepared")
        write_json(artifacts / "prepared/summary.json", result)
        print(json.dumps(result, indent=2))
        return
    if stage == "report":
        from .report import report

        print(json.dumps(report(root, cfg, artifacts), indent=2))
        return
    if stage == "rank":
        from .preferences import make_ai_pairs, make_human_pairs

        candidate_file = artifacts / "generations/feedback/sft/candidates.jsonl"
        output = artifacts / "preferences" / args.source / "pairs.jsonl"
        if args.source == "human":
            if not args.ballots:
                raise ValueError("--ballots is required for human ranking")
            pairs = make_human_pairs(candidate_file, args.ballots, output)
        else:
            pairs = make_ai_pairs(candidate_file, output, cfg)
        print(f"Wrote {len(pairs)} {args.source} pairs to {output}")
        return

    _require_gpu_args(args, cfg)
    from .ace import preprocess

    if stage == "preprocess":
        prepared = _prepared(artifacts)
        for split in ("train", "validation"):
            result = preprocess(args.ace_root, args.checkpoints, cfg, prepared / f"{split}.json",
                                artifacts / "tensors" / split)
            print(split, result)
    elif stage == "sft":
        from .train import run_sft

        _prepared(artifacts)
        if not (artifacts / "tensors/train").is_dir():
            raise FileNotFoundError("Run preprocess first")
        run_sft(args.checkpoints, cfg, artifacts / "tensors/train",
                artifacts / "tensors/validation",
                artifacts / "checkpoints/sft")
    elif stage == "generate":
        from .generate import generate

        adapter = None if args.model == "base" else _adapter(artifacts, args.model)
        rows = generate(root, args.ace_root, args.checkpoints, cfg,
                        args.model, adapter, args.split,
                        artifacts / "generations" / args.split / args.model)
        print(f"Generated {len(rows)} audio candidates")
    elif stage == "preprocess-pairs":
        from .preferences import make_preprocess_manifest

        pair_root = artifacts / "preferences" / args.source
        count = make_preprocess_manifest(
            artifacts / "generations/feedback/sft/candidates.jsonl",
            pair_root / "pairs.jsonl", pair_root / "ace_samples.json")
        result = preprocess(args.ace_root, args.checkpoints, cfg,
                            pair_root / "ace_samples.json", pair_root / "tensors")
        print(f"Preprocessed {count} paired candidates: {result}")
    elif stage == "preference":
        from .train import run_preference

        pair_root = artifacts / "preferences" / args.source
        run_preference(args.checkpoints, cfg, _adapter(artifacts, "sft"),
                       pair_root / "pairs.jsonl", pair_root / "tensors",
                       artifacts / "checkpoints" / args.source)
    else:
        raise AssertionError(stage)


if __name__ == "__main__":
    main()
