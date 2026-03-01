import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

KNOWLEDGE_DIR = "ai-engine/knowledge"
VECTOR_STORE_DIR = "ai-engine/vector_store"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MODEL_NAME = "all-MiniLM-L6-v2"

DEBUG = False


def log(message):
    if DEBUG:
        print(message)


def load_markdown_files():
    documents = []

    for root, _, files in os.walk(KNOWLEDGE_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                if content:
                    documents.append({
                        "content": content,
                        "source": path
                    })

    return documents


def chunk_text(text):
    text = text.strip()

    if not text:
        return []

    if len(text) <= CHUNK_SIZE:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def prepare_chunks(documents):
    all_chunks = []
    metadata = []

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for chunk in chunks:
            if chunk.strip():
                all_chunks.append(chunk)
                metadata.append({
                    "source": doc["source"],
                    "text": chunk
                })

    return all_chunks, metadata


def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    return index


def main():
    documents = load_markdown_files()

    if not documents:
        raise ValueError("No markdown documents found in knowledge base.")

    chunks, metadata = prepare_chunks(documents)

    if not chunks:
        raise ValueError("No chunks generated.")

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(chunks, convert_to_numpy=True)
    embeddings = embeddings.astype("float32")

    index = build_faiss_index(embeddings)

    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

    faiss.write_index(index, os.path.join(VECTOR_STORE_DIR, "index.faiss"))

    with open(os.path.join(VECTOR_STORE_DIR, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)

    print(f"Vector store ready. Indexed {index.ntotal} chunks.")


if __name__ == "__main__":
    main()