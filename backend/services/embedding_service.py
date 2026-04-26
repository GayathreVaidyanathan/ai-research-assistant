import chromadb
from sentence_transformers import SentenceTransformer
from backend.config import EMBEDDING_MODEL, CHROMA_PATH
import uuid

model = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=CHROMA_PATH)

def get_or_create_collection(paper_id: str):
    return client.get_or_create_collection(name=paper_id)

def add_chunks_to_collection(paper_id: str, chunks: list[str]):
    collection = get_or_create_collection(paper_id)
    embeddings = model.encode(chunks).tolist()
    ids = [str(uuid.uuid4()) for _ in chunks]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    return len(chunks)

def query_collection(paper_id: str, query: str, n_results: int = 5) -> list[str]:
    collection = get_or_create_collection(paper_id)
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=n_results)
    return results['documents'][0]

def delete_collection(paper_id: str):
    try:
        client.delete_collection(name=paper_id)
    except:
        pass