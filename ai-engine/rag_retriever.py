import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_STORE_DIR = "ai-engine/vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.pkl")

TOP_K = 3

model = SentenceTransformer("all-MiniLM-L6-v2")


class RAGRetriever:
    def __init__(self):
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError("FAISS index not found. Run embedder.py first.")

        print("Loading FAISS index...")
        self.index = faiss.read_index(INDEX_PATH)

        print("Loading metadata...")
        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query, top_k=TOP_K):
        print(f"Embedding query: {query}")
        query_embedding = model.encode([query], convert_to_numpy=True)

        print("Running similarity search...")
        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for i, idx in enumerate(indices[0]):
            result = {
                "source": self.metadata[idx]["source"],
                "text": self.metadata[idx]["text"],
                "score": float(distances[0][i])
            }
            results.append(result)

        return results


if __name__ == "__main__":
    retriever = RAGRetriever()

    query = "S3 bucket without encryption"
    results = retriever.search(query)

    print("\nTop Results:\n")
    for r in results:
        print("Source:", r["source"])
        print("Score:", r["score"])
        print("Text:", r["text"][:200])
        print("-" * 60)