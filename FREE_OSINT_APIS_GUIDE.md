# Руководство: Свободные API для OSINT и Phone Lookup

Этот документ содержит список свободных API, которые можно интегрировать в инструмент для OSINT и поиска по телефонам.

---

## 1. КОЛЛЕКЦИИ СВОБОДНЫХ API (Основные репозитории)

### 1.1 **public-apis/public-apis**
- **URL**: https://github.com/public-apis/public-apis
- **Описание**: Подробный список free/open JSON APIs
- **Содержит**: 1000+ API в различных категориях
- **Автентификация**: Разная для каждого API
- **Интеграция**: Справочник всех основных свободных API

### 1.2 **n0shake/Public-APIs**
- **URL**: https://github.com/n0shake/Public-APIs
- **Описание**: Каталог публичных API
- **Автентификация**: Большая часть без требований
- **Интеграция**: Ссылка на файл с примерами использования

### 1.3 **jivoi/awesome-osint**
- **URL**: https://github.com/jivoi/awesome-osint
- **Описание**: Кураторский список OSINT ресурсов и инструментов
- **Категории**: 50+ различных типов инструментов для OSINT
- **Интеграция**: Выборочное использование для расширения функций

---

## 2. ПОИСК ТЕЛЕФОНА И ВЕРИФИКАЦИЯ

### 2.1 **NumVerify (openrates)**
- **Назначение**: Валидация и поиск информации по телефону
- **URL**: https://numverify.com
- **Бесплатный уровень**: 100 запросов/месяц
- **Лимиты**: HTTP (300 запросов/мес), HTTPS (100 запросов/мес)
- **Автентификация**: Требуется API ключ
- **Интеграция**:
```python
import requests
api_key = "YOUR_API_KEY"
phone = "+1234567890"
url = f"https://api.numverify.com/validate?number={phone}&access_key={api_key}"
```
- **Возвращает**: Валидность номера, страну, оператора, примечания

### 2.2 **TrueCaller API**
- **Назначение**: Идентификация звонящего, спам-детекция
- **URL**: https://www.truecaller.com/api
- **Бесплатный уровень**: Ограничен для разработчиков
- **Автентификация**: Требуется API ключ
- **Интеграция**: REST API для идентификации номеров

### 2.3 **OpenPhoneNumber (deprecated)**
- **Альтернатива**: Используйте numverify или вспомогательные базы данных

### 2.4 **OSINT Framework - Phone Lookup (Collections)**
- **Назначение**: Каталог инструментов для поиска по телефону
- **URL**: https://osintframework.com
- **Интеграция**: Портал со ссылками на 50+ инструментов поиска по телефону

---

## 3. ГЕОЛОКАЦИЯ ПО IP

### 3.1 **IP API (ip-api.com)**
- **Назначение**: Геолокация по IP адресу
- **URL**: https://ip-api.com
- **Бесплатный уровень**: 45 запросов/мин (бесплатно), без ключа
- **Лимиты**: 45 req/min для HTTP, неограниченно для HTTPS с прокси
- **Автентификация**: Необязательно для базовой версии
- **Интеграция**:
```python
import requests
ip = "8.8.8.8"
response = requests.get(f'http://ip-api.com/json/{ip}')
data = response.json()
print(f"Страна: {data['country']}, Город: {data['city']}")
```
- **Возвращает**: Страна, регион, город, широта/долгота, ISP

### 3.2 **ipapi.co**
- **Назначение**: Геолокация по IP
- **URL**: https://ipapi.co/api/docs/
- **Бесплатный уровень**: 30,000 запросов/месяц
- **Автентификация**: За бесплатно - максимум 1000 запросов/день
- **Интеграция**:
```python
import requests
response = requests.get('https://ipapi.co/json/')
data = response.json()
```

### 3.3 **MaxMind GeoIP2 (GeoLite2)**
- **Назначение**: Точная геолокация по IP (бесплатная версия)
- **URL**: https://www.maxmind.com/en/geolite2/
- **Бесплатный уровень**: GeoLite2 - Бесплатно, но менее точно
- **Лимиты**: Без лимитов запросов
- **Интеграция**: Скачайте бинарную базу и используйте локально
```python
import geoip2.database
with geoip2.database.Reader('/path/to/GeoLite2-City.mmdb') as reader:
    response = reader.city('8.8.8.8')
```

