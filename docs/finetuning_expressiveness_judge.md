# Plan: Fine-getuntes lokales Modell für die Expressiveness-Bewertung

> Ziel: den LLM-gestützten *Expressiveness*-Judge durch ein **kleines, lokal
> fine-getuntes Modell** ersetzen (Distillation aus einem Frontier-Modell) und
> empirisch zeigen, ob es das große Modell auf diesem Nischen-Task einholt –
> bei besserer Reproduzierbarkeit, ohne API-Kosten und ohne Datenabfluss.

---

## TL;DR / Empfehlung

- **Einziger sinnvoller Fine-Tuning-Kandidat im Prototyp:** der Expressiveness-Judge.
  Die anderen vier Dimensionen sind deterministisch/regelbasiert – dort wäre ein
  ML-Modell überflüssig und sogar schädlich (nicht-deterministisch, teurer).
- **Methode der Wahl:** Knowledge Distillation – ein starkes Modell (Sonnet/GPT)
  erzeugt Labels, ein kleines lokales Modell (7–8B, LoRA) lernt sie nachzuahmen.
- **Aufwand niedrig**, weil drei Dinge schon existieren:
  1. eine saubere LLM-Naht (`llm`-Parameter, duck-typed),
  2. ein lokaler Inferenz-Pfad (`provider: "local"`, llama.cpp),
  3. eine Mess-Methodik (Notebook `09_run_aggregate_stats.ipynb`, Modellvergleich).

---

## Empfohlene Reihenfolge (Master-Roadmap)

> Kernprinzip: **erst die Messlatte, dann den Prompt, dann erst Labels & Training.**
> Labels vor dem Einfrieren des Prompts zu erzeugen ist rausgeworfenes Geld
> (inkonsistente Label-Verteilung). Frei wiederverwendbar sind die **Inputs**
> (Datensätze), nicht die alten Labels.

### Phase 0 — Mini-Gold-Set anlegen *(Messlatte)*
- **Ziel:** ein objektiver Maßstab, um Prompt- *und* Modell-Qualität zu messen.
- **Tun:** 20–50 *distinkte* Datensätze von Hand bewerten (6 Kriterien je
  `status`/`score`, kurze Begründung). Spektrum abdecken: gute, mittlere, kaputte
  (`data/extreme_cases*` einbeziehen). Idealerweise 2 Annotatoren → Agreement messen.
- **Output:** `data/gold/expressiveness_gold.jsonl` (held-out, fließt **nie** ins Training).
- **Gate:** Inter-Annotator-Agreement akzeptabel; sonst Kriterien-Definitionen schärfen.

### Phase 1 — Prompt-Engineering + Baselines
- **Ziel:** den **Teacher**-Prompt so gut/konsistent wie möglich machen (jedes spätere
  Label erbt diese Qualität) und die „ohne Fine-Tuning"-Baselines festnageln.
- **Tun:** Prompt iterativ gegen das Gold-Set optimieren (~10–30 diverse Beispiele,
  inkl. der bekannten Fehlerfälle aus vorhandenen `run_outputs`). Parallel messen:
  (a) Teacher gegen Gold, (b) **lokales Basismodell nur mit Prompt/Few-Shot** als
  Baseline „C".
- **Output:** eingefrorener Prompt (versioniert), Baseline-Kennzahlen.
- **Gate:** Teacher trifft das Gold-Set gut genug, um als Label-Quelle zu taugen.

### Phase 2 — Daten beschaffen & Prompt einfrieren
- **Ziel:** genug **diverse, distinkte** Inputs (Diversität > Menge).
- **Tun:** über die vorhandene Pipeline (`playground/notebooks/01_fetch_metadata.ipynb`,
  CKAN-Fetch, `catalog_distributions.csv`) ein paar hundert distinkte Records ziehen;
  die Inputs aus bestehenden Läufen wiederverwenden. **Prompt ab hier nicht mehr ändern.**
- **Output:** Liste der zu labelnden Datensätze (train/val/test **datensatz-disjunkt**).

### Phase 3 — Trainingslabels erzeugen *(Distillation)*
- **Ziel:** Labels in Volumen, kostengünstig.
- **Tun:** alle Datensätze mit dem **eingefrorenen** Prompt labeln. **Kein Opus** —
  Sonnet/GPT-mid genügt (~$0,035–0,04/Call). Optional gestuft: günstiges Modell für
  die Masse, Frontier nur für strittige/schwere Fälle (dort, wo Sonnet & GPT divergieren).
  Bestehende Inputs mit finalem Prompt **neu** labeln (~$5 für ~150).
