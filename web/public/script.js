const DATA_PATH = "./data/benchmark_results.csv";

const implementationLabels = {
  sequential: "Sequential",
  multiprocessing: "Multiprocessing",
  mpi: "MPI",
};

const implementationColors = {
  sequential: "#66e4df",
  multiprocessing: "#ffaf6d",
  mpi: "#a995ff",
};

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  if (lines.length < 2) throw new Error("The benchmark CSV contains no data rows.");
  const headers = lines[0].split(",").map((header) => header.trim());
  return lines.slice(1).map((line) => {
    const values = line.split(",");
    return headers.reduce((record, header, index) => {
      record[header] = values[index]?.trim() ?? "";
      return record;
    }, {});
  });
}

function numericRows(rows) {
  const required = ["implementation", "workers", "n", "repetitions", "result", "average_time"];
  if (!rows.length || required.some((column) => !(column in rows[0]))) {
    throw new Error("The benchmark CSV is missing required columns.");
  }
  return rows.map((row) => {
    const parsed = { ...row, workers: Number(row.workers), n: Number(row.n), repetitions: Number(row.repetitions), result: BigInt(row.result), average_time: Number(row.average_time) };
    if (!Number.isFinite(parsed.workers) || !Number.isFinite(parsed.average_time) || parsed.workers < 1 || parsed.average_time <= 0) {
      throw new Error("The benchmark CSV contains invalid numeric values.");
    }
    return parsed;
  }).sort((a, b) => a.implementation.localeCompare(b.implementation) || a.workers - b.workers);
}

function formatSeconds(value) {
  return `${value.toFixed(3)} s`;
}

function formatSpeedup(value) {
  return `${value.toFixed(2)}×`;
}

function setMetric(name, value) {
  const element = document.querySelector(`[data-metric="${name}"]`);
  if (element) element.textContent = value;
}

function renderDashboard(rows) {
  const sequential = rows.find((row) => row.implementation === "sequential" && row.workers === 1);
  if (!sequential) throw new Error("The sequential baseline is missing.");
  const validImplementations = new Set(["sequential", "multiprocessing", "mpi"]);
  if (rows.some((row) => !validImplementations.has(row.implementation))) throw new Error("The benchmark includes an unsupported implementation.");

  const enriched = rows.map((row) => ({ ...row, speedup: sequential.average_time / row.average_time, efficiency: sequential.average_time / row.average_time / row.workers }));
  const fastest = enriched.reduce((best, row) => row.average_time < best.average_time ? row : best, enriched[0]);
  const bestSpeedup = enriched.reduce((best, row) => row.speedup > best.speedup ? row : best, enriched[0]);

  setMetric("fastest-time", formatSeconds(fastest.average_time));
  setMetric("fastest-detail", `${implementationLabels[fastest.implementation]} · ${fastest.workers} worker${fastest.workers === 1 ? "" : "s"}`);
  setMetric("best-speedup", formatSpeedup(bestSpeedup.speedup));
  setMetric("best-speedup-detail", `${implementationLabels[bestSpeedup.implementation]} · ${bestSpeedup.workers} workers`);
  setMetric("workload", `${(sequential.n / 1000000).toFixed(0)}M`);
  setMetric("result", sequential.result.toLocaleString("en-US"));

  const table = document.querySelector("#benchmark-table");
  table.innerHTML = enriched.map((row) => `
    <tr>
      <td><span class="impl-pill" style="--pill-color: ${implementationColors[row.implementation]}">${implementationLabels[row.implementation]}</span></td>
      <td>${row.workers}</td>
      <td>${formatSeconds(row.average_time)}</td>
      <td>${formatSpeedup(row.speedup)}</td>
      <td>${row.efficiency.toFixed(3)}</td>
    </tr>`).join("");
}

