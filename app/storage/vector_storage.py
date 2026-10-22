from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from query import Query
from upload import Upload
from ingestion.extraction import Extraction
client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("intfloat/multilingual-e5-base")
query = "Типы данных в Пайтон" 
extraction = Extraction("data/Junior_Py_Dev.py")
txt,title = extraction.extract_text()
COLLECTION_NAME = "docs"
q = Query(client,COLLECTION_NAME,model)
u = Upload(client,COLLECTION_NAME)

res = q.request_query(query,15)
upload = u.create_point_qdrant()
print(res)









