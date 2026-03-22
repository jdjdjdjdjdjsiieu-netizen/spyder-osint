#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интеграция множественных ИИ моделей для OSINT анализа
Поддерживает: OpenAI, Anthropic, Groq, Ollama и другие
"""

import os
import json
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

class AIModelInterface(ABC):
    """Интерфейс для различных ИИ моделей"""
    
    @abstractmethod
    def analyze(self, prompt: str, context: Dict[str, Any]) -> str:
        """Анализировать данные"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Получить информацию о модели"""
        pass


class OpenAIModel(AIModelInterface):
    """Интеграция с OpenAI GPT"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = 'gpt-3.5-turbo'
        
    def analyze(self, prompt: str, context: Dict[str, Any]) -> str:
        """Анализ через OpenAI"""
        if not self.api_key:
            return "❌ OpenAI API ключ не найден. Установите OPENAI_API_KEY"
        
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты - эксперт по OSINT анализу"},
                    {"role": "user", "content": f"{prompt}\n\nКонтекст: {json.dumps(context)}"}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except ImportError:
            return "❌ openai модуль не установлен: pip install openai"
        except Exception as e:
            return f"❌ Ошибка OpenAI: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            'name': 'OpenAI GPT-3.5',
            'endpoint': 'https://api.openai.com/v1/chat/completions',
            'model': self.model,
            'status': '✓ Available' if self.api_key else '✗ No API key'
        }


class AnthropicModel(AIModelInterface):
    """Интеграция с Claude от Anthropic"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.model = 'claude-3-sonnet-20240229'
        
    def analyze(self, prompt: str, context: Dict[str, Any]) -> str:
        """Анализ через Claude"""
        if not self.api_key:
            return "❌ Anthropic API ключ не найден. Установите ANTHROPIC_API_KEY"
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.model,
                max_tokens=2048,
                system="Ты - эксперт по OSINT анализу и расследованиям. Анализируй данные глубоко.",
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nКонтекст: {json.dumps(context, ensure_ascii=False)}"
                    }
                ]
            )
            return response.content[0].text
        except ImportError:
            return "❌ anthropic модуль не установлен: pip install anthropic"
        except Exception as e:
            return f"❌ Ошибка Anthropic: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            'name': 'Anthropic Claude 3 Sonnet',
            'endpoint': 'https://api.anthropic.com/v1/messages',
            'model': self.model,
            'status': '✓ Available' if self.api_key else '✗ No API key'
        }


