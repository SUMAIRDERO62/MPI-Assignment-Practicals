# Project overview

MPI-Assignment-Practicals is a Python university semester project that compares one
deterministic sum-of-squares workload using sequential Python,
`multiprocessing`, and MPI through `mpi4py`.

## Scope

For an input `n`, every implementation computes:

```text
1^2 + 2^2 + ... + n^2
```

The project separates three concerns:

1. **Measurement** — `benchmark.py` records repeated execution timings.
2. **Analysis** — `analysis.py` validates raw data and derives metrics.
3. **Visualization** — `visualization.py` creates report-ready PNG charts.

## Objectives

- Compare sequential, shared-memory, and distributed process execution.
- Use balanced, non-overlapping range partitioning.
- Validate that every implementation returns the same integer result.
- Study worker-count effects using speedup, efficiency, and scalability.
- Preserve raw benchmark data independently from derived analysis.

## Implementations

| Implementation | Entry point | Work distribution |
|---|---|---|
| Sequential | `python -m parallel_lab.sequential` | One Python process |
| Multiprocessing | `python -m parallel_lab.multiprocessing_sum` | `multiprocessing.Pool` workers |
| MPI | `mpiexec -n P python -m parallel_lab.mpi_sum` | MPI ranks in `MPI.COMM_WORLD` |

## Current status

Phase 6 Steps 2, 3, and 5 are implemented. The repository contains the
analysis engine, five professional charts, automated tests, and synchronized
project documentation. A separate performance report is not part of this step.

See also:

- [Architecture](architecture.md)
- [Methodology](methodology.md)
- [Installation](INSTALLATION.md)
- [Execution guide](EXECUTION_GUIDE.md)
- [Performance analysis](PERFORMANCE_ANALYSIS.md)
