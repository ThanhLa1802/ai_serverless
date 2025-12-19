import os
import google.generativeai as genai

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Thiếu GEMINI_API_KEY trong biến môi trường!")
        genai.configure(api_key=self.api_key)

    def get_model(self, model_name="gemini-1.5-flash"):
        return genai.GenerativeModel(model_name)