import os
from abc import ABC, abstractmethod
from typing import Optional


class AIProvider(ABC):
    """Base class untuk semua AI providers"""
    
    @abstractmethod
    def generate_response(self, messages: list, temperature: float = 0.7, max_tokens: int = 300000000000) -> str:
        """Generate response dari AI"""
        pass


class OpenAIProvider(AIProvider):
    """Provider untuk OpenAI (ChatGPT)"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("openai package tidak terinstall. Install dengan: pip install openai")
    
    def generate_response(self, messages: list, temperature: float = 0.7, max_tokens: int = 3000) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI Error: {str(e)}")


class DeepSeekProvider(AIProvider):
    """Provider untuk DeepSeek"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        try:
            from openai import OpenAI
            # DeepSeek menggunakan OpenAI-compatible API
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            self.model = model
        except ImportError:
            raise ImportError("openai package tidak terinstall. Install dengan: pip install openai")
    
    def generate_response(self, messages: list, temperature: float = 0.7, max_tokens: int = 3000) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"DeepSeek Error: {str(e)}")


class GroqProvider(AIProvider):
    """Provider untuk Groq (existing)"""
    
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        try:
            from groq import Groq
            self.client = Groq(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("groq package tidak terinstall. Install dengan: pip install groq")
    
    def generate_response(self, messages: list, temperature: float = 0.7, max_tokens: int = 3000000) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq Error: {str(e)}")


class AnthropicProvider(AIProvider):
    """Provider untuk Anthropic Claude"""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("anthropic package tidak terinstall. Install dengan: pip install anthropic")
    
    def generate_response(self, messages: list, temperature: float = 0.7, max_tokens: int = 3000) -> str:
        try:
            # Anthropic menggunakan format yang berbeda
            system_message = None
            conversation_messages = []
            
            for msg in messages:
                if msg.get("role") == "system":
                    system_message = msg.get("content", "")
                else:
                    conversation_messages.append({
                        "role": msg.get("role"),
                        "content": msg.get("content", "")
                    })
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message if system_message else "You are a helpful assistant.",
                messages=conversation_messages
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic Error: {str(e)}")


def get_ai_provider(provider_name: str = None, api_key: str = None, model: str = None) -> AIProvider:
    """
    Factory function untuk mendapatkan AI provider berdasarkan konfigurasi
    
    Args:
        provider_name: Nama provider ('openai', 'deepseek', 'groq', 'anthropic')
        api_key: API key untuk provider
        model: Nama model yang akan digunakan
    
    Returns:
        Instance dari AIProvider
    """
    # Jika provider_name tidak diberikan, ambil dari environment variable
    if not provider_name:
        provider_name = os.getenv("AI_PROVIDER", "groq").lower()
    
    # Jika api_key tidak diberikan, ambil dari environment variable berdasarkan provider
    if not api_key:
        provider_key_map = {
            "openai": "OPENAI_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "groq": "GROQ_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY"
        }
        env_key = provider_key_map.get(provider_name)
        if env_key:
            api_key = os.getenv(env_key)
    
    if not api_key:
        raise ValueError(f"❌ API key untuk {provider_name} tidak ditemukan! Pastikan file .env sudah dibuat.")
    
    # Jika model tidak diberikan, ambil dari environment variable atau gunakan default
    if not model:
        model = os.getenv(f"{provider_name.upper()}_MODEL")
    
    # Mapping provider names ke class
    provider_map = {
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider,
        "groq": GroqProvider,
        "anthropic": AnthropicProvider,
    }
    
    provider_class = provider_map.get(provider_name)
    if not provider_class:
        raise ValueError(f"❌ Provider '{provider_name}' tidak didukung! Pilih dari: {', '.join(provider_map.keys())}")
    
    # Default models untuk setiap provider
    default_models = {
        "openai": "gpt-3.5-turbo",
        "deepseek": "deepseek-chat",
        "groq": "llama-3.1-8b-instant",
        "anthropic": "claude-3-5-sonnet-20241022",
    }
    
    if not model:
        model = default_models.get(provider_name)
    
    try:
        return provider_class(api_key=api_key, model=model)
    except Exception as e:
        raise Exception(f"❌ Gagal menginisialisasi {provider_name}: {str(e)}")
