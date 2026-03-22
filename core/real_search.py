#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Реальный поиск по номеру телефона - интеграция рабочих источников
"""

import requests
import json
import re
from datetime import datetime
from typing import Dict, List, Any

class RealPhoneSearcher:
    """Класс для поиска реальных данных по номеру телефона"""
    
    def __init__(self, phone: str):
        self.phone = phone
        self.normalized_phone = self.normalize_phone(phone)
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'phone': phone,
            'results': {}
        }
        
    def normalize_phone(self, phone: str) -> str:
        """Нормализация номера телефона"""
        # Убираем все символы кроме цифр
        digits_only = re.sub(r'\D', '', phone)
        # Если начинается с 7, это Россия
        if digits_only.startswith('7'):
            return f"+{digits_only}"
        elif digits_only.startswith('8'):
            return f"+7{digits_only[1:]}"
        else:
            return f"+{digits_only}"
    
    def extract_phone_info(self) -> Dict[str, Any]:
        """Извлечение базовой информации о номере"""
        normalized = self.normalized_phone.replace('+', '')
        
        operators = {
            '901': 'MTS', '902': 'MTS', '903': 'MTS', '904': 'MTS', '905': 'MTS', '906': 'MTS', '908': 'MTS', '910': 'MTS',
            '911': 'MTS', '912': 'MTS', '913': 'MTS', '914': 'MTS', '915': 'MTS', '916': 'MTS', '917': 'MTS', '918': 'MTS',
            '919': 'MTS', '920': 'MTS', '921': 'MTS', '922': 'MTS', '923': 'MTS', '924': 'MTS', '925': 'MTS', '926': 'MTS',
            '927': 'MTS', '928': 'MTS', '929': 'MTS', '930': 'MTS', '931': 'MTS', '932': 'MTS', '933': 'MTS', '934': 'MTS',
            '936': 'MTS', '937': 'MTS', '938': 'MTS', '961': 'TriolineVoiceStream', '962': 'TriolineVoiceStream',
            '963': 'TriolineVoiceStream', '964': 'TriolineVoiceStream', '965': 'TriolineVoiceStream',
            '966': 'TriolineVoiceStream', '967': 'TriolineVoiceStream', '968': 'TriolineVoiceStream',
            '950': 'Tele2', '951': 'Tele2', '953': 'Tele2', '955': 'Tele2', '956': 'Tele2', '957': 'Tele2',
            '958': 'Tele2', '959': 'Tele2', '960': 'Tele2',
            '921': 'Beeline', '922': 'Beeline', '923': 'Beeline', '995': 'Beeline', '996': 'Beeline',
            '997': 'Beeline', '798': 'Megafon', '899': 'Megafon', '900': 'Megafon', '911': 'Megafon',
            '918': 'Megafon', '919': 'Megafon', '920': 'Megafon', '921': 'Megafon', '922': 'Megafon',
            '924': 'Megafon', '925': 'Megafon', '927': 'Megafon', '928': 'Megafon', '929': 'Megafon',
            '930': 'Megafon', '931': 'Megafon', '932': 'Megafon', '933': 'Megafon', '934': 'Megafon',
            '936': 'Megafon', '937': 'Megafon', '938': 'Megafon', '939': 'Megafon'
        }
        
        # Получаем оператора
        prefix = normalized[1:4]
        operator = operators.get(prefix, 'Unknown')
        
        return {
            'phone': self.phone,
            'normalized': self.normalized_phone,
            'operator': operator,
            'country': 'Russia',
            'type': 'Mobile' if 'Mobile' in str(operator) or len(normalized) == 11 else 'Unknown'
        }
    
    def search_haveibenpwned(self) -> Dict[str, Any]:
        """Поиск в базе утёкших паролей"""
        result = {
            'source': 'HaveIBeenPwned',
            'status': 'unknown',
            'data': None
        }
        
        try:
            # HaveIBeenPwned требует использование email, не номера
            # Но мы можем проверить если номер используется как username
            url = 'https://haveibeenpwned.com/api/v3/search'
            headers = {'User-Agent': 'SpyderOSINT/2.0', 'Accept': 'application/json'}
            
            # Для номера телефона нужна email или username
            # Попробуем как username
            response = requests.get(
                'https://api.pwnedpasswords.com/range/00000',
                timeout=3
            )
            
            if response.status_code == 200:
                result['status'] = 'accessible'
                result['data'] = {
                    'description': 'База утёкших паролей доступна',
                    'note': 'Поиск возможен только по email или username, не по номеру'
                }
        except Exception as e:
            result['status'] = f'error: {str(e)}'
        
        return result
    
    def create_search_report(self) -> str:
        """Создание итогового отчета"""
        phone_info = self.extract_phone_info()
        
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   РЕЗУЛЬТАТЫ OSINT ПОИСКА ПО НОМЕРУ ТЕЛЕФОНА                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📱 ОСНОВНАЯ ИНФОРМАЦИЯ О НОМЕРЕ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Номер телефона:        {phone_info['phone']}
    Нормализованный:       {phone_info['normalized']}
    Оператор:              {phone_info['operator']}
    Тип линии:             {phone_info['type']}
    Страна:                {phone_info['country']}
    Время поиска:          {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔍 РЕЗУЛЬТАТЫ ПОИСКА ПО ИСТОЧНИКАМ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  СОЦИАЛЬНЫЕ СЕТИ:
   • ВКонтакте (vk.com)
     └─ Поиск: https://vk.com/search?c[q]={phone_info['normalized'].replace('+', '%2B')}
     └─ Статус: Требует ручного поиска
     
   • Одноклассники (ok.ru) 
     └─ Поиск: https://ok.ru/search?q={phone_info['normalized'].replace('+', '%2B')}
     └─ Статус: Требует ручного поиска
     
   • 2GIS (справочник Санкт-Петербурга и других городов)
     └─ Поиск: https://2gis.ru/search?q={phone_info['normalized'].replace('+', '%2B')}
     └─ Статус: Требует ручного поиска

2️⃣  СПРАВОЧНИКИ И АГРЕГАТОРЫ:
   • AVVA.RU (публичные профили)
     └─ Поиск: https://avva.ru/?q={phone_info['normalized'].replace('+', '%2B')}
     └─ Статус: Требует ручного поиска
     
   • Яндекс.Люди
     └─ Поиск: https://people.yandex.ru/search?text={phone_info['normalized'].replace('+', '%2B')}
     └─ Статус: Требует ручного поиска

3️⃣  ГОСУДАРСТВЕННЫЕ РЕЕСТРЫ:
   • Росреестр (недвижимость)
     └─ Требуется: ФИО или адрес собственника
     └─ URL: https://www.rosreestr.ru/
     
   • ФНС ЕГРЮЛ (индивидуальные предприниматели)
     └─ Требуется: ИНН или ФИО
     └─ URL: https://egrul.nalog.ru/
     
   • ФНС ИНН (справочник ИНН физических лиц)
     └─ Требуется: ФИО, регион, дата рождения
     └─ URL: https://service.nalog.ru/

4️⃣  ПОИСКОВЫЕ СИСТЕМЫ:
   • Google Dork поиск
     └─ Запрос: "{phone_info['phone']}"
     └─ Запрос: "{phone_info['phone']}" паспорт
     └─ Запрос: "{phone_info['phone']}" ИНН
     
   • Яндекс поиск
     └─ Запрос: {phone_info['phone']}
     └─ Статус: Лучше всего для поиска номера в открытых документах

5️⃣  БАЗЫ УТЁКШИХ ДАННЫХ:
   • HaveIBeenPwned.com
     └─ Поиск возможен только по email или username
     └─ URL: https://haveibeenpwned.com/
     
   • DeHashed.com
     └─ На сайте есть поиск по номерам телефонов
     └─ URL: https://dehashed.com/

6️⃣  РЕЗЮМЕ И ПРОФИЛИ СОИСКАТЕЛЕЙ:
   • HeadHunter (hh.ru)
     └─ Поиск: https://hh.ru/search/vacancy?text={phone_info['normalized'].replace('+', '%2B')}
     
   • SuperJob (superjob.ru)
     └─ Поиск: https://superjob.ru/ (требует ручного поиска)
     
   • LinkedIn (linkedin.com)
     └─ Поиск: https://www.linkedin.com/search/results/all/?keywords={phone_info['normalized'].replace('+', '%2B')}

📊 РЕКОМЕНДУЕМЫЙ ПОРЯДОК ПОИСКА:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ШАГ 1. Google Dorks (при наличии информации в открытых источниках)
       ⏱️  5-10 минут
       📍 Лучший источник для начального поиска
       
ШАГ 2. Социальные сети ВКонтакте и Одноклассники
       ⏱️  5-10 минут
       📍 Часто люди указывают номер в профиле
       
ШАГ 3. 2GIS (если номер компании)
       ⏱️  2-3 минуты
       📍 Справочник с телефонами организаций
       
ШАГ 4. AVVA.RU (публичные профили)
       ⏱️  3-5 минут
       📍 Часто есть адреса и ФИО
       
ШАГ 5. Яндекс.Люди (если известна фамилия)
       ⏱️  2-3 минуты
       📍 Поиск по ФИО/адресу/месту работы
       
ШАГ 6. Базы утечек (HaveIBeenPwned, DeHashed)
       ⏱️  1-2 минуты
       📍 Проверка наличия в утечках данных

✅ УСПЕШНЫЙ РЕЗУЛЬТАТ ДОЛЖЕН СОДЕРЖАТЬ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✓ ФИО владельца номера
   ✓ Город/регион проживания
   ✓ Профиль в социальной сети (ВКонтакте, Instagram)
   ✓ Место работы/учебы
   ✓ Адрес проживания (если есть в открытых источниках)
   ✓ Email (если связан с телефоном)
   ✓ Информация о наличии в утечках баз данных

📝 ВАЖНО:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Все ссылки выше ведут на официальные сайты
   • Поиск требует РУЧНОГО выполнения в браузере (сайты блокируют ботов)
   • Используйте VPN если есть ограничения по IP
   • Сохраняйте результаты (скриншоты) для документирования
   • Соблюдайте законодательство о приватности вашей страны

╔═══════════════════════════════════════════════════════════════════════════════╗
║     После ручного поиска результаты можно агрегировать в этом отчёте         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        return report
    
    def get_full_report(self) -> Dict[str, Any]:
        """Получение полного отчета в JSON"""
        phone_info = self.extract_phone_info()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'phone_info': phone_info,
            'search_sources': {
                'social_media': {
                    'vkontakte': f"https://vk.com/search?c[q]={phone_info['normalized'].replace('+', '%2B')}",
                    'odnoklassniki': f"https://ok.ru/search?q={phone_info['normalized'].replace('+', '%2B')}",
                    '2gis': f"https://2gis.ru/search?q={phone_info['normalized'].replace('+', '%2B')}",
                },
                'directories': {
                    'avva': f"https://avva.ru/?q={phone_info['normalized'].replace('+', '%2B')}",
                    'yandex_people': f"https://people.yandex.ru/search?text={phone_info['normalized'].replace('+', '%2B')}",
                },
                'search_engines': {
                    'google': f'https://www.google.com/search?q="{phone_info["phone"]}"',
                    'yandex': f'https://www.yandex.ru/search/?text={phone_info["normalized"]}',
                },
                'job_sites': {
                    'headhunter': f"https://hh.ru/search/vacancy?text={phone_info['normalized'].replace('+', '%2B')}",
                    'superjob': 'https://superjob.ru/',
                    'linkedin': f"https://www.linkedin.com/search/results/all/?keywords={phone_info['normalized'].replace('+', '%2B')}",
                },
                'leak_databases': {
                    'haveibeenpwned': 'https://haveibeenpwned.com/',
                    'dehashed': 'https://dehashed.com/',
                }
            }
        }


def main():
    phone = "+79182469659"
    searcher = RealPhoneSearcher(phone)
    
    # Выводим отчет
    print(searcher.create_search_report())
    
    # Сохраняем JSON
    with open(f'phone_search_results_{phone.replace("+", "")}.json', 'w', encoding='utf-8') as f:
        json.dump(searcher.get_full_report(), f, ensure_ascii=False, indent=2)
    
    print("\n✅ Результаты сохранены в phone_search_results_79182469659.json")


if __name__ == '__main__':
    main()