### 3.4 **Yandex Maps API (для России)**
- **Назначение**: Геолокация и геокодирование
- **URL**: https://yandex.ru/dev/maps/
- **Бесплатный уровень**: 50,000 запросов/день (бесплатно)
- **Автентификация**: Требуется API ключ
- **Интеграция**: Официальная документация на https://tech.yandex.ru/maps/

---

## 4. EMAIL ВЕРИФИКАЦИЯ И ПОИСК

### 4.1 **Hunter.io Email Finder**
- **Назначение**: Поиск и верификация email адресов
- **URL**: https://hunter.io/api
- **Бесплатный уровень**: 50 поисков/месяц
- **Автентификация**: Требуется API ключ
- **Интеграция**:
```python
import requests
domain = "example.com"
api_key = "YOUR_API_KEY"
response = requests.get(
    f'https://api.hunter.io/v2/domain-search?domain={domain}&access_key={api_key}'
)
```

### 4.2 **Clearbit Email Finder**
- **Назначение**: Email поиск и верификация
- **URL**: https://clearbit.com/email
- **Бесплатный уровень**: 100 запросов/месяц
- **Автентификация**: Требуется API ключ
- **Интеграция**: REST API для поиска email

### 4.3 **RocketReach API**
- **Назначение**: Поиск контактов, включая email
- **URL**: https://rocketreach.co/api
- **Бесплатный уровень**: Пробный период с ограничениями
- **Автентификация**: Требуется API ключ

### 4.4 **EmailRep.io**
- **Назначение**: Репутация и проверка email
- **URL**: https://emailrep.io
- **Бесплатный уровень**: 100 запросов/день - БЕЗ КЛЮЧА
- **Автентификация**: Необязательно
- **Интеграция**:
```python
import requests
email = "example@gmail.com"
response = requests.get(f'https://emailrep.io/{email}')
data = response.json()
print(f"Репутация: {data['reputation']}")
```

### 4.5 **TheHarvester (Tool)**
- **Назначение**: Инструмент для сбора email и другой информации
- **URL**: https://github.com/laramies/theHarvester
- **Бесплатный уровень**: Полностью бесплатно и open-source
- **Автентификация**: Не требуется (использует публичные источники)
- **Интеграция**: Python библиотека для интеграции
```bash
pip install theharvester
python3 -m theHarvester -d example.com -b google
```

---

## 5. УТЕЧКИ ДАННЫХ И BREACH LOOKUP

### 5.1 **HaveIBeenPwned API**
- **Назначение**: Проверка скомпрометированных email и паролей
- **URL**: https://haveibeenpwned.com/API/v3
- **Бесплатный уровень**: Полностью свободно для личного использования
- **Лимиты**: 1 запрос/каждую секунду
- **Автентификация**: Требуется User-Agent
- **Интеграция**:
```python
import requests
email = "test@example.com"
headers = {'User-Agent': 'MyOSINTTool/1.0'}
url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}'
response = requests.get(url, headers=headers)
```

### 5.2 **PwnedPasswordsDownloader (HIBP Passwords)**
- **Назначение**: Загрузка скомпрометированных паролей
- **URL**: https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader
- **Бесплатный уровень**: Полностью свободно
- **Автентификация**: Не требуется
- **Интеграция**: Используйте локальную базу для проверки паролей

### 5.3 **LeaksDB**
- **Назначение**: База данных утечек информации
- **URL**: https://leaksdb.com
- **Бесплатный уровень**: Ограниченный доступ
- **Автентификация**: Требуется регистрация

### 5.4 **DBCan (Deprecated - Альтернативы)**
- **Альтернативы**:
  - BreachDirectory: https://breachdirectory.org
  - Dehashed: https://www.dehashed.com (Частично бесплатно)
  - IntelX: https://intelx.io (Частично бесплатно)

---

## 6. ПОИСК ПО ЛЮДЯМ И СОЦИАЛЬНЫМ СЕТЯМ

### 6.1 **Sherlock (OSINT Tool)**
- **Назначение**: Поиск username во всех соцсетях
- **URL**: https://github.com/sherlock-project/sherlock
- **Бесплатный уровень**: Полностью open-source
- **Автентификация**: Не требуется
- **Интеграция**:
```bash
pip install sherlock-project
sherlock username
```
- **Поддерживаемые сайты**: 400+ соцсетей и сайтов

