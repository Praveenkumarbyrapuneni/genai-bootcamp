from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")

def chunk_text(text: str, chunk_size=200, chunk_overlap=40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

if __name__ == "__main__":
    text = load_text_file("data.txt")
    chunks = chunk_text(text)

    print(f"✅ Total chunks created: {len(chunks)}\n")

    for i, chunk in enumerate(chunks, start=1):
        print(f"--- Chunk {i} ---")
        print(chunk)
        print()
