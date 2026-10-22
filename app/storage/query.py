
class Query:
    def __init__(self, client, collection,model):
        self.client = client
        self.collection_name = collection
        self.embed_model = model

    def request_query(self,query, limit):
        res = self.client.query_points(
            collection_name=self.collection_name,
            query=query,
            with_payload=True,
            limit= limit
        ).points
        return res