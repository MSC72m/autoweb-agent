# ابزار خودکارسازی بانک پاسارگاد 🏦

ابزار خودکارسازی وب برای سرویس‌های بانک پاسارگاد با رابط کاربری فارسی و استفاده از Playwright.

## ویژگی‌ها ✨

- 🔄 تبدیل شماره کارت به شبا
- 🔄 تبدیل شماره سپرده به شبا  
- 🔄 تبدیل شماره شبا به سپرده
- 🌐 رابط کاربری فارسی با Streamlit
- 🤖 خودکارسازی کامل با Playwright
- 🔧 نصب خودکار مرورگر Chromium

## نصب و راه‌اندازی 🚀

### ویندوز (Windows) - نصب خودکار 🪟
```batch
# دابل کلیک روی فایل setup.bat
setup.bat

# اجرای برنامه
start.bat
```

### گزینه 1: نصب خودکار (توصیه شده)
```bash
# فعال‌سازی محیط مجازی (اگر دارید)
source venv/bin/activate

# اجرای اسکریپت نصب
python setup.py

# اجرای برنامه
streamlit run main.py
```

### گزینه 2: نصب دستی
```bash
# نصب کتابخانه‌ها
pip install -r requirements.txt

# نصب مرورگر Playwright
python -m playwright install chromium

# نصب وابستگی‌های سیستم (لینوکس/WSL)
python -m playwright install-deps

# اجرای برنامه
streamlit run main.py
```

### برای WSL (Windows Subsystem for Linux)
```bash
# فعال‌سازی محیط مجازی
source venv/bin/activate

# نصب خودکار
python setup.py

# اجرای برنامه
streamlit run main.py
```

## استفاده 📋

### ویندوز:
1. دابل کلیک روی `start.bat`
2. مرورگر باز می‌شود و رابط کاربری نمایش داده می‌شود

### لینوکس/WSL:
1. برنامه را اجرا کنید: `streamlit run main.py`
2. مرورگر باز می‌شود و رابط کاربری نمایش داده می‌شود

### مراحل استفاده:
3. سرویس مورد نظر را انتخاب کنید
4. شماره مربوطه را وارد کنید
5. دکمه "اجرای عملیات" را بزنید
6. منتظر نتیجه بمانید

## ساختار فایل‌ها 📁

```
autoweb-agent/
├── main.py              # فایل اصلی برنامه
├── requirements.txt     # وابستگی‌های Python
├── setup.py            # اسکریپت نصب خودکار (Linux/WSL)
├── setup.bat           # نصب خودکار برای ویندوز
├── start.bat           # اجرای برنامه در ویندوز
├── cleanup.bat         # پاک‌سازی محیط ویندوز
├── automate.html       # فایل HTML نمونه
└── README.md           # راهنمای استفاده
```

## عیب‌یابی 🔧

### ویندوز:
```batch
# پاک‌سازی و نصب مجدد
cleanup.bat
setup.bat
```

### مشکل: مرورگر یافت نشد
```bash
# نصب مجدد مرورگر Playwright
python -m playwright install chromium
```

### مشکل: خطا در اجرای عملیات
```bash
# نصب وابستگی‌های سیستم
python -m playwright install-deps
```

### مشکل: خطا در WSL
```bash
# اطمینان از فعال بودن محیط مجازی
source venv/bin/activate

# اجرای نصب کامل
python setup.py
```

## مزایای Playwright نسبت به Selenium 🎯

- ✅ نصب خودکار مرورگر
- ✅ سرعت بالاتر
- ✅ پایداری بیشتر
- ✅ عدم نیاز به ChromeDriver
- ✅ پشتیبانی بهتر از WSL

## نکات مهم ⚠️

- مطمئن شوید اتصال اینترنت برقرار است
- شماره‌ها را بدون فاصله وارد کنید
- برای شماره شبا، "IR" را وارد نکنید
- در صورت خطا، مجدداً تلاش کنید

## پشتیبانی 💬

در صورت بروز مشکل:

### ویندوز:
1. ابتدا `cleanup.bat` را اجرا کنید
2. سپس `setup.bat` را اجرا کنید
3. نسخه Python 3.7+ استفاده کنید
4. سپس start.bat را اجرا کنید.

---

**نوشته شده با ❤️ برای خودکارسازی بانکی** 