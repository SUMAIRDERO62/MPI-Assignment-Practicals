"""Practical 03: distribute and gather an uneven one-dimensional array."""

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
    data = np.arange(1, args.length + 1, dtype=np.int32) if rank == 0 else None
    local = np.empty(int(counts[rank]), dtype=np.int32)
    comm.Scatterv([data, counts, displacements, MPI.INT], local, root=0)
    gathered = np.empty(args.length, dtype=np.int32) if rank == 0 else None
    comm.Gatherv(local, [gathered, counts, displacements, MPI.INT], root=0)

    print(f"Rank {rank} received {local.tolist()}")
    if rank == 0:
        if not np.array_equal(gathered, data):
            raise RuntimeError("gathered data did not match the original array")
        print(f"Gathered array: {gathered.tolist()}")


if __name__ == "__main__":
    main()
