# Teacher presentation guide

## Start the presentation

From the repository root, run a static server:

```powershell
python -m http.server 8000 --directory web\public
```

Open `http://localhost:8000/presentation.html`. Use **Next**, **Previous**, the arrow keys, or the space bar. **Full screen** starts browser presentation mode.

## Suggested practical-first sequence

1. Introduce the assignment goal and explain what MPI adds to parallel computing.
2. Show the project structure and the six practical source files.
3. Run Practical 01 with four ranks; identify rank and communicator size.
4. Run Practical 02 with two ranks; trace the sender, receiver, and message tag.
5. Run Practical 03 with 11 elements and four ranks; explain uneven distribution and reconstruction.
6. Run Practical 04; compare the Reduce result with the sequential check.
7. Run Practical 05; explain distributing rows and gathering the matrix sum.
8. Run Practical 06; explain why B is broadcast and rows of A are distributed.
9. Use the dashboard visualizer to discuss communication patterns. Clarify that it is a browser simulation.
10. Open benchmark charts and explain what the measured results do—and do not—show.
11. Run the test suite and finish with limitations and viva questions.

## Commands to demonstrate

Run from the repository root:

```powershell
mpiexec -n 4 python practicals\practical_01_process_rank_size.py
mpiexec -n 2 python practicals\practical_02_send_receive.py
mpiexec -n 4 python practicals\practical_03_array_distribution.py --length 11
mpiexec -n 4 python practicals\practical_04_parallel_array_sum.py --length 11
mpiexec -n 4 python practicals\practical_05_parallel_matrix_addition.py
mpiexec -n 4 python practicals\practical_06_parallel_matrix_multiplication.py
```

Before presenting, run these commands on the actual demonstration computer and capture its output. MPI output order may vary. Do not treat documentation sample output as proof that the current machine has executed the commands.

## Teacher talking points

- **Rank and size:** rank identifies one process within a communicator; size is the total number of communicator processes.
- **Point-to-point:** sender and receiver identify endpoints; tags distinguish message types.
- **Scatterv/Gatherv:** variable counts and displacements support uneven chunks.
- **Reduce:** combines partial values at a root; Allreduce makes the result available to all ranks.
- **Matrix addition:** each process adds its assigned rows.
- **Matrix multiplication:** every rank needs matrix B, while only a subset of A's rows is assigned to each rank.
- **Performance:** startup, synchronization, communication, and workload size influence whether parallelism helps.

## Viva prompts

1. What does `MPI.COMM_WORLD` represent?
2. Why does rank numbering begin at zero?
3. What happens if the number of array elements is not divisible by the number of ranks?
4. What is the difference between Gather and Reduce?
5. Why is matrix B broadcast in Practical 06?
6. What is the difference between MPI and Python multiprocessing?
7. Why can a parallel solution be slower for a small input?
8. Does the dashboard visualizer launch real MPI processes? (No; it is an educational browser simulation.)

## Local quality checks

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m pytest -v
```

The test suite includes an MPI integration check when `mpiexec` is available. Run all six practical commands above on the presentation machine to confirm its MPI runtime and environment before the teacher demonstration.
