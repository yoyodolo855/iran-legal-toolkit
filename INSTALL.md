<div dir="rtl">

# راهنمای نصب روی هر هوش مصنوعی

این جعبه‌ابزار به چهار شکل ساخته می‌شود. هر هوش مصنوعی یکی از این شکل‌ها را می‌پذیرد:

| شکل | فایل | برای |
|---|---|---|
| **اسکیل کامل** | [iran-legal-toolkit-skill.zip](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/iran-legal-toolkit-skill.zip) | Claude، Gemini، ChatGPT (طرح‌های کاری)، Grok، Perplexity، Mistral Vibe، Copilot |
| **اسکیل سبک** (زیر ۱۰۰ فایل) | [iran-legal-toolkit-skill-lite.zip](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/iran-legal-toolkit-skill-lite.zip) | جاهایی که بیشتر از ۱۰۰ فایل نمی‌پذیرند (مثل Gemini Enterprise) |
| **فایل قابل حمل** | [کامل](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/iran-legal-toolkit-portable.md) یا [سبک](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/iran-legal-toolkit-lite.md) | هر چتی که فایل می‌پذیرد: DeepSeek، Qwen Chat، Meta AI، Kimi، ChatGPT رایگان و ... |
| **سرور MCP** | [`plugins/iran-legal-toolkit/mcp/`](plugins/iran-legal-toolkit/mcp/README.md) | برنامه‌های رومیزی و مدل‌های محلی: Claude Desktop، Cursor، VS Code، LM Studio، Jan، Ollama |

اگر نمی‌دانید کدام را بردارید: اگر هوش مصنوعی شما بخشی به نام **Skills** دارد، اسکیل کامل؛ اگر ندارد، فایل قابل حمل.

> ⚠️ منوها و طرح‌های اشتراک هر شرکت مدام عوض می‌شود. نام دکمه‌ها ممکن است کمی فرق کند. این راهنما در آبان ۱۴۰۵ بررسی شده است.

---

## هوش مصنوعی‌هایی که «Skills» دارند

### Claude (claude.ai، برنامهٔ رومیزی و موبایل)

1. فایل `iran-legal-toolkit-skill.zip` را دانلود کنید. **باز نکنید.**
2. در Claude به Settings ← Customize ← Skills بروید و «+» یا Upload را بزنید.
3. فایل ZIP را انتخاب کنید و اسکیل را روشن کنید.
4. در یک گفت‌وگوی تازه مسئله‌تان را بنویسید. Claude خودش اسکیل را به کار می‌گیرد.

راه دیگر: فایل [iran-legal-toolkit.plugin](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/iran-legal-toolkit.plugin) را در گفت‌وگو بفرستید و دکمهٔ نصب را بزنید.

### Claude Code

<div dir="ltr">

```
/plugin marketplace add yoyodolo855/iran-legal-toolkit
/plugin install iran-legal-toolkit@iran-legal-free
```

</div>

### Gemini (gemini.google.com)

1. فایل ZIP کامل را دانلود و **باز (Extract)** کنید. یک پوشه به نام `iran-legal-toolkit` به دست می‌آید.
2. در Gemini وب به Settings ← Skills ← Upload بروید.
3. پوشهٔ `iran-legal-toolkit` را بارگذاری کنید. (بارگذاری فعلاً در نسخهٔ وب هست، نه در برنامهٔ موبایل.)

Gems از آبان ۱۴۰۵ برای حساب‌های شخصی کنار گذاشته می‌شود. اگر قبلاً Gem ساخته بودید، به‌جایش همین اسکیل را نصب کنید.

**Gemini Enterprise:** بخش Skills ← Upload skill، و فایل **iran-legal-toolkit-skill-lite.zip** را بدهید (سقف ۱۰۰ فایل).

### ChatGPT

- **طرح‌های Business، Enterprise و Edu:** نوار کناری ← Plugins ← زبانهٔ Skills ← Create ← Upload from your computer، و فایل ZIP کامل را بدهید. ممکن است مدیر فضای کاری باید بارگذاری اسکیل را فعال کرده باشد.
- **طرح‌های رایگان، Plus و Pro:** اسکیل ندارند. یک **Project** بسازید، بخش «دستور سیستمی» ابتدای فایل قابل حمل را در Instructions بگذارید و خود فایل را در Files بارگذاری کنید.

### Grok

در grok.com بخش Skills (اگر برای حساب شما فعال شده) را باز کنید و فایل ZIP کامل را بارگذاری کنید. اگر این بخش را نمی‌بینید، فایل قابل حمل را در گفت‌وگو پیوست کنید (روش «چت‌های بدون اسکیل» در پایین).

### Perplexity

در Perplexity Computer بخش Skills ← Upload، و فایل ZIP کامل. این بخش در طرح‌های پولی هست؛ در طرح رایگان از فایل قابل حمل استفاده کنید.

### Mistral Vibe (Le Chat سابق)

در chat.mistral.ai حالت **Work** را باز کنید، به بخش Skills بروید و فایل ZIP کامل را بارگذاری کنید. مدیر فضای کاری می‌تواند Skills را خاموش کرده باشد.

