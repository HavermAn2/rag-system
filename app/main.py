import extraction
import chanking
import cleaning_text
import embeddings

class Run:
    def __init__(self):
        self.emb = embeddings.Embeddings()
        self.vectors = []
        self.text =""
        extraction.extract_text()
    def run(self):
        with open("output.txt", "r", encoding="utf-8") as file:
            self.text = file.read()
        cleared_text = cleaning_text.clean_text(self.text)
        words = chanking.chunking(cleared_text)
        embedding = self.emb.video_to_vector(words)
        self.vectors.extend(embedding)
        return self.vectors,words
# r=Run()
# res = r.run()





