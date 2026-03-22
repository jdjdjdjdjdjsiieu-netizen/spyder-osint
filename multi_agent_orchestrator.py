#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Многоагентная система OSINT с оркестрацией ИИ моделей
Использует CrewAI для координации специализированных агентов
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

# Попробуем импортировать CrewAI, если установлен
try:
    from crewai import Agent, Task, Crew
    HAS_CREWAI = True
except ImportError:
    HAS_CREWAI = False
    print("⚠️  CrewAI не установлен. Используем симуляцию многоагентной системы.")

class OSINTAgent:
    """Базовый OSINT агент"""
    
    def __init__(self, name: str, role: str, expertise: str):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.results = []
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализировать данные в соответствии с ролью"""
        return {
            'agent': self.name,
            'role': self.role,
            'analysis': self._perform_analysis(data)
        }
    
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Переопределяется в подклассах"""
        raise NotImplementedError


class PhoneValidationAgent(OSINTAgent):
    """Агент для валидации и анализа номера телефона"""
    
    def __init__(self):
        super().__init__(
            name="PhoneValidator",
            role="Phone Validator",
            expertise="Валидация и анализ номеров телефонов"
        )
    
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        phone = data.get('phone', '')
        phone_clean = re.sub(r'\D', '', phone)
        
        return {
            'valid': len(phone_clean) >= 10,
            'normalized': f"+{phone_clean}" if phone_clean.startswith('7') else f"+7{phone_clean[1:]}",
            'operator': self._identify_operator(phone_clean),
            'country': 'Russia' if phone_clean.startswith('7') else 'Unknown',
            'type': 'Mobile' if len(phone_clean) == 11 else 'Unknown'
        }
    
    def _identify_operator(self, phone_clean: str) -> str:
        """Определить оператора по коду"""
        operators = {
            '901': 'MTS', '902': 'MTS', '903': 'MTS', '904': 'MTS', '905': 'MTS',
            '911': 'MTS', '918': 'Megafon', '919': 'Megafon', '920': 'Megafon',
            '950': 'Tele2', '951': 'Tele2', '953': 'Tele2', '955': 'Tele2',
            '960': 'Beeline', '961': 'Beeline', '962': 'Beeline'
        }
        prefix = phone_clean[1:4] if len(phone_clean) >= 4 else phone_clean[:3]
        return operators.get(prefix, 'Unknown Operator')


class SocialMediaAgent(OSINTAgent):
    """Агент для поиска в социальных сетях"""
    
    def __init__(self):
        super().__init__(
            name="SocialMediaSearcher",
            role="Social Media Searcher",
            expertise="Поиск в социальных сетях и публичных профилях"
        )
    
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        phone = data.get('phone', '')
        phone_encoded = phone.replace("+", "%2B")
        
        return {
            'platforms': {
                'vkontakte': f'https://vk.com/search?c[q]={phone_encoded}',
                'odnoklassniki': f'https://ok.ru/search?q={phone_encoded}',
                '2gis': f'https://2gis.ru/search?q={phone_encoded}',
                'twitter': f'https://twitter.com/search?q={phone_encoded}',
                'instagram': f'https://www.instagram.com/explore/tags/{phone.replace("+", "")}/',
            },
            'recommendation': 'Требуется ручной поиск в браузере (сайты блокируют ботов)',
            'search_strategy': [
                'Начать с ВКонтакте - наиболее полная база русских пользователей',
                'Затем Одноклассники - часто есть полная информация',
                'Проверить 2GIS - если это деловой номер',
                'Instagram/Twitter - для молодежи',
                'Telegram - требует специального клиента'
            ]
        }


