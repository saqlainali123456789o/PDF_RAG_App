import faiss
import numpy as np

from embeddings import embed_texts


def create_index(chunks):
    if not chunks:
        raise ValueError("No chunks are available to index.")

    texts = [chunk["text"] for chunk in chunks]
    vectors = embed_texts(texts).astype("float32")

    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    return index


def search_index(question, index, chunks, top_k=4):
    if index is None or index.ntotal == 0:
        return []

    question_vector = embed_texts([question]).astype("float32")
    k = min(top_k, index.ntotal)

    scores, indices = index.search(question_vector, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        item = dict(chunks[int(idx)])
        item["score"] = float(score)
        results.append(item)

    return results
