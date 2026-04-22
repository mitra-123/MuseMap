from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> list:
    embedding = model.encode(text)
    return embedding.tolist()

def embedding_to_string(embedding: list) -> str:
    return json.dumps(embedding)

def string_to_embedding(string: str) -> list:
    return json.loads(string)