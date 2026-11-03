
class Embeddings:
    def __init__(self,model):
        self.model = model

    def text_to_vector(self, texts: list[dict]):
            passages = [text["text"]for text in texts]
            return self.model.encode(
                passages,
                batch_size=32,
                normalize_embeddings=True,
                show_progress_bar=False
        )
    
    def query_to_vector(self,query:str):
        return self.model.encode(
                f"query: {query}",
                normalize_embeddings=True
            ).tolist()