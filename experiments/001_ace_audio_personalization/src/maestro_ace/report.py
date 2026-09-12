"""Frozen prompt/seed matching for manual listening evaluation."""

from __future__ import annotations

import random
import shutil
from pathlib import Path

from .config import Config
from .data import load_prompts
from .io import file_hash, write_json, write_jsonl


def report(root: Path, cfg: Config, artifacts: Path) -> dict:
    prompts = load_prompts(root, cfg)["eval"]
    stages = ["base", "sft", "human", "ai"]
    rows = []
    answer_key = []
    blind = artifacts / "reports/blind_clips"
    blind.mkdir(parents=True, exist_ok=True)
    for prompt in prompts:
        for seed in cfg.generation.seeds:
            variants = {}
            for stage in stages:
                path = artifacts / "generations/eval" / stage / f"{prompt['id']}-{seed}.flac"
                if path.is_file():
                    variants[stage] = path
            order = sorted(variants)
            random.Random(f"{cfg.seed}:{prompt['id']}:{seed}").shuffle(order)
            clips = {}
            key = {"prompt_id": prompt["id"], "seed": seed, "take_to_stage": {}}
            for index, stage in enumerate(order):
                label = chr(ord("A") + index)
                target = blind / f"{prompt['id']}-{seed}-take-{label}.flac"
                if not target.exists() or file_hash(target) != file_hash(variants[stage]):
                    shutil.copyfile(variants[stage], target)
                clips[label] = str(target)
                key["take_to_stage"][label] = stage
            answer_key.append(key)
            rows.append({"prompt_id": prompt["id"], "seed": seed,
                         "caption": prompt["caption"], "clips": clips,
                         "questions": ["Which take would you keep?", "Is the instrumentation correct?",
                                       "Is the musical phrasing convincing?", "Any audible artifacts?"]})
    target = artifacts / "reports/eval_listening.jsonl"
    write_jsonl(target, rows)
    write_json(artifacts / "reports/answer_key.json", answer_key)
    summary = {"matched_cases": len(rows), "stages": stages,
               "complete_base_sft_pairs": sum(
                   {"base", "sft"} <= set(key["take_to_stage"].values()) for key in answer_key),
               "listening_index": str(target),
               "answer_key": str(artifacts / "reports/answer_key.json")}
    write_json(artifacts / "reports/summary.json", summary)
    return summary
