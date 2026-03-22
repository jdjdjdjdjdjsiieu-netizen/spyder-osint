#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Расширенный OSINT поиск по номеру телефона
Поддерживает все возможные форматы: +7, 8, 79182469659, и т.д.
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Set, Tuple
from urllib.parse import quote

class PhoneFormatConverter:
    """Конвертирует номер телефона в различные форматы"""
    
    def __init__(self, phone: str):
        self.original = phone
        self.clean = self._extract_digits(phone)
        self.formats = self._generate_all_formats()
    
    def _extract_digits(self, phone: str) -> str:
        """Извлечь только цифры"""
        return re.sub(r'\D', '', phone)
    
    def _generate_all_formats(self) -> Dict[str, List[str]]:
        """Генерировать все возможные форматы номера"""
        clean = self.clean
        
        # Базовые форматы
        formats = {
            'international': [],
            'russianPrefix8': [],
            'withoutPrefix': [],
            'formatted_spaces': [],
            'formatted_dashes': [],
            'formatted_dots': [],
            'partial': []
        }
        
        # 1. МЕЖДУНАРОДНЫЙ ФОРМАТ с +7
        if clean.startswith('7') and len(clean) == 11:
            formats['international'].append(f"+{clean}")
            formats['international'].append(f"+{clean[:1]}-{clean[1:4]}-{clean[4:7]}-{clean[7:]}")
            formats['international'].append(f"+{clean[:1]} {clean[1:4]} {clean[4:7]} {clean[7:]}")
        elif clean.startswith('8') and len(clean) == 11:
            clean_7 = '7' + clean[1:]
            formats['international'].append(f"+{clean_7}")
            formats['international'].append(f"+{clean_7[:1]}-{clean_7[1:4]}-{clean_7[4:7]}-{clean_7[7:]}")
            formats['international'].append(f"+{clean_7[:1]} {clean_7[1:4]} {clean_7[4:7]} {clean_7[7:]}")
        elif len(clean) == 10:
            clean_7 = '7' + clean
            formats['international'].append(f"+{clean_7}")
            formats['international'].append(f"+{clean_7[:1]}-{clean_7[1:4]}-{clean_7[4:7]}-{clean_7[7:]}")
            formats['international'].append(f"+{clean_7[:1]} {clean_7[1:4]} {clean_7[4:7]} {clean_7[7:]}")
        
        # 2. ФОРМАТ С 8 (РОССИЙСКИЙ)
        if clean.startswith('7') and len(clean) == 11:
            local_8 = '8' + clean[1:]
            formats['russianPrefix8'].append(local_8)
            formats['russianPrefix8'].append(f"8-{local_8[1:4]}-{local_8[4:7]}-{local_8[7:]}")
            formats['russianPrefix8'].append(f"8 {local_8[1:4]} {local_8[4:7]} {local_8[7:]}")
        elif clean.startswith('8') and len(clean) == 11:
            formats['russianPrefix8'].append(clean)
            formats['russianPrefix8'].append(f"8-{clean[1:4]}-{clean[4:7]}-{clean[7:]}")
            formats['russianPrefix8'].append(f"8 {clean[1:4]} {clean[4:7]} {clean[7:]}")
        elif len(clean) == 10:
            formats['russianPrefix8'].append(f"8{clean}")
            formats['russianPrefix8'].append(f"8-{clean[0:3]}-{clean[3:6]}-{clean[6:]}")
            formats['russianPrefix8'].append(f"8 {clean[0:3]} {clean[3:6]} {clean[6:]}")
        
        # 3. БЕЗ ПРЕФИКСА
        if clean.startswith('7') and len(clean) == 11:
            without = clean[1:]
            formats['withoutPrefix'].append(without)
            formats['withoutPrefix'].append(f"{without[0:3]}-{without[3:6]}-{without[6:]}")
            formats['withoutPrefix'].append(f"{without[0:3]} {without[3:6]} {without[6:]}")
        elif clean.startswith('8') and len(clean) == 11:
            without = clean[1:]
            formats['withoutPrefix'].append(without)
            formats['withoutPrefix'].append(f"{without[0:3]}-{without[3:6]}-{without[6:]}")
            formats['withoutPrefix'].append(f"{without[0:3]} {without[3:6]} {without[6:]}")
        elif len(clean) == 10:
            formats['withoutPrefix'].append(clean)
            formats['withoutPrefix'].append(f"{clean[0:3]}-{clean[3:6]}-{clean[6:]}")
            formats['withoutPrefix'].append(f"{clean[0:3]} {clean[3:6]} {clean[6:]}")
        
        # 4. ФОРМАТИРОВАННЫЕ (ПРОБЕЛЫ)
        if len(clean) == 11:
            if clean.startswith('7'):
                formats['formatted_spaces'].append(f"+7 {clean[1:4]} {clean[4:7]} {clean[7:]}")
            elif clean.startswith('8'):
                formats['formatted_spaces'].append(f"8 {clean[1:4]} {clean[4:7]} {clean[7:]}")
        elif len(clean) == 10:
            formats['formatted_spaces'].append(f"+7 {clean[0:3]} {clean[3:6]} {clean[6:]}")
            formats['formatted_spaces'].append(f"8 {clean[0:3]} {clean[3:6]} {clean[6:]}")
        
        # 5. ФОРМАТИРОВАННЫЕ (ДЕФИСЫ)
        if len(clean) == 11:
            if clean.startswith('7'):
                formats['formatted_dashes'].append(f"+7-{clean[1:4]}-{clean[4:7]}-{clean[7:]}")
            elif clean.startswith('8'):
                formats['formatted_dashes'].append(f"8-{clean[1:4]}-{clean[4:7]}-{clean[7:]}")
        elif len(clean) == 10:
            formats['formatted_dashes'].append(f"+7-{clean[0:3]}-{clean[3:6]}-{clean[6:]}")
            formats['formatted_dashes'].append(f"8-{clean[0:3]}-{clean[3:6]}-{clean[6:]}")
        
        # 6. ФОРМАТИРОВАННЫЕ (ТОЧКИ)
        if len(clean) == 11:
            if clean.startswith('7'):
                formats['formatted_dots'].append(f"+7.{clean[1:4]}.{clean[4:7]}.{clean[7:]}")
            elif clean.startswith('8'):
                formats['formatted_dots'].append(f"8.{clean[1:4]}.{clean[4:7]}.{clean[7:]}")
        
        # 7. ЧАСТИЧНЫЕ ФОРМАТЫ
        if len(clean) >= 10:
            # Только последние 10 цифр
            last_10 = clean[-10:]
            formats['partial'].append(last_10)
            formats['partial'].append(f"{last_10[0:3]}-{last_10[3:6]}-{last_10[6:]}")
            # Только код оператора + последние 7
            operator_code = clean[-10:-7]
            last_7 = clean[-7:]
            formats['partial'].append(f"{operator_code}{last_7}")
            formats['partial'].append(f"{operator_code}-{last_7}")
        
        return formats
    
    def get_all_unique_formats(self) -> List[str]:
        """Получить список всех уникальных форматов"""
        all_formats = set()
        for category, numbers in self.formats.items():
            for num in numbers:
                if num:
                    all_formats.add(num)
        return sorted(list(all_formats))
    
    def get_formats_by_category(self) -> Dict[str, List[str]]:
        """Получить форматы сгруппированные по категориям"""
        result = {}
        for category, numbers in self.formats.items():
            unique_nums = list(set(numbers))
            if unique_nums:
                result[category] = unique_nums
        return result


