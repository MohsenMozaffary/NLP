
def similarity_search(query, vectordb, N=5):
    docs = vectordb.similarity_search(query, k=N)
    retrieved_contents = [str(d.page_content)+"\n\n" for d in docs]

    return retrieved_contents