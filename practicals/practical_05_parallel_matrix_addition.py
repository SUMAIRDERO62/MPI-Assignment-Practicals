"""Practical 05: add two matrices by distributing rows across MPI ranks."""

from __future__ import annotations

import argparse

import numpy as np
from mpi4py import MPI

try:
    from practicals.common import partition_counts, validate_matrix_pair
except ModuleNotFoundError:
    from common import partition_counts, validate_matrix_pair


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=5)
    parser.add_argument("--columns", type=int, default=3)
    args = parser.parse_args()
    if args.rows < 1 or args.columns < 1:
        parser.error("--rows and --columns must be positive")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    matrix_a = np.arange(args.rows * args.columns, dtype=np.float64).reshape(args.rows, args.columns) if rank == 0 else None
    matrix_b = np.ones((args.rows, args.columns), dtype=np.float64) if rank == 0 else None
    if rank == 0:
        validate_matrix_pair(matrix_a, matrix_b)
    counts, displacements = partition_counts(args.rows, size)
    row_count = int(counts[rank])
    send_counts = counts * args.columns
    send_displacements = displacements * args.columns
    local_a = np.empty((row_count, args.columns), dtype=np.float64)
    local_b = np.empty_like(local_a)
    comm.Scatterv([matrix_a, send_counts, send_displacements, MPI.DOUBLE], local_a, root=0)
    comm.Scatterv([matrix_b, send_counts, send_displacements, MPI.DOUBLE], local_b, root=0)
    local_result = local_a + local_b
    result = np.empty((args.rows, args.columns), dtype=np.float64) if rank == 0 else None
    comm.Gatherv(local_result, [result, send_counts, send_displacements, MPI.DOUBLE], root=0)

    if rank == 0:
        expected = matrix_a + matrix_b
        if not np.allclose(result, expected):
            raise RuntimeError("parallel matrix addition did not match the reference")
        print(f"Matrix shape: {args.rows}x{args.columns}")
        print(f"Result:\n{result}")
        print("Verified: parallel and sequential matrix addition match.")


if __name__ == "__main__":
    main()
