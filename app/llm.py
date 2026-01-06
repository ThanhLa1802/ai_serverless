from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        api_key=api_key
    )