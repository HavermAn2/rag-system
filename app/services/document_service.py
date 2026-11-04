from pathlib import Path
from uuid import uuid4
from shutil import copyfileobj
from app.tasks.tasks import upload_task,delete_task
from app.core.exeptions import FileNotFoundError,InvalidPathError,ExtractionError


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
            print(buffer)
        x = upload_task.delay(filename)
        return x.id

    
    def list_documents(self):
        files_with_sub = [f for f in Path(f"{self.path}").iterdir() if f.is_file()]
        files = [Path(f"{f}").name for f in files_with_sub]
        return files

    
    def get_document(self,file_name):
        res = ''
        try:
            _,txt= self.ingestion.extract(file_name)
            cleand_txt = self.ingestion.clean_text(txt) 
            for page in cleand_txt:
                for page_number, content in page.items():
                    res +=content


        except ExtractionError as exc:
            print(f"Extraction failed: {exc}")
        print (res)
        return res


    
    def delete_document(self,file_name):
        file_path = Path(self.path) / Path(file_name)
        if not file_path.is_file():
            raise FileNotFoundError(
                f"Document {file_name} not found"
            )
        task = delete_task.delay(str(file_path))
        return task.id


        
        
        



        

        