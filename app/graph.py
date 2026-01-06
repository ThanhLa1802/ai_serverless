from langgraph.graph import StateGraph
from app.state import ChatState
from app.nodes import (
    load_history,
    retrieve_documents,
    has_docs,
    fallback_response,
    generate_answer
)

def build_graph():
    graph = StateGraph(ChatState)

    graph.add_node("load_history", load_history)
    graph.add_node("retrieve_docs", retrieve_documents)
    graph.add_node("fallback_answer", fallback_response)
    graph.add_node("rag_answer", generate_answer)

    graph.set_entry_point("load_history")
    graph.add_edge("load_history", "retrieve_docs")

    graph.add_conditional_edges(
        "retrieve_docs",
        has_docs,
        {
            "no_docs": "fallback_answer",
            "has_docs": "rag_answer"
        }
    )

    graph.set_finish_point("fallback_answer")
    graph.set_finish_point("rag_answer")

    return graph.compile()
