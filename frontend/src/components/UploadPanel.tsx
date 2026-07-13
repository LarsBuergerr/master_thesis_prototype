import { useRef } from "react";

interface Props {
  files: File[];
  onFilesChange: (files: File[]) => void;
  onSubmit: () => void;
  submitting: boolean;
}

export function UploadPanel({ files, onFilesChange, onSubmit, submitting }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);

  function handlePick(e: React.ChangeEvent<HTMLInputElement>) {
    const picked = e.target.files ? Array.from(e.target.files) : [];
    onFilesChange(picked);
  }

  return (
    <div className="panel">
      <h2>RDF-Dateien</h2>
      <input
        ref={inputRef}
        type="file"
        multiple
        accept=".rdf,.ttl,.xml,.n3,.nt,.jsonld"
        onChange={handlePick}
        style={{ display: "none" }}
      />
      <div className="row" style={{ gap: 8 }}>
        <button className="secondary" onClick={() => inputRef.current?.click()}>
          Dateien wählen
        </button>
        <span className="muted">{files.length} ausgewählt</span>
      </div>
      {files.length > 0 && (
        <ul className="muted" style={{ margin: "8px 0 0", paddingLeft: 18 }}>
          {files.map((f) => (
            <li key={f.name}>{f.name}</li>
          ))}
        </ul>
      )}
      <div style={{ marginTop: 12 }}>
        <button onClick={onSubmit} disabled={submitting || files.length === 0}>
          {submitting ? "Analysiere…" : "Analyse starten"}
        </button>
      </div>
    </div>
  );
}
