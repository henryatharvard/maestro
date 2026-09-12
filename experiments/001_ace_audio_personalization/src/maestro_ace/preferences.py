"""Turn matched candidate audio into traceable human or AI preference pairs."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np
import soundfile as sf
from pydantic import Field

from .config import ID_PATTERN, Config, StrictModel
from .io import read_jsonl, write_json, write_jsonl


class Ballot(StrictModel):
    prompt_id: str = Field(pattern=ID_PATTERN)
    chosen: str = Field(pattern=ID_PATTERN)
    rejected: str = Field(pattern=ID_PATTERN)
    reviewer: str = Field(min_length=2)
    reason: str = Field(min_length=5)


def candidates(path: Path) -> list[dict]:
    rows = read_jsonl(path)
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("Duplicate candidate IDs")
    for row in rows:
        if not Path(row["audio_path"]).is_file():
            raise FileNotFoundError(f"Candidate audio missing: {row['audio_path']}")
    return rows


def make_human_pairs(candidate_file: Path, ballot_file: Path, output: Path) -> list[dict]:
    by_id = {r["id"]: r for r in candidates(candidate_file)}
    pairs = []
    for raw in read_jsonl(ballot_file):
        ballot = Ballot.model_validate(raw)
        if ballot.chosen == ballot.rejected:
            raise ValueError("Chosen and rejected IDs must differ")
        left, right = by_id[ballot.chosen], by_id[ballot.rejected]
        if left["prompt_id"] != right["prompt_id"] or left["prompt_id"] != ballot.prompt_id:
            raise ValueError("Preference candidates must share the specified prompt")
        if left["stage"] != right["stage"]:
            raise ValueError("Compare candidates from the same checkpoint stage")
        pairs.append({"prompt_id": ballot.prompt_id, "chosen": ballot.chosen,
                      "rejected": ballot.rejected, "source": "human",
                      "reviewer": ballot.reviewer, "reason": ballot.reason})
    write_jsonl(output, pairs)
    return pairs


def clap_score(path: Path, caption: str, processor, model, window_seconds: float) -> float:
    """Score one window; automated prompt match only, never a musical-taste verdict."""
    import torch

    audio, sr = sf.read(path, dtype="float32", always_2d=True)
    if sr != 48000:
        raise ValueError(f"CLAP judge expects 48 kHz ACE output, got {sr}: {path}")
    mono = audio.mean(axis=1)
    frames = int(sr * window_seconds)
    if len(mono) < frames:
        mono = np.pad(mono, (0, frames - len(mono)))
    if np.abs(mono).max() < 0.001:
        raise ValueError(f"Silent generated candidate: {path}")
    starts = sorted(set([0, max(0, (len(mono) - frames) // 2), max(0, len(mono) - frames)]))
    with torch.inference_mode():
        text = processor(text=[caption], return_tensors="pt", padding=True)
        text_embedding = model.get_text_features(**text)
        text_embedding = torch.nn.functional.normalize(text_embedding, dim=-1)
        scores = []
        for start in starts:
            segment = mono[start:start + frames]
            sound = processor(audios=[segment], sampling_rate=sr, return_tensors="pt", padding=True)
            audio_embedding = model.get_audio_features(**sound)
            audio_embedding = torch.nn.functional.normalize(audio_embedding, dim=-1)
            scores.append(float((audio_embedding * text_embedding).sum()))
    return sum(scores) / len(scores)


def make_ai_pairs(candidate_file: Path, output: Path, cfg: Config, *, scorer=None) -> list[dict]:
    model_name = cfg.judge.model
    if scorer is None:
        from transformers import AutoProcessor, ClapModel

        processor = AutoProcessor.from_pretrained(cfg.judge.model)
        model = ClapModel.from_pretrained(cfg.judge.model).eval()

        def scorer(path, caption):
            return clap_score(path, caption, processor, model, cfg.judge.window_seconds)
    else:
        model_name = "smoke-energy-v1"
    groups = defaultdict(list)
    records = []
    for row in candidates(candidate_file):
        score = scorer(Path(row["audio_path"]), row["caption"])
        groups[row["prompt_id"]].append((score, row))
        records.append({"id": row["id"], "score": score, "model": model_name})
    pairs = []
    for prompt_id, group in groups.items():
        group.sort(key=lambda item: item[0])
        low, high = group[0], group[-1]
        if high[1]["stage"] != low[1]["stage"]:
            raise ValueError("AI ranking requires candidates from a single checkpoint stage")
        if high[0] - low[0] >= cfg.judge.min_margin:
            pairs.append({"prompt_id": prompt_id, "chosen": high[1]["id"],
                          "rejected": low[1]["id"], "source": "ai-clap",
                          "judge_model": model_name, "margin": high[0] - low[0]})
    if not pairs:
        raise ValueError("No AI pairs exceeded the configured score margin")
    write_jsonl(output, pairs)
    write_json(output.with_suffix(".scores.json"), records)
    return pairs


def make_preprocess_manifest(candidate_file: Path, pairs_file: Path, output: Path) -> int:
    by_id = {r["id"]: r for r in candidates(candidate_file)}
    pairs = read_jsonl(pairs_file)
    used = {p[key] for p in pairs for key in ("chosen", "rejected")}
    if not used <= by_id.keys():
        raise ValueError(f"Unknown preference candidate IDs: {sorted(used - by_id.keys())}")
    samples = []
    for ident in sorted(used):
        row = by_id[ident]
        samples.append({"audio_path": row["audio_path"], "caption": row["caption"],
                        "lyrics": "[Instrumental]", "is_instrumental": True,
                        "duration": row["duration"], "bpm": row["bpm"],
                        "keyscale": row["keyscale"], "timesignature": row["timesignature"]})
    write_json(output, {"metadata": {"genre_ratio": 0}, "samples": samples})
    return len(samples)
