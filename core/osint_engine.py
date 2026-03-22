#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced OSINT Engine with integrated APIs and tools
"""

import json
import requests
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import socket
from urllib.parse import quote

from utils.logger import get_logger

logger = get_logger(__name__)


class OSINTEngine:
    """Main OSINT engine with multiple data sources integration"""
    
    # Free APIs and Services
    FREE_APIS = {
        "ipqualityscore": {
            "url": "https://ipqualityscore.com/api/json/phone",
            "params": ["phone"],
            "note": "Requires IP Quality Score free tier"
        },
        "numverify": {
            "url": "https://numverify.com/",
            "note": "Basic validation available",
            "free_tier": True
        },
        "ovh_reverse": {
            "url": "https://www.ovh.com/cgi-bin/tools/reverse-phone",
            "method": "web_scrape"
        },
        "truecaller_web": {
            "url": "https://www.truecaller.com/",
            "method": "web_lookup",
            "free_tier": True
        },
        "2gis_api": {
            "url": "https://2gis.ru/search",
            "method": "web_scrape",
            "region": "Russia"
        },
        "yandex_search": {
            "url": "https://www.yandex.ru/search",
            "method": "dork",
            "free_tier": True
        },
        "google_custom_search": {
            "url": "https://www.google.com/search",
            "method": "dork",
            "free_tier": True
        }
    }
    
    # Social Media APIs
    SOCIAL_MEDIA_SOURCES = {
        "vk": {
            "url": "https://vk.com/search",
            "method": "social_search",
            "data": ["ФИО", "возраст", "город", "работа"]
        },
        "ok": {
            "url": "https://ok.ru/search",
            "method": "social_search"
        },
        "telegram": {
            "method": "username_search",
            "tool": "@username_bot"
        },
        "instagram": {
            "url": "https://www.instagram.com/",
            "method": "username_search"
        },
        "twitter_x": {
            "url": "https://twitter.com/search",
            "method": "search_api"
        }
    }
    
    # Russian sources
    RUSSIAN_SOURCES = {
        "rosreestr": {
            "url": "https://www.rosreestr.ru/",
            "data": "Недвижимость, регистрация"
        },
        "fns": {
            "url": "https://egrul.nalog.ru/",
            "data": "ИП, ООО, ИНН"
        },
        "2gis": {
            "url": "https://2gis.ru/",
            "data": "Справочник компаний, контакты"
        },
        "yandex_maps": {
            "url": "https://yandex.ru/maps/",
            "data": "Адреса, компании, контакты"
        },
        "avva": {
            "url": "https://avva.ru/",
            "data": "Публичные профили, ФИО, адреса"
        },
        "hh": {
            "url": "https://hh.ru/",
            "data": "Резюме, опыт работы, контакты"
        }
    }
    
    def __init__(self):
        self.phone = None
        self.results = {}
        self.search_methods = []
        
    def comprehensive_search(self, phone: str) -> Dict[str, Any]:
        """Execute comprehensive OSINT search"""
        self.phone = self._normalize_phone(phone)
        logger.info(f"Starting comprehensive OSINT search for: {phone}")
        
        results = {
            "phone": phone,
            "normalized": self.phone,
            "timestamp": datetime.now().isoformat(),
            "basic_info": self._get_basic_info(),
            "google_dorks": self._generate_google_dorks(),
            "social_media_links": self._get_social_media_links(),
            "russian_sources": self._get_russian_sources(),
            "api_endpoints": self._get_api_endpoints(),
            "scraping_methods": self._get_scraping_methods(),
            "open_sources": self._get_open_sources(),
        }
        
        self.results = results
        return results
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number to standard format"""
        normalized = re.sub(r'[\s\-\(\)]', '', phone)
        if normalized.startswith('+'):
            normalized = normalized[1:]
        if not normalized.startswith('7'):
            if normalized.startswith('8'):
                normalized = '7' + normalized[1:]
            else:
                normalized = '7' + normalized
        return '+' + normalized
    
    def _get_basic_info(self) -> Dict[str, Any]:
        """Get basic phone information"""
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
        
        normalized = self.phone.replace('+', '')
        operator_code = normalized[1:4]
        
        return {
            "phone": self.phone,
            "operator": operators.get(operator_code, "Unknown"),
            "operator_code": operator_code,
            "country": "Russia",
            "type": "Mobile"
        }
    
    def _generate_google_dorks(self) -> List[str]:
        """Generate Google Dork search queries"""
        phone_plain = self.phone[2:]  # Remove +7
        
        return [
            f'"{self.phone}"',
            f'"+7{phone_plain}"',
            f'"{self.phone}" паспорт',
            f'"{self.phone}" ИНН',
            f'"{self.phone}" банк',
            f'"{self.phone}" карта',
            f'"{self.phone}" документы',
            f'"{self.phone}" резюме',
            f'"{self.phone}" контакт',
            f'site:avva.ru "{self.phone}"',
            f'site:2gis.ru "{self.phone}"',
            f'site:vk.com "{self.phone}"',
            f'site:ok.ru "{self.phone}"',
            f'site:hh.ru "{self.phone}"',
            f'site:forums.moeginfo.com "{self.phone}"',
            f'site:github.com "{self.phone}"',
            f'"{self.phone}" filetype:pdf',
            f'"{self.phone}" filetype:docx',
            f'"{self.phone}" filetype:xlsx',
        ]
    
    def _get_social_media_links(self) -> Dict[str, str]:
        """Generate social media search links"""
        phone_encoded = quote(self.phone)
        
        return {
            "vkontakte": f"https://vk.com/search?c[q]={phone_encoded}",
            "odnoklassniki": f"https://ok.ru/search?q={phone_encoded}",
            "telegram": "https://t.me/username_bot - поиск по username",
            "instagram": f"https://www.instagram.com/",
            "twitter": f"https://twitter.com/search?q={phone_encoded}",
            "whatsapp": "https://web.whatsapp.com/ - добавить номер",
            "viber": "Viber Desktop - поиск по номеру",
            "2gis": f"https://2gis.ru/spb/search/{phone_encoded}",
            "yandex_people": "https://people.yandex.ru/ - поиск по ФИО",
        }
    
    def _get_russian_sources(self) -> Dict[str, Dict[str, Any]]:
        """Russian-specific data sources"""
        return {
            "rosreestr": {
                "url": "https://www.rosreestr.ru/",
                "data": "Реестр недвижимости",
                "requires": "ФИО или ИНН"
            },
            "fns_egrul": {
                "url": "https://egrul.nalog.ru/",
                "data": "Реестр ИП и ООО",
                "requires": "ИНН"
            },
            "2gis": {
                "url": "https://2gis.ru/",
                "data": "Справочник компаний и контактов"
            },
            "yandex_maps": {
                "url": "https://yandex.ru/maps/",
                "data": "Адреса и компании"
            },
            "avva_profiles": {
                "url": "https://avva.ru/",
                "data": "Публичные профили (ФИО, адреса, фото)"
            },
            "hh_ru": {
                "url": "https://hh.ru/",
                "data": "Резюме соискателей"
            },
            "superjob": {
                "url": "https://superjob.ru/",
                "data": "Резюме и контакты"
            }
        }
    
    def _get_api_endpoints(self) -> Dict[str, Dict[str, Any]]:
        """Available API endpoints and free services"""
        return {
            "ipqualityscore": {
                "url": "https://ipqualityscore.com/api/json/phone",
                "method": "GET",
                "free_tier": "25 requests/month",
                "data": ["operator", "valid", "number_type"]
            },
            "numverify": {
                "url": "https://numverify.com/api",
                "method": "GET",
                "free_tier": "100 requests/month",
                "data": ["country", "carrier", "line_type"]
            },
            "abstractapi_phonenumber": {
                "url": "https://api.abstractapi.com/phonenumber",
                "method": "GET",
                "free_tier": "100 requests/month",
                "data": ["type", "carrier", "country"]
            },
            "vk_api": {
                "url": "https://api.vk.com/method/",
                "note": "Requires VK API key",
                "data": ["user_search", "groups", "posts"]
            }
        }
    
    def _get_scraping_methods(self) -> Dict[str, Dict[str, Any]]:
        """Web scraping sources"""
        return {
            "truecaller_web": {
                "url": "https://www.truecaller.com/",
                "method": "web_lookup",
                "data": "ФИО, компания, категория"
            },
            "2gis_scrape": {
                "url": "https://2gis.ru/search",
                "method": "web_scrape",
                "data": "компании, контакты, сайты"
            },
            "yandex_scrape": {
                "url": "https://www.yandex.ru/search",
                "method": "dork_results",
                "data": "все открытые результаты"
            },
            "avva_scrape": {
                "url": "https://avva.ru/",
                "note": "Публичные профили с информацией о людях"
            }
        }
    
    def _get_open_sources(self) -> Dict[str, List[str]]:
        """Open source intelligence resources"""
        return {
            "forums": [
                "forums.moeginfo.com - финансовые форумы",
                "pikabu.ru - социальный контент",
                "reddit.com - обсуждения"
            ],
            "databases": [
                "haveibeenpwned.com - утечки БД",
                "dehashed.com - утечённые данные",
                "leakpeek.com - поиск по компании/email"
            ],
            "github": [
                f"github.com/search?q={quote(self.phone)} - поиск в кодах",
                "утечки паспортных данных и конфиг-файлов"
            ],
            "documents": [
                "Яндекс.Диск - публичные папки",
                "Google Drive - открытые документы",
                "Документы с номерами телефонов"
            ]
        }
    
    def get_search_plan(self) -> Dict[str, Any]:
        """Generate step-by-step search plan"""
        return {
            "step_1": {
                "name": "Google Dork поиск",
                "duration": "5-10 минут",
                "queries": self._generate_google_dorks()[:10],
                "expected_data": ["упоминания номера", "ФИО", "адреса"]
            },
            "step_2": {
                "name": "Социальные сети",
                "duration": "10-15 минут",
                "sources": ["vk.com", "ok.ru", "2gis.ru"],
                "expected_data": ["профиль", "ФИО", "фото", "город"]
            },
            "step_3": {
                "name": "Государственные БД",
                "duration": "10-15 минут",
                "sources": ["rosreestr.ru", "egrul.nalog.ru"],
                "requires": "ФИО или ИНН",
                "expected_data": ["недвижимость", "компания", "ОГРН"]
            },
            "step_4": {
                "name": "Данные агрегаторы",
                "duration": "5-10 минут",
                "sources": ["dossier.today", "intellij.ru", "avva.ru"],
                "expected_data": ["ФИО", "адреса", "ИНН", "контакты"]
            },
            "step_5": {
                "name": "Мессенджеры",
                "duration": "5 минут",
                "tools": ["WhatsApp Web", "Viber Desktop", "Telegram"],
                "expected_data": ["аватар", "статус", "online status"]
            },
            "step_6": {
                "name": "Резюме и профили",
                "duration": "5 минут",
                "sources": ["hh.ru", "superjob.ru", "linkedin.com"],
                "expected_data": ["опыт работы", "зарплата", "навыки"]
            }
        }


