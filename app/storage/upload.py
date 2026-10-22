from qdrant_client import models

class Upload:
    def __init__(self,client,collection):
        self.client = client
        self.collection_name = collection
        
    def create_point_qdrant(self,title,text,vectors):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,
                    distance=models.Distance.DOT
                )
            )

        points = [
        self.models.PointStruct(
            id=idx,
            vector=vector.tolist() if hasattr(vector, "tolist") else vector,
            payload={
                "title": title,
                "text": chunk,
                "chunk_index": idx,
                "page": 1,
            }
        )
        for idx, (chunk, vector) in enumerate(zip(text, vectors))
        ]
        self.client.upload_points(
            collection_name=self.collection_name,
            points=points
        )