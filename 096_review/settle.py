"""Append a round's refuted and minor findings to 096_review/rejected.csv, so later finders skip them.
Reads findings/round_<n>.json and gates/round_<n>.json. Fixed findings are not added.
Usage: python3 settle.py <n> [ids fixed outside the gate ...]"""
import csv, json, sys
from pathlib import Path
HERE = Path(__file__).parent

def rows(n, also_fixed):
    found = json.loads((HERE / f"findings/round_{n}.json").read_text())
    gates = json.loads((HERE / f"gates/round_{n}.json").read_text())
    fixed = set(gates["fixes"]) | set(also_fixed)
    for x in gates["all"]:
        g, f = x["gate"], found[x["i"]]
        if x["id"] in fixed or g["verdict"] == "settled":
            continue
        status = "rejected" if g["verdict"] == "refuted" else "minor"
        yield [f["problem"][:400], status, g["reason"][:600]]

def main(n, *also_fixed):
    path = HERE / "rejected.csv"
    have = list(csv.DictReader(path.open()))
    k = 1 + max(int(r["id"][1:]) for r in have)
    with path.open("a", newline="") as fh:
        w = csv.writer(fh)
        new = list(rows(n, also_fixed))
        for j, (finding, status, reason) in enumerate(new):
            w.writerow([f"R{k + j}", finding, status, f"round {n} gate: {reason}"])
    print(len(new), "rows added")

if __name__ == "__main__":
    main(*sys.argv[1:])
