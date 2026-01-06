from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class ChatState(TypedDict):
    question: str
    messages: List[BaseMessage]
    documents: List[str]
    answer: str