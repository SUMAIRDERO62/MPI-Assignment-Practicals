const slides = [
  {
    kicker: "MPI-Assignment-Practicals",
    title: "From one process to a parallel system.",
    body: "A practical demonstration of MPI communication, distributed data, matrix operations, and measured performance.",
    note: "Teacher demonstration mode · 80% execution, 20% theory",
  },
  {
    kicker: "01 / Objective",
    title: "What problem does this project solve?",
    body: "The same workload should produce the same answer whether it runs sequentially, with local multiprocessing, or across MPI ranks.",
    code: "1² + 2² + ... + n²",
    note: "We measure correctness first, then compare the cost of each execution model.",
  },
  {
    kicker: "02 / Architecture",
    title: "A small system with clear boundaries.",
    body: "Standalone practicals demonstrate MPI. The benchmark engine records real CSV measurements. The static dashboard teaches and visualizes those recorded results.",
    code: "practicals/  →  src/parallel_lab/  →  results/  →  web/public/",
    note: "Vercel hosts the educational dashboard; MPI runs on a compatible host.",
  },
  {
    kicker: "03 / Practical 01",
    title: "Rank and total processes.",
    body: "Every process calls Get_rank() and Get_size(). Rank zero is the root used for coordination and reporting.",
    command: "mpiexec -n 4 python practicals\\practical_01_process_rank_size.py",
    output: "Process rank 0 of 4 total processes.\nRank 0 is the root process.",
  },
  {
    kicker: "04 / Practical 02",
    title: "Point-to-point communication.",
    body: "Rank 0 sends one tagged message. Rank 1 receives it from the explicit source.",
    command: "mpiexec -n 2 python practicals\\practical_02_send_receive.py",
    output: "Rank 0 sent a message to rank 1.\nRank 1 received: Hello from rank 0",
  },
  {
    kicker: "05 / Practical 03",
    title: "Scatterv handles uneven arrays.",
    body: "The root creates the array, Scatterv distributes chunks, and Gatherv rebuilds the original order.",
    command: "mpiexec -n 4 python practicals\\practical_03_array_distribution.py --length 11",
    output: "Rank 0 received [1, 2, 3]\nRank 3 received [10, 11]\nGathered array: [1, ..., 11]",
  },
  {
    kicker: "06 / Practical 04",
    title: "Reduce combines local sums.",
    body: "Each rank calculates independently. MPI.SUM combines the local values at rank 0, which checks the sequential reference.",
    command: "mpiexec -n 4 python practicals\\practical_04_parallel_array_sum.py --length 11",
    output: "Parallel sum: 66\nSequential check: 66\nVerified: parallel and sequential sums match.",
  },
  {
    kicker: "07 / Practical 05",
    title: "Matrix addition by rows.",
    body: "Rows are partitioned with Scatterv, added locally, and gathered into one result matrix.",
    command: "mpiexec -n 4 python practicals\\practical_05_parallel_matrix_addition.py",
    output: "Matrix shape: 5x3\nVerified: parallel and sequential matrix addition match.",
  },
  {
    kicker: "08 / Practical 06",
    title: "Matrix multiplication with Broadcast.",
    body: "A rows are distributed. Matrix B is broadcast to every rank. Each rank computes its result rows before Gatherv.",
    command: "mpiexec -n 4 python practicals\\practical_06_parallel_matrix_multiplication.py",
    output: "A: 5x3, B: 3x2\nVerified: parallel and sequential matrix multiplication match.",
  },
  {
    kicker: "09 / Concepts",
    title: "Collectives versus point-to-point.",
    body: "Send/receive names two participants. Broadcast shares one value. Scatter distributes pieces. Gather collects pieces. Reduce combines values.",
    code: "Bcast → everyone gets B\nScatterv → ranks get chunks\nReduce → root gets one combined value",
    note: "Barrier synchronizes ranks before a phase where timing must be comparable.",
  },
  {
    kicker: "10 / Browser lab",
    title: "The visualizer is an honest simulation.",
    body: "The dashboard animates the communication idea in a browser. It does not launch MPI processes and it does not create benchmark measurements.",
    note: "Real execution remains available through the PowerShell commands on the previous slides.",
  },
  {
    kicker: "11 / Benchmark lab",
    title: "Measured data, not invented numbers.",
    body: "The dashboard reads the checked-in benchmark CSV and presents execution time, sequential-baseline speedup, and efficiency.",
    image: "./charts/execution_time_comparison.png",
    note: "Timing boundaries are documented: multiprocessing includes pool lifecycle; MPI measures post-barrier local computation.",
  },
  {
    kicker: "12 / Matrix lab",
    title: "Try small matrices interactively.",
    body: "The browser calculator provides a sequential reference for addition and multiplication. The MPI practicals distribute the same operations by rows.",
    note: "Use this to explain dimensions before running Practical 05 or 06.",
  },
  {
    kicker: "13 / Quality",
    title: "Correctness is tested at multiple levels.",
    body: "Unit tests cover partitioning and validation. Full tests cover the existing benchmark engine. MPI subprocess runs verify 1, 2, and 4 ranks.",
    code: "python -m pytest -q\nmpiexec -n 4 python practicals\\practical_04_parallel_array_sum.py --length 11",
    note: "The expected result is checked against a sequential reference.",
  },
  {
    kicker: "14 / Conclusion",
    title: "What did we learn?",
    body: "Parallel programming is a coordination problem as much as a computation problem: partition work, communicate safely, reduce results, validate correctness, and measure honestly.",
    note: "Questions: Which operation needs a root? Why can uneven arrays require Scatterv? What does efficiency measure?",
  },
];

let current = 0;
const slide = document.querySelector("#slide");
const counter = document.querySelector("#slide-counter");
const progress = document.querySelector("#progress-bar");

function render() {
  const item = slides[current];
  const media = item.image ? `<img class="slide-image" src="${item.image}" alt="Measured benchmark chart">` : "";
  const command = item.command ? `<div class="terminal"><small>PowerShell</small><pre>${item.command}</pre></div>` : "";
  const output = item.output ? `<div class="terminal output"><small>Verified output</small><pre>${item.output}</pre></div>` : "";
  const code = item.code ? `<pre class="code-block">${item.code}</pre>` : "";
  slide.innerHTML = `<p class="kicker">${item.kicker}</p><h1>${item.title}</h1><p class="body">${item.body}</p>${media}${code}${command}${output}<p class="note">${item.note || ""}</p>`;
  counter.textContent = `${String(current + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`;
  progress.style.width = `${((current + 1) / slides.length) * 100}%`;
  document.querySelector("#previous").disabled = current === 0;
  document.querySelector("#next").textContent = current === slides.length - 1 ? "Restart ↻" : "Next →";
}

function move(step) {
  current = (current + step + slides.length) % slides.length;
  render();
}

document.querySelector("#previous").addEventListener("click", () => move(-1));
document.querySelector("#next").addEventListener("click", () => move(1));
document.querySelector("#fullscreen").addEventListener("click", () => {
  if (document.fullscreenElement) document.exitFullscreen();
  else document.documentElement.requestFullscreen();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight" || event.key === " ") move(1);
  if (event.key === "ArrowLeft") move(-1);
  if (event.key === "Home") { current = 0; render(); }
  if (event.key === "End") { current = slides.length - 1; render(); }
});
render();
