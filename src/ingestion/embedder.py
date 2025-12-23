import os
import time
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.common.logger import get_logger

_logger = get_logger(__name__)

class IngestionService:
    def __init__(self):
        # 1. Khởi tạo HuggingFace Embeddings (Chạy local trên CPU/GPU của bạn)
        # Model này tạo ra vector 384 chiều
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2. Khởi tạo Pinecone Vector Store
        pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
        self.namespace = os.getenv("PINECONE_NAMESPACE", "default")
        
        self.vector_store = PineconeVectorStore(
            index_name=pinecone_index_name,
            embedding=self.embeddings,
            namespace=self.namespace
        )
        
        # 3. Khởi tạo Text Splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def process_and_upload(self, documents):
        total_chunks = 0
        for doc in documents:
            source_info = doc.metadata.get("source", "unknown")
            page_info = doc.metadata.get("page", 0)

            chunks = self.text_splitter.split_text(doc.page_content)
            
            metadatas = [{
                "source": source_info,
                "page": page_info,
                "text": chunk
            } for chunk in chunks]

            self.vector_store.add_texts(
                texts=chunks,
                metadatas=metadatas
            )
            
            total_chunks += len(chunks)
            _logger.info(f"Đã tải lên {len(chunks)} đoạn từ trang {page_info}")
        
        return total_chunks