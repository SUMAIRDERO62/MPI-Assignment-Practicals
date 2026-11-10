"""Practical 04: distribute an array and reduce local sums to the root."""

from __future__ import annotations

import argparse

import numpy as np
from mpi4py import MPI

try:
    from practicals.common import partition_counts
except ModuleNotFoundError:
    from common import partition_counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=int, default=10)
    args = parser.parse_args()
    if args.length < 1:
        parser.error("--length must be positive")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    counts, displacements = partition_counts(args.length, size)
    data = np.arange(1, args.length + 1, dtype=np.int64) if rank == 0 else None
    local = np.empty(int(counts[rank]), dtype=np.int64)
    comm.Scatterv([data, counts, displacements, MPI.LONG_LONG], local, root=0)
    local_sum = np.sum(local, dtype=np.int64)
    total = comm.reduce(int(local_sum), op=MPI.SUM, root=0)

    print(f"Rank {rank} local sum: {int(local_sum)}")
    if rank == 0:
        expected = int(np.sum(data, dtype=np.int64))
        if total != expected:
            raise RuntimeError(f"reduced sum {total} did not match {expected}")
        print(f"Parallel sum: {total}")
        print(f"Sequential check: {expected}")
        print("Verified: parallel and sequential sums match.")


if __name__ == "__main__":
    main()
