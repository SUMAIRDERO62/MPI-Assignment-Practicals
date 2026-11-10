# Deployment

The dashboard is a static site in `web/public/`. It can be hosted by Vercel
or any static hosting provider without Python or MPI.

For a local preview, serve the directory with any static file server:

```powershell
python -m http.server 8000 --directory web\public
```

Open `http://localhost:8000`. The dashboard reads the checked-in
`data/benchmark_results.csv` and chart images from `web/public/`.

Real MPI execution requires a host with a matching MPI runtime and
`mpi4py`. Vercel serverless functions must not be used to launch MPI child
processes. Run the six practicals and benchmark commands locally, on a
university lab machine, or on an MPI cluster.
