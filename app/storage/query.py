class Query:
    def __init__(self, client, collection,model):
        self.client = client
        self.collection_name = collection
        self.embed_model = model

    def request_query(self,query, limit):
        query_vector = self.embed_model.encode(query).tolist()
        res = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            with_payload=True,
            limit= limit
        ).points
        return res