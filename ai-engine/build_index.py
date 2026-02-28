import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
KNOWLEDGE_PATH = "ai-engine/knowledge"
INDEX_PATH = "ai-engine/vector.index"
META_PATH = "ai-engine/vector_meta.json"

model = SentenceTransformer(MODEL_NAME)


def load_documents():
    docs = []
    for root, _, files in os.walk(KNOWLEDGE_PATH):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    text = f.read()
                docs.append({
                    "content": text,
                    "source": path
                })
    return docs


def build_index():
    docs = load_documents()

    texts = [doc["content"] for doc in docs]
    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w") as f:
        json.dump(docs, f)

    print("FAISS index built successfully.")


if __name__ == "__main__":
    build_index()