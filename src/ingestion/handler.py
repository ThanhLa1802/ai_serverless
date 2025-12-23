import base64
import boto3
import json
from .parser import PDFParser
from .embedder import IngestionService
from src.common.logger import get_logger

#use English comments
_logger = get_logger(__name__)
s3_client = boto3.client('s3')

def handler(event, _context):
    print("Ingestion handler called")
    print("Event received:", json.dumps(event))
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        _logger.info(f"Processing file from S3 - Bucket: {bucket}, Key: {key}")
        
        file_bytes = s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()

        _logger.info(f"File of size {len(file_bytes)} bytes downloaded from S3.")
        parser = PDFParser()
        docs = parser.parse_from_bytes(file_bytes)
        _logger.info(f"Extracted {len(docs)} pages from the PDF document.")
        if not docs:
            raise ValueError("No documents extracted from the PDF.")
        
        # step 2: Split and embed + upload
        service = IngestionService()
        count = service.process_and_upload(docs)
        _logger.info(f"Uploaded {count} chunks to the vector store.")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Successfully processed and uploaded embeddings.",
                "pages_processed": len(docs),
                "chunks_created": count
            })
        }
    except Exception as e:
        _logger.error(f"LỖI XỬ LÝ INGESTION: {str(e)}", exc_info=True)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}