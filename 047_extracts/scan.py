"""Forward step: scan a full text for key passages and write verified candidates.

Two passes, both verified against the full text (a passage that cannot be located is dropped):
  structural  numbered statements (Assumption 3.1, Theorem 4.1, ...); no model call.
  llm         one question per chunk, following PROTOCOL.md; needs a model (port `ask`).
Usage: python3 scan.py structural [key ...]     python3 scan.py llm [key ...]
       python3 scan.py merge <pass name> <key> [...]          (verify <key>/llm_*.json, written by agents of a workflow)
       python3 scan.py promote <key> <candidate id> [...]     (curation: copy candidates into extracts.csv)
Writes 047_extracts/<key>/candidates.csv. It never edits extracts.csv, which is curated.
"""
from pathlib import Path
import csv
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "300_render"))
import backcheck  # noqa: E402

STATEMENT = re.compile(r"^(Assumption|Theorem|Lemma|Proposition|Corollary|Definition)\s+([A-Z]?\.?\d+(?:\.\d+)*)\b")
MAX_STATEMENT = 900
CHUNK, OVERLAP = 12000, 1000
FIELDS = ["id", "pass", "topic", "locator", "line", "text"]


def structural(fulltext):
    """Numbered statements, each from its heading to the end of its paragraph (cut at a sentence end)."""
    lines, out = fulltext.split("\n"), []
    for i, line in enumerate(lines):
        m = STATEMENT.match(line.strip())
        if not m:
            continue
        body = []
        for nxt in lines[i:]:
            if not nxt.strip() and body:
                break
            body.append(nxt.strip())
        text = " ".join(b for b in body if b)[:MAX_STATEMENT]
        text = text[:text.rfind(".") + 1] or text
        topic = "assumption" if m.group(1) == "Assumption" else "guarantee" if m.group(1) != "Definition" else "setting"
        out.append({"topic": topic, "locator": f"{m.group(1)} {m.group(2)}", "text": text})
    return out


def chunks(fulltext, size=CHUNK, overlap=OVERLAP):
    return [fulltext[i:i + size] for i in range(0, max(len(fulltext) - overlap, 1), size - overlap)]


def prompt_for(chunk, protocol):
    return (f"{protocol}\n\nFrom the text below, return a JSON list of objects with keys topic, locator, text. "
            "`text` must be copied character for character from the text, one to three sentences. "
            "`locator` is the section, assumption or theorem label if one is visible, else empty. "
            "Return [] if nothing fits. Return only JSON.\n\n<text>\n" + chunk + "\n</text>")


def llm(fulltext, protocol, ask):
    """Passages proposed by the model `ask(prompt) -> str`, one call per chunk. Malformed answers are skipped."""
    out = []
    for chunk in chunks(fulltext):
        try:
            items = json.loads(ask(prompt_for(chunk, protocol)))
        except (json.JSONDecodeError, TypeError):
            continue
        out += [{"topic": str(x.get("topic", "")), "locator": str(x.get("locator", "")), "text": str(x.get("text", ""))}
                for x in items if isinstance(x, dict)]
    return out


def verified(proposals, fulltext, pass_name):
    """Keep proposals whose text is in the full text; add the line number; drop duplicates."""
    index, rows, seen = backcheck.build_index(fulltext), [], set()
    for p in proposals:
        line = backcheck.locate(index, p["text"]) if p["text"].strip() else None
        if line is None or (line, p["text"][:60]) in seen:
            continue
        seen.add((line, p["text"][:60]))
        rows.append({"id": f"c{len(rows) + 1}", "pass": pass_name, "topic": p["topic"], "locator": p["locator"],
                     "line": line, "text": re.sub(r"\s+", " ", p["text"]).strip()})
    return rows


def claude_cli(prompt):
    """Adapter for the `ask` port: the Claude CLI in print mode, with the small model."""
    run = subprocess.run(["env", "-u", "ANTHROPIC_API_KEY", "claude", "-p", "--model", "haiku"],
                         input=prompt, capture_output=True, text=True, timeout=300)
    return run.stdout.strip().removeprefix("```json").removesuffix("```").strip()


def parse_proposals(blob):
    """Proposals from one JSON file written by an extraction agent; anything malformed gives an empty list."""
    try:
        items = json.loads(blob)
    except json.JSONDecodeError:
        return []
    return [{"topic": str(x.get("topic", "")), "locator": str(x.get("locator", "")), "text": str(x.get("text", ""))}
            for x in items if isinstance(x, dict)] if isinstance(items, list) else []


def write_candidates(key, pass_name, proposals, text):
    """Replace this pass's rows in <key>/candidates.csv by the verified proposals; return (proposed, kept)."""
    path = Path(__file__).parent / key / "candidates.csv"
    path.parent.mkdir(exist_ok=True)
    kept = [r for r in csv.DictReader(open(path, newline=""))] if path.exists() else []
    rows = [r for r in kept if r["pass"] != pass_name] + verified(proposals, text, pass_name)
    for i, r in enumerate(rows, 1):
        r["id"] = f"c{i}"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    return len(proposals), sum(r["pass"] == pass_name for r in rows)


def merge(pass_name, keys):
    """Verify the passages that workflow agents wrote to <key>/llm_*.json and store the verbatim ones as candidates."""
    files = {m["key"]: m["file"] for m in csv.DictReader(open(ROOT / "045_fulltext/manifest.csv", newline=""))}
    for key in keys:
        text = (ROOT / "045_fulltext" / files[key]).read_text(errors="replace")
        proposals = [p for f in sorted((Path(__file__).parent / key).glob("llm_*.json")) for p in parse_proposals(f.read_text())]
        print(key, pass_name, "%d proposed, %d verified" % write_candidates(key, pass_name, proposals, text))


def promote(key, ids):
    """Append the chosen candidates to the curated extracts of `key`, with new extract ids."""
    folder = Path(__file__).parent / key
    chosen = [c for c in csv.DictReader(open(folder / "candidates.csv", newline="")) if c["id"] in ids]
    rows = list(csv.DictReader(open(folder / "extracts.csv", newline="")))
    for c in chosen:
        rows.append({"id": f"e{len(rows) + 1}", "kind": c["topic"], "locator": c["locator"], "text": c["text"], "tex": ""})
    with open(folder / "extracts.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "kind", "locator", "text", "tex"])
        w.writeheader()
        w.writerows(rows)
    print(key, "promoted", [c["id"] for c in chosen])


def main(pass_name, keys):
    manifest = list(csv.DictReader(open(ROOT / "045_fulltext/manifest.csv", newline="")))
    protocol = (Path(__file__).parent / "PROTOCOL.md").read_text()
    for m in manifest:
        if keys and m["key"] not in keys:
            continue
        text = (ROOT / "045_fulltext" / m["file"]).read_text(errors="replace")
        proposals = structural(text) if pass_name == "structural" else llm(text, protocol, claude_cli)
        print(m["key"], pass_name, "%d proposed, %d verified" % write_candidates(m["key"], pass_name, proposals, text))


if __name__ == "__main__":
    if sys.argv[1] == "promote":
        promote(sys.argv[2], sys.argv[3:])
    elif sys.argv[1] == "merge":
        merge(sys.argv[2], sys.argv[3:])
    else:
        main(sys.argv[1], sys.argv[2:])
