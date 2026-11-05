import logging
from functools import lru_cache
from pathlib import Path
from uuid import UUID

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from app.core.celery_app import celery_app
from app.services.ingestion_service import Ingestion
from app.services.embeddings_service import Embeddings
from app.services.qdrant_service import Upload


logger = logging.getLogger(__name__)

FILE_STORAGE = (
    Path(__file__).resolve().parents[1] / "storage" / "data"
)

COLLECTION_NAME = "docs"


# ---------- RESOURCES ----------

@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(
        "intfloat/multilingual-e5-base"
    )


@lru_cache(maxsize=1)
def get_qdrant_client():
    return QdrantClient(
        url="http://localhost:6333"
    )


@lru_cache(maxsize=1)
def get_qdrant_service():
    return Upload(
        get_qdrant_client(),
        COLLECTION_NAME
    )


def get_ingestion():
    return Ingestion(
        FILE_STORAGE,
        get_qdrant_client()
    )


# ---------- HELPERS ----------

def get_document_path(document_id: str) -> Path:
    try:
        document_uuid = UUID(
            document_id.removesuffix(".pdf")
        )
    except ValueError as exc:
        raise ValueError("Invalid document ID") from exc

    if document_id != f"{document_uuid}.pdf":
        raise ValueError("Invalid document ID")

    return FILE_STORAGE / document_id


# ---------- TASKS ----------

@celery_app.task
def upload_task(document_id: str):

    logger.info("Processing document: %s", document_id)

    get_document_path(document_id)

    ingestion = get_ingestion()
    embeddings = Embeddings(get_model())
    qdrant = get_qdrant_service()

    try:
        pages = ingestion.extract(document_id)
        cleaned = ingestion.clean_text(pages)
        chunks = ingestion.chunking(cleaned)

        if not chunks:
            raise ValueError("Document has no text chunks")

        vectors = embeddings.text_to_vector(chunks)

        qdrant.create_point_qdrant(
            document_id,
            chunks,
            vectors
        )

        logger.info("Document indexed: %s", document_id)

        return {
            "document_id": document_id,
            "chunks": len(chunks),
            "status": "completed"
        }

    except Exception:
        logger.exception(
            "Failed to process document: %s",
            document_id
        )
        raise


@celery_app.task
def delete_task(document_id: str):

    file_path = get_document_path(document_id)
    qdrant = get_qdrant_service()

    if not file_path.is_file():
        raise FileNotFoundError(document_id)

    qdrant.delete_point_qdrant(document_id)
    file_path.unlink()

    logger.info("Document deleted: %s", document_id)

    return {
        "document_id": document_id,
        "status": "deleted"
    }