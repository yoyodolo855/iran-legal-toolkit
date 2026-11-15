#!/usr/bin/env python3
"""Print one or more articles from the law texts, or search them, without loading whole files.

Usage:
  find_article.py <law> <number> [<number> ...]   e.g.  find_article.py cpc 49 50
  find_article.py <law> --search "<phrase>"       e.g.  find_article.py tazirat --search "خیانت در امانت"
  find_article.py --list
Law keys: civil, civil-procedure, family, labor, cheque, lease-1376, lease-1376-reg, lease-1362, lease-1356, financial-judgments, civil-enforcement, transfer-anothers-property, registration-mandate, councils-full, reduction-1399, registration, computer-crimes, unemployment-insurance, deeds-regulation, administrative-court, commercial-code, joint-stock-1347, housing-1403, pre-sale, pre-sale-reg, registration-reg, fraud-1367, consumer, third-party-insurance, social-security, direct-taxes, sodagari-1404, farmland-use-1374, land-reform-reg, civil-liability, narcotics, arms, smuggling, armed-forces, youth-population, municipality, vat, registration-text, pazireh, constitution, non-contentious, partition, pos-terminals, e-notification, apartment, apartment-reg, cooperative, guild, e-services-offices, medical-council, medical-disciplinary, engineering, government-revenues, guild-amendment, ipc, tazirat, cpc, labor-procedure, councils
"""
import os, re, signal, sys

if hasattr(signal, "SIGPIPE"):
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

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
    "administrative-court": "administrative-court-1402.md",
    "commercial-code": "commercial-code-1311.md",
    "joint-stock-1347": "joint-stock-1347.md",
    "housing-1403": "housing-market-1403.md",
    "pre-sale": "pre-sale-building-1389.md",
    "pre-sale-reg": "pre-sale-building-regulation-1393.md",
    "registration-reg": "registration-law-regulation-1317.md",
    "fraud-1367": "aggravated-fraud-bribery-1367.md",
    "consumer": "consumer-protection-1388.md",
    "third-party-insurance": "third-party-insurance-1395.md",
    "social-security": "social-security-1354.md",
    "direct-taxes": "direct-taxes.md",
    "sodagari-1404": "sodagari-1404.md",
    "farmland-use-1374": "farmland-use-1374.md",
    "land-reform-reg": "land-reform-regulation-1343.md",
    "civil-liability": "civil-liability-1339.md",
    "narcotics": "narcotics-1367.md",
    "arms": "arms-smuggling-1390.md",
    "smuggling": "smuggling-goods-currency-1392.md",
    "armed-forces": "armed-forces-crimes-1382.md",
    "youth-population": "youth-population-1400.md",
    "municipality": "municipality-1334.md",
    "vat": "vat-1400.md",
    "registration-text": "registration-law-1310-text.md",
    "pazireh": "pazireh-regulation-1365.md",
    "constitution": "constitution.md",
    "non-contentious": "non-contentious-1319.md",
    "partition": "partition-1357.md",
    "pos-terminals": "pos-terminals-1398.md",
    "e-notification": "e-notification-1395.md",
    "apartment": "apartment-ownership-1343.md",
    "apartment-reg": "apartment-ownership-regulation-1347.md",
    "cooperative": "cooperative-sector-1370.md",
    "guild": "guild-system-1382.md",
    "e-services-offices": "e-services-offices-1396.md",
    "medical-council": "medical-council-1383.md",
    "medical-disciplinary": "medical-disciplinary-regulation-1390.md",
    "engineering": "engineering-building-control-1374.md",
    "government-revenues": "government-revenues-1373.md",
    "guild-amendment": "guild-amendment-1392.md",
    "ipc": "islamic-penal-code-1392.md",
    "tazirat": "tazirat-1375.md",
    "cpc": "criminal-procedure-code-1392.md",
    "labor-procedure": "labor-procedure-regulation.md",
    "councils": "dispute-councils-1402-art12.md",
}
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
LAT = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")



_LMAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ة": "ه", "ؤ": "و", "ئ": "ی", "ي": "ی", "ك": "ک", "\u0654": None, "\u064b": None, "\u064c": None, "\u064d": None, "\u064e": None, "\u064f": None, "\u0650": None, "\u0651": None, "\u0652": None, "\u0640": None})


def loose(s):
    """Spacing- and spelling-tolerant form for searching: ignores spaces, half-spaces and hamza/diacritic variants."""
    return re.sub(r"[\s\u200c\u200f\u200e]+", "", s.translate(FA).translate(_LMAP))

def load(key):
    with open(os.path.join(REF, LAWS[key]), encoding="utf-8") as f:
        text = f.read()
    head = text.split("\n## ", 1)[0]
    arts = re.split(r"\n(?=## )", text)[1:]
    return head, arts


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--list":
        for k, v in LAWS.items():
            try:
                with open(os.path.join(REF, v), encoding="utf-8") as fh:
                    title = fh.readline().lstrip("# ").strip()
            except OSError:
                continue  # not in this package (lite build)
            print(f"{k}\t{title}")
        return 0
    key = argv[0]
    if key not in LAWS:
        print(f"unknown law '{key}'. Use --list.", file=sys.stderr)
        return 2
    if not os.path.isfile(os.path.join(REF, LAWS[key])):
        print(f"law '{key}' ({LAWS[key]}) is not in this package. Full text: the full package "
              "iran-legal-toolkit-skill.zip, or https://qavanin.ir", file=sys.stderr)
        return 3
    head, arts = load(key)
    notice = [l for l in head.splitlines() if l.startswith("> **")]
    if notice:
        print("\n".join(notice[:2]) + "\n")
    if len(argv) < 2:
        print("give an article number or --search \"<phrase>\"", file=sys.stderr)
        return 2
    if argv[1] == "--search":
        if len(argv) < 3 or not argv[2].strip():
            print("--search needs a phrase", file=sys.stderr)
            return 2
        q = argv[2].translate(FA).replace("ي", "ی").replace("ك", "ک")[:200]
        lq = loose(q)
        hits = [a for a in arts if lq and lq in loose(a)]
        for a in hits[:15]:
            title = a.splitlines()[0]
            i = a.translate(FA).find(q)
            if i < 0:
                i = a.translate(FA).find(q.split()[0]) if q.split() else 0
            i = max(i, 0)
            print(f"{title}: …{a[max(0, i - 80):i + 120].strip()}…\n")
        print(f"[{len(hits)} match(es)]")
        return 0
    found = False
    for n in argv[1:]:
        num = n.translate(FA).strip()
        num = re.sub(r"\s*مکرر.*$", "", num)
        if not re.fullmatch(r"[۰-۹]{1,4}", num):
            print(f"not an article number: {n!r}", file=sys.stderr)
            continue
        if key == "computer-crimes" and int(num.translate(LAT)) <= 55:
            alt = str(int(num.translate(LAT)) + 728).translate(FA)
            print(f"(مادهٔ {num} قانون جرایم رایانه‌ای = مادهٔ {alt} تعزیرات)\n")
            num = alt
        want = f"## مادهٔ {num}" if key != "constitution" else f"## اصل {num}"
        for a in arts:
            first = a.splitlines()[0].strip()
            if first == want or first.startswith(want + " مکرر"):
                print(a.strip() + "\n")
                found = True
    if not found:
        print("article not found in this source text", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
