from qdrant_client import QdrantClient,models
# from qdrant_client.models import Distance, VectorParams,PointStruct,Filter, FieldCondition, MatchValuefrom
from sentence_transformers import SentenceTransformer
from main import Run
client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("all-mpnet-base-v2")
        

COLLECTION_NAME = "docs"
r = Run()
vectors,text = r.run()
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=768,
            distance=models.Distance.COSINE
        )
    )
points = [
    models.PointStruct(
        id=idx,
        vector=vector.tolist() if hasattr(vector, "tolist") else vector,
        payload={
            "text": chunk,
            "chunk_index": idx
        }
    )
    for idx, (chunk, vector) in enumerate(zip(text, vectors))
]


client.upload_points(
    collection_name=COLLECTION_NAME,
    points=points
)




question = "Генераторы"

# Получаем готовый embedding
query_vector = model.encode(question).tolist()

# Ищем в Qdrant
hits = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    with_payload=True,
    limit=10
).points

for hit in hits:
    print("Score:", hit.score)
    print("Payload:", hit.payload)