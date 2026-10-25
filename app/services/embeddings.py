from fastapi import FastAPI
from app.storage.query import Query
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from app.embeddings.embeddings import Embeddings
e = Embeddings()
client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("intfloat/multilingual-e5-base")
COLLECTION_NAME = "docs"
app = FastAPI()

@app.post("/api/documents")
async def upload_doc():
    pass