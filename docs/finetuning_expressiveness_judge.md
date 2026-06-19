# Fine-Tuning Expressiveness-Judge

> Ziel: den LLM-gestützten *Expressiveness*-Judge durch ein **kleines, lokal fine-getuntes
> Modell** ersetzen (Distillation aus einem Frontier-Modell) — bessere Reproduzierbarkeit,
> keine API-Kosten, kein Datenabfluss.

## 1. Kernidee & Empfehlung

**Einziger sinnvoller Fine-Tuning-Kandidat:** der Expressiveness-Judge. Die anderen vier
Dimensionen sind deterministisch/regelbasiert — dort wäre ML nicht sinnvoll.

**Methode:** Knowledge Distillation — ein starkes Modell (Sonnet) erzeugt Labels, ein
kleines lokales Modell (7–8B, QLoRA) lernt sie nachzuahmen.

**Aufwand niedrig**, weil drei Dinge bereits existieren:
1. eine saubere LLM-Naht (`llm`-Parameter, duck-typed),
2. ein lokaler Inferenz-Pfad (`provider: "local"`, llama.cpp),
3. eine Mess-Methodik (Notebook `09_run_aggregate_stats.ipynb`).

**Praktisches Thesis-Argument:** kein API-Key, keine Token-Kosten, On-Prem-Inferenz —
bei deutschen Behörden-Metadaten ist **Datensouveränität** ein verteidigbares Argument.

## 2. Phasen-Roadmap

> Kernprinzip: **erst Messlatte, dann Prompt einfrieren, dann Labels & Training.**
> Labels vor dem Einfrieren des Prompts zu erzeugen ist verschwendetes Budget.

| Phase | Ziel | Output | Kosten |
|-------|------|--------|--------|
| **0** Gold-Set | objektiver Maßstab | `data/gold/expressiveness_gold.jsonl` | 0 € |
| **1** Prompt | Teacher-Prompt einfrieren + Baselines | eingefrorener Prompt, Kennzahlen | < 1 € |
| **2** Daten | diverse Inputs sammeln | Datensatz-Liste, Splits | 0 € |
| **3** Labels | Distillation (Teacher labelt) | `data/ft/expressiveness_train.jsonl` | ~5–15 € |
| **4** Fine-Tune | QLoRA auf 7–8B | GGUF-Modell | 0 € (lokal) |
| **5** Eval | FT vs. Teacher vs. Gold | Notebook-Bericht | 0 € (lokal) |
| **6** Iterieren | Edge-Cases nachlabeln | mehr Labels | gering |

### Phase 0 — Gold-Set *(Messlatte)*
20–50 Datensätze von Hand bewerten (6 Kriterien je status/score, kurze Begründung).
Spektrum abdecken: gut, mittel, kaputt (`data/extreme_cases*` einbeziehen). Idealerweise
2 Annotator:innen → Agreement messen. **Fließt nie ins Training.**
Gate: Inter-Annotator-Agreement akzeptabel; sonst Kriterien schärfen.

### Phase 1 — Prompt einfrieren
Prompt iterativ gegen das Gold-Set optimieren. Parallel messen: (a) Teacher gegen Gold,
(b) lokales Basismodell nur mit Prompt/Few-Shot als Baseline „C".
Gate: Teacher trifft das Gold-Set gut genug als Label-Quelle.

### Phase 2 — Daten beschaffen
Diverse, distinkte Inputs aus der bestehenden Pipeline
(`playground/notebooks/01_fetch_metadata.ipynb`, CKAN-Fetch). **Prompt ab hier nicht mehr ändern.**
Train/Val/Test **datensatz-disjunkt** aufteilen (nicht datei-disjunkt, sonst leakt ein
Datensatz in beide Splits).

### Phase 3 — Labels (Distillation)
Alle Inputs mit dem **eingefrorenen** Prompt labeln. Kein Opus — Sonnet genügt (~€0,04/Call).
Richtwert: ~300–500 distinkte Labels; nur nachlegen, wenn die Eval es verlangt.

