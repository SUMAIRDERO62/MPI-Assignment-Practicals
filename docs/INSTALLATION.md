# Installation

These instructions target Windows PowerShell from the repository root.

## Python environment

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pytest
```

The project uses a `src` layout. Set the import path for the current
PowerShell session:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

If activation is restricted, use the virtual-environment interpreter
directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install pytest
```

## MPI runtime

On Windows, use the `mpiexec.exe` shipped with the MPI implementation used
by `mpi4py`. Do not mix a Microsoft MPI launcher with an `mpi4py` build that
loads Intel MPI or another implementation. After installing the requirements,
the bundled launcher can be selected explicitly:

```powershell
.\.venv\Library\bin\mpiexec.exe -n 4 .\.venv\Scripts\python.exe `
    practicals\01_process_rank_size.py
```

If using a separately installed MPI implementation, verify that its launcher
matches the vendor reported by `mpi4py` before placing it on `PATH`. The
benchmark launcher checks common MPI locations inside the active environment
before searching `PATH`.

## Dependencies

Runtime dependencies are declared in [requirements.txt](../requirements.txt):

- `mpi4py==4.1.2`
- NumPy
- Matplotlib
- pandas

`pytest` is used by the test suite but is currently installed separately
because it is not listed in `requirements.txt`.
