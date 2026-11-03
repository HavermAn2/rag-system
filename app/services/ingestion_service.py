import pymupdf
import re
class Ingestion:
    def __init__(self,path,client):
        self.path = path
        self.client = client
        
    
    def extract(self,file_name:str):
                texts = []
                text_for_chunking=[]
                with pymupdf.open(self.path / file_name) as doc:
                    for page_num, page in enumerate(doc, start=1):
                        text = page.get_text("text")
                        # text += "\n"f"{page_num}"
                        if text.strip():
                            texts.append(text)
                        text_for_chunking.append({page_num : text})
        
                text = "\n".join(texts)
                return text, text_for_chunking

    
    def chunking(self, text, chunk_size=80, overlap=10):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if not 0 <= overlap < chunk_size:
            raise ValueError("Invalid overlap")

        words = []

        for page in text:
            for page_number, content in page.items():
                chunk = []

                for word in content.split():
                    chunk.append(word)

                    if len(chunk) == chunk_size:
                        words.append({
                            "page": page_number,
                            "text": " ".join(chunk)
                        })

                        chunk = chunk[-overlap:] if overlap else []

                if chunk and (not words or words[-1]["text"] != " ".join(chunk)):
                    words.append({
                        "page": page_number,
                        "text": " ".join(chunk)
                    })

        return words


    def clean_text(self,text: dict) -> dict:

        for page in text:
             for page_number, content in page.items():
                  if ("\uf0b7" or "\x0c" or "\xa0"):
                    content = content.replace("\uf0b7", "•")
                    content = content.replace("\x0c", "\n")
                    content = content.replace("\xa0", " ")

                    content = re.sub(r"[ \t]+", " ", content)
                    content = re.sub(r"\n{3,}", "\n\n", content)
                    page[page_number] = content

        return text
    
        