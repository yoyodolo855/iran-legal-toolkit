#!/usr/bin/env python3
"""Print one or more articles from the law texts, or search them, without loading whole files.

Usage:
  find_article.py <law> <number> [<number> ...]   e.g.  find_article.py cpc 49 50
  find_article.py <law> --search "<phrase>"       e.g.  find_article.py tazirat --search "خیانت در امانت"
  find_article.py --list
Law keys: civil, civil-procedure, family, labor, cheque, lease-1376, lease-1376-reg, lease-1362, lease-1356, financial-judgments, civil-enforcement, transfer-anothers-property, registration-mandate, councils-full, reduction-1399, registration, computer-crimes, unemployment-insurance, deeds-regulation, administrative-court, commercial-code, housing-1403, pre-sale, pre-sale-reg, registration-reg, fraud-1367, ipc, tazirat, cpc, labor-procedure, councils
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
    "financial-judgments": "financial-judgments-1394.md",
    "civil-enforcement": "civil-judgments-enforcement-1356.md",
    "transfer-anothers-property": "transfer-of-anothers-property-1308.md",
    "registration-mandate": "mandatory-official-registration-1403.md",
    "councils-full": "dispute-councils-1402.md",
    "reduction-1399": "reduction-of-tazir-imprisonment-1399.md",
    "registration": "registration-law-1310.md",
    "computer-crimes": "computer-crimes-1388.md",
    "unemployment-insurance": "unemployment-insurance-1369.md",
    "deeds-regulation": "official-deeds-enforcement-regulation-1387.md",
    "administrative-court": "administrative-court-1392.md",
    "commercial-code": "commercial-code-1311.md",
    "housing-1403": "housing-market-1403.md",
    "pre-sale": "pre-sale-building-1389.md",
    "pre-sale-reg": "pre-sale-building-regulation-1393.md",
    "registration-reg": "registration-law-regulation-1317.md",
    "fraud-1367": "aggravated-fraud-bribery-1367.md",
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
