"""Practical 06: multiply matrices by distributing rows of A across MPI ranks."""

from __future__ import annotations

import argparse

import numpy as np
from mpi4py import MPI

try:
    from practicals.common import partition_counts, validate_multiplication
except ModuleNotFoundError:
    from common import partition_counts, validate_multiplication


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows-a", type=int, default=4)
    parser.add_argument("--shared", type=int, default=3)
    parser.add_argument("--columns-b", type=int, default=2)
    args = parser.parse_args()
    if min(args.rows_a, args.shared, args.columns_b) < 1:
        parser.error("matrix dimensions must be positive")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    matrix_a = np.arange(args.rows_a * args.shared, dtype=np.float64).reshape(args.rows_a, args.shared) if rank == 0 else None
    matrix_b = np.arange(args.shared * args.columns_b, dtype=np.float64).reshape(args.shared, args.columns_b) if rank == 0 else np.empty((args.shared, args.columns_b), dtype=np.float64)
    if rank == 0:
        validate_multiplication(matrix_a, matrix_b)
    comm.Bcast(matrix_b, root=0)
    counts, displacements = partition_counts(args.rows_a, size)
    send_counts = counts * args.shared
    send_displacements = displacements * args.shared
    local_a = np.empty((int(counts[rank]), args.shared), dtype=np.float64)
    comm.Scatterv([matrix_a, send_counts, send_displacements, MPI.DOUBLE], local_a, root=0)
    local_result = local_a @ matrix_b
    result = np.empty((args.rows_a, args.columns_b), dtype=np.float64) if rank == 0 else None
    result_counts = counts * args.columns_b
    result_displacements = displacements * args.columns_b
    comm.Gatherv(local_result, [result, result_counts, result_displacements, MPI.DOUBLE], root=0)

    if rank == 0:
        expected = matrix_a @ matrix_b
        if not np.allclose(result, expected):
            raise RuntimeError("parallel matrix multiplication did not match the reference")
        print(f"A: {args.rows_a}x{args.shared}, B: {args.shared}x{args.columns_b}")
        print(f"Result:\n{result}")
        print("Verified: parallel and sequential matrix multiplication match.")


if __name__ == "__main__":
    main()
