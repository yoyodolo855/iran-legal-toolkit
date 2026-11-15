#!/usr/bin/env python3
"""Check that every article the guides cite exists in the full law texts.

For each citation like «مادهٔ ۱۰۸ ق.آ.د.م» or «مواد ۱۵۸ تا ۱۷۷ قانون آیین دادرسی مدنی» in the
skills (not in the law texts themselves), look the article up in iran-law-texts.
Prints problems; exit code 1 if any cited article is missing from its source text.
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SK = os.path.join(ROOT, "plugins", "iran-legal-toolkit", "skills")
REF = os.path.join(SK, "iran-law-texts", "references")
EN = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

# law marker -> reference file. Order matters: longer/more specific first.
MARKERS = [
    (r"ق\.آ\.د\.م|قانون آیین دادرسی مدنی|آیین دادرسی مدنی", "civil-procedure-code-1379.md"),
    (r"ق\.آ\.د\.ک|قانون آیین دادرسی کیفری", "criminal-procedure-code-1392.md"),
    (r"ق\.م\.ا|قانون مجازات اسلامی", "islamic-penal-code-1392.md"),
    (r"ق\.م(?![.\w])|قانون مدنی", "civil-code.md"),
    (r"ق\.ک(?![.\w])|قانون کار(?! ?کشاورزی)", "labor-code-1369.md"),
    (r"ق\.ت(?![.\w])|قانون تجارت", "commercial-code-1311.md"),
    (r"کتاب تعزیرات|تعزیرات", "tazirat-1375.md"),
    (r"قانون حمایت خانواده", "family-protection-1391.md"),
    (r"قانون صدور چک", "cheque-law.md"),
    (r"قانون ثبت", "registration-law-1310.md"),
    (r"قانون نحوهٔ اجرای محکومیت‌های مالی|قانون ۱۳۹۴", "financial-judgments-1394.md"),
    (r"قانون روابط موجر و مستأجر ۱۳۷۶|قانون ۱۳۷۶", "landlord-tenant-1376.md"),
    (r"قانون تأمین اجتماعی", "social-security-1354.md"),
    (r"قانون بیمهٔ بیکاری", "unemployment-insurance-1369.md"),
    (r"قانون مالیات‌های مستقیم", "direct-taxes.md"),
]
CITE = re.compile(r"(مادهٔ|ماده|مواد)\s+((?:[۰-۹]+(?:\s*مکرر)?(?:\s*(?:،|و|تا)\s*)?)+)(?:\s*\(?[^\n.؛]{0,25}?)\s*(?P<law>" + "|".join(m for m, _ in MARKERS) + r")")


def articles(fname, cache={}):
    if fname not in cache:
        t = open(os.path.join(REF, fname), encoding="utf-8").read()
        cache[fname] = {int(x.translate(EN)) for x in re.findall(r"^## مادهٔ ([۰-۹]+)", t, re.M)}
        if fname == "tazirat-1375.md":   # computer crimes are articles 729-783 of the same book
            t2 = open(os.path.join(REF, "computer-crimes-1388.md"), encoding="utf-8").read()
            cache[fname] |= {int(x.translate(EN)) for x in re.findall(r"^## مادهٔ ([۰-۹]+)", t2, re.M)}
    return cache[fname]


def expand(nums):
    out, prev, rng = [], None, False
    for tok in re.findall(r"[۰-۹]+|تا", nums):
        if tok == "تا":
            rng = True
            continue
        n = int(tok.translate(EN))
        if rng and prev is not None and 0 < n - prev <= 60:
            out += list(range(prev + 1, n + 1))
        else:
            out.append(n)
        prev, rng = n, False
    return out


# articles the guides cite correctly but the source text could not supply (OCR gaps)
KNOWN_GAPS = {("registration-law-1310.md", 93)}


def main():
    total, problems = 0, []
    for dp, dn, fn in os.walk(SK):
        if "iran-law-texts" in dp or "evals" in dp:
            continue
        for f in fn:
            if not f.endswith(".md"):
                continue
            path = os.path.join(dp, f)
            text = open(path, encoding="utf-8").read()
            for line_no, line in enumerate(text.splitlines(), 1):
                for m in CITE.finditer(line):
                    law = next(fname for pat, fname in MARKERS if re.fullmatch(pat, m.group("law")))
                    have = articles(law)
                    for n in expand(m.group(2)):
                        total += 1
                        if n not in have and (law, n) not in KNOWN_GAPS:
                            problems.append(f"{os.path.relpath(path, SK)}:{line_no}: article {n} not in {law}  «{m.group(0)[:70]}»")
    for p in problems:
        print(p)
    print(f"[{total} citations checked, {len(problems)} not found]")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
