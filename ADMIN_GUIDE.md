# 👨‍💼 **دليل المدير الشامل - SBARDS v2.0.0**
## دليل إدارة وصيانة نظام تحليل السلوك الأمني المتقدم

---

## 📋 **فهرس المحتويات**

1. [🎯 نظرة عامة للإدارة](#admin-overview)
2. [🗄️ إدارة قاعدة البيانات](#database-management)
3. [⚙️ تكوين النظام المتقدم](#system-configuration)
4. [📊 المراقبة والأداء](#monitoring-performance)
5. [🔒 الأمان والنسخ الاحتياطي](#security-backup)
6. [👥 إدارة المستخدمين](#user-management)
7. [🛠️ الصيانة والاستكشاف](#maintenance-troubleshooting)
8. [📈 التحسين والتوسع](#optimization-scaling)

---

## 🎯 **نظرة عامة للإدارة** {#admin-overview}

### **مسؤوليات المدير:**
- **🗄️ إدارة قاعدة البيانات** والنسخ الاحتياطي
- **⚙️ تكوين النظام** والطبقات الأمنية
- **📊 مراقبة الأداء** وصحة النظام
- **👥 إدارة المستخدمين** والصلاحيات
- **🔒 الأمان والامتثال** للمعايير
- **🛠️ الصيانة الدورية** وحل المشاكل

### **أدوات الإدارة الرئيسية:**

#### **سطر الأوامر:**
```bash
# أدوات الإدارة الأساسية
python run.py --admin-mode                    # وضع الإدارة
python start_sbards_admin.py                  # لوحة إدارة SBARDS
python start_database_admin.py                # إدارة قاعدة البيانات
```

#### **واجهة الويب:**
```bash
# الوصول للوحة الإدارة
http://localhost:8000/admin                   # لوحة إدارة شاملة
http://localhost:8080/pgadmin                 # إدارة PostgreSQL
http://localhost:8000/dashboard/admin         # إحصائيات متقدمة
```

---

## 🗄️ **إدارة قاعدة البيانات** {#database-management}

### **هيكل قاعدة البيانات:**

#### **الجداول الأساسية (16 جدول):**
```sql
-- الجداول الرئيسية
Files                    -- معلومات الملفات الأساسية
Hashes                   -- هاشات متعددة الخوارزميات  
StaticReports           -- تقارير التحليل الثابت
DynamicReports          -- تقارير التحليل الديناميكي
Verdicts                -- القرارات النهائية

-- إدارة المستخدمين والأمان
Users                   -- بيانات المستخدمين
AccessControl           -- التحكم في الوصول
AuditLogs              -- سجلات المراجعة

-- التحليل المتقدم
PermissionAnalysis      -- تحليل الصلاحيات
EnhancedScanReport     -- تقارير الفحص المحسنة
VirusHashDatabase      -- قاعدة هاشات الفيروسات
WhitelistDatabase      -- قاعدة القوائم البيضاء

-- الاستخبارات والمقاييس
ThreatIntelligence     -- استخبارات التهديدات
SystemMetrics          -- مقاييس النظام
PerformanceMetrics     -- مقاييس الأداء
ConfigurationHistory   -- تاريخ التكوين
```

### **إدارة قاعدة البيانات:**

#### **العمليات الأساسية:**
```bash
# فحص حالة قاعدة البيانات
python run.py --check-database

# إنشاء نسخة احتياطية
python run.py --backup-database --output ./backups/

# استعادة من نسخة احتياطية
python run.py --restore-database --backup ./backups/backup_20241220.sql

# تحسين الأداء
python run.py --optimize-database

# فحص سلامة البيانات
python run.py --verify-database-integrity
```

#### **إدارة PostgreSQL المتقدمة:**
```sql
-- مراقبة الاتصالات
SELECT * FROM pg_stat_activity WHERE datname = 'sbards';

-- فحص حجم قاعدة البيانات
SELECT pg_size_pretty(pg_database_size('sbards'));

-- إحصائيات الجداول
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del 
FROM pg_stat_user_tables;

-- فحص الفهارس
SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes;
```

### **النسخ الاحتياطي المتقدم:**

#### **استراتيجية النسخ الاحتياطي:**
```json
{
    "backup_strategy": {
        "full_backup": {
            "schedule": "daily_at_02:00",
            "retention_days": 30,
            "compression": true,
            "encryption": true
        },
        "incremental_backup": {
            "schedule": "every_6_hours",
            "retention_days": 7,
            "compression": true
        },
        "transaction_log_backup": {
            "schedule": "every_15_minutes",
            "retention_hours": 24
        }
    }
}
```

#### **تنفيذ النسخ الاحتياطي:**
```bash
# نسخة احتياطية كاملة مشفرة
pg_dump sbards | gzip | gpg --encrypt --recipient admin@sbards.org > backup_full_$(date +%Y%m%d).sql.gz.gpg

# نسخة احتياطية تزايدية
pg_dump --incremental sbards > backup_incremental_$(date +%Y%m%d_%H%M).sql

# نسخ احتياطي تلقائي
crontab -e
# 0 2 * * * /path/to/sbards/scripts/daily_backup.sh
# 0 */6 * * * /path/to/sbards/scripts/incremental_backup.sh
```

---

## ⚙️ **تكوين النظام المتقدم** {#system-configuration}

### **ملف التكوين الرئيسي:**

#### **config.json - التكوين الشامل:**
```json
{
    "system": {
        "environment": "production",
        "debug_mode": false,
        "log_level": "INFO",
        "max_workers": 8,
        "memory_limit_gb": 4
    },
    "database": {
        "type": "postgresql",
        "host": "localhost",
        "port": 5432,
        "name": "sbards",
        "pool_size": 20,
        "max_overflow": 30,
        "connection_timeout": 30,
        "encryption_enabled": true
    },
    "security": {
        "authentication_required": true,
        "session_timeout": 3600,
        "max_failed_attempts": 3,
        "password_policy": {
            "min_length": 12,
            "require_uppercase": true,
            "require_lowercase": true,
            "require_numbers": true,
            "require_symbols": true
        },
        "encryption": {
            "algorithm": "AES-256-GCM",
            "key_rotation_days": 90
        }
    },
    "monitoring": {
        "health_check_interval": 30,
        "performance_metrics_interval": 60,
        "alert_thresholds": {
            "cpu_usage": 80,
            "memory_usage": 85,
            "disk_usage": 90,
            "response_time_ms": 1000
        }
    }
}
```

### **تكوين الطبقات الأمنية:**

#### **Capture Layer Configuration:**
```json
{
    "capture": {
        "enabled": true,
        "real_time_monitoring": true,
        "monitored_locations": [
            "/home/*/Downloads",
            "/tmp",
            "/var/tmp",
            "C:\\Users\\*\\Downloads",
            "C:\\Temp"
        ],
        "file_size_limits": {
            "max_file_size_mb": 500,
            "max_daily_files": 10000
        },
        "exclusions": {
            "file_extensions": [".log", ".tmp", ".cache"],
            "file_patterns": ["*backup*", "*temp*"],
            "directories": ["/var/log", "/proc", "/sys"]
        },
        "performance": {
            "max_concurrent_scans": 10,
            "scan_timeout_seconds": 300,
            "queue_size": 1000
        }
    }
}
```

#### **Analysis Configuration:**
```json
{
    "analysis": {
        "static_analysis": {
            "enabled": true,
            "analyzers": {
                "yara": {"enabled": true, "rules_path": "./yara_rules/"},
                "code": {"enabled": true, "deep_scan": true},
                "document": {"enabled": true, "macro_analysis": true},
                "network": {"enabled": true, "dns_analysis": true},
                "entropy": {"enabled": true, "threshold": 7.5},
                "ml": {"enabled": true, "model_path": "./ml_models/"}
            }
        },
        "dynamic_analysis": {
            "enabled": false,
            "sandbox_timeout": 300,
            "vm_snapshots": true
        }
    }
}
```

### **إدارة التكوين:**

#### **تحديث التكوين:**
```bash
# تحديث تكوين محدد
python run.py --set-config "database.pool_size=25"

# تحديث من ملف
python run.py --load-config ./configs/production.json

# التحقق من صحة التكوين
python run.py --validate-config

# عرض التكوين الحالي
python run.py --show-config
```

#### **تكوين متقدم للأداء:**
```json
{
    "performance": {
        "threading": {
            "capture_threads": 4,
            "analysis_threads": 8,
            "io_threads": 2
        },
        "caching": {
            "enabled": true,
            "cache_size_mb": 512,
            "cache_ttl_seconds": 3600
        },
        "optimization": {
            "batch_processing": true,
            "batch_size": 100,
            "compression_enabled": true
        }
    }
}
```

---

## 📊 **المراقبة والأداء** {#monitoring-performance}

### **مراقبة النظام في الوقت الفعلي:**

#### **مؤشرات الأداء الرئيسية:**
```bash
# مراقبة مباشرة
python run.py --monitor --real-time

# إحصائيات مفصلة
python run.py --system-stats --detailed

# تقرير أداء شامل
python run.py --performance-report --period 24h
```

#### **Dashboard المراقبة:**
```python
# مؤشرات الأداء المعروضة
{
    "system_health": {
        "cpu_usage": "15.2%",
        "memory_usage": "2.1GB / 8GB (26%)",
        "disk_usage": "45GB / 100GB (45%)",
        "network_io": "1.2MB/s"
    },
    "sbards_metrics": {
        "files_processed_today": 2847,
        "threats_detected": 12,
        "false_positives": 3,
        "average_processing_time": "127ms",
        "queue_size": 23
    },
    "database_metrics": {
        "active_connections": 15,
        "queries_per_second": 45,
        "cache_hit_ratio": "94.2%",
        "database_size": "2.3GB"
    }
}
```

### **تنبيهات وإنذارات:**

#### **تكوين التنبيهات:**
```json
{
    "alerts": {
        "email": {
            "enabled": true,
            "smtp_server": "smtp.company.com",
            "recipients": ["admin@company.com", "security@company.com"]
        },
        "slack": {
            "enabled": true,
            "webhook_url": "https://hooks.slack.com/...",
            "channel": "#security-alerts"
        },
        "thresholds": {
            "critical": {
                "multiple_threats": 5,
                "system_cpu": 90,
                "system_memory": 95,
                "database_connections": 50
            },
            "warning": {
                "processing_delay": 5000,
                "queue_size": 500,
                "disk_space": 85
            }
        }
    }
}
```

#### **سكريبت مراقبة مخصص:**
```bash
#!/bin/bash
# scripts/health_monitor.sh

# فحص صحة النظام
HEALTH=$(python run.py --health-check --json)
CPU_USAGE=$(echo $HEALTH | jq '.cpu_usage')
MEMORY_USAGE=$(echo $HEALTH | jq '.memory_usage')

# إرسال تنبيه إذا تجاوز الحد
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    python run.py --send-alert "High CPU usage: $CPU_USAGE%"
fi

if (( $(echo "$MEMORY_USAGE > 85" | bc -l) )); then
    python run.py --send-alert "High memory usage: $MEMORY_USAGE%"
fi
```

### **تحليل الأداء:**

#### **تقارير الأداء الدورية:**
```bash
# تقرير يومي
python run.py --daily-performance-report

# تقرير أسبوعي مفصل
python run.py --weekly-performance-report --detailed

# تحليل الاتجاهات
python run.py --trend-analysis --period 30d

# تقرير مقارن
python run.py --compare-performance --baseline last_month
```

#### **تحسين الأداء:**
```bash
# تحليل الاختناقات
python run.py --analyze-bottlenecks

# تحسين قاعدة البيانات
python run.py --optimize-database --vacuum --reindex

# تنظيف الملفات المؤقتة
python run.py --cleanup-temp-files --older-than 7d

# ضغط السجلات القديمة
python run.py --compress-logs --older-than 30d
```

---

## 🔒 **الأمان والنسخ الاحتياطي** {#security-backup}

### **إدارة الأمان المتقدمة:**

#### **تشفير البيانات:**
```bash
# تفعيل تشفير قاعدة البيانات
python run.py --enable-database-encryption --key-file ./keys/db_key.pem

# تشفير الملفات الحساسة
python run.py --encrypt-sensitive-files --algorithm AES-256

# دوران المفاتيح
python run.py --rotate-encryption-keys --backup-old-keys
```

#### **مراجعة الأمان:**
```bash
# فحص أمني شامل
python run.py --security-audit --detailed

# فحص الثغرات
python run.py --vulnerability-scan

# تحديث قواعد الأمان
python run.py --update-security-rules

# فحص سلامة الملفات
python run.py --integrity-check --all-files
```

### **إدارة الصلاحيات:**

#### **أدوار المستخدمين:**
```sql
-- إنشاء أدوار مخصصة
CREATE ROLE sbards_admin;
CREATE ROLE sbards_analyst;
CREATE ROLE sbards_viewer;

-- منح صلاحيات محددة
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sbards_admin;
GRANT SELECT, INSERT, UPDATE ON Files, StaticReports TO sbards_analyst;
GRANT SELECT ON Files, StaticReports, Verdicts TO sbards_viewer;
```

#### **إدارة المستخدمين:**
```bash
# إضافة مستخدم جديد
python run.py --add-user --username analyst1 --role analyst --email analyst1@company.com

# تعديل صلاحيات مستخدم
python run.py --modify-user --username analyst1 --role senior_analyst

# إلغاء تفعيل مستخدم
python run.py --disable-user --username analyst1

# عرض جميع المستخدمين
python run.py --list-users --detailed
```

### **النسخ الاحتياطي والاستعادة:**

#### **استراتيجية النسخ الاحتياطي الشاملة:**
```bash
# نسخة احتياطية كاملة للنظام
python run.py --full-system-backup --include-config --include-logs

# نسخة احتياطية للبيانات فقط
python run.py --data-backup --compress --encrypt

# نسخة احتياطية تزايدية
python run.py --incremental-backup --since-last-full

# اختبار سلامة النسخ الاحتياطية
python run.py --verify-backups --all
```

#### **خطة الاستعادة من الكوارث:**
```bash
# استعادة كاملة للنظام
python run.py --disaster-recovery --backup-location /backup/full_20241220/

# استعادة قاعدة البيانات فقط
python run.py --restore-database --backup ./backups/db_backup_20241220.sql

# استعادة التكوين
python run.py --restore-config --backup ./backups/config_backup_20241220.json

# التحقق من سلامة الاستعادة
python run.py --verify-restoration --run-tests
```

---

## 👥 **إدارة المستخدمين** {#user-management}

### **نظام إدارة المستخدمين:**

#### **إنشاء وإدارة المستخدمين:**
```python
# إدارة المستخدمين عبر Python API
from core.user_management import UserManager

user_manager = UserManager()

# إضافة مستخدم جديد
new_user = user_manager.create_user(
    username="security_analyst",
    email="analyst@company.com",
    role="analyst",
    permissions=["read_reports", "create_reports", "manage_quarantine"]
)

# تعديل صلاحيات
user_manager.update_permissions(
    username="security_analyst",
    add_permissions=["admin_dashboard"],
    remove_permissions=["manage_quarantine"]
)
```

#### **أدوار وصلاحيات محددة مسبقاً:**
```json
{
    "roles": {
        "super_admin": {
            "permissions": ["*"],
            "description": "صلاحيات كاملة للنظام"
        },
        "admin": {
            "permissions": [
                "manage_users", "manage_config", "view_all_reports",
                "manage_database", "system_maintenance"
            ],
            "description": "إدارة النظام والمستخدمين"
        },
        "senior_analyst": {
            "permissions": [
                "view_all_reports", "create_reports", "manage_quarantine",
                "configure_analysis", "view_system_stats"
            ],
            "description": "محلل أمني متقدم"
        },
        "analyst": {
            "permissions": [
                "view_reports", "create_basic_reports", "view_quarantine"
            ],
            "description": "محلل أمني أساسي"
        },
        "viewer": {
            "permissions": ["view_dashboard", "view_basic_reports"],
            "description": "عرض فقط"
        }
    }
}
```

### **مراقبة نشاط المستخدمين:**

#### **سجلات المراجعة:**
```sql
-- عرض نشاط المستخدمين
SELECT 
    u.username,
    al.action,
    al.resource,
    al.timestamp,
    al.ip_address
FROM AuditLogs al
JOIN Users u ON al.user_id = u.user_id
WHERE al.timestamp >= NOW() - INTERVAL '24 hours'
ORDER BY al.timestamp DESC;

-- إحصائيات نشاط المستخدمين
SELECT 
    u.username,
    COUNT(*) as total_actions,
    COUNT(CASE WHEN al.action = 'LOGIN' THEN 1 END) as logins,
    MAX(al.timestamp) as last_activity
FROM Users u
LEFT JOIN AuditLogs al ON u.user_id = al.user_id
GROUP BY u.username;
```

---

## 🛠️ **الصيانة والاستكشاف** {#maintenance-troubleshooting}

### **الصيانة الدورية:**

#### **مهام الصيانة اليومية:**
```bash
#!/bin/bash
# scripts/daily_maintenance.sh

echo "بدء الصيانة اليومية..."

# تنظيف الملفات المؤقتة
python run.py --cleanup-temp --older-than 1d

# ضغط السجلات القديمة
python run.py --compress-logs --older-than 7d

# تحديث قواعد YARA
python run.py --update-yara-rules

# فحص سلامة قاعدة البيانات
python run.py --check-database-integrity

# إنشاء تقرير صحة النظام
python run.py --health-report --email-admin

echo "انتهت الصيانة اليومية"
```

#### **مهام الصيانة الأسبوعية:**
```bash
#!/bin/bash
# scripts/weekly_maintenance.sh

echo "بدء الصيانة الأسبوعية..."

# تحسين قاعدة البيانات
python run.py --optimize-database --full

# تنظيف الملفات المحجورة القديمة
python run.py --cleanup-quarantine --older-than 30d

# تحديث قواعد التهديدات
python run.py --update-threat-intelligence

# إنشاء نسخة احتياطية كاملة
python run.py --full-backup --verify

# تحليل أداء الأسبوع
python run.py --weekly-performance-analysis

echo "انتهت الصيانة الأسبوعية"
```

### **استكشاف الأخطاء:**

#### **مشاكل شائعة وحلولها:**

##### **1. ارتفاع استهلاك الذاكرة:**
```bash
# تحليل استهلاك الذاكرة
python run.py --memory-analysis --detailed

# تنظيف ذاكرة التخزين المؤقت
python run.py --clear-cache --all

# إعادة تشغيل الخدمات الثقيلة
python run.py --restart-services --heavy-only
```

##### **2. بطء في الأداء:**
```bash
# تحليل الاختناقات
python run.py --performance-analysis --identify-bottlenecks

# تحسين الفهارس
python run.py --optimize-indexes --rebuild

# تقليل عدد الخيوط
python run.py --reduce-threads --temporary
```

##### **3. مشاكل قاعدة البيانات:**
```bash
# إصلاح قاعدة البيانات
python run.py --repair-database --safe-mode

# إعادة بناء الفهارس
python run.py --rebuild-indexes --all

# فحص الاتساق
python run.py --consistency-check --fix-errors
```

### **أدوات التشخيص المتقدمة:**

#### **تشخيص شامل للنظام:**
```bash
# تشغيل تشخيص كامل
python run.py --full-diagnosis --generate-report

# فحص التكامل بين المكونات
python run.py --integration-test --all-components

# اختبار الأداء تحت الضغط
python run.py --stress-test --duration 300s

# تحليل السجلات للأخطاء
python run.py --log-analysis --error-patterns
```

---

## 📈 **التحسين والتوسع** {#optimization-scaling}

### **تحسين الأداء:**

#### **تحسين قاعدة البيانات:**
```sql
-- تحسين الاستعلامات الشائعة
CREATE INDEX CONCURRENTLY idx_files_created_at ON Files(created_at);
CREATE INDEX CONCURRENTLY idx_static_reports_verdict ON StaticReports(verdict);
CREATE INDEX CONCURRENTLY idx_hashes_algorithm_value ON Hashes(algorithm, hash_value);

-- إحصائيات الجداول
ANALYZE Files;
ANALYZE StaticReports;
ANALYZE Hashes;

-- تحسين التكوين
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '16MB';
```

#### **تحسين التطبيق:**
```python
# تحسين معالجة الملفات
async def optimized_file_processing():
    # معالجة متوازية
    semaphore = asyncio.Semaphore(10)  # حد أقصى 10 ملفات متزامنة
    
    async def process_file_with_limit(file_path):
        async with semaphore:
            return await process_file(file_path)
    
    # معالجة دفعية
    batch_size = 50
    for i in range(0, len(files), batch_size):
        batch = files[i:i + batch_size]
        results = await asyncio.gather(*[
            process_file_with_limit(f) for f in batch
        ])
```

### **التوسع الأفقي:**

#### **Load Balancing:**
```yaml
# nginx.conf
upstream sbards_backend {
    server 127.0.0.1:8000 weight=3;
    server 127.0.0.1:8001 weight=3;
    server 127.0.0.1:8002 weight=2;
    server 127.0.0.1:8003 weight=2;
}

server {
    listen 80;
    location / {
        proxy_pass http://sbards_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### **Database Clustering:**
```yaml
# PostgreSQL Cluster Configuration
postgresql:
  primary:
    host: db-primary.sbards.local
    port: 5432
  replicas:
    - host: db-replica-1.sbards.local
      port: 5432
    - host: db-replica-2.sbards.local
      port: 5432
  connection_pooling:
    max_connections: 100
    pool_size: 20
```

### **مراقبة التوسع:**

#### **مؤشرات التوسع:**
```python
# مراقبة الحاجة للتوسع
scaling_metrics = {
    "cpu_usage_avg": 75,      # إذا تجاوز 80% لمدة 10 دقائق
    "memory_usage_avg": 80,   # إذا تجاوز 85% لمدة 5 دقائق
    "queue_size_avg": 500,    # إذا تجاوز 1000 لمدة 15 دقيقة
    "response_time_avg": 800, # إذا تجاوز 1000ms لمدة 5 دقائق
}

# تنبيهات التوسع التلقائي
if should_scale_up(scaling_metrics):
    trigger_auto_scaling("scale_up")
elif should_scale_down(scaling_metrics):
    trigger_auto_scaling("scale_down")
```

---

<div align="center">

**👨‍💼 دليل المدير الشامل - SBARDS v2.0.0**

*إدارة متقدمة لنظام أمني عالي الأداء*

**🛡️ إدارة محترفة لحماية متقدمة 🛡️**

</div>
