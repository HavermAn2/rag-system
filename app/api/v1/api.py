from fastapi import FastAPI,UploadFile
from app.storage.query import Query
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from app.ingestion.extraction import Extraction
from contextlib import asynccontextmanager
from fastapi import FastAPI,  Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    collection = "docs"
    client = QdrantClient(url="http://localhost:6333")
    model = SentenceTransformer("intfloat/multilingual-e5-base")
    query = Query(client,collection)
    file_storage = "app/storage/data"

    app.state.file_storage = file_storage
    app.state.model = model
    app.state.query = query
    app.state.client = client
    app.state.collection = collection
    yield

    client.close()
app = FastAPI(lifespan=lifespan)
extract = Extraction("/app/storage/data/Junior_Py_Dev.pdf")
@app.get("/api/v1/health",status_code=200)
async def health():
    return {"message": "Hello World"}
@app.get("/api/v1/search", status_code=200)
async def query(request:Request,users_query:str, limit = 10 ):
    query = request.app.state.query
    res = query.request_query(users_query,limit)
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
@app.delete("/app/v1/delete-document/{file_name}")
async def del_file(file_name:str):
    return


    
