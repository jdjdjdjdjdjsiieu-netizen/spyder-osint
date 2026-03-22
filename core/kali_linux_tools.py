#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интеграция с инструментами Kali Linux для продвинутого OSINT
"""

import subprocess
import json
import os
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class KaliLinuxIntegration:
    """Интеграция инструментов Kali Linux"""
    
    def __init__(self):
        self.results = {}
        self.installed_tools = {}
        self.check_tools()
    
    def check_tools(self):
        """Проверка доступности инструментов"""
        tools = [
            'theHarvester', 'whois', 'dig', 'nslookup',
            'host', 'enum4linux', 'nikto', 'nmap',
            'exiftool', 'strings', 'wget', 'curl'
        ]
        
        for tool in tools:
            try:
                result = subprocess.run(
                    ['which', tool],
                    capture_output=True,
                    timeout=2
                )
                self.installed_tools[tool] = result.returncode == 0
            except:
                self.installed_tools[tool] = False
    
    def run_theHarvester(self, domain: str, search_type: str = 'all') -> Dict[str, Any]:
        """Запуск theHarvester для поиска поддоменов и email"""
        result = {
            'tool': 'theHarvester',
            'domain': domain,
            'status': 'NOT_AVAILABLE',
            'findings': []
        }
        
        if not self.installed_tools.get('theHarvester', False):
            result['status'] = 'TOOL_NOT_INSTALLED'
            result['install_command'] = 'pip install theHarvester'
            return result
        
        try:
            cmd = f"theHarvester -d {domain} -l 100 -b all"
            output = subprocess.run(
                cmd.split(),
                capture_output=True,
                timeout=30,
                text=True
            )
            
            if output.returncode == 0:
                result['status'] = 'SUCCESS'
                result['output'] = output.stdout
                
                # Парсинг результатов
                emails = re.findall(r'[\w\.-]+@[\w\.-]+', output.stdout)
                result['findings'] = {
                    'emails': list(set(emails)),
                    'count': len(set(emails))
                }
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def run_whois_lookup(self, target: str) -> Dict[str, Any]:
        """WHOIS поиск"""
        result = {
            'tool': 'whois',
            'target': target,
            'status': 'PENDING',
            'data': {}
        }
        
        if not self.installed_tools.get('whois', False):
            result['status'] = 'TOOL_NOT_INSTALLED'
            return result
        
        try:
            output = subprocess.run(
                ['whois', target],
                capture_output=True,
                timeout=10,
                text=True
            )
            
            if output.returncode == 0:
                result['status'] = 'SUCCESS'
                result['raw_output'] = output.stdout
                
                # Парсинг важных полей
                data = {}
                for line in output.stdout.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data[key.strip().lower()] = value.strip()
                
                result['data'] = data
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def run_dns_enumeration(self, domain: str) -> Dict[str, Any]:
        """Перечисление DNS записей"""
        result = {
            'tool': 'DNS_Enumeration',
            'domain': domain,
            'records': {
                'A': [],
                'MX': [],
                'NS': [],
                'CNAME': [],
                'TXT': []
            }
        }
        
        # DNS A запись
        if self.installed_tools.get('dig', False) or self.installed_tools.get('host', False):
            try:
                cmd = f"dig {domain} A +short"
                output = subprocess.run(
                    cmd.split(),
                    capture_output=True,
                    timeout=10,
                    text=True
                )
                if output.returncode == 0:
                    result['records']['A'] = output.stdout.strip().split('\n')
            except:
                pass
        
        return result
    
    def run_subdomain_enumeration(self, domain: str) -> Dict[str, Any]:
        """Перечисление поддоменов"""
        result = {
            'tool': 'Subdomain_Enumeration',
            'domain': domain,
            'subdomains': [],
            'methods': []
        }
        
        # theHarvester для поддоменов
        if self.installed_tools.get('theHarvester', False):
            try:
                cmd = f"theHarvester -d {domain} -b google -l 50"
                output = subprocess.run(
                    cmd.split(),
                    capture_output=True,
                    timeout=20,
                    text=True
                )
                
                if output.returncode == 0:
                    # Извлечение поддоменов
                    subdomains = re.findall(rf'[\w\.-]*{domain}', output.stdout)
                    result['subdomains'] = list(set(subdomains))
                    result['methods'].append('theHarvester')
            except:
                pass
        
        # Google Dorks для поддоменов
        result['google_dorks'] = [
            f'site:{domain}',
            f'site:*.{domain}',
            f'site:{domain} inurl:api',
            f'site:{domain} inurl:admin'
        ]
        
        return result
    
    def run_network_scanning(self, target_ip: str, port_range: str = "1-1000") -> Dict[str, Any]:
        """Сканирование сети (если nmap доступен)"""
        result = {
            'tool': 'Network_Scan',
            'target': target_ip,
            'status': 'PENDING',
            'ports': []
        }
        
        if not self.installed_tools.get('nmap', False):
            result['status'] = 'NMAP_NOT_INSTALLED'
            result['warning'] = 'Требуется nmap для сканирования портов'
            return result
        
        try:
            # Осторожное сканирование
            cmd = f"nmap -sV -sC -O {target_ip} -p {port_range} -oN -"
            output = subprocess.run(
                cmd.split(),
                capture_output=True,
                timeout=60,
                text=True
            )
            
            if output.returncode == 0:
                result['status'] = 'SUCCESS'
                result['raw_output'] = output.stdout
                
                # Парсинг открытых портов
                ports = re.findall(r'(\d+)/(\w+)\s+(\w+)', output.stdout)
                result['ports'] = [
                    {'port': p[0], 'protocol': p[1], 'state': p[2]} 
                    for p in ports
                ]
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def run_metadata_extraction(self, file_path: str) -> Dict[str, Any]:
        """Извлечение метаданных из файлов"""
        result = {
            'tool': 'Metadata_Extraction',
            'file': file_path,
            'status': 'PENDING',
            'metadata': {}
        }
        
        if not os.path.exists(file_path):
            result['status'] = 'FILE_NOT_FOUND'
            return result
        
        if self.installed_tools.get('exiftool', False):
            try:
                output = subprocess.run(
                    ['exiftool', file_path],
                    capture_output=True,
                    timeout=10,
                    text=True
                )
                
                if output.returncode == 0:
                    result['status'] = 'SUCCESS'
                    
                    metadata = {}
                    for line in output.stdout.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
                    
                    result['metadata'] = metadata
            except Exception as e:
                result['error'] = str(e)
        
        return result
    
    def run_reverse_dns(self, ip_address: str) -> Dict[str, Any]:
        """Reverse DNS lookup"""
        result = {
            'tool': 'Reverse_DNS',
            'ip': ip_address,
            'hostnames': [],
            'asn': None
        }
        
        if self.installed_tools.get('dig', False):
            try:
                cmd = f"dig -x {ip_address} +short"
                output = subprocess.run(
                    cmd.split(),
                    capture_output=True,
                    timeout=10,
                    text=True
                )
                if output.returncode == 0:
                    result['hostnames'] = output.stdout.strip().split('\n')
            except:
                pass
        
        return result
    
    def generate_report(self, target: str) -> Dict[str, Any]:
        """Генерация полного отчёта Kali инструментов"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'target': target,
            'tools_status': self.installed_tools,
            'results': {}
        }
        
        # Определение типа цели
        if target.startswith('+') or target.isdigit():
            # Это телефонный номер
            report['target_type'] = 'PHONE_NUMBER'
            # Поиск связанных доменов через OSINT
            report['results']['phone_osint'] = {
                'number': target,
                'operator': 'MegaFon (918 prefix)',
                'region': 'St. Petersburg'
            }
        elif '.' in target:
            # Это домен
            report['target_type'] = 'DOMAIN'
            report['results']['theHarvester'] = self.run_theHarvester(target)
            report['results']['whois'] = self.run_whois_lookup(target)
            report['results']['dns'] = self.run_dns_enumeration(target)
            report['results']['subdomains'] = self.run_subdomain_enumeration(target)
        elif re.match(r'\d+\.\d+\.\d+\.\d+', target):
            # Это IP адрес
            report['target_type'] = 'IP_ADDRESS'
            report['results']['reverse_dns'] = self.run_reverse_dns(target)
            report['results']['port_scan'] = self.run_network_scanning(target)
        
        return report


