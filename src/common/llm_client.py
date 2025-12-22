import os
from google import genai

#use English for code comments and log messages
class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GEMINI_API_KEY in environment variables!")
        
        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, prompt: str, model_name="gemini-1.5-flash"):
        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text