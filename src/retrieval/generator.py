import os
import google.generativeai as genai

class AnswerGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # Sử dụng Gemini 1.5 Flash theo sơ đồ của bạn
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_answer(self, question: str, context_documents: List[str]) -> str:
        """
        Tạo câu trả lời dựa trên ngữ cảnh được cung cấp (RAG).
        """
        context_text = "\n\n".join(context_documents)
        
        prompt = f"""
        Bạn là một chuyên gia phân tích tài liệu. Hãy trả lời câu hỏi dựa trên thông tin dưới đây.
        Nếu thông tin không có trong tài liệu, hãy nói là bạn không biết, đừng tự bịa ra câu trả lời.
        
        NGỮ CẢNH (DỮ LIỆU TỪ HỆ THỐNG):
        {context_text}
        
        CÂU HỎI:
        {question}
        
        TRẢ LỜI:
        """
        
        response = self.model.generate_content(prompt)
        return response.text