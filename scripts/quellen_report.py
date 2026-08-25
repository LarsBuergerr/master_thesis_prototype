# -*- coding: utf-8 -*-
"""Erzeugt thesis/README_quellen.md: alle Quellen mit ihren Fundstellen.

Liest thesis/bib/report.bib sowie contents.tex, report.tex und appendix/*.tex,
sammelt jede \\cite-Stelle mit Zeilennummer, Gliederungspfad und tragendem Satz
und schreibt daraus einen Pruefbericht.

Aufruf aus dem Repo-Wurzelverzeichnis:  python3 scripts/quellen_report.py
"""
import io, re, os, glob, collections, json

BIB   = "thesis/bib/report.bib"
FILES = ["thesis/contents.tex", "thesis/report.tex"] + sorted(glob.glob("thesis/appendix/*.tex"))

# ---------------------------------------------------------------- BibTeX ----
def parse_bib(path):
    raw = io.open(path, encoding="utf-8").read()
    entries = {}
    for m in re.finditer(r'@(\w+)\s*\{\s*([^,]+),', raw):
        typ, key = m.group(1).lower(), m.group(2).strip()
        # Feldblock bis zur schliessenden Klammer des Eintrags
        i = m.end(); depth = 1; j = i
        while j < len(raw) and depth:
            if raw[j] == '{': depth += 1
            elif raw[j] == '}': depth -= 1
            j += 1
        body = raw[i:j-1]
        f = {}
        for fm in re.finditer(r'(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|"[^"]*"|[^,\n]+)', body):
            v = fm.group(2).strip().strip('{}"').strip()
            v = re.sub(r'\s+', ' ', v).replace('\\&', '&')
            f[fm.group(1).lower()] = v
        f['__type'] = typ
        entries[key] = f
    return entries

def _delatex(s):
    """LaTeX-Akzente und Gruppierungsklammern aus einem Namen entfernen."""
    import unicodedata
    acc = {"'": "\u0301", "`": "\u0300", '"': "\u0308", "^": "\u0302",
           "~": "\u0303", "c": "\u0327", "v": "\u030c", "=": "\u0304", ".": "\u0307"}
    def sub(m):
        return unicodedata.normalize("NFC", m.group(2) + acc.get(m.group(1), ""))
    s = re.sub(r"\\(['`\"^~cv=.])\s*\{?([A-Za-z])\}?", sub, s)
    s = s.replace(r"\ss", "\u00df").replace(r"\&", "&")
    return s.replace("{", "").replace("}", "").strip()


# Autorenfelder, die in Wahrheit Koerperschaften sind: ausschreiben, statt das
# letzte Wort faelschlich als Nachnamen zu lesen.
_ORG_HINT = re.compile(r"(?i)\b(organi[sz]ation|institut|standard|cent(er|re)|"
                       r"committee|komitee|bundes|ministerium|agentur|agency|"
                       r"consortium|w3c|fitko|gmbh|universit|bydata)")


def short_authors(f):
    a = f.get('author') or f.get('editor') or f.get('organization') or f.get('publisher') or ''
    a = _delatex(a)
    if not a:
        return '\u2014'
    names = [x.strip() for x in re.split(r'\s+and\s+', a) if x.strip()]

    def last(n):
        if ',' in n:
            return n.split(',')[0].strip()
        p = n.split()
        return p[-1] if p else n

    if len(names) == 1:
        n = names[0]
        # Einzelner Eintrag ohne Komma, mehrwortig oder mit Koerperschafts-Signal
        if ',' not in n and (len(n.split()) > 2 or _ORG_HINT.search(n)):
            return n if len(n) <= 38 else n[:37] + "\u2026"
        return last(n)
    if len(names) == 2:
        return "%s & %s" % (last(names[0]), last(names[1]))
    return "%s et al." % last(names[0])


