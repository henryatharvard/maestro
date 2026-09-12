from pathlib import Path

import pytest

pytest.importorskip("torch")

from maestro_ace.config import load_config  # noqa: E402
from maestro_ace.smoke import run_smoke  # noqa: E402


def test_complete_synthetic_pipeline():
    root = Path(__file__).resolve().parents[1]
    result = run_smoke(load_config(root / "configs/piano_violin.toml"))
    assert result["status"] == "passed"
    assert result["matched_eval_cases"] == 2
