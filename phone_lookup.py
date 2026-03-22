#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phone number lookup script for Russian numbers
"""

import re
import json
from core.validator import Validator
from core.processor import Processor


def parse_russian_phone(phone: str) -> dict:
    """
    Parse Russian phone number format
    Russian numbers: +7 9XX XXX XX XX
    """
    # Normalize: remove spaces, dashes, parentheses
    normalized = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Remove leading +
    if normalized.startswith('+'):
        normalized = normalized[1:]
    
    # Check if it's Russian number (starts with 7)
    if not normalized.startswith('7'):
        return {"error": "Not a Russian number"}
    
    # Extract operator code (first digit after country code)
    if len(normalized) < 11:
        return {"error": "Invalid phone length"}
    
    country_code = normalized[0]  # 7
    operator_code = normalized[1:4]  # 918
    
    # Russian mobile operators mapping
    operators = {
        '910': 'MegaFon', '911': 'MegaFon', '912': 'MegaFon', '913': 'MegaFon', '914': 'MegaFon',
        '915': 'MegaFon', '916': 'MegaFon', '917': 'MegaFon', '918': 'MegaFon', '919': 'MegaFon',
        '921': 'Beeline', '922': 'Beeline', '923': 'Beeline', '924': 'Beeline', '925': 'Beeline',
        '926': 'Beeline', '927': 'Beeline', '928': 'Beeline', '929': 'Beeline',
        '930': 'Vivo', '931': 'Vivo', '932': 'Vivo', '933': 'Vivo', '934': 'Vivo',
        '935': 'Vivo', '936': 'Vivo', '937': 'Vivo', '938': 'Vivo', '939': 'Vivo',
        '950': 'Rostelecom', '951': 'Rostelecom', '952': 'Rostelecom', '953': 'Rostelecom',
        '901': 'Megafon', '902': 'Beeline', '903': 'Beeline', '904': 'Vivo', '905': 'Megafon',
    }
    
    info = {
        "phone": phone,
        "normalized": f"+{normalized}",
        "country_code": country_code,
        "country": "Russia",
        "operator_code": operator_code,
        "operator": operators.get(operator_code, "Unknown operator"),
        "number_type": "Mobile",
    }
    
    # Extract region from first 4 digits (ABC region coding)
    first_4 = operator_code + normalized[4]
    
    regions = {
        '9181': 'Moscow region', '9182': 'St. Petersburg region', '9183': 'Leningrad region',
        '9184': 'Novgorod region', '9185': 'Smolensk region', '9186': 'Tver region',
        '9187': 'Yaroslavl region', '9188': 'Ivanovo region', '9189': 'Kostroma region',
    }
    
    info["region"] = regions.get(first_4, "Russia (specific region unknown)")
    
    return info


def lookup_phone(phone: str) -> dict:
    """Main phone lookup function"""
    print(f"\n[*] Searching for information about {phone}...\n")
    
    # Validate
    validator = Validator()
    is_valid, error = validator.validate(phone, "phone")
    
    if not is_valid:
        print(f"[!] Validation error: {error}")
        return {"error": error}
    
    # Parse Russian phone
    result = parse_russian_phone(phone)
    
    # Process through OSINT pipeline
    processor = Processor()
    processed = processor.process(phone, "phone")
    
    # Merge results
    result.update(processed)
    
    return result


def display_results(data: dict, indent: int = 0):
    """Pretty print results"""
    prefix = "  " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{prefix}{key}:")
            display_results(value, indent + 1)
        elif isinstance(value, list):
            print(f"{prefix}{key}: {json.dumps(value, ensure_ascii=False, indent=1)}")
        else:
            print(f"{prefix}{key}: {value}")


def main():
    # Example: +79182469659
    phone = "+79182469659"
    
    result = lookup_phone(phone)
    
    print("=" * 60)
    print("PHONE LOOKUP RESULTS")
    print("=" * 60)
    display_results(result)
    print("=" * 60)
    
    # Save to JSON
    output_file = "phone_lookup_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n[+] Results saved to {output_file}")


if __name__ == "__main__":
    main()
