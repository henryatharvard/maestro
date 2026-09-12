import json
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from maestro_ace.config import ROOT, load_config
from maestro_ace.data import load_prompts, prepare, split_recordings, validate_recordings
from maestro_ace.io import write_json
from maestro_ace.preferences import make_human_pairs, make_preprocess_manifest
from maestro_ace.report import report


def _setup(tmp_path: Path):
    cfg = load_config(ROOT / "configs/piano_violin.toml")
    (tmp_path / "data/audio").mkdir(parents=True)
    (tmp_path / "prompts").mkdir()
    for name in ("feedback", "eval"):
        target = tmp_path / f"prompts/{name}.jsonl"
        target.write_text((ROOT / f"prompts/{name}.jsonl").read_text())
    rows = []
    sample_rate = 8000
    t = np.arange(sample_rate * 11) / sample_rate
    for ident, group, freq in (("a-piano", "a", 220), ("a-duet", "a", 330),
                                ("b-violin", "b", 440)):
        path = tmp_path / f"data/audio/{ident}.wav"
        sf.write(path, 0.15 * np.sin(2 * np.pi * freq * t), sample_rate)
        rows.append({"id": ident, "composition_id": group,
                     "audio_path": f"data/audio/{ident}.wav",
                     "caption": f"Original instrumental performance with {ident} melody and accompaniment.",
                     "instruments": ["piano"], "provenance": "Original performance by the composer."})
    manifest = tmp_path / cfg.data.manifest
    manifest.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return cfg


def test_prepare_keeps_all_stems_of_composition_together(tmp_path):
    cfg = _setup(tmp_path)
    result = prepare(tmp_path, cfg, tmp_path / "artifacts/prepared")
    assert result["train"] + result["validation"] == 3
    prepared = tmp_path / "artifacts/prepared"
    train = json.loads((prepared / "train.json").read_text())["samples"]
    validation = json.loads((prepared / "validation.json").read_text())["samples"]
    assert {Path(s["audio_path"]).name for s in train}.isdisjoint(
        {Path(s["audio_path"]).name for s in validation})
    split = split_recordings(validate_recordings(tmp_path, cfg), 0.5, cfg.seed)
    assert len({r["composition_id"] for r in split["train"]}) == 1
    assert len({r["composition_id"] for r in split["validation"]}) == 1
    assert all(s["lyrics"] == "[Instrumental]" for s in train + validation)
    assert len(load_prompts(tmp_path, cfg)["eval"]) == 3
    write_json(prepared / "summary.json", result)
    assert prepare(tmp_path, cfg, prepared) == result
    manifest = tmp_path / cfg.data.manifest
    changed = manifest.read_text().replace("flowing", "lively")
    if changed == manifest.read_text():
        changed = manifest.read_text().replace("melody", "theme")
    manifest.write_text(changed)
    with pytest.raises(ValueError, match="inputs changed"):
        prepare(tmp_path, cfg, prepared)


def test_duplicate_audio_rejected(tmp_path):
    cfg = _setup(tmp_path)
    path = tmp_path / "data/audio/b-violin.wav"
    path.write_bytes((tmp_path / "data/audio/a-piano.wav").read_bytes())
    with pytest.raises(ValueError, match="Duplicate recording"):
        validate_recordings(tmp_path, cfg)


def test_human_preferences_reject_cross_prompt_and_keep_provenance(tmp_path):
    _setup(tmp_path)
    rows = [
        {"id": "p-1", "prompt_id": "p", "stage": "sft",
         "audio_path": str(tmp_path / "data/audio/a-piano.wav"),
         "caption": "A clear piano instrumental", "duration": 11, "bpm": 80,
         "keyscale": "C major", "timesignature": "4"},
        {"id": "p-2", "prompt_id": "p", "stage": "sft",
         "audio_path": str(tmp_path / "data/audio/a-duet.wav"),
         "caption": "A clear piano instrumental", "duration": 11, "bpm": 80,
         "keyscale": "C major", "timesignature": "4"},
    ]
    candidate_file = tmp_path / "candidates.jsonl"
    candidate_file.write_text("".join(json.dumps(r) + "\n" for r in rows))
    ballot_file = tmp_path / "ballots.jsonl"
    ballot_file.write_text(json.dumps({"prompt_id": "p", "chosen": "p-1",
                                       "rejected": "p-2", "reviewer": "Henry",
                                       "reason": "Better phrase ending"}) + "\n")
    pairs_file = tmp_path / "pairs.jsonl"
    pairs = make_human_pairs(candidate_file, ballot_file, pairs_file)
    assert pairs[0]["source"] == "human"
    assert make_preprocess_manifest(candidate_file, pairs_file, tmp_path / "ace.json") == 2
    assert len(json.loads((tmp_path / "ace.json").read_text())["samples"]) == 2
    rows[1]["prompt_id"] = "other"
    candidate_file.write_text("".join(json.dumps(r) + "\n" for r in rows))
    with pytest.raises(ValueError, match="share"):
        make_human_pairs(candidate_file, ballot_file, pairs_file)


def test_report_hides_checkpoint_labels_in_listening_index(tmp_path):
    cfg = _setup(tmp_path)
    artifacts = tmp_path / "artifacts"
    for stage in ("base", "sft"):
        folder = artifacts / "generations/eval" / stage
        folder.mkdir(parents=True)
        (folder / "eval-piano-101.flac").write_bytes(b"test audio " + stage.encode())
    summary = report(tmp_path, cfg, artifacts)
    assert summary["complete_base_sft_pairs"] == 1
    index = (artifacts / "reports/eval_listening.jsonl").read_text()
    assert "take-A.flac" in index and "take-B.flac" in index
    assert "generations/eval/base" not in index
    answer_key = json.loads((artifacts / "reports/answer_key.json").read_text())
    assert set(answer_key[0]["take_to_stage"].values()) == {"base", "sft"}
