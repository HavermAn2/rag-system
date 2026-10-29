from fastapi import FastAPI,UploadFile
from app.storage.query import Query
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from app.ingestion.extraction import Extraction
from contextlib import asynccontextmanager
from fastapi import FastAPI,  Request
from pathlib import Path
from app.services.document_service import DocumentService
from app.services.ingestion_service import Ingestion
from app.services.embeddings_service import Embeddings
@asynccontextmanager
async def lifespan(app: FastAPI):
    collection = "docs"
    client = QdrantClient(url="http://localhost:6333")
    model = SentenceTransformer("intfloat/multilingual-e5-base")
    query = Query(client,collection)
    extract = Extraction("/app/storage/data/Junior_Py_Dev.pdf")
    FILE_STORAGE = Path("app/storage/data")
    document = DocumentService(FILE_STORAGE)
    ingestion = Ingestion(FILE_STORAGE,client)
    embed = Embeddings(model)
    app.state.model = model
    app.state.query = query
    app.state.extract = extract
    app.state.client = client
    app.state.collection = collection
    app.state.document = document
    app.state.ingestion = ingestion
    app.state.embeddings = embed
    yield

    client.close()
app = FastAPI(lifespan=lifespan)



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
    #soon
    return{"filename": file.filename}


@app.get("/app/v1/documents",status_code=200)
async def get_file_names(request:Request):
    res = request.app.state.document.list_documents()
    return {"OK":200,"RES":res}


@app.get("/app/v1/documents/{file_name}",status_code=200)
async def get_file(request:Request,file_name: Path):
    txt = request.app.state.ingestion.extract(file_name)
    cleand_txt = request.app.state.ingestion.clean_text(txt) # for optimization
    return cleand_txt


@app.delete("/app/v1/delete-document/{file_name}")
async def del_file(file_name:str):
    return


    
