# Deployment

The dashboard is a static site in `web/public/`. It can be hosted by Vercel
or any static hosting provider without Python or MPI.

The root [`vercel.json`](../vercel.json) routes `/` and static assets into
`web/public/`, and exposes `/presentation` as the teacher presentation page.
No build command, package installation, backend, or environment variable is
required.

For a local preview, serve the directory with any static file server:

```powershell
python -m http.server 8000 --directory web\public
```

Open `http://localhost:8000`. The dashboard reads the checked-in
`data/benchmark_results.csv` and chart images from `web/public/`.

## Vercel deployment

From the repository root, after installing and authenticating the Vercel CLI:

```powershell
npm install --global vercel
vercel login
vercel link
vercel
```

Confirm that the linked project is the intended
`MPI-Assignment-Practicals` project before deploying. Verify `/`,
`/presentation`, `/data/benchmark_results.csv`, and one chart URL in the
preview. Promote to production only after the preview is correct:

```powershell
vercel --prod
```

The Vercel CLI and account authentication were not available during local
validation, so no preview or production deployment is claimed here.

Real MPI execution requires a host with a matching MPI runtime and
`mpi4py`. Vercel serverless functions must not be used to launch MPI child
processes. Run the six practicals and benchmark commands locally, on a
university lab machine, or on an MPI cluster.
