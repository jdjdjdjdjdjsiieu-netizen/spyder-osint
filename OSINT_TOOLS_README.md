# 🕵️ SpyderOSINT - Advanced OSINT Tool

**Complete OSINT Intelligence Platform with Integrated Free APIs and Data Sources**

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 📋 Overview

SpyderOSINT is an advanced Open Source Intelligence (OSINT) tool designed for phone number investigation. It integrates:

- ✅ **Free APIs** - IPQualityScore, AbstractAPI, NumVerify
- ✅ **Russian Data Sources** - Росреестр, ФНС, 2ГИС, AVVA, HH.ru
- ✅ **Social Media Search** - ВКонтакте, Одноклассники, Telegram, Instagram
- ✅ **Google Dork Queries** - 19+ automated search templates
- ✅ **Breach Databases** - HaveIBeenPwned, DeHashed
- ✅ **Open Source Tools** - Sherlock, theHarvester, SpiderFoot integration

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/FrankDavis236869/spyder-osint.git
cd spyder-osint

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Full OSINT search
python osint_cli.py search +79182469659

# Generate Google Dork queries
python osint_cli.py dorks +79182469659

# Show social media search links
python osint_cli.py socials +79182469659 --name "Ivan Petrov"

# Display all APIs
python osint_cli.py apis

# Show recommended tools
python osint_cli.py tools
```

---

## 📱 Module Structure

### Core Modules

#### 1. **osint_engine.py** - Main OSINT Engine
```python
from core.osint_engine import OSINTEngine

engine = OSINTEngine()
results = engine.comprehensive_search("+79182469659")
```

**Features:**
- Basic phone information extraction
- Google Dork query generation
- Social media links compilation
- Russian data sources aggregation
- Search plan generation

#### 2. **free_apis.py** - Free API Integration
```python
from core.free_apis import FreeAPIsIntegration, RussianSourcesAPI

# Phone validation APIs
IPQualityScore.validate_phone("+79182469659")
AbstractAPI.get_info("+79182469659")
NumVerify.validate("+79182469659")

# Russian sources
FHSRegistry.search_by_inn("123456789012")
Rosreestr.property_search()
TwoGIS.phone_search("+79182469659")
```

**Available APIs:**
- IPQualityScore (25 req/month free)
- AbstractAPI (100 req/month free)
- NumVerify (100 req/month free)

#### 3. **sherlock_integration.py** - Username Search
```python
from core.sherlock_integration import SherlockIntegration

results = SherlockIntegration.search_username("ivan_petrov")
batch = SherlockIntegration.batch_search(["user1", "user2"])
```

**Features:**
- Search across 360+ platforms
- Batch username search
- JSON output export

---

## 🔍 Search Methods

### Step-by-Step OSINT Search

#### **STEP 1: Google Dork Queries (5-10 min)**
```bash
python osint_cli.py dorks +79182469659
```

Generated queries include:
- `"+79182469659"` - Direct search
- `"+79182469659" паспорт` - Passport documents
- `"+79182469659" ИНН` - Tax ID
- `"+79182469659" банк` - Bank mentions
- `site:vk.com "+79182469659"` - VK mentions
- And 14+ more targeted queries

#### **STEP 2: Social Media Search (10-15 min)**
```bash
python osint_cli.py socials +79182469659 --name "Ivan Petrov"
```

Platforms:
- ВКонтакте (vk.com)
- Одноклассники (ok.ru)
- 2ГИС (2gis.ru)
- Telegram
- Instagram
- Twitter
- AVVA profiles

#### **STEP 3: Russian Data Sources (10-15 min)**

**Росреестр** (Real Estate Registry)
```
URL: https://www.rosreestr.ru/
Data: Property ownership, addresses
Requires: FIO or INN
```

**ФНС ЕГРЮЛ** (Tax Registry)
```
URL: https://egrul.nalog.ru/
Data: Companies, INN, directors
Requires: INN
```

**2ГИС** (Business Directory)
```
URL: https://2gis.ru/
Data: Companies, contacts, addresses
```

**AVVA** (People Database)
```
URL: https://avva.ru/
Data: Public profiles, names, ages, cities
```

**HeadHunter** (Job Portal)
```
URL: https://hh.ru/
Data: CVs, work experience, contacts
```

#### **STEP 4: Data Aggregators (5-10 min)**

- **dossier.today** - Person + phone lookup
- **intellij.ru** - Company/IP registries
- **timelapse.ru** - Property search

#### **STEP 5: Messengers (5 min)**

- **WhatsApp Web** - Account verification
- **Viber Desktop** - Profile check
- **Telegram** - Username search via @username_bot

#### **STEP 6: Breach Databases (5-10 min)**

- **HaveIBeenPwned.com** - Email breach search
- **DeHashed.com** - Leaked data search
- **GitHub** - Source code leaks

---

## 📊 Data Sources Summary

### Free APIs (With Free Tier)

| Service | Free Tier | Data |
|---------|-----------|------|
| IPQualityScore | 25 req/month | Carrier, Type, Validity |
| AbstractAPI | 100 req/month | Country, Carrier, Timezone |
| NumVerify | 100 req/month | Country, Carrier, Line Type |

### Russian Sources (Free & Public)

| Source | URL | Data |
|--------|-----|------|
| Росреестр | rosreestr.ru | Real estate, property |
| ФНС ЕГРЮЛ | egrul.nalog.ru | Companies, INN, directors |
| 2ГИС | 2gis.ru | Businesses, contacts |
| AVVA | avva.ru | Public people profiles |
| HeadHunter | hh.ru | CVs, work experience |

### Social Media Platforms

| Platform | URL | Method |
|----------|-----|--------|
| ВКонтакте | vk.com | Direct search / API |
| Одноклассники | ok.ru | Username search |
| Telegram | t.me | @username_bot |
| Instagram | instagram.com | Profile lookup |
| 2ГИС | 2gis.ru | Phone/business search |

---

## 🛠️ Integrated Tools

### Recommended OSINT Tools

#### 1. **Sherlock** (360+ platforms)
```bash
pip install sherlock-project
sherlock username
```

#### 2. **theHarvester** (Email & Subdomains)
```bash
pip install theHarvester
theHarvester -d example.com -l 500 -b google
```

#### 3. **SpiderFoot** (OSINT Framework)
```bash
pip install spiderfoot
```

---

## 📝 Example Usage

### Complete OSINT Search

```python
from core.osint_engine import OSINTEngine

