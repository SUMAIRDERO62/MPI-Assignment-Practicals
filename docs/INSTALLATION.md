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

Install Microsoft MPI or another Windows MPI runtime that provides
`mpiexec.exe`. Verify that the launcher is available:

```powershell
Get-Command mpiexec
mpiexec -help
```

The benchmark launcher also checks common MPI locations inside the active
environment before searching `PATH`.

## Dependencies

Runtime dependencies are declared in [requirements.txt](../requirements.txt):

- `mpi4py==4.1.2`
- NumPy
- Matplotlib
- pandas

`pytest` is used by the test suite but is currently installed separately
because it is not listed in `requirements.txt`.
