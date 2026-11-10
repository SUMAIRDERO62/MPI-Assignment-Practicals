# MPI Assignment Practicals

## Project purpose

This repository presents six practical exercises in parallel programming with the Message Passing Interface (MPI), using Python and `mpi4py`. The practicals move from identifying MPI processes to point-to-point communication, collective array operations, and distributed matrix computation.

Run every command from the repository root with an MPI launcher compatible with the installed `mpi4py`.

## Environment setup

Follow [INSTALLATION.md](INSTALLATION.md) to create a Python environment, install requirements, and verify the MPI runtime. On Windows with Microsoft MPI, use the installed Microsoft MPI `mpiexec.exe` and the Python interpreter that imports the matching `mpi4py`.

Quick runtime check:

```powershell
mpiexec -n 4 python -c "from mpi4py import MPI; c=MPI.COMM_WORLD; print(f'Rank {c.Get_rank()} of {c.Get_size()}')"
```

## Practical 01: Identify process rank and total number of processes

**Objective:** Identify each process in `MPI.COMM_WORLD` and print the communicator size.

**Source:** `practicals/practical_01_process_rank_size.py`

**Run:**

```powershell
mpiexec -n 4 python practicals\practical_01_process_rank_size.py
```

**Key ideas:**
- `MPI.COMM_WORLD` is the communicator containing the launched processes.
- `Get_rank()` returns the calling process's rank, numbered from zero.
- `Get_size()` returns the number of processes in the communicator.
- Rank zero is conventionally used as the root for coordination and reporting.

**Expected behavior:** Four rank messages for a four-process launch, plus a root message from rank zero. MPI does not guarantee print order.

## Practical 02: Point-to-point send and receive

**Objective:** Send a tagged message from rank 0 to rank 1.

**Source:** `practicals/practical_02_send_receive.py`

**Run:**

```powershell
mpiexec -n 2 python practicals\practical_02_send_receive.py
```

**Key ideas:** Rank 0 sends a Python object using `comm.send()`; rank 1 receives it using `comm.recv()`. The source, destination, and tag identify the message. At least two ranks are required.

## Practical 03: Distribute and gather an array

**Objective:** Distribute array elements among ranks and reconstruct the original array, including uneven partitions.

**Source:** `practicals/practical_03_array_distribution.py`

**Run:**

```powershell
mpiexec -n 4 python practicals\practical_03_array_distribution.py --length 11
```

**Key ideas:** `Scatterv` supports per-rank element counts and displacements; `Gatherv` collects variable-sized chunks back at the root. With 11 elements and four ranks, the partition is intentionally uneven.

## Practical 04: Parallel array sum

**Objective:** Calculate a local sum on each rank and combine the partial sums at the root.

**Source:** `practicals/practical_04_parallel_array_sum.py`

**Run:**

```powershell
mpiexec -n 4 python practicals\practical_04_parallel_array_sum.py --length 11
```

**Key ideas:** The root distributes values with `Scatterv`; each process computes its local sum; `comm.reduce(..., op=MPI.SUM, root=0)` combines the partial values. The root checks the result against a sequential NumPy sum.

## Practical 05: Parallel matrix addition

**Objective:** Add two matrices by distributing rows among ranks.

**Source:** `practicals/practical_05_parallel_matrix_addition.py`

**Run:**

```powershell
mpiexec -n 4 python practicals\practical_05_parallel_matrix_addition.py
```

Optional dimensions:

```powershell
mpiexec -n 4 python practicals\practical_05_parallel_matrix_addition.py --rows 7 --columns 3
```

**Key ideas:** Matrix rows are partitioned across processes; each rank adds its local rows; the root gathers the result and validates it against NumPy's sequential matrix addition.

## Practical 06: Parallel matrix multiplication

**Objective:** Multiply matrices by distributing rows of matrix A while making matrix B available to all ranks.

**Source:** `practicals/practical_06_parallel_matrix_multiplication.py`

**Run:**

```powershell
mpiexec -n 4 python practicals\practical_06_parallel_matrix_multiplication.py
```

Optional dimensions:

```powershell
mpiexec -n 4 python practicals\practical_06_parallel_matrix_multiplication.py --rows-a 5 --shared 3 --columns-b 4
```

**Key ideas:** The root broadcasts matrix B using `Bcast`; rows of A are distributed; each rank computes its local product; the root gathers the result and compares it with NumPy's matrix multiplication.

## Additional MPI concepts

The six practicals directly demonstrate rank/size, point-to-point communication, `Scatterv`, `Gatherv`, `Reduce`, and `Bcast`. Related concepts worth discussing in a viva:

- **Broadcast (`Bcast`):** distribute the same data from one root to every rank.
- **Scatter / Scatterv:** distribute equal-sized or variable-sized portions from a root.
- **Gather / Gatherv:** collect equal-sized or variable-sized portions at a root.
- **Reduce:** combine values across ranks and return the result to a root.
- **Allreduce:** combine values and make the result available to every rank.
- **Barrier:** synchronize ranks at a point in the program.
- **Point-to-point:** communicate between explicitly selected sender and receiver ranks.

These additional concepts are explanatory context; a concept is not necessarily a separate standalone practical in this repository.

## Viva preparation

1. What is an MPI communicator?
2. What is the difference between rank and size?
3. Why is rank zero often selected as root?
4. What do source, destination, and tag mean in point-to-point communication?
5. Why is `Scatterv` useful when the array length is not divisible by the process count?
6. What is the role of displacements in `Scatterv` and `Gatherv`?
7. How does `Reduce` differ from `Gather`?
8. How does `Allreduce` differ from `Reduce`?
9. Why does matrix multiplication broadcast matrix B?
10. Why might a parallel program be slower than its sequential version for a small workload?

## Browser learning material

The static dashboard in `web/public/index.html` contains educational explanations and browser-side visualizations. These are teaching aids, not a browser-hosted MPI runtime. The teacher presentation is available at `web/public/presentation.html`; see [PROJECT_PRESENTATION.md](PROJECT_PRESENTATION.md).

## Test the code

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m pytest -v
```

The automated suite includes helper tests, practical entry-point compilation, and an MPI integration test when `mpiexec` is available. For a complete demonstration, run each of the six commands above on a machine with a working MPI installation.
