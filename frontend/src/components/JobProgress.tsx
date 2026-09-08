import type { JobDetail } from "../api/types";

export function JobProgress({ job }: { job: JobDetail }) {
  const { done, total, current_file } = job.progress;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  return (
    <div className="design-box design-box-padding">
      <div className="gd-row between">
        <h2 style={{ marginBottom: 0 }}>
          {job.status === "running" ? "Analyse läuft…" : `Status: ${job.status}`}
        </h2>
        <span className="muted">
          {done}/{total}
        </span>
      </div>
      <div className="progress-track" style={{ marginTop: 12 }}>
        <div className="progress-bar" style={{ width: `${pct}%` }} />
      </div>
      {current_file && (
        <p className="muted" style={{ marginBottom: 0 }}>
          Aktuell: {current_file}
        </p>
      )}
      {job.error && (
        <div className="alert gd-alert-danger" role="alert" style={{ marginTop: 12 }}>
          {job.error}
        </div>
      )}
    </div>
  );
}