class GroqModel(AIModelInterface):
    """Интеграция с Groq для быстрого анализа"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.model = 'mixtral-8x7b-32768'
        
    def analyze(self, prompt: str, context: Dict[str, Any]) -> str:
        """Анализ через Groq"""
        if not self.api_key:
            return "❌ Groq API ключ не найден. Установите GROQ_API_KEY"
        
        try:
            from groq import Groq
            
            client = Groq(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты - эксперт OSINT. Анализируй быстро и точно."},
                    {"role": "user", "content": f"{prompt}\n\nКонтекст: {json.dumps(context)}"}
                ]
            )
            return response.choices[0].message.content
        except ImportError:
            return "❌ groq модуль не установлен: pip install groq"
        except Exception as e:
            return f"❌ Ошибка Groq: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            'name': 'Groq Mixtral 8x7B',
            'endpoint': 'https://api.groq.com/openai/v1/chat/completions',
            'model': self.model,
            'status': '✓ Available' if self.api_key else '✗ No API key'
        }


class OllamaModel(AIModelInterface):
    """Интеграция с локальным Ollama (локальные модели)"""
    
    def __init__(self, model: str = 'llama2', host: str = 'http://localhost:11434'):
        self.model = model
        self.host = host
        
    def analyze(self, prompt: str, context: Dict[str, Any]) -> str:
        """Анализ через локальный Ollama"""
        try:
            import requests
            
            response = requests.post(
                f'{self.host}/api/generate',
                json={
                    'model': self.model,
                    'prompt': f"{prompt}\n\nКонтекст: {json.dumps(context, ensure_ascii=False)}",
                    'stream': False
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"❌ Ollama ошибка: HTTP {response.status_code}"
        except requests.exceptions.ConnectionError:
            return "❌ Ollama не доступен. Запустите: ollama serve"
        except Exception as e:
            return f"❌ Ошибка Ollama: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        try:
            import requests
            response = requests.get(f'{self.host}/api/tags', timeout=5)
            available = response.status_code == 200
        except:
            available = False
        
        return {
            'name': f'Ollama {self.model}',
            'endpoint': f'{self.host}/api/generate',
            'model': self.model,
            'status': '✓ Available' if available else '✗ Not running'
        }


class MultiModelAnalyzer:
    """Анализатор с поддержкой множественных моделей"""
    
    def __init__(self):
        self.models = {
            'openai': OpenAIModel(),
            'anthropic': AnthropicModel(),
            'groq': GroqModel(),
            'ollama': OllamaModel()
        }
        self.results = {}
    
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """Получить список доступных моделей"""
        available = {}
        for name, model in self.models.items():
            info = model.get_model_info()
            if '✓ Available' in info['status'] or 'running' in info['status'].lower():
                available[name] = info
        return available
    
    def analyze_with_model(self, model_name: str, prompt: str, context: Dict[str, Any]) -> str:
        """Анализ с конкретной моделью"""
        if model_name not in self.models:
            return f"❌ Модель {model_name} не поддерживается"
        
        model = self.models[model_name]
        return model.analyze(prompt, context)
    
    def analyze_with_all_models(self, prompt: str, context: Dict[str, Any]) -> Dict[str, str]:
        """Анализ со всеми доступными моделями"""
        results = {}
        
        for name, model in self.models.items():
            print(f"🔄 Анализирую с {name}...")
            results[name] = model.analyze(prompt, context)
        
        return results


class OSINTAnalysisPipeline:
    """Полный pipeline анализа OSINT данных через множество моделей"""
    
    def __init__(self):
        self.analyzer = MultiModelAnalyzer()
    
    def analyze_phone_profile(self, phone: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализировать профиль телефона через в все доступные модели"""
        
        prompt = f"""
        Проанализируй следующий профиль телефона для OSINT исследования:
        
        Номер: {phone}
        Данные: {json.dumps(data, ensure_ascii=False)}
        
        Дай детальный анализ:
        1. Что можно узнать из этого номера?
        2. Какие источники наиболее вероятно содержат полную информацию?
        3. Какова рекомендуемая последовательность поиска?
        4. Какие риски при публикации такой информации?
        5. Какие мере защиты были бы эффективны?
        """
        
        # Получаем анализ со всех доступных моделей
        analyses = self.analyzer.analyze_with_all_models(prompt, {'phone': phone, **data})
        
        return {
            'phone': phone,
            'analyses_by_model': analyses,
            'timestamp': json.dumps({'timestamp': str(__import__('datetime').datetime.now())}),
            'available_models': self.analyzer.get_available_models()
        }


def main():
    print("\n" + "="*100)
    print("🤖 MULTI-MODEL AI OSINT ANALYZER")
    print("="*100 + "\n")
    
    # Инициализируем анализатор
    analyzer = MultiModelAnalyzer()
    
    # Показываем доступные модели
    print("📊 ДОСТУПНЫЕ ИИ МОДЕЛИ:")
    print("─"*100 + "\n")
    
    all_models = analyzer.models
    for name, model in all_models.items():
        info = model.get_model_info()
        print(f"  {name.upper()}")
        print(f"    ├─ Модель: {info['model']}")
        print(f"    ├─ Статус: {info['status']}")
        print(f"    └─ Endpoint: {info['endpoint']}\n")
    
    # Пример анализа
    print("\n🔍 ПРИМЕР АНАЛИЗА ЧЕРЕЗ МНОЖЕСТВЕННЫЕ МОДЕЛИ:")
    print("─"*100 + "\n")
    
    pipeline = OSINTAnalysisPipeline()
    
    sample_data = {
        'operator': 'Megafon',
        'country': 'Russia',
        'type': 'Mobile',
        'normalized': '+79182469659'
    }
    
    result = pipeline.analyze_phone_profile('+79182469659', sample_data)
    
    print("📋 РЕЗУЛЬТАТЫ АНАЛИЗА:\n")
    
    for model_name, analysis in result['analyses_by_model'].items():
        print(f"\n🔹 {model_name.upper()}:")
        print("─"*100)
        if analysis.startswith('❌'):
            print(f"  {analysis}")
        else:
            # Выводим первые 500 символов анализа
            preview = analysis[:500] + "..." if len(analysis) > 500 else analysis
            print(f"  {preview}")
    
    print("\n" + "="*100)
    print("✅ АНАЛИЗ ЗАВЕРШЕН")
    print("="*100 + "\n")
    
    # Сохраняем результаты
    with open('multi_model_analysis.json', 'w', encoding='utf-8') as f:
        # Очищаем чрезмерно длинный текст для JSON
        for key in result['analyses_by_model']:
            result['analyses_by_model'][key] = result['analyses_by_model'][key][:1000]
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("✅ Результаты сохранены в multi_model_analysis.json")


if __name__ == '__main__':
    main()
