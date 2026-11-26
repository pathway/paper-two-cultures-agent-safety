"""Record that a person or a model has read a claim against the files it depends on.

Usage: python3 stamp.py <claim id> [<claim id> ...] --by <name>      (the build never runs this)
"""
from pathlib import Path
import csv
import sys
import time

import claims

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "095_claims/claims.csv"


def main(ids, by):
    rows = list(csv.DictReader(open(PATH, newline="")))
    for r in rows:
        if r["id"] in ids:
            contents = [(ROOT / p).read_text() for p in claims.split_list(r["depends_on"])]
            r.update(verified_hash=claims.claim_hash(r["text"], contents), verified_by=by, verified_on=time.strftime("%Y-%m-%d"))
            print("stamped", r["id"], "by", by)
    with open(PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args[:args.index("--by")], args[args.index("--by") + 1])
