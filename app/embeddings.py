from sentence_transformers import SentenceTransformer

class Embeddings:
    def __init__(self):
        self.model = SentenceTransformer("intfloat/multilingual-e5-base")

    def video_to_vector(self,text:str):
        return self.model.encode(text, batch_size=32)
    