### 6.2 **SHODAN API**
- **Назначение**: Поиск устройств в интернете (включая люди за ними)
- **URL**: https://shodan.io/api
- **Бесплатный уровень**: 1 ключ, 1 кредит/месяц
- **Автентификация**: Требуется API ключ
- **Интеграция**: API для поиска по IP, hostname, etc.

### 6.3 **Pipl/Clearbit (Person Search)**
- **Назначение**: Поиск информации о человеке
- **URL**: https://pipl.com/api
- **Бесплатный уровень**: Демонстрационный API
- **Автентификация**: Требуется API ключ

### 6.4 **Instagram/TikTok/VK API (Ограничения)**
- **Назначение**: Поиск в соцсетях
- **Ограничения**: Большинство соцсетей не предоставляют free API
- **Альтернативы**: Используйте Sherlock или веб-скрейпинг (с осторожностью)

### 6.5 **Google Custom Search API**
- **Назначение**: Поиск информации в интернете
- **URL**: https://developers.google.com/custom-search/docs/overview
- **Бесплатный уровень**: 100 запросов/день - БЕСПЛАТНО
- **Интеграция**: Python client library

---

## 7. ДОМЕН И WHOIS LOOKUP

### 7.1 **WHOIS Lookup APIs (Free)**
- **WhoisXML API**: https://www.whoisxmlapi.com
  - Бесплатный уровень: 500 запросов/месяц
  - Интеграция: REST API
  
- **DomainDB**: https://domaindb.info
  - Бесплатный уровень: Полностью свободно для базового поиска
  - Интеграция: REST API

- **Bulk WHOIS**: https://bulkwhois.com
  - Бесплатный уровень: 5 запросов/день (без ключа)
  - Интеграция: API + веб-интерфейс

### 7.2 **DNS Lookup и Certificate Search**
- **DNSDumpster**: https://dnsdumpster.com
  - Бесплатный уровень: Полностью свободно
  - Интеграция: Веб-интерфейс + API
  
- **SSL Certificate Transparency**: 
  - https://crt.sh - Поиск по сертификатам, совершенно свободно
  - Интеграция:
```python
import requests
domain = "example.com"
response = requests.get(f'https://crt.sh/?q={domain}&output=json')
```

### 7.3 **URLhaus**
- **Назначение**: Поиск вредоносных доменов
- **URL**: https://urlhaus.abuse.ch/api/
- **Бесплатный уровень**: Полностью свободно
- **Интеграция**: REST API

---

## 8. РУССКОЯЗЫЧНЫЕ API И СЕРВИСЫ

### 8.1 **VK API (VKontakte)**
- **Назначение**: Поиск пользователей и информации
- **URL**: https://dev.vk.com/ru/api
- **Бесплатный уровень**: Ограничен лимитами, требуется регистрация
- **Лимиты**: 500 запросов/сек
- **Автентификация**: Требуется токен
- **Интеграция**:
```python
import requests
token = "YOUR_VK_TOKEN"
params = {'v': '5.131', 'access_token': token}
response = requests.get('https://api.vk.com/method/users.search', params=params)
```

### 8.2 **Yandex APIs**
- **Yandex Maps API**: Геокодирование, маршруты, места
  - URL: https://yandex.ru/dev/maps/
  - Лимиты: 50,000 запросов/день
  
- **Yandex Metrica API**: Аналитика трафика
  - URL: https://yandex.ru/dev/metrica/

### 8.3 **2GIS API (ДваГиса)**
- **Назначение**: Поиск мест, эталоны, контакты, часы
- **URL**: https://2gis.com/api
- **Бесплатный уровень**: Требуется регистрация API ключа
- **Лимиты**: 200 запросов/сек
- **Интеграция**: REST API

### 8.4 **OKapi (Mail.ru API)**
- **Назначение**: Поиск пользователей в Одноклассниках
- **URL**: https://ok.ru/dev/
- **Бесплатный уровень**: Требуется регистрация и одобрение
- **Лимиты**: Ограниченные расценки

### 8.5 **RostelecomTariffs (Базы операторов)**
- **Назначение**: Проверка оператора по номеру телефона
- **URL**: https://github.com/russianpost/russia-post-api (разные источники)
- **Интеграция**: Locale разработка с использованием открытых данных

---

## 9. PROXY И VPN API (Для OSINT исследований)

