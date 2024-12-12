import tempfile
from utils.Loader import import_pdf
from utils.Splitter import splitter
import streamlit as st
from utils.Embed_batch import embed_batch
import time
import gc
import chromadb
from chromadb.utils import embedding_functions

def upload_and_makedb(pdf, db_dir, batch_size= 30, encoder = 'gpt2', embedding = "text-embedding-ada-002", api_key="OPENAI_API_KEY"):
    

    status_placeholder = st.empty()

    status_placeholder.write("Importing pdf file...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf.getvalue())
        tmp_file_path = tmp_file.name

    pdf_uploaded = import_pdf([tmp_file_path])

    status_placeholder.write("Chunking pdf...")
    chunks = splitter(pdf_uploaded, encoding_name = encoder)
    chunks = chunks[:90]
    # documents = [Document(page_content=chunk) for chunk in chunks]
    # documents = [Document(page_content="This is a test.")]
    status_placeholder.write("Making database...")
    collection_name = "vector_database"
    chroma_client = chromadb.PersistentClient(path=db_dir)
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(model_name = embedding ,api_key= api_key)
    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function)
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        embeddings = embed_batch(batch)
        ids = [f"doc-{i+j}" for j in range(len(batch))]
        metadata = [{"chunk_id": i+j} for j in range(len(batch))]
        collection.add(
        documents=batch,
        metadatas=metadata,
        ids=ids,
        embeddings=embeddings
        )

        del embeddings, batch, ids, metadata
        gc.collect()
        time.sleep(2)
    
    try:
        chroma_client = chromadb.PersistentClient(path=db_dir)
        st.write("Chroma DB created successfully.")
    except Exception as e:
        st.error(f"Error creating Chroma DB: {e}")
    
    return collection



