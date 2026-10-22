import ingestion.extraction as extraction
import ingestion.chanking as chanking
import ingestion.cleaning_text as cleaning_text
import embeddings.embeddings as embeddings
from ingestion.extraction import Extraction 
model = SentenceTransformer("intfloat/multilingual-e5-base")
class Run:
    def __init__(self,question):
        self.emb = embeddings.Embeddings()
        self.chunks = []
        self.vectors = []
        self.title = ""
        self.text = ""
        self.extraction = Extraction(path = "Junior_Py_Dev.pdf")
        self.question = question
        
    def run(self):
        self.text,self.title = self.extraction.extract_text()
        _cleared_text = cleaning_text.clean_text(self.text)
        self.chunks = chanking.chunking(_cleared_text)
        self.vectors = self.emb.text_to_vector(self.chunks)
        query_vector = model.encode(self.question).tolist()
        return self.vectors,self.chunks,self.title






