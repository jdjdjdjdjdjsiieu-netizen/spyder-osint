#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sherlock Integration for SpyderOSINT
Search for usernames across 360+ social media platforms
"""

import json
import subprocess
import sys
from typing import Dict, List, Any
from pathlib import Path

from utils.logger import get_logger

logger = get_logger(__name__)


class SherlockIntegration:
    """Integration with Sherlock username search tool"""
    
    @staticmethod
    def is_installed() -> bool:
        """Check if Sherlock is installed"""
        try:
            __import__('sherlock')
            return True
        except ImportError:
            return False
    
    @staticmethod
    def install() -> bool:
        """Install Sherlock"""
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sherlock-project'])
            logger.info("Sherlock installed successfully")
            return True
        except subprocess.CalledProcessError:
            logger.error("Failed to install Sherlock")
            return False
    
    @staticmethod
    def search_username(username: str, json_output: bool = True) -> Dict[str, Any]:
        """
        Search username across platforms using Sherlock
        
        Args:
            username: Username to search
            json_output: Return as JSON
            
        Returns:
            Dictionary with search results
        """
        if not SherlockIntegration.is_installed():
            logger.warning("Sherlock not installed. Install with: pip install sherlock-project")
            return {
                "status": "not_installed",
                "message": "Install Sherlock: pip install sherlock-project",
                "manual_search": f"https://www.google.com/search?q={username}"
            }
        
        try:
            from sherlock import sherlock
            from sherlock.result import QueryStatus
            
            # Search
            results = sherlock.sherlock(
                username=username,
                verbose=False,
                json_output=json_output
            )
            
            # Format results
            formatted = {
                "username": username,
                "platforms_found": [],
                "profiles": {}
            }
            
            for site, status in results.items():
                if status[0] == QueryStatus.FOUND:
                    formatted["platforms_found"].append(site)
                    formatted["profiles"][site] = {
                        "url": status[1]["url"],
                        "status": "found"
                    }
            
            return formatted
            
        except Exception as e:
            logger.error(f"Sherlock search error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    @staticmethod
    def batch_search(usernames: List[str]) -> Dict[str, Any]:
        """Search multiple usernames"""
        results = {}
        for username in usernames:
            results[username] = SherlockIntegration.search_username(username)
        return results


class UsernameExtractor:
    """Extract possible usernames from phone and name data"""
    
    @staticmethod
    def generate_from_name(first_name: str, last_name: str) -> List[str]:
        """Generate possible usernames from name"""
        usernames = []
        
        # Various combinations
        usernames.append(f"{first_name.lower()}{last_name.lower()}")
        usernames.append(f"{first_name.lower()}.{last_name.lower()}")
        usernames.append(f"{first_name.lower()}_{last_name.lower()}")
        usernames.append(f"{first_name.lower()]}{last_name[0].lower()}")
        usernames.append(f"{first_name[0].lower()}{last_name.lower()}")
        usernames.append(f"{last_name.lower()}{first_name.lower()}")
        
        return list(set(usernames))
    
    @staticmethod
    def extract_from_email(email: str) -> List[str]:
        """Extract username from email"""
        if '@' in email:
            return [email.split('@')[0]]
        return []
    
    @staticmethod
    def common_variants(base: str) -> List[str]:
        """Generate common username variants"""
        variants = [base]
        
        # Add numbers
        for i in range(100):
            variants.append(f"{base}{i}")
            variants.append(f"{base}{i:02d}")
        
        return variants[:10]  # Limit to 10 most common


class SocialMediaSearcher:
    """Advanced social media search"""
    
    PLATFORMS = {
        "vkontakte_web": {
            "url": "https://vk.com/search?c[q]={query}",
            "type": "phone_search"
        },
        "2gis": {
            "url": "https://2gis.ru/spb/search/{query}",
            "type": "phone_search"
        },
        "yandex": {
            "url": "https://yandex.ru/search/?text={query}",
            "type": "general_search"
        },
        "google": {
            "url": "https://www.google.com/search?q={query}",
            "type": "general_search"
        },
        "avva": {
            "url": "https://avva.ru/search?q={query}",
            "type": "people_search"
        },
        "hh": {
            "url": "https://hh.ru/search/vacancy?text={query}",
            "type": "resume_search"
        }
    }
    
    @staticmethod
    def search_all_platforms(query: str) -> Dict[str, str]:
        """Generate search URLs for all platforms"""
        results = {}
        for platform, config in SocialMediaSearcher.PLATFORMS.items():
            results[platform] = config["url"].format(query=query)
        return results


if __name__ == "__main__":
    # Example usage
    print("Testing Sherlock Integration...")
    
    # Check if installed
    if SherlockIntegration.is_installed():
        print("✓ Sherlock is installed")
    else:
        print("✗ Sherlock not installed")
        print("Installing Sherlock...")
        SherlockIntegration.install()
    
    # Example search
    print("\nSearching username 'ivan_petrov'...")
    results = SherlockIntegration.search_username("ivan_petrov")
    print(json.dumps(results, indent=2, ensure_ascii=False))
