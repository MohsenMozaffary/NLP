import streamlit as st
from utils.Upload import upload_and_makedb
from utils.Response import make_response
import os
import base64

# Setup the database directory
db_dir = os.path.join(os.getcwd(), "db")
if not os.path.exists(db_dir):
    os.mkdir(db_dir)

st.set_page_config(page_title="Course Helper", page_icon="🤖")

# Inject custom CSS to set the background and text styling
def add_styles(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded_string = f"data:image/png;base64,{base64.b64encode(data).decode()}"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .custom-title {{
            color: lightblue;
            font-size: 36px;
            font-weight: bold;
        }}
        .custom-input {{
            color: yellow;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Call the function to set the background and styles
add_styles("background.png")

status_placeholder = st.empty()

# Sidebar inputs
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your API Key:", type="password")

llm_engine = st.sidebar.selectbox("Select LLM Engine:", 
                                  ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4"])
sentence_splitter = st.sidebar.selectbox("Select Splitter:", 
                                         ["r50k_base", "gpt2", "p50k_base", "p50k_edit", "cl100k_base"])
chunk_embedding_model = st.sidebar.selectbox("Select Embedding:", 
                                         ["text-embedding-ada-002", "text-similarity-babbage-001", "text-search-ada-query-001"])

# Main layout
st.markdown('<h1 class="custom-title">PDF-based Chatbot</h1>', unsafe_allow_html=True)

# File upload
uploaded_pdf = st.file_uploader("Upload a PDF file:", type=["pdf"])

if "vectordb" not in st.session_state:
    st.session_state.vectordb = None  # Initialize the state

if uploaded_pdf:  # Check if a file is uploaded
    if st.session_state.vectordb is None:  # Create the vector database only once
        status_placeholder.write("Creating vector database...")
        st.session_state.vectordb = upload_and_makedb(
            uploaded_pdf, db_dir, encoder=sentence_splitter, embedding=chunk_embedding_model, api_key=api_key
        )
        st.write("Vector database creation complete!")

course_name = st.text_input("Course Name:", value="", placeholder="Enter the course name here")

# User query input
user_query = st.text_input("Ask a question about the content:", placeholder="Type your question here...")
mode = st.radio("Select a mode:", ["Only use the pdf", "Use pdf and LLM knowledge"])

# A button to trigger the query
if st.button("Get Answer"):
    if not api_key:
        st.warning("Please provide an API key in the sidebar.")
    elif not uploaded_pdf:
        st.warning("Please upload a PDF file first.")
    elif not user_query.strip():
        st.warning("Please enter a question.")
    else:
        answer = make_response(
            user_query, st.session_state.vectordb, course_name, api_key, llm_engine, N=5, mode=mode
        )
        st.write(f"<div class='custom-input'>{answer}</div>", unsafe_allow_html=True)