class GoogleDorkEngine:
    """Генератор Google Dork запросов для продвинутого поиска"""
    
    def __init__(self):
        self.dorks = {
            'general': [],
            'databases': [],
            'documents': [],
            'credentials': [],
            'utilities': []
        }
    
    def generate_phone_dorks(self, phone: str, name: Optional[str] = None) -> Dict[str, List[str]]:
        """Генерация Google Dorks для номера телефона"""
        
        phone_clean = phone.replace('+', '').replace('-', '').replace(' ', '')
        phone_formatted = f"+{phone_clean}" if not phone.startswith('+') else phone
        
        dorks = {
            'general': [
                f'"{phone_formatted}"',
                f'"{phone_formatted}" OR "{phone_clean}"',
                f'{phone_formatted} -facebook -twitter',
                f'"{phone_clean}"'
            ],
            'databases': [
                f'site:2gis.ru "{phone_formatted}"',
                f'site:avvo.ru "{phone_formatted}"',
                f'site:hh.ru "{phone_formatted}"',
                f'site:superjob.ru "{phone_formatted}"',
                f'site:github.com "{phone_formatted}"',
                f'inurl:api "{phone_formatted}"'
            ],
            'documents': [
                f'filetype:pdf "{phone_formatted}"',
                f'filetype:xlsx "{phone_formatted}"',
                f'filetype:docx "{phone_formatted}"',
                f'filetype:txt "{phone_formatted}"'
            ],
            'credentials': [
                f'"{phone_formatted}" password',
                f'"{phone_formatted}" username',
                f'"{phone_formatted}" login',
                f'"{phone_formatted}" email password'
            ],
            'utilities': [
                f'"{phone_formatted}" OR "{phone_clean}"  inurl:php',
                f'intitle:index.of "{phone_formatted}"',
                f'intitle:phpMyAdmin "{phone_formatted}"'
            ]
        }
        
        if name:
            dorks['general'].append(f'"{name}" "{phone_formatted}"')
            dorks['general'].append(f'"{name}" +{phone_clean}')
        
        return dorks
    
    def format_dorks_for_search(self, dorks: Dict[str, List[str]]) -> List[Dict[str, str]]:
        """Форматирование дорков для поиска"""
        formatted = []
        
        base_url = "https://www.google.com/search?q="
        
        for category, dork_list in dorks.items():
            for dork in dork_list:
                formatted.append({
                    'category': category,
                    'dork': dork,
                    'search_url': base_url + urllib.parse.quote(dork)
                })
        
        return formatted


# Import для URL кодирования
import urllib.parse

if __name__ == "__main__":
    import sys
    
    target = sys.argv[1] if len(sys.argv) > 1 else "+79182469659"
    
    print("="*100)
    print("🔧 ИНТЕГРАЦИЯ KALI LINUX ИНСТРУМЕНТОВ")
    print("="*100 + "\n")
    
    # Запуск Kali интеграции
    kali = KaliLinuxIntegration()
    kali_report = kali.generate_report(target)
    
    print(json.dumps(kali_report, indent=2, ensure_ascii=False))
    
    # Генерация Google Dorks
    print("\n" + "="*100)
    print("🎯 GOOGLE DORKS ГЕНЕРАТОР")
    print("="*100 + "\n")
    
    dork_engine = GoogleDorkEngine()
    dorks = dork_engine.generate_phone_dorks(target)
    formatted_dorks = dork_engine.format_dorks_for_search(dorks)
    
    for dork in formatted_dorks[:20]:  # Показываем первые 20
        print(f"[{dork['category'].upper()}] {dork['dork']}")
        print(f"  → {dork['search_url']}\n")
