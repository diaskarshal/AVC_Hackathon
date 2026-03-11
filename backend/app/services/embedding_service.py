from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

# Load once at startup — model is ~80MB, cached in Docker layer
_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def embed_text(text: str) -> List[float]:
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()

def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    a = np.array(vec_a)
    b = np.array(vec_b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))