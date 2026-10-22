
class Query:
    def __init__(self, client, model, collection):
        self.client = client
        self.collection_name = collection
        self.query = query
        self.embed_model = model

    def request_query(self,query, limit):
        query_vector = self.embed_model.encode(self.query).tolist()
        res = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            with_payload=True,
            limit= limit
        ).points
        return res