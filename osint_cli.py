#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SpyderOSINT - CLI Tool for Phone Number Intelligence
Complete OSINT search with integrated APIs
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.osint_engine import OSINTEngine, GoogleDorkExecutor, SocialMediaSearcher, DataAggregator
from core.free_apis import (
    FreeAPIsIntegration, RussianSourcesAPI, SocialMediaAPIs,
    DataLeaksAndBreaches, GoogleDorkResources, ToolsRegistry, OSINTAPIsRegistry
)
from utils.logger import get_logger

logger = get_logger(__name__)


class SpyderOSINTCLI:
    """Command-line interface for SpyderOSINT"""
    
    def __init__(self):
        self.engine = OSINTEngine()
        
    def run_full_search(self, phone: str, name: Optional[str] = None) -> None:
        """Execute full OSINT search"""
        print("\n" + "="*70)
        print("🔍 SPYDEROSINT - FULL OSINT SEARCH")
        print("="*70 + "\n")
        
        # 1. Basic info
        print("📱 STEP 1: Extracting basic phone information...")
        results = self.engine.comprehensive_search(phone)
        
        basic = results["basic_info"]
        print(f"""
  ✓ Phone: {basic['phone']}
  ✓ Operator: {basic['operator']}
  ✓ Country: {basic['country']}
  ✓ Type: {basic['type']}
""")
        
        # 2. Google Dorks
        print("🔍 STEP 2: Generating Google Dork queries...")
        dorks = results["google_dorks"]
        print(f"  ✓ Generated {len(dorks)} search queries\n")
        
        print("  Top 5 Google Dorks:")
        for i, dork in enumerate(dorks[:5], 1):
            url = GoogleDorkExecutor.execute_dork(dork)
            print(f"    {i}. {url[:80]}...")
        
        # 3. Social media
        print("\n👥 STEP 3: Social media search URLs...")
        socials = results["social_media_links"]
        print("  Generated links:")
        for platform, url in list(socials.items())[:5]:
            print(f"    • {platform}: {url[:70]}...")
        
        # 4. Russian sources
        print("\n🇷🇺 STEP 4: Russian data sources...")
        ru_sources = results["russian_sources"]
        print(f"  ✓ {len(ru_sources)} Russian sources available")
        for source, info in list(ru_sources.items())[:3]:
            print(f"    • {source}: {info['url']}")
        
        # 5. APIs
        print("\n🔌 STEP 5: Available APIs...")
        apis = results["api_endpoints"]
        print(f"  ✓ {len(apis)} free APIs configured")
        for api, info in list(apis.items())[:3]:
            print(f"    • {api}: {info.get('free_tier', 'Limited')}")
        
        # 6. Search plan
        print("\n📋 STEP 6: Search Plan:")
        plan = self.engine.get_search_plan()
        
        for step, details in plan.items():
            print(f"""
  {step.upper()}: {details['name']} ({details['duration']})
    Sources: {', '.join(details.get('sources', details.get('tools', [])))}
""")
        
        print("\n" + "="*70)
        print("✅ OSINT Search Complete")
        print("="*70 + "\n")
        
        # Save report
        self._save_report(phone, results)
    
    def show_google_dorks(self, phone: str) -> None:
        """Display all Google Dork queries"""
        dorks = GoogleDorkResources.get_all_templates(phone)
        
        print("\n" + "="*70)
        print("🔍 GOOGLE DORK QUERIES")
        print("="*70 + "\n")
        
        for i, dork in enumerate(dorks, 1):
            url = GoogleDorkExecutor.execute_dork(dork)
            print(f"{i:2}. Query: {dork}")
            print(f"    URL: {url}\n")
    
    def show_social_media(self, phone: str, name: Optional[str] = None) -> None:
        """Display social media search links"""
        links = SocialMediaSearcher.search_all_platforms(phone, name)
        
        print("\n" + "="*70)
        print("👥 SOCIAL MEDIA SEARCH LINKS")
        print("="*70 + "\n")
        
        for platform, url in links.items():
            print(f"{'Platform':<20} {platform}")
            print(f"{'URL':<20} {url}\n")
    
    def show_apis(self) -> None:
        """Display all integrated APIs"""
        apis = OSINTAPIsRegistry.get_all_apis()
        
        print("\n" + "="*70)
        print("🔌 INTEGRATED APIs AND SERVICES")
        print("="*70 + "\n")
        
        for category, services in apis.items():
            print(f"\n📂 {category.upper()}")
            print("-" * 70)
            for service_name, service_data in services.items():
                print(f"  • {service_name}")
                if isinstance(service_data, dict):
                    for key, value in service_data.items():
                        if not key.startswith("_"):
                            print(f"      {key}: {value}")
    
    def show_tools(self) -> None:
        """Display all recommended tools"""
        tools = ToolsRegistry.get_all_tools()
        
        print("\n" + "="*70)
        print("🛠️  RECOMMENDED OSINT TOOLS")
        print("="*70 + "\n")
        
        for tool in tools:
            print(f"📦 {tool['name']}")
            print(f"   GitHub: {tool['github']}")
            print(f"   Install: {tool['installation']}")
            print(f"   Features: {', '.join(tool['capabilities'])}\n")
    
    def _save_report(self, phone: str, results: dict) -> None:
        """Save search results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON report
        json_file = f"osint_report_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # Text report
        txt_file = f"osint_report_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("SPYDEROSINT OSINT SEARCH REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Phone: {results['phone']}\n")
            f.write(f"Search Date: {results['timestamp']}\n\n")
            
            f.write("BASIC INFO:\n")
            for key, value in results['basic_info'].items():
                f.write(f"  {key}: {value}\n")
            
            f.write("\nGOOGLE DORKS:\n")
            for i, dork in enumerate(results['google_dorks'][:10], 1):
                f.write(f"  {i}. {dork}\n")
            
            f.write("\nSOCIAL MEDIA LINKS:\n")
            for platform, url in list(results['social_media_links'].items())[:5]:
                f.write(f"  {platform}: {url}\n")
        
        print(f"\n✅ Reports saved:")
        print(f"   • JSON: {json_file}")
        print(f"   • TEXT: {txt_file}")


def main():
    parser = argparse.ArgumentParser(
        description="SpyderOSINT - Advanced OSINT Intelligence Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python osint_cli.py search +79182469659
  python osint_cli.py dorks +79182469659
  python osint_cli.py socials +79182469659 --name "Ivan Petrov"
  python osint_cli.py apis
  python osint_cli.py tools
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Execute full OSINT search')
    search_parser.add_argument('phone', help='Phone number to search')
    search_parser.add_argument('--name', help='Person name (optional)')
    
    # Google Dorks command
    dorks_parser = subparsers.add_parser('dorks', help='Show Google Dork queries')
    dorks_parser.add_argument('phone', help='Phone number')
    
    # Social media command
    socials_parser = subparsers.add_parser('socials', help='Show social media search links')
    socials_parser.add_argument('phone', help='Phone number')
    socials_parser.add_argument('--name', help='Person name (optional)')
    
    # APIs command
    subparsers.add_parser('apis', help='Show all integrated APIs')
    
    # Tools command
    subparsers.add_parser('tools', help='Show recommended OSINT tools')
    
    args = parser.parse_args()
    
    cli = SpyderOSINTCLI()
    
    if args.command == 'search':
        cli.run_full_search(args.phone, args.name)
    elif args.command == 'dorks':
        cli.show_google_dorks(args.phone)
    elif args.command == 'socials':
        cli.show_social_media(args.phone, args.name)
    elif args.command == 'apis':
        cli.show_apis()
    elif args.command == 'tools':
        cli.show_tools()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
