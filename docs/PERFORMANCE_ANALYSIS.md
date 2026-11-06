# Performance analysis

The analysis engine is implemented in
[src/parallel_lab/analysis.py](../src/parallel_lab/analysis.py).

## Inputs and outputs

Input:

- [results/benchmark_results.csv](../results/benchmark_results.csv)

Output:

- [results/performance_analysis.csv](../results/performance_analysis.csv)

The raw benchmark CSV is never used as an output target by the analysis
engine. Output paths are configurable for tests and experiments.

## Validation

The loader rejects:

- Missing required columns.
- Malformed integer or timing values.
- Non-positive `n`, repetitions, workers, or timings.
- Unsupported implementation names.
- Duplicate implementation/worker combinations.
- Missing sequential or parallel one-worker baselines.
- Inconsistent workload metadata or results.

## Metrics

For a current configuration with time `T_current` and worker count `P`:

```text
sequential_baseline_speedup =
    sequential_time / T_current

sequential_baseline_efficiency =
    sequential_baseline_speedup / P
```

For each parallel implementation:

```text
implementation_relative_speedup =
    implementation_one_worker_time / T_current

implementation_relative_efficiency =
    implementation_relative_speedup / P
```

The implementation-relative baseline is the one-worker row for the same
implementation. One-worker relative speedup and efficiency are therefore
`1.0`.

MPI and multiprocessing comparisons use matching worker counts:

```text
mpi_vs_multiprocessing_speedup =
    multiprocessing_time / mpi_time
```

This ratio describes the recorded execution paths and is not a
hardware-independent claim.

## Current checked-in measurements

The raw CSV uses `n=5,000,000` and three repetitions. All rows return
`41666679166667500000`.

| Implementation | Workers | Average time (s) | Relative speedup | Relative efficiency |
|---|---:|---:|---:|---:|
| Sequential | 1 | 1.228292 | 1.000000 | 1.000000 |
| Multiprocessing | 1 | 1.191418 | 1.000000 | 1.000000 |
| Multiprocessing | 2 | 0.715021 | 1.666270 | 0.833135 |
| Multiprocessing | 4 | 0.724475 | 1.644526 | 0.411131 |
| MPI | 1 | 0.932027 | 1.000000 | 1.000000 |
| MPI | 2 | 0.487354 | 1.912423 | 0.956211 |
| MPI | 4 | 0.441152 | 2.112710 | 0.528178 |

These values describe one recorded run only.

## Visualizations

The visualization module consumes the validated analysis CSV and writes:

- [Execution time comparison](../results/execution_time_comparison.png)
- [Speedup comparison](../results/speedup_comparison.png)
- [Efficiency comparison](../results/efficiency_comparison.png)
- [Scalability comparison](../results/scalability_comparison.png)
- [MPI versus multiprocessing](../results/mpi_vs_multiprocessing.png)

The scalability chart includes an ideal linear reference. The comparison chart
labels which measured implementation has the lower time at matching worker
counts. Neither chart implies a universal ranking across hardware or
workloads.
