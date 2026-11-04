
from app.core.celery_app import celery_app
from app.services.ingestion_service import Ingestion
from app.services.embeddings_service import Embeddings
from app.services.qdrant_service import Upload
from qdrant_client import QdrantClient
from pathlib import Path
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://localhost:6333")
qdrant = Upload(client,"docs")
FILE_STORAGE = Path("app/storage/data")
@celery_app.task
def upload_task(document_id: str,):
    model = SentenceTransformer("intfloat/multilingual-e5-base")
    INTERSECTION = Ingestion(FILE_STORAGE,client)
    
    extraction = INTERSECTION.extract(document_id)   
    clean_txt = INTERSECTION.clean_text(extraction)
    chunks = INTERSECTION.chunking(clean_txt)
    embed = Embeddings(model)
    embeds = embed.text_to_vector(chunks)
    qdrant.create_point_qdrant(document_id,chunks,embeds)
    return {
        "document_id": document_id,
        "chunks": len(chunks),
        "status": "completed"
    }


@celery_app.task
def delete_task(file_path: str):
    file_path = Path(file_path)
    qdrant.delete_point_qdrant(file_path.name)
    file_path.unlink()
    return {"Done":"Everything was deleted"}