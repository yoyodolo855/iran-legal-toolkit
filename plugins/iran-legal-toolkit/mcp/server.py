#!/usr/bin/env python3
"""Iran Legal Toolkit MCP server (stdio, no dependencies).

Exposes the toolkit's law texts, rulings and guides as MCP tools so any MCP
client (Claude Desktop, Cursor, VS Code / Copilot, Gemini CLI, Codex, Windsurf,
Cline, LM Studio, ...) can look up exact articles instead of loading whole files.

Run:  python3 server.py        (Windows: py server.py)
Protocol: JSON-RPC 2.0, one JSON message per line on stdin/stdout.
"""
import contextlib
import importlib.util
import io
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # keep the skill folders clean

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.normpath(os.path.join(HERE, "..", "skills"))
SCRIPTS = os.path.join(SKILLS, "iran-law-texts", "scripts")
MAX_OUT = 20000
VERSION = "0.25.0"
PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SCRIPTS, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FA = _load("find_article")
FR = _load("find_ruling")


def _run(mod, argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            mod.main(argv)
        except SystemExit:
            pass
    text = (out.getvalue() + err.getvalue()).strip() or "نتیجه‌ای پیدا نشد."
    if len(text) > MAX_OUT:
        text = text[:MAX_OUT] + f"\n…[{len(text) - MAX_OUT} نویسهٔ دیگر بریده شد؛ جست‌وجو را دقیق‌تر کن]"
    return text


def _guides():
    items = []
    for root, _, files in os.walk(SKILLS):
        rel_root = os.path.relpath(root, SKILLS)
        if rel_root.startswith(os.path.join("iran-law-texts", "references")) or \
           rel_root.startswith(os.path.join("iran-law-texts", "rulings")) or \
           os.sep + "evals" in os.sep + rel_root:
            continue
        for f in sorted(files):
            if f.endswith(".md"):
                p = os.path.join(root, f)
                with open(p, encoding="utf-8") as fh:
                    first = ""
                    for line in fh:
                        s = line.strip()
                        if s.startswith("description:"):
                            first = s[12:].strip()[:160]
                            break
                        if s.startswith("# "):
                            first = s[2:].strip()
                            break
                items.append((os.path.relpath(p, SKILLS).replace(os.sep, "/"), first))
    return sorted(items)


def tool_list_laws(_):
    return _run(FA, ["--list"])


def tool_get_articles(a):
    arts = a.get("articles") or []
    if isinstance(arts, (str, int)):
        arts = [arts]
    return _run(FA, [str(a.get("law", ""))] + [str(x) for x in arts])


def tool_search_law(a):
    q = str(a.get("query", "")).strip()
    law = str(a.get("law", "") or "").strip()
    if not q:
        return "query لازم است."
    if law and law != "all":
        return _run(FA, [law, "--search", q])
    hits = []
    for key in FA.LAWS:
        r = _run(FA, [key, "--search", q])
        if r and "نتیجه‌ای پیدا نشد" not in r and not r.startswith("no match") and "[0 match" not in r:
            hits.append(f"### {key}\n{r}")
        if sum(len(h) for h in hits) > MAX_OUT:
            break
    text = "\n\n".join(hits) or "نتیجه‌ای پیدا نشد."
    return text[:MAX_OUT]


def tool_get_ruling(a):
    return _run(FR, ["--number", str(a.get("number", ""))])


def tool_search_rulings(a):
    words = str(a.get("query", "")).split()
    mx = int(a.get("max", 5) or 5)
    return _run(FR, ["--search"] + words + ["--max", str(max(1, min(mx, 20)))])


def tool_list_guides(_):
    return "\n".join(f"{p}\t{d}" for p, d in _guides())


def tool_read_guide(a):
    rel = str(a.get("path", "")).replace("\\", "/").lstrip("/")
    full = os.path.normpath(os.path.join(SKILLS, rel))
    if not full.startswith(SKILLS + os.sep) or not full.endswith(".md") or not os.path.isfile(full):
        return "مسیر نامعتبر است. از list_guides استفاده کن."
    with open(full, encoding="utf-8") as fh:
        text = fh.read()
    if len(text) > MAX_OUT * 2:
        text = text[:MAX_OUT * 2] + "\n…[بقیهٔ فایل بریده شد]"
    return text


TOOLS = [
    ("list_laws", "فهرست کلید و عنوان ۶۴ قانون و آیین‌نامهٔ ایران در این بسته. List law keys and titles.",
     {}, [], tool_list_laws),
    ("get_articles", "متن دقیق یک یا چند ماده از یک قانون. law = کلید قانون (مثل civil، cpc، labor، constitution)، articles = شماره‌ها (مثل [\"10\", \"190\"] یا [\"2 مکرر\"]). Exact article text.",
     {"law": {"type": "string"}, "articles": {"type": "array", "items": {"type": "string"}}}, ["law", "articles"], tool_get_articles),
    ("search_law", "جست‌وجوی عبارت در یک قانون (law) یا همهٔ قوانین (law را خالی بگذار). نسبت به فاصله و نیم‌فاصله حساس نیست. Phrase search in one or all laws.",
     {"query": {"type": "string"}, "law": {"type": "string"}}, ["query"], tool_search_law),
    ("get_ruling", "متن رأی وحدت رویهٔ دیوان عالی کشور یا نظریهٔ مشورتی با شماره (مثل 873 یا 7/1404/131). Unification ruling or advisory opinion by number.",
     {"number": {"type": "string"}}, ["number"], tool_get_ruling),
    ("search_rulings", "جست‌وجو در آرای وحدت رویه، نظریه‌های مشورتی و آرای دیوان عدالت اداری (همهٔ کلمه‌ها باید باشند). Search rulings.",
     {"query": {"type": "string"}, "max": {"type": "integer"}}, ["query"], tool_search_rulings),
    ("list_guides", "فهرست راهنماها و الگوها (دادخواست، شکواییه، قرارداد، مهلت‌ها، صلاحیت، هزینه‌ها). List practical guides and templates.",
     {}, [], tool_list_guides),
    ("read_guide", "خواندن یک راهنما با مسیر از list_guides (مثل iran-legal-core/SKILL.md). Read a guide by path.",
     {"path": {"type": "string"}}, ["path"], tool_read_guide),
]

INSTRUCTIONS = (
    "این سرور جعبه‌ابزار حقوقی رایگان ایران است برای کسی که وکیل ندارد. روش کار: "
    "۱) پیش از هر پاسخ حقوقی، read_guide('iran-legal-core/SKILL.md') را بخوان و از آن پیروی کن؛ "
    "بعد راهنمای موضوع را از list_guides بردار (خانواده، کار، ملک و اجاره، کیفری، دعاوی حقوقی، قرارداد، نامهٔ اداری). "
    "۲) شمارهٔ ماده یا رأی را هرگز از حافظه نگو؛ با get_articles و get_ruling بررسی کن. "
    "۳) مهلت‌ها، مرجع صالح و هزینه‌ها را از راهنماها بگیر و تاریخ به‌روز بودنشان را بگو. "
    "۴) پاسخ را فارسی، ساده و گام‌به‌گام بنویس و بگو کجا باید با وکیل یا مرجع رسمی مشورت شود. "
    "Free Iranian legal toolkit: read iran-legal-core/SKILL.md first, verify every article and ruling with the tools, answer in plain Persian."
)


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    params = msg.get("params") or {}
    if mid is None:
        return None  # notification
    if method == "initialize":
        want = params.get("protocolVersion")
        proto = want if want in PROTOCOLS else PROTOCOLS[0]
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": proto,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "iran-legal-toolkit", "version": VERSION},
            "instructions": INSTRUCTIONS}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        tools = [{"name": n, "description": d,
                  "inputSchema": {"type": "object", "properties": props, "required": req}}
                 for n, d, props, req, _ in TOOLS]
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools}}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        for n, _, _, _, fn in TOOLS:
            if n == name:
                try:
                    text = fn(args)
                    return {"jsonrpc": "2.0", "id": mid, "result": {
                        "content": [{"type": "text", "text": text}], "isError": False}}
                except Exception as e:  # report, never crash the server
                    return {"jsonrpc": "2.0", "id": mid, "result": {
                        "content": [{"type": "text", "text": f"خطا: {e}"}], "isError": True}}
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"unknown tool {name}"}}
    if method in ("resources/list", "prompts/list"):
        key = "resources" if method == "resources/list" else "prompts"
        return {"jsonrpc": "2.0", "id": mid, "result": {key: []}}
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}


def main():
    stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
        else:
            msgs = msg if isinstance(msg, list) else [msg]
            out = [r for r in (handle(m) for m in msgs) if r is not None]
            resp = (out if isinstance(msg, list) else (out[0] if out else None))
        if resp is not None:
            stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            stdout.flush()


if __name__ == "__main__":
    main()
