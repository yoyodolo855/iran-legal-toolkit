#!/usr/bin/env python3
"""Build the universal Agent Skill (one SKILL.md at the root) for chat apps that accept
skill uploads: Claude.ai, ChatGPT, Gemini, Grok, Perplexity, Mistral, Copilot.

  dist/iran-legal-toolkit-skill.zip       full: every guide, law text and ruling
  dist/iran-legal-toolkit-skill-lite.zip  under 100 files, for apps with a file cap

Inside the zip everything sits in one folder `iran-legal-toolkit/`:
  SKILL.md                                 router (the only SKILL.md in the package)
  guides/<skill>/GUIDE.md                  each original skill, renamed so uploaders see one SKILL.md
  guides/<skill>/references|rulings|scripts
"""
import io, os, re, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS = os.path.join(ROOT, "plugins", "iran-legal-toolkit", "skills")
DIST = os.path.join(ROOT, "dist")
STAMP = (2026, 1, 1, 0, 0, 0)
NAME = "iran-legal-toolkit"

# laws kept in the lite package (most used); everything else is full-only
LITE_LAWS = {
    "civil-code.md", "civil-procedure-code-1379.md", "family-protection-1391.md", "labor-code-1369.md",
    "cheque-law.md", "landlord-tenant-1376.md", "landlord-tenant-1362.md", "landlord-tenant-1356.md",
    "financial-judgments-1394.md", "civil-judgments-enforcement-1356.md", "transfer-of-anothers-property-1308.md",
    "mandatory-official-registration-1403.md", "dispute-councils-1402.md", 
    "reduction-of-tazir-imprisonment-1399.md", "registration-law-1310-text.md", "computer-crimes-1388.md",
    "social-security-1354.md", "third-party-insurance-1395.md", "islamic-penal-code-1392.md", "tazirat-1375.md",
    "criminal-procedure-code-1392.md", "labor-procedure-regulation.md", "constitution.md", "civil-liability-1339.md",
    "non-contentious-1319.md", "partition-1357.md", "apartment-ownership-1343.md", "apartment-ownership-regulation-1347.md",
    "e-notification-1395.md", "youth-population-1400.md", "pre-sale-building-1389.md", "consumer-protection-1388.md",
    "unemployment-insurance-1369.md", "administrative-court-1402.md",
}
LITE_RULINGS = {
    "supreme-court-unification-1390-1402.md", "supreme-court-unification-1402-1405.md",
    "supreme-court-unification-1404.md", "advisory-opinions-1404.md", "advisory-opinions-1405.md",
    "guardian-council-interpretations.md",
}
SKILL_NAMES = sorted(d for d in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md")))


def rewrite(text):
    """Point cross-skill paths and script calls at their place inside the bundle."""
    for s in SKILL_NAMES:
        text = re.sub(r"(?<![\w/-])" + re.escape(s) + r"/SKILL\.md", f"guides/{s}/GUIDE.md", text)
        text = re.sub(r"(?<![\w/-])" + re.escape(s) + r"/(references|rulings|scripts)/", f"guides/{s}/\\1/", text)
    text = re.sub(r"python3 scripts/(find_article|find_ruling)\.py", r"python3 guides/iran-law-texts/scripts/\1.py", text)
    return text


def router():
    core = open(os.path.join(SKILLS, "iran-legal-core", "SKILL.md"), encoding="utf-8").read()
    rows = []
    for s in SKILL_NAMES:
        t = open(os.path.join(SKILLS, s, "SKILL.md"), encoding="utf-8").read()
        d = re.search(r"^description:\s*(.+)$", t, re.M).group(1)
        d = re.split(r"(?<=[.؛])\s", d)[0][:170]
        rows.append(f"| `guides/{s}/GUIDE.md` | {d} |")
    return f"""---
name: {NAME}
description: جعبه‌ابزار حقوقی رایگان ایران برای کسی که وکیل ندارد. هر وقت کاربر دربارهٔ حقوق و قوانین ایران می‌پرسد یا می‌خواهد دادخواست، شکواییه، لایحه، اظهارنامه، قرارداد، اقرارنامه یا نامهٔ اداری بنویسد (کار و بیمه، مهریه و طلاق و ارث، اجاره و ملک، چک و طلب، شکایت کیفری، مهلت‌ها، مرجع صالح، هزینهٔ دادرسی) از این اسکیل استفاده کن. متن کامل قوانین و آرای وحدت رویه را دارد. Free Iranian legal toolkit: court filings, complaints, contracts, deadlines, jurisdiction, full statute texts and unification rulings.
---

# جعبه‌ابزار حقوقی ایران

این بسته نُه راهنمای تخصصی و متن کامل قوانین ایران را دارد. همهٔ فایل‌ها زیر پوشهٔ `guides/` است. هیچ فایلی را کامل نخوان مگر لازم باشد؛ فقط راهنمای همان موضوع را باز کن.

## ترتیب کار

1. **اول همیشه** `guides/iran-legal-core/GUIDE.md` را بخوان: روش کار، قواعد ارجاع، مرجع صالح، مهلت‌ها و هزینه‌ها آن‌جاست.
2. بعد راهنمای موضوع را از جدول زیر باز کن و فقط فایل‌های ارجاع‌شده در همان راهنما را بخوان.
3. شمارهٔ ماده یا رأی را هرگز از حافظه نگو. اگر می‌توانی کد اجرا کنی: `python3 guides/iran-law-texts/scripts/find_article.py civil 10` یا `find_article.py civil --search "عبارت"`، و برای رأی `python3 guides/iran-law-texts/scripts/find_ruling.py --number 873`. اگر نمی‌توانی، در فایل قانون دنبال سرتیتر `## مادهٔ ۱۰` بگرد. فهرست قوانین: `guides/iran-law-texts/references/INDEX.md`.

| راهنما | کاربرد |
|---|---|
{chr(10).join(rows)}

## یادداشت مسیرها

در متن راهنماها هر جا نام اسکیل دیگری آمده (مثلاً `iran-legal-core/references/deadlines.md`)، آن فایل در این بسته زیر `guides/` است (`guides/iran-legal-core/references/deadlines.md`)، و `SKILL.md` هر راهنما این‌جا `GUIDE.md` نام دارد.

## قواعدی که همیشه برقرار است

- پاسخ فارسی، ساده و گام‌به‌گام؛ اصطلاح حقوقی را یک بار توضیح بده.
- قانونی بودن یا نبودن کار کاربر را صادقانه بگو؛ اگر پرونده پیچیده یا پرخطر است، گرفتن مشاوره از وکیل یا معاضدت قضایی رایگان را پیشنهاد کن.
- اگر اطلاعات لازم (تاریخ، مبلغ، نوع سند، شهر) را نداری، پیش از نوشتن متن نهایی بپرس.
- ارقام سالانه (هزینهٔ دادرسی، مزد، دیه) را فقط از فایل‌های همان سال بگو و سال را ذکر کن.
"""


def collect(lite):
    files = []
    for s in SKILL_NAMES:
        base = os.path.join(SKILLS, s)
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if d not in ("evals", "__pycache__")]
            for f in fn:
                if f.endswith((".pyc", ".DS_Store")) or f.startswith("."):
                    continue
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, base).replace(os.sep, "/")
                if lite and s == "iran-law-texts":
                    if rel.startswith("references/") and os.path.basename(rel) not in LITE_LAWS | {"INDEX.md"}:
                        continue
                    if rel.startswith("rulings/") and os.path.basename(rel) not in LITE_RULINGS:
                        continue
                arc = f"guides/{s}/" + ("GUIDE.md" if rel == "SKILL.md" else rel)
                files.append((arc, p))
    return sorted(files)


