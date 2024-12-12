from openai import OpenAI
import os

def embed_query(query_text, api_key, chunk_embedding_model = "text-embedding-ada-002"):

    """
    Generate an embedding for the given query text using text-embedding-ada-002.
    """

    client = OpenAI(
        api_key=os.environ[api_key],  # this is also the default, it can be omitted
        )
    response = client.embeddings.create(
        input=query_text,
        model=chunk_embedding_model
    )

    return response.data[0].embedding