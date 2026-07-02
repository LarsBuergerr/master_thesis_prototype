# Code Freeze — Checkliste

Ziel: Ab dem Freeze beschreibt und evaluiert die Thesis **genau eine eingefrorene
Modellversion** (Git-Tag). Danach ändert sich die score-erzeugende Logik nicht
mehr — nur noch die Config.

## Prinzip

**Instrument bauen (vor Freeze) ≠ mit dem Instrument messen (nach Freeze).**
Alles, was den Score einer beliebigen Eingabedatei verändert, ist eine
*Konstruktionsänderung* und MUSS vor den Freeze. Alles, was du bewusst pro
Experiment variieren willst, gehört in die *Config* und darf nach dem Freeze.

Die Linie zwischen beidem ist der Tag. Testruns von vor dem Freeze sind
Entwicklungsartefakte und kommen nicht in die Thesis.

---

## MUSS vor den Freeze (Code — verändert Scores)

- [ ] **Obligation-Level-Severity-Mapping** (DCAT-AP.de §3.2): Pflicht→FAIL,
      Empfohlen→PARTIAL, Optional→neutral. Die große strukturelle Änderung.
- [ ] **`acc_access_url` Präsenz-Indikator** (einziges Pflichtfeld der Distribution,
      fehlt aktuell).
- [ ] **Optionales Feld `reuse_contributor_id`**: laut Spec optional, feuert aber
      FAIL bei Abwesenheit — Entscheidung: neutral werten oder so lassen.
      (`find_identifier` und `acc_distribution_status` wurden bereits entfernt;
      `dcatap:availability` ist als `reuse_availability` umgesetzt.)
- [ ] **Restliche Indikator-Logik**, die schon feststeht: keywords (3–15/16–25),
      `reuse_contact` (ternär), `find_political_geocoding` (dcatde primär).
- [ ] **`score_policy` GRADED-Verhalten** (roher Score, keine FAIL-Klippe) — bereits umgesetzt.
- [ ] **Blacklist festzurren**: `acc_format_congruence`, `acc_distribution_model` raus.
- [ ] **Expressiveness-Prompt** — nur falls die verbesserte LLM-Bewertung Teil der
      evaluierten Version sein soll. ← Entscheidung, verändert Scores.
- [ ] **Doc/Code-Konsistenz** (z. B. `reuse_contributor_id`-Docstring) — kosmetisch,
      aber vor den Freeze.
- [ ] **Ground-Truth-Evaluation MUSS gegen die eingefrorene Version laufen** —
      sonst ist das Cohen's κ ungültig.

## Nur Config — NACH dem Freeze erlaubt

Diese Knöpfe erzeugen deine *gewollten* Vergleiche in der Thesis, ohne das
Instrument zu verändern:

- `indicator_weights` / `dimension_weights` (Gewichtungs-Experimente)
- `pass_score` / `partial_score` / `fail_score` / `allow_partial` + Per-Indikator-Overrides
- `indicator_blacklist` / `indicator_whitelist` / `dimension_whitelist` (Ablationen)
- LLM-Provider / -Modell, Sample-Auswahl, Input-Pfade

## Nicht in den Freeze / später / außerhalb Scope

- **Dubletten-Check** für `dct:identifier` — braucht Portal-Level-Infrastruktur
  (Kommentar-Stub liegt bereits im Code).
- **Sensitivitätsanalyse** der Schwellen — Notebook-Arbeit, keine Code-Änderung.
- **`acc_format_congruence` / `acc_distribution_model`** — bewusst geblacklistet,
  Code bleibt reversibel liegen.
- Neue Indikatoren, die du nicht evaluierst.

---

## Ablauf

1. Alle Konstruktionsänderungen mergen.
2. **Tag setzen** (z. B. `model-v1.0`) + Commit-Hash im Methoden-Kapitel notieren.
3. Ground-Truth-Evaluation gegen den Tag.
4. Config-Experimente gegen denselben Tag.
5. Internes `CHANGELOG.md` (nur für dich, nicht für die Thesis) für die
   Nachvollziehbarkeit in der Verteidigung.

## Faustregel

> Ändert es den Score einer festen Eingabedatei? → vor den Freeze.
> Willst du es zwischen Läufen bewusst variieren? → Config, nach dem Freeze.
