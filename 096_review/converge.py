"""Convergence report over scored review rounds.

Each round file scores/round_<n>.csv has columns: id, verdict, changed, finder_hits, evidence.
verdict: supported | qualify | refuted (score of the paper as frozen at the start of the round).
changed: yes when that round's fixes changed or qualified the claim in the paper.
finder_hits: accepted findings of that round's blind finders that bear on the claim.
A round is clean when every key claim is supported, none changed, and no accepted finding hits one.
"""
import csv
import sys
from pathlib import Path

VERDICTS = ("supported", "qualify", "refuted")


def load(path):
    rows = {r["id"]: r for r in csv.DictReader(open(path))}
    for r in rows.values():
        if r["verdict"] not in VERDICTS:
            raise ValueError(f"{path}: {r['id']} has verdict {r['verdict']!r}")
    return rows


def summarise(rounds):
    """rounds: list of (name, {id: row}). Returns one summary dict per round."""
    out, prev = [], None
    for name, rows in rounds:
        bad = sorted(i for i, r in rows.items() if r["verdict"] != "supported")
        changed = sorted(i for i, r in rows.items() if r.get("changed") == "yes")
        hits = sum(int(r.get("finder_hits") or 0) for r in rows.values())
        flips = sorted(i for i in rows if prev and i in prev and rows[i]["verdict"] != prev[i]["verdict"])
        out.append({"round": name, "not_supported": bad, "changed": changed, "flips": flips, "hits": hits,
                    "clean": not bad and not changed and not hits})
        prev = rows
    return out


def main(folder):
    files = sorted(Path(folder).glob("round_*.csv"), key=lambda p: int(p.stem.split("_")[1]))
    for s in summarise([(f.stem, load(f)) for f in files]):
        print(f"{s['round']}: not supported {len(s['not_supported'])} {s['not_supported']}; "
              f"changed {len(s['changed'])} {s['changed']}; accepted finder hits {s['hits']}; "
              f"flips vs previous {s['flips']}; "
              f"{'CLEAN' if s['clean'] else 'not clean'}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent / "scores")
