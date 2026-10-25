import pymupdf
from pathlib import Path


class Extraction:
    def __init__(self,path):
        self.path = path

    def extract_text(self):
        title = Path(self.path).name
        texts = []

        with pymupdf.open(self.path) as doc:
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text("text")
                text += "\n"f"{page_num}"

                if text.strip():
                    texts.append(text)

        text = "\n".join(texts)
        return text, title
    
    def extract_titles_only(self):
        files_with_sub = [f for f in Path(f"{self.path}").iterdir() if f.is_file()]
        files = [Path(f"{f}").name for f in files_with_sub]
        return files