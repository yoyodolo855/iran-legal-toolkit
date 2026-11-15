#!/usr/bin/env python3
"""Build the downloadable files in dist/ (deterministic, so the checker can verify them).

  dist/iran-legal-toolkit.plugin           Claude plugin (skills without test cases)
  dist/iran-legal-toolkit-portable.md      single file for ChatGPT, Gemini, Grok, ...
  dist/iran-legal-toolkit-lite.md          small single file (guides only) for chats with small context
  dist/iran-legal-toolkit-skill(-lite).zip universal Agent Skill upload (see tools/build_universal.py)
  dist/laws.zip                            full law texts, one Markdown file per law
"""
import os, shutil, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN = os.path.join(ROOT, "plugins", "iran-legal-toolkit")
DIST = os.path.join(ROOT, "dist")
STAMP = (2026, 1, 1, 0, 0, 0)


def add_tree(zf, base, prefix="", skip=lambda rel: False):
    files = []
    for dp, dn, fn in os.walk(base):
        for f in fn:
            p = os.path.join(dp, f)
            files.append((os.path.relpath(p, base).replace(os.sep, "/"), p))
    for rel, p in sorted(files):
        if skip(rel):
            continue
        info = zipfile.ZipInfo(prefix + rel, STAMP)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (0o755 if rel.endswith(".py") else 0o644) << 16
        with open(p, "rb") as fh:
            zf.writestr(info, fh.read())


def main():
    os.makedirs(DIST, exist_ok=True)
    with zipfile.ZipFile(os.path.join(DIST, "iran-legal-toolkit.plugin"), "w") as zf:
        add_tree(zf, PLUGIN, skip=lambda r: "/evals/" in r or "__pycache__" in r or r.endswith((".DS_Store", ".pyc")))
    for f in ("iran-legal-toolkit-portable.md", "iran-legal-toolkit-lite.md"):
        shutil.copy(os.path.join(ROOT, "portable", f), DIST)
    with zipfile.ZipFile(os.path.join(DIST, "laws.zip"), "w") as zf:
        add_tree(zf, os.path.join(ROOT, "portable", "laws"), prefix="laws/")
    import importlib.util  # load by path: check.py runs this script with -I
    spec = importlib.util.spec_from_file_location("build_universal", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_universal.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()
    print("dist built:", ", ".join(sorted(os.listdir(DIST))))


if __name__ == "__main__":
    main()
