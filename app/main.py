import extraction
import chanking
import cleaning_text
import embeddings
emb = embeddings.Embeddings()
vectors = []
extraction.extract_text()
text = ""
with open("output.txt", "r", encoding="utf-8") as file:
    text = file.read()
cleared_text = cleaning_text.clean_text(text)
words = chanking.chunking(cleared_text)
embedding = emb.video_to_vector(words)
vectors.extend(embedding)
print(len(vectors))
print(len(text))