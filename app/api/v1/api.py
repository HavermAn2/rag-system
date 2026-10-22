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
q = Query(client,COLLECTION_NAME,model)
@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/query")
async def query(users_query:str, limit = 10 ):
    req = e.query_to_vector(users_query)
    res = q.request_query(req,limit)
    return {"OK":200,"RES":res}
    
