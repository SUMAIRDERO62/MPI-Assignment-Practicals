# Project summary

## Objectives

ParallelLab-MPI was developed to demonstrate and compare three execution
models for a deterministic CPU-bound workload: sequential Python, local
multiprocessing, and MPI processes. The project also establishes a repeatable
benchmarking and visualization workflow.

## Completed work

- Implemented the sum-of-squares workload and reusable balanced partitioning.
- Added a sequential reference implementation.
- Added multiprocessing workers using `multiprocessing.Pool`.
- Added MPI ranks using `mpi4py`, including barrier synchronization and
  reductions.
- Added result validation, repeated timing, CSV output, and chart generation.
- Added tests for correctness and partition coverage.
- Documented architecture, methodology, measured results, and limitations.

## Technologies

The project uses Python 3, `mpi4py`, Python's `multiprocessing` module,
Matplotlib, pandas, and pytest. Windows PowerShell commands and an MPI
launcher such as Microsoft MPI support local execution.

## Outcomes

The checked-in benchmark uses `n=5,000,000` and three repetitions. The best
recorded configuration is MPI with two workers at `0.697793 s`, with speedup
`1.224363` and efficiency `0.612181` relative to the sequential average of
`0.854352 s`. Four workers were slower than two workers for both MPI and
multiprocessing in this data set, demonstrating the effect of process and
coordination overhead on a small, communication-light workload.

These are observations from the recorded CSV, not universal performance
claims. Repeating the benchmark on another machine may produce different
results.

## Conclusion

The project provides a compact, reproducible comparison of process-based
parallel execution in Python. It shows how partitioning and aggregation can
preserve correctness while also showing that additional workers do not
guarantee better performance. Future evaluation should add larger workloads,
more repetitions, variability statistics, and explicit communication
measurements.
