from fastapi import APIRouter,Depends,UploadFile
from app.dependencies import (get_document)
from app.services.document_service import DocumentService
router = APIRouter(
    prefix="/documents"
    
)

@router.post("/", status_code=201)
def upload_document(file:UploadFile,document:DocumentService = Depends(get_document)):
    return document.upload_document(file)

@router.get("/")
def list_documents(document:DocumentService = Depends(get_document)):
    return document.list_documents()
    
@router.get("/{document_id}")
def get_document(file_name,document:DocumentService = Depends(get_document)):
    return document.get_file(file_name)

@router.delete("/{document_id}")
def delete_document(document_id: str):
    pass
