#!/usr/bin/env python3
"""Build the downloadable files in dist/ (deterministic, so the checker can verify them).

  dist/iran-legal-toolkit.plugin           Claude plugin (skills without test cases)
  dist/iran-legal-toolkit-portable.md      single file for ChatGPT, Gemini, Grok, ...
  dist/laws.zip                            full law texts, one Markdown file per law
"""
import os, shutil, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN = os.path.join(ROOT, "plugins", "iran-legal-toolkit")
DIST = os.path.join(ROOT, "dist")
STAMP = (2026, 1, 1, 0, 0, 0)


def add_tree(zf, base, prefix="", skip=lambda rel: False):
    for dp, dn, fn in sorted(os.walk(base)):
        dn.sort()
        for f in sorted(fn):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, base).replace(os.sep, "/")
            if skip(rel):
                continue
            info = zipfile.ZipInfo(prefix + rel, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if os.access(p, os.X_OK) else 0o644) << 16
            with open(p, "rb") as fh:
                zf.writestr(info, fh.read())


def main():
    os.makedirs(DIST, exist_ok=True)
    with zipfile.ZipFile(os.path.join(DIST, "iran-legal-toolkit.plugin"), "w") as zf:
        add_tree(zf, PLUGIN, skip=lambda r: "/evals/" in r or r.endswith(".DS_Store"))
    shutil.copy(os.path.join(ROOT, "portable", "iran-legal-toolkit-portable.md"), DIST)
    with zipfile.ZipFile(os.path.join(DIST, "laws.zip"), "w") as zf:
        add_tree(zf, os.path.join(ROOT, "portable", "laws"), prefix="laws/")
    print("dist built:", ", ".join(sorted(os.listdir(DIST))))


if __name__ == "__main__":
    main()
