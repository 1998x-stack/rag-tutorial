#!/usr/bin/env python3
"""2-D hand-assigned vectors for illustrating dot, cosine, MaxSim and InfoNCE.

These are *not* outputs of a trained language embedding model and do not
measure semantic similarity or production retrieval quality.
"""
from __future__ import annotations
from math import exp, isfinite, log, sqrt


def dot(x, y):
    if not x or len(x) != len(y):
        raise ValueError("vectors must have the same positive dimension")
    if not all(isfinite(v) for v in [*x, *y]):
        raise ValueError("non-finite vector entry")
    return sum(a * b for a, b in zip(x, y))


def cosine(x, y):
    nx, ny = sqrt(dot(x, x)), sqrt(dot(y, y))
    if nx == 0 or ny == 0:
        raise ValueError("cosine is undefined for a zero vector")
    return dot(x, y) / (nx * ny)


def rank(query, documents, metric="cosine"):
    if metric not in ("dot", "cosine"):
        raise ValueError("unsupported metric")
    fn = cosine if metric == "cosine" else dot
    return sorted(documents, key=lambda item: (-fn(query, item[1]), item[0]))


def infonce_loss(query, positive, negatives, temperature=0.1):
    """Single-query illustrative InfoNCE over unit-normalized vectors."""
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    scores = [dot(query, v) / temperature for v in [positive, *negatives]]
    m = max(scores)
    return -scores[0] + (m + log(sum(exp(score - m) for score in scores)))


def maxsim(query_token_vectors, doc_token_vectors):
    """Illustrative unmasked ColBERT-like score on precomputed token vectors."""
    if not query_token_vectors or not doc_token_vectors:
        raise ValueError("token sequences must not be empty")
    return sum(max(dot(q, d) for d in doc_token_vectors)
               for q in query_token_vectors)


DOCUMENTS = [
    ("D1", (0.9, 0.1)),  # higher cosine despite smaller norm
    ("D2", (3.0, 3.0)),  # higher raw dot due to larger norm
]


if __name__ == "__main__":
    q = (1.0, 0.0)
    print("cosine ranking:", [name for name, _ in rank(q, DOCUMENTS)])
    print("raw dot ranking:", [name for name, _ in rank(q, DOCUMENTS, "dot")])
    print("example InfoNCE:", round(
        infonce_loss(q, (1.0, 0.0), [(0.0, 1.0)], temperature=0.5), 6))
    print("example MaxSim:", maxsim([(1.0, 0.0)], [(0.0, 1.0), (1.0, 0.0)]))
