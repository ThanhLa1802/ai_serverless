import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from src.common.logger import get_logger

_logger = get_logger(__name__)

class SearchService:
    def __init__(self):
        # 1. BẮT BUỘC: Dùng cùng model với lúc Ingest
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2. Kết nối tới Pinecone
        index_name = os.getenv("PINECONE_INDEX_NAME")
        namespace = os.getenv("PINECONE_NAMESPACE", "default")
        
        self.vector_store = PineconeVectorStore(
            index_name=index_name,
            embedding=self.embeddings,
            namespace=namespace
        )

    def search_context(self, query: str, k: int = 3):
        """Tìm kiếm k đoạn văn bản liên quan nhất"""
        _logger.info(f"Đang tìm kiếm ngữ cảnh cho câu hỏi: {query}")
        
        # Tìm kiếm similarity search
        results = self.vector_store.similarity_search(query, k=k)
        
        # Trích xuất nội dung text từ metadata mà chúng ta đã lưu lúc Ingest
        context_list = [doc.page_content for doc in results]
        return context_list