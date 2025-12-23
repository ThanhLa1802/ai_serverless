import os
from openai import OpenAI
from src.common.logger import get_logger

_logger = get_logger(__name__)

class AnswerGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # model tối ưu cho RAG
        self.model = "gpt-4o-mini"

    def generate_answer(self, question: str, contexts: list[str]) -> str:
        # Ghép context
        context_text = "\n".join([f"- {c}" for c in contexts])

        prompt = f"""
        Bạn là một trợ lý AI trả lời câu hỏi dựa trên tài liệu nội bộ.

        QUY TẮC BẮT BUỘC:
        - Chỉ sử dụng thông tin trong CONTEXT.
        - Không được suy đoán hoặc dùng kiến thức bên ngoài.
        - Nếu CONTEXT không đủ thông tin, hãy trả lời:
        "Tôi không tìm thấy thông tin trong tài liệu được cung cấp."

        CONTEXT:
        {context_text}

        QUESTION:
        {question}

        ANSWER (tiếng Việt, ngắn gọn, rõ ràng):
        """

        try:
            _logger.info("Calling OpenAI API...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Bạn là trợ lý AI chuyên trả lời câu hỏi từ tài liệu."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,   # thấp để tránh bịa
                max_tokens=300    # đủ cho câu trả lời
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            _logger.error(f"OpenAI error: {str(e)}", exc_info=True)
            return "Lỗi khi tạo câu trả lời."
