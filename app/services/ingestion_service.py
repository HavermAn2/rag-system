import pymupdf
import re
class Ingestion:
    def __init__(self,path,client):
        self.path = path
        self.client = client
        
    
    def extract(self,file_name:str):
                texts = []
                with pymupdf.open(self.path / file_name) as doc:
                    for page_num, page in enumerate(doc, start=1):
                        text = page.get_text("text")
                        text += "\n"f"{page_num}"
                        if text.strip():
                            texts.append(text)
        
                text = "\n".join(texts)
                return text

    
    def chunking(self,text,chunk_size=80, overlap=16):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")     
        if not 0 <= overlap < chunk_size:
            raise ValueError("Invalid overlap")

        chunk = []
        word = ""
        words = []
        for i, val in enumerate(text):
            if val.isspace():
                if word:
                    chunk.append(word)
                    word = ""

                    if len(chunk) == chunk_size:
                        words.append(chunk.copy())
                        chunk = chunk[-overlap:]
            else:
                word += val
        if word:
            chunk.append(word)

        if chunk and (not words or chunk != words[-1]):
            words.append(chunk.copy())
        words = [" ".join(chunk) for chunk in words]
        return words
    

    def clean_text(self,text: str) -> str:
        text = text.replace("\uf0b7", "•")
        text = text.replace("\x0c", "\n")
        text = text.replace("\xa0", " ")

        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
        