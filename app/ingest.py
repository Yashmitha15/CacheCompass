
import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


SOURCE_DIR = Path("data/raw/valkey")


def remove_comments(content):
    """Remove C-style comments while preserving strings and code."""

    pattern = re.compile(
        r'"(?:\\.|[^"\\])*"'       # Double-quoted strings
        r"|'(?:\\.|[^'\\])*'"      # Single-quoted characters
        r"|/\*[\s\S]*?\*/"         # Block comments
        r"|//[^\n]*",              # Single-line comments
    )

    def replace_comment(match):
        matched_text = match.group(0)

        # Keep strings and character literals unchanged.
        if matched_text.startswith('"') or matched_text.startswith("'"):
            return matched_text

        # Preserve line breaks from removed comments.
        return "\n" * matched_text.count("\n")

    return pattern.sub(replace_comment, content)


def load_source_files():
    documents = []

    for extension in ["*.c", "*.h"]:
        for file_path in SOURCE_DIR.rglob(extension):
            try:
                content = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                cleaned_content = remove_comments(content)

                if cleaned_content.strip():
                    documents.append(
                        Document(
                            page_content=cleaned_content,
                            metadata={
                                "source": str(file_path),
                                "file_name": file_path.name,
                            },
                        )
                    )

            except OSError as error:
                print(f"Could not read {file_path}: {error}")

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    return splitter.split_documents(documents)


if __name__ == "__main__":
    documents = load_source_files()
    chunks = split_documents(documents)

    print("Total documents loaded:", len(documents))
    print("Total chunks created:", len(chunks))

    if chunks:
        print("First chunk source:", chunks[0].metadata["source"])
        print("First chunk characters:", len(chunks[0].page_content))
        print("\nFirst chunk preview:")
        print(chunks[0].page_content[:500])
