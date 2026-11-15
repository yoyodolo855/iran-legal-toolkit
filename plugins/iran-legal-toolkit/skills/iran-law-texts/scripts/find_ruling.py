#!/usr/bin/env python3
"""Search unification rulings and advisory opinions without loading whole files.

Usage:
  find_ruling.py --search "<word>" ["<word>" ...] [--max N]   all words must appear (default max 5)
  find_ruling.py --number 799            a unification ruling by number
  find_ruling.py --number 7/1405/276     an advisory opinion by number
  find_ruling.py --list
Words may be typed with Persian or Latin digits.
"""
import glob, os, re, signal, sys

if hasattr(signal, "SIGPIPE"):
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "..", "rulings")
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def norm(s):
    s = s.translate(FA).replace("ي", "ی").replace("ك", "ک").replace("‌", " ")
    return re.sub(r"\s+", " ", s)



_LMAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ة": "ه", "ؤ": "و", "ئ": "ی", "ي": "ی", "ك": "ک", "\u0654": None, "\u064b": None, "\u064c": None, "\u064d": None, "\u064e": None, "\u064f": None, "\u0650": None, "\u0651": None, "\u0652": None, "\u0640": None})


def loose(s):
    """Spacing- and spelling-tolerant form for searching: ignores spaces, half-spaces and hamza/diacritic variants."""
    return re.sub(r"[\s\u200c\u200f\u200e]+", "", s.translate(FA).translate(_LMAP))

def blocks():
    for path in sorted(glob.glob(os.path.join(DIR, "*.md"))):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for b in re.split(r"\n(?=## )", text)[1:]:
            yield os.path.basename(path), b.strip()


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--list":
        for path in sorted(glob.glob(os.path.join(DIR, "*.md"))):
            n = sum(1 for _ in re.finditer(r"^## ", open(path, encoding="utf-8").read(), re.M))
            print(f"{os.path.basename(path)}\t{n}")
        return 0
    if argv[0] == "--number" and len(argv) > 1:
        key = norm(argv[1])
        for name, b in blocks():
            head = norm(b.split("\n", 1)[0])
            if re.search(r"(?<![۰-۹/])" + re.escape(key) + r"(?![۰-۹/])", head):
                if len(b) > 8000:
                    b = b[:8000] + f"\n…[بقیه بریده شد؛ {len(b) - 8000} نویسهٔ دیگر]"
                print(f"[{name}]\n{b}\n")
                return 0
        print("not found")
        return 1
    if argv[0] == "--search":
        words, mx = [], 5
        rest = argv[1:]
        if "--max" in rest:
            i = rest.index("--max")
            try:
                mx = int(rest[i + 1])
            except (IndexError, ValueError):
                print("--max needs a number", file=sys.stderr)
                return 2
            mx = max(1, min(mx, 50))
            rest = rest[:i] + rest[i + 2:]
        words = [loose(w)[:200] for w in rest if w.strip()]
        if not words:
            print("--search needs at least one word", file=sys.stderr)
            return 2
        hits = 0
        for name, b in blocks():
            nb = loose(b)
            if all(w in nb for w in words):
                hits += 1
                if hits <= mx:
                    print(f"[{name}]\n{b}\n")
        print(f"[{hits} match(es){', showing ' + str(mx) if hits > mx else ''}]")
        return 0 if hits else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
