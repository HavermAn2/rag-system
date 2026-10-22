from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from query import Query
from upload import Upload
from embeddings.embeddings import Embeddings
from ingestion.extraction import Extraction
from ingestion.chanking import chunking

client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("intfloat/multilingual-e5-base")
COLLECTION_NAME = "docs"
q = Query(client,COLLECTION_NAME,model)
u = Upload(client,COLLECTION_NAME)
e = Embeddings()

query = "Типы данных в Пайтон" 
extraction = Extraction("data/Junior_Py_Dev.py")
txt,title = extraction.extract_text()
chunks = chunking(txt)
emb = e.text_to_vector(chunks)
req = e.query_to_vector(query)




res = q.request_query(req,15)
upload = u.create_point_qdrant(title,chunks,emb)
print(res)









