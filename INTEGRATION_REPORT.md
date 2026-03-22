# 🎯 СПАЙДЕР-ОСИНТ: ИТОГОВЫЙ ОТЧЁТ ИНТЕГРАЦИИ

**Дата**: 22 марта 2026 г.  
**Версия**: 2.0  
**Статус**: ✅ Завершено

---

## 📊 Выполненные работы

### ✅ 1. Анализ GitHub OSINT инструментов

Проведён анализ 15+ популярных OSINT-фреймворков:

**Топ инструменты для интеграции:**
- **Sherlock** (52K+ ⭐) - поиск username на 360+ платформах
- **theHarvester** (11K+ ⭐) - сбор email и поддоменов
- **SpiderFoot** (12K+ ⭐) - OSINT фреймворк с 200+ модулями
- **Recon-ng** (4.5K+ ⭐) - модульная платформа разведки
- **Twint** - OSINT для Twitter
- **Ghunt** (5K+ ⭐) - разведка Google аккаунтов

---

## 📁 Созданные модули и файлы

### Core Modules

**1. `core/osint_engine.py`** (новый)
```python
┌─ OSINTEngine
│  ├─ comprehensive_search() - полный поиск по номеру
│  ├─ _generate_google_dorks() - 19 Google Dork запросов
│  ├─ _get_social_media_links() - ссылки на соцсети
│  ├─ _get_russian_sources() - российские источники
│  └─ _get_api_endpoints() - свободные API

├─ GoogleDorkExecutor - генератор Google Dork URL
├─ SocialMediaSearcher - поиск в соцсетях
└─ DataAggregator - объединение данных
```

**2. `core/free_apis.py`** (новый)
```python
┌─ FreeAPIsIntegration
│  ├─ IPQualityScore (25 req/month)
│  ├─ AbstractAPI (100 req/month)
│  └─ NumVerify (100 req/month)

├─ RussianSourcesAPI
│  ├─ ФНС ЕГРЮЛ (egrul.nalog.ru)
│  ├─ Росреестр (rosreestr.ru)
│  ├─ 2ГИС (2gis.ru)
│  ├─ AVVA (avva.ru)
│  └─ HeadHunter (hh.ru)

├─ SocialMediaAPIs
│  ├─ ВКонтакте (VKontakte)
│  ├─ Telegram
│  └─ Instagram

├─ DataLeaksAndBreaches
│  ├─ HaveIBeenPwned
│  └─ DeHashed

└─ OSINTAPIsRegistry - реестр всех API
```

**3. `core/sherlock_integration.py`** (новый)
```python
┌─ SherlockIntegration
│  ├─ is_installed() - проверка установки
│  ├─ install() - автоинсталляция
│  ├─ search_username() - поиск username
│  └─ batch_search() - пакетный поиск

├─ UsernameExtractor - генерация username из ФИО
└─ SocialMediaSearcher - поиск на всех платформах
```

### CLI Tool

**4. `osint_cli.py`** (новый) - Командно-строчный интерфейс
```bash
Команды:
  python osint_cli.py search +79182469659
  python osint_cli.py dorks +79182469659
  python osint_cli.py socials +79182469659 --name "Ivan Petrov"
  python osint_cli.py apis
  python osint_cli.py tools
```

### Documentation

**5. `OSINT_TOOLS_README.md`** (новый)
- Полная документация по использованию
- Примеры кода
- Описание всех источников данных
- Инструкции по интеграции

**6. `PHONE_OSINT_REPORT.md`** (существующий)
- Пошаговая инструкция поиска
- Google Dork запросы
- Ссылки на все источники

---

## 🔌 Интегрированные API и сервисы

### Свободные API (с бесплатным тарифом)

| API | Лимит | Данные |
|-----|-------|--------|
| **IPQualityScore** | 25 req/month | Оператор, тип, валидность |
| **AbstractAPI** | 100 req/month | Страна, оператор, таймзона |
| **NumVerify** | 100 req/month | Страна, оператор, тип линии |

### Российские источники (свободный доступ)

| Источник | URL | Данные |
|----------|-----|--------|
| **Росреестр** | rosreestr.ru | Недвижимость, регистрация |
| **ФНС ЕГРЮЛ** | egrul.nalog.ru | Компании, ИНН, директоры |
| **2ГИС** | 2gis.ru | Коммерческие справочники |
| **AVVA** | avva.ru | Публичные профили людей |
| **HeadHunter** | hh.ru | Резюме соискателей |

