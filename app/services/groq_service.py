import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_content(self, model: str, messages: list, temperature: float = 0.7):
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            response.raise_for_status()