class GoogleDorkExecutor:
    """Execute Google Dork searches"""
    
    @staticmethod
    def execute_dork(query: str) -> str:
        """Generate Google search URL for manual execution"""
        return f"https://www.google.com/search?q={quote(query)}"
    
    @staticmethod
    def batch_dorks(dorks: List[str]) -> Dict[str, str]:
        """Generate batch of Google Dork URLs"""
        return {
            f"dork_{i+1}": GoogleDorkExecutor.execute_dork(dork)
            for i, dork in enumerate(dorks)
        }


class SocialMediaSearcher:
    """Social media profile search"""
    
    @staticmethod
    def search_all_platforms(phone: str, name: Optional[str] = None) -> Dict[str, str]:
        """Generate search URLs for all major platforms"""
        phone_encoded = quote(phone)
        
        results = {
            "vkontakte": f"https://vk.com/search?c[q]={phone_encoded}",
            "odnoklassniki": f"https://ok.ru/search?q={phone_encoded}",
            "2gis": f"https://2gis.ru/spb/search/{phone_encoded}",
            "avva": f"https://avva.ru/search?q={phone_encoded}",
            "hh_ru": f"https://hh.ru/search/vacancy?text={phone_encoded}",
        }
        
        if name:
            name_encoded = quote(name)
            results["vk_by_name"] = f"https://vk.com/search?c[section]=people&c[q]={name_encoded}"
            results["ok_by_name"] = f"https://ok.ru/search?q={name_encoded}"
            results["google_name"] = f"https://www.google.com/search?q={name_encoded}"
        
        return results


class DataAggregator:
    """Aggregate data from multiple sources"""
    
    @staticmethod
    def compile_profile(phone: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Compile complete OSINT profile"""
        engine = OSINTEngine()
        results = engine.comprehensive_search(phone)
        
        profile = {
            "phone": phone,
            "name": name,
            "search_plan": engine.get_search_plan(),
            "google_dorks": engine._generate_google_dorks(),
            "social_media": SocialMediaSearcher.search_all_platforms(phone, name),
            "russian_sources": engine._get_russian_sources(),
            "apis": engine._get_api_endpoints(),
            "open_sources": engine._get_open_sources(),
        }
        
        return profile


if __name__ == "__main__":
    # Example usage
    engine = OSINTEngine()
    phone = "+79182469659"
    
    results = engine.comprehensive_search(phone)
    search_plan = engine.get_search_plan()
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print("\n" + "="*70)
    print(json.dumps(search_plan, ensure_ascii=False, indent=2))
