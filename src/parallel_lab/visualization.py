"""Generate benchmark charts from the CSV results."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "results" / "benchmark_results.csv"
TIME_CHART_PATH = ROOT / "results" / "execution_time.png"
SPEEDUP_CHART_PATH = ROOT / "results" / "speedup.png"


def main() -> None:
    """Read benchmark results and save execution-time and speedup charts."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Benchmark results not found: {INPUT_PATH}")
    data = pd.read_csv(INPUT_PATH)
    required_columns = {"implementation", "workers", "average_time", "speedup"}
    missing = required_columns.difference(data.columns)
    if missing:
        raise ValueError(f"Benchmark CSV is missing columns: {', '.join(sorted(missing))}")

    output_directory = INPUT_PATH.parent
    output_directory.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(10, 6))
    for implementation, group in data.groupby("implementation"):
        axis.plot(group["workers"], group["average_time"], marker="o", label=implementation)
    axis.set_xlabel("Worker/process count")
    axis.set_ylabel("Average execution time (seconds)")
    axis.set_title("ParallelLab-MPI execution time")
    axis.legend(title="Implementation")
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    figure.savefig(TIME_CHART_PATH, dpi=160)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(10, 6))
    for implementation, group in data[data["implementation"] != "sequential"].groupby("implementation"):
        axis.plot(group["workers"], group["speedup"], marker="o", label=implementation)
    axis.set_xlabel("Worker/process count")
    axis.set_ylabel("Speedup relative to sequential")
    axis.set_title("ParallelLab-MPI speedup")
    axis.legend(title="Implementation")
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    figure.savefig(SPEEDUP_CHART_PATH, dpi=160)
    plt.close(figure)
    print(f"Saved {TIME_CHART_PATH}")
    print(f"Saved {SPEEDUP_CHART_PATH}")


if __name__ == "__main__":
    main()
