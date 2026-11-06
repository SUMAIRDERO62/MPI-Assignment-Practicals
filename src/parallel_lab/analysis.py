"""Analyze benchmark results without changing the original benchmark data."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Iterable, Mapping, Sequence


IMPLEMENTATIONS = ("sequential", "multiprocessing", "mpi")
PARALLEL_IMPLEMENTATIONS = ("multiprocessing", "mpi")
REQUIRED_COLUMNS = {
    "implementation",
    "workers",
    "n",
    "repetitions",
    "result",
    "average_time",
}
ANALYSIS_COLUMNS = (
    "implementation",
    "workers",
    "average_time",
    "sequential_baseline_speedup",
    "sequential_baseline_efficiency",
    "implementation_relative_speedup",
    "implementation_relative_efficiency",
    "mpi_average_time",
    "multiprocessing_average_time",
    "mpi_vs_multiprocessing_speedup",
)


class AnalysisError(ValueError):
    """Raised when benchmark data cannot support a reliable analysis."""


def _parse_int(value: str, field: str, row_number: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise AnalysisError(
            f"Row {row_number}: {field} must be an integer, got {value!r}"
        ) from error
    return parsed


def _parse_positive_int(value: str, field: str, row_number: int) -> int:
    parsed = _parse_int(value, field, row_number)
    if parsed <= 0:
        raise AnalysisError(f"Row {row_number}: {field} must be positive")
    return parsed


def _parse_time(value: str, row_number: int) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as error:
        raise AnalysisError(
            f"Row {row_number}: average_time must be a number, got {value!r}"
        ) from error
    if not math.isfinite(parsed) or parsed <= 0:
        raise AnalysisError(
            f"Row {row_number}: average_time must be finite and positive"
        )
    return parsed


def load_benchmark(path: str | Path) -> list[dict[str, object]]:
    """Load and validate benchmark records from ``path``."""
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Benchmark CSV not found: {input_path}")

    try:
        with input_path.open(newline="", encoding="utf-8-sig") as source:
            reader = csv.DictReader(source)
            columns = set(reader.fieldnames or [])
            missing = REQUIRED_COLUMNS - columns
            if missing:
                names = ", ".join(sorted(missing))
                raise AnalysisError(f"Benchmark CSV is missing columns: {names}")

            records: list[dict[str, object]] = []
            seen: set[tuple[str, int]] = set()
            for row_number, row in enumerate(reader, start=2):
                implementation = (row.get("implementation") or "").strip()
                if not implementation:
                    raise AnalysisError(f"Row {row_number}: implementation is required")
                workers = _parse_int(row["workers"], "workers", row_number)
                if workers <= 0:
                    raise AnalysisError(f"Row {row_number}: workers must be positive")
                key = (implementation, workers)
                if key in seen:
                    raise AnalysisError(
                        f"Duplicate benchmark row for implementation={implementation!r}, "
                        f"workers={workers}"
                    )
                seen.add(key)
                records.append({
                    "implementation": implementation,
                    "workers": workers,
                    "n": _parse_positive_int(row["n"], "n", row_number),
                    "repetitions": _parse_positive_int(row["repetitions"], "repetitions", row_number),
                    "result": _parse_int(row["result"], "result", row_number),
                    "average_time": _parse_time(row["average_time"], row_number),
                })
    except csv.Error as error:
        raise AnalysisError(f"Malformed benchmark CSV {input_path}: {error}") from error

    _validate_records(records)
    return sorted(records, key=lambda record: (str(record["implementation"]), int(record["workers"])))


def _validate_records(records: Sequence[Mapping[str, object]]) -> None:
    if not records:
        raise AnalysisError("Benchmark CSV contains no data rows")

    implementations = {str(record["implementation"]) for record in records}
    unsupported = implementations - set(IMPLEMENTATIONS)
    if unsupported:
        raise AnalysisError(
            f"Unsupported implementation name(s): {', '.join(sorted(unsupported))}"
        )
    missing = set(IMPLEMENTATIONS) - implementations
    if missing:
        raise AnalysisError(f"Benchmark CSV is missing implementations: {', '.join(sorted(missing))}")

    expected_keys = {("sequential", 1), ("multiprocessing", 1), ("mpi", 1)}
    actual_keys = {(str(record["implementation"]), int(record["workers"])) for record in records}
    missing_baselines = expected_keys - actual_keys
    if missing_baselines:
        names = ", ".join(f"{implementation}/1" for implementation, _ in sorted(missing_baselines))
        raise AnalysisError(f"Missing implementation baseline row(s): {names}")

    reference = records[0]
    for field in ("n", "repetitions", "result"):
        if any(record[field] != reference[field] for record in records):
            raise AnalysisError(f"Inconsistent benchmark {field} values")

    sequential = next(
        record for record in records
        if record["implementation"] == "sequential" and record["workers"] == 1
    )
    if any(
        record["implementation"] == "sequential" and record["workers"] != 1
        for record in records
    ):
        raise AnalysisError("Sequential implementation must have exactly one worker")
    if sequential["workers"] != 1:
        raise AnalysisError("Sequential baseline must use one worker")


def calculate_metrics(
    average_time: float,
    workers: int,
    sequential_time: float,
    implementation_one_worker_time: float,
) -> dict[str, float]:
    """Calculate baseline and implementation-relative performance metrics."""
    for name, value in (
        ("average_time", average_time),
        ("sequential_time", sequential_time),
        ("implementation_one_worker_time", implementation_one_worker_time),
    ):
        if not math.isfinite(value) or value <= 0:
            raise AnalysisError(f"{name} must be finite and positive")
    if workers <= 0:
        raise AnalysisError("workers must be positive")

    baseline_speedup = sequential_time / average_time
    relative_speedup = implementation_one_worker_time / average_time
    return {
        "sequential_baseline_speedup": baseline_speedup,
        "sequential_baseline_efficiency": baseline_speedup / workers,
        "implementation_relative_speedup": relative_speedup,
        "implementation_relative_efficiency": relative_speedup / workers,
    }


def calculate_worker_scalability(
    records: Iterable[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Return one-worker-relative scalability metrics for parallel records."""
    records = list(records)
    baselines: dict[str, float] = {}
    for implementation in PARALLEL_IMPLEMENTATIONS:
        baseline = next((
            record["average_time"] for record in records
            if record["implementation"] == implementation and record["workers"] == 1
        ), None)
        if baseline is None:
            raise AnalysisError(
                f"Missing implementation baseline row: {implementation}/1"
            )
        baselines[implementation] = float(baseline)
    results: list[dict[str, object]] = []
    for record in records:
        implementation = str(record["implementation"])
        if implementation not in PARALLEL_IMPLEMENTATIONS:
            continue
        speedup = baselines[implementation] / float(record["average_time"])
        efficiency = speedup / int(record["workers"])
        results.append({
            "implementation": implementation,
            "workers": int(record["workers"]),
            "speedup": speedup,
            "efficiency": efficiency,
        })
    return sorted(results, key=lambda record: (str(record["implementation"]), int(record["workers"])))


