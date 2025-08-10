import os
import google.generativeai as genai
from dotenv import load_dotenv
import sqlite3

load_dotenv()

class ModelProvider:
    def __init__(self, provider="gemini", model="gemini-1.5-flash"):
        self.provider = provider
        self.model = model
        if provider == "gemini":
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.client = genai.GenerativeModel(model)

    def generate(self, prompt):
        if self.provider == "gemini":
            response = self.client.generate_content(prompt)
            return response.text
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented yet")
