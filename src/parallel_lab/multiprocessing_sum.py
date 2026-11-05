"""Multiprocessing implementation of the sum-of-squares workload."""

from __future__ import annotations

import argparse
import multiprocessing
import time
from typing import Sequence, Tuple

from parallel_lab.common import calculate_sum_of_squares, partition_range


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=5_000_000, help="upper bound of the workload")
    parser.add_argument(
        "--processes", type=int, default=multiprocessing.cpu_count(),
        help="number of worker processes",
    )
    args = parser.parse_args(argv)
    if args.n < 1:
        parser.error("--n must be a positive integer")
    if args.processes < 1:
        parser.error("--processes must be a positive integer")
    return args


def run(n: int, processes: int) -> Tuple[int, float]:
    """Calculate ``1² + ... + n²`` and return ``(result, elapsed_seconds)``."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    if processes < 1:
        raise ValueError("processes must be a positive integer")

    chunks = [partition_range(n, rank, processes) for rank in range(processes)]
    start_time = time.perf_counter()
    with multiprocessing.Pool(processes=processes) as pool:
        partial_sums = pool.starmap(calculate_sum_of_squares, chunks)
    return sum(partial_sums), time.perf_counter() - start_time


def main(argv: Sequence[str] | None = None) -> None:
    """Run and report the multiprocessing workload."""
    args = parse_args(argv)
    result, elapsed = run(args.n, args.processes)
    print(f"Result: {result}")
    print(f"Workers: {args.processes}")
    print(f"Execution time: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()
