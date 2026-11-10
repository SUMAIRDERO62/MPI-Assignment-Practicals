# MPI Assignment Practicals

A practical-first Parallel Computing learning project built with **Python, mpi4py, NumPy, and Microsoft MPI**. It contains six independently runnable MPI practicals, a browser-based learning dashboard, a teacher presentation deck, automated tests, and a benchmark suite comparing sequential, multiprocessing, and MPI execution.

> **Repository:** [SUMAIRDERO62/MPI-Assignment-Practicals](https://github.com/SUMAIRDERO62/MPI-Assignment-Practicals)  
> **Focus:** MPI fundamentals → collective communication → parallel arrays and matrices → performance analysis.

## What this project demonstrates

### Six assignment practicals

| # | Practical | Main MPI concepts |
|---|---|---|
| 01 | Process rank and size | `MPI.COMM_WORLD`, `Get_rank()`, `Get_size()` |
| 02 | Point-to-point send and receive | `send()`, `recv()`, source, destination, tag |
| 03 | Array distribution | `Scatterv()`, `Gatherv()`, uneven data partitions |
| 04 | Parallel array sum | `Scatterv()`, local computation, `Reduce()`, `MPI.SUM` |
| 05 | Parallel matrix addition | Row distribution, `Scatterv()`, `Gatherv()` |
| 06 | Parallel matrix multiplication | `Bcast()`, row distribution, `Gatherv()` |

Each practical is a separate entry point under `practicals/`. The programs validate their results against the original input or a NumPy reference where applicable.

### Learning dashboard and teacher presentation

- **Dashboard:** `web/public/index.html` — static learning material, MPI concept visualizer, matrix calculator, practical navigation, and benchmark chart previews.
- **Presentation:** `web/public/presentation.html` — a keyboard-accessible teacher demonstration deck.
- **Written guide:** [docs/PROJECT_PRESENTATION.md](docs/PROJECT_PRESENTATION.md).

The browser visualizer is an educational simulation; it does not launch MPI processes. Run the Python practicals with a real MPI runtime.

### Performance comparison

The `src/parallel_lab/` package also compares the same sum-of-squares workload across:
1. Sequential Python
2. Python `multiprocessing`
3. MPI using `mpi4py`

It records timing data, derives speedup and efficiency metrics, and generates charts. Checked-in benchmark numbers are measurements from one recorded environment, not universal performance guarantees.

## Repository structure

```text
MPI-Assignment-Practicals/
├── .github/workflows/ci.yml
├── docs/                 # Assignment, installation, execution, concepts and presentation guides
├── practicals/            # Six standalone MPI practicals and shared helpers
├── src/parallel_lab/      # Sequential, multiprocessing, MPI and benchmark modules
├── tests/                 # Correctness, entry-point and MPI integration tests
├── results/               # Recorded CSV data and generated charts
├── web/public/            # Static dashboard and teacher presentation
├── requirements.txt
└── README.md
```

## Quick start — Windows PowerShell

### 1. Prerequisites

- Python 3.10+ (the CI workflow uses Python 3.11).
- An MPI implementation installed on the machine.
- `mpi4py` linked to the same MPI implementation used by `mpiexec`.

For Windows, Microsoft MPI is a supported setup. Do not mix an MS-MPI launcher with an `mpi4py` installation linked against a different MPI vendor.

### 2. Create the Python environment

Run from the repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:PYTHONPATH = "$PWD\src"
```

If activation is restricted, call `.venv\Scripts\python.exe` directly.

### 3. Verify the MPI launcher and Python binding

```powershell
mpiexec -n 4 python -c "from mpi4py import MPI; c=MPI.COMM_WORLD; print(f'Hello from rank {c.Get_rank()} of {c.Get_size()}')"
```

You should see four messages, one from each rank. Their print order is not guaranteed. If this fails, check that `mpiexec` and `mpi4py` use the same MPI implementation.

### 4. Run the six practicals

Run commands from the repository root:

```powershell
mpiexec -n 4 python practicals\practical_01_process_rank_size.py
mpiexec -n 2 python practicals\practical_02_send_receive.py
mpiexec -n 4 python practicals\practical_03_array_distribution.py --length 11
mpiexec -n 4 python practicals\practical_04_parallel_array_sum.py --length 11
mpiexec -n 4 python practicals\practical_05_parallel_matrix_addition.py
mpiexec -n 4 python practicals\practical_06_parallel_matrix_multiplication.py
```

Practical 02 needs at least two ranks. For uneven distribution, the length of 11 with four ranks is intentional: not every rank receives the same number of elements.

Detailed objectives, algorithms, commands, and viva prompts: [Six practicals](docs/PRACTICALS.md) and [MPI assignment guide](docs/MPI_ASSIGNMENT.md).

## Run tests

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m pytest -v
```

The test suite includes helper and validation tests, entry-point compilation checks, and an MPI integration test when `mpiexec` is available. A passing integration test exercises the array-sum practical with two MPI ranks; it does not by itself certify every practical on every MPI installation.

## Open the dashboard and presentation locally

```powershell
python -m http.server 8000 --directory web\public
```

- Dashboard: [http://localhost:8000](http://localhost:8000)
- Teacher presentation: [http://localhost:8000/presentation.html](http://localhost:8000/presentation.html)

Use the presentation's Previous/Next controls or keyboard arrows; browser fullscreen is available from the deck.

## Run the benchmark project

Set the source import path first:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m parallel_lab.benchmark
python -m parallel_lab.analysis --input results\benchmark_results.csv --output results\performance_analysis.csv
python -m parallel_lab.visualization --benchmark results\benchmark_results.csv --analysis results\performance_analysis.csv --output-dir results
```

The benchmark invokes MPI as well as multiprocessing, so a working MPI launcher is required. See [execution guide](docs/EXECUTION_GUIDE.md), [methodology](docs/methodology.md), and [performance analysis](docs/PERFORMANCE_ANALYSIS.md).

## Documentation

- [Project overview](docs/PROJECT_OVERVIEW.md)
- [MPI assignment practicals](docs/MPI_ASSIGNMENT.md)
- [Six practical quick reference](docs/PRACTICALS.md)
- [MPI concepts](docs/MPI_CONCEPTS.md)
- [Installation](docs/INSTALLATION.md)
- [Execution guide](docs/EXECUTION_GUIDE.md)
- [Teacher presentation guide](docs/PROJECT_PRESENTATION.md)
- [Deployment notes](docs/DEPLOYMENT.md)
- [Performance analysis](docs/PERFORMANCE_ANALYSIS.md)
- [Methodology](docs/methodology.md)
- [Recorded results analysis](docs/results-analysis.md)

## Deployment boundary

The dashboard and presentation are static files and can be hosted on Vercel or another static host. **MPI execution is not performed by Vercel**: run the practicals and benchmarks on a local machine, university lab system, or MPI cluster. Deployment instructions are in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Limitations

- Parallel speedup depends on workload size, hardware, MPI runtime, process startup, communication, and system load.
- A browser-based visualization is explanatory, not a substitute for running the MPI programs.
- Checked-in benchmark results represent a particular recorded run and should be regenerated for a new machine.
- The GitHub Actions workflow checks Python compilation and tests on Ubuntu; local Windows MPI execution remains an environment-specific verification.

## License

No license has been specified yet. Contact the repository owner before reusing this project beyond the permissions granted by GitHub's default repository terms.
