
import time
from pathlib import Path

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import get_settings
from app.ingest import load_source_files, split_documents


INDEX_DIR = Path("data/index_v2")

BATCH_SIZE = 100
DELAY_SECONDS = 65
MAX_RETRIES = 5


def create_vector_store():
    settings = get_settings()

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2",
        google_api_key=settings.gemini_api_key,
    )

    documents = load_source_files()
    chunks = split_documents(documents)

    total_chunks = len(chunks)

    print("Total documents:", len(documents))
    print("Total chunks:", total_chunks)

    vector_store = None
    start_index = 0

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    # Resume only from the new index.
    if (INDEX_DIR / "index.faiss").exists():
        print("Existing new index found. Loading it...")

        vector_store = FAISS.load_local(
            str(INDEX_DIR),
            embeddings,
            allow_dangerous_deserialization=True,
        )

        start_index = vector_store.index.ntotal
        print("Already indexed:", start_index)

    if start_index > total_chunks:
        raise ValueError("Existing index has more vectors than current chunks.")

    # Process remaining chunks in batches.
    for start in range(start_index, total_chunks, BATCH_SIZE):

        batch = chunks[start:start + BATCH_SIZE]

        print(
            f"\nProcessing chunks {start + 1} "
            f"to {start + len(batch)} of {total_chunks}"
        )

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                if vector_store is None:
                    vector_store = FAISS.from_documents(
                        documents=batch,
                        embedding=embeddings,
                    )
                else:
                    vector_store.add_documents(batch)

                # Save every successful batch.
                vector_store.save_local(str(INDEX_DIR))

                print("Batch saved successfully.")
                break

            except Exception as error:
                error_message = str(error)

                is_rate_limit = (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                )

                if not is_rate_limit:
                    raise

                if attempt == MAX_RETRIES:
                    raise RuntimeError(
                        "Maximum retries reached. "
                        "Run the script again after quota reset."
                    ) from error

                wait_time = DELAY_SECONDS * attempt

                print(
                    f"Rate limit reached. "
                    f"Attempt {attempt}/{MAX_RETRIES}. "
                    f"Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)

        if start + len(batch) < total_chunks:
            print(f"Waiting {DELAY_SECONDS} seconds...")
            time.sleep(DELAY_SECONDS)

    if vector_store is None:
        raise RuntimeError("No chunks were indexed.")

    print("\nIndexing completed!")
    print("Total indexed chunks:", vector_store.index.ntotal)
    print("Index location:", INDEX_DIR)


if __name__ == "__main__":
    create_vector_store()
