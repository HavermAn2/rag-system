import extraction
import chanking
import cleaning_text

extraction.extract_text()
text = ""
with open("output.txt", "r", encoding="utf-8") as file:
    text = file.read()

cleared_text = cleaning_text.clean_text(text)
words = chanking.chunking(cleared_text)
print(words)