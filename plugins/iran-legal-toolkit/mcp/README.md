<div dir="rtl">

# سرور MCP جعبه‌ابزار حقوقی ایران

این سرور به هر برنامهٔ هوش مصنوعی که از MCP پشتیبانی می‌کند هفت ابزار می‌دهد. مدل با این ابزارها فقط همان ماده یا رأیی را که لازم دارد می‌خواند و لازم نیست همهٔ فایل‌ها را بارگذاری کند. نتیجه: پاسخ دقیق‌تر با توکن کمتر.

| ابزار | کار |
|---|---|
| `list_laws` | فهرست قوانینی که متن کاملشان در بسته هست |
| `get_articles` | متن یک یا چند ماده از یک قانون (`law`، `articles`) |
| `search_law` | جست‌وجوی عبارت در یک قانون یا همهٔ قوانین |
| `get_ruling` | متن رأی وحدت رویه با شماره |
| `search_rulings` | جست‌وجو در آرای وحدت رویه و نظریه‌های مشورتی |
| `list_guides` | فهرست راهنماها (کار، خانواده، ملک، کیفری و ...) |
| `read_guide` | خواندن یک راهنما |

## پیش‌نیاز

- پایتون ۳.۸ یا بالاتر. هیچ بستهٔ دیگری لازم نیست.
- یک نسخه از مخزن روی رایانه: `git clone https://github.com/yoyodolo855/iran-legal-toolkit` یا دانلود ZIP از گیت‌هاب.

در نمونه‌های زیر، `/PATH/TO` را با مسیر پوشهٔ دانلودشده عوض کنید. در ویندوز اگر `python3` کار نکرد، `python` یا `py` بنویسید و مسیر را این‌طور بنویسید: `C:/Users/you/iran-legal-toolkit/...`.

## Claude Desktop، Cursor، LM Studio، Windsurf، Cline

این برنامه‌ها همه همین قالب را می‌خوانند:

<div dir="ltr">

```json
{
  "mcpServers": {
    "iran-legal": {
      "command": "python3",
      "args": ["/PATH/TO/iran-legal-toolkit/plugins/iran-legal-toolkit/mcp/server.py"]
    }
  }
}
```

</div>

- **Claude Desktop:** منوی Settings ← Developer ← Edit Config، و افزودن بالا به `claude_desktop_config.json`.
- **Cursor:** فایل `~/.cursor/mcp.json`.
- **LM Studio (مدل محلی):** زبانهٔ Program در نوار کناری ← Install ← Edit mcp.json. فقط بخش داخل `mcpServers` را اضافه کنید.
- **Cline / Windsurf:** تنظیمات MCP همان برنامه.

## Jan (مدل محلی)

Settings ← MCP Servers ← «+ Add MCP Server». نوع را STDIO بگذارید، Command را `python3` و Argument را مسیر `server.py` بنویسید.

## VS Code (GitHub Copilot)

فایل `.vscode/mcp.json`:

<div dir="ltr">

```json
{
  "servers": {
    "iran-legal": {
      "type": "stdio",
      "command": "python3",
      "args": ["/PATH/TO/iran-legal-toolkit/plugins/iran-legal-toolkit/mcp/server.py"]
    }
  }
}
```

</div>

## Claude Code، Gemini CLI، Codex CLI، Qwen Code

<div dir="ltr">

```bash
claude mcp add iran-legal -- python3 /PATH/TO/iran-legal-toolkit/plugins/iran-legal-toolkit/mcp/server.py
gemini mcp add iran-legal python3 /PATH/TO/iran-legal-toolkit/plugins/iran-legal-toolkit/mcp/server.py
codex mcp add iran-legal -- python3 /PATH/TO/iran-legal-toolkit/plugins/iran-legal-toolkit/mcp/server.py
```

</div>

در Qwen Code همان قالب JSON بالا را در `~/.qwen/settings.json` زیر `mcpServers` بگذارید.

## نکته برای مدل‌های محلی (Ollama، LM Studio، Jan)

- مدلی انتخاب کنید که «tool calling» دارد، مثل Qwen3 یا Llama 3.1 به بالا. مدل‌های خیلی کوچک ابزار را درست صدا نمی‌زنند.
- متن `portable/system-prompt-mini.md` را در System Prompt بگذارید. کوتاه است و جای کمی از حافظهٔ مدل می‌گیرد.
- خود Ollama رابط چت ندارد؛ از برنامه‌ای استفاده کنید که روی Ollama کار می‌کند و MCP دارد (مثل Jan یا Open WebUI)، یا مدل را مستقیم در LM Studio اجرا کنید.

## آزمایش سریع

<div dir="ltr">

```bash
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18"}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_articles","arguments":{"law":"civil","articles":["10"]}}}' \
  | python3 plugins/iran-legal-toolkit/mcp/server.py
```

</div>

اگر متن مادهٔ ۱۰ قانون مدنی چاپ شد، سرور درست کار می‌کند.

## چرا در ChatGPT و Gemini وب نیست؟

این سرور روی رایانهٔ خود شما اجرا می‌شود (stdio). نسخهٔ وب ChatGPT، Gemini و بیشتر چت‌های وب فقط سرور MCP راه دور (روی اینترنت) را می‌پذیرند و این پروژه سرور ندارد. برای آن‌ها از بستهٔ اسکیل یا فایل قابل حمل استفاده کنید (راهنمای نصب: `INSTALL.md`).

</div>
