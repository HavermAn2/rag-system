from app.services.embeddings_service import Embeddings
from app.services.llm_service import llm
class Query:
    def __init__(self, client, collection, model):
        self.client = client
        self.collection_name = collection
        self.embed_model = Embeddings(model)

    def request_query(self,query, limit):
        tsk_embed = self.embed_model.query_to_vector(query)
        res = self.client.query_points(
            collection_name=self.collection_name,
            query=tsk_embed,
            with_payload=True,
            limit= limit
        ).points
        chunks = []
        for point in res:
            chunks.append(point.payload["text"])
        answer = llm(chunks,user_query = query)
        return answer