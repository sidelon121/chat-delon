import os
from groq import Groq

class AIProvider:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY tidak ditemukan di environment variables")

        self.client = Groq(api_key=api_key)

    def generate_response(self, messages, temperature=0.7, max_tokens=40960):
        try:
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message["content"]
        except Exception as e:
            return f"[AI ERROR] {str(e)}"


def get_ai_provider():
    """Factory untuk membuat AI provider"""
    provider = AIProvider()
    return provider
