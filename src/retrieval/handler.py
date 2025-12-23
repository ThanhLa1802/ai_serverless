import json
from src.retrieval.search import get_answer_from_query
from src.common.logger import get_logger

_logger = get_logger(__name__)

def handler(event, _context):
    try:
        _logger.info(f"Received event: {json.dumps(event)}")
        # Phân giải request từ API Gateway
        body = json.loads(event.get("body", "{}"))
        query = body.get("question") # Hoặc query tùy bạn đặt tên bên client

        if not query:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No query provided"})
            }

        _logger.info(f"Processing query: {query}")

        # Gọi hàm logic của bạn
        answer_text = get_answer_from_query(query)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "answer": answer_text
            })
        }
    except Exception as e:
        _logger.error(f"Error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }