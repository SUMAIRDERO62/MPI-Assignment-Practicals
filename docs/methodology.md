# Methodology

## Workload

Each run computes the integer sum of squares:

```text
1^2 + 2^2 + ... + n^2
```

The checked-in benchmark uses `n=5,000,000`. Every implementation validates
its result against the sequential result, and the recorded result is
`41666679166667500000`.

## Partitioning

The range `1..n` is divided into balanced, non-overlapping inclusive chunks.
For `size` workers, each chunk receives `n // size` values and the first
`n % size` chunks receive one additional value. This ensures that every input
value is processed exactly once, including when `n` is not evenly divisible
by the worker count.

MPI maps chunks to ranks. Multiprocessing maps chunks to pool workers. The
sequential implementation processes the complete range in one process.

## Repetitions and timing

The benchmark defaults to three repetitions for each implementation and
worker count. It records the arithmetic mean of those timings and writes one
row per configuration to `results/benchmark_results.csv`.

The benchmark times:

- the sequential calculation;
- multiprocessing pool creation, task execution, result collection, and pool
  cleanup, as implemented by `run`;
- the MPI local computation interval after a barrier, with rank 0 reporting
  the maximum local elapsed time across ranks.

The benchmark checks that all repetitions for a configuration return the same
integer result before writing the CSV.

## Metrics

Speedup is calculated relative to the sequential average:

\[
\text{speedup} = \frac{T_{\text{sequential}}}{T_{\text{parallel}}}
\]

Efficiency is speedup divided by the number of workers:

\[
\text{efficiency} = \frac{\text{speedup}}{\text{number of workers}}
\]

An efficiency of `1.0` would represent ideal linear scaling. Values below
`1.0` indicate that worker parallelism did not achieve ideal scaling for the
measured configuration. The sequential baseline is assigned speedup and
efficiency values of `1.0`.

## Measurement limitations

The CSV is one measurement set, not a hardware-independent performance
claim. Timings can vary with CPU load, operating-system scheduling, Python and
MPI versions, process affinity, and background activity. Three repetitions
provide limited information about variance and do not support confidence
intervals.

Process startup, worker-pool construction, synchronization, inter-process
communication, result transfer, and MPI reduction can dominate a relatively
small arithmetic workload. MPI and multiprocessing also use different timing
boundaries, so their values should be interpreted as measurements of the
implemented execution paths rather than as a complete hardware model.

The methodology does not currently include warm-up runs, multiple input-size
sweeps, standard deviations, confidence intervals, or explicit communication
profiling. These are appropriate improvements for a more rigorous scaling
study.