class MultiFormatOSINTSearcher:
    """Поиск по множественным форматам номера"""
    
    def __init__(self, phone: str):
        self.phone = phone
        self.converter = PhoneFormatConverter(phone)
        self.results = {}
    
    def generate_search_urls(self, phone_format: str) -> Dict[str, str]:
        """Сгенерировать ссылки поиска для конкретного формата"""
        encoded = quote(phone_format)
        
        return {
            'vkontakte': f'https://vk.com/search?c[q]={encoded}',
            'odnoklassniki': f'https://ok.ru/search?q={encoded}',
            '2gis': f'https://2gis.ru/search?q={encoded}',
            'google': f'https://www.google.com/search?q=%22{encoded}%22',
            'google_dork': f'https://www.google.com/search?q=%22{encoded}%22+%D0%9F%D0%90%D0%A1%D0%9F%D0%9E%D0%A0%D0%A2',
            'yandex': f'https://www.yandex.ru/search/?text={encoded}',
            'avva': f'https://avva.ru/?q={encoded}',
            'dehashed': f'https://dehashed.com/search?query={encoded}',
        }
    
    def search_all_formats(self) -> Dict[str, any]:
        """Провести поиск по всем форматам"""
        all_formats = self.converter.get_all_unique_formats()
        
        print("\n" + "="*120)
        print("🔍 РАСШИРЕННЫЙ ПОИСК ПО ВСЕМ ФОРМАТАМ НОМЕРА")
        print("="*120 + "\n")
        
        print(f"📱 ИСХОДНЫЙ НОМЕР: {self.phone}")
        print(f"🔢 НАЙДЕНО УМНИКАЛЬНЫХ ФОРМАТОВ: {len(all_formats)}\n")
        
        # Группируем по категориям
        formats_by_category = self.converter.get_formats_by_category()
        
        print("📋 КАТЕГОРИИ ФОРМАТОВ:")
        print("─"*120 + "\n")
        
        for category, formats_list in formats_by_category.items():
            category_name = category.replace('_', ' ').upper()
            print(f"  {category_name} ({len(formats_list)} формат):")
            for fmt in formats_list[:3]:  # Показываем первые 3
                print(f"    • {fmt}")
            if len(formats_list) > 3:
                print(f"    ... и еще {len(formats_list) - 3}")
            print()
        
        # Генерируем поиск для каждого уникального формата
        print("\n" + "="*120)
        print("🌐 ПОИСК ПО 8 ПЛАТФОРМАМ ДЛЯ КАЖДОГО ФОРМАТА")
        print("="*120 + "\n")
        
        search_data = {}
        
        for idx, phone_format in enumerate(all_formats, 1):
            urls = self.generate_search_urls(phone_format)
            search_data[phone_format] = urls
            
            # Выводим первые 5 форматов
            if idx <= 5:
                print(f"{idx}. ФОРМАТ: {phone_format}")
                print("   Ссылки для поиска:")
                for platform, url in list(urls.items())[:3]:
                    print(f"     • {platform}: {url[:80]}...")
                print()
        
        if len(all_formats) > 5:
            print(f"... и еще {len(all_formats) - 5} форматов с поиском по всем платформам\n")
        
        return {
            'original_phone': self.phone,
            'total_formats': len(all_formats),
            'formats_by_category': formats_by_category,
            'all_formats': all_formats,
            'search_urls': search_data,
            'total_search_urls': len(all_formats) * len(self.generate_search_urls(all_formats[0])) if all_formats else 0
        }


