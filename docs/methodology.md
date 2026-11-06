# Methodology

## Workload

Each implementation computes:

```text
1^2 + 2^2 + ... + n^2
```

The checked-in benchmark uses `n=5,000,000`. Every row reports the same
validated result, `41666679166667500000`.

## Partitioning

The inclusive range `1..n` is divided into balanced, non-overlapping chunks.
For `size` workers, each chunk receives `n // size` values and the first
`n % size` chunks receive one additional value. Empty chunks are represented
as `(1, 0)` and contribute zero.

MPI maps chunks to ranks. Multiprocessing maps chunks to pool workers. The
sequential implementation processes the complete range in one process.

## Repetitions and timing

The benchmark defaults to three repetitions for each implementation and worker
count. It records the arithmetic mean in
`results/benchmark_results.csv`.

The timing boundaries are:

- **Sequential:** calculation of the complete sum.
- **Multiprocessing:** pool creation, task execution, result collection, and
  pool cleanup.
- **MPI:** local computation after `MPI.COMM_WORLD` synchronization, with the
  maximum local elapsed time reported by rank 0. MPI launch and process startup
  are not included.

The benchmark checks that repeated runs and all implementations return the
same integer result before writing the CSV.

## Analysis engine

`src/parallel_lab/analysis.py` loads and validates the raw CSV, then writes
`results/performance_analysis.csv`. It rejects missing columns, malformed
types, unsupported implementation names, duplicate implementation/worker
rows, non-positive values, missing one-worker baselines, and inconsistent
workload metadata.

The engine uses two baselines:

```text
sequential_baseline_speedup = sequential_time / current_time
sequential_baseline_efficiency = sequential_baseline_speedup / workers

implementation_relative_speedup = implementation_one_worker_time / current_time
implementation_relative_efficiency = implementation_relative_speedup / workers
```

Worker scalability uses implementation-relative speedup for multiprocessing
and MPI. The MPI-versus-multiprocessing comparison uses matching worker counts
and reports the ratio of multiprocessing time to MPI time. These metrics
describe the recorded execution paths; they do not establish universal
hardware-independent performance.

## Visualization methodology

`src/parallel_lab/visualization.py` validates the analysis CSV, sorts worker
counts numerically, and generates five PNG charts:

- Execution time comparison
- Speedup comparison
- Parallel efficiency comparison
- Scalability comparison with ideal linear scaling
- MPI versus multiprocessing comparison

The module also preserves the two legacy chart filenames. All charts use the
actual CSV measurements and are written to a configurable output directory.

## Measurement limitations

The checked-in CSV is one measurement set, not a hardware-independent claim.
Timings can vary with CPU load, operating-system scheduling, Python and MPI
versions, process affinity, and background activity. Three repetitions provide
limited information about variance and do not support confidence intervals.

Process startup, worker-pool construction, synchronization, inter-process
communication, result transfer, and MPI reduction can dominate this
communication-light workload. MPI and multiprocessing also use different
timing boundaries, so their values should be interpreted as measurements of
the implemented execution paths.

The current methodology does not include warm-up runs, multiple input-size
sweeps, standard deviations, confidence intervals, or explicit communication
profiling. These are appropriate future improvements.
