# AGENTS.md

دستور کار برای هر دستیار هوش مصنوعی که این مخزن را باز می‌کند (Codex، Cursor، GitHub Copilot، Gemini CLI، Qwen Code، Mistral Vibe، Kiro و ...).

## اگر کاربر پرسش حقوقی دارد

این مخزن «جعبه‌ابزار حقوقی ایران» است. برای پاسخ دادن:

1. اول `plugins/iran-legal-toolkit/skills/iran-legal-core/SKILL.md` را بخوان و از روش آن پیروی کن.
2. راهنمای موضوع را از `plugins/iran-legal-toolkit/skills/<نام>/SKILL.md` بردار: `iran-civil-litigation`، `iran-criminal-procedure`، `iran-contracts-deeds`، `iran-labor-law`، `iran-family-law`، `iran-property-lease`، `iran-official-letters`، `iran-law-texts`.
3. شمارهٔ ماده را از حافظه نگو. با اسکریپت بررسی کن:
   - `python3 plugins/iran-legal-toolkit/skills/iran-law-texts/scripts/find_article.py civil 10`
   - `python3 plugins/iran-legal-toolkit/skills/iran-law-texts/scripts/find_article.py labor --search "عبارت"`
   - `python3 plugins/iran-legal-toolkit/skills/iran-law-texts/scripts/find_ruling.py --number 873`
4. پاسخ را فارسی، ساده و گام‌به‌گام بنویس.

## If you are changing the repository

- Source of truth: `plugins/iran-legal-toolkit/skills/`. Everything in `portable/` and `dist/` is generated.
- After any change run `python3 tools/check.py` (rebuilds `portable/` and `dist/`) and `python3 tools/audit_citations.py`. Both must pass.
- Law texts come only from official sources (qavanin.ir, rc.majlis.ir, the judiciary's official sites). Do not import AI summaries or news articles as law text.
- Persian text: use ZWNJ (نیم‌فاصله), Persian ی and ک, and Persian punctuation.
- Versions must match in `.claude-plugin/plugin.json`, `plugin.json` and `mcp/server.py`.
- When something is added, update the README «🆕 تازه‌ها» section, `docs/index.md` and `CHANGELOG.md`.
- License: CC BY 4.0, attribution «yoyodolo — https://github.com/yoyodolo855/iran-legal-toolkit».
