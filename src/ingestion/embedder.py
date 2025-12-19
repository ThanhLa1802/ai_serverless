from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeSparseVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
#use English commenting for code files
class IngestionService:
    def __init__(self):
        # Initialize Google Generative AI Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings()
        
        # Initialize Pinecone Vector Store
        pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
        pinecone_namespace = os.getenv("PINECONE_NAMESPACE", "default")
        self.vector_store = PineconeSparseVectorStore(
            index_name=pinecone_index_name,
            namespace=pinecone_namespace,
            embedding_function=self.embeddings
        )
        
        # Initialize Text Splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def process_and_upload(self, documents):
        total_chunks = 0
        
        for doc in documents:
            # Split document into smaller chunks
            chunks = self.text_splitter.split_text(doc.page_content)
            total_chunks += len(chunks)
            
            # Create embeddings and upload to Pinecone
            self.vector_store.add_texts(
                texts=chunks,
                metadatas=[{"source": doc.metadata.get("source", "unknown")}] * len(chunks)
            )
        
        return total_chunks