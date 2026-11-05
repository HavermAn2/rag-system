from pathlib import Path
from uuid import uuid4
from shutil import copyfileobj
from app.tasks.tasks import upload_task,delete_task
from app.core.exceptions import FileNotFoundError,ExtractionError,InvalidDocumentError


class DocumentService:
    def __init__(self, path: str, ingestion):
        self.path = path
        self.ingestion = ingestion
        self.path.mkdir(parents=True, exist_ok=True)

    def upload_document(self,file):
        if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are allowed")
        filename = f"{uuid4()}.pdf"
        file_path = self.path / filename
        with file_path.open("wb") as buffer:
            copyfileobj(file.file, buffer)
        x = upload_task.delay(filename)
        return x.id

    
    def list_documents(self):
        files_with_sub = [f for f in Path(f"{self.path}").iterdir() if f.is_file()]
        files = [Path(f"{f}").name for f in files_with_sub]
        return files

    
    def get_document(self, document_id: str):
        file_path = self.path / document_id

        if (
            Path(document_id).name != document_id
            or Path(document_id).suffix.lower() != ".pdf"
        ):
            raise InvalidDocumentError("Invalid document ID")

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Document {document_id} not found"
            )

        try:
            pages = self.ingestion.extract(document_id)
            cleaned_text = self.ingestion.clean_text(pages)

        except Exception as exc:
            raise ExtractionError(
                f"Failed to extract document {document_id}"
            ) from exc

        return cleaned_text

        
    def delete_document(self,file_name):
        file_path = Path(self.path) / Path(file_name)
        if not file_path.is_file():
            raise FileNotFoundError(
                f"Document {file_name} not found"
            )
        task = delete_task.delay(file_name)
        return task.id


        
        
        



        

        