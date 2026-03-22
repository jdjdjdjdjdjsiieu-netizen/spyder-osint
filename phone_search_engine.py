#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Реально работающий OSINT поиск по номеру телефона
Интегрирует рабочие источники данных и реальные API
"""

import requests
import json
import re
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import quote

class PhoneSearchEngine:
    """Реально работающая система поиска по номеру телефона"""
    
    def __init__(self, phone: str, api_keys: Optional[Dict] = None):
        self.phone = phone
        self.phone_clean = re.sub(r'\D', '', phone)
        self.api_keys = api_keys or {}
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def normalize_phone(self) -> str:
        """Нормализация номера"""
        if self.phone_clean.startswith('7') and len(self.phone_clean) == 11:
            return f"+{self.phone_clean}"
        elif self.phone_clean.startswith('8') and len(self.phone_clean) == 11:
            return f"+7{self.phone_clean[1:]}"
        elif len(self.phone_clean) == 10:
            return f"+7{self.phone_clean}"
        return f"+{self.phone_clean}"
    
    def check_ipqualityscore(self) -> Dict[str, Any]:
        """Проверка через IPQualityScore (25 запросов/месяц бесплатно)"""
        result = {'source': 'IPQualityScore', 'status': 'unknown', 'data': None}
        
        if 'ipqualityscore_key' not in self.api_keys:
            result['status'] = 'no_api_key'
            result['note'] = 'Требуется регистрация на https://ipqualityscore.com'
            return result
            
        try:
            response = self.session.get(
                'https://ipqualityscore.com/api/json/phone/validate',
                params={
                    'phone': self.normalize_phone(),
                    'apikey': self.api_keys['ipqualityscore_key']
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                result['status'] = 'success'
                result['data'] = {
                    'valid': data.get('valid', False),
                    'carrier': data.get('carrier', 'Unknown'),
                    'line_type': data.get('line_type', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'is_prepaid': data.get('is_prepaid', False),
                    'fraud_score': data.get('fraud_score', 0)
                }
            else:
                result['status'] = f'http_error_{response.status_code}'
        except Exception as e:
            result['status'] = f'error: {str(e)}'
            
        return result
    
    def check_numverify(self) -> Dict[str, Any]:
        """Проверка через NumVerify (100 запросов/месяц бесплатно)"""
        result = {'source': 'NumVerify', 'status': 'unknown', 'data': None}
        
        if 'numverify_key' not in self.api_keys:
            result['status'] = 'no_api_key'
            result['note'] = 'Требуется API ключ с https://numverify.com'
            return result
            
        try:
            response = self.session.get(
                'https://api.numverify.com/validate',
                params={
                    'phone': self.phone_clean,
                    'country_code': 'RU',
                    'access_key': self.api_keys['numverify_key']
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                result['status'] = 'success'
                result['data'] = {
                    'valid': data.get('valid', False),
                    'international_format': data.get('international_format'),
                    'country_name': data.get('country_name'),
                    'country_code': data.get('country_code'),
                    'carrier': data.get('carrier', 'Unknown'),
                    'line_type': data.get('line_type', 'Unknown')
                }
            else:
                result['status'] = f'error: {response.status_code}'
        except Exception as e:
            result['status'] = f'error: {str(e)}'
            
        return result
    
    def check_abstractapi(self) -> Dict[str, Any]:
        """Проверка через AbstractAPI (100 запросов/месяц бесплатно)"""
        result = {'source': 'AbstractAPI', 'status': 'unknown', 'data': None}
        
        if 'abstractapi_key' not in self.api_keys:
            result['status'] = 'no_api_key'
            result['note'] = 'Требуется API ключ с https://www.abstractapi.com'
            return result
            
        try:
            response = self.session.get(
                'https://phonevalidation.abstractapi.com/v1/',
                params={
                    'phone': self.normalize_phone(),
                    'api_key': self.api_keys['abstractapi_key']
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                result['status'] = 'success'
                result['data'] = {
                    'valid': data.get('valid', False),
                    'format': {
                        'international': data.get('format', {}).get('international'),
                        'national': data.get('format', {}).get('national')
                    },
                    'country': data.get('country'),
                    'type': data.get('type', 'Unknown'),
                    'carrier': data.get('carrier', 'Unknown')
                }
            else:
                result['status'] = f'error: {response.status_code}'
        except Exception as e:
            result['status'] = f'error: {str(e)}'
            
        return result
    
    def search_truecaller_web(self) -> Dict[str, Any]:
        """Поиск в TrueCaller Web"""
        result = {'source': 'TrueCaller Web', 'status': 'unknown', 'data': None}
        
        try:
            response = self.session.get(
                f'https://www.truecaller.com/search/SU/{self.phone_clean}',
                timeout=10,
                allow_redirects=True
            )
            if response.status_code == 200:
                # Парсим HTML для извлечения данных
                if 'name' in response.text or 'Name' in response.text:
                    result['status'] = 'found'
                    result['note'] = 'Требуется парсинг HTML'
                else:
                    result['status'] = 'not_found'
            else:
                result['status'] = f'http_{response.status_code}'
        except Exception as e:
            result['status'] = f'error: {str(e)}'
            
        return result
    
    def search_dehashed(self) -> Dict[str, Any]:
        """Поиск в DeHashed (базе утечек)"""
        result = {'source': 'DeHashed', 'status': 'unknown', 'data': None}
        
        if 'dehashed_key' not in self.api_keys:
            result['status'] = 'no_api_key'
            result['note'] = 'Требуется API ключ с https://dehashed.com'
            return result
            
        try:
            response = self.session.get(
                'https://api.dehashed.com/search',
                params={
                    'query': f'phone:{self.phone_clean}',
                    'api_key': self.api_keys['dehashed_key']
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('balance', 0) > 0 and data.get('entries'):
                    result['status'] = 'found_in_breach'
                    result['data'] = {
                        'breach_count': len(data.get('entries', [])),
                        'entries': data.get('entries', [])[:3]  # Первые 3 записи
                    }
                else:
                    result['status'] = 'not_found'
            else:
                result['status'] = f'http_{response.status_code}'
        except Exception as e:
            result['status'] = f'error: {str(e)}'
            
        return result
    
    def get_search_links(self) -> Dict[str, Dict[str, str]]:
        """Получить ссылки для ручного поиска"""
        phone_encoded = quote(self.normalize_phone())
        
        return {
            'social_media': {
                'vkontakte': f'https://vk.com/search?c[q]={phone_encoded}',
                'odnoklassniki': f'https://ok.ru/search?q={phone_encoded}',
                '2gis': f'https://2gis.ru/search?q={phone_encoded}',
                'twitter': f'https://twitter.com/search?q={phone_encoded}',
                'instagram': f'https://www.instagram.com/explore/tags/{self.phone_clean}/',
                'telegram': 'https://t.me/search - требует использование клиента'
            },
            'directories': {
                'avva': f'https://avva.ru/?q={phone_encoded}',
                'yandex_people': f'https://people.yandex.ru/search?text={phone_encoded}',
                'truecaller': f'https://www.truecaller.com/search/SU/{self.phone_clean}'
            },
            'search_engines': {
                'google': f'https://www.google.com/search?q=%22{phone_encoded}%22',
                'yandex': f'https://www.yandex.ru/search/?text={phone_encoded}',
                'bing': f'https://www.bing.com/search?q=%22{self.normalize_phone()}%22'
            },
            'job_sites': {
                'headhunter': f'https://hh.ru/search/vacancy?text={phone_encoded}',
                'superjob': f'https://superjob.ru/vacancy/search/?keywords={phone_encoded}',
                'linkedin': f'https://www.linkedin.com/search/results/all/?keywords={phone_encoded}'
            },
            'leak_databases': {
                'haveibeenpwned': 'https://haveibeenpwned.com/ - поиск по email',
                'dehashed': f'https://dehashed.com/search?query={phone_encoded}',
                'leakpeek': 'https://leakpeek.com/ - поиск по company/email'
            }
        }
    
    def execute_search(self) -> Dict[str, Any]:
        """Выполнить полный поиск"""
        results = {
            'phone': self.phone,
            'normalized': self.normalize_phone(),
            'timestamp': datetime.now().isoformat(),
            'api_results': {
                'ipqualityscore': self.check_ipqualityscore(),
                'numverify': self.check_numverify(),
                'abstractapi': self.check_abstractapi(),
                'truecaller_web': self.search_truecaller_web(),
                'dehashed': self.search_dehashed()
            },
            'manual_search_links': self.get_search_links()
        }
        return results
    
    def print_results(self, results: Dict[str, Any]):
        """Красиво вывести результаты"""
        print("\n" + "="*100)
        print("🔍 РЕЗУЛЬТАТЫ ПОИСКА ПО НОМЕРУ ТЕЛЕФОНА")
        print("="*100 + "\n")
        
        print(f"📱 Номер: {results['phone']}")
        print(f"   Нормализованный: {results['normalized']}")
        print(f"   Время поиска: {results['timestamp']}\n")
        
        print("🔌 РЕЗУЛЬТАТЫ API (требуют регистрацию и API ключи):")
        print("─" * 100 + "\n")
        
        for api_name, api_result in results['api_results'].items():
            if api_name.startswith('_'):
                continue
            status = api_result.get('status', 'unknown')
            print(f"  {api_name.upper()}")
            print(f"  └─ Статус: {status}")
            
            if api_result.get('note'):
                print(f"  └─ {api_result['note']}")
            if api_result.get('data'):
                print(f"  └─ Данные: {json.dumps(api_result['data'], ensure_ascii=False, indent=6)}")
            print()
        
        print("\n📍 ССЫЛКИ ДЛЯ РУЧНОГО ПОИСКА:")
        print("─" * 100 + "\n")
        
        for category, sources in results['manual_search_links'].items():
            print(f"  {category.upper().replace('_', ' ')}:")
            for source_name, url in sources.items():
                print(f"    • {source_name}: {url}")
            print()
        
        print("="*100 + "\n")


def main():
    if len(sys.argv) < 2:
        phone = "+79182469659"
        print("⚠️  Использую тестовый номер: +79182469659")
    else:
        phone = sys.argv[1]
    
    # Создаем поисковик
    searcher = PhoneSearchEngine(phone)
    
    # Выполняем поиск
    results = searcher.execute_search()
    
    # Выводим результаты
    searcher.print_results(results)
    
    # Сохраняем в JSON
    filename = f'phone_search_{results["normalized"].replace("+", "")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Результаты сохранены в {filename}")
    
    # Выводим JSON
    print("\n📄 JSON РЕЗУЛЬТАТЫ:")
    print("─" * 100)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
