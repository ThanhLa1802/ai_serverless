import json
import os
from .search import SearchService
from .generator import AnswerGenerator
from src.common.logger import get_logger

_logger = get_logger(__name__)


search_service = None
answer_generator = None

def handler(event, context):
    global search_service, answer_generator
    
    _logger.info("Query handler called")
    _logger.info(
    f"PINECONE_INDEX_NAME={os.getenv('PINECONE_INDEX_NAME')}"
)
    
    try:
        # 1. Khởi tạo service nếu chưa có
        if search_service is None:
            search_service = SearchService()
        if answer_generator is None:
            answer_generator = AnswerGenerator()

        # 2. Lấy câu hỏi từ người dùng (hỗ trợ cả gọi trực tiếp hoặc qua API Gateway)
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
            
        query_text = body.get('query') or event.get('query')
        
        if not query_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'query' in request body"})
            }

        _logger.info(f"User Question: {query_text}")

        # 3. Bước Retrieval: Tìm context liên quan từ Pinecone
        contexts = search_service.search_context(query_text, k=3)
        
        if not contexts:
            _logger.warning("No relevant context found in Pinecone.")
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "answer": "Tôi không tìm thấy thông tin liên quan trong tài liệu đã upload.",
                    "sources": []
                })
            }

        # 4. Bước Generation: Dùng gloq để tạo câu trả lời
        answer = answer_generator.generate_answer(query_text, contexts)

        # 5. Trả về kết quả
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*" # Hỗ trợ gọi từ Website (CORS)
            },
            "body": json.dumps({
                "answer": answer,
                "has_context": True,
                "context_count": len(contexts)
            }, ensure_ascii=False)
        }

    except Exception as e:
        _logger.error(f"Error in query handler: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error during query processing"})
        }