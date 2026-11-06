"""Tests for shared and parallel sum-of-squares implementations."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.image as mpimg
import pandas as pd
import pytest

from parallel_lab.analysis import (
    AnalysisError,
    analyze_file,
    build_analysis,
    calculate_metrics,
    calculate_worker_scalability,
    load_benchmark,
)
from parallel_lab.common import calculate_sum_of_squares, partition_range
from parallel_lab.multiprocessing_sum import run
from parallel_lab.sequential import calculate_sum_of_squares as sequential_sum
from parallel_lab.visualization import generate_all_charts


def test_sum_of_squares_small_input() -> None:
    assert calculate_sum_of_squares(1, 5) == 55


def test_partition_covers_all_values_without_overlap() -> None:
    n = 23
    chunks = [partition_range(n, rank, 4) for rank in range(4)]
    values = [value for start, end in chunks for value in range(start, end + 1)]
    assert values == list(range(1, n + 1))


def test_partition_handles_uneven_division() -> None:
    chunks = [partition_range(10, rank, 3) for rank in range(3)]
    assert chunks == [(1, 4), (5, 7), (8, 10)]


def test_multiprocessing_matches_sequential() -> None:
    result, _ = run(1_000, 2)
    assert result == sequential_sum(1_000)


def benchmark_rows() -> list[dict[str, object]]:
    return [
        {"implementation": "sequential", "workers": 1, "n": 100, "repetitions": 2, "result": 338350, "average_time": 10.0},
        {"implementation": "multiprocessing", "workers": 1, "n": 100, "repetitions": 2, "result": 338350, "average_time": 8.0},
        {"implementation": "multiprocessing", "workers": 2, "n": 100, "repetitions": 2, "result": 338350, "average_time": 5.0},
        {"implementation": "mpi", "workers": 1, "n": 100, "repetitions": 2, "result": 338350, "average_time": 7.0},
        {"implementation": "mpi", "workers": 2, "n": 100, "repetitions": 2, "result": 338350, "average_time": 4.0},
    ]


def test_performance_metrics_use_both_baselines() -> None:
    metrics = calculate_metrics(5.0, 2, 10.0, 8.0)
    assert metrics["sequential_baseline_speedup"] == pytest.approx(2.0)
    assert metrics["sequential_baseline_efficiency"] == pytest.approx(1.0)
    assert metrics["implementation_relative_speedup"] == pytest.approx(1.6)
    assert metrics["implementation_relative_efficiency"] == pytest.approx(0.8)


def test_one_worker_baselines_have_unit_relative_metrics() -> None:
    rows = build_analysis(benchmark_rows())
    for row in rows:
        if row["implementation"] != "sequential" and row["workers"] == 1:
            assert row["implementation_relative_speedup"] == pytest.approx(1.0)
            assert row["implementation_relative_efficiency"] == pytest.approx(1.0)


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda rows: rows[0].pop("average_time"), "missing columns"),
        (lambda rows: rows.append(rows[1].copy()), "Duplicate benchmark row"),
        (lambda rows: rows[0].update(average_time=0), "finite and positive"),
        (lambda rows: rows[0].update(average_time=-1), "finite and positive"),
        (lambda rows: rows.pop(0), "missing implementations"),
        (lambda rows: rows.pop(3), "Missing implementation baseline"),
        (lambda rows: rows[0].update(n=0), "n must be positive"),
        (lambda rows: rows[0].update(repetitions=-1), "repetitions must be positive"),
        (lambda rows: rows[0].update(implementation="unsupported"), "Unsupported implementation"),
    ],
)
def test_invalid_benchmark_data_is_rejected(tmp_path, mutate, message) -> None:
    rows = benchmark_rows()
    mutate(rows)
    path = tmp_path / "benchmark.csv"
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys(), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(AnalysisError, match=message):
        load_benchmark(path)


def test_scalability_rejects_missing_one_worker_baseline() -> None:
    rows = [row for row in benchmark_rows() if not (
        row["implementation"] == "mpi" and row["workers"] == 1
    )]
    with pytest.raises(AnalysisError, match="Missing implementation baseline row: mpi/1"):
        calculate_worker_scalability(rows)


def test_mpi_multiprocessing_comparison_and_csv_generation(tmp_path) -> None:
    input_path = tmp_path / "benchmark.csv"
    output_path = tmp_path / "analysis.csv"
    rows = benchmark_rows()
    with input_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    original = input_path.read_bytes()
    analyze_file(input_path, output_path)

    assert input_path.read_bytes() == original
    with output_path.open(newline="", encoding="utf-8") as analysis_file:
        analysis_rows = list(csv.DictReader(analysis_file))
    matching_rows = [row for row in analysis_rows if row["implementation"] == "mpi" and row["workers"] == "2"]
    assert matching_rows[0]["mpi_average_time"] == "4.0"
    assert matching_rows[0]["multiprocessing_average_time"] == "5.0"
    assert float(matching_rows[0]["mpi_vs_multiprocessing_speedup"]) == pytest.approx(1.25)


def test_all_visualization_outputs_are_valid_and_preserve_benchmark(tmp_path) -> None:
    benchmark_path = tmp_path / "benchmark.csv"
    analysis_path = tmp_path / "analysis.csv"
    output_directory = tmp_path / "charts"
    rows = benchmark_rows()
    with benchmark_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=(
            "implementation", "workers", "n", "repetitions", "result", "average_time",
        ))
        writer.writeheader()
        writer.writerows(rows)
    from parallel_lab.analysis import analyze_file
    analyze_file(benchmark_path, analysis_path)
    original = benchmark_path.read_bytes()

    paths = generate_all_charts(benchmark_path, analysis_path, output_directory)

    assert set(paths) == {
        "execution_time_comparison",
        "speedup_comparison",
        "efficiency_comparison",
        "scalability_comparison",
        "mpi_vs_multiprocessing",
    }
    for path in paths.values():
        assert path.parent == output_directory
        assert path.stat().st_size > 0
        image = mpimg.imread(path)
        assert image.shape[0] > 0
        assert image.shape[1] > 0
    assert (output_directory / "execution_time.png").exists()
    assert (output_directory / "speedup.png").exists()
    assert benchmark_path.read_bytes() == original


@pytest.mark.parametrize("missing", ["analysis", "benchmark"])
def test_visualization_rejects_missing_input(tmp_path, missing) -> None:
    benchmark_path = tmp_path / "benchmark.csv"
    analysis_path = tmp_path / "analysis.csv"
    if missing == "analysis":
        benchmark_path.write_text("implementation,workers,n,repetitions,result,average_time\n"
                                  "sequential,1,1,1,1,1\n", encoding="utf-8")
    with pytest.raises((FileNotFoundError, ValueError)):
        generate_all_charts(benchmark_path, analysis_path, tmp_path / "charts")


def test_visualization_rejects_invalid_analysis_data(tmp_path) -> None:
    benchmark_path = tmp_path / "benchmark.csv"
    analysis_path = tmp_path / "analysis.csv"
    rows = benchmark_rows()
    with benchmark_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=(
            "implementation", "workers", "n", "repetitions", "result", "average_time",
        ))
        writer.writeheader()
        writer.writerows(rows)
    pd.DataFrame({"implementation": ["mpi"], "workers": [1]}).to_csv(analysis_path, index=False)
    with pytest.raises(ValueError, match="missing columns"):
        generate_all_charts(benchmark_path, analysis_path, tmp_path / "charts")
