from sentence_transformers import SentenceTransformer
from functools import lru_cache
import numpy as np

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# 🔥 LRU Cache (stores last 500 embeddings)
@lru_cache(maxsize=500)
def encode_cached(text):
    """
    Returns embedding for a given text.
    Uses LRU cache to avoid recomputation.
    """
    vec = model.encode([text])[0]
    
    # Convert to tuple because lru_cache requires hashable return types
    return tuple(vec)


def encode(text):
    """
    Wrapper to convert cached tuple back to numpy array
    """
    return np.array(encode_cached(text))