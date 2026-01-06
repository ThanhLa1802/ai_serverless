from app.llm import llm
from app.vectorstore import load_vectorstore
from app.state import ChatState
from langchain_core.messages import HumanMessage, AIMessage

retriever = load_vectorstore()

def load_history(state: ChatState):
    return {
        "messages": state.get("messages", [])
    }

def retrieve_documents(state: ChatState):
    docs = retriever.invoke(state["question"])
    return {"documents": docs}

def has_docs(state: ChatState):
    print(state)
    if not state.get("documents"):
        print("No documents found.")
        return "no_docs"
    print(f"Found {len(state['documents'])} documents.")
    return "has_docs"

def fallback_response(state: ChatState):
    return {
        "answer": "I don't have enough information in the provided documents to answer this question.",
        "documents": []
    }

def generate_answer(state: ChatState):
    docs_content = "\n".join([doc.page_content for doc in state["documents"]])
    prompt = f"""
            You are a technical assistant.
            The user asked: {state['question']}
            Keep the answer SHORT and CONCISE.
            Maximum 3 sentences.
            Use the following documents to provide a detailed answer:
            {docs_content}
            """
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"answer": response.content}
