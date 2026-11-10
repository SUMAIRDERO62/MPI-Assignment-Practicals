"""Practical 01: identify an MPI process rank and communicator size."""

from __future__ import annotations

import argparse

from mpi4py import MPI


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print(f"Hello from rank {rank} of {size} processes.")
    if rank == 0:
        print(f"Root rank: 0 | Total processes: {size}")


if __name__ == "__main__":
    main()

