from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

def load_vectorstore() -> FAISS:
    with open("data/docs.txt", "r", encoding="utf-8") as f:
        documents = [Document(page_content=line.strip()) for line in f if line.strip()]
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})