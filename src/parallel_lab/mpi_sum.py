"""MPI implementation of the sum-of-squares workload."""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from mpi4py import MPI

from parallel_lab.common import calculate_sum_of_squares, partition_range


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=5_000_000, help="upper bound of the workload")
    parser.add_argument("--json", action="store_true", help="also emit a JSON result record")
    args = parser.parse_args(argv)
    if args.n < 1:
        parser.error("--n must be a positive integer")
    return args


def main(argv: Sequence[str] | None = None) -> None:
    """Run the workload across all processes in ``MPI.COMM_WORLD``."""
    args = parse_args(argv)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    start, end = partition_range(args.n, rank, size)
    comm.Barrier()
    start_time = MPI.Wtime()
    local_sum = calculate_sum_of_squares(start, end)
    local_elapsed = MPI.Wtime() - start_time
    total = comm.reduce(local_sum, op=MPI.SUM, root=0)
    elapsed = comm.reduce(local_elapsed, op=MPI.MAX, root=0)

    if rank == 0:
        print(f"Result: {total}")
        print(f"Processes: {size}")
        print(f"Execution time: {elapsed:.6f} seconds")
        if args.json:
            print(json.dumps({
                "implementation": "mpi",
                "n": args.n,
                "workers": size,
                "result": total,
                "execution_time": elapsed,
            }))


if __name__ == "__main__":
    main()
