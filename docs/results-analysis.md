# Results analysis

This analysis uses the checked-in
[benchmark CSV](../results/benchmark_results.csv) and generated
[performance analysis CSV](../results/performance_analysis.csv). No values are
inferred from hardware specifications or synthetic measurements.

All rows use `n=5,000,000` and three repetitions. Every row reports
`41666679166667500000`.

## Recorded measurements

| Implementation | Workers | Average time (s) | Sequential speedup | Sequential efficiency | Relative speedup | Relative efficiency |
|---|---:|---:|---:|---:|---:|---:|
| Sequential | 1 | 1.228292 | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| Multiprocessing | 1 | 1.191418 | 1.030950 | 1.030950 | 1.000000 | 1.000000 |
| Multiprocessing | 2 | 0.715021 | 1.717841 | 0.858921 | 1.666270 | 0.833135 |
| Multiprocessing | 4 | 0.724475 | 1.695424 | 0.423856 | 1.644526 | 0.411131 |
| MPI | 1 | 0.932027 | 1.317872 | 1.317872 | 1.000000 | 1.000000 |
| MPI | 2 | 0.487354 | 2.520329 | 1.260165 | 1.912423 | 0.956211 |
| MPI | 4 | 0.441152 | 2.784283 | 0.696071 | 2.112710 | 0.528178 |

Sequential-baseline metrics use the sequential row. Relative metrics use the
one-worker row of the same implementation.

## Comparison

The fastest measured row in this CSV is MPI with four workers at `0.441152 s`.
MPI with two workers is the fastest configuration at the same worker count
comparison against multiprocessing: `0.487354 s` versus `0.715021 s`.
MPI is also faster at four workers: `0.441152 s` versus `0.724475 s`.

These statements describe this checked-in run only. They are not claims that
MPI is universally faster than multiprocessing on other machines, workloads,
or MPI configurations.

## Scaling observations

Implementation-relative speedup reaches `2.112710` for MPI with four workers
and `1.644526` for multiprocessing with four workers. The corresponding
relative efficiencies are `0.528178` and `0.411131`, both below ideal linear
scaling.

The simple arithmetic workload and the timing boundaries make process startup,
scheduling, synchronization, result transfer, and reduction overhead
important. A larger worker count does not guarantee a lower measured time.

## Five performance charts

- [Execution time comparison](../results/execution_time_comparison.png):
  compares measured average time for all three implementations.
- [Speedup comparison](../results/speedup_comparison.png): distinguishes
  sequential-baseline speedup from implementation-relative speedup.
- [Efficiency comparison](../results/efficiency_comparison.png): compares
  both efficiency definitions and shows ideal efficiency at `1.0`.
- [Scalability comparison](../results/scalability_comparison.png): compares
  multiprocessing and MPI relative speedup against ideal linear scaling.
- [MPI versus multiprocessing](../results/mpi_vs_multiprocessing.png):
  compares matching worker counts and labels the faster measured path.

The legacy [execution-time chart](../results/execution_time.png) and
[speedup chart](../results/speedup.png) are retained for compatibility.

## Interpretation limits

The data contains one input size and three repetitions. It does not provide
confidence intervals, warm-up analysis, hardware characterization, affinity
control, or communication profiling. Future conclusions should use a broader
experimental design.
