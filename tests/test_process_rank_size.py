"""Tests for the reusable logic in MPI Practical 01."""

from __future__ import annotations

import importlib.util
from pathlib import Path


PRACTICAL_PATH = (
    Path(__file__).parents[1] / "practicals" / "01_process_rank_size.py"
)
SPEC = importlib.util.spec_from_file_location("process_rank_size", PRACTICAL_PATH)
assert SPEC is not None
assert SPEC.loader is not None
PRACTICAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRACTICAL)


def test_format_rank_message_includes_rank_and_process_count() -> None:
    assert PRACTICAL.format_rank_message(2, 4) == (
        "Process rank 2 of 4 total processes."
    )


def test_format_root_message_identifies_root_process() -> None:
    assert PRACTICAL.format_root_message() == "Rank 0 is the root process."
