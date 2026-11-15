#!/usr/bin/env python3
"""Build the single-file portable edition (for ChatGPT, Gemini, Grok, ...) and the law-text files.

Run from anywhere:  python3 tools/build_portable.py
Writes:
  portable/iran-legal-toolkit-portable.md   all skills and references, without full law texts
  portable/laws/*.md                         full law texts, one file per law (optional extra knowledge files)
"""
import json, os, re, shutil, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN = os.path.join(ROOT, "plugins", "iran-legal-toolkit")
OUT = os.path.join(ROOT, "portable")
ORDER = ["iran-legal-core", "iran-civil-litigation", "iran-criminal-procedure",
         "iran-contracts-deeds", "iran-labor-law", "iran-family-law", "iran-property-lease", "iran-official-letters", "iran-law-texts"]
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

HEAD = """# جعبه‌ابزار حقوقی ایران، نسخهٔ قابل حمل ({ver})

تاریخ اعتبار اطلاعات: آبان ۱۴۰۵. این فایل برای هر مدل هوش مصنوعی قابل استفاده است.

سازنده: yoyodolo — https://github.com/yoyodolo855/iran-legal-toolkit (رایگان، با مجوز CC BY 4.0؛ هنگام بازنشر، نام سازنده و این نشانی را بیاورید).

## دستور سیستمی (این بخش را در Instructions / System Prompt بگذارید)

تو دستیار حقوقی برای حقوق ایران هستی و به کسانی کمک می‌کنی که وکیل ندارند. فایل دانش «جعبه‌ابزار حقوقی ایران» در اختیار توست. قواعد:

1. برای هر پرسش حقوقی یا درخواست نگارش، اول بخش `iran-legal-core/SKILL.md` را دنبال کن، سپس بخش حوزهٔ مربوط را (مدنی، کیفری، قرارداد و سند، کار، خانواده و ارث، ملک و اجاره).
2. الگوها و فهرست مواد همین فایل را به حافظهٔ خودت ترجیح بده. شمارهٔ ماده، شمارهٔ رأی یا مبلغ نساز. اگر چیزی در فایل نیست و مطمئن نیستی، بگو باید با متن رسمی تطبیق داده شود.
3. اگر فایل‌های `laws/*.md` (متن کامل قوانین) هم در اختیار توست، برای نقل دقیق ماده فقط همان ماده را در آن‌ها پیدا کن. پوشهٔ `laws/rulings/` آرای وحدت رویه و نظریه‌های مشورتی را دارد؛ در آن فقط با واژه جست‌وجو کن و شمارهٔ رأی یا نظریه را فقط از همان‌جا بیاور.
4. اگر مهلتی در کار است، همان ابتدای پاسخ بگو.
5. متن حقوقی را کامل، به فارسی رسمی و روشن، با جای خالی در قلاب [ ] تحویل بده؛ بعد فهرست مدارک و قدم بعدی را بنویس.
6. نتیجه را تضمین نکن. در پرونده‌های سنگین یا وقتی کسی بازداشت است، راه گرفتن وکیل رایگان را نشان بده.
7. به جعل، شهادت دروغ، فرار از دین یا تهدید کمک نکن.
8. اطلاعات این فایل تا آبان ۱۴۰۵ معتبر است؛ دربارهٔ موضوع‌های فهرست «ناپایدار» این را به کاربر بگو.

هر بخش این فایل با خط `# FILE: مسیر` شروع می‌شود. وقتی متن به `references/...` ارجاع می‌دهد، منظور بخشی با همان مسیر در همین فایل است. متن کامل قوانین در فایل‌های جداگانهٔ `laws/` است.

---
"""


def strip_frontmatter(text, skill):
    m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", text)
    if not m or m.group(1).strip() != skill:
        sys.exit(f"bad frontmatter in {skill}/SKILL.md")
    return text[m.end():]


def demote(text):
    return re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", text, flags=re.M)


def main():
    ver = json.load(open(os.path.join(PLUGIN, ".claude-plugin", "plugin.json"), encoding="utf-8"))["version"]
    parts = [HEAD.format(ver=ver.translate(FA).replace(".", "٫"))]
    for skill in ORDER:
        d = os.path.join(PLUGIN, "skills", skill)
        files = ["SKILL.md"]
        if skill != "iran-law-texts":
            files += sorted("references/" + f for f in os.listdir(os.path.join(d, "references")))
        for f in files:
            t = open(os.path.join(d, f), encoding="utf-8").read()
            if f == "SKILL.md":
                t = strip_frontmatter(t, skill)
            parts.append(f"\n# FILE: {skill}/{f}\n\n{demote(t).strip()}\n")
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "iran-legal-toolkit-portable.md"), "w", encoding="utf-8") as fh:
        fh.write("".join(parts))
    laws_out = os.path.join(OUT, "laws")
    shutil.rmtree(laws_out, ignore_errors=True)
    os.makedirs(laws_out)
    src = os.path.join(PLUGIN, "skills", "iran-law-texts", "references")
    for f in sorted(os.listdir(src)):
        shutil.copy(os.path.join(src, f), os.path.join(laws_out, f))
    rul = os.path.join(PLUGIN, "skills", "iran-law-texts", "rulings")
    if os.path.isdir(rul):
        os.makedirs(os.path.join(laws_out, "rulings"))
        for f in sorted(os.listdir(rul)):
            shutil.copy(os.path.join(rul, f), os.path.join(laws_out, "rulings", f))
    print(f"portable built: {len(parts)-1} sections, {len(os.listdir(laws_out))-1} law files + rulings")


if __name__ == "__main__":
    main()
