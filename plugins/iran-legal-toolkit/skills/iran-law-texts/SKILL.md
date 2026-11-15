---
name: iran-law-texts
description: متن کامل ۶۴ قانون و آیین‌نامهٔ ایران به تفکیک ماده (مدنی، آیین دادرسی مدنی و کیفری، مجازات اسلامی و تعزیرات، خانواده، کار، چک، اجاره، ثبت، تجارت، مالیات، قانون اساسی و…) و بانک آرای وحدت رویه و نظریه‌های مشورتی. هر وقت باید متن دقیق یک ماده را بیاوری، شمارهٔ ماده یا رأی را بررسی کنی، یا در قوانین ایران عبارتی را جست‌وجو کنی، از این اسکیل استفاده کن. Full text of Iranian statutes, unification rulings and advisory opinions for exact quotation and citation checks.
---
# متن قوانین

متن کامل ۶۴ قانون و آیین‌نامه به تفکیک ماده، و بانک آرای وحدت رویه و نظریه‌های مشورتی. برای نقل دقیق یا بررسی شمارهٔ ماده به کار می‌رود. اسکیل‌های دیگر این بسته خلاصه و الگو دارند و برای متن دقیق به این‌جا ارجاع می‌دهند.

## فایل‌ها را کامل نخوان

فایل‌ها بزرگ‌اند. فقط مادهٔ لازم را بیرون بکش:

- یک یا چند ماده: `python3 scripts/find_article.py cpc 49 50` (مادهٔ مکرر: `find_article.py smuggling "2 مکرر"`؛ اصل قانون اساسی: `find_article.py constitution 35`)
- جست‌وجوی عبارت: `python3 scripts/find_article.py tazirat --search "خیانت در امانت"`
- فهرست کلیدها با عنوان قانون: `python3 scripts/find_article.py --list`
- رأی وحدت رویه یا نظریهٔ مشورتی: `python3 scripts/find_ruling.py --number 873` یا `--search "مهریه"`
- اگر نمی‌توانی دستور اجرا کنی: در فایل دنبال سرتیتر `## مادهٔ ۴۹` (رقم فارسی) بگرد و فقط همان بخش را بخوان. جدول کامل فایل‌ها: `references/INDEX.md`.

## کلیدهای پرکاربرد

- **مدنی و دادرسی:** `civil` (قانون مدنی)، `civil-procedure` (آیین دادرسی مدنی)، `civil-enforcement` (اجرای احکام مدنی)، `financial-judgments` (محکومیت‌های مالی، اعسار)، `councils` و `councils-full` (شورای حل اختلاف و دادگاه صلح)، `civil-liability` (مسئولیت مدنی)، `non-contentious` (امور حسبی، ترکه، حصر وراثت)، `e-notification` (ابلاغ ثنا)
- **کیفری:** `ipc` (مجازات اسلامی)، `tazirat` (تعزیرات)، `cpc` (آیین دادرسی کیفری)، `reduction-1399` (کاهش حبس)، `cheque` (چک)، `computer-crimes`، `fraud-1367`، `narcotics`، `smuggling`، `arms`، `armed-forces`
- **خانواده:** `family` (حمایت خانواده)، `youth-population` (جوانی جمعیت، مرخصی زایمان)
- **ملک و اجاره:** `lease-1376`، `lease-1362`، `lease-1356` (تجاری)، `registration` و `registration-text` (قانون ثبت)، `registration-mandate` (الزام به ثبت رسمی ۱۴۰۳)، `pre-sale`، `apartment` و `apartment-reg`، `partition` (افراز)، `municipality` (کمیسیون مادهٔ ۱۰۰)، `farmland-use-1374`، `housing-1403`
- **کار و بیمه:** `labor`، `labor-procedure`، `social-security`، `unemployment-insurance`، `third-party-insurance`
- **مالیات و تجارت:** `direct-taxes`، `vat`، `sodagari-1404`، `pos-terminals`، `commercial-code`، `joint-stock-1347`، `guild`، `cooperative`، `consumer`، `government-revenues`
- **اداری و سایر:** `constitution`، `administrative-court`، `medical-council` و `medical-disciplinary`، `engineering`، `e-services-offices`
- **آیین‌نامه‌ها و متن‌های تکمیلی:** `lease-1376-reg`، `registration-reg`، `deeds-regulation` (اجرای اسناد رسمی)، `pre-sale-reg`، `land-reform-reg`، `pazireh` (اوقاف)، `transfer-anothers-property` (انتقال مال غیر)، `guild-amendment`

## قواعد استفاده

1. **مجازات‌ها:** متن قانون مجازات و تعزیرات پیش از قانون کاهش حبس ۱۳۹۹ است. برای میزان روز مجازات یک جرم تعزیری اول `reduction-1399` را جست‌وجو کن (مثلاً `--search "۶۷۴"`).
2. **تاریخ متن:** سرآیند فایل (که اسکریپت خودکار چاپ می‌کند) می‌گوید متن تا کی به‌روز است و چه هشداری دارد. اگر ماده‌ای در `iran-legal-core/references/volatile-and-sources.md` آمده (مثلاً مادهٔ ۱۰۴ قانون مجازات)، متن اصلاحی آن‌جا مقدم است و باید به کاربر بگویی متن این‌جا پیش از اصلاح است.
3. **نقل مستقیم:** متن را داخل «» بگذار و بنویس «طبق متن مصوب [سال]». متن‌هایی که هشدار «دربارهٔ دقت متن» دارند از PDF استخراج شده‌اند؛ برای نقل عین عبارت در دادخواست، تطبیق با qavanin.ir را توصیه کن.
4. **شمارهٔ ماده:** اگر شماره‌ای که اسکیل دیگری داده این‌جا با موضوع نمی‌خواند، به متن این‌جا اعتماد کن و ناسازگاری را بگو.
5. **آرای قدیمی:** آرای وحدت رویهٔ ۱۳۲۳ تا ۱۳۸۹ با OCR خوانده شده‌اند؛ مضمون قابل اتکاست ولی رقم‌های داخل متن را پیش از نقل تطبیق بده.
6. قانونی که کلید ندارد (مثل قانون رسیدگی به تخلفات اداری) متن کامل ندارد؛ از خلاصهٔ اسکیل‌های دیگر استفاده کن و بگو باید با متن رسمی تطبیق شود.