function showError(message) {
  const status = document.querySelector("#data-status");
  const error = document.querySelector("#error-state");
  status.hidden = true;
  error.hidden = false;
  error.textContent = `Unable to load benchmark data: ${message}`;
  document.querySelector("#benchmark-table").innerHTML = `<tr><td colspan="5" class="table-loading">Benchmark data unavailable.</td></tr>`;
}

async function loadBenchmarkData() {
  try {
    const response = await fetch(DATA_PATH, { cache: "no-store" });
    if (!response.ok) throw new Error(`request failed (${response.status})`);
    const rows = numericRows(parseCsv(await response.text()));
    renderDashboard(rows);
    const status = document.querySelector("#data-status");
    status.classList.add("loaded");
    status.innerHTML = '<span class="loading-spinner"></span> Live from benchmark_results.csv';
  } catch (error) {
    showError(error.message);
  }
}

function parseMatrix(value) {
  const rows = value.trim().split(/\r?\n/).map((line) => line.split(",").map((item) => Number(item.trim())));
  if (!rows.length || rows.some((row) => !row.length || row.some((item) => !Number.isFinite(item)))) {
    throw new Error("Matrices must contain comma-separated numbers.");
  }
  const columns = rows[0].length;
  if (rows.some((row) => row.length !== columns)) throw new Error("Every matrix row must have the same number of columns.");
  return rows;
}

function formatMatrix(matrix) {
  return matrix.map((row) => row.map((value) => Number.isInteger(value) ? String(value) : value.toFixed(3)).join("  ")).join("\n");
}

function matrixAdd(left, right) {
  if (left.length !== right.length || left[0].length !== right[0].length) throw new Error("Addition requires matrices with the same shape.");
  return left.map((row, i) => row.map((value, j) => value + right[i][j]));
}

function matrixMultiply(left, right) {
  if (left[0].length !== right.length) throw new Error("Multiplication requires A columns to equal B rows.");
  return left.map((row) => right[0].map((_, column) => row.reduce((sum, value, index) => sum + value * right[index][column], 0)));
}

function setupMatrixLab() {
  const output = document.querySelector("#matrix-output");
  const calculate = (operation) => {
    try {
      const left = parseMatrix(document.querySelector("#matrix-a").value);
      const right = parseMatrix(document.querySelector("#matrix-b").value);
      const result = operation === "add" ? matrixAdd(left, right) : matrixMultiply(left, right);
      output.textContent = `Sequential reference result:\n${formatMatrix(result)}`;
      output.classList.remove("matrix-error");
    } catch (error) {
      output.textContent = error.message;
      output.classList.add("matrix-error");
    }
  };
  document.querySelector("#add-matrices").addEventListener("click", () => calculate("add"));
  document.querySelector("#multiply-matrices").addEventListener("click", () => calculate("multiply"));
}

function setupVisualizer() {
  const output = document.querySelector("#simulation-output");
  document.querySelector("#run-simulation").addEventListener("click", () => {
    const type = document.querySelector("#simulation-select").value;
    const messages = {
      scatter: ["Rank 0 owns [1, 2, 3, 4, 5, 6, 7].", "Scatterv partitions the values as [1, 2], [3, 4], [5, 6], [7].", "Every rank computes on its local chunk."],
      reduce: ["Rank 0 computes 3, rank 1 computes 7, rank 2 computes 11.", "Reduce with MPI.SUM combines local values at rank 0.", "Root receives the final total: 21."],
      send: ["Rank 0 prepares a tagged message.", "MPI sends it directly to rank 1.", "Rank 1 receives and verifies the message."]
    };
    output.innerHTML = messages[type].map((message, index) => `<div class="simulation-step"><span>${String(index + 1).padStart(2, "0")}</span><p>${message}</p></div>`).join("");
  });
}

document.querySelectorAll("section").forEach((section) => {
  const observer = new IntersectionObserver((entries, instance) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("reveal");
        instance.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  observer.observe(section);
});

setupMatrixLab();
setupVisualizer();
loadBenchmarkData();
