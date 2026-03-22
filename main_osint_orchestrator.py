#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главный OSINT оркестр - запуск всех систем поиска
"""

import json
import sys
from datetime import datetime

# Импорт всех систем
from core.real_search_system import RealPhoneSearchSystem
from core.advanced_agent_orchestrator import AgentOrchestrator
from core.advanced_osint_engine import AdvancedOSINTEngine
from core.kali_linux_tools import KaliLinuxIntegration, GoogleDorkEngine


def main():
    """Главная функция оркестра"""
    
    if len(sys.argv) < 2:
        print("Usage: python3 main_osint_orchestrator.py <phone_number> [name]")
        print("Example: python3 main_osint_orchestrator.py +79182469659 'Ivan Petrov'")
        sys.exit(1)
    
    phone = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("\n" + "█"*130)
    print("█" + " "*128 + "█")
    print("█" + "🔥 ПОЛНАЯ OSINT СИСТЕМА - ПОИСК ВСЕХ ТИПОВ 🔥".center(128) + "█")
    print("█" + f"Номер: {phone} | Имя: {name or 'Unknown'} | Время: {datetime.now()}".center(128) + "█")
    print("█" + " "*128 + "█")
    print("█"*130 + "\n")
    
    final_report = {
        'timestamp': datetime.now().isoformat(),
        'target': {
            'phone': phone,
            'name': name
        },
        'all_searches': {}
    }
    
    # ===== СИСТЕМА 1: Реальный поиск (прямой, обратный, DNS, WHOIS, БД) =====
    print("\n" + "▓"*130)
    print("▓ СИСТЕМА 1: ПОЛНЫЙ ПОИСК (Прямой + Обратный + DNS + WHOIS + БД + Социальные сети)")
    print("▓"*130 + "\n")
    
    try:
        searcher = RealPhoneSearchSystem()
        search_report = searcher.generate_full_report(phone, name)
        final_report['all_searches']['real_search_system'] = search_report
        searcher.save_report(search_report)
    except Exception as e:
        print(f"❌ Ошибка в системе поиска: {e}")
        final_report['all_searches']['real_search_system'] = {'error': str(e)}
    
    # ===== СИСТЕМА 2: Оркестр специализированных агентов =====
    print("\n" + "▓"*130)
    print("▓ СИСТЕМА 2: ОРКЕСТР СПЕЦИАЛИЗИРОВАННЫХ АГЕНТОВ")
    print("▓"*130 + "\n")
    
    try:
        orchestrator = AgentOrchestrator()
        agent_results = orchestrator.execute_all_agents(phone)
        agent_report = orchestrator.generate_final_report(phone)
        final_report['all_searches']['agent_orchestrator'] = agent_report
        orchestrator.save_report(agent_report)
    except Exception as e:
        print(f"❌ Ошибка в оркестре агентов: {e}")
        final_report['all_searches']['agent_orchestrator'] = {'error': str(e)}
    
    # ===== СИСТЕМА 3: Продвинутый OSINT движок =====
    print("\n" + "▓"*130)
    print("▓ СИСТЕМА 3: ПРОДВИНУТЫЙ OSINT ДВИЖОК")
    print("▓"*130 + "\n")
    
    try:
        engine = AdvancedOSINTEngine()
        engine_report = engine.generate_comprehensive_report(phone)
        final_report['all_searches']['advanced_engine'] = engine_report
        engine.save_report()
    except Exception as e:
        print(f"❌ Ошибка в OSINT движке: {e}")
        final_report['all_searches']['advanced_engine'] = {'error': str(e)}
    
    # ===== СИСТЕМА 4: Kali Linux инструменты и Google Dorks =====
    print("\n" + "▓"*130)
    print("▓ СИСТЕМА 4: KALI LINUX ИНСТРУМЕНТЫ И GOOGLE DORKS")
    print("▓"*130 + "\n")
    
    try:
        kali = KaliLinuxIntegration()
        kali_report = kali.generate_report(phone)
        final_report['all_searches']['kali_tools'] = kali_report
        
        # Google Dorks
        dork_engine = GoogleDorkEngine()
        dorks = dork_engine.generate_phone_dorks(phone, name)
        final_report['all_searches']['google_dorks'] = dorks
        
        print(json.dumps(kali_report, indent=2, ensure_ascii=False)[:500])
    except Exception as e:
        print(f"❌ Ошибка в Kali инструментах: {e}")
        final_report['all_searches']['kali_tools'] = {'error': str(e)}
    
    # ===== ФИНАЛЬНЫЙ ОТЧЁТ =====
    print("\n" + "█"*130)
    print("█" + " "*128 + "█")
    print("█" + "✅ ПОЛНЫЙ OSINT ПОИСК ЗАВЕРШЕН ✅".center(128) + "█")
    print("█" + " "*128 + "█")
    print("█"*130 + "\n")
    
    # Сохранение финального отчёта
    final_filename = f"FINAL_OSINT_REPORT_{phone.replace('+', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(final_filename, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Все отчёты сохранены:")
    print(f"   • ФИНАЛЬНЫЙ: {final_filename}")
    print(f"   • Отчеты в папке: /workspaces/spyder-osint/\n")
    
    # Выводим рекомендации
    print("📋 РЕКОМЕНДУЕМЫЕ ДАЛЬНЕЙШИЕ ДЕЙСТВИЯ:")
    print("-" * 130)
    print("""
1. ✅ Проверить все Google Dork запросы вручную
2. ✅ Перейти на все найденные социальные сети
3. ✅ Проверить в DeHashed и Have I Been Pwned
4. ✅ Выполнить обратный поиск по найденным email/имену
5. ✅ Проверить 2GIS и Яндекс.Карты для адресов
6. ✅ Изучить найденные документы (PDF, XLSX, DOCX)
7. ✅ Мониторить даркнет на упоминания
8. ✅ Выполнить анализ географии по IP
    """)
    
    print("="*130)
    print("✨ СИСТЕМА ПОЛНОСТЬЮ ГОТОВА К ИСПОЛЬЗОВАНИЮ ✨")
    print("="*130 + "\n")
    
    return final_report


if __name__ == "__main__":
    final_report = main()