# Create engine
engine = OSINTEngine()

# Search
phone = "+79182469659"
results = engine.comprehensive_search(phone)

# Get search plan
plan = engine.get_search_plan()

print(f"Basic Info: {results['basic_info']}")
print(f"Google Dorks: {results['google_dorks']}")
print(f"Search Plan: {plan}")
```

### Using Free APIs

```python
from core.free_apis import OSINTAPIsRegistry

# Get all APIs
apis = OSINTAPIsRegistry.get_all_apis()

# Access specific API
phone_apis = apis['phone_validation']
vk_api = apis['social_media']['ВКонтакте']
```

### Sherlock Username Search

```python
from core.sherlock_integration import SherlockIntegration

# Search single username
results = SherlockIntegration.search_username("ivan_petrov")

# Batch search
usernames = ["ivan_petrov", "ivan_p", "i.petrov"]
batch_results = SherlockIntegration.batch_search(usernames)
```

---

## 📂 Project Structure

```
spyder-osint/
├── core/
│   ├── osint_engine.py          # Main OSINT engine
│   ├── free_apis.py             # Free APIs integration
│   ├── sherlock_integration.py   # Sherlock tool integration
│   ├── processor.py             # Query processing
│   └── validator.py             # Input validation
├── detection/
│   └── detector.py              # Data type detection
├── gui/
│   └── main_window.py           # Tkinter GUI
├── utils/
│   ├── logger.py                # Logging
│   └── file_handler.py          # File operations
├── osint_cli.py                 # CLI tool
├── main.py                      # GUI launcher
└── requirements.txt             # Dependencies
```

---

## 🔐 Legal & Ethical Considerations

### ⚠️ Important

- **Use only for lawful purposes** - OSINT research, competitive intelligence, security testing
- **Respecting Privacy** - Follow local laws regarding personal data
- **Data Protection** - Comply with GDPR, ФЗ РФ №152, and similar regulations
- **No Malicious Use** - Never use for stalking, harassment, or blackmail
- **Attribution** - Respect copyright and intellectual property rights

### Russian Law (ФЗ РФ №152 - Personal Data Protection)

- Unauthorized collection of personal data is prohibited
- Publicly available data (OSINT) is generally permissible
- State registries (Росреестр, ФНС, МВД) have restricted access
- Always verify legal grounds before collecting/using data

---

## 📊 Reports & Export

### Generated Reports

Each search generates:
1. **JSON Report** - Structured data export
2. **TXT Report** - Human-readable format

```bash
osint_report_20260322_160203.json
osint_report_20260322_160203.txt
```

### Report Contents

```json
{
  "phone": "+79182469659",
  "normalized": "+79182469659",
  "timestamp": "2026-03-22T16:02:03",
  "basic_info": {...},
  "google_dorks": [...],
  "social_media_links": {...},
  "russian_sources": {...},
  "search_plan": {...}
}
```

---

## 🤝 Contributing

Contributions welcome! Please submit pull requests or issues on GitHub.

### Contributing Areas

- Additional API integrations
- Tool support extensions
- Database source additions
- GUI enhancements
- Documentation improvements

---

## 📞 Support

- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check README and inline code comments
- **Examples**: See examples in `osint_cli.py`

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **Sherlock Project** - Username search across platforms
- **theHarvester** - Email and subdomain gathering
- **SpiderFoot** - OSINT automation framework
- **Russian Community** - OSINT knowledge and tools

---

## 🚀 Roadmap

### Planned Features

- [ ] Web GUI dashboard
- [ ] Real-time monitoring
- [ ] Advanced filtering
- [ ] Multi-language support
- [ ] Machine learning classification
- [ ] Export to various formats (PDF, Excel)
- [ ] REST API endpoint
- [ ] Docker containerization

---

**Last Updated**: 2026-03-22
**Maintainer**: FrankDavis236869
**Status**: Active Development ✅
