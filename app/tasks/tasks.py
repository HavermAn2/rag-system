
from app.core.celery_app import celery_app
from app.services.ingestion_service import Ingestion
from app.services.embeddings_service import Embeddings
from app.storage.upload import Upload
from qdrant_client import QdrantClient
from pathlib import Path
from sentence_transformers import SentenceTransformer
@celery_app.task
def test_task(document_id: str):
    model = SentenceTransformer("intfloat/multilingual-e5-base")
    FILE_STORAGE = Path("app/storage/data")
    client = QdrantClient(url="http://localhost:6333")
    INTERSECTION = Ingestion(FILE_STORAGE,client)
    _,extraction = INTERSECTION.extract(document_id)
    # clean_text = INTERSECTION.clean_text(extraction)
    chunks = INTERSECTION.chunking(extraction)
    embed = Embeddings(model)
    embeds = embed.text_to_vector(chunks)
    qdrant = Upload(client,"docs")
    qdrant.create_point_qdrant(document_id,chunks,embeds)
    return {
        "document_id": document_id,
        "chunks": len(chunks),
        "status": "completed"
    }