def link_of(f):
    """Bester erreichbarer Link zu einer Quelle.

    Rueckgabe: (url, art). Art ist 'DOI', 'Web' oder 'Suche' -- letzteres ist
    eine Google-Scholar-Suche nach dem Titel und damit kein Nachweis der Quelle,
    sondern nur ein Sprungbrett.
    """
    doi = (f.get('doi') or '').strip()
    if doi:
        doi = re.sub(r'^(https?://(dx\.)?doi\.org/|doi:)\s*', '', doi, flags=re.I)
        return "https://doi.org/" + doi, "DOI"
    url = (f.get('url') or '').strip()
    if url:
        return url, "Web"
    title = (f.get('title') or '').strip()
    if title:
        import urllib.parse
        return ("https://scholar.google.com/scholar?q="
                + urllib.parse.quote_plus(_delatex(title)[:180]), "Suche")
    return "", ""

# ------------------------------------------------------- LaTeX-Aufbereitung --
def strip_comments(text):
    out = []
    for ln in text.split("\n"):
        # % am Zeilenanfang oder unmaskiertes % -> Rest der Zeile faellt weg
        ln = re.sub(r'(?<!\\)%.*$', '', ln)
        out.append(ln)
    return "\n".join(out)

def clean(s):
    """LaTeX-Rauschen aus einem Satz entfernen, Inhalt erhalten."""
    s = re.sub(r'\\caption\[[^]]*\]', ' ', s)   # Kurzform der Unterschrift verwerfen
    s = re.sub(r'\\(?:begin|end)\{[^}]*\}', ' ', s)
    s = re.sub(r'\\(?:label|index)\{[^}]*\}', '', s)
    s = re.sub(r'\\(?:ref|autoref|nameref|eqref)\{([^}]*)\}', r'[\1]', s)
    s = re.sub(r'\\[a-zA-Z]*cite[a-zA-Z]*(?:\[[^]]*\])*\{([^}]*)\}', r'[@\1]', s)
    s = re.sub(r'\\(?:emph|textit|textbf|texttt|enquote|acrfull|acrshort|acrlong|gls)\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\[a-zA-Z]+\s*', ' ', s)
    s = s.replace('{,}', ',').replace('\\%', '%').replace('~', ' ')
    s = re.sub(r'[{}$\\]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

SENT_END = re.compile(r'(?<=[.!?:])\s+(?=[A-ZÄÖÜ\\])')

def sentence_around(flat, pos):
    """Satz, in dem Position pos liegt."""
    lo = 0
    for m in SENT_END.finditer(flat, 0, pos):
        lo = m.end()
    hi = len(flat)
    m = SENT_END.search(flat, pos)
    if m: hi = m.start() + 1
    return flat[lo:hi].strip()

# --------------------------------------------------------------- Scannen ----
HEAD = re.compile(r'\\(chapter|section|subsection|subsubsection|paragraph)\*?\{')

def brace_arg(text, start):
    """Argument ab der oeffnenden Klammer bei start."""
    depth = 0; i = start
    while i < len(text):
        if text[i] == '{': depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0: return text[start+1:i], i+1
        i += 1
    return '', start+1

hits  = collections.defaultdict(list)  # key -> Liste von Fundstellen
sites = []                             # Zitatstellen in Dokumentreihenfolge
order = []                             # Reihenfolge des ersten Auftretens
_fileno = {p: i for i, p in enumerate(FILES)}

for path in FILES:
    if not os.path.exists(path): continue
    raw  = io.open(path, encoding="utf-8").read()
    text = strip_comments(raw)
    # Zeilennummern-Index
    line_of = [0]*(len(text)+1); ln = 1
    for i,ch in enumerate(text):
        line_of[i] = ln
        if ch == "\n": ln += 1
    line_of[len(text)] = ln

    # Ueberschriften-Positionen
    heads = []
    for m in HEAD.finditer(text):
        title, _ = brace_arg(text, m.end()-1)
        heads.append((m.start(), m.group(1), clean(title)))

    def context(pos):
        cur = {'chapter':'', 'section':'', 'subsection':'', 'subsubsection':'', 'paragraph':''}
        for p, lvl, title in heads:
            if p > pos: break
            cur[lvl] = title
            if lvl == 'chapter':       cur['section']=cur['subsection']=cur['subsubsection']=cur['paragraph']=''
            elif lvl == 'section':     cur['subsection']=cur['subsubsection']=cur['paragraph']=''
            elif lvl == 'subsection':  cur['subsubsection']=cur['paragraph']=''
        parts = [cur['chapter'], cur['section'], cur['subsection'], cur['subsubsection']]
        return " › ".join([p for p in parts if p])

    for m in re.finditer(r'\\[a-zA-Z]*cite[a-zA-Z]*(\[[^]]*\])*\{([^}]*)\}', text):
        keys  = [k.strip() for k in m.group(2).split(',') if k.strip()]
        extra = (m.group(1) or '').strip('[]')
        # Flachtext des umgebenden Absatzes
        pstart = text.rfind("\n\n", 0, m.start()); pstart = 0 if pstart < 0 else pstart+2
        pend   = text.find("\n\n", m.end());       pend   = len(text) if pend < 0 else pend
        para   = text[pstart:pend]
        # Art der Fundstelle: Bild-/Tabellenunterschrift, Tabellenzelle, Fliesstext
        pre = text[pstart:m.start()]
        cap = pre.rfind('\\caption')
        kind = 'Fliesstext'
        if cap >= 0 and pre[cap:].count('{') > pre[cap:].count('}'):
            kind = 'Unterschrift'
        elif re.search(r'\\begin\{(tabular|table|longtable)', pre):
            kind = 'Tabelle'
        rel    = m.start() - pstart
        # Position im bereinigten Text annaehern: vor+nach getrennt saeubern
        before = clean(para[:rel]); 
        flat   = clean(para)
        pos    = min(len(before), len(flat)-1) if flat else 0
        sent   = sentence_around(flat, pos) if flat else ''
        sites.append({
            'file': path, 'fileno': _fileno.get(path, 99), 'pos': m.start(),
            'line': line_of[m.start()], 'ctx': context(m.start()),
            'sent': sent, 'kind': kind, 'extra': extra, 'keys': keys,
        })
        for k in keys:
            if k not in hits: order.append(k)
            hits[k].append({
                'file': path, 'line': line_of[m.start()],
                'ctx': context(m.start()), 'sent': sent,
                'multi': len(keys) > 1, 'co': [x for x in keys if x != k],
                'kind': kind,
                'extra': extra,
            })

bib = parse_bib(BIB)
pass



# ===================== Bericht schreiben =====================
import json, io, re, collections


def _delatex(s):
    """LaTeX-Akzente und Gruppierungsklammern aus einem Namen entfernen."""
    import unicodedata
    acc = {"'": "\u0301", "`": "\u0300", '"': "\u0308", "^": "\u0302",
           "~": "\u0303", "c": "\u0327", "v": "\u030c", "=": "\u0304", ".": "\u0307"}
    def sub(m):
        return unicodedata.normalize("NFC", m.group(2) + acc.get(m.group(1), ""))
    s = re.sub(r"\\(['`\"^~cv=.])\s*\{?([A-Za-z])\}?", sub, s)
    s = s.replace(r"\ss", "\u00df").replace(r"\&", "&")
    return s.replace("{", "").replace("}", "").strip()


# Autorenfelder, die in Wahrheit Koerperschaften sind: ausschreiben, statt das
# letzte Wort faelschlich als Nachnamen zu lesen.
_ORG_HINT = re.compile(r"(?i)\b(organi[sz]ation|institut|standard|cent(er|re)|"
                       r"committee|komitee|bundes|ministerium|agentur|agency|"
                       r"consortium|w3c|fitko|gmbh|universit|bydata)")


def short_authors(f):
    a = f.get('author') or f.get('editor') or f.get('organization') or f.get('publisher') or ''
    a = _delatex(a)
    if not a:
        return '\u2014'
    names = [x.strip() for x in re.split(r'\s+and\s+', a) if x.strip()]

    def last(n):
        if ',' in n:
            return n.split(',')[0].strip()
        p = n.split()
        return p[-1] if p else n

    if len(names) == 1:
        n = names[0]
        # Einzelner Eintrag ohne Komma, mehrwortig oder mit Koerperschafts-Signal
        if ',' not in n and (len(n.split()) > 2 or _ORG_HINT.search(n)):
            return n if len(n) <= 38 else n[:37] + "\u2026"
        return last(n)
    if len(names) == 2:
        return "%s & %s" % (last(names[0]), last(names[1]))
    return "%s et al." % last(names[0])


def link_of(f):
    """Bester erreichbarer Link zu einer Quelle.

    Rueckgabe: (url, art). Art ist 'DOI', 'Web' oder 'Suche' -- letzteres ist
    eine Google-Scholar-Suche nach dem Titel und damit kein Nachweis der Quelle,
    sondern nur ein Sprungbrett.
    """
    doi = (f.get('doi') or '').strip()
    if doi:
        doi = re.sub(r'^(https?://(dx\.)?doi\.org/|doi:)\s*', '', doi, flags=re.I)
        return "https://doi.org/" + doi, "DOI"
    url = (f.get('url') or '').strip()
    if url:
        return url, "Web"
    title = (f.get('title') or '').strip()
    if title:
        import urllib.parse
        return ("https://scholar.google.com/scholar?q="
                + urllib.parse.quote_plus(_delatex(title)[:180]), "Suche")
    return "", ""

CH_ORDER = ["Einleitung", "Theoretische und konzeptionelle Grundlagen", "Experteninterviews",
            "Konzeption eines Metadatenqualitätsmodells", "Prototypische Operationalisierung",
            "Evaluation", "Diskussion der Qualitätsmetrik", "Fazit und Ausblick"]
def ch_of(ctx): return ctx.split(" › ")[0] if ctx else "(ohne Kapitel)"
def ch_num(c):
    return CH_ORDER.index(c)+1 if c in CH_ORDER else 99
def ch_lbl(c):
    n = ch_num(c)
    return ("Kap. %d" % n) if n < 99 else "Anhang"

# Sortierung: haeufigste zuerst
by_count = sorted(hits.keys(), key=lambda k: (-len(hits[k]), k.lower()))

L = []
w = L.append

w("# Quellenverzeichnis mit Fundstellen")
w("")
w("Automatisch erzeugt aus `thesis/bib/report.bib` und den `.tex`-Quellen "
  "(`contents.tex`, `report.tex`, `appendix/*.tex`).")
w("")
w("## Wie diese Datei zu lesen ist")
w("")
w("Die Datei hat zwei Sichten auf dieselben Daten:")
w("")
w("- **B. Durchgang in Textreihenfolge** — alle Zitatstellen so, wie sie im Text stehen. "
  "Für den linearen Prüfdurchgang.")
w("- **C. Quellen im Detail** — nach Quelle gruppiert. Beantwortet die andere Frage: "
  "trägt eine Quelle wirklich alle Aussagen, die ihr zugeschrieben werden?")
w("")
w("Zu jeder Stelle stehen:")
w("")
w("- **Fundstelle** — Datei und Zeilennummer, dazu der Gliederungspfad bis zur Unterüberschrift")
w("- **Aussage** — der Satz aus der Thesis, der die Zitation trägt. Das ist die Behauptung, "
  "die die Quelle belegen soll.")
w("- **`- [ ]`** — Obsidian-Task; beim Durchgehen direkt abhakbar")
w("- **Link** — `DOI` und `Web` führen direkt zur Quelle. `Suche` heißt, dass in der "
  "`.bib` weder DOI noch URL steht; der Link ist dann nur eine Google-Scholar-Suche "
  "nach dem Titel und **kein Nachweis**.")
w("")
w("In den Sätzen sind `\\ref{…}` als `[label]` und Zitationen als `[@key]` dargestellt, "
  "sonstiges LaTeX-Markup ist entfernt.")
w("")
w("> **Wichtige Einschränkung.** Diese Datei sagt, *was die Thesis an der jeweiligen Stelle "
  "behauptet* — nicht, ob die Quelle das tatsächlich hergibt. Genau das ist beim Prüfen die "
  "eigentliche Arbeit. Seitenangaben lassen sich nicht ausgeben, weil die Zitationen im "
  "Dokument bis auf eine Ausnahme keine Locator tragen (siehe Abschnitt "
  "„Auffälligkeiten“).")
w("")

tot_keys, tot_sites = len(hits), sum(len(v) for v in hits.values())
unused = sorted(k for k in bib if k not in hits)
w("## Kennzahlen")
w("")
w("| | |")
w("|---|---|")
w("| Einträge in `report.bib` | %d |" % len(bib))
w("| davon zitiert | %d |" % tot_keys)
w("| davon nie zitiert | %d |" % len(unused))
w("| Zitatstellen (`\\cite`-Befehle) | %d |" % len(sites))
w("| Quellenverweise gesamt | %d |" % tot_sites)
w("| Quellen mit nur einer Fundstelle | %d |" % sum(1 for k in hits if len(hits[k]) == 1))
w("")

# ------------------------------------------------------------ Übersicht ----
w("## A. Übersicht")
w("")
w("Alphabetisch nach BibTeX-Key. „Kapitel“ nennt jedes Kapitel, in dem die Quelle vorkommt.")
w("")
w("| Key | Kurzbeleg | Jahr | Link | Stellen | Kapitel |")
w("|---|---|---|---|---:|---|")
for k in sorted(hits, key=lambda x: x.lower()):
    f = bib.get(k, {})
    chs = sorted({ch_of(h['ctx']) for h in hits[k]}, key=ch_num)
    lbl = ", ".join(ch_lbl(c) for c in chs)
    ttl = f.get('title', '—')
    ttl = (ttl[:57] + "…") if len(ttl) > 58 else ttl
    u, kindl = link_of(f)
    lnk = "[%s](%s)" % (kindl, u) if u else "—"
    w("| `%s` | %s | %s | %s | %d | %s |" % (k, short_authors(f), f.get('year', '—'), lnk, len(hits[k]), lbl))
w("")

# --------------------------------------------------------------- Detail ----
w("## B. Durchgang in Textreihenfolge")
w("")
w("Alle Zitatstellen in der Reihenfolge, in der sie im Text vorkommen, gruppiert nach "
  "Kapitel und Abschnitt. Für einen linearen Prüfdurchgang: Arbeit und Liste "
  "nebeneinander, von oben nach unten.")
w("")
w("Ein `\\cite` mit mehreren Quellen steht hier **einmal** mit allen beteiligten "
  "Quellen — an solchen Stellen ist zu prüfen, ob jede von ihnen die Aussage trägt.")
w("")

_cur_ch = _cur_sec = None
for s in sorted(sites, key=lambda x: (x['fileno'], x['pos'])):
    c = ch_of(s['ctx'])
    if c != _cur_ch:
        _cur_ch, _cur_sec = c, None
        w("### %s — %s" % (ch_lbl(c), c))
        w("")
    parts = s['ctx'].split(" \u203a ")
    sec = " \u203a ".join(parts[1:]) if len(parts) > 1 else "(Kapiteleinleitung)"
    if sec != _cur_sec:
        _cur_sec = sec
        w("**%s**" % sec)
        w("")
    def _kl(k):
        u, art = link_of(bib.get(k, {}))
        return "[`%s`](%s)" % (k, u) if u else "`%s`" % k
    tag = ""
    if s['kind'] != 'Fliesstext': tag += " · _%s_" % s['kind']
    if s['extra']:                tag += " · Locator: `%s`" % s['extra']
    w("- [ ] `%s:%d`%s — %s  " % (s['file'].replace('thesis/',''), s['line'], tag,
                                  ", ".join(_kl(k) for k in s['keys'])))
    w("  > %s" % (s['sent'] if s['sent'] else "_(Satz nicht extrahierbar)_"))
    w("")

w("## C. Quellen im Detail")
w("")
w("Sortiert nach Anzahl der Fundstellen, absteigend — die tragendsten Quellen zuerst.")
w("")
for k in by_count:
    f  = bib.get(k, {})
    hs = hits[k]
    w("### `%s` — %s (%s)" % (k, short_authors(f), f.get('year', 'o. J.')))
    w("")
    w("**%s**  " % f.get('title', '—'))
    meta = []
    for fld, lab in [('journal','in'), ('booktitle','in'), ('publisher','Verlag'),
                     ('institution','Institution'), ('organization','Organisation'),
                     ('howpublished','Medium'), ('note','Anm.')]:
        if f.get(fld): meta.append("%s: %s" % (lab, f[fld]))
    if f.get('__type'): meta.append("Typ: `%s`" % f['__type'])
    if meta: w(" · ".join(meta) + "  ")
    u, kindl = link_of(f)
    if kindl == "DOI":
        w("\u2192 **[Quelle \u00f6ffnen (DOI)](%s)**  " % u)
        if f.get('url'): w("Zusatz-URL: <%s>  " % f['url'])
    elif kindl == "Web":
        w("\u2192 **[Quelle \u00f6ffnen](%s)**  " % u)
    elif kindl == "Suche":
        w("\u2192 kein Link hinterlegt \u2014 [auf Google Scholar suchen](%s)  " % u)
    if f.get('urldate'): w("Zugriff: %s  " % f['urldate'])
    w("")
    w("%d Fundstelle%s." % (len(hs), "" if len(hs) == 1 else "n"))
    w("")
    cur = None
    for h in sorted(hs, key=lambda x: (ch_num(ch_of(x['ctx'])), x['line'])):
        c = ch_of(h['ctx'])
        if c != cur:
            cur = c
            w("**%s — %s**" % (ch_lbl(c), c))
            w("")
        path = h['file'].replace("thesis/", "")
        loc  = h['ctx'].split(" › ", 1)
        sub  = loc[1] if len(loc) > 1 else "(Kapiteleinleitung)"
        extra = ""
        if h.get('kind') and h['kind'] != 'Fliesstext':
            extra += " · _%s_" % h['kind']
        if h['extra']: extra += " · Locator: `%s`" % h['extra']
        if h['co']:
            def _co(c2):
                cu, _ = link_of(bib.get(c2, {}))
                return "[`%s`](%s)" % (c2, cu) if cu else "`%s`" % c2
            extra += " · gemeinsam mit " + ", ".join(_co(c2) for c2 in h['co'])
        _u, _kl = link_of(f)
        _lnk = " · [%s](%s)" % (_kl, _u) if _u else ""
        w("- [ ] `%s:%d` — %s%s%s  " % (path, h['line'], sub, extra, _lnk))
        w("  > %s" % (h['sent'] if h['sent'] else "_(Satz nicht extrahierbar)_"))
        w("")
    w("---")
    w("")

# ------------------------------------------------------- Kapitel-Index ----
# -------------------------------------------------------- Auffälligkeiten --
w("## D. Auffälligkeiten")
w("")
w("### Nie zitiert")
w("")
if unused:
    w("Diese Einträge stehen in der `.bib`, werden aber nirgends zitiert. "
      "Bei `biblatex` mit Standardeinstellung erscheinen sie nicht im Literaturverzeichnis — "
      "entweder verwenden oder entfernen.")
    w("")
    for k in unused:
        f = bib[k]
        u, kindl = link_of(f)
        sfx = " \u2014 [%s](%s)" % (kindl, u) if u else ""
        w("- [ ] `%s` — %s (%s): %s%s" % (k, short_authors(f), f.get('year','o. J.'), f.get('title','—'), sfx))
    w("")
else:
    w("Keine. Jeder Eintrag der `.bib` wird mindestens einmal zitiert.")
    w("")

w("### Nur eine Fundstelle")
w("")
w("Einmal zitierte Quellen tragen jeweils genau eine Aussage. Wenn diese Aussage nicht hält, "
  "fällt die Quelle ersatzlos weg — deshalb lohnt hier der genaueste Blick.")
w("")
singles = [k for k in by_count if len(hits[k]) == 1]
for k in sorted(singles, key=lambda x: x.lower()):
    h = hits[k][0]
    u, kindl = link_of(bib.get(k, {}))
    sfx = " · [%s](%s)" % (kindl, u) if u else ""
    w("- [ ] `%s` — %s:%d, %s%s" % (k, h['file'].replace('thesis/',''), h['line'], ch_lbl(ch_of(h['ctx'])), sfx))
    w("  > %s" % h['sent'])
w("")

w("### Auskommentierte Zitationen")
w("")
_cmt = []
for _p in FILES:
    if not os.path.exists(_p): continue
    for _i, _ln in enumerate(io.open(_p, encoding="utf-8").read().split("\n"), 1):
        if re.match(r'\s*%', _ln):
            for _m in re.finditer(r'\\[a-zA-Z]*cite[a-zA-Z]*(?:\[[^]]*\])*\{([^}]*)\}', _ln):
                for _k in [x.strip() for x in _m.group(1).split(',') if x.strip()]:
                    _cmt.append((_p, _i, _k, _k in bib))
if _cmt:
    w("Diese Zitationen stehen in auskommentiertem Text und sind deshalb oben nicht "
      "aufgeführt. Relevant nur, falls der Text wieder aktiviert wird — Schlüssel, die "
      "nicht in der `.bib` stehen, würden dann ins Leere laufen.")
    w("")
    for _p, _i, _k, _ok in _cmt:
        w("- [ ] `%s:%d` — `%s` %s" % (_p.replace('thesis/',''), _i, _k,
          "" if _ok else "\u2014 **nicht in der `.bib`**"))
else:
    w("Keine.")
w("")

w("### Ohne hinterlegten Link")
w("")
_nolink = sorted([k for k in hits if link_of(bib.get(k, {}))[1] == "Suche"], key=str.lower)
if _nolink:
    w("Bei diesen Einträgen enthält die `.bib` weder `doi` noch `url`. Für die Prüfung "
      "und für Leserinnen und Leser wäre je ein Nachweis sinnvoll.")
    w("")
    for k in _nolink:
        f = bib[k]
        u, _ = link_of(f)
        w("- [ ] `%s` — %s (%s): %s — [suchen](%s)"
          % (k, short_authors(f), f.get('year', 'o. J.'), f.get('title', '—'), u))
else:
    w("Zu jeder zitierten Quelle ist ein DOI oder eine URL hinterlegt.")
w("")

w("### Zitationen mit Locator")
w("")
loc = [(k, h) for k in hits for h in hits[k] if h['extra']]
if loc:
    w("Nur diese Stellen nennen eine konkrete Position in der Quelle. "
      "Bei allen übrigen %d Stellen muss die Fundstelle in der Quelle beim Prüfen "
      "selbst gesucht werden." % (tot_sites - len(loc)))
    w("")
    for k, h in loc:
        w("- [ ] `%s` · Locator `%s` — %s:%d" % (k, h['extra'], h['file'].replace('thesis/',''), h['line']))
        w("  > %s" % h['sent'])
else:
    w("Keine Zitation trägt einen Locator.")
w("")

w("### Mehrfachzitationen")
w("")
multi = collections.Counter()
for k in hits:
    for h in hits[k]:
        if h['co']: multi[tuple(sorted([k] + h['co']))] += 1
if multi:
    w("Stellen, an denen mehrere Quellen gemeinsam einen Satz belegen. "
      "Hier ist zu prüfen, ob wirklich jede der Quellen die Aussage trägt.")
    w("")
    w("| Quellen | Stellen |")
    w("|---|---:|")
    # jede Fundstelle wurde einmal je beteiligter Quelle gezaehlt
    multi = {g: n // len(g) for g, n in multi.items()}
    for grp, n in sorted(multi.items(), key=lambda x: (-x[1], x[0])):
        w("| %s | %d |" % (", ".join("`%s`" % g for g in grp), n))
w("")

w("---")
w("")
w("Neu erzeugen: `python3 scripts/quellen_report.py` (Skript liegt im Repo, "
  "schreibt diese Datei nach `thesis/README_quellen.md`).")

io.open("thesis/README_quellen.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("geschrieben: thesis/README_quellen.md (%d Zeilen)" % len(L))
