# Results analysis

This analysis uses the checked-in
[benchmark CSV](../results/benchmark_results.csv), rather than inferred or
synthetic measurements. All rows use `n=5,000,000` and `3` repetitions, and
all rows report the same result: `41666679166667500000`.

## Recorded measurements

| Implementation | Workers | Average time (s) | Speedup | Efficiency |
|---|---:|---:|---:|---:|
| Sequential | 1 | 0.854352 | 1.000000 | 1.000000 |
| Multiprocessing | 1 | 0.850150 | 1.004943 | 1.004943 |
| Multiprocessing | 2 | 0.717222 | 1.191195 | 0.595598 |
| Multiprocessing | 4 | 0.846824 | 1.008889 | 0.252222 |
| MPI | 1 | 0.846328 | 1.009481 | 1.009481 |
| MPI | 2 | 0.697793 | 1.224363 | 0.612181 |
| MPI | 4 | 0.755873 | 1.130284 | 0.282571 |

Speedup is computed as sequential average time divided by the configuration's
average time. Efficiency is speedup divided by the worker count.

## Comparison

The best observed configuration is MPI with two workers: `0.697793 s`,
speedup `1.224363`, and efficiency `0.612181`. Multiprocessing with two
workers is the second-fastest parallel row at `0.717222 s`, speedup `1.191195`,
and efficiency `0.595598`.

The one-worker rows are close to the sequential baseline. The small
above-baseline speedups in those rows should not be interpreted as parallel
scaling; they are within the kind of run-to-run variation expected from
process and timing differences.

Four workers are slower than two workers for both parallel approaches in this
CSV. Multiprocessing takes `0.846824 s`, while MPI takes `0.755873 s`. Thus,
the data does not show monotonic scaling with worker count. The corresponding
efficiencies, `0.252222` and `0.282571`, are substantially below the
two-worker efficiencies.

## Overhead and scaling

The workload performs simple integer arithmetic and has little communication
per input value. Creating processes, scheduling work, synchronizing, moving
partial results, and reducing them therefore consume a meaningful portion of
the run. With four workers, the smaller chunks do not compensate for those
costs in this measurement.

The MPI two-worker row is the fastest recorded configuration, but this result
is specific to the checked-in run and its execution environment. It does not
establish that MPI is universally faster than multiprocessing. A stronger
scaling study would repeat the experiment across input sizes, record
variability, and control hardware and system load.

The generated [execution-time chart](../results/execution_time.png) and
[speedup chart](../results/speedup.png) visualize the same CSV values.