### Phase 4 — Fine-Tuning
**Basismodell:** Qwen2.5-7B-Instruct oder Llama-3.1-8B-Instruct (Deutsch, JSON-fähig).
**Methode:** QLoRA (4-bit), 1–3 Epochen, LoRA-Rank 16–32, Loss nur auf der Completion.
Frameworks: `axolotl` oder `unsloth`.

### Phase 5 — Evaluation
Vollen Run mit dem FT-Modell fahren → als 4. Modell in `09_run_aggregate_stats.ipynb`
aufnehmen.

Zielmetriken:
- MAE(FT, Teacher) ≈ Teacher-Run-zu-Run (~0.03)
- Bias ≈ 0 (keine systematische Über-/Unterbewertung)
- Pearson hoch (gleiche Datensatz-Rangordnung)
- Reproduzierbarkeit FT-zu-FT ≤ Teacher

### Phase 6 — Iterieren
Fälle finden, wo FT am stärksten vom Gold/Teacher abweicht → dort Labels nachlegen →
zurück zu Phase 4.

## 3. Integrations-Naht

Der gesamte Agent wird nur über eine duck-typed Methodenkette genutzt
(`src/extraction/semantic_assessment.py`):

```text
structured = llm.with_structured_output(ExpressivenessAssessment, method="function_calling", include_raw=True)
result     = structured.invoke(messages)   # → {"parsed": ExpressivenessAssessment, "raw": ...}
context.semantic_assessment = result["parsed"]
```

Einbindung des FT-Modells: als OpenAI-kompatibler Endpoint (llama.cpp / vLLM) über den
bestehenden `provider: "local"`-Pfad. Nur `base_url`/`model` in der Config setzen.

```yaml
llm:
  enabled: true
  provider: "local"
  base_url: "http://localhost:8080/v1"
  model: "expr-judge-ft"
  temperature: 0.0
```

**JSON-Schema/Grammar-Constraint am Server aktivieren** — das FT-Modell muss valides JSON
nach `ExpressivenessAssessment` (6 Kriterien je `{status, score, reasoning, findings}` +
`overall_summary`) liefern.

## 4. Optionen

| Option | Methode | Aufwand | Empfehlung |
|--------|---------|---------|------------|
| **A. Distillation + QLoRA** | Frontier labelt, kleines Modell lernt | mittel | **erste Wahl** |
| B. Full Fine-Tune | gesamtes Modell trainieren | hoch | nur wenn LoRA klar zu schwach |
| C. Nur Prompt/Few-Shot | kein Training | sehr niedrig | **als Baseline messen** |
| D. DPO/Präferenz-Tuning | paarweise Urteile | hoch | Ausblick |

Strategie: C als Baseline → A umsetzen → A gegen C und Teacher vergleichen.
Differenz „A − C" zeigt den reinen Fine-Tuning-Effekt.

## 5. Gold-Standard & Ehrlichkeit

Distillation lernt die **Biases des Teachers** mit — der Student kann per Definition nur
approximieren, nicht übertreffen. Für eine belastbare Aussage braucht es den
human-annotierten Test-Satz (Phase 0) als einzigen unabhängigen Maßstab. Ohne ihn bleibt
nur die Aussage „das kleine Modell imitiert das große Modell gut" — valide, aber schwächer.

## 6. Risiken

| Risiko | Gegenmaßnahme |
|--------|---------------|
| Zu wenige/einseitige Labels | mehrere Teacher-Läufe + `extreme_cases`; Score-Verteilung prüfen |
| Modell bricht JSON-Schema | constrained decoding (grammar/JSON-Schema) am Server |
| Overfitting | datensatz-disjunkter Split, wenige Epochen, kleine LoRA-Rank |
| Teacher-Bias als „Wahrheit" | human-annotierter Test-Satz als unabhängiger Maßstab |
| Deutsch-Qualität | Qwen2.5/Llama-3.1 wählen; reasoning stichprobenartig prüfen |

## 7. Offene Entscheidungen

- [ ] Teacher: nur Sonnet oder Ensemble aus Sonnet + GPT?
- [ ] Basismodell: Qwen2.5-7B vs. Llama-3.1-8B (Deutsch-Qualität testen).
- [ ] Human-annotierter Test-Satz ja/nein (Aufwand vs. wissenschaftliche Stärke).
- [ ] Framework: axolotl vs. unsloth.
