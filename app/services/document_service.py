from pathlib import Path
from uuid import uuid4
from shutil import copyfileobj



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

        return filename
    def list_documents(self):
        files_with_sub = [f for f in Path(f"{self.path}").iterdir() if f.is_file()]
        files = [Path(f"{f}").name for f in files_with_sub]
        return files
    def get_file(self,file_name):
        txt = self.ingestion.extract(file_name)
        cleand_txt = self.ingestion.clean_text(txt) # for optimization
        return cleand_txt
    def delete_document(self,file_name):
        pass