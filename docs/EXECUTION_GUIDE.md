# Execution guide

Run these commands from the repository root after following
[Installation](INSTALLATION.md).

## Sequential implementation

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m parallel_lab.sequential
```

This runs the reference calculation in one Python process.

## Multiprocessing implementation

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m parallel_lab.multiprocessing_sum `
  --n 5000000 --processes 4
```

This uses local `multiprocessing.Pool` workers. It does not require
`mpiexec`.

## MPI implementation

```powershell
$env:PYTHONPATH = "$PWD\src"
mpiexec -n 4 python -m parallel_lab.mpi_sum --n 5000000
```

For machine-readable output:

```powershell
mpiexec -n 4 python -m parallel_lab.mpi_sum `
  --n 5000000 --json
```

MPI commands require a working MPI runtime and `mpiexec`.

## Benchmark

The default benchmark measures `n=5,000,000` three times using worker counts
`1`, `2`, and `4`:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m parallel_lab.benchmark
```

Explicit options:

```powershell
python -m parallel_lab.benchmark `
  --n 5000000 --repeats 3 --processes 1 2 4
```

The benchmark writes [benchmark_results.csv](../results/benchmark_results.csv).
It invokes both multiprocessing and MPI measurements, so `mpiexec` must be
available.

## Analysis

```powershell
python -m parallel_lab.analysis `
  --input results\benchmark_results.csv `
  --output results\performance_analysis.csv
```

This reads the raw CSV and writes a separate derived-data CSV.

## Visualizations

```powershell
python -m parallel_lab.visualization `
  --benchmark results\benchmark_results.csv `
  --analysis results\performance_analysis.csv `
  --output-dir results
```

This preserves `execution_time.png` and `speedup.png` and writes the five
Phase 6 comparison charts.

## Tests

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m pytest -q
```

The suite does not require an actual MPI run; MPI-related analysis tests use
temporary CSV data.
