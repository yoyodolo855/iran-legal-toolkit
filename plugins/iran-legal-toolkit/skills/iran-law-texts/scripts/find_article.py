#!/usr/bin/env python3
"""Print one or more articles from the law texts, or search them, without loading whole files.

Usage:
  find_article.py <law> <number> [<number> ...]   e.g.  find_article.py cpc 49 50
  find_article.py <law> --search "<phrase>"       e.g.  find_article.py tazirat --search "خیانت در امانت"
  find_article.py --list
Law keys: civil, civil-procedure, family, labor, cheque, lease-1376, lease-1376-reg, lease-1362, lease-1356, ipc, tazirat, cpc, labor-procedure, councils
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references")
LAWS = {
    "civil": "civil-code.md",
    "family": "family-protection-1391.md",
    "civil-procedure": "civil-procedure-code-1379.md",
    "labor": "labor-code-1369.md",
    "cheque": "cheque-law.md",
    "lease-1376": "landlord-tenant-1376.md",
    "lease-1376-reg": "landlord-tenant-1376-regulation.md",
    "lease-1362": "landlord-tenant-1362.md",
    "lease-1356": "landlord-tenant-1356.md",
    "ipc": "islamic-penal-code-1392.md",
    "tazirat": "tazirat-1375.md",
    "cpc": "criminal-procedure-code-1392.md",
    "labor-procedure": "labor-procedure-regulation.md",
    "councils": "dispute-councils-1402-art12.md",
}
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def load(key):
    with open(os.path.join(REF, LAWS[key]), encoding="utf-8") as f:
        text = f.read()
    head = text.split("\n## ", 1)[0]
    arts = re.split(r"\n(?=## مادهٔ )", text)[1:]
    return head, arts


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--list":
        for k, v in LAWS.items():
            print(f"{k}\t{v}")
        return 0
    key = argv[0]
    if key not in LAWS:
        print(f"unknown law '{key}'. Use --list.", file=sys.stderr)
        return 2
    head, arts = load(key)
    notice = [l for l in head.splitlines() if l.startswith("> **")]
    if notice:
        print("\n".join(notice[:2]) + "\n")
    if len(argv) >= 3 and argv[1] == "--search":
        q = argv[2]
        hits = [a for a in arts if q in a]
        for a in hits[:15]:
            title = a.splitlines()[0]
            i = a.find(q)
            print(f"{title}: …{a[max(0, i - 80):i + 120].strip()}…\n")
        print(f"[{len(hits)} match(es)]")
        return 0
    found = False
    for n in argv[1:]:
        num = n.translate(FA)
        want = f"## مادهٔ {num}"
        for a in arts:
            first = a.splitlines()[0].strip()
            if first == want or first == want + " مکرر":
                print(a.strip() + "\n")
                found = True
    if not found:
        print("article not found in this source text", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
