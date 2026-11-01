
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import get_settings


INDEX_DIR = "data/index"


def get_retriever():
    settings = get_settings()

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=settings.gemini_api_key,
    )

    vector_store = FAISS.load_local(
        INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 5}
    )


if __name__ == "__main__":
    retriever = get_retriever()

    question = "How does Valkey handle access control lists?"

    results = retriever.invoke(question)

    print("Question:", question)
    print("Retrieved documents:", len(results))

    for i, document in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Source:", document.metadata["source"])
        print("Content:")
        print(document.page_content[:500])
