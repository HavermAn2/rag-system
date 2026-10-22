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

                if text.strip():
                    texts.append(text)

        text = "\n".join(texts)

        Path("output.txt").write_text(
            text,
            encoding="utf-8"
        )
        return text, title

