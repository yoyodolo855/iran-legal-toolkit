#!/usr/bin/env python3
"""Checks run on every change (locally and in GitHub Actions).

1. Plugin structure: manifest, every skill has valid frontmatter, every referenced file exists.
2. Safety scan: hidden bidi/zero-width characters, prompt-injection phrases, secrets, executable surprises.
3. Privacy: no personal names or e-mail addresses besides the maintainer handle.
4. Portable edition is up to date with the plugin source.
5. Law texts: article headings are in order and the lookup script works.
"""
import json, os, re, subprocess, sys, tempfile, filecmp

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN = os.path.join(ROOT, "plugins", "iran-legal-toolkit")
errors = []


def err(msg):
    errors.append(msg)


def check_structure():
    mf = json.load(open(os.path.join(PLUGIN, ".claude-plugin", "plugin.json"), encoding="utf-8"))
    if not re.fullmatch(r"[a-z0-9-]+", mf.get("name", "")):
        err("plugin name must be kebab-case")
    for skill in sorted(os.listdir(os.path.join(PLUGIN, "skills"))):
        d = os.path.join(PLUGIN, "skills", skill)
        t = open(os.path.join(d, "SKILL.md"), encoding="utf-8").read()
        m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", t)
        if not m or m.group(1).strip() != skill:
            err(f"{skill}: bad frontmatter")
            continue
        if len(m.group(2)) > 1024:
            err(f"{skill}: description longer than 1024 characters")
        for ref in set(re.findall(r"`((?:references|scripts)/[\w.-]+)`", t)):
            if not os.path.exists(os.path.join(d, ref)):
                err(f"{skill}: missing {ref}")


HIDDEN = {0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069, 0x200B, 0x200E, 0x200F, 0xFEFF, 0x2060}
INJECT = re.compile(r"ignore (all|previous|the above)|disregard (all|previous)|you are now|system prompt override|<script|BEGIN (RSA|OPENSSH|PGP)|api[_-]?key\s*[:=]|password\s*[:=]", re.I)
PRIVACY = re.compile(r"(?<![/\w])[\w.+-]+@[\w-]+\.[a-z]{2,}\b", re.I)
ALLOWED_MAIL = ("noreply.github.com",)


def check_safety():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", "node_modules", "_site")]
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, ROOT)
            try:
                t = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                if not f.endswith((".png", ".jpg", ".ico", ".woff2", ".zip", ".plugin")):
                    err(f"{rel}: not UTF-8 text")
                continue
            bad = {hex(ord(c)) for c in t if ord(c) in HIDDEN}
            if bad:
                err(f"{rel}: hidden characters {sorted(bad)}")
            if rel != os.path.join("tools", "check.py"):
                for m in INJECT.finditer(t):
                    err(f"{rel}: suspicious text '{m.group(0)}'")
                for m in PRIVACY.finditer(t):
                    if not m.group(0).endswith(ALLOWED_MAIL):
                        err(f"{rel}: e-mail address found ({m.group(0)})")


def check_portable():
    with tempfile.TemporaryDirectory() as tmp:
        cur = os.path.join(ROOT, "portable", "iran-legal-toolkit-portable.md")
        if not os.path.exists(cur):
            err("portable edition missing; run tools/build_portable.py")
            return
        before = open(cur, encoding="utf-8").read()
        subprocess.run([sys.executable, "-I", os.path.join(ROOT, "tools", "build_portable.py")], check=True, capture_output=True)
        after = open(cur, encoding="utf-8").read()
        if before != after:
            err("portable edition was out of date (rebuilt now; commit the result)")


def _content(p):
    # Compare what is inside a zip, not its compressed bytes: zlib output can
    # differ between Python builds even when every file inside is identical.
    if not os.path.exists(p):
        return None
    if p.endswith((".zip", ".plugin")):
        import zipfile
        with zipfile.ZipFile(p) as zf:
            return [(i.filename, i.external_attr, zf.read(i)) for i in zf.infolist()]
    return open(p, "rb").read()


def check_dist():
    names = ["iran-legal-toolkit.plugin", "iran-legal-toolkit-portable.md", "laws.zip"]
    before = {n: _content(os.path.join(ROOT, "dist", n)) for n in names}
    subprocess.run([sys.executable, "-I", os.path.join(ROOT, "tools", "build_dist.py")], check=True, capture_output=True)
    for n in names:
        if _content(os.path.join(ROOT, "dist", n)) != before[n]:
            err(f"dist/{n} was out of date (rebuilt now; commit the result)")


def check_laws():
    d = os.path.join(PLUGIN, "skills", "iran-law-texts")
    for f in os.listdir(os.path.join(d, "references")):
        t = open(os.path.join(d, "references", f), encoding="utf-8").read()
        nums = [int(n.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))) for n in re.findall(r"^## مادهٔ ([۰-۹]+)", t, re.M)]
        if nums != sorted(nums):
            err(f"law-texts/{f}: article headings out of order")
    r = subprocess.run([sys.executable, "-I", os.path.join(d, "scripts", "find_article.py"), "cpc", "49"], capture_output=True, text=True)
    if r.returncode != 0 or "یک ساعت" not in r.stdout:
        err("find_article.py failed on a known article (cpc 49)")


if __name__ == "__main__":
    check_structure()
    check_safety()
    check_laws()
    check_portable()
    check_dist()
    if errors:
        print("FAILED:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("all checks passed")
