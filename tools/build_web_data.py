#!/usr/bin/env python3
"""Build static JSON data for the in-browser chat on GitHub Pages (no server).

Writes docs/data/:
  manifest.json          version, law keys with titles and file names, guide list, ruling files
  guides.json            the nine SKILL.md bodies plus their references (path -> text)
  laws/<key>.json        one law: {"key","title","head","articles":[[label, text], ...]}
  rulings/<name>.json    one rulings file split the same way (## headings)
  system-prompt.md       the short system prompt for the chat

The browser loads manifest + guides once, then fetches only the law or ruling files a question needs.
"""
import importlib.util, json, os, re, shutil, sys

sys.dont_write_bytecode = True

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN = os.path.join(ROOT, "plugins", "iran-legal-toolkit")
SK = os.path.join(PLUGIN, "skills")
LT = os.path.join(SK, "iran-law-texts")
OUT = os.path.join(ROOT, "docs", "data")


def split(text):
    head, *rest = re.split(r"\n(?=## )", text)
    arts = []
    for a in rest:
        first, _, body = a.partition("\n")
        arts.append([first[3:].strip(), body.strip()])
    return head.strip(), arts


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, separators=(",", ":"))


def main():
    spec = importlib.util.spec_from_file_location("fa", os.path.join(LT, "scripts", "find_article.py"))
    fa = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fa)
    version = json.load(open(os.path.join(PLUGIN, "plugin.json"), encoding="utf-8"))["version"]
    shutil.rmtree(OUT, ignore_errors=True)

    laws = []
    for key, fn in fa.LAWS.items():
        text = open(os.path.join(LT, "references", fn), encoding="utf-8").read()
        title = text.splitlines()[0].lstrip("# ").strip()
        head, arts = split(text)
        dump(os.path.join(OUT, "laws", key + ".json"), {"key": key, "title": title, "head": head, "articles": arts})
        laws.append({"key": key, "title": title, "articles": len(arts)})

    rulings = []
    for fn in sorted(os.listdir(os.path.join(LT, "rulings"))):
        text = open(os.path.join(LT, "rulings", fn), encoding="utf-8").read()
        title = text.splitlines()[0].lstrip("# ").strip()
        head, arts = split(text)
        name = fn[:-3]
        dump(os.path.join(OUT, "rulings", name + ".json"), {"key": name, "title": title, "head": head, "articles": arts})
        rulings.append({"key": name, "title": title, "items": len(arts)})

    guides = {}
    for skill in sorted(os.listdir(SK)):
        if skill == "iran-law-texts":
            guides[f"{skill}/SKILL.md"] = open(os.path.join(SK, skill, "SKILL.md"), encoding="utf-8").read()
            continue
        base = os.path.join(SK, skill)
        for dp, dn, fns in os.walk(base):
            dn[:] = [d for d in dn if d not in ("evals", "__pycache__")]
            for f in fns:
                if f.endswith(".md"):
                    rel = os.path.relpath(os.path.join(dp, f), SK).replace(os.sep, "/")
                    guides[rel] = open(os.path.join(dp, f), encoding="utf-8").read()
    dump(os.path.join(OUT, "guides.json"), guides)
    dump(os.path.join(OUT, "manifest.json"), {"version": version, "laws": laws, "rulings": rulings, "guides": sorted(guides)})
    shutil.copy(os.path.join(ROOT, "portable", "system-prompt-mini.md"), os.path.join(OUT, "system-prompt.md"))
    size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print(f"web data: {len(laws)} laws, {len(rulings)} ruling files, {len(guides)} guide files, {size // 1024} KB")


if __name__ == "__main__":
    main()