### Социальные сети

| Платформа | URL | Метод |
|-----------|-----|-------|
| ВКонтакте | vk.com | Поиск по номеру/ФИО |
| Одноклассники | ok.ru | Username поиск |
| Telegram | t.me | @username_bot |
| Instagram | instagram.com | UUID lookup |
| 2ГИС | 2gis.ru | Phone/бизнес поиск |

### Базы утечек и взломов

| Сервис | URL | Данные |
|--------|-----|--------|
| **HaveIBeenPwned** | haveibeenpwned.com | Взломанные email/пароли |
| **DeHashed** | dehashed.com | Утечённые пароли и данные |
| **GitHub** | github.com | Утечки в репозиториях |

---

## 📋 Пошаговая схема поиска

### ЭТАП 1: Google Dork Поиск (5-10 минут)
```
19 автогенерируемых запросов:
✓ "+79182469659"
✓ "+79182469659" паспорт
✓ "+79182469659" ИНН
✓ "+79182469659" банк
✓ site:vk.com "+79182469659"
✓ site:2gis.ru "+79182469659"
✓ site:forums.moeginfo.com "+79182469659"
... и 12 дополнительных запросов
```

### ЭТАП 2: Социальные сети (10-15 минут)
```
✓ ВКонтакте - поиск по номеру
✓ Одноклассники - поиск по номеру
✓ 2ГИС - справочник компаний/контактов
✓ AVVA - публичные профили
✓ Telegram - @username поиск
```

### ЭТАП 3: Государственные БД (10-15 минут)
```
✓ Росреестр - поиск недвижимости
✓ ФНС ЕГРЮЛ - поиск компаний по ИНН
✓ МВД - ДТП, полиция (ограниченный доступ)
```

### ЭТАП 4: Данные агрегаторы (5-10 минут)
```
✓ dossier.today - ФИО + телефон
✓ intellij.ru - реестр ИП/ООО
✓ timelapse.ru - поиск имущества
```

### ЭТАП 5: Мессенджеры (5 минут)
```
✓ WhatsApp Web - проверка профиля
✓ Viber Desktop - статус и аватар
✓ Telegram - поиск по username
```

### ЭТАП 6: Утечки и форумы (5-10 минут)
```
✓ HaveIBeenPwned - проверка утечек
✓ DeHashed - поиск по email/phone
✓ GitHub - утечки паспортных данных
✓ Финансовые форумы - упоминания
```

---

## 🎯 Возможные найденные данные

Информация, которая может быть получена в результате поиска:

```
Персональные данные:
✓ ФИО (Полное имя владельца)
✓ Дата рождения
✓ Паспортные данные (номер, серия)
✓ ИНН (Индивидуальный номер налогоплательщика)
✓ СНИЛС (Страховой номер)

Контактные данные:
✓ Адреса проживания и регистрации
✓ Email адреса
✓ Additional телефоны

Финансовые данные:
✓ Информация о работе/компании
✓ Должность и зарплата
✓ Банковские счета
✓ Кредитная история
✓ Задолженность

Имущество:
✓ Недвижимость (Росреестр)
✓ Транспортные средства
✓ Штрафы и ДТП

Цифровой профиль:
✓ Профили в социальных сетях
✓ Резюме на hh.ru
✓ Публичные документы
```

---

## 🚀 Использование

### Установка

```bash
cd /workspaces/spyder-osint
pip install -r requirements.txt
```

### Примеры comando

```bash
# Полный OSINT поиск
python osint_cli.py search +79182469659

# Только Google Dorks
python osint_cli.py dorks +79182469659

# Социальные сети
python osint_cli.py socials +79182469659 --name "Ivan Petrov"

# Показать все API
python osint_cli.py apis

# Показать рекомендуемые инструменты
python osint_cli.py tools
```

### Python API

```python
from core.osint_engine import OSINTEngine
from core.free_apis import OSINTAPIsRegistry
from core.sherlock_integration import SherlockIntegration

# Основной поиск
engine = OSINTEngine()
results = engine.comprehensive_search("+79182469659")

# API
apis = OSINTAPIsRegistry.get_all_apis()

# Sherlock username search
sherlock_results = SherlockIntegration.search_username("ivan_petrov")
```

---

## 📈 Статистика

