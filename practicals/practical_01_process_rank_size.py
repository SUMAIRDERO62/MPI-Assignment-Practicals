"""Practical 01: identify an MPI process rank and communicator size."""

from __future__ import annotations

import argparse

from mpi4py import MPI


def format_rank_message(rank: int, process_count: int) -> str:
    """Return a beginner-friendly message for one MPI rank."""
    return f"Process rank {rank} of {process_count} total processes."


def format_root_message() -> str:
    """Return the message identifying rank zero as the root."""
    return "Rank 0 is the root process."


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print(format_rank_message(rank, size), flush=True)
    if rank == 0:
        print(format_root_message(), flush=True)


if __name__ == "__main__":
    main()