def build(lite):
    out = os.path.join(DIST, f"{NAME}-skill{'-lite' if lite else ''}.zip")
    entries = [("SKILL.md", router().encode("utf-8"))]
    for arc, p in collect(lite):
        data = open(p, "rb").read()
        if arc.endswith(".md"):
            data = rewrite(data.decode("utf-8")).encode("utf-8")
        entries.append((arc, data))
    if lite:
        n = str(sum(1 for a, _ in entries if "/iran-law-texts/references/" in a and not a.endswith("INDEX.md")))
        note = (f"\n> ⚠️ نسخهٔ سبک: فقط {n.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))} قانون پرکاربرد در این بسته هست. اگر find_article.py گفت فایل نیست، "
                "به کاربر بگو متن آن قانون در نسخهٔ کامل (iran-legal-toolkit-skill.zip) یا qavanin.ir است.\n")
        entries[0] = ("SKILL.md", entries[0][1] + note.encode("utf-8"))
    with zipfile.ZipFile(out, "w") as zf:
        for arc, data in entries:
            info = zipfile.ZipInfo(f"{NAME}/{arc}", STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if arc.endswith(".py") else 0o644) << 16
            zf.writestr(info, data)
    return out, len(entries)


def main():
    os.makedirs(DIST, exist_ok=True)
    for lite in (False, True):
        out, n = build(lite)
        print(f"{os.path.basename(out)}: {n} files, {os.path.getsize(out)//1024} KB")


if __name__ == "__main__":
    main()
