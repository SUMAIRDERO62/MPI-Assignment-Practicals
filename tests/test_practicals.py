"""Correctness tests for the standalone assignment practical helpers."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from practicals.common import (
    partition_counts,
    split_evenly,
    validate_matrix_pair,
    validate_multiplication,
)


ROOT = Path(__file__).parents[1]


def test_partition_counts_cover_uneven_workload() -> None:
    counts, displacements = partition_counts(10, 3)
    assert counts.tolist() == [4, 3, 3]
    assert displacements.tolist() == [0, 4, 7]
    assert sum(counts) == 10


def test_partition_counts_support_more_workers_than_values() -> None:
    counts, displacements = partition_counts(2, 4)
    assert counts.tolist() == [1, 1, 0, 0]
    assert displacements.tolist() == [0, 1, 2, 2]


def test_partition_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="length"):
        partition_counts(-1, 2)
    with pytest.raises(ValueError, match="workers"):
        partition_counts(1, 0)


def test_split_evenly_preserves_order() -> None:
    assert split_evenly(range(7), 3) == [[0, 1, 2], [3, 4], [5, 6]]


def test_matrix_validation_and_reference_results() -> None:
    left = np.arange(6).reshape(2, 3)
    right = np.ones((2, 3))
    assert validate_matrix_pair(left, right) == (2, 3)
    assert np.array_equal(left + right, np.array([[1, 2, 3], [4, 5, 6]]))
    assert validate_multiplication(left, np.ones((3, 4))) == (2, 3, 4)


@pytest.mark.parametrize(
    ("left", "right", "message"),
    [
        (np.ones((2, 3)), np.ones((3, 2)), "same shape"),
        (np.ones(3), np.ones((3, 1)), "two-dimensional"),
    ],
)
def test_matrix_addition_validation_rejects_invalid_dimensions(left, right, message) -> None:
    with pytest.raises(ValueError, match=message):
        validate_matrix_pair(left, right)


def test_matrix_multiplication_validation_rejects_invalid_dimensions() -> None:
    with pytest.raises(ValueError, match="left columns"):
        validate_multiplication(np.ones((2, 3)), np.ones((2, 2)))


@pytest.mark.parametrize(
    "script",
    [
        "practical_01_process_rank_size.py",
        "practical_02_send_receive.py",
        "practical_03_array_distribution.py",
        "practical_04_parallel_array_sum.py",
        "practical_05_parallel_matrix_addition.py",
        "practical_06_parallel_matrix_multiplication.py",
    ],
)
def test_practical_entrypoints_compile(script: str) -> None:
    source = ROOT / "practicals" / script
    subprocess.run([sys.executable, "-m", "py_compile", str(source)], check=True)


@pytest.mark.skipif(shutil.which("mpiexec") is None, reason="MPI integration requires mpiexec")
def test_practical_04_mpi_integration() -> None:
    result = subprocess.run(
        [
            "mpiexec",
            "-n",
            "2",
            sys.executable,
            str(ROOT / "practicals" / "practical_04_parallel_array_sum.py"),
            "--length",
            "11",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Verified: parallel and sequential sums match." in result.stdout
