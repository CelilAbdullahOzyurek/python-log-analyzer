# Python-Log-Analyzer - Güvenlik Log Analiz Aracı

Docker container içinde çalışan, gerçek zamanlı log izleme ve güvenlik tehdit analizi yapabilen CLI tabanlı bir araçtır. Web sunucu logları (access.log) ve sistem logları (auth.log, syslog) üzerinde önceden tanımlanmış kurallara göre tehdit tespiti yapar.

---

## İçindekiler

- [Özellikler](#özellikler)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Proje Yapısı](#proje-yapısı)
- [Konfigürasyon](#konfigürasyon)
- [Docker Yapılandırması](#docker-yapılandırması)
- [Güvenlik Uyarıları](#güvenlik-uyarıları)
- [Docker Olmadan Çalıştırma](#docker-olmadan-çalıştırma)
- [Test Etme](#test-etme)
- [Geliştirici](#geliştirici)

---

## Özellikler

| Özellik | Açıklama |
|---------|----------|
| **Statik Analiz** | Mevcut log dosyalarını tarayarak tehdit tespiti |
| **Canlı İzleme** | Gerçek zamanlı log takibi (tail -f benzeri) |
| **CSV Raporlama** | Tespit edilen tehditleri Excel uyumlu CSV formatında dışa aktarma |
| **Özelleştirilebilir Kurallar** | YAML tabanlı regex kuralları ile esnek tehdit tanımlama |
| **Docker Desteği** | İzole ve taşınabilir konteyner ortamı |

### Tespit Edilen Tehdit Türleri

- **SQL Injection** denemeleri
- **Bot/Scanner** saldırıları (wp-admin, admin panel taramaları)
- **Hassas Dosya Erişim** denemeleri (.env, .git, .htaccess vb.)
- **SSH Brute Force** saldırıları (Başarısız login denemeleri)
- **SSH Invalid User** denemeleri
- **Sudo Abuse** girişimleri

---

## Gereksinimler

### Zorunlu

- **Docker** (v20.10+)
- **Docker Compose** (v2.0+)
- **Root/Sudo Yetkisi** (Linux sistemlerde Docker daemon'a erişim için gereklidir)

---

## Kurulum

### 1. Projeyi İndirin

```bash
git clone https://github.com/CelilAbdullahOzyurek/python-log-analyzer.git
cd python-log-analyzer
```

### 2. Docker Image'ı Oluşturun

```bash
sudo docker-compose build
```

> İlk build işlemi birkaç dakika sürebilir.

### 3. Uygulamayı Başlatın

```bash
sudo docker-compose run app
```

> **Önemli:** Linux sistemlerde Docker daemon'a erişim için `sudo` kullanmanız gerekir. Eğer "permission denied" hatası alıyorsanız, komutun başına `sudo` eklemeyi unutmayın.

> **Not:** `docker-compose up` komutu yerine `docker-compose run app` kullanılmalıdır. Aksi takdirde interaktif terminal düzgün çalışmaz ve girdi alamazsınız.

---

## Kullanım

Uygulama başladığında interaktif bir menü ile karşılaşacaksınız:

```
  CLI - Log analysis tool
1. Static File Analysis (Read & Summarize File)
2. Live Monitoring Mode (Real-time Tailing)
3. Create CSV (Exel) Report
4. Exit
Choese between (1-4):
```

### ÖNEMLİ: Docker İçindeki Dosya Yolları

Container içinde çalıştığınız için **dosya yolları host sistemden farklıdır!**

| Host Sistemi | Container İçi |
|--------------|---------------|
| `/var/log/auth.log` | `/app/logs/auth.log` |
| `/var/log/nginx/access.log` | `/app/logs/nginx/access.log` |
| `/var/log/syslog` | `/app/logs/syslog` |
| `./reports/` | `/app/reports/` |

### Seçenek 1: Statik Dosya Analizi

Mevcut bir log dosyasını tarar ve tehdit tespiti yapar.

```
Choese between (1-4): 1
Enter the log path do you want to analysis: /app/logs/auth.log
```

**Örnek Çıktı:**
```
[HIGH]: SSH Failed Login
Log: Jan 15 14:32:01 server sshd[12345]: Failed password for root from 192.168.1.100...
------------------------------
==================================================
total scanned lines: 1523
Potential threats: 47
```

### Seçenek 2: Canlı İzleme Modu

Log dosyasını gerçek zamanlı olarak izler. Yeni satırlar eklendikçe anında analiz eder.

```
Choese between (1-4): 2
Enter the log path you want to monitor live: /app/logs/access.log
```

>  Çıkmak için `Ctrl + C` tuşlarını kullanın.

### Seçenek 3: CSV Raporu Oluşturma

Tespit edilen tehditleri detaylı bir CSV dosyasına aktarır.

```
Choese between (1-4): 3
Enter the log path do you want get report: /app/logs/auth.log
```

**Çıktı:**
```
Your report is created Report2026-01-31_14-30-00.csv
File Path: /app/reports/Report2026-01-31_14-30-00.csv
Total 47 threats added your report.
```

Rapor dosyası host sistemdeki `./reports/` klasöründe oluşturulur.

**CSV Rapor İçeriği:**
| Alan | Açıklama |
|------|----------|
| Detection Date | Tespit tarihi |
| Log Date | Log kaydının tarihi |
| Line Number | Satır numarası |
| IP Address | Kaynak IP adresi |
| Threat Type | Tehdit türü |
| Severity | Önem seviyesi (Critical/High/Medium/Info) |
| Request Info | İstek detayları |
| Device Info | User-Agent bilgisi |
| Raw Log | Ham log satırı |

---

## Proje Yapısı

```
log-analyzer/
├── main.py              # Ana uygulama ve CLI menüsü
├── analyzer.py          # Log analiz motoru ve kural işleyici
├── monitor.py           # Gerçek zamanlı log izleme modülü
├── reporter.py          # CSV rapor oluşturma modülü
├── requirements.txt     # Python bağımlılıkları
├── Dockerfile           # Docker image tanımı
├── docker-compose.yml   # Docker Compose yapılandırması
├── config/
│   └── rules.yaml       # Tehdit tespit kuralları
└── reports/             # Oluşturulan CSV raporları
```

---

## Konfigürasyon

### Tehdit Kuralları (config/rules.yaml)

> **Önemli Uyarı:** Bu araçta tanımlı kurallar yalnızca **belirli tehdit kalıplarını** tespit etmek için tasarlanmıştır. Kurallar tüm saldırı vektörlerini kapsamaz ve %100 güvenlik garantisi vermez. Saldırganlar farklı encoding yöntemleri, obfuscation teknikleri veya henüz tanımlanmamış yeni saldırı desenleri kullanabilir. Bu araç, kapsamlı bir güvenlik çözümü değil, yalnızca bir **yardımcı analiz aracı** olarak değerlendirilmelidir. Üretim ortamlarında profesyonel WAF, IDS/IPS ve SIEM çözümleriyle birlikte kullanılması önerilir.

Kurallar YAML formatında tanımlanır. Her kural şu alanları içerir:

```yaml
rules:
  - name: "Kural Adı"           # Tehdit adı
    type: "regex"               # Kural tipi (şu an sadece regex desteklenir)
    pattern: "regex_pattern"    # Aranacak regex deseni
    severity: "critical"        # Önem seviyesi: critical, high, medium, info
```

### Yeni Kural Ekleme

1. `config/rules.yaml` dosyasını açın
2. Yeni kuralınızı ekleyin:

```yaml
  - name: "XSS Attack Attempt"
    type: "regex"
    pattern: "<script.*?>|javascript:|onerror\\s*="
    severity: "high"
```

3. Container'ı yeniden başlatın (konfigürasyon otomatik yüklenir)

---

## Docker Yapılandırması

### docker-compose.yml Açıklaması

```yaml
services:
  app:
    build: .
    user: "0:0"                          # Root olarak çalışır (log erişimi için)
    privileged: false                     # Güvenlik: privileged mod kapalı
    image: log-analyzer
    container_name: log-analyzer-cli
    stdin_open: true                      # İnteraktif giriş için
    tty: true                             # Terminal için

    volumes:
      - /var/log:/app/logs:ro             # Host logları (salt okunur)
      - ./reports:/app/reports            # Raporlar (yazılabilir)
      - /etc/localtime:/etc/localtime:ro  # Zaman senkronizasyonu
      - /etc/timezone:/etc/timezone:ro    # Timezone senkronizasyonu
```

### Volume Mapping Detayları

| Volume | Açıklama | Mod |
|--------|----------|-----|
| `/var/log:/app/logs` | Host sistem loglarını container'a bağlar | Read-Only (`:ro`) |
| `./reports:/app/reports` | Raporların kaydedileceği klasör | Read-Write |
| `/etc/localtime:/etc/localtime` | Zaman senkronizasyonu | Read-Only |
| `/etc/timezone:/etc/timezone` | Timezone ayarı | Read-Only |

### Farklı Log Dizinleri İçin Özelleştirme

Nginx veya özel log dizinlerini eklemek için `docker-compose.yml` dosyasını düzenleyin:

```yaml
volumes:
  - /var/log:/app/logs:ro
  - /var/log/nginx:/app/logs/nginx:ro        # Nginx logları
  - /var/log/apache2:/app/logs/apache2:ro    # Apache logları
  - /opt/myapp/logs:/app/logs/myapp:ro       # Özel uygulama logları
  - ./reports:/app/reports
```

---

## Güvenlik Uyarıları

### Root Yetkileri Hakkında

Bu uygulama, sistem loglarına (`/var/log`) erişebilmek için **root yetkisiyle** çalışmaktadır:

```yaml
user: "0:0"  # UID:GID = root:root
```

**Neden gerekli?**
- `/var/log/auth.log`, `/var/log/syslog` gibi dosyalar genellikle sadece root tarafından okunabilir
- Container içinde log dosyalarına erişim için bu yetki zorunludur

**Güvenlik önlemleri:**

- `privileged: false` - Container sistem çağrılarına tam erişime sahip değil
- Loglar `:ro` (read-only) olarak mount edilmiş - Container logları değiştiremez
- Container izole bir ortamda çalışır

---

## Docker Olmadan Çalıştırma

Eğer Docker kullanmak istemiyorsanız:

### Linux/macOS

```bash
# Virtual environment oluştur
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Çalıştır (root gerekebilir)
sudo python main.py
```

### Windows

```powershell
# Bağımlılıkları yükle
pip install -r requirements.txt

# Çalıştır
python main.py
```

> **Not:** Docker olmadan çalıştırırken `analyzer.py` ve `reporter.py` dosyalarındaki path'leri güncellemeniz gerekebilir:
> - `/app/config/rules.yaml` → `./config/rules.yaml`
> - `/app/reports/` → `./reports/`

---

## Test Etme

```bash
# Uygulamayı başlat
sudo docker-compose run app

# Örnek access.log analizi için menüden 1 seçin
1
/app/logs/access.log

# Örnek auth.log analizi için menüden 1 seçin
1
/app/logs/auth.log
```

---

## Geliştirici

**Celil Abdullah Özyürek**

- GitHub: [@CelilAbdullahOzyurek](https://github.com/CelilAbdullahOzyurek)
