def sliding_window_chunk(text, chunk_size=2, overlap=1):
    tokens = text.split()
    chunks = []
    print("Original Text:", tokens)
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = ' '.join(tokens[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Applying Sliding Window Chunking
sliding_chunks = sliding_window_chunk("This is sample sentence to be chunked.")
for chunk in sliding_chunks:
    print(chunk, '\n---\n')
