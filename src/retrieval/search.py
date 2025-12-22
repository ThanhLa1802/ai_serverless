import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore # Hoặc PineconeSparseVectorStore tùy setup của bạn
from src.retrieval.generator import AnswerGenerator

def get_answer_from_query(query: str) -> str:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector_store = PineconeVectorStore(
        index_name=os.getenv("PINECONE_INDEX_NAME"), 
        embedding=embeddings
    )

    
    relevant_docs = vector_store.similarity_search(query, k=3)
    context_list = [doc.page_content for doc in relevant_docs]
    generator = AnswerGenerator()
    answer = generator.generate_answer(query, context_list)

    return answer