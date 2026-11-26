"""Claims that the paper prints as fixed wording (captions, set labels), and whether their check is still current.

A claim is verified against the files it depends on. Its stamp is a hash of its wording and of those files.
When the wording or a file changes, the stamp no longer matches: the claim is stale and must be read again.
Pure functions; `stamp.py` is the shell that writes a stamp.
"""
import hashlib


def split_list(field):
    return [x.strip() for x in field.split(";") if x.strip()]


def claim_hash(text, contents):
    """Hash of a claim's wording and of the contents of the files it depends on (in the given order)."""
    h = hashlib.sha256(text.encode())
    for c in contents:
        h.update(b"\0" + c.encode())
    return h.hexdigest()[:16]


def stale(claims, read):
    """Problems for claims whose stamp does not match today's wording and files. read(path) -> file contents."""
    out = []
    for c in claims:
        now = claim_hash(c["text"], [read(p) for p in split_list(c["depends_on"])])
        if not c["verified_hash"].strip():
            out.append(f"claim {c['id']}: never verified; read it against {c['depends_on']} and run stamp.py {c['id']} --by <name>")
        elif c["verified_hash"] != now:
            out.append(f"claim {c['id']}: stale (its wording or {c['depends_on']} changed since {c['verified_by']} "
                       f"verified it); read it again and run stamp.py {c['id']} --by <name>")
    return out
