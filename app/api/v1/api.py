from fastapi import FastAPI
from app.routes.router import api_router
from app.services.query_service import Query
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from app.ingestion.extraction import Extraction
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pathlib import Path
from app.services.document_service import DocumentService
from app.services.ingestion_service import Ingestion
from app.services.embeddings_service import Embeddings
@asynccontextmanager
async def lifespan(app: FastAPI):
    collection = "docs"
    client = QdrantClient(url="http://localhost:6333")
    model = SentenceTransformer("intfloat/multilingual-e5-base")
    FILE_STORAGE = Path("app/storage/data")
    query = Query(client,collection,model)
    extract = Extraction("/app/storage/data/Junior_Py_Dev.pdf")
    ingestion = Ingestion(FILE_STORAGE,client)
    document = DocumentService(FILE_STORAGE,ingestion)
    
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

    app.state.client.close()
app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")
