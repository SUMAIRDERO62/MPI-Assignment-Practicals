"""MPI smoke-test entry point used by local and CI diagnostics."""

from mpi4py import MPI


def main() -> None:
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print(f"Hello from Process {rank} out of {size} processes", flush=True)


if __name__ == "__main__":
    main()
