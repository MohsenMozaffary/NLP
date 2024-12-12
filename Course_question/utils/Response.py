from utils.Similarity import similarity_search
from openai import OpenAI
import yaml
import os
import streamlit as st
from utils.Embed_query import embed_query



def make_response(query, vectordb, course_name, api_key, llm_engine, chunk_embedding_model = "text-embedding-ada-002", N=5, mode = 0):
    st.write(os.getcwd())
    with open(r"./utils/Config.yml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    _ = config["language_config"]["max_token"]
    system_role = config["language_config"]["system_role_1"]
    if mode == "Use pdf and LLM knowledge":
        system_role = config["language_config"]["system_role_2"]
    embedded = embed_query(query, api_key, chunk_embedding_model = chunk_embedding_model)
    retrieved = vectordb.query(
    query_embeddings=[embedded],  # Embedding of the query
    n_results=N  # Number of results to retrieve
    )
    retrieved_contents = [str(d)+"\n\n" for d in retrieved['documents'][0]]
    

    prompt = "# User's question: \n" + query + "# Retrieved content number:\n" + str(retrieved_contents) + "# Name of the course: \n" + str(course_name)
    client = OpenAI(api_key=os.environ[api_key])
    response = client.chat.completions.create(
        model= llm_engine,
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
            ]
    )

    return response.choices[0].message.content.strip()