class DatabaseAgent(OSINTAgent):
    """Агент для поиска в базах данных и реестрах"""
    
    def __init__(self):
        super().__init__(
            name="DatabaseSearcher",
            role="Database Researcher",
            expertise="Поиск в открытых БД и государственных реестрах"
        )
    
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'russian_registries': {
                'rosreestr': {
                    'url': 'https://www.rosreestr.ru/',
                    'data': 'Реестр недвижимости (требуется ФИО или адрес)',
                    'access': 'Public with limitations'
                },
                'fns_egrul': {
                    'url': 'https://egrul.nalog.ru/',
                    'data': 'Реестр ИП и ООО (требуется ИНН)',
                    'access': 'Public API available'
                },
                'tax_registry': {
                    'url': 'https://service.nalog.ru/',
                    'data': 'Справочник ИНН физических лиц',
                    'access': 'Public API available'
                }
            },
            'search_sequence': [
                '1. Получить ФИО из социальных сетей',
                '2. Поискать в Росреестре по ФИО',
                '3. Если найдено имущество - получить адрес',
                '4. Поискать ИНН через ФНС ЕГРЮЛ',
                '5. Проверить банковскую активность'
            ]
        }


class LeakDatabaseAgent(OSINTAgent):
    """Агент для поиска в базах утечек"""
    
    def __init__(self):
        super().__init__(
            name="LeakChecker",
            role="Breach Database Researcher",
            expertise="Поиск в базах компрометированных данных"
        )
    
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        phone = data.get('phone', '')
        phone_encoded = phone.replace("+", "%2B")
        
        return {
            'databases': {
                'haveibeenpwned': {
                    'url': 'https://haveibeenpwned.com/',
                    'note': 'Поиск возможен по email (требуется получить email из профиля)',
                    'api': 'Available with rate limiting'
                },
                'dehashed': {
                    'url': 'https://dehashed.com/',
                    'query': f'https://dehashed.com/search?query={phone_encoded}',
                    'data': 'Утечки email, пароли, IP адреса',
                    'cost': 'Paid, with free tier'
                },
                'leakpeek': {
                    'url': 'https://leakpeek.com/',
                    'data': 'Поиск по компании и email в утечках',
                    'cost': 'Free'
                }
            },
            'findings_if_compromised': [
                'Email адреса из утечек',
                'Захешированные пароли',
                'IP адреса использования',
                'История использования',
                'Связанные аккаунты'
            ]
        }


class AggregationAgent(OSINTAgent):
    """Агент для агрегации и анализа результатов"""
    
    def __init__(self):
        super().__init__(
            name="AggregationEngine",
            role="Data Aggregator",
            expertise="Объединение данных из разных источников и создание профиля"
        )
    
    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'data_profile': {
                'identification': 'ФИО, дата рождения, фото',
                'location': 'Город, адрес, координаты',
                'contacts': 'Email, другие номера телефонов, мессенджеры',
                'social': 'Профили в соцсетях, друзья, интересы',
                'employment': 'Место работы, должность, резюме',
                'financial': 'История платежей, банковские счета',
                'property': 'Недвижимость, ТС, регистрация',
                'security': 'Наличие в утечках, компрометированные пароли'
            },
            'confidence_scoring': {
                'high_confidence': ['Найдено в 3+ источниках', 'Возможна перекрестная проверка'],
                'medium_confidence': ['Найдено в 2 источниках', 'Требует уточнения'],
                'low_confidence': ['Найдено в 1 источнике', 'Требует верификации']
            },
            'final_report_includes': [
                'Полный профиль с фото',
                'Все найденные контакты',
                'История активности',
                'Связи с другими людьми/компаниями',
                'Оценка надежности данных',
                'Источники информации'
            ]
        }


