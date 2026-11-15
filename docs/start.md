---
layout: default
title: شروع
---

# راهنمای قدم‌به‌قدم

## ۱. فایل‌ها را بگیرید

روی نام فایل بزنید تا دانلود شود:

| فایل | برای چه؟ |
|------|----------|
| [iran-legal-toolkit-portable.md](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/iran-legal-toolkit-portable.md) | فایل اصلی برای ChatGPT، Gemini، Grok و هر هوش مصنوعی دیگر |
| [laws.zip](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/laws.zip) | متن کامل چند قانون (اختیاری، برای نقل دقیق ماده) |
| [iran-legal-toolkit.plugin](https://github.com/yoyodolo855/iran-legal-toolkit/raw/main/dist/iran-legal-toolkit.plugin) | فقط برای Claude |

## ۲. به هوش مصنوعی‌تان بدهید

### در ChatGPT

<ol class="steps">
<li>در ChatGPT بخش <b>GPTs</b> را باز کنید و <b>Create</b> را بزنید (یا یک <b>Project</b> بسازید).</li>
<li>فایل <code>iran-legal-toolkit-portable.md</code> را با یک ویرایشگر متن باز کنید. بخش «دستور سیستمی» در ابتدای فایل را کپی کنید و در کادر <b>Instructions</b> بگذارید.</li>
<li>در بخش <b>Knowledge</b> خود فایل را بارگذاری کنید. اگر <code>laws.zip</code> را گرفتید، فایل‌های داخلش را هم اضافه کنید.</li>
<li>ذخیره کنید. از این به بعد هر پرسش حقوقی را در همین GPT بپرسید.</li>
</ol>

### در Gemini

<ol class="steps">
<li>در Gemini بخش <b>Gems</b> را باز کنید و یک Gem تازه بسازید.</li>
<li>بخش «دستور سیستمی» را در <b>Instructions</b> بگذارید.</li>
<li>فایل را در بخش <b>Knowledge</b> اضافه کنید و ذخیره کنید.</li>
</ol>

### در Grok و هوش مصنوعی‌های دیگر

فایل را در ابتدای گفت‌وگو پیوست کنید و بنویسید: «طبق این فایل عمل کن.» اگر مدل فایل بزرگ نمی‌پذیرد، فقط بخش‌های «هسته» و حوزهٔ مورد نیازتان را کپی کنید؛ هر بخش با `# FILE:` شروع می‌شود.

### در Claude

فایل `iran-legal-toolkit.plugin` را در گفت‌وگو باز کنید و دکمهٔ افزودن را بزنید. اگر Claude Code دارید:

```
/plugin marketplace add yoyodolo855/iran-legal-toolkit
/plugin install iran-legal-toolkit@iran-legal-free
```

## ۳. درست بپرسید

- **ماجرا را کامل بگویید:** چه شد، کی شد (تاریخ دقیق)، چقدر پول، چه مدرکی دارید، کدام شهر.
- **بگویید چه می‌خواهید:** «دادخواست بنویس»، «شکواییه بنویس»، «قرارداد را بررسی کن».
- **اطلاعات شخصی واقعی را لازم نیست بدهید.** هوش مصنوعی جای نام و کد ملی را با [ ] خالی می‌گذارد؛ خودتان بعداً پر کنید.

[نمونه درخواست‌های خوب را ببینید](examples.html).

## ۴. پیش از ثبت، بخوانید

متن آماده را یک بار با دقت بخوانید. هر جا شمارهٔ ماده یا مبلغی آمده و هوش مصنوعی گفته «تطبیق بده»، آن را با متن رسمی یا در دفتر خدمات قضایی چک کنید.
