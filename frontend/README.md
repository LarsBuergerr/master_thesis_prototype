# DCAT-AP-DE Quality Analyzer — Frontend

React + TypeScript + Vite + Recharts UI for the analyzer backend, styled
after the official **GovData** portal frontend
([GovDataOfficial/GovData-Frontend](https://github.com/GovDataOfficial/GovData-Frontend))
so it can be embedded into GovData with minimal effort — same SCSS color
tokens, Noto Sans typography, Bootstrap 5 grid/breakpoints and component
class names (`design-box`, `gd-button`, `gd-tag`, `gd-table`, `alert`,
`gd-input`). See `docs/frontend_govdata_adoption.md` for the token mapping
and computed WCAG contrast evidence, and
`docs/frontend_design_literatur.md` for the underlying design literature.

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
  css/        GovData SCSS: main.scss + _color-tokens/_variables/_fonts/
              _mixins/_global (verbatim GovData tokens) and
              components/_gd-*.scss (GovData component styles) +
              components/_analyzer.scss (app-specific layout)
  hooks/      TanStack Query hooks (indicators, submit, job polling)
  components/
    UploadPanel, ConfigPanel, JobProgress
    results/  OverallScoreCard (gauge), DimensionRadar (with per-dimension
              scores), DimensionPanel (table), BatchComparison (good/bad
              spread), ResultsView
  lib/        GovData chart palette (theme.ts) + status helpers (status.ts)
```

The config panel is built dynamically from `GET /indicators`, so it always
matches the live indicator registry (weights, dimensions, graded flag).

## Styling notes

- Light-only, like GovData (the previous dark mode was removed).
- Charts keep Recharts (GovData's Chart.js 2.x is EOL) but use the exact
  colors of GovData's Metadatenqualität dashboard (magenta
  `#80004b`/`#e6cbda`) plus GovData status tokens for status-coded bars.
- Status is always encoded as color + icon glyph + text (WCAG 1.4.1); all
  color pairs are computed to meet WCAG AA (see docs).
