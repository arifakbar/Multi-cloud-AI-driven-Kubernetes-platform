import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "ai-engine/vector.index"
META_PATH = "ai-engine/vector_meta.json"

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_context(query, top_k=3):
    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "r") as f:
        metadata = json.load(f)

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx]["content"])

    return results


def enhance_violations():
    with open("violations.json", "r") as f:
        data = json.load(f)

    enhanced = []

    for violation in data["violations"]:
        query = f"{violation['message']} {violation['severity']}"

        contexts = retrieve_context(query)

        violation["rag_context"] = contexts
        enhanced.append(violation)

    data["violations"] = enhanced

    with open("violations_enhanced.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Enhanced violations written to violations_enhanced.json")


if __name__ == "__main__":
    enhance_violations()