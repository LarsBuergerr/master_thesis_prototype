# DCAT-AP-DE Quality Analyzer — Frontend

React + TypeScript + Vite + Recharts UI for the analyzer backend.

## Prerequisites

- Node.js ≥ 18 (not installed in the dev container — run this on a machine with Node)
- The backend running: `uvicorn backend.app:app --reload --port 8000` (from the repo root)

## Setup

```bash
cd frontend
npm install
cp .env.example .env   # optional; defaults to http://localhost:8000
npm run dev            # http://localhost:5173
```

`npm run build` produces a static bundle in `dist/`; `npm run typecheck` runs `tsc`.

## How it talks to the backend

- `VITE_API_BASE` (default `http://localhost:8000`) — the FastAPI base URL.
  CORS for `:5173` is already enabled there. Alternatively set it to `/api` to
  use the Vite dev proxy (see `vite.config.ts`).
- Flow: upload files + config → `POST /analyze` → `{job_id}` → the
  `useJob` hook polls `GET /jobs/{id}` every second until `done`/`error`.

## Structure

```
src/
  api/        types (mirror backend schemas) + axios client
  hooks/      TanStack Query hooks (indicators, submit, job polling)
  components/
    UploadPanel, ConfigPanel, JobProgress
    results/  OverallScoreCard (gauge), DimensionRadar, IndicatorBarChart,
              DimensionPanel (table), BatchComparison (good/bad spread),
              ResultsView
  lib/        status/grade colors + formatting
```

The config panel is built dynamically from `GET /indicators`, so it always
matches the live indicator registry (weights, dimensions, graded flag).
