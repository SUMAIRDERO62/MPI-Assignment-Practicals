"""MPI Practical 01: identify each process rank and the communicator size."""

from __future__ import annotations

from mpi4py import MPI


def format_rank_message(rank: int, process_count: int) -> str:
    """Return the shared message printed by every MPI process."""
    return f"Process rank {rank} of {process_count} total processes."


def format_root_message() -> str:
    """Return the message that identifies rank 0 as the root process."""
    return "Rank 0 is the root process."


def main() -> None:
    """Print rank information for every process in MPI.COMM_WORLD."""
    communicator = MPI.COMM_WORLD
    rank = communicator.Get_rank()
    process_count = communicator.Get_size()

    print(format_rank_message(rank, process_count), flush=True)
    if rank == 0:
        print(format_root_message(), flush=True)


if __name__ == "__main__":
    main()
