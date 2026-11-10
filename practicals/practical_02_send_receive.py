"""Practical 02: send a point-to-point message from rank 0 to rank 1."""

from __future__ import annotations

import argparse

from mpi4py import MPI


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if size < 2:
        if rank == 0:
            print("Practical 02 requires at least 2 MPI processes.")
        return

    if rank == 0:
        message = {"from": 0, "text": "Hello from rank 0"}
        comm.send(message, dest=1, tag=10)
        print("Rank 0 sent a message to rank 1.")
    elif rank == 1:
        message = comm.recv(source=0, tag=10)
        if message != {"from": 0, "text": "Hello from rank 0"}:
            raise RuntimeError("rank 1 received an unexpected message")
        print(f"Rank 1 received: {message['text']}")


if __name__ == "__main__":
    main()

