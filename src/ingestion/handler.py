import base64
import boto3
import json
from .parser import PDFParser
from .embedder import IngestionService
from src.common.logger import get_logger

#use English comments
_logger = get_logger(__name__)
s3_client = boto3.client('s3')

def handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        _logger.info(f"Processing file from S3 - Bucket: {bucket}, Key: {key}")
        
        file_bytes = s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()

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