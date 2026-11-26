"""Merge one round's raw findings into 096_review/findings/round_<n>.json for the gate.
Inputs: the Claude round result (scores + findings) and optional Codex JSON lines.
A key claim scored qualify or refuted becomes a finding too.
Usage: python3 collect.py <n> <claude_round.json> [codex.jsonl]"""
import json, sys
from pathlib import Path
FIELDS = ("where", "claim", "problem", "evidence", "severity", "key", "fix")

def from_claude(d):
    out = [{"source": "claude", "lens": f.get("lens", ""), **{k: f.get(k, "") for k in FIELDS}} for f in d["findings"]]
    out += [{"source": "claude", "lens": "score", "where": "096_review/key.csv", "claim": s["id"],
             "problem": f"key claim scored {s['verdict']}", "evidence": s["evidence"], "severity": "overclaim",
             "key": s["id"], "fix": s["fix"]} for s in d["scores"] if s["verdict"] != "supported"]
    return out

def from_codex(lines):
    out = []
    for line in lines:
        line = line.strip()
        if not line.startswith("{"):
            continue
        f = json.loads(line)
        if "problem" in f:
            out.append({"source": "codex", "lens": "codex", **{k: f.get(k, "") for k in FIELDS}})
    return out

def main(n, claude, codex=None):
    d = json.load(open(claude))
    d = d.get("result", d)
    found = from_claude(d) + (from_codex(open(codex)) if codex else [])
    out = Path(__file__).parent / "findings" / f"round_{n}.json"
    out.write_text(json.dumps(found, indent=1))
    print(out, len(found), "findings")

if __name__ == "__main__":
    main(*sys.argv[1:])
