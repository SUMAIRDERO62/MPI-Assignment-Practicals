"""Shared helpers for the ParallelLab-MPI experiments."""

from __future__ import annotations

from typing import Tuple


def calculate_sum_of_squares(start: int, end: int) -> int:
    """Return the sum of squares for the inclusive range ``start`` through ``end``.

    An empty or reversed range contributes zero.  This makes the helper useful
    for ranks or workers that receive no values when there are more workers
    than input values.
    """
    if start > end:
        return 0
    return sum(value * value for value in range(start, end + 1))


def partition_range(n: int, rank: int, size: int) -> Tuple[int, int]:
    """Return a balanced, non-overlapping inclusive chunk of ``1..n``.

    The first ``n % size`` chunks receive one additional value.  Empty chunks
    are represented as ``(1, 0)`` when ``size`` is greater than ``n``.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if size <= 0:
        raise ValueError("size must be positive")
    if rank < 0 or rank >= size:
        raise ValueError("rank must be between 0 and size - 1")

    base, remainder = divmod(n, size)
    chunk_length = base + (1 if rank < remainder else 0)
    start = rank * base + min(rank, remainder) + 1
    end = start + chunk_length - 1
    return start, end
