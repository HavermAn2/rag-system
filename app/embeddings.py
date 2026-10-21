from sentence_transformers import SentenceTransformer

class Embeddings:
    def __init__(self):
        self.model = SentenceTransformer("all-mpnet-base-v2")

    def video_to_vector(self,text:str):
        return self.model.encode(text, batch_size=32)
    
