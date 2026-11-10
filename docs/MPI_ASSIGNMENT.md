# MPI Assignment Practicals

This document records the introductory MPI practicals for this repository.

## Practical 01: Identify process rank and total number of processes

### Objective

Use `mpi4py` to identify each process's rank in `MPI.COMM_WORLD` and the total
number of processes participating in the run. Rank 0 is also identified as the
root process.

### MPI concepts

- **Communicator:** `MPI.COMM_WORLD` contains all processes launched for the
  program.
- **Rank:** `Get_rank()` returns the unique integer identifier of the calling
  process, starting at 0.
- **Size:** `Get_size()` returns the total number of processes in the
  communicator.
- **Root process:** Rank 0 is conventionally used as the root for coordination
  and reporting.

### Algorithm

1. Import `MPI` from `mpi4py`.
2. Select `MPI.COMM_WORLD`.
3. Call `Get_rank()` and `Get_size()` on the communicator.
4. Print the rank and total process count from every process.
5. If the rank is 0, print a message identifying the root process.

The process count is supplied by the MPI launcher; the Python code does not
hardcode it or read input.

### Windows Microsoft MPI execution

From the repository root, with Python and Microsoft MPI installed:

```powershell
mpiexec -n 4 python practicals\01_process_rank_size.py
```

The `-n 4` value is only a launcher choice for this example. Use any positive
process count supported by the local MPI installation.

If the virtual environment is not activated, use its interpreter explicitly:

```powershell
mpiexec -n 4 .venv\Scripts\python.exe practicals\01_process_rank_size.py
```

### Example output

MPI does not guarantee output ordering between processes, so the lines may
appear in a different order:

```text
Process rank 0 of 4 total processes.
Rank 0 is the root process.
Process rank 1 of 4 total processes.
Process rank 2 of 4 total processes.
Process rank 3 of 4 total processes.
```
