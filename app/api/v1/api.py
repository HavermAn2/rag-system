from fastapi import FastAPI
from app.core.exceptions import AppError
from app.core.exception_handlers import app_exception_handler
from app.routes.router import api_router
from app.services.query_service import Query
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
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
    ingestion = Ingestion(FILE_STORAGE,client)
    document = DocumentService(FILE_STORAGE,ingestion)
    
    embed = Embeddings(model)
    app.state.model = model
    app.state.query = query
    app.state.client = client
    app.state.collection = collection
    app.state.document = document
    app.state.ingestion = ingestion
    app.state.embeddings = embed
    app.state.storage = FILE_STORAGE
    yield

    app.state.client.close()
app = FastAPI(lifespan=lifespan)
app.add_exception_handler(
    AppError,
    app_exception_handler,
)

app.include_router(api_router, prefix="/api/v1")
