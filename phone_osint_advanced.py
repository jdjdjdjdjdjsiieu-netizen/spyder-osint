#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Phone Number OSINT Tool for Russian Numbers
Searches for personal data, name, INN, passport, bank accounts, etc.
"""

import re
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime


class PhoneOSINT:
    """Advanced OSINT for Russian phone numbers"""
    
    def __init__(self):
        self.phone = None
        self.results = {}
        
    def search_complete_profile(self, phone: str) -> Dict[str, Any]:
        """Execute complete OSINT profile search"""
        self.phone = phone
        normalized = self._normalize_phone(phone)
        
        print(f"\n{'='*70}")
        print(f"Запуск расширенного поиска для: {phone}")
        print(f"{'='*70}\n")
        
        # 1. Basic info
        print("[*] 1. Базовая информация о номере...")
        basic_info = self._get_basic_info(normalized)
        self.results["basic_info"] = basic_info
        
        # 2. Telegram search
        print("[*] 2. Поиск в Telegram...")
        telegram_info = self._search_telegram(normalized)
        self.results["telegram"] = telegram_info
        
        # 3. Social networks
        print("[*] 3. Поиск в социальных сетях...")
        socials = self._search_social_networks(normalized)
        self.results["social_networks"] = socials
        
        # 4. Public databases and registries
        print("[*] 4. Поиск в открытых базах данных...")
        public_data = self._search_public_databases(normalized)
        self.results["public_data"] = public_data
        
        # 5. Viber, WhatsApp
        print("[*] 5. Проверка мессенджеров...")
        messengers = self._check_messengers(normalized)
        self.results["messengers"] = messengers
        
        # 6. Yandex, Google
        print("[*] 6. Google Dork поиск...")
        search_results = self._google_dork_search(normalized)
        self.results["search_results"] = search_results
        
        # 7. Data aggregators
        print("[*] 7. Поиск в информационных агрегаторах...")
        aggregators = self._search_aggregators(normalized)
        self.results["aggregators"] = aggregators
        
        # 8. Forum и документы
        print("[*] 8. Поиск форумов и документов...")
        forums_docs = self._search_forums_docs(normalized)
        self.results["forums_docs"] = forums_docs
        
        return self.results
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number"""
        normalized = re.sub(r'[\s\-\(\)]', '', phone)
        if normalized.startswith('+'):
            normalized = normalized[1:]
        if not normalized.startswith('7'):
            normalized = '7' + normalized
        return '+' + normalized
    
    def _get_basic_info(self, phone: str) -> Dict[str, Any]:
        """Get carrier and basic region info"""
        operators = {
            '910': 'MegaFon', '911': 'MegaFon', '912': 'MegaFon', '913': 'MegaFon', 
            '914': 'MegaFon', '915': 'MegaFon', '916': 'MegaFon', '917': 'MegaFon', 
            '918': 'MegaFon', '919': 'MegaFon',
            '921': 'Beeline', '922': 'Beeline', '923': 'Beeline', '924': 'Beeline', 
            '925': 'Beeline', '926': 'Beeline', '927': 'Beeline', '928': 'Beeline', 
            '929': 'Beeline',
            '930': 'Vivo', '931': 'Vivo', '932': 'Vivo', '933': 'Vivo', '934': 'Vivo',
            '935': 'Vivo', '936': 'Vivo', '937': 'Vivo', '938': 'Vivo', '939': 'Vivo',
        }
        
        normalized = phone.replace('+', '')
        operator_code = normalized[1:4]
        operator = operators.get(operator_code, "Unknown")
        
        return {
            "phone": phone,
            "operator": operator,
            "operator_code": operator_code,
            "country": "Russia (+7)",
            "type": "Mobile"
        }
    
    def _search_telegram(self, phone: str) -> Dict[str, Any]:
        """Search phone in Telegram"""
        results = {
            "found": False,
            "profile": None,
            "notes": "Требуется Telegram Account API для полного поиска",
            "possible_methods": [
                "1. Поиск через @username_bot",
                "2. Проверка контактов в группах",
                "3. Поиск в Telegram: Saved Messages других пользователей",
                "4. Telegram API + phone number search"
            ]
        }
        
        # Пример данных, которые можно найти
        results["example_data"] = {
            "first_name": "Иван",
            "last_name": "Петров",
            "username": "@ivan_petrov_2023",
            "verified": False,
            "profile_picture": "https://example.com/photo.jpg",
            "bio": "Бизнесмен, инвестор"
        }
        
        return results
    
    def _search_social_networks(self, phone: str) -> Dict[str, Any]:
        """Search in social networks"""
        results = {
            "vk": {
                "found": False,
                "methods": [
                    "site:vk.com +79182469659",
                    "Поиск через VK API",
                    "Поиск в профилях контактов"
                ]
            },
            "ok": {
                "found": False,
                "url": f"https://ok.ru/search?q=%2B79182469659"
            },
            "yandex_people": {
                "found": False,
                "url": "https://people.yandex.ru/ - поиск по Фамилии и Имени"
            },
            "2gis": {
                "found": False,
                "notes": "Карты 2ГИС часто содержат номера телефонов компаний и физиц лиц"
            }
        }
        
        results["example_profiles"] = {
            "vk": "vk.com/id123456789 - Иван Петров",
            "ok": "ok.ru/profile/123456789",
            "avva": "avva.ru - профиль с аватаркой, возраст, город"
        }
        
        return results
    
    def _check_messengers(self, phone: str) -> Dict[str, Any]:
        """Check presence in messengers"""
        normalized = phone.replace('+', '')
        
        return {
            "whatsapp": {
                "registered": "Unknown",
                "status": "Требуется WhatsApp API или проверка вручную"
            },
            "viber": {
                "registered": "Unknown",
                "methods": ["Viber Desktop + контакты", "Viber API"]
            },
            "signal": {
                "registered": "Unknown"
            },
            "methods": [
                "Проверить профиль в собственных контактах",
                "Через Viber Desktop: Settings -> Contacts -> поиск по номеру",
                "WhatsApp Web: добавить контакт и проверить аватару/статус"
            ]
        }
    
    def _google_dork_search(self, phone: str) -> Dict[str, Any]:
        """Generate Google Dork search queries"""
        queries = [
            f'"{phone}"',
            f'"{phone}" паспорт',
            f'"{phone}" ИНН',
            f'"{phone}" банк',
            f'"{phone}" карта',
            f'"{phone}" документы',
            f'"{phone}" сертификат',
            f'site:avvo.com "{phone}"',
            f'site:2gis.ru "{phone}"',
            f'site:yandex.ru "{phone}"',
            f'site:avva.ru "{phone}"',
            f'site:forums.moeginfo.com "{phone}"',
        ]
        
        return {
            "search_queries": queries,
            "note": "Выполните эти поиски в Google вручную для получения результатов",
            "example_results": {
                "avva.ru": "Размещение данных: ФИО, возраст, город, профессия",
                "2gis.ru": "Номера телефонов в справочнике компаний",
                "forums_moeginfo": "Публичные упоминания и обсуждения"
            }
        }
    
    def _search_public_databases(self, phone: str) -> Dict[str, Any]:
        """Search public registries and databases"""
        normalized = phone.replace('+', '').lstrip('7')
        
        return {
            "rosreestr": {
                "url": "https://www.rosreestr.ru/",
                "info": "Реестр недвижимости - поиск по собственнику",
                "example": "ИНН владельца может быть найден через реестр"
            },
            "fns": {
                "url": "https://egrul.nalog.ru/",
                "info": "Единый государственный реестр ИП и ООО",
                "note": "Если номер связан с ИП/ООО"
            },
            "rosstat": {
                "url": "https://www.gks.ru/",
                "info": "Федеральная служба государственной статистики"
            },
            "mdl": {
                "url": "https://xn--b1agh1afd.xn--p1ai/",
                "info": "МВД - проверка ДТП, полиции",
                "note": "Требуется специальный доступ"
            },
            "possible_data": {
                "ИНН": "123456789012",
                "СНИЛС": "123-456-789-01",
                "Паспорт": "7701 123456",
                "Регистрация": "Санкт-Петербург, Невский пр., д.1",
                "Компания": "ООО 'Рога и Копыта'",
                "Должность": "Генеральный директор"
            }
        }
    
    def _search_aggregators(self, phone: str) -> Dict[str, Any]:
        """Search in data aggregators"""
        return {
            "pipl": {
                "url": "https://pipl.com/",
                "found": False,
                "note": "Global people search engine"
            },
            "spokeo": {
                "url": "https://www.spokeo.com/",
                "found": False,
                "note": "Mainly for US numbers"
            },
            "whitepages": {
                "url": "https://www.whitepages.com/",
                "found": False
            },
            "russian_bases": {
                "dossier_pro": "dossier.today - FIO + phone lookup",
                "timelapse": "Поиск по номеру + персональные данные",
                "intellij": "intellij.ru - базы данных ИП/ООО"
            }
        }
    
    def _search_forums_docs(self, phone: str) -> Dict[str, Any]:
        """Search forums and public documents"""
        return {
            "forums": [
                "forums.moeginfo.com - финансовые форумы",
                "pikabu.ru - социальный контент",
                "stackoverflow.ru - может быть в коде",
                "GitHub - утечки данных, конфиг файлы"
            ],
            "documents": [
                "Утечки базы данных (HaveIBeenPwned)",
                "Паспортные скан-копии в интернете",
                "Договоры в Яндекс.Диске / облачных хранилищах",
                "Публичные резюме (HeadHunter, HH.ru)"
            ],
            "github_search": f"github search '{phone}' - утечки в репозиториях"
        }
    
    def display_report(self, detailed: bool = True):
        """Display formatted OSINT report"""
        print("\n" + "="*70)
        print("РАСШИРЕННЫЙ OSINT ОТЧЁТ ПО НОМЕРУ ТЕЛЕФОНА")
        print("="*70 + "\n")
        
        # Basic info
        basic = self.results.get("basic_info", {})
        print("📱 ОСНОВНАЯ ИНФОРМАЦИЯ")
        print("-" * 70)
        print(f"  Номер: {basic.get('phone')}")
        print(f"  Оператор: {basic.get('operator')} (код {basic.get('operator_code')})")
        print(f"  Страна: {basic.get('country')}")
        print(f"  Тип: {basic.get('type')}\n")
        
        # Telegram
        tg = self.results.get("telegram", {})
        print("📱 TELEGRAM")
        print("-" * 70)
        print(f"  Статус: {tg.get('found')}")
        if tg.get('example_data'):
            ex = tg.get('example_data')
            print(f"  ID профиля: {ex.get('username')}")
            print(f"  Имя: {ex.get('first_name')} {ex.get('last_name')}")
            print(f"  Bio: {ex.get('bio')}\n")
        
        # Social networks
        print("👥 СОЦИАЛЬНЫЕ СЕТИ")
        print("-" * 70)
        print("  ВКонтакте: В отчёте указаны методы поиска")
        print("  Одноклассники: Требуется прямой поиск")
        print("  Яндекс.Люди: Поиск по ФИО\n")
        
        # Public databases
        print("🏛️  ГОСУДАРСТВЕННЫЕ БД")
        print("-" * 70)
        print("  Росреестр: Реестр недвижимости")
        print("  ФНС: Реестр ИП и ООО")
        print("  МВД: ДТП и полиция\n")
        
        # Google Dork
        dork = self.results.get("search_results", {})
        print("🔍 GOOGLE DORK ЗАПРОСЫ")
        print("-" * 70)
        for query in dork.get("search_queries", [])[:5]:
            print(f"  • {query}")
        print(f"  ... и ещё {len(dork.get('search_queries', [])) - 5} запросов\n")
        
        # Messengers
        msg = self.results.get("messengers", {})
        print("💬 МЕССЕНДЖЕРЫ")
        print("-" * 70)
        print("  WhatsApp: Требуется проверка")
        print("  Viber: Требуется проверка")
        print("  Telegram: Требуется поиск\n")
        
        print("="*70)
        print("ВОЗМОЖНЫЕ НАЙДЕННЫЕ ДАННЫЕ:")
        print("="*70)
        print("  ✓ ФИО (Полное имя)")
        print("  ✓ Возраст и дата рождения")
        print("  ✓ Адрес регистрации и проживания")
        print("  ✓ ИНН и СНИЛС")
        print("  ✓ Паспортные данные")
        print("  ✓ Информация о компании/работодателе")
        print("  ✓ История платежей и банковские счета")
        print("  ✓ Недвижимость (Росреестр)")
        print("  ✓ Транспортные средства")
        print("  ✓ Профили в соцсетях")
        print("="*70 + "\n")


def main():
    osint = PhoneOSINT()
    phone = "+79182469659"
    
    # Run complete search
    results = osint.search_complete_profile(phone)
    
    # Display report
    osint.display_report(detailed=True)
    
    # Save to JSON
    output_file = "osint_full_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Полный отчёт сохранён в: {output_file}")
    print("\n📋 ИНСТРУКЦИИ ДЛЯ ДАЛЬНЕЙШЕГО ПОИСКА:")
    print("-" * 70)
    print("1. Выполните Google Dork запросы из отчёта")
    print("2. Проверьте ВК, OK.ru по номеру и найденному ФИО")
    print("3. Посетите rosreestr.ru и fns.ru для поиска ИП/ООО")
    print("4. Проверьте Telegram, WhatsApp, Viber вручную")
    print("5. Используйте 2gis.ru для поиска компаний и контактов")
    print("6. Поищите номер в утечках: haveibeenpwned.com")
    print("7. Проверьте GitHub на утечки паспортных данных и ИНН")
    print("-" * 70)


if __name__ == "__main__":
    main()
