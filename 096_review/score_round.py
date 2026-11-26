"""Write scores/round_<n>.csv from a round's measurement, gate and change log.
finder_hits counts gate-confirmed material findings that name the key claim.
changed is yes when a confirmed finding on that claim was fixed in this round.
Usage: python3 score_round.py <n> <claude_round.json>"""
import csv, json, sys
from collections import Counter
from pathlib import Path
HERE = Path(__file__).parent

def main(n, claude):
    d = json.load(open(claude)); d = d.get("result", d)
    found = json.loads((HERE / f"findings/round_{n}.json").read_text())
    gates = json.loads((HERE / f"gates/round_{n}.json").read_text())
    fixed = set(gates["fixes"])
    hits = Counter(found[x["i"]]["key"] for x in gates["all"] if x["id"] in fixed)
    with (HERE / f"scores/round_{n}.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "verdict", "changed", "finder_hits", "evidence"])
        for s in sorted(d["scores"], key=lambda s: s["id"]):
            k = s["id"]
            w.writerow([k, s["verdict"], "yes" if hits[k] else "no", hits[k], s["evidence"][:300]])
    print("hits", dict(hits), "not keyed:", sum(v for k, v in hits.items() if not k.startswith("K")))

if __name__ == "__main__":
    main(*sys.argv[1:])
