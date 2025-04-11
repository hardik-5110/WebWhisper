from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Use: "all-MiniLM-L6-v2"
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks):
    return model.encode(chunks).astype("float32")

def store_in_faiss(embeddings, chunks):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, chunks
