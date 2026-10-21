import pymupdf


def extract_text():
    doc = pymupdf.open("../6356c48f3b429782050d0025d29af5e5.pdf") # open a document
    out = open("output.txt", "wb") # create a text output
    for page in doc: # iterate the document pages
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
        out.write(text) # write text of page
        out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
        print(page)
    out.close()
    doc.close()
