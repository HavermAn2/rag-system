from qdrant_client import QdrantClient,models
from sentence_transformers import SentenceTransformer
from main import Run
client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("intfloat/multilingual-e5-base")
        

COLLECTION_NAME = "docs"
r = Run("Типы данных в Пайтон")
vectors,text,title = r.run()
client.delete_collection(collection_name=COLLECTION_NAME)
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=768,
            distance=models.Distance.DOT
        )
    )

points = [
    models.PointStruct(
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


client.upload_points(
    collection_name=COLLECTION_NAME,
    points=points
)





query_vector = model.encode(question).tolist()


hits = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    with_payload=True,
    limit=10
).points

for hit in hits:
    print("Score:", hit.score)
    print("Title:", hit.payload["title"])
    print("Text:", hit.payload["text"])
    print("Page:", hit.payload["page"])