class AdvancedOSINTReporter:
    """Создание продвинутого отчета с анализом всех форматов"""
    
    def __init__(self, search_results: Dict):
        self.results = search_results
    
    def create_report(self) -> Dict:
        """Создать полный отчет"""
        return {
            'timestamp': datetime.now().isoformat(),
            'search_summary': {
                'original_phone': self.results['original_phone'],
                'total_unique_formats': self.results['total_formats'],
                'total_search_urls_generated': self.results['total_search_urls'],
                'platforms_per_format': 8
            },
            'formats_analysis': {
                'by_category': self.results['formats_by_category'],
                'all_formats': self.results['all_formats']
            },
            'search_sources': {
                'vkontakte': 'Российская соцсеть (ВКонтакте)',
                'odnoklassniki': 'Российская соцсеть (Одноклассники)',
                '2gis': 'Справочник компаний и людей',
                'google': 'Поиск точного совпадения',
                'google_dork': 'Google Dork с ключевыми словами',
                'yandex': 'Русский поисковик',
                'avva': 'Агрегатор публичных профилей',
                'dehashed': 'База утечек и скомпрометированных данных'
            },
            'search_strategy': [
                '1. Проверить каждый формат в ВКонтакте (наиболее полная база)',
                '2. Проверить в Одноклассниках (часто полная информация)',
                '3. Проверить в 2ГИС (если деловой номер)',
                '4. Выполнить Google Dork поиск для каждого формата',
                '5. Проверить Яндекс для русского контента',
                '6. Проверить AVVA на публичные профили',
                '7. Проверить DeHashed на скомпрометированные данные'
            ],
            'recommendations': {
                'best_format_for_search': 'Используйте формат +7ХХХХХХХХХХ (международный)',
                'alternative_formats': 'Если не найдено, попробуйте 8ХХХХХХХХХХ (российский)',
                'partial_search': 'Поиск по последним 7 цифрам может найти в профилях',
                'formatted_search': 'Формат с пробелами/дефисами может найтись в документах'
            }
        }


def main():
    phone = "+79182469659"
    
    print("\n" + "█"*120)
    print("█" + " "*118 + "█")
    print("█" + "🔍 МНОГОФОРМАТНЫЙ OSINT ПОИСК ПО НОМЕРУ ТЕЛЕФОНА".center(118) + "█")
    print("█" + " "*118 + "█")
    print("█"*120 + "\n")
    
    # Создаем конвертер форматов
    searcher = MultiFormatOSINTSearcher(phone)
    
    # Проводим поиск
    search_results = searcher.search_all_formats()
    
    # Создаем отчет
    reporter = AdvancedOSINTReporter(search_results)
    full_report = reporter.create_report()
    
    # Выводим итоговый отчет
    print("\n" + "="*120)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("="*120 + "\n")
    
    print(f"📱 Номер: {full_report['search_summary']['original_phone']}")
    print(f"📝 Уникальных форматов: {full_report['search_summary']['total_unique_formats']}")
    print(f"🔗 Всего ссылок для поиска: {full_report['search_summary']['total_search_urls_generated']}")
    print(f"🌐 Платформ для каждого формата: {full_report['search_summary']['platforms_per_format']}\n")
    
    print("📋 РЕКОМЕНДУЕМАЯ СТРАТЕГИЯ ПОИСКА:")
    print("─"*120 + "\n")
    for step in full_report['search_strategy']:
        print(f"  {step}")
    
    print("\n💡 РЕКОМЕНДАЦИИ:")
    print("─"*120 + "\n")
    for rec_type, rec_text in full_report['recommendations'].items():
        print(f"  {rec_type.replace('_', ' ').title()}: {rec_text}")
    
    # Сохраняем в JSON
    filename = f'multi_format_osint_report_{phone.replace("+", "")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(full_report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Полный отчет сохранен: {filename}\n")
    print("█"*120 + "\n")
    
    return full_report


if __name__ == '__main__':
    main()
