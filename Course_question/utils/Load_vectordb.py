import chromadb
from chromadb.utils import embedding_functions

def load_vectordb(db_dir, collection_name, embedding="text-embedding-ada-002", api_key="OPENAI_API_KEY"):
    try:
        # Connect to the persistent Chroma DB
        chroma_client = chromadb.PersistentClient(path=db_dir)
        
        # Specify the embedding function (same as used during creation)
        embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            model_name=embedding, 
            api_key=api_key
        )
        
        # Get the collection
        collection = chroma_client.get_collection(
            name=collection_name, 
            embedding_function=embedding_function
        )
        
        print("Vector database loaded successfully.")
        return collection
    except Exception as e:
        print(f"Error loading vector database: {e}")
        return None
