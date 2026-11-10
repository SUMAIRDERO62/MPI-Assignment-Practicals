"""Small, reusable helpers for the six MPI practicals."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def partition_counts(length: int, workers: int) -> tuple[np.ndarray, np.ndarray]:
    """Return element counts and displacements for an uneven Scatterv/Gatherv."""
    if length < 0:
        raise ValueError("length must be non-negative")
    if workers < 1:
        raise ValueError("workers must be positive")
    base, remainder = divmod(length, workers)
    counts = np.asarray(
        [base + (1 if rank < remainder else 0) for rank in range(workers)],
        dtype=np.int32,
    )
    displacements = np.zeros(workers, dtype=np.int32)
    if workers > 1:
        displacements[1:] = np.cumsum(counts[:-1])
    return counts, displacements


def split_evenly(values: Iterable[object], workers: int) -> list[list[object]]:
    """Return balanced Python lists, including empty lists when needed."""
    items = list(values)
    counts, _ = partition_counts(len(items), workers)
    result: list[list[object]] = []
    offset = 0
    for count in counts.tolist():
        result.append(items[offset : offset + count])
        offset += count
    return result


def validate_matrix_pair(left: np.ndarray, right: np.ndarray) -> tuple[int, int]:
    """Validate two matrices for element-wise addition and return their shape."""
    if left.ndim != 2 or right.ndim != 2:
        raise ValueError("both matrices must be two-dimensional")
    if left.shape != right.shape:
        raise ValueError("matrices must have the same shape")
    return left.shape


def validate_multiplication(left: np.ndarray, right: np.ndarray) -> tuple[int, int, int]:
    """Validate matrix multiplication dimensions and return ``(m, k, n)``."""
    if left.ndim != 2 or right.ndim != 2:
        raise ValueError("both matrices must be two-dimensional")
    if left.shape[1] != right.shape[0]:
        raise ValueError("left columns must equal right rows")
    return left.shape[0], left.shape[1], right.shape[1]

