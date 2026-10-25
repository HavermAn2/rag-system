from fastapi import FastAPI,File,UploadFile
from app.storage.query import Query
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from app.embeddings.embeddings import Embeddings
from app.ingestion.extraction import Extraction
e = Embeddings()
client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("intfloat/multilingual-e5-base")
COLLECTION_NAME = "docs"
app = FastAPI()
task = Query(client,COLLECTION_NAME)
extract = Extraction("app/storage/data")
file_starage = "app/storage/data"

@app.get("/api/v1/health",status_code=200)
async def health():
    return {"message": "Hello World"}


@app.get("/api/v1/search", status_code=200)
async def query(users_query:str, limit = 10 ):
    res = task.request_query(users_query,limit)
    return {"OK":200,"RES":res}



@app.post("/api/v1/document",status_code=201)
async def upload_file(file:UploadFile):
    return{"filename": file.filename}
@app.get("/app/v1/documents",status_code=200)
async def get_file_names():
    res = extract.extract_titles_only()
    return {"OK":200,"RES":res}
@app.get("/app/v1/documents/{file_name}",status_code=200)
async def get_file(file_name: str):
    return 


    