### 9.1 **ProxyList APIs**
- **FreeProxyList**: https://www.freeproxylists.net/api/
  - Бесплатный уровень: Полностью свободно
  - Интеграция: JSON API
  
- **Proxy-List**: https://github.com/clarketm/proxy-list
  - Бесплатный уровень: Open-source список прокси
  - Интеграция: CSV/JSON файлы

### 9.2 **RapidAPI Proxy Services**
- **URL**: https://rapidapi.com
- **Бесплатный уровень**: 5,000 запросов/месяц
- **Описание**: Лучший конце для доступа к 1000+ API с одной подписки

---

## 10. СПЕЦИАЛИЗИРОВАННЫЕ OSINT API И ИНСТРУМЕНТЫ

### 10.1 **URLhaus API (Malware Detection)**
- **Назначение**: Проверка вредоносных URL
- **URL**: https://urlhaus.abuse.ch/api/
- **Бесплатный уровень**: Полностью свободно, без ограничений
- **Интеграция**:
```python
import requests
url = "http://example.com"
response = requests.post('https://urlhaus-api.abuse.ch/v1/url/', data={'url': url})
```

### 10.2 **VirusTotal API**
- **Назначение**: Сканирование файлов и URL на вирусы
- **URL**: https://www.virustotal.com/api/
- **Бесплатный уровень**: 600 запросов/мин, 4 запроса/сек
- **Автентификация**: Требуется API ключ
- **Интеграция**:
```python
import requests
url = "http://example.com"
headers = {'x-apikey': 'YOUR_API_KEY'}
response = requests.get(
    'https://www.virustotal.com/api/v3/domain_info',
    params={'domain': url}, headers=headers
)
```

### 10.3 **AbuseIPDB**
- **Назначение**: Проверка репутации IP адреса
- **URL**: https://www.abuseipdb.com/api
- **Бесплатный уровень**: 1,000 запросов/день
- **Автентификация**: Требуется API ключ
- **Интеграция**:
```python
import requests
ip = "8.8.8.8"
api_key = "YOUR_API_KEY"
response = requests.get(
    'https://api.abuseipdb.com/api/v2/check',
    params={'ipAddress': ip},
    headers={'Key': api_key}
)
```

### 10.4 **Censys API**
- **Назначение**: Поиск интернет-хостов и сертификатов
- **URL**: https://censys.io/api
- **Бесплатный уровень**: 120 квоты запросов/час
- **Автентификация**: Требуется регистрация

---

## 11. ДОПОЛНИТЕЛЬНЫЕ ПОЛЕЗНЫЕ API

### 11.1 **Nominatim (OpenStreetMap)**
- **Назначение**: Геокодирование и обратное геокодирование
- **URL**: https://nominatim.org/
- **Бесплатный уровень**: Полностью свободно (с лимитом 1 запрос/сек)
- **Интеграция**:
```python
import requests
response = requests.get(
    'https://nominatim.openstreetmap.org/search',
    params={'q': 'New York', 'format': 'json'}
)
```

### 11.2 **OpenWeather API**
- **Назначение**: Погода и координаты (для контекста)
- **URL**: https://openweathermap.org/api
- **Бесплатный уровень**: 1,000 запросов/день
- **Автентификация**: Требуется API ключ

### 11.3 **DBpedia**
- **Назначение**: Открытая база знаний
- **URL**: https://www.dbpedia.org/
- **Бесплатный уровень**: Полностью свободно
- **Интеграция**: SPARQL запросы

---

## 12. КОЛЛЕКЦИИ API КЛЮЧЕЙ И РЕСУРСОВ

### 12.1 **Awesome APIs Collections**
- **GitHub**: https://github.com/topics/awesome-api
- **Содержит**: Сотни ссылок на свободные API

### 12.2 **RapidAPI Hub**
- **URL**: https://rapidapi.com
- **Содержит**: 10,000+ API с документацией
- **Фильтр**: Можно искать по "free" и "OSINT"

### 12.3 **OpenCorporates API**
- **Назначение**: Ищи компании и директоров
- **URL**: https://opencorporates.com/api
- **Бесплатный уровень**: 2 запроса/сек
- **Интеграция**: REST API

---

## 13. ИНТЕГРАЦИЯ В PHONE LOOKUP OSINT ИНСТРУМЕНТ

### Рекомендуемая архитектура:

