import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_STORE_DIR = "ai-engine/vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.pkl")

MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3


class RAGRetriever:
    def __init__(self):
        self.index = None
        self.metadata = []
        self.model = None

        self._load_index()
        self._load_metadata()
        self._load_model()

        # Final safety check
        if self.index is None or self.index.ntotal == 0:
            raise Exception("FAISS index is empty or invalid.")

        if len(self.metadata) != self.index.ntotal:
            raise Exception(
                f"Metadata count ({len(self.metadata)}) does not match index size ({self.index.ntotal})"
            )

    def _load_index(self):
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError("FAISS index not found. Run embedder.py first.")

        print("Loading FAISS index...")
        try:
            self.index = faiss.read_index(INDEX_PATH)
        except Exception as e:
            raise Exception(f"Failed to load FAISS index: {e}")

    def _load_metadata(self):
        if not os.path.exists(METADATA_PATH):
            raise FileNotFoundError("Metadata file not found.")

        print("Loading metadata...")
        try:
            with open(METADATA_PATH, "rb") as f:
                self.metadata = pickle.load(f)
        except Exception as e:
            raise Exception(f"Failed to load metadata: {e}")

    def _load_model(self):
        print("Loading embedding model...")
        try:
            self.model = SentenceTransformer(MODEL_NAME)
        except Exception as e:
            raise Exception(f"Failed to load embedding model: {e}")

    def search(self, query, top_k=TOP_K):
        if not query or not isinstance(query, str):
            return []

        print(f"Embedding query: {query}")

        try:
            query_embedding = self.model.encode(
                [query],
                convert_to_numpy=True
            ).astype("float32")

            # Normalize for cosine similarity
            faiss.normalize_L2(query_embedding)

            print("Running similarity search...")
            scores, indices = self.index.search(query_embedding, top_k)

        except Exception as e:
            print(f"Search failed: {e}")
            return []

        results = []

        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue

            results.append({
                "source": self.metadata[idx].get("source", "unknown"),
                "text": self.metadata[idx].get("text", ""),
                "score": float(scores[0][i])
            })

        return results


if __name__ == "__main__":
    retriever = RAGRetriever()

    query = "S3 bucket without encryption"
    results = retriever.search(query)

    print("\nTop Results:\n")

    for r in results:
        print("Source:", r["source"])
        print("Similarity Score:", r["score"])
        print("Text:", r["text"][:200])
        print("-" * 60)