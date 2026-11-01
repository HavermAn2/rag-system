
from fastapi import Depends
from app.core.celery_app import celery_app
from app.dependencies import (get_ingestion)
from pathlib import Path
@celery_app.task
def test_task(document_id: str):
    INTERSECTION = Depends(get_ingestion)
    extraction = INTERSECTION.extract(document_id)
    return {
        "document_id": document_id,
        "status": "completed"
    }