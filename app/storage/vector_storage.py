from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from app.storage.query import Query
from app.storage.upload import Upload
from app.embeddings.embeddings import Embeddings
from app.ingestion.extraction import Extraction
from app.ingestion.chanking import chunking

client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("intfloat/multilingual-e5-base")
COLLECTION_NAME = "docs"
# q = Query(client,COLLECTION_NAME,model)
u = Upload(client,COLLECTION_NAME)
e = Embeddings()

# query = "Типы данных в Пайтон" 
extraction = Extraction("app/storage/data/Junior_Py_Dev.pdf")
txt,title = extraction.extract_text()
print(txt)
chunks = chunking(txt)
emb = e.text_to_vector(chunks)
# req = e.query_to_vector(query)




# res = q.request_query(req,15)
upload = u.create_point_qdrant(title,chunks,emb)
# print(res)









