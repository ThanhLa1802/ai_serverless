import base64
import json
from .parser import PDFParser
from .embedder import IngestionService

def handler(event, context):
    try:
        # Lấy file base64 từ API request
        body = json.loads(event['body'])
        file_bytes = base64.b64decode(body['file'])
        
        # Bước 1: Trích xuất text (Dùng LangChain Loader)
        parser = PDFParser()
        docs = parser.parse_from_bytes(file_bytes)
        
        # step 2: Split and embed + upload
        service = IngestionService()
        count = service.process_and_upload(docs)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Successfully processed and uploaded embeddings.",
                "pages_processed": len(docs),
                "chunks_created": count
            })
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}