"""Consistency checks over the stage folders. Each check returns a list of problems; the build stops on any."""
import re
from render import cite_keys

QUOTE = re.compile(r'"([^"]+)"')
EVIDENCE_TYPES = {"quote", "absence", "judgement"}
PHASES = {"training", "deployment"}
OWNERS = {"RL", "LLM", "Both"}
INCIDENT_SETTINGS = {"deployed-incident", "red-team-on-product"}
VERIFICATION = {"verified-primary", "verified-secondary"}
WRITABLE = {"yes", "partial", "no", "unclear", ""}
NUMBER_WORDS = "two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen".split()


def normalise(text):
    return re.sub(r"\s+", " ", text.replace("“", '"').replace("”", '"').replace("’", "'"))


def split_list(field):
    return [x.strip() for x in field.split(";") if x.strip()]


def missing_keys(texts, refs):
    keys = {r["key"] for r in refs}
    return [f"citation @{k} not in 040_biblio" for t in texts for k in sorted(cite_keys(t) - keys)]


def existence_problems(cited, existence):
    """040: every cited reference must be confirmed to exist (status ok), or checked by hand (manual, with a note)."""
    status = {r["key"]: r for r in existence}
    out = []
    for k in sorted(cited):
        r = status.get(k)
        if r is None:
            out.append(f"reference @{k}: not checked; run 040_biblio/verify.py")
        elif r["status"] != "ok" and not (r["status"] == "manual" and r["note"].strip()):
            out.append(f"reference @{k}: existence {r['status']}; check by hand and record status manual with a note")
    return out


def note_problems(keys, notes):
    """010/050: each target or quoted source has a note with a read scope in its front matter."""
    out = []
    for k in keys:
        if k not in notes:
            out.append(f"source {k}: no note in 010_target or 050_biblio_notes")
        elif not re.search(r"^read: (full|partial|quotes)$", notes[k], re.M):
            out.append(f"note {k}: no read scope in front matter")
    return out


def verified_quotes(note):
    """Phrases listed under a note's "Verified quotes" heading (one per line, as - "phrase")."""
    _, found, tail = note.partition("Verified quotes")
    return re.findall(r'^- "(.+?)"', tail, re.M) if found else []


def settings_problems(settings, decisions):
    decided = {d["id"] for d in decisions}
    out = []
    for s in settings:
        if s["phase"] not in PHASES:
            out.append(f"setting {s['id']}: phase must be training or deployment")
        if not s["posed_as"].strip():
            out.append(f"setting {s['id']}: no 'posed as'")
        if s["decision"] not in decided:
            out.append(f"setting {s['id']}: decision {s['decision']!r} is not in 005_decisions")
    return out


def primitive_problems(primitives, target_extracts):
    """062: each primitive has an RL definition backed by extracts of the target text."""
    ids = {e["id"] for e in target_extracts}
    out = []
    for p in primitives:
        if not p["rl_definition"].strip():
            out.append(f"primitive {p['id']}: no RL definition")
        ev = split_list(p["evidence"])
        if not ev:
            out.append(f"primitive {p['id']}: no extract ids")
        out += [f"primitive {p['id']}: evidence {i} is not a sutton2018 extract" for i in ev if i not in ids]
    return out


def cell_problems(primitives, settings, cells):
    """065: every primitive x setting cell exists, has a value and a reason, and declares its evidence."""
    have = {(c["primitive"], c["setting"]) for c in cells}
    out = [f"cell {p['id']} {s['id']}: missing" for p in primitives for s in settings if (p["id"], s["id"]) not in have]
    for c in cells:
        name = f"cell {c['primitive']} {c['setting']}"
        if not c["value"].strip():
            out.append(f"{name}: no value")
        if not c["reason"].strip():
            out.append(f"{name}: no reason")
        if c["evidence_type"] not in EVIDENCE_TYPES:
            out.append(f"{name}: bad evidence_type {c['evidence_type']!r}")
        elif c["evidence_type"] == "quote" and not (c["evidence"].strip() and c["evidence_source"].strip() and QUOTE.search(c["reason"])):
            out.append(f"{name}: a quote cell needs a quoted phrase, an evidence_source and extract ids")
        elif c["evidence_type"] == "judgement" and QUOTE.search(c["reason"]) and not c["evidence"].strip():
            out.append(f"{name}: a judgement cell that quotes must cite extracts (make it a quote cell)")
    return out


def assumption_problems(assumptions, refs, primitives):
    keys = {r["key"] for r in refs}
    prim = {p["id"] for p in primitives}
    out = []
    seen = set()
    for a in assumptions:
        if a["id"] in seen:
            out.append(f"assumption {a['id']}: duplicate id")
        seen.add(a["id"])
        if a["owner"] not in OWNERS:
            out.append(f"assumption {a['id']}: owner must be RL, LLM or Both")
        out += [f"assumption {a['id']}: ref @{k} not in 040_biblio" for k in split_list(a["refs"]) if k not in keys]
        out += [f"assumption {a['id']}: unknown primitive {p}" for p in split_list(a["primitive"]) if p not in prim]
    return out


def incident_problems(incidents, assumptions, snapshots):
    """075: valid setting and verification, known assumption tags, at least one source URL, and a snapshot attempt per URL."""
    ids = {a["id"] for a in assumptions}
    fetched = {(r["incident"], r["url"]): r for r in snapshots}
    out = []
    for i in incidents:
        if i["setting"] not in INCIDENT_SETTINGS:
            out.append(f"incident {i['id']}: setting {i['setting']!r} not allowed")
        if i["verification"] not in VERIFICATION:
            out.append(f"incident {i['id']}: verification {i['verification']!r} not allowed")
        out += [f"incident {i['id']}: unknown assumption tag {t}" for t in i["assumption_tags"].split(",") if t.strip() and t.strip() not in ids]
        urls = [u for u in re.split(r"[;\s]+", i["source_urls"]) if u.startswith("http")]
        if not urls:
            out.append(f"incident {i['id']}: no source URL")
        out += [f"incident {i['id']}: source {u} has no snapshot row in 045_fulltext/web_manifest.csv" for u in urls if (i["id"], u) not in fetched]
        if urls and all(fetched.get((i["id"], u), {}).get("status") != "ok" for u in urls) and i["verification"] == "verified-primary" and not i.get("snapshot_note", "").strip():
            out.append(f"incident {i['id']}: verified-primary but no source snapshot could be stored; add snapshot_note")
    return out


def label_problems(incidents, labels, raters=("haiku", "sonnet")):
    """078: every incident has a writable-in-advance verdict and a failure type from each rater, with allowed values."""
    have = {(r["incident"], r["rater"], r["dimension"]): r["value"] for r in labels}
    out = []
    for i in incidents:
        for rater in raters:
            for dim in ("writable_in_advance", "failure_type"):
                v = have.get((i["id"], rater, dim))
                if v is None:
                    out.append(f"label {i['id']} {rater} {dim}: missing")
                elif dim == "writable_in_advance" and v not in WRITABLE:
                    out.append(f"label {i['id']} {rater} {dim}: bad value {v!r}")
    return out


def culture_problems(cultures, breiman_extracts):
    ids = {e["id"] for e in breiman_extracts}
    out = []
    for c in cultures:
        name = f"culture {c['culture']} {c['line']}"
        if not c["text"].strip():
            out.append(f"{name}: no text")
        if QUOTE.search(c["text"]) and not c["evidence"].strip():
            out.append(f"{name}: quotes but cites no extract")
        out += [f"{name}: evidence {i} is not a breiman2001 extract" for i in split_list(c["evidence"]) if i not in ids]
    return out


def draft_problems(draft):
    return [f"draft line {i}: typed table row; import tables with {{{{table:...}}}}"
            for i, line in enumerate(draft.splitlines(), 1) if line.lstrip().startswith("|")]


def typed_count_problems(text, nouns):
    """A count of a defined set must be a {{fact:...}}; flag a number typed next to one of the set nouns."""
    words = re.findall(r"[A-Za-z0-9{}:_]+", text)
    out = []
    for i, w in enumerate(words):
        if w.lower() in NUMBER_WORDS or w.isdigit():
            near = [x.lower() for x in words[i + 1:i + 3]]
            hit = next((n for n in nouns if n in near), None)
            if hit:
                out.append(f"draft: typed count \"{w} ... {hit}\"; use a {{{{fact:...}}}} so the count follows its set")
    return out