class OSINTOrchestrator:
    """Оркестратор агентов OSINT - координирует работу всех агентов"""
    
    def __init__(self):
        self.agents = {
            'phone_validator': PhoneValidationAgent(),
            'social_media': SocialMediaAgent(),
            'databases': DatabaseAgent(),
            'leaks': LeakDatabaseAgent(),
            'aggregation': AggregationAgent()
        }
        self.results = {}
    
    def orchestrate_search(self, phone: str) -> Dict[str, Any]:
        """
        Оркестрирует полный поиск через всех агентов
        """
        print("\n" + "="*100)
        print("🤖 МНОГОАГЕНТНАЯ OSINT СИСТЕМА")
        print("="*100 + "\n")
        
        # Фаза 1: Валидация
        print("ФАЗА 1️⃣  ВАЛИДАЦИЯ И АНАЛИЗ НОМЕРА")
        print("─"*100)
        phone_data = {'phone': phone}
        phone_result = self.agents['phone_validator'].analyze(phone_data)
        self.results['phone_validation'] = phone_result
        print(f"✓ Агент {phone_result['agent']} завершил анализ")
        print(json.dumps(phone_result['analysis'], ensure_ascii=False, indent=2))
        print()
        
        # Фаза 2: Поиск в соцсетях
        print("ФАЗА 2️⃣  ПОИСК В СОЦИАЛЬНЫХ СЕТЯХ")
        print("─"*100)
        social_result = self.agents['social_media'].analyze(phone_data)
        self.results['social_media'] = social_result
        print(f"✓ Агент {social_result['agent']} генерирует ссылки для поиска")
        print(f"\n📱 Социальные платформы: {len(social_result['analysis']['platforms'])} шт")
        print(f"Стратегия: {social_result['analysis']['recommendation']}\n")
        for platform, url in list(social_result['analysis']['platforms'].items())[:3]:
            print(f"  • {platform}: {url}")
        print()
        
        # Фаза 3: Поиск в БД
        print("ФАЗА 3️⃣  ПОИСК В РЕЕСТРАХ И БД")
        print("─"*100)
        db_result = self.agents['databases'].analyze(phone_data)
        self.results['databases'] = db_result
        print(f"✓ Агент {db_result['agent']} планирует поиск в реестрах")
        print(f"📊 Доступно реестров: {len(db_result['analysis']['russian_registries'])} шт")
        print(f"Последовательность поиска:")
        for step in db_result['analysis']['search_sequence']:
            print(f"  → {step}")
        print()
        
        # Фаза 4: Проверка утечек
        print("ФАЗА 4️⃣  ПРОВЕРКА БАЗ УТЕЧЕК")
        print("─"*100)
        leak_result = self.agents['leaks'].analyze(phone_data)
        self.results['leaks'] = leak_result
        print(f"✓ Агент {leak_result['agent']} проверяет утечки")
        print(f"💾 Базы утечек: {len(leak_result['analysis']['databases'])} доступных")
        print()
        
        # Фаза 5: Агрегация
        print("ФАЗА 5️⃣  АГРЕГАЦИЯ И АНАЛИЗ")
        print("─"*100)
        agg_result = self.agents['aggregation'].analyze(phone_data)
        self.results['aggregation'] = agg_result
        print(f"✓ Агент {agg_result['agent']} готовит итоговый профиль")
        print(f"📋 Компоненты профиля: {len(agg_result['analysis']['data_profile'])} элементов")
        for component, desc in list(agg_result['analysis']['data_profile'].items())[:5]:
            print(f"  ✓ {component.upper()}: {desc}")
        print()
        
        return self._compile_final_report(phone)
    
    def _compile_final_report(self, phone: str) -> Dict[str, Any]:
        """Создает финальный отчет"""
        return {
            'phone': phone,
            'timestamp': datetime.now().isoformat(),
            'orchestration_phases': 5,
            'agents_used': list(self.agents.keys()),
            'agents_results': self.results,
            'search_status': 'READY_FOR_MANUAL_EXECUTION',
            'next_steps': [
                '1. Откройте ссылки на социальные сети в браузере (блокируют ботов)',
                '2. Проведите ручной поиск и соберите ФИО',
                '3. Используйте ФИО для поиска в государственных реестрах',
                '4. Проверьте базы утечек через найденные email',
                '5. Агрегируйте все найденные данные в один профиль'
            ]
        }


def main():
    import sys
    
    phone = sys.argv[1] if len(sys.argv) > 1 else "+79182469659"
    
    # Создаем оркестратор
    orchestrator = OSINTOrchestrator()
    
    # Запускаем поиск
    report = orchestrator.orchestrate_search(phone)
    
    # Выводим финальный отчет
    print("="*100)
    print("✅ МНОГОАГЕНТНАЯ СИСТЕМА ЗАВЕРШИЛА РАБОТУ")
    print("="*100 + "\n")
    
    print("📄 ФИНАЛЬНЫЙ ОТЧЕТ:")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    # Сохраняем
    filename = f'multi_agent_osint_report_{phone.replace("+", "")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Отчет сохранен: {filename}")


if __name__ == '__main__':
    main()
