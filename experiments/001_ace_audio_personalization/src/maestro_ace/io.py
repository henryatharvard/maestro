from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}. See the experiment README and examples/.")
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not rows:
        raise ValueError(f"Empty input: {path}")
    return rows


def write_json(path: Path, value) -> None:
    atomic_text(path, json.dumps(value, indent=2, allow_nan=False) + "\n")


def write_jsonl(path: Path, rows) -> None:
    atomic_text(path, "".join(json.dumps(r, allow_nan=False) + "\n" for r in rows))


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as handle:
        temp = Path(handle.name)
        try:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        except BaseException:
            temp.unlink(missing_ok=True)
            raise
    temp.replace(path)
