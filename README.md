# ParallelLab-MPI

ParallelLab-MPI is a Python distributed-computing experiment that evaluates
three ways to calculate the sum of squares:

\[
\sum_{i=1}^{n} i^2
\]

The project provides a sequential baseline, an MPI implementation, and a
shared-memory multiprocessing implementation. It measures execution time,
computes speedup and efficiency, and generates charts from the recorded
benchmark data.

## Objectives

- Implement the same deterministic workload with sequential, MPI, and
  multiprocessing execution models.
- Partition the inclusive range `1..n` without overlap or omission.
- Validate that every implementation returns the same result.
- Measure execution time and compare the effect of worker count.
- Provide reproducible benchmark data and visualizations.

## Problem statement and features

The experiment explores how a CPU-bound Python workload behaves when divided
among processes. The workload is intentionally simple: each worker computes
partial sums of squares, and the partial results are combined.

Features include:

- Balanced range partitioning for uneven divisions and empty chunks.
- Sequential, MPI, and multiprocessing implementations with compatible
  command-line interfaces.
- MPI result aggregation with `MPI.SUM` and elapsed-time aggregation with
  `MPI.MAX`.
- Repeated benchmarks with result-consistency checks.
- CSV output containing average time, speedup, and efficiency.
- Matplotlib charts for execution time and speedup.

## Technology stack

- Python 3
- `mpi4py` for MPI communication
- NumPy, pandas, and Matplotlib for the project environment and visualization
- Python `multiprocessing.Pool` for local worker processes
- `pytest` for tests
- Microsoft MPI or another MPI implementation providing `mpiexec` for MPI
  execution on Windows

## Architecture and folder structure

```text
ParallelLab-MPI/
├── src/parallel_lab/
│   ├── common.py                 # Workload and balanced partitioning helpers
│   ├── sequential.py             # Single-process implementation
│   ├── multiprocessing_sum.py   # multiprocessing.Pool implementation
│   ├── mpi_sum.py                # MPI implementation
│   ├── benchmark.py              # Repeated benchmark and CSV generation
│   └── visualization.py          # Chart generation
├── tests/test_parallel.py        # Unit and consistency tests
├── results/
│   ├── benchmark_results.csv
│   ├── execution_time.png
│   └── speedup.png
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   ├── results-analysis.md
│   └── project-summary.md
├── requirements.txt
└── README.md
```

See [the architecture document](docs/architecture.md) for the execution and
communication model.

## Installation on Windows PowerShell

From the repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell prevents script activation, use the policy permitted by your
organization, or invoke the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

For MPI commands, install Microsoft MPI (or another Windows MPI
implementation) and ensure `mpiexec` is available. The benchmark module also
checks common MPI locations inside the active environment before searching
`PATH`.

The package uses a `src` layout. Set `PYTHONPATH` for the current PowerShell
session:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

## Running the implementations

Sequential execution:

```powershell
python -m parallel_lab.sequential
```

MPI execution with four ranks:

```powershell
mpiexec -n 4 python -m parallel_lab.mpi_sum --n 5000000
```

MPI execution with machine-readable JSON output:

```powershell
mpiexec -n 4 python -m parallel_lab.mpi_sum --n 5000000 --json
```

Multiprocessing execution with four worker processes:

```powershell
python -m parallel_lab.multiprocessing_sum --n 5000000 --processes 4
```

All implementations should report the same sum. For `n=5,000,000`, the
expected result recorded in the benchmark is
`41666679166667500000`.

## Benchmarking and visualization

Run the default benchmark (`n=5,000,000`, three repetitions, and worker
counts 1, 2, and 4):

```powershell
python -m parallel_lab.benchmark
```

Choose the workload, repetitions, and worker counts explicitly:

```powershell
python -m parallel_lab.benchmark --n 5000000 --repeats 3 --processes 1 2 4
```

The benchmark writes [results/benchmark_results.csv](results/benchmark_results.csv).
Generate both charts from that CSV with:

```powershell
python -m parallel_lab.visualization
```

Generated charts:

- [Execution-time chart](results/execution_time.png)
- [Speedup chart](results/speedup.png)

Run the tests with:

```powershell
python -m pytest
```

## Speedup and efficiency

For a parallel configuration, speedup is:

```text
speedup = sequential average time / parallel average time
```

Efficiency normalizes speedup by the number of workers:

```text
efficiency = speedup / number of workers
```

The sequential row is the baseline, so its speedup and efficiency are both
`1.0`. Efficiency below `1.0` indicates that the observed speedup is less than
ideal linear scaling.

## Benchmark findings

The checked-in CSV uses `n=5,000,000` and `3` repetitions for every row. The
sequential baseline averaged `0.854352 s`. The fastest observed parallel
configuration was MPI with `2` workers: `0.697793 s`, speedup `1.224363`, and
efficiency `0.612181`. Multiprocessing with `2` workers was next at
`0.717222 s`, speedup `1.191195`, and efficiency `0.595598`.

Increasing either implementation to four workers did not improve this
measurement: multiprocessing averaged `0.846824 s` and MPI averaged
`0.755873 s`. The one-worker rows were close to the sequential baseline
(multiprocessing `0.850150 s`; MPI `0.846328 s`). These observations describe
this recorded run only; they are not a claim of general performance on other
hardware or workloads. See the [full results analysis](docs/results-analysis.md).

## Limitations and future improvements

- Results are host- and system-dependent and use only three repetitions.
- Process startup, pool creation, MPI launch, synchronization, and reduction
  overhead affect short workloads.
- The benchmark currently varies worker count but does not sweep multiple input
  sizes or collect variability statistics.
- The workload is CPU-bound but has minimal communication volume, so it does not
  represent every distributed application.
- Future work could add confidence intervals, warm-up runs, larger size sweeps,
  serialization and communication measurements, and automated result
  archiving.

Further details are available in [the methodology](docs/methodology.md) and
[the project summary](docs/project-summary.md).