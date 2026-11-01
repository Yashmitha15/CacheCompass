from app.retriever import get_retriever

retriever = get_retriever()

question = "What is a radix tree in Valkey ACL implementation?"

documents = retriever.invoke(question)

print("Retrieved chunks:", len(documents))

for i, document in enumerate(documents, start=1):
    print(f"\n--- Result {i} ---")
    print("Source:", document.metadata.get("source"))
    print(document.page_content[:700])