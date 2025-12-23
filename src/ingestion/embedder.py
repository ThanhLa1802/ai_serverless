import os
import time
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.common.logger import get_logger

_logger = get_logger(__name__)

class IngestionService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        self.vector_store = PineconeVectorStore(
            index_name=os.getenv("PINECONE_INDEX_NAME"),
            embedding=self.embeddings,
            namespace=os.getenv("PINECONE_NAMESPACE", "default")
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )

    def process_and_upload(self, documents):
        total_chunks = 0

        for doc in documents:
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", 0)

            chunks = self.text_splitter.split_text(doc.page_content)
            metadatas = [{"source": source, "page": page} for _ in chunks]

            self.vector_store.add_texts(
                texts=chunks,
                metadatas=metadatas,
                batch_size=50
            )

            total_chunks += len(chunks)
            _logger.info(f"Uploaded {len(chunks)} chunks from page {page}")

        return total_chunks

