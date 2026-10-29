from fastapi import APIRouter,Depends,UploadFile
from app.dependencies import (get_doc)
from app.services.document_service import DocumentService
router = APIRouter(
    prefix="/documents"
    
)

@router.post("/", status_code=201)
def upload_document(file:UploadFile,document:DocumentService = Depends(get_doc)):

    return document.upload_document(file)

@router.get("/")
def list_documents(document:DocumentService = Depends(get_doc)):
    return document.list_documents()
    
@router.get("/{document_id}")
def get_document(document_id,document:DocumentService = Depends(get_doc)):
    return document.get_document(document_id)

@router.delete("/{document_name}")
def delete_document(
    document_name: str,
    service: DocumentService = Depends(get_doc)
):
    return service.delete_document(document_name)