def compare_implementations(
    records: Iterable[Mapping[str, object]],
) -> dict[int, dict[str, float]]:
    """Compare MPI and multiprocessing timings at matching worker counts."""
    by_key = {
        (str(record["implementation"]), int(record["workers"])): float(record["average_time"])
        for record in records
    }
    worker_counts = sorted({
        workers for implementation, workers in by_key
        if implementation in PARALLEL_IMPLEMENTATIONS
    })
    comparison: dict[int, dict[str, float]] = {}
    for workers in worker_counts:
        mpi_time = by_key.get(("mpi", workers))
        multiprocessing_time = by_key.get(("multiprocessing", workers))
        if mpi_time is None or multiprocessing_time is None:
            continue
        comparison[workers] = {
            "mpi_average_time": mpi_time,
            "multiprocessing_average_time": multiprocessing_time,
            "mpi_vs_multiprocessing_speedup": multiprocessing_time / mpi_time,
        }
    return comparison


def build_analysis(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    """Build sorted analysis rows from validated benchmark records."""
    _validate_records(records)
    sequential_time = float(next(
        record["average_time"] for record in records
        if record["implementation"] == "sequential" and record["workers"] == 1
    ))
    baselines = {
        implementation: float(next(
            record["average_time"] for record in records
            if record["implementation"] == implementation and record["workers"] == 1
        ))
        for implementation in PARALLEL_IMPLEMENTATIONS
    }
    comparisons = compare_implementations(records)
    analysis: list[dict[str, object]] = []
    for record in records:
        implementation = str(record["implementation"])
        workers = int(record["workers"])
        baseline = sequential_time if implementation == "sequential" else baselines[implementation]
        metrics = calculate_metrics(float(record["average_time"]), workers, sequential_time, baseline)
        comparison = comparisons.get(workers, {}) if implementation in PARALLEL_IMPLEMENTATIONS else {}
        analysis.append({
            "implementation": implementation,
            "workers": workers,
            "average_time": float(record["average_time"]),
            **metrics,
            "mpi_average_time": comparison.get("mpi_average_time", ""),
            "multiprocessing_average_time": comparison.get("multiprocessing_average_time", ""),
            "mpi_vs_multiprocessing_speedup": comparison.get("mpi_vs_multiprocessing_speedup", ""),
        })
    return sorted(analysis, key=lambda row: (str(row["implementation"]), int(row["workers"])))


def write_analysis(records: Sequence[Mapping[str, object]], path: str | Path) -> Path:
    """Write analysis records to a configurable CSV path."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=ANALYSIS_COLUMNS)
        writer.writeheader()
        writer.writerows(build_analysis(records))
    return output_path


def analyze_file(input_path: str | Path, output_path: str | Path) -> Path:
    """Load a benchmark CSV and write its derived performance analysis."""
    return write_analysis(load_benchmark(input_path), output_path)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse analysis input and output paths."""
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "results" / "benchmark_results.csv")
    parser.add_argument("--output", type=Path, default=root / "results" / "performance_analysis.csv")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """Generate the performance analysis CSV."""
    args = parse_args(argv)
    output_path = analyze_file(args.input, args.output)
    print(f"Performance analysis saved to {output_path}")


if __name__ == "__main__":
    main()
