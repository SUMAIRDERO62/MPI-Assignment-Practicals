# Project summary

## Purpose

MPI-Assignment-Practicals is a university semester project comparing sequential Python,
Python multiprocessing, and MPI through `mpi4py` on the same sum-of-squares
workload.

## Completed functionality

- Implemented the sequential reference calculation.
- Implemented balanced shared-memory multiprocessing.
- Implemented MPI rank partitioning, synchronization, and reductions.
- Added repeated benchmark execution and correctness validation.
- Preserved raw benchmark measurements in CSV format.
- Added a validated performance-analysis engine.
- Added sequential-baseline and implementation-relative speedup and efficiency.
- Added worker scalability and MPI-versus-multiprocessing comparison data.
- Added five professional performance charts and retained legacy charts.
- Added automated tests for computation, analysis, validation, and charts.
- Updated architecture, methodology, results, and project documentation.

## Current recorded outcome

The checked-in experiment uses `n=5,000,000` and three repetitions. Every
implementation returns `41666679166667500000`. In this recorded run, MPI with
four workers has the lowest measured average time, `0.441152 s`; MPI with two
workers is also faster than multiprocessing at two workers.

These are observations from the checked-in CSV, not general performance
claims. See the [results analysis](results-analysis.md) and
[methodology](methodology.md).

## Technologies

The project uses Python 3, `mpi4py`, the standard-library
`multiprocessing` module, pandas, Matplotlib, pytest, and a Windows MPI
launcher such as Microsoft MPI.

## Project status

Phase 6 Steps 2, 3, and 5 are implemented. The analysis engine,
visualization workflow, and documentation package are complete for the current
scope. The performance report and later Phase 6 steps remain separate work.

## Conclusion

The project demonstrates how correct range partitioning and aggregation can
support comparable sequential, multiprocessing, and MPI experiments. It also
shows why measured scalability depends on workload size, process overhead,
timing boundaries, and execution environment.
