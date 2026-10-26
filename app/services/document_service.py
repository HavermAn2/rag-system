from pathlib import Path

class DocumentService:
    def __init__(self,path):
        self.path = path

    def upload_document(self):
        pass
    def list_documents(self):
        files_with_sub = [f for f in Path(f"{self.path}").iterdir() if f.is_file()]
        files = [Path(f"{f}").name for f in files_with_sub]
        return files
        
    def list_document(self,file_name: str):
        return self.path / file_name
    def delete_document(self,file_name):
        pass