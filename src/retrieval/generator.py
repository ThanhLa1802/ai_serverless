import os
from google import genai
from src.common.logger import get_logger

# Khởi tạo logger để theo dõi quá trình tạo câu trả lời
_logger = get_logger(__name__)

class AnswerGenerator:
    def __init__(self):
        # Lấy API Key từ biến môi trường
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            _logger.error("Thiếu GEMINI_API_KEY trong biến môi trường!")
            raise ValueError("Thiếu GEMINI_API_KEY")
        
        # Khởi tạo Client mới theo chuẩn thư viện google-genai
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-1.5-flash"

    def generate_answer(self, question: str, context_documents: list) -> str:
        """
        Tạo câu trả lời dựa trên ngữ cảnh được cung cấp (RAG) sử dụng google-genai Client.
        """
        try:
            # Gộp các tài liệu tìm kiếm được thành một đoạn văn bản ngữ cảnh
            context_text = "\n\n".join(context_documents)
            
            # Xây dựng prompt chuyên nghiệp cho RAG
            prompt = f"""
            Bạn là một chuyên gia phân tích tài liệu. Hãy trả lời câu hỏi dựa trên thông tin dưới đây.
            Nếu thông tin không có trong tài liệu, hãy nói là bạn không biết, đừng tự bịa ra câu trả lời.
            
            NGỮ CẢNH (DỮ LIỆU TỪ HỆ THỐNG):
            {context_text}
            
            CÂU HỎI:
            {question}
            
            TRẢ LỜI:
            """
            
            _logger.info(f"Đang gửi yêu cầu tạo câu trả lời tới model: {self.model_id}")

            # Gọi API theo cú pháp của thư viện mới
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )

            if not response.text:
                _logger.warning("Model trả về kết quả rỗng.")
                return "Xin lỗi, tôi không tìm thấy thông tin phù hợp trong tài liệu."

            return response.text

        except Exception as e:
            _logger.error(f"Lỗi khi gọi Gemini API: {str(e)}", exc_info=True)
            return f"Đã xảy ra lỗi khi xử lý câu hỏi: {str(e)}"