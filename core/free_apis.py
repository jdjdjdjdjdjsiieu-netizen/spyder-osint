#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Free APIs and Public Services Integration
"""

import requests
import json
from typing import Dict, Any, Optional, List
from utils.logger import get_logger

logger = get_logger(__name__)


class FreeAPIsIntegration:
    """Integration with free OSINT APIs"""
    
    class IPQualityScore:
        """IPQualityScore - Phone & IP verification"""
        BASE_URL = "https://ipqualityscore.com/api/json/phone"
        FREE_TIER = "25 requests/month"
        
        @staticmethod
        def validate_phone(phone: str) -> Dict[str, Any]:
            """
            Validate phone number using IPQualityScore
            Requires: Free API key (register at ipqualityscore.com)
            """
            # This is example - requires API key
            return {
                "service": "IPQualityScore",
                "status": "requires_api_key",
                "free_tier": "25 requests/month",
                "url": "https://ipqualityscore.com/api/json/phone",
                "note": "Register at ipqualityscore.com for free tier"
            }
    
    class AbstractAPI:
        """AbstractAPI - Phone validation and lookup"""
        BASE_URL = "https://api.abstractapi.com/phonenumber"
        FREE_TIER = "100 requests/month"
        
        @staticmethod
        def get_info(phone: str, api_key: Optional[str] = None) -> Dict[str, Any]:
            """
            Get phone information from AbstractAPI
            Free tier: 100 requests/month
            """
            return {
                "service": "AbstractAPI",
                "status": "requires_api_key",
                "free_tier": "100 requests/month",
                "url": "https://api.abstractapi.com/phonenumber",
                "signup_url": "https://www.abstractapi.com/phonenumber-validation-api",
                "data_available": ["type", "carrier", "country", "timezone"]
            }
    
    class NumVerify:
        """NumVerify - Phone validation"""
        BASE_URL = "https://numverify.com/api"
        FREE_TIER = "100 requests/month"
        
        @staticmethod
        def validate(phone: str, api_key: Optional[str] = None) -> Dict[str, Any]:
            """Basic phone validation data"""
            return {
                "service": "NumVerify",
                "status": "requires_api_key",
                "free_tier": "100 requests/month",
                "url": "https://numverify.com/api",
                "data_available": ["country", "carrier", "line_type"]
            }


class RussianSourcesAPI:
    """Integration with Russian data sources"""
    
    class FHSRegistry:
        """Federal Tax Service (ФНС) - Company registry"""
        URL = "https://egrul.nalog.ru/"
        
        @staticmethod
        def search_by_inn(inn: str) -> Dict[str, Any]:
            """
            Search company by INN in Federal Tax Service registry
            Free and public
            """
            return {
                "service": "ФНС ЕГРЮЛ",
                "url": "https://egrul.nalog.ru/",
                "search_url": "https://egrul.nalog.ru/index.html",
                "requires": "ИНН",
                "data": ["Компания", "ОГРН", "Директор", "Адрес", "Статус"],
                "access": "Свободный доступ"
            }
    
    class Rosreestr:
        """Rosreestr - Real estate registry"""
        URL = "https://www.rosreestr.ru/"
        
        @staticmethod
        def property_search() -> Dict[str, Any]:
            """Search properties by owner"""
            return {
                "service": "Росреестр",
                "url": "https://www.rosreestr.ru/",
                "info": "Реестр недвижимости",
                "requires": "ФИО или ИНН владельца",
                "data": ["Адреса", "Размер участков", "Право собственности"],
                "access": "Свободный доступ"
            }
    
    class TwoGIS:
        """2GIS - Business directory"""
        URL = "https://2gis.ru/"
        
        @staticmethod
        def phone_search(phone: str) -> Dict[str, Any]:
            """Search phone in 2GIS business directory"""
            return {
                "service": "2ГИС",
                "url": "https://2gis.ru/",
                "search_url": f"https://2gis.ru/spb/search/{phone}",
                "data": ["Компании", "Контакты", "Адреса", "Сайты"],
                "access": "Свободный доступ"
            }
    
    class AVVA:
        """AVVA - Public people database"""
        URL = "https://avva.ru/"
        
        @staticmethod
        def search_person() -> Dict[str, Any]:
            """Search person in AVVA public database"""
            return {
                "service": "AVVA",
                "url": "https://avva.ru/",
                "info": "Публичные профили людей",
                "data": ["ФИО", "Возраст", "Город", "Профессия", "Фото"],
                "access": "Свободный доступ"
            }
    
    class HeadHunter:
        """HeadHunter - Job portal with CVs"""
        URL = "https://hh.ru/"
        
        @staticmethod
        def cv_search() -> Dict[str, Any]:
            """Search CVs by phone"""
            return {
                "service": "HeadHunter",
                "url": "https://hh.ru/",
                "info": "Поиск резюме соискателей",
                "data": ["Опыт работы", "Зарплата", "Образование", "Контакты"],
                "access": "Свободный доступ"
            }


class SocialMediaAPIs:
    """Social media integration"""
    
    class VKontakte:
        """VKontakte social network"""
        API_URL = "https://api.vk.com/method/"
        WEB_URL = "https://vk.com/"
        
        @staticmethod
        def web_search_profile(phone: str) -> Dict[str, Any]:
            """Web search profile by phone"""
            return {
                "service": "ВКонтакте",
                "method": "web_search",
                "url": f"https://vk.com/search?c[q]={phone}",
                "api_method": "Requires VK API token",
                "data": ["Профиль", "ФИО", "Возраст", "Город", "Работа"]
            }
    
    class Telegram:
        """Telegram messenger"""
        
        @staticmethod
        def username_search() -> Dict[str, Any]:
            """Search Telegram username"""
            return {
                "service": "Telegram",
                "method": "username_search",
                "tools": ["@username_bot", "Telegram API"],
                "url": "https://t.me/username_bot",
                "data": ["Профиль", "ФИО", "Username", "Bio"]
            }
    
    class Instagram:
        """Instagram social network"""
        
        @staticmethod
        def username_search() -> Dict[str, Any]:
            """Search Instagram by username"""
            return {
                "service": "Instagram",
                "method": "username_search",
                "url": "https://www.instagram.com/",
                "data": ["Профиль", "Фото", "Подписчики", "Bio"]
            }


class DataLeaksAndBreaches:
    """Data breach and leak databases"""
    
    class HaveIBeenPwned:
        """HaveIBeenPwned - Breach database search"""
        URL = "https://haveibeenpwned.com/"
        API = "https://haveibeenpwned.com/api/v3/"
        
        @staticmethod
        def search_email(email: str) -> Dict[str, Any]:
            """Search if email was compromised"""
            return {
                "service": "HaveIBeenPwned",
                "url": "https://haveibeenpwned.com/",
                "api": "https://haveibeenpwned.com/api/v3/",
                "search_type": "email",
                "free_tier": "Unlimited with rate limiting",
                "data": ["Утечённые сервисы", "Дата утечки", "Пароли"]
            }
    
    class DeHashed:
        """DeHashed - Leaked data search"""
        URL = "https://www.dehashed.com/"
        
        @staticmethod
        def search() -> Dict[str, Any]:
            """Search leaked data by email or phone"""
            return {
                "service": "DeHashed",
                "url": "https://www.dehashed.com/",
                "free_tier": "Limited (5 searches/day free)",
                "data": ["Утечённые пароли", "Email", "Телефон", "ФИО"]
            }


class GoogleDorkResources:
    """Google Dork search query templates"""
    
    TEMPLATES = {
        "direct_search": '"{phone}"',
        "passport_search": '"{phone}" паспорт',
        "inn_search": '"{phone}" ИНН',
        "bank_search": '"{phone}" банк',
        "card_search": '"{phone}" карта',
        "documents": '"{phone}" документы',
        "cv": '"{phone}" резюме',
        "forum_mentions": 'site:forums.moeginfo.com "{phone}"',
        "2gis": 'site:2gis.ru "{phone}"',
        "vk": 'site:vk.com "{phone}"',
        "github": 'site:github.com "{phone}"',
        "pdf": '"{phone}" filetype:pdf',
    }
    
    @staticmethod
    def get_all_templates(phone: str) -> List[str]:
        """Generate all Google Dork queries for phone"""
        return [query.format(phone=phone) for query in GoogleDorkResources.TEMPLATES.values()]


class ToolsRegistry:
    """Registry of all integrated tools and their capabilities"""
    
    TOOLS = {
        "sherlock": {
            "name": "Sherlock - Social Media Search",
            "github": "https://github.com/sherlock-project/sherlock",
            "installation": "pip install sherlock-project",
            "usage": "python -m sherlock username",
            "capabilities": ["Search 360+ platforms", "Username lookup"]
        },
        "theHarvester": {
            "name": "theHarvester - Email & Subdomain",
            "github": "https://github.com/laramies/theHarvester",
            "installation": "pip install theHarvester",
            "capabilities": ["Email harvesting", "Subdomain enumeration"]
        },
        "spiderfoot": {
            "name": "SpiderFoot - OSINT Framework",
            "github": "https://github.com/smicallef/spiderfoot",
            "installation": "pip install spiderfoot",
            "capabilities": ["Phone analysis", "200+ data sources"]
        },
        "twint": {
            "name": "Twint - Twitter OSINT",
            "github": "https://github.com/twintproject/twint",
            "installation": "pip install twint",
            "capabilities": ["Twitter scrape", "Account analysis"]
        }
    }
    
    @staticmethod
    def get_all_tools() -> List[Dict[str, Any]]:
        """Get all available tools"""
        return list(ToolsRegistry.TOOLS.values())


class OSINTAPIsRegistry:
    """Complete registry of OSINT APIs"""
    
    @staticmethod
    def get_all_apis() -> Dict[str, Dict[str, Any]]:
        """Get all configured APIs"""
        return {
            "phone_validation": {
                "IPQualityScore": FreeAPIsIntegration.IPQualityScore.validate_phone("+79182469659"),
                "AbstractAPI": FreeAPIsIntegration.AbstractAPI.get_info("+79182469659"),
                "NumVerify": FreeAPIsIntegration.NumVerify.validate("+79182469659")
            },
            "russian_sources": {
                "ФНС_ЕГРЮЛ": RussianSourcesAPI.FHSRegistry.search_by_inn("123456789012"),
                "Росреестр": RussianSourcesAPI.Rosreestr.property_search(),
                "2ГИС": RussianSourcesAPI.TwoGIS.phone_search("+79182469659"),
                "AVVA": RussianSourcesAPI.AVVA.search_person(),
                "HeadHunter": RussianSourcesAPI.HeadHunter.cv_search()
            },
            "social_media": {
                "ВКонтакте": SocialMediaAPIs.VKontakte.web_search_profile("+79182469659"),
                "Telegram": SocialMediaAPIs.Telegram.username_search(),
                "Instagram": SocialMediaAPIs.Instagram.username_search()
            },
            "breaches": {
                "HaveIBeenPwned": DataLeaksAndBreaches.HaveIBeenPwned.search_email("example@email.com"),
                "DeHashed": DataLeaksAndBreaches.DeHashed.search()
            }
        }


if __name__ == "__main__":
    # Display all available APIs
    apis = OSINTAPIsRegistry.get_all_apis()
    print(json.dumps(apis, ensure_ascii=False, indent=2))
