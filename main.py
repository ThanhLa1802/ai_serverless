from app.graph import build_graph

rag_graph = build_graph()

print("=== Conversational RAG Agent (LangGraph) ===")
print("Type 'exit' to quit\n")

messages = []

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    result = rag_graph.invoke({
        "question": question,
        "messages": messages
    })

    print(f"AI: {result['answer']}\n")
