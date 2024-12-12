from langchain.text_splitter import TokenTextSplitter
import streamlit as st
def splitter(pdfs, encoding_name = 'gpt2', chunk_size = 100, chunk_overlap = 20):
    # This function is used to split the pdfs' contents to chunks.
    # It is using gpt2 tokenizer.
    # encoding_name: defining the tokenizer.
    # chunk_size: maximum number of tokens in each chunk.
    # chunk_overlap: Number of overlapped tokens from the previous chunk with the new chunk.
    text_splitter = TokenTextSplitter(
    encoding_name=encoding_name, 
    chunk_size=chunk_size,        
    chunk_overlap=chunk_overlap
    )
    print('splitting document...')
    # Concatenating all pdfs to a single string
    all_contents = ""
    for page in pdfs:
        all_contents += page.page_content
    chunks = text_splitter.split_text(all_contents)

    # Returning the chunks
    return chunks