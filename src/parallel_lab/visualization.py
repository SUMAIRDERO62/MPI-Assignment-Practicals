"""Generate professional performance charts from validated benchmark data."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from parallel_lab.analysis import load_benchmark


ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "results" / "benchmark_results.csv"
ANALYSIS_PATH = ROOT / "results" / "performance_analysis.csv"
TIME_CHART_PATH = ROOT / "results" / "execution_time.png"
SPEEDUP_CHART_PATH = ROOT / "results" / "speedup.png"

IMPLEMENTATIONS = ("sequential", "multiprocessing", "mpi")
PARALLEL_IMPLEMENTATIONS = ("multiprocessing", "mpi")
COLORS = {
    "sequential": "#4C78A8",
    "multiprocessing": "#F58518",
    "mpi": "#54A24B",
}
ANALYSIS_REQUIRED_COLUMNS = {
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
}
NUMERIC_ANALYSIS_COLUMNS = {
    "workers",
    "average_time",
    "sequential_baseline_speedup",
    "sequential_baseline_efficiency",
    "implementation_relative_speedup",
    "implementation_relative_efficiency",
}


def _read_analysis(path: str | Path) -> pd.DataFrame:
    """Read and validate the generated performance analysis CSV."""
    analysis_path = Path(path)
    if not analysis_path.exists():
        raise FileNotFoundError(f"Performance analysis CSV not found: {analysis_path}")
    try:
        data = pd.read_csv(analysis_path)
    except (OSError, pd.errors.ParserError) as error:
        raise ValueError(f"Could not read performance analysis CSV: {analysis_path}") from error
    missing = ANALYSIS_REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"Performance analysis CSV is missing columns: {names}")
    if data.empty:
        raise ValueError("Performance analysis CSV contains no data rows")
    unsupported = set(data["implementation"].dropna().astype(str)) - set(IMPLEMENTATIONS)
    if unsupported:
        raise ValueError(
            f"Performance analysis CSV contains unsupported implementations: "
            f"{', '.join(sorted(unsupported))}"
        )
    for column in NUMERIC_ANALYSIS_COLUMNS:
        values = pd.to_numeric(data[column], errors="coerce")
        if values.isna().any() or not values.map(math.isfinite).all():
            raise ValueError(f"Performance analysis column contains invalid values: {column}")
        if column in {"workers", "average_time"} and (values <= 0).any():
            raise ValueError(f"Performance analysis column must be positive: {column}")
        data[column] = values
    data["workers"] = data["workers"].astype(int)
    return data.sort_values(["implementation", "workers"]).reset_index(drop=True)


def _style_axis(axis: plt.Axes, title: str, ylabel: str) -> None:
    axis.set_title(title, fontsize=15, fontweight="bold", pad=12)
    axis.set_xlabel("Worker/process count", fontsize=11)
    axis.set_ylabel(ylabel, fontsize=11)
    axis.grid(True, axis="y", alpha=0.25)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def _plot_metric(
    axis: plt.Axes,
    data: pd.DataFrame,
    column: str,
    label_prefix: str = "",
    linestyle: str = "-",
) -> None:
    for implementation in IMPLEMENTATIONS:
        group = data[data["implementation"] == implementation].sort_values("workers")
        if group.empty:
            continue
        axis.plot(
            group["workers"],
            group[column],
            marker="o",
            linewidth=2,
            linestyle=linestyle,
            color=COLORS[implementation],
            label=f"{label_prefix}{implementation}",
        )


def generate_execution_time_comparison(
    benchmark_data: pd.DataFrame,
    output_path: str | Path,
) -> Path:
    """Generate execution-time comparison chart from benchmark records."""
    figure, axis = plt.subplots(figsize=(11, 6.5))
    _plot_metric(axis, benchmark_data, "average_time")
    _style_axis(axis, "Execution Time Comparison", "Average execution time (seconds; lower is faster)")
    axis.legend(title="Implementation", frameon=False)
    figure.tight_layout()
    path = _save_figure(figure, output_path)
    return path


def generate_speedup_comparison(data: pd.DataFrame, output_path: str | Path) -> Path:
    """Generate sequential-baseline and implementation-relative speedup chart."""
    figure, axis = plt.subplots(figsize=(11, 6.5))
    _plot_metric(axis, data, "sequential_baseline_speedup", "Sequential baseline: ")
    _plot_metric(axis, data, "implementation_relative_speedup", "Implementation-relative: ", "--")
    _style_axis(axis, "Speedup Comparison", "Speedup (higher is better)")
    axis.legend(title="Metric definition", frameon=False, ncol=2)
    figure.tight_layout()
    return _save_figure(figure, output_path)


def generate_efficiency_comparison(data: pd.DataFrame, output_path: str | Path) -> Path:
    """Generate sequential-baseline and implementation-relative efficiency chart."""
    figure, axis = plt.subplots(figsize=(11, 6.5))
    _plot_metric(axis, data, "sequential_baseline_efficiency", "Sequential baseline: ")
    _plot_metric(axis, data, "implementation_relative_efficiency", "Implementation-relative: ", "--")
    axis.axhline(1.0, color="#666666", linewidth=1, linestyle=":", label="Ideal efficiency")
    _style_axis(axis, "Parallel Efficiency Comparison", "Efficiency (1.0 = ideal linear efficiency)")
    axis.legend(title="Metric definition", frameon=False, ncol=2)
    figure.tight_layout()
    return _save_figure(figure, output_path)


def generate_scalability_comparison(data: pd.DataFrame, output_path: str | Path) -> Path:
    """Generate implementation-relative scalability chart with an ideal reference."""
    figure, axis = plt.subplots(figsize=(11, 6.5))
    parallel = data[data["implementation"].isin(PARALLEL_IMPLEMENTATIONS)]
    for implementation in PARALLEL_IMPLEMENTATIONS:
        group = parallel[parallel["implementation"] == implementation].sort_values("workers")
        axis.plot(
            group["workers"],
            group["implementation_relative_speedup"],
            marker="o",
            linewidth=2,
            color=COLORS[implementation],
            label=implementation,
        )
    workers = sorted(parallel["workers"].unique())
    if workers:
        axis.plot(workers, workers, color="#666666", linewidth=1.5, linestyle=":", label="Ideal linear scaling")
    _style_axis(axis, "Scalability Comparison", "Implementation-relative speedup (higher is better)")
    axis.legend(frameon=False)
    figure.tight_layout()
    return _save_figure(figure, output_path)


def generate_mpi_vs_multiprocessing(
    data: pd.DataFrame,
    output_path: str | Path,
) -> Path:
    """Generate matched-worker MPI and multiprocessing execution comparison."""
    parallel = data[data["implementation"].isin(PARALLEL_IMPLEMENTATIONS)]
    pivot = parallel.pivot_table(index="workers", columns="implementation", values="average_time", aggfunc="first")
    pivot = pivot.dropna(subset=list(PARALLEL_IMPLEMENTATIONS)).sort_index()
    if pivot.empty:
        raise ValueError("No matching MPI and multiprocessing worker counts are available")

    figure, axis = plt.subplots(figsize=(11, 6.5))
    for implementation in PARALLEL_IMPLEMENTATIONS:
        axis.plot(
            pivot.index,
            pivot[implementation],
            marker="o",
            linewidth=2,
            color=COLORS[implementation],
            label=implementation,
        )
    for workers, row in pivot.iterrows():
        faster = "MPI faster" if row["mpi"] < row["multiprocessing"] else "Multiprocessing faster"
        axis.annotate(
            faster,
            (workers, min(row["mpi"], row["multiprocessing"])),
            textcoords="offset points",
            xytext=(0, -18),
            ha="center",
            fontsize=8,
            color="#444444",
        )
    _style_axis(axis, "MPI vs Multiprocessing Comparison", "Average execution time (seconds; lower is faster)")
    axis.legend(title="Implementation", frameon=False)
    figure.tight_layout()
    return _save_figure(figure, output_path)


def _save_figure(
    figure: plt.Figure,
    output_path: str | Path,
    dpi: int = 180,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=dpi, format="png")
    plt.close(figure)
    return path


def _generate_legacy_charts(benchmark_data: pd.DataFrame, output_directory: Path) -> None:
    """Preserve the original execution-time and speedup chart outputs."""
    sequential_time = float(
        benchmark_data.loc[
            (benchmark_data["implementation"] == "sequential")
            & (benchmark_data["workers"] == 1),
            "average_time",
        ].iloc[0]
    )
    figure, axis = plt.subplots(figsize=(10, 6))
    for implementation, group in benchmark_data.groupby("implementation"):
        axis.plot(group["workers"], group["average_time"], marker="o", label=implementation)
    axis.set_xlabel("Worker/process count")
    axis.set_ylabel("Average execution time (seconds)")
    axis.set_title("ParallelLab-MPI execution time")
    axis.legend(title="Implementation")
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    _save_figure(figure, output_directory / "execution_time.png", dpi=160)

    figure, axis = plt.subplots(figsize=(10, 6))
    for implementation in PARALLEL_IMPLEMENTATIONS:
        group = benchmark_data[benchmark_data["implementation"] == implementation].sort_values("workers")
        axis.plot(
            group["workers"],
            sequential_time / group["average_time"],
            marker="o",
            label=implementation,
        )
    axis.set_xlabel("Worker/process count")
    axis.set_ylabel("Speedup relative to sequential")
    axis.set_title("ParallelLab-MPI speedup")
    axis.legend(title="Implementation")
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    _save_figure(figure, output_directory / "speedup.png", dpi=160)


def generate_all_charts(
    benchmark_path: str | Path = INPUT_PATH,
    analysis_path: str | Path = ANALYSIS_PATH,
    output_directory: str | Path | None = None,
) -> dict[str, Path]:
    """Generate five Phase 6 charts and preserve the two legacy chart files."""
    benchmark_records = load_benchmark(benchmark_path)
    benchmark_data = pd.DataFrame(benchmark_records)
    analysis_data = _read_analysis(analysis_path)
    output_dir = Path(output_directory) if output_directory is not None else Path(benchmark_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    _generate_legacy_charts(benchmark_data, output_dir)

    paths = {
        "execution_time_comparison": output_dir / "execution_time_comparison.png",
        "speedup_comparison": output_dir / "speedup_comparison.png",
        "efficiency_comparison": output_dir / "efficiency_comparison.png",
        "scalability_comparison": output_dir / "scalability_comparison.png",
        "mpi_vs_multiprocessing": output_dir / "mpi_vs_multiprocessing.png",
    }
    generate_execution_time_comparison(benchmark_data, paths["execution_time_comparison"])
    generate_speedup_comparison(analysis_data, paths["speedup_comparison"])
    generate_efficiency_comparison(analysis_data, paths["efficiency_comparison"])
    generate_scalability_comparison(analysis_data, paths["scalability_comparison"])
    generate_mpi_vs_multiprocessing(analysis_data, paths["mpi_vs_multiprocessing"])
    return paths


def main(argv: list[str] | None = None) -> None:
    """Generate the five professional charts and preserve legacy charts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, default=INPUT_PATH)
    parser.add_argument("--analysis", type=Path, default=ANALYSIS_PATH)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    args = parser.parse_args(argv)
    for path in generate_all_charts(args.benchmark, args.analysis, args.output_dir).values():
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
