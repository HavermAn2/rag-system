from qdrant_client import models
from uuid import uuid4
class Upload:
    def __init__(self,client,collection):
        self.client = client
        self.collection_name = collection
        
    def create_point_qdrant(self,title,text,vectors):
        # self.client.delete(
        #     collection_name="docs",
        #     points_selector=models.FilterSelector(
        #         filter=models.Filter(must=[])
        #     ),
        #     wait=True
        # )
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,
                    distance=models.Distance.DOT
                )
            )

        points = [
        models.PointStruct(
            id=str(uuid4()),
            vector=vector.tolist() if hasattr(vector, "tolist") else vector,
            payload={
                "title": title,
                "page": chunk["page"],
                "text": chunk["text"],
                "chunk_index": idx,
                
            }
        )
        for idx, (chunk, vector) in enumerate(zip(text, vectors))
        ]
        self.client.upload_points(
            collection_name=self.collection_name,
            points=points
        )
        # print(type(text))
        # print(type(text[0]))
        # print(len(text))
        # print(len(vectors))
        return print({"OK":200})