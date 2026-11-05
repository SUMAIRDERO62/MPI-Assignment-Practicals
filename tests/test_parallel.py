"""Tests for shared and parallel sum-of-squares implementations."""

from __future__ import annotations

from parallel_lab.common import calculate_sum_of_squares, partition_range
from parallel_lab.multiprocessing_sum import run
from parallel_lab.sequential import calculate_sum_of_squares as sequential_sum


def test_sum_of_squares_small_input() -> None:
    assert calculate_sum_of_squares(1, 5) == 55


def test_partition_covers_all_values_without_overlap() -> None:
    n = 23
    chunks = [partition_range(n, rank, 4) for rank in range(4)]
    values = [value for start, end in chunks for value in range(start, end + 1)]
    assert values == list(range(1, n + 1))


def test_partition_handles_uneven_division() -> None:
    chunks = [partition_range(10, rank, 3) for rank in range(3)]
    assert chunks == [(1, 4), (5, 7), (8, 10)]


def test_multiprocessing_matches_sequential() -> None:
    result, _ = run(1_000, 2)
    assert result == sequential_sum(1_000)
