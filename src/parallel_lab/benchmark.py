"""Benchmark the sequential, multiprocessing, and MPI implementations."""

from __future__ import annotations

import argparse
import csv
import json
import multiprocessing
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from statistics import mean
from typing import Any, Sequence

from parallel_lab.multiprocessing_sum import run as run_multiprocessing
from parallel_lab.sequential import calculate_sum_of_squares as sequential_sum


ROOT = Path(__file__).resolve().parents[2]
RESULTS_PATH = ROOT / "results" / "benchmark_results.csv"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse benchmark options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=5_000_000)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--processes", type=int, nargs="+", default=[1, 2, 4])
    args = parser.parse_args(argv)
    if args.n < 1:
        parser.error("--n must be a positive integer")
    if args.repeats < 1:
        parser.error("--repeats must be a positive integer")
    if any(processes < 1 for processes in args.processes):
        parser.error("--processes values must be positive integers")
    return args


def _mpi_launcher() -> str:
    """Locate the environment MPI launcher before falling back to PATH."""
    candidates = [
        Path(sys.executable).parent.parent / "Library" / "bin" / "mpiexec.exe",
        Path(sys.executable).parent / "mpiexec.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    launcher = shutil.which("mpiexec")
    if launcher:
        return launcher
    raise RuntimeError("Could not find mpiexec in the active environment or PATH")


def _run_mpi(n: int, processes: int) -> tuple[int, float]:
    """Run the MPI module and parse its machine-readable result."""
    command = [
        _mpi_launcher(), "-n", str(processes), sys.executable,
        "-m", "parallel_lab.mpi_sum", "--n", str(n), "--json",
    ]
    environment = os.environ.copy()
    source_path = str(ROOT / "src")
    environment["PYTHONPATH"] = source_path + os.pathsep + environment.get("PYTHONPATH", "")
    completed = subprocess.run(
        command, cwd=ROOT, env=environment, capture_output=True, text=True, check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"MPI benchmark failed with exit code {completed.returncode}:\n"
            f"{completed.stderr.strip() or completed.stdout.strip()}"
        )
    for line in reversed(completed.stdout.splitlines()):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("implementation") == "mpi":
            return int(record["result"]), float(record["execution_time"])
    raise RuntimeError(f"MPI output did not contain a JSON result:\n{completed.stdout}")


def _benchmark_implementation(
    name: str, workers: int, repeats: int, runner: Any,
) -> tuple[int, float]:
    """Run one implementation repeatedly and return its result and mean time."""
    results: list[int] = []
    timings: list[float] = []
    for _ in range(repeats):
        result, elapsed = runner()
        results.append(result)
        timings.append(elapsed)
    if len(set(results)) != 1:
        raise RuntimeError(f"{name} produced inconsistent results: {results}")
    return results[0], mean(timings)


def main(argv: Sequence[str] | None = None) -> None:
    """Run benchmarks, validate results, write CSV, and print a table."""
    args = parse_args(argv)
    expected = sequential_sum(args.n)
    records: list[dict[str, Any]] = []

    sequential_result, sequential_average = _benchmark_implementation(
        "sequential", 1, args.repeats,
        lambda: _timed_sequential(args.n),
    )
    if sequential_result != expected:
        raise RuntimeError("Sequential implementation returned an unexpected result")
    records.append({
        "implementation": "sequential", "workers": 1, "n": args.n,
        "repetitions": args.repeats, "result": sequential_result,
        "average_time": sequential_average, "speedup": 1.0, "efficiency": 1.0,
    })

    for name, runner in (
        ("multiprocessing", lambda workers: lambda: run_multiprocessing(args.n, workers)),
        ("mpi", lambda workers: lambda: _run_mpi(args.n, workers)),
    ):
        for workers in args.processes:
            result, average = _benchmark_implementation(
                name, workers, args.repeats, runner(workers),
            )
            if result != expected:
                raise RuntimeError(f"{name} with {workers} workers returned an unexpected result")
            speedup = sequential_average / average
            records.append({
                "implementation": name, "workers": workers, "n": args.n,
                "repetitions": args.repeats, "result": result,
                "average_time": average, "speedup": speedup,
                "efficiency": speedup / workers,
            })

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"{'Implementation':<18} {'Workers':>7} {'Avg time (s)':>14} {'Speedup':>10} {'Efficiency':>12}")
    print("-" * 66)
    for record in records:
        print(
            f"{record['implementation']:<18} {record['workers']:>7} "
            f"{record['average_time']:>14.6f} {record['speedup']:>10.3f} "
            f"{record['efficiency']:>12.3f}"
        )
    print(f"\nResults saved to {RESULTS_PATH}")


def _timed_sequential(n: int) -> tuple[int, float]:
    """Time the existing sequential baseline without modifying it."""
    start_time = time.perf_counter()
    result = sequential_sum(n)
    return result, time.perf_counter() - start_time


if __name__ == "__main__":
    main()
