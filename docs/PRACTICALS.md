# Six MPI assignment practicals

All practicals are standalone Python entry points and use
`MPI.COMM_WORLD`. Run them from the repository root with a compatible
`mpiexec` and the same Python environment that contains `mpi4py`.

## 01 - Process rank and size

- **Objective:** identify each process and the root process.
- **Source:** `practicals/practical_01_process_rank_size.py`
- **Run:** `mpiexec -n 4 python practicals\practical_01_process_rank_size.py`
- **Viva:** `Get_rank()` identifies the current process; `Get_size()` returns the communicator size.

## 02 - Send and receive

- **Objective:** send a tagged message from rank 0 to rank 1.
- **Source:** `practicals/practical_02_send_receive.py`
- **Run:** `mpiexec -n 2 python practicals\practical_02_send_receive.py`
- **Viva:** point-to-point communication names a source, destination, and optional tag.

## 03 - Array distribution

- **Objective:** distribute and gather real array elements, including uneven chunks.
- **Source:** `practicals/practical_03_array_distribution.py`
- **Run:** `mpiexec -n 4 python practicals\practical_03_array_distribution.py --length 11`
- **Viva:** `Scatterv` supports a different element count for each rank; displacements are offsets into the root buffer.

## 04 - Parallel array sum

- **Objective:** calculate local sums and combine them with `MPI.SUM`.
- **Source:** `practicals/practical_04_parallel_array_sum.py`
- **Run:** `mpiexec -n 4 python practicals\practical_04_parallel_array_sum.py --length 11`
- **Viva:** `Reduce` returns the combined value to the selected root, while `Allreduce` would return it to every rank.

## 05 - Parallel matrix addition

- **Objective:** distribute rows and add corresponding elements.
- **Source:** `practicals/practical_05_parallel_matrix_addition.py`
- **Run:** `mpiexec -n 4 python practicals\practical_05_parallel_matrix_addition.py`
- **Viva:** row distribution keeps the algorithm simple and supports uneven row counts.

## 06 - Parallel matrix multiplication

- **Objective:** distribute rows of A, broadcast B, and gather result rows.
- **Source:** `practicals/practical_06_parallel_matrix_multiplication.py`
- **Run:** `mpiexec -n 4 python practicals\practical_06_parallel_matrix_multiplication.py`
- **Viva:** every rank needs matrix B, so `Bcast` avoids sending a separate copy to each rank.

Every matrix practical validates its dimensions and compares the gathered result
with NumPy's sequential reference calculation.
