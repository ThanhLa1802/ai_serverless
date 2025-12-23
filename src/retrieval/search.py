import os
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from src.common.logger import get_logger

_logger = get_logger(__name__)

class SearchService:
    def __init__(self):
        
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

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