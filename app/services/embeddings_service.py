
class Embeddings:
    def __init__(self,model):
        self.model = model

    def text_to_vector(self,text:str):
        return self.model.encode(text, batch_size=32)
    
    def query_to_vector(self,query:str):
        return self.model.encode(
                f"query: {query}",
                normalize_embeddings=True
            ).tolist()