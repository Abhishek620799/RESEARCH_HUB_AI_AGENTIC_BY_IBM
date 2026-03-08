# ResearchHub AI - Embedding Service
# Milestone 4: Activity 4.1 - Text embedding and similarity search
# Milestone 5: Activity 5.1 - Research paper analysis with vector embeddings
# Responsible: Aditya Singh

import numpy as np
from typing import List, Dict, Any

# Lightweight embedding without sentence-transformers (avoids heavy PyTorch dependency)
# Uses simple TF-IDF style bag-of-words vectors
# Aditya Singh - Embedding implementation


def simple_embed(text: str) -> np.ndarray:
    """
    Create a simple normalized bag-of-words embedding.
    Aditya Singh - Lightweight embedding without PyTorch.
    """
    words = text.lower().split()
    word_set = sorted(set(words))
    vec = np.zeros(min(len(word_set), 500))
    for i, word in enumerate(word_set[:500]):
        vec[i] = words.count(word)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec


def get_embedding(text: str) -> List[float]:
    """
    Convert text to vector embedding.
    Aditya Singh - Embedding interface.
    """
    return simple_embed(text).tolist()


def get_relevant_context(query: str, papers: List[Dict[str, Any]], top_k: int = 3) -> str:
    """
    Find relevant papers based on cosine similarity to query.
    Aditya Singh - Context retrieval for AI responses.
    """
    if not papers:
        return ""

    query_embedding = simple_embed(query)

    # Compute cosine similarity with each paper
    similarities = []
    for paper in papers:
        text = paper.get("title", "") + " " + paper.get("abstract", "")
        paper_emb = simple_embed(text)
        min_len = min(len(query_embedding), len(paper_emb))
        if min_len == 0:
            similarities.append(0.0)
            continue
        q = query_embedding[:min_len]
        p = paper_emb[:min_len]
        denom = np.linalg.norm(q) * np.linalg.norm(p)
        sim = float(np.dot(q, p) / denom) if denom > 0 else 0.0
        similarities.append(sim)

    # Get top-k most relevant papers
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    context_parts = []
    for idx in top_indices:
        paper = papers[int(idx)]
        title = paper.get("title", "Untitled")
        authors = str(paper.get("authors", "Unknown"))
        abstract = paper.get("abstract", "")[:200]
        entry = "Title: " + title + "\nAuthors: " + authors + "\nAbstract: " + abstract
        context_parts.append(entry)

    return "\n\n".join(context_parts)
