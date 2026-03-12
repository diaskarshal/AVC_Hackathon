from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

# Multilingual model — critical for Russian-language tender/project data.
# all-MiniLM-L6-v2 was English-only and produced poor similarity scores
# for Cyrillic text. This model supports 50+ languages including Russian.
_model = None
_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
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