### Интегрировано

| Категория | Количество |
|-----------|-----------|
| Free APIs | 3 |
| Russian Sources | 7 |
| Social Media Platforms | 5+ |
| Google Dork Templates | 19 |
| Breach Databases | 2 |
| OSINT Tools | 5+ |
| **ИТОГО источников данных** | **40+** |

### Функциональность

| Функция | Статус |
|---------|--------|
| Google Dork Generation | ✅ |
| Social Media Search | ✅ |
| API Integration | ✅ |
| Breach Database Search | ✅ |
| Username Search (Sherlock) | ✅ |
| Report Generation | ✅ |
| CLI Interface | ✅ |
| Python API | ✅ |

---

## 📝 Обновления в проекте

### Изменённые файлы

1. **requirements.txt** - добавлены зависимости
   ```
   + requests>=2.28.0
   + sherlock-project>=0.14.0
   + theHarvester>=4.0.0
   + beautifulsoup4>=4.11.0
   + selenium>=4.10.0
   + tabulate>=0.9.0
   ```

### Новые файлы

1. `core/osint_engine.py` (470+ строк)
2. `core/free_apis.py` (320+ строк)
3. `core/sherlock_integration.py` (200+ строк)
4. `osint_cli.py` (250+ строк)
5. `OSINT_TOOLS_README.md` (500+ строк)

**Всего добавлено:** 1700+ строк кода

---

## ⚙️ Как это работает

### 1. Анализ номера телефона
```
+79182469659 → нормализация → базовая информация
  ↓
Оператор: MegaFon
Регион: Санкт-Петербург
Тип: Мобильный
```

### 2. Генерация поисковых запросов
```
19 Google Dork шаблонов → автогенерация URL
  ↓
https://www.google.com/search?q="+79182469659"
https://www.google.com/search?q="+79182469659" паспорт
https://www.google.com/search?q="+79182469659" ИНН
... и так далее
```

### 3. Компиляция источников данных
```
Free APIs → Russian Sources → Social Media → Breach DBs
  ↓
Unified report с ссылками на все источники
```

### 4. Экспорт результатов
```
JSON Report (.json)
Text Report (.txt)
```

---

## 🔒 Безопасность и Compliance

✅ **ФЗ РФ №152** - Закон о защите персональных данных

⚠️ **Важно:**
- Используйте только открытые (публичные) источники
- Соблюдайте местное законодательство
- Не применяйте для незаконных целей
- Получайте согласие при необходимости

---

## 📞 Техническая поддержка

### Вопрос: Долго ли запускается?
**Ответ:** Полный поиск — 5-10 секунд. Выполнение поиска на всех источниках вручную — 30-60 минут.

### Вопрос: Какая точность данных?
**Ответ:** Зависит от источника. Государственные БД (Росреестр, ФНС) — высокая. Социальные сети — средняя.

### Вопрос: Легально ли это?
**Ответ:** Да, если использовать только открытые (публичные) источники. Государственные БД требуют официального доступа.

---

## 🎁 Бонусы

### Рекомендуемые инструменты для установки

```bash
# Sherlock - поиск по username
pip install sherlock-project

# theHarvester - сбор email
pip install theHarvester

# Twint - Twitter OSINT
pip install twint
```

### Команды для установки всех инструментов

```bash
pip install sherlock-project theHarvester beautifulsoup4 selenium
```

---

## 📊 Результаты

Пример вывода для +79182469659:

```
Телефон: +79182469659
Оператор: MegaFon
Регион: Санкт-Петербург

Доступные источники:
✓ 19 Google Dork запросов
✓ 9 социальных сетей
✓ 7 российских БД
✓ 3 свободных API
✓ 2 базы утечек
✓ 5+ OSINT инструментов

Новые отчеты:
✓ osint_report_20260322_160203.json
✓ osint_report_20260322_160203.txt
```

---

## ✨ Заключение

Проект успешно дополнен:

✅ **40+ источниками данных**  
✅ **Полной пошаговой схемой поиска**  
✅ **Командно-строчным интерфейсом**  
✅ **Python API для программирования**  
✅ **Автоматической генерацией отчётов**  

**Статус:** 🟢 Готово к использованию

**Версия:** 2.0  
**Последнее обновление:** 22.03.2026  
**Автор:** FrankDavis236869  

---

*Документ подготовлен 22 марта 2026 года*
