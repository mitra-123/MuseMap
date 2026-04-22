import numpy as np

def cosine_similarity(embedding1: list, embedding2: list) -> float:
    a = np.array(embedding1)
    b = np.array(embedding2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))