برای **Vibe CLI** (خط فرمان): پوشهٔ بازشدهٔ `iran-legal-toolkit` را در `~/.vibe/skills/` کپی کنید.

### Microsoft Copilot

- **Microsoft 365 Copilot (حساب کاری):** پوشهٔ بازشدهٔ `iran-legal-toolkit` را در OneDrive در مسیر `Documents/Cowork/skills/` بگذارید. نام پوشه باید دقیقاً `iran-legal-toolkit` بماند.
- **Copilot Studio:** در عامل خود Build ← Skills ← Upload a skill، و فایل ZIP کامل.
- **Copilot رایگان (copilot.microsoft.com):** اسکیل ندارد. فایل قابل حمل **سبک** را پیوست کنید.

### Qwen

- **Qwen Code (خط فرمان):** پوشهٔ `iran-legal-toolkit` را در `~/.qwen/skills/` کپی کنید.
- **QwenWork:** بخش Skills، و فایل ZIP کامل.
- **Qwen Chat / Qwen Studio (وب):** اسکیل ندارد. فایل قابل حمل را پیوست کنید.

### ابزارهای برنامه‌نویسی (Codex، Cursor، Gemini CLI، Kiro، GitHub Copilot در VS Code)

پوشهٔ بازشدهٔ `iran-legal-toolkit` را در پوشهٔ اسکیل همان ابزار بگذارید (مثلاً `~/.codex/skills/`، `~/.gemini/skills/` یا `.agents/skills/` در پروژه). اگر کل این مخزن را باز کنید، فایل `AGENTS.md` خودش راه را به ابزار نشان می‌دهد. برای دقت بیشتر سرور MCP را هم وصل کنید.

---

## چت‌های بدون اسکیل (DeepSeek، Meta AI، Kimi، Qwen Chat، Copilot رایگان، ChatGPT رایگان)

1. فایل قابل حمل را دانلود کنید:
   - [**سبک**](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/iran-legal-toolkit-lite.md) (حدود ۸۰ کیلوبایت): برای Meta AI، Copilot رایگان و هر چتی که فایل بزرگ نمی‌پذیرد.
   - [**کامل**](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/iran-legal-toolkit-portable.md) (حدود ۷۴۰ کیلوبایت): برای DeepSeek، Kimi، Qwen Chat و ChatGPT که فایل بزرگ را می‌خوانند.
2. در یک گفت‌وگوی تازه فایل را پیوست کنید و بنویسید: «طبق این فایل عمل کن.»
3. بعد مسئله‌تان را کامل بگویید.

این چت‌ها فایل را بین گفت‌وگوها نگه نمی‌دارند؛ هر بار گفت‌وگوی تازه باز کردید، فایل را دوباره پیوست کنید.

اگر متن دقیق یک قانون را لازم دارید، فایل همان قانون را هم از [پوشهٔ laws](portable/laws/) بردارید و پیوست کنید.

---

## مدل‌های محلی روی رایانهٔ خودتان (Ollama، LM Studio، Jan)

بهترین راه **سرور MCP** است: مدل فقط همان ماده‌ای را که لازم دارد می‌خواند و حافظهٔ کوچک مدل پر نمی‌شود. راهنمای کامل: [mcp/README.md](plugins/iran-legal-toolkit/mcp/README.md).

- **LM Studio:** زبانهٔ Program ← Install ← Edit mcp.json.
- **Jan:** Settings ← MCP Servers ← Add.
- **Ollama:** از برنامه‌ای استفاده کنید که روی Ollama کار می‌کند و MCP دارد (مثل Jan یا Open WebUI).

متن [`portable/system-prompt-mini.md`](portable/system-prompt-mini.md) را در System Prompt بگذارید. مدلی انتخاب کنید که tool calling دارد (مثل Qwen3 یا Llama 3.1 به بالا).

اگر برنامهٔ شما MCP ندارد، فایل قابل حمل **سبک** را در System Prompt یا Knowledge بگذارید. مدل باید دست‌کم ۶۴ هزار توکن حافظه (context) داشته باشد.

---

## Fostera

دربارهٔ «Fostera» منبع معتبری پیدا نکردیم. اگر نشانی سایت یا نام دقیقش را بفرستید، روش نصب را اضافه می‌کنیم. تا آن موقع: اگر بخش Skills دارد، اسکیل کامل؛ اگر ندارد، فایل قابل حمل.

---

## مشکل رایج

| مشکل | راه حل |
|---|---|
| «فایل SKILL.md پیدا نشد» | ZIP را دوباره دانلود کنید. در Claude و ChatGPT خود ZIP را بدهید، نه پوشهٔ باز شده را. در Gemini برعکس: پوشه را بدهید. |
| «بیشتر از ۱۰۰ فایل» | نسخهٔ `skill-lite.zip` را بدهید. |
| «فایل خیلی بزرگ است» | فایل قابل حمل **سبک** را بدهید. |
| هوش مصنوعی شمارهٔ ماده را اشتباه می‌گوید | از او بخواهید ماده را در فایل قانون پیدا کند؛ یا سرور MCP را وصل کنید. |

سازنده: yoyodolo — https://github.com/yoyodolo855/iran-legal-toolkit (رایگان، با مجوز CC BY 4.0)

</div>