```python
# phone_osint_full.py
import requests
import json
from datetime import datetime

class OSINTPhoneLookup:
    def __init__(self):
        self.config = {
            'numverify_key': 'YOUR_NUMVERIFY_KEY',
            'hunter_key': 'YOUR_HUNTER_KEY',
            'emailrep_enabled': True,
            'hibp_enabled': True,
            'shodan_key': 'YOUR_SHODAN_KEY'
        }
    
    def lookup_phone(self, phone_number):
        """Основной метод для поиска по телефону"""
        results = {}
        
        # 1. Валидация номера через numverify
        results['phone_validation'] = self._validate_phone(phone_number)
        
        # 2. Поиск владельца через социальные сигналы
        results['social_signals'] = self._search_social_signals(phone_number)
        
        # 3. Проверка утечек данных
        results['breach_check'] = self._check_breaches(phone_number)
        
        # 4. Геолокация (если доступен IP)
        if results.get('social_signals', {}).get('ip'):
            results['geolocation'] = self._geolocate_ip(
                results['social_signals']['ip']
            )
        
        return results
    
    def _validate_phone(self, phone):
        """Используйте NumVerify API"""
        # Код для валидации
        pass
    
    def _search_social_signals(self, phone):
        """Комбо: Hunter + Sherlock + EmailRep"""
        # Поиск через email + социальные сети
        pass
    
    def _check_breaches(self, identifier):
        """Используйте HaveIBeenPwned API"""
        # Проверка утечек
        pass
    
    def _geolocate_ip(self, ip):
        """Используйте IP-API для геолокации"""
        # Геолокация по IP
        pass

# Использование
osint = OSINTPhoneLookup()
results = osint.lookup_phone("+1234567890")
print(json.dumps(results, indent=2))
```

### Приоритет интеграции:

1. **Основной функционал** (обязательные):
   - NumVerify для валидации телефона
   - IP-API для геолокации
   - HaveIBeenPwned для проверки утечек

2. **Расширенные функции** (рекомендуется):
   - Hunter/Clearbit для email поиска
   - EmailRep для проверки email репутации
   - Sherlock для поиска по соцсетям
   - VirusTotal для проверки безопасности

3. **Дополнительные функции** (опционально):
   - WHOIS для информации о домене
   - Censys для поиска хостов
   - AbuseIPDB для репутации IP

---

## 14. ВАЖНЫЕ ЗАМЕЧАНИЯ И ОГРАНИЧЕНИЯ

### 14.1 Юридические ограничения:
- ✅ **Разрешено**: Сбор публичной информации
- ⚠️ **С осторожностью**: Проверка email/телефонов (может быть нарушением приватности)
- ❌ **Запрещено**: Получение информации без согласия, взлом, социальная инженерия

### 14.2 Лучшие практики:
- Соблюдайте rate limits API
- Используйте кэширование для сокращения запросов
- Обрабатывайте ошибки и таймауты
- Используйте User-Agent заголовки
- Логируйте все запросы для аудита

### 14.3 Альтернативные методы без API:
- Веб-скрейпинг (с осторожностью и уважением к robots.txt)
- OSINT Framework: https://osintframework.com
- Intelx: https://intelx.io (частично бесплатно)
- Maltego Community Edition

---

## 15. БЫСТРЫЙ СТАРТ: РЕКОМЕНДУЕМЫЕ ПЕРВЫЕ ШАГИ

1. **Скачайте основные tools**:
   ```bash
   pip install sherlock-project
   pip install theharvester
   pip install requests
   ```

2. **Зарегистрируйте бесплатные API ключи**:
   - HaveIBeenPwned (на этот нет)
   - IP-API (на этот нет)
   - NumVerify
   - Hunter

3. **Клонируйте полезные репозитории**:
   ```bash
   git clone https://github.com/public-apis/public-apis.git
   git clone https://github.com/sherlock-project/sherlock.git
   git clone https://github.com/jivoi/awesome-osint.git
   ```

4. **Создайте конфиг файл** с API ключами и включите интеграцию

---

## Ресурсы для дальнейшего изучения:

- OSINT Framework: https://osintframework.com
- OSINT Curious: https://osintcurio.us/
- OSINT Techniques (Book): https://osint.expose/
- r/OSINT: https://reddit.com/r/OSINT/
- 0INT.com: https://0int.com/
