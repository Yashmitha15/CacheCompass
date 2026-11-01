
from google import genai

from app.config import get_settings
from app.retriever import get_retriever


def ask_gemini(question: str) -> str:
    settings = get_settings()

    # Step 1: Retrieve relevant Valkey source code.
    retriever = get_retriever()
    documents = retriever.invoke(question)

    if not documents:
        return "I could not find relevant information in the indexed Valkey source code."

    # Step 2: Prepare the retrieved code as context.
    context = ""

    for i, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "Unknown source")

        context += (
            f"\nSource {i}: {source}\n"
            f"{document.page_content}\n"
        )

    # Step 3: Ask Gemini to answer using the retrieved context.
    client = genai.Client(api_key=settings.gemini_api_key)

    prompt = f"""
You are CacheCompass, an assistant for Valkey source code
and Redis-to-Valkey migration.

Use the retrieved Valkey source code below to answer the question.
Rules:
- Answer ONLY using the retrieved Valkey source code.
- Do not use general knowledge to answer questions.
- If the retrieved context does not contain the answer,
  respond exactly:
  "I could not find sufficient information in the indexed Valkey source code."
- Do not guess or invent technical details.
- Mention the source file names supporting your answer.
Retrieved Valkey source code:
{context}

User question:
{question}
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    return response.text or "No answer was generated."
