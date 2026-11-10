# Installation

These instructions target Windows PowerShell and assume commands are run from the repository root.

## 1. Prerequisites

- Python 3.10 or newer.
- An installed MPI implementation. Microsoft MPI is a supported Windows option.
- `mpi4py` built/installed against the same MPI implementation used by `mpiexec`.

Check Python:

```powershell
py -3 --version
```

Check that the MPI launcher is discoverable:

```powershell
where.exe mpiexec
mpiexec -?
```

## 2. Create an isolated Python environment

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, either enable it for the current terminal session or call `.venv\Scripts\python.exe` directly.

## 3. Configure the source layout

The Python package is under `src/parallel_lab`. Set the import path in the active PowerShell session:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

## 4. Verify mpi4py and the launcher together

First inspect the MPI library loaded by Python:

```powershell
python -c "from mpi4py import MPI; print('Vendor:', MPI.get_vendor()); print(MPI.Get_library_version())"
```

Then run a multi-process smoke test:

```powershell
mpiexec -n 4 python -c "from mpi4py import MPI; c=MPI.COMM_WORLD; print(f'Hello from rank {c.Get_rank()} of {c.Get_size()}')"
```

A four-process launch should produce four messages, with ranks 0 through 3. Output order is nondeterministic.

**Important:** Do not mix a Microsoft MPI launcher with an `mpi4py` installation linked against Intel MPI or another MPI implementation. If the smoke test fails, confirm that the launcher on `PATH` matches the vendor reported by `MPI.get_vendor()`, and confirm that `mpiexec` starts the same Python interpreter in which `mpi4py` is installed.

## 5. Run the tests

```powershell
python -m pytest -v
```

The suite covers helper functions, input validation, practical entry-point compilation, and an MPI integration test when `mpiexec` is available.

## 6. Run an assignment practical

```powershell
mpiexec -n 4 python practicals\practical_01_process_rank_size.py
```

See [MPI_ASSIGNMENT.md](MPI_ASSIGNMENT.md) and [PRACTICALS.md](PRACTICALS.md) for all six practicals.

## Troubleshooting

- **`ModuleNotFoundError: mpi4py`:** install requirements into the interpreter used by the command; check `python -c "import sys; print(sys.executable)"`.
- **MPI DLL or runtime errors:** check that the active `mpiexec` and `mpi4py` use the same MPI vendor.
- **`ModuleNotFoundError: parallel_lab`:** set `$env:PYTHONPATH = "$PWD\src"` from the repository root.
- **Only one rank appears:** ensure the command uses `mpiexec -n 4` and not a direct Python invocation.
- **A practical expects two ranks:** use at least `-n 2` for Practical 02.
