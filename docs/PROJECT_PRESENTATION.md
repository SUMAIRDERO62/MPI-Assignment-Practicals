# Teacher presentation guide

Open [`web/public/presentation.html`](../web/public/presentation.html) in a
static server for a focused teacher demonstration:

```powershell
python -m http.server 8000 --directory web\public
```

Then open `http://localhost:8000/presentation.html`. Use **Next**, **Previous**,
the arrow keys, or the space bar. **Full screen** starts browser presentation
mode.

## Suggested live sequence

1. Introduce the problem: one deterministic workload, three execution models.
2. Show the architecture and explain that the browser dashboard is static.
3. Run Practical 01 with 2 or 4 ranks.
4. Run Practical 02 with 2 ranks and point out the source and destination.
5. Run Practical 03 with length 11 and 4 ranks to make uneven chunks visible.
6. Run Practical 04 and compare the Reduce result with the sequential check.
7. Run Practical 05 and inspect the validated matrix result.
8. Run Practical 06 and explain why matrix B is broadcast.
9. Use the dashboard visualizer to contrast collective and point-to-point flows.
10. Open the benchmark charts and explain measured speedup and efficiency.
11. Finish with the test command and the limitations of small CPU workloads.

## Practical commands

```powershell
mpiexec -n 4 python practicals\practical_01_process_rank_size.py
mpiexec -n 2 python practicals\practical_02_send_receive.py
mpiexec -n 4 python practicals\practical_03_array_distribution.py --length 11
mpiexec -n 4 python practicals\practical_04_parallel_array_sum.py --length 11
mpiexec -n 4 python practicals\practical_05_parallel_matrix_addition.py
mpiexec -n 4 python practicals\practical_06_parallel_matrix_multiplication.py
```

The presentation records verified sample output from the local MPI runs. The
dashboard visualizer is explicitly a simulation; it never claims to launch
MPI processes in the browser.

## Viva prompts

- **Why is rank 0 special?** It is a conventional root for coordination and
  reporting; MPI does not make rank 0 inherently faster.
- **Why use Scatterv instead of Scatter?** The workload may not divide evenly,
  so each rank can receive a different count.
- **What is the difference between Gather and Reduce?** Gather collects
  separate values; Reduce combines values with an operation such as `SUM`.
- **Why broadcast matrix B?** Every rank needs B to multiply its assigned rows
  of A.
- **Why can parallel execution be slower?** Startup, synchronization, data
  movement, and communication overhead can exceed the computation.