- **Output:** `data/ft/expressiveness_train.jsonl` (Format siehe
  [Datensatz-Format](#2-datensatz-format-jsonl-chat--structured)).
- **Richtwert Menge:** Start **~300–500** distinkte Labels; nur nachlegen, wenn die
  Eval es verlangt (siehe Phase 6). Frontier-Budget einmalig ~€5–15.

### Phase 4 — Fine-Tuning
- **Ziel:** kleines lokales Modell, das den Teacher imitiert.
- **Tun:** QLoRA auf Qwen2.5-7B / Llama-3.1-8B (Details siehe
  [Training](#4-training)). Loss nur auf der Completion, wenige Epochen.
- **Output:** gemergtes GGUF-Modell, am llama.cpp-Server serviert
  ([Serving](#5-serving--einbindung)).

### Phase 5 — Evaluation
- **Ziel:** belegen, ob das FT-Modell Teacher-Niveau erreicht.
- **Tun:** vollen Run mit dem FT-Modell fahren; im Notebook
  `playground/notebooks/09_run_aggregate_stats.ipynb` als **4. Modell** in
  `MODEL_RUNS` aufnehmen. Zusätzlich gegen das **Gold-Set** messen
  (FT vs. Gold *und* Teacher vs. Gold).
- **Zielmetriken:** MAE(FT, Teacher) ≈ Teacher-Run-zu-Run (~0.03); Bias ≈ 0; hoher
  Pearson; FT-zu-FT-Reproduzierbarkeit ≤ Teacher.

### Phase 6 — Iterieren *(Active Learning)*
- **Ziel:** gezielt verbessern statt blind mehr Daten kaufen.
- **Tun:** Fälle finden, wo FT am stärksten vom Gold/Teacher abweicht → genau dort
  Labels nachlegen (schwere/Edge-Fälle) → zurück zu Phase 4.

| Phase | Output | Frontier-Kosten |
|---|---|---|
| 0 Gold-Set | `expressiveness_gold.jsonl` | 0 € (Handarbeit) |
| 1 Prompt | eingefrorener Prompt + Baselines | < €1 |
| 2 Daten | Datensatz-Liste, Splits | 0 € |
| 3 Labels | `expressiveness_train.jsonl` | ~€5–15 |
| 4 Fine-Tune | GGUF-Modell | 0 € (lokal) |
| 5 Eval | Notebook-Vergleich + Gold-Report | 0 € (lokal) |
| 6 Iterieren | mehr Labels für Edge-Fälle | gering, gezielt |

---

## Warum genau dieser Task passt

1. **Eng umrissene, strukturierte Aufgabe.** Das Modell muss nicht „alles können",
   sondern exakt 6 Kriterien bewerten und ein festes Schema (`ExpressivenessAssessment`,
   `src/extraction/semantic_assessment.py`) füllen. Fine-Tuning glänzt bei schmalen
   Tasks mit fixem Output – ein 7–8B-Modell kann hier ein generelles Frontier-Modell
   durchaus einholen.
2. **Trainingsdaten-Pipeline existiert bereits.** Jeder Lauf erzeugt Paare
   `(metadata JSON → ExpressivenessAssessment)`. Siehe Abschnitt
   [Trainingsdaten](#1-trainingsdatensatz-aus-run_outputs-bauen).
3. **Reproduzierbarkeit ist gemessen und ein offenes Problem.** Run-zu-Run-MAE ~0.03
   (Sonnet, gleiches Modell), Modell-zu-Modell-MAE 0.08–0.11. Ein deterministisch
   (Temp 0) bedientes, auf *unsere* Definition kalibriertes Modell kann stabiler sein.
4. **Praktische Hebel für die Thesis:** kein API-Key/Netz, **keine Per-Call-Kosten**,
   On-Prem-Inferenz – bei deutschen Behörden-Metadaten ist **Datensouveränität** ein
   echtes, verteidigbares Argument.

### Wo Fine-Tuning NICHT sinnvoll ist

- Die deterministischen Dimensionen (findability, accessibility, … – siehe
  `src/scoring/indicators/`): regelbasiert, sollen exakt/reproduzierbar bleiben.
- Metadaten-*Reparatur* (bessere Titel/Beschreibungen generieren) wäre fine-tune-bar,
  ist aber Generierung statt Bewertung, schwer zu evaluieren und sprengt den Scope.
  → bewusst out of scope, höchstens Ausblick.

---

## Die Integrations-Naht (wie ein eigenes Modell andockt)

Der gesamte „Agent" wird nur über eine duck-typed Methodenkette benutzt
(`src/extraction/semantic_assessment.py`):

```text
structured = llm.with_structured_output(ExpressivenessAssessment, method="function_calling", include_raw=True)
result     = structured.invoke(messages)      # -> {"parsed": ExpressivenessAssessment, "raw": ...}
context.semantic_assessment = result["parsed"]
```

Daraus folgen die Andock-Punkte (kein Pipeline-Umbau nötig):

- **Inferenz im echten Run:** Das fine-getunte Modell als OpenAI-kompatiblen Endpoint
  (llama.cpp / vLLM) servieren und über den bestehenden `provider: "local"`-Pfad
  (`create_local_llm`, `src/main.py`) einbinden. Nur `base_url`/`model` in der
  State-Config setzen.
- **Optionaler `provider: "ft"`-Zweig** in `build_llm`, falls ein eigener Adapter/
  andere Defaults gewünscht sind.
- **Tests/Offline:** ein duck-typed Fake mit `with_structured_output().invoke()`
  reicht, um die ganze Dimension ohne Netz zu durchlaufen.

> Wichtig: Das fine-getunte Modell muss **valides JSON nach `ExpressivenessAssessment`**
> liefern (6 Kriterien je `{status, score, reasoning, findings}` + `overall_summary`).
> Bei llama.cpp/vLLM am besten per **grammar / JSON-Schema-constrained decoding**
> erzwingen, damit `with_structured_output(...)` robust parst.

---

## Umsetzungs-Optionen (gereiht)

| Option | Idee | Aufwand | Risiko | Empfehlung |
|---|---|---|---|---|
| **A. Distillation + LoRA** | Frontier-Modell labelt, kleines lokales Modell (Qwen2.5-7B / Llama-3.1-8B) wird per LoRA/QLoRA getunt | mittel | niedrig | **erste Wahl** |
| B. Full Fine-Tune | gesamtes Modell trainieren | hoch | mittel (Overfit, GPU) | nur wenn LoRA klar zu schwach |
| C. Nur Prompt/Few-Shot am lokalen Basismodell | kein Training, nur Prompt-Engineering | sehr niedrig | – | **als Baseline** zwingend mitmessen |
| D. Reward-/Präferenz-Tuning (DPO) | aus paarweisen Urteilen | hoch | hoch | Ausblick, nicht Kern |

**Strategie:** C als Baseline messen → A umsetzen → A gegen C und gegen Sonnet/GPT/Qwen
vergleichen. Die Differenz „A − C" zeigt den reinen Fine-Tuning-Effekt.

---

## Schritt-für-Schritt-Plan

### 1. Trainingsdatensatz aus `run_outputs` bauen

Pro Datensatz-Ordner liegen die nötigen Teile bereits vor:

- **Input (Prompt + Metadaten-JSON):** `openai.log` → `json_data.messages`
  (`messages[0]` = System-Prompt, `messages[1]` = User-Prompt inkl. eingebettetem
  `to_agent_json()`-Payload).
- **Label (strukturiertes Urteil):** `result.json` →
  `by_dimension.expressiveness.indicators[*].details`
  (`criterion`, `llm_status`, `score`, `findings`, `message_de` = reasoning) plus
  `overall_summary`.

Daraus lässt sich das vollständige `ExpressivenessAssessment` als Ziel-JSON
rekonstruieren. Alternativ den Input frisch via `DatasetContext.to_agent_json()`
aus der Quell-`.rdf` (`data/<sample>/*.rdf`) erzeugen – robuster als Log-Parsing.

**Datenquellen für Labels:** möglichst aus dem **stärksten** Modell (Sonnet) als
Teacher; für Diversität die `data/extreme_cases*`-Sets mitnehmen (decken die
Score-Ränder ab).

**Skript-Skizze:** `playground/scripts/build_ft_dataset.py`
```text
für jeden run_dir (Teacher-Modell):
    für jeden dataset-ordner:
        input  = lade messages aus openai.log  (oder to_agent_json aus .rdf)
        label  = baue ExpressivenessAssessment aus result.json[by_dimension.expressiveness]
        schreibe JSONL-Zeile {messages:[system,user], completion: label_json}
dedupe + train/val/test split (datensatz-disjunkt!, nicht datei-disjunkt)
```

### 2. Datensatz-Format (JSONL, chat + structured)

```text
{"messages": [
   {"role": "system", "content": "<AUDITOR_PROMPT[de]>"},
   {"role": "user",   "content": "Bewerte ... Metadaten (JSON):\n<to_agent_json>"}
 ],
 "response": { ...valides ExpressivenessAssessment-JSON... }}
```

- **Identischer System-/User-Prompt wie im Prototyp** verwenden (Konsistenz Train↔Inferenz).
- Ziel ist exakt das JSON, das `with_structured_output` erwartet.

### 3. Basismodell & Methode

- Basismodell: **Qwen2.5-7B-Instruct** oder **Llama-3.1-8B-Instruct** (gutes
  Deutsch, JSON-fähig, läuft lokal). Passt zum schon getesteten `qwen3-5`-Run.
- **QLoRA** (4-bit) – trainierbar auf einer einzelnen 16–24 GB GPU.
- Frameworks: `axolotl` oder `unsloth` (schnell, wenig Boilerplate).

### 4. Training

- Wenige Epochen (1–3), kleine LoRA-Rank (16–32), Loss nur auf der Completion.
- Train/Val getrennt **nach Datensatz** (nicht nach `_02/_03`-Wiederholung), sonst
  leakt der quasi-gleiche Datensatz in den Val-Split.
- Checkpoint nach Val-Loss + erstem Mini-Eval (siehe Schritt 6) wählen.

### 5. Serving / Einbindung

- LoRA mergen → GGUF exportieren → **llama.cpp server** (`/v1`, OpenAI-kompatibel).
- In einer State-Config (`conf/state/*.yaml`):
  ```text
  llm:
    enabled: true
    provider: "local"
    base_url: "http://localhost:8080/v1"
    model: "expr-judge-ft"
    temperature: 0.0
  ```
- **JSON-Schema/Grammar-Constraint** am Server aktivieren, damit der Output
  garantiert dem Schema folgt.

### 6. Evaluation (an bestehende Mess-Methodik andocken)

- Einen vollen Run mit dem FT-Modell fahren → erzeugt `run_aggregate.json` wie gehabt.
- Im Notebook `playground/notebooks/09_run_aggregate_stats.ipynb` das FT-Modell als
  **viertes Modell** in `MODEL_RUNS` aufnehmen → liefert automatisch:
  - Pro-Modell-Kennzahlen (mean, stdev, Noten),
  - paarweisen Datei-für-Datei-Vergleich (MAE, Bias, Pearson) **FT vs. Teacher**.
- **Zielmetriken:**
  - MAE(FT, Teacher) möglichst nahe an MAE(Teacher-Run-zu-Run) ≈ 0.03 → „so gut wie
    das große Modell mit sich selbst".
  - Bias ≈ 0 (keine systematische Über-/Unterbewertung).
  - Pearson hoch (gleiche Rangordnung der Datensätze).
  - Reproduzierbarkeit FT-zu-FT (Temp 0): sollte ≤ Teacher sein.

---

## Gold-Standard / Label-Problem (ehrlich)

- Distillation lernt die **Biases des Teachers** mit – der Student kann den Teacher
  per Definition nur *approximieren*, nicht *übertreffen*.
- Für eine belastbare Aussage braucht es einen **unabhängigen, human-annotierten
  Test-Satz** (z.B. 30–50 Datensätze, ggf. 2 Annotatoren + Inter-Annotator-Agreement).
  Das ist Zusatzaufwand, aber ein eigenständiger wissenschaftlicher Beitrag und der
  einzige Weg, „gut" objektiv zu belegen.
- Mindestens: ein kleines, manuell geprüftes Sanity-Set, um grobe Fehlkalibrierung
  zu erkennen.

---

## Risiken & Gegenmaßnahmen

| Risiko | Gegenmaßnahme |
|---|---|
| Zu wenige/zu einseitige Labels | mehrere Teacher-Läufe + `extreme_cases` einbeziehen; Score-Verteilung prüfen |
| Modell bricht JSON-Schema | constrained decoding (grammar/JSON-Schema) am Server |
| Overfitting auf wenige Datensätze | datensatz-disjunkter Split, wenige Epochen, kleine LoRA-Rank |
| Teacher-Bias als „Wahrheit" | human-annotierter Test-Satz als unabhängiger Maßstab |
| Deutsch-Qualität des Basismodells | Qwen2.5/Llama-3.1 wählen; reasoning/findings im Eval stichprobenartig lesen |

---

## Aufwandsschätzung (grob)

| Schritt | Aufwand |
|---|---|
| Datensatz-Extraktion aus `run_outputs` | 0.5–1 Tag |
| QLoRA-Training + Iteration | 1–2 Tage (inkl. GPU-Wartezeit) |
| Serving + Pipeline-Einbindung | 0.5 Tag (Pfade existieren) |
| Evaluation im Notebook | 0.5 Tag (Methodik existiert) |
| Optional: human-annotierter Test-Satz | 1–2 Tage |

---

## Offene Entscheidungen

- [ ] Teacher-Modell: nur Sonnet, oder Ensemble/Mehrheit aus Sonnet+GPT?
- [ ] Basismodell: Qwen2.5-7B vs. Llama-3.1-8B (Deutsch-Qualität testen).
- [ ] Human-annotierter Test-Satz ja/nein (Aufwand vs. wissenschaftliche Stärke).
- [ ] Trainings-Framework: axolotl vs. unsloth.
- [ ] Eigener `provider: "ft"` oder Wiederverwendung von `provider: "local"`.
