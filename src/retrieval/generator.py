import os
from langchain_groq import ChatGroq
from src.common.logger import get_logger

_logger = get_logger(__name__)

class AnswerGenerator:
    def __init__(self):
        # Lấy API Key từ .env (Bạn hãy thêm GROQ_API_KEY vào .env)
        api_key = os.getenv("GROQ_API_KEY")
        
        # Sử dụng model Llama 3.1 70B hoặc 8B (miễn phí và rất thông minh)
        self.llm = ChatGroq(
            temperature=0,
            model_name="llama-3.1-8b-instant",
            groq_api_key=api_key
        )

    def generate_answer(self, question, contexts):
        source_knowledge = "\n".join([f"- {c}" for c in contexts])
        
        prompt = f"""
        Bạn là một trợ lý thông minh. Hãy trả lời câu hỏi dựa vào ngữ cảnh sau:
        
        NGỮ CẢNH:
        {source_knowledge}
        
        CÂU HỎI: 
        {question}
        
        TRẢ LỜI:
        """

        try:
            _logger.info("Đang gọi Groq API...")
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            _logger.error(f"Lỗi Groq: {str(e)}")
            return "Lỗi khi tạo câu trả lời."