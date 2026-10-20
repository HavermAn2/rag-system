text = "Python- /?is a powerful    pr!ogramming language us-ed for AI development"



def chunking(text,chunk_size=60):
    chunk = []
    word = ""
    words = []
    for i, val in enumerate(text):
        if val.isspace():
            if word:
                chunk.append(word)
                word = ""

                if len(chunk) == chunk_size:
                    words.append(chunk.copy())
                    chunk = chunk[-1:]

        else:
            word += val

    if word:
        chunk.append(word)

    if chunk and (not words or chunk != words[-1]):
        words.append(chunk.copy())
    words = [" ".join(chunk) for chunk in words]
    return words


