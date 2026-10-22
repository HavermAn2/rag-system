
def chunking(text,chunk_size=80, overlap=16):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not 0 <= overlap < chunk_size:
        raise ValueError("Invalid overlap")

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
                    chunk = chunk[-overlap:]
        else:
            word += val
    if word:
        chunk.append(word)

    if chunk and (not words or chunk != words[-1]):
        words.append(chunk.copy())
    words = [" ".join(chunk) for chunk in words]
    return words


