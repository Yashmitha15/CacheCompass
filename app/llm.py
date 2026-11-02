from google import genai

from app.config import get_settings
from app.retriever import get_retriever


# In-memory usage statistics.
# These reset whenever the application restarts.
usage_stats = {
    "requests": 0,
    "prompt_tokens": 0,
    "output_tokens": 0,
    "total_tokens": 0,
    "estimated_cost_usd": 0.0,
}


def ask_gemini(question: str) -> str:
    settings = get_settings()

    # Step 1: Retrieve relevant Valkey source code.
    retriever = get_retriever()
    documents = retriever.invoke(question)

    if not documents:
        return "I could not find relevant information in the indexed Valkey source code."

    # Step 2: Prepare retrieved code as context.
    context = ""

    for i, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "Unknown source")

        context += (
            f"\nSource {i}: {source}\n"
            f"{document.page_content}\n"
        )

    # Step 3: Ask Gemini.
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

    # Step 4: Record token usage returned by Gemini.
    metadata = response.usage_metadata

    if metadata:
        prompt_tokens = metadata.prompt_token_count or 0
        output_tokens = metadata.candidates_token_count or 0
        total_tokens = metadata.total_token_count or 0

        input_cost = (
            prompt_tokens
            / 1_000_000
            * settings.gemini_input_cost_per_million
        )

        output_cost = (
            output_tokens
            / 1_000_000
            * settings.gemini_output_cost_per_million
        )

        usage_stats["requests"] += 1
        usage_stats["prompt_tokens"] += prompt_tokens
        usage_stats["output_tokens"] += output_tokens
        usage_stats["total_tokens"] += total_tokens
        usage_stats["estimated_cost_usd"] += input_cost + output_cost

    return response.text or "No answer was generated."


def get_usage_summary() -> dict:
    return usage_stats.copy()