# 👤 **دليل المستخدم الشامل - SBARDS v2.0.0**
## دليل كامل لاستخدام نظام تحليل السلوك الأمني المتقدم

---

## 📋 **فهرس المحتويات**

1. [🎯 مقدمة للمستخدمين](#introduction)
2. [⚡ التثبيت والإعداد](#installation)
3. [🚀 البدء السريع](#quick-start)
4. [🎨 استخدام واجهة المستخدم](#user-interface)
5. [🔧 التكوين الأساسي](#configuration)
6. [📊 مراقبة النظام](#monitoring)
7. [🔒 الأمان والخصوصية](#security)
8. [🛠️ حل المشاكل الشائعة](#troubleshooting)
9. [❓ الأسئلة الشائعة](#faq)

---

## 🎯 **مقدمة للمستخدمين** {#introduction}

### **ما هو SBARDS؟**
SBARDS هو نظام أمان متقدم يحمي جهازك من التهديدات الأمنية عبر:

- **🛡️ الحماية الفورية**: اعتراض الملفات قبل وصولها لجهازك
- **🔍 التحليل الذكي**: فحص شامل باستخدام 8 محللات متخصصة
- **⚡ الاستجابة السريعة**: إجراءات تلقائية لحماية النظام
- **📊 المراقبة المستمرة**: تتبع حالة الأمان في الوقت الفعلي

### **لماذا تحتاج SBARDS؟**
- **حماية من برامج الفدية** والتهديدات المتقدمة
- **كشف التهديدات الجديدة** (Zero-day attacks)
- **حماية البيانات الحساسة** والملفات المهمة
- **مراقبة شاملة** لنشاط النظام
- **سهولة الاستخدام** مع حماية متقدمة

---

## ⚡ **التثبيت والإعداد** {#installation}

### **المتطلبات الأساسية:**

#### **متطلبات النظام:**
- **نظام التشغيل**: Windows 10+ أو Linux Ubuntu 18.04+
- **المعالج**: Intel i5 أو AMD Ryzen 5 (أو أفضل)
- **الذاكرة**: 4GB RAM (8GB مستحسن)
- **التخزين**: 2GB مساحة فارغة
- **الشبكة**: اتصال إنترنت للتحديثات

#### **البرامج المطلوبة:**
- **Python 3.8+** - [تحميل من هنا](https://python.org)
- **Git** - [تحميل من هنا](https://git-scm.com)
- **C++ Compiler** (يتم تثبيته تلقائياً)

### **خطوات التثبيت:**

#### **الطريقة الأولى: التثبيت التلقائي (مستحسن)**
```bash
# 1. تحميل سكريبت التثبيت
curl -sSL https://install.sbards.org | bash

# 2. تشغيل النظام
sbards start
```

#### **الطريقة الثانية: التثبيت اليدوي**
```bash
# 1. استنساخ المشروع
git clone https://github.com/sbards/sbards-v2.git
cd sbards-v2

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. تهيئة النظام
python run.py --setup

# 4. تشغيل النظام
python run.py
```

### **التحقق من التثبيت:**
```bash
# فحص حالة النظام
python run.py --check-system

# اختبار سريع
python run.py --test

# عرض معلومات الإصدار
python run.py --version
```

---

## 🚀 **البدء السريع** {#quick-start}

### **التشغيل الأول:**

#### **1. تشغيل النظام الكامل:**
```bash
# تشغيل جميع الطبقات (الطريقة المستحسنة)
python run.py

# أو باستخدام الأمر المختصر
sbards start
```

#### **2. الوصول لواجهة المستخدم:**
```bash
# فتح المتصفح تلقائياً
python run.py --open-browser

# أو الوصول يدوياً
http://localhost:8000/dashboard
```

#### **3. التحقق من عمل النظام:**
- ✅ **طبقة الاعتراض**: يجب أن تظهر "نشطة"
- ✅ **قاعدة البيانات**: يجب أن تظهر "متصلة"
- ✅ **المحللات**: يجب أن تظهر "جاهزة"
- ✅ **واجهة API**: يجب أن تظهر "متاحة"

### **اختبار النظام:**

#### **اختبار ملف آمن:**
```bash
# إنشاء ملف اختبار آمن
echo "This is a safe test file" > test_safe.txt

# نقل الملف لمجلد المراقبة
mv test_safe.txt ~/Downloads/

# مراقبة النتيجة في Dashboard
```

#### **مراقبة النتائج:**
1. افتح Dashboard: `http://localhost:8000/dashboard`
2. راقب قسم "الملفات المعالجة"
3. تحقق من ظهور الملف كـ "آمن"
4. راجع تفاصيل التحليل

---

## 🎨 **استخدام واجهة المستخدم** {#user-interface}

### **🌐 Dashboard الرئيسي:**

#### **الأقسام الرئيسية:**
1. **📊 نظرة عامة**: إحصائيات سريعة عن النظام
2. **🛡️ حالة الحماية**: مستوى الأمان الحالي
3. **📈 الملفات المعالجة**: قائمة الملفات المفحوصة
4. **🚨 التنبيهات**: التهديدات المكتشفة
5. **⚙️ إعدادات النظام**: تكوين الخيارات

#### **استخدام الميزات:**

##### **1. مراقبة النشاط المباشر:**
- **الملفات الجديدة**: تظهر فور اعتراضها
- **حالة التحليل**: تحديث مباشر لحالة الفحص
- **النتائج**: عرض فوري للنتائج

##### **2. إدارة التنبيهات:**
- **التنبيهات الحرجة**: تظهر بلون أحمر
- **التنبيهات المتوسطة**: تظهر بلون برتقالي
- **المعلومات**: تظهر بلون أزرق

##### **3. تخصيص العرض:**
- **الوضع المظلم/الفاتح**: تبديل حسب التفضيل
- **تحديث البيانات**: كل ثانيتين تلقائياً
- **الفلترة**: حسب نوع الملف أو التاريخ

### **📱 واجهة الهاتف المحمول:**
- **تصميم متجاوب**: يعمل على جميع الأجهزة
- **تنبيهات فورية**: إشعارات للتهديدات
- **تحكم عن بُعد**: إيقاف/تشغيل النظام

---

## 🔧 **التكوين الأساسي** {#configuration}

### **ملف التكوين الرئيسي:**

#### **موقع الملف:**
```
config.json - في مجلد المشروع الرئيسي
```

#### **الإعدادات الأساسية:**
```json
{
    "capture": {
        "enabled": true,
        "monitored_folders": [
            "~/Downloads",
            "~/Desktop", 
            "~/Documents",
            "/tmp",
            "/var/tmp",
            "C:\\Users\\%USERNAME%\\Downloads"
        ],
        "file_size_limit_mb": 100,
        "excluded_extensions": [".log", ".tmp"]
    },
    "analysis": {
        "static_analysis_enabled": true,
        "dynamic_analysis_enabled": false,
        "ml_analysis_enabled": true,
        "virustotal_enabled": false
    },
    "security": {
        "quarantine_enabled": true,
        "auto_delete_malicious": false,
        "backup_before_quarantine": true
    }
}
```

### **تخصيص المراقبة:**

#### **إضافة مجلدات للمراقبة:**
```bash
# عبر سطر الأوامر
python run.py --add-folder "/path/to/monitor"

# عبر ملف التكوين
# أضف المسار لقائمة monitored_folders
```

#### **استثناء ملفات معينة:**
```json
{
    "capture": {
        "excluded_extensions": [".log", ".tmp", ".cache"],
        "excluded_patterns": ["*backup*", "*temp*"],
        "excluded_folders": ["/var/log", "C:\\Windows\\Temp"]
    }
}
```

### **إعدادات الأمان:**

#### **مستويات الحماية:**
```json
{
    "security": {
        "protection_level": "high",  // low, medium, high, maximum
        "quarantine_enabled": true,
        "real_time_scanning": true,
        "cloud_analysis": false
    }
}
```

#### **إعدادات التنبيهات:**
```json
{
    "alerts": {
        "email_notifications": true,
        "email_address": "user@example.com",
        "desktop_notifications": true,
        "sound_alerts": true,
        "log_level": "INFO"
    }
}
```

---

## 📊 **مراقبة النظام** {#monitoring}

### **مؤشرات الأداء الرئيسية:**

#### **1. حالة النظام:**
- **🟢 نشط**: النظام يعمل بشكل طبيعي
- **🟡 تحذير**: مشكلة بسيطة تحتاج انتباه
- **🔴 خطأ**: مشكلة حرجة تحتاج تدخل فوري

#### **2. إحصائيات المعالجة:**
```
📊 إحصائيات اليوم:
├── الملفات المفحوصة: 1,247
├── الملفات الآمنة: 1,198 (96.1%)
├── الملفات المشبوهة: 42 (3.4%)
├── الملفات الضارة: 7 (0.5%)
└── متوسط وقت المعالجة: 85ms
```

#### **3. استهلاك الموارد:**
- **استهلاك المعالج**: <10%
- **استهلاك الذاكرة**: <500MB
- **استهلاك القرص**: <2GB
- **استهلاك الشبكة**: <1MB/ساعة

### **تقارير مفصلة:**

#### **تقرير يومي:**
```bash
# إنشاء تقرير يومي
python run.py --daily-report

# إرسال التقرير بالبريد
python run.py --email-report daily
```

#### **تقرير أسبوعي:**
```bash
# تقرير أسبوعي مفصل
python run.py --weekly-report

# تصدير لملف PDF
python run.py --export-report weekly --format pdf
```

### **المراقبة المتقدمة:**

#### **سجلات النظام:**
```bash
# عرض السجلات المباشرة
tail -f logs/sbards_main.log

# البحث في السجلات
grep "MALICIOUS" logs/sbards_main.log

# تحليل السجلات
python run.py --analyze-logs --days 7
```

#### **تنبيهات مخصصة:**
```json
{
    "custom_alerts": {
        "high_cpu_usage": {
            "threshold": 80,
            "action": "email_admin"
        },
        "multiple_threats": {
            "threshold": 5,
            "timeframe": "1hour",
            "action": "shutdown_system"
        }
    }
}
```

---

## 🔒 **الأمان والخصوصية** {#security}

### **حماية البيانات:**

#### **التشفير:**
- **البيانات الحساسة**: مشفرة بـ AES-256
- **الاتصالات**: HTTPS/TLS 1.3
- **قاعدة البيانات**: تشفير على مستوى الحقول
- **الملفات المؤقتة**: حذف آمن تلقائي

#### **الخصوصية:**
- **عدم جمع بيانات شخصية** بدون إذن
- **التحليل المحلي**: لا يتم إرسال ملفات للخارج
- **سجلات مجهولة**: لا تحتوي على معلومات شخصية
- **تحكم كامل**: يمكن إيقاف أي ميزة

### **إعدادات الأمان المتقدمة:**

#### **المصادقة:**
```json
{
    "authentication": {
        "enabled": true,
        "method": "password",  // password, 2fa, certificate
        "session_timeout": 3600,
        "max_failed_attempts": 3
    }
}
```

#### **التحكم في الوصول:**
```json
{
    "access_control": {
        "admin_only_settings": true,
        "user_can_disable": false,
        "require_admin_for_quarantine": true
    }
}
```

### **النسخ الاحتياطي:**

#### **النسخ التلقائي:**
```bash
# تفعيل النسخ الاحتياطي التلقائي
python run.py --enable-backup --interval daily

# استعادة من نسخة احتياطية
python run.py --restore-backup backup_20241220.tar.gz
```

#### **إعدادات النسخ:**
```json
{
    "backup": {
        "enabled": true,
        "schedule": "daily",
        "location": "./backups/",
        "retention_days": 30,
        "compress": true,
        "encrypt": true
    }
}
```

---

## 🛠️ **حل المشاكل الشائعة** {#troubleshooting}

### **مشاكل التشغيل:**

#### **1. النظام لا يبدأ:**
```bash
# فحص السجلات
cat logs/sbards_main.log | tail -50

# فحص التكوين
python run.py --validate-config

# إعادة تهيئة
python run.py --reset-config
```

#### **2. استهلاك عالي للموارد:**
```bash
# فحص استهلاك الموارد
python run.py --resource-monitor

# تحسين الأداء
python run.py --optimize-performance

# تقليل المراقبة
python run.py --reduce-monitoring
```

#### **3. مشاكل قاعدة البيانات:**
```bash
# فحص سلامة قاعدة البيانات
python run.py --check-database

# إصلاح قاعدة البيانات
python run.py --repair-database

# إعادة إنشاء قاعدة البيانات
python run.py --recreate-database
```

### **مشاكل الكشف:**

#### **إنذارات كاذبة كثيرة:**
```json
{
    "analysis": {
        "sensitivity": "medium",  // high -> medium
        "whitelist_enabled": true,
        "learning_mode": true
    }
}
```

#### **عدم كشف تهديدات:**
```json
{
    "analysis": {
        "sensitivity": "high",
        "all_analyzers_enabled": true,
        "cloud_analysis": true
    }
}
```

### **أدوات التشخيص:**

#### **تشخيص شامل:**
```bash
# تشغيل تشخيص كامل
python run.py --full-diagnosis

# إنشاء تقرير مشكلة
python run.py --create-issue-report

# اختبار جميع المكونات
python run.py --test-all-components
```

---

## ❓ **الأسئلة الشائعة** {#faq}

### **أسئلة عامة:**

**س: هل SBARDS مجاني؟**
ج: نعم، SBARDS مفتوح المصدر ومجاني للاستخدام الشخصي والتجاري.

**س: هل يؤثر على أداء النظام؟**
ج: لا، SBARDS مصمم ليكون خفيف الوزن ويستهلك أقل من 10% من موارد النظام.

**س: هل يحتاج اتصال إنترنت؟**
ج: لا للعمل الأساسي، نعم للتحديثات والتحليل السحابي الاختياري.

### **أسئلة تقنية:**

**س: ما هي أنواع الملفات المدعومة؟**
ج: جميع أنواع الملفات، مع تركيز خاص على الملفات التنفيذية والمستندات.

**س: كيف يتم التعامل مع الملفات الكبيرة؟**
ج: الملفات أكبر من 100MB يتم تحليلها بطريقة خاصة لتجنب استهلاك الذاكرة.

**س: هل يمكن تخصيص قواعد الكشف؟**
ج: نعم، يمكن إضافة قواعد YARA مخصصة وتعديل حساسية المحللات.

### **الدعم والمساعدة:**

**📧 البريد الإلكتروني**: support@sbards.org
**💬 المجتمع**: [Discord Server](https://discord.gg/sbards)
**📖 الوثائق**: [GitHub Wiki](https://github.com/sbards/sbards/wiki)
**🐛 الأخطاء**: [GitHub Issues](https://github.com/sbards/sbards/issues)

---

<div align="center">

**👤 دليل المستخدم الشامل - SBARDS v2.0.0**

*حماية متقدمة مع سهولة الاستخدام*

**🛡️ نظام أمان ذكي لحماية عالمك الرقمي 🛡️**

</div>
