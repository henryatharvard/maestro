from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import soundfile as sf
from pydantic import Field

from .config import ID_PATTERN, Config, StrictModel
from .io import digest, file_hash, read_jsonl, write_json


class Recording(StrictModel):
    id: str = Field(pattern=ID_PATTERN)
    composition_id: str = Field(pattern=ID_PATTERN)
    audio_path: str
    caption: str = Field(min_length=15)
    instruments: list[str] = Field(min_length=1)
    provenance: str = Field(min_length=10)
    bpm: int | None = Field(default=None, gt=0, le=300)
    keyscale: str = ""
    timesignature: str = ""


class Prompt(StrictModel):
    id: str = Field(pattern=ID_PATTERN)
    caption: str = Field(min_length=15)
    duration: float = Field(ge=10, le=180)
    bpm: int | None = Field(default=None, gt=0, le=300)
    keyscale: str = ""
    timesignature: str = ""


def audio_metrics(path: Path) -> dict:
    info = sf.info(path)
    peak, squares, count, clipped, active = 0.0, 0.0, 0, 0, 0
    with sf.SoundFile(path) as handle:
        for block in handle.blocks(blocksize=65536, dtype="float32", always_2d=True):
            if not np.isfinite(block).all():
                raise ValueError(f"Non-finite audio: {path}")
            magnitude = np.abs(block)
            peak = max(peak, float(magnitude.max(initial=0)))
            squares += float(np.square(block.astype(np.float64)).sum())
            count += block.size
            clipped += int((magnitude >= 0.999).sum())
            active += int((magnitude > 0.001).sum())
    return dict(duration=info.duration, sample_rate=info.samplerate, channels=info.channels,
                peak=peak, rms=math.sqrt(squares / max(count, 1)),
                clipping_fraction=clipped / max(count, 1),
                active_fraction=active / max(count, 1))


def load_prompts(root: Path, cfg: Config) -> dict[str, list[dict]]:
    sets = {}
    seen_ids, seen_captions = set(), set()
    for name in ("feedback", "eval"):
        path = root / getattr(cfg.generation, f"{name}_prompts")
        rows = [Prompt.model_validate(r).model_dump() for r in read_jsonl(path)]
        for row in rows:
            caption = " ".join(row["caption"].lower().split())
            if row["id"] in seen_ids or caption in seen_captions:
                raise ValueError("Feedback and evaluation need distinct IDs and captions")
            if row["duration"] > cfg.data.max_seconds:
                raise ValueError("Prompt duration exceeds preprocessing max_seconds")
            seen_ids.add(row["id"])
            seen_captions.add(caption)
        sets[name] = rows
    return sets


def validate_recordings(root: Path, cfg: Config) -> list[dict]:
    rows, ids, hashes = [], set(), set()
    for raw in read_jsonl(root / cfg.data.manifest):
        item = Recording.model_validate(raw)
        path = (root / item.audio_path).resolve()
        if path.suffix.lower() not in {".wav", ".flac"}:
            raise ValueError(f"Use lossless WAV or FLAC for this experiment: {path}")
        if not path.is_file():
            raise FileNotFoundError(f"Missing recording: {path}")
        sha = file_hash(path)
        if item.id in ids or sha in hashes:
            raise ValueError(f"Duplicate recording ID or audio content: {item.id}")
        metrics = audio_metrics(path)
        if not cfg.data.min_seconds <= metrics["duration"] <= cfg.data.max_seconds:
            raise ValueError(f"{item.id}: duration outside configured limits; cut explicitly")
        if metrics["channels"] not in (1, 2):
            raise ValueError(f"{item.id}: expected mono or stereo")
        if metrics["peak"] < 0.001 or metrics["clipping_fraction"] > 0.001:
            raise ValueError(f"{item.id}: silent/very quiet or clipped audio; inspect the take")
        rows.append({**item.model_dump(), "audio_path": str(path), "sha256": sha, **metrics})
        ids.add(item.id)
        hashes.add(sha)
    if len({r["composition_id"] for r in rows}) < 2:
        raise ValueError("Need at least two distinct compositions for a held-out split")
    return rows


def split_recordings(rows: list[dict], fraction: float, seed: int) -> dict[str, list[dict]]:
    groups = sorted({r["composition_id"] for r in rows}, key=lambda g: digest([seed, g]))
    count = min(len(groups) - 1, max(1, round(len(groups) * fraction)))
    validation = set(groups[:count])
    return {
        "train": [r for r in rows if r["composition_id"] not in validation],
        "validation": [r for r in rows if r["composition_id"] in validation],
    }


def ace_sample(row: dict, audio_path: Path | None = None) -> dict:
    return {
        "audio_path": str(audio_path or row["audio_path"]),
        "caption": row["caption"], "lyrics": "[Instrumental]", "is_instrumental": True,
        "duration": row["duration"], "bpm": row.get("bpm"),
        "keyscale": row.get("keyscale", ""), "timesignature": row.get("timesignature", ""),
    }


def prepare(root: Path, cfg: Config, output: Path) -> dict:
    rows = validate_recordings(root, cfg)
    prompts = load_prompts(root, cfg)
    fingerprint = digest({"recordings": rows, "config": cfg.model_dump(), "prompts": prompts})
    summary_file = output / "summary.json"
    if summary_file.is_file():
        import json

        old = json.loads(summary_file.read_text())
        if old.get("fingerprint") != fingerprint:
            raise ValueError("Prepared experiment inputs changed. Start a new exp-id.")
        return old
    splits = split_recordings(rows, cfg.data.validation_fraction, cfg.seed)
    # Stage uniquely named lossless copies: upstream caches by basename.
    # Keep audio unchanged, including channels, sample rate and expressive timing.
    import shutil

    staged = output / "audio"
    staged.mkdir(parents=True, exist_ok=True)
    for row in rows:
        path = staged / (row["id"] + Path(row["audio_path"]).suffix.lower())
        if not path.exists() or file_hash(path) != row["sha256"]:
            shutil.copyfile(row["audio_path"], path)
    for split, selected in splits.items():
        samples = [ace_sample(r, staged / (r["id"] + Path(r["audio_path"]).suffix.lower()))
                   for r in selected]
        write_json(output / f"{split}.json", {"metadata": {"genre_ratio": 0}, "samples": samples})
    write_json(output / "recordings.json", rows)
    write_json(output / "prompts.json", prompts)
    return {"recordings": len(rows), "train": len(splits["train"]),
            "validation": len(splits["validation"]), "dataset_sha256": digest(rows),
            "fingerprint": fingerprint}
