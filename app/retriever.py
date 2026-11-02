from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import get_settings


def get_retriever():
    settings = get_settings()

    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured in settings or environment.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=settings.gemini_api_key,
    )

    index_path = Path(settings.index_dir)
    if not (index_path / "index.faiss").exists():
        index_path = Path(settings.fallback_index_dir)

    if not (index_path / "index.faiss").exists():
        raise FileNotFoundError(
            f"FAISS index not found in '{settings.index_dir}' or '{settings.fallback_index_dir}'."
        )

    vector_store = FAISS.load_local(
        str(index_path),
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
