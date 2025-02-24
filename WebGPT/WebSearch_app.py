# Frontend of WebGPT for interet search

import streamlit as st
from streamlit_chat import message
from utils.api_call import *
from utils.web_functions import *
import json

st.set_page_config(
    page_title="WebSearch",
    layout="wide"
)

# Custom heading with CSS styling
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
    <style>
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        .custom-heading {
            text-align: center;
            font-family: 'Pacifico', cursive;
            font-size: 50px;
            color: white;
            background: linear-gradient(90deg, #FF5733, #33FF57);
            padding: 20px;
            border-radius: 10px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
            animation: fadeIn 2s;
        }
    </style>
    <h1 class="custom-heading">
        WebGPT
    </h1>
    """,
    unsafe_allow_html=True
)

# Available GPT models
gpt_models = ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "deepseek"]

# Sidebar: Model selection and parameters
selected_model = st.sidebar.selectbox("Choose a model:", gpt_models)
history_length = st.sidebar.slider("History range:", min_value=1, max_value=10)
temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
max_answers = st.sidebar.slider("Max number of answers:", min_value=1, max_value=10, value=1, step=1)

# Sidebar: Function selection
selected_functions = []
st.sidebar.title("Choose functions")
if st.sidebar.checkbox("text_search"):
    selected_functions.append(text_search)
if st.sidebar.checkbox("pdf_search"):
    selected_functions.append(pdf_search)
if st.sidebar.checkbox("image_search"):
    selected_functions.append(image_search)
if st.sidebar.checkbox("video_search"):
    selected_functions.append(video_search)
if st.sidebar.checkbox("news_search"):
    selected_functions.append(news_search)

# Sidebar: API keys
openai_api_key = st.sidebar.text_input("Enter your OpenAI API key:", placeholder="Write your API key here...")
deepseek_api_key = st.sidebar.text_input("Enter your DeepSeek API key:", placeholder="Write your API key here...")

# Chat history layout
history_layout = st.container()
current_layout = st.container()

# Chat history CSS
history_layout.markdown("""
    <style>
        .chat-history {
            height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #f9f9f9;
            margin-bottom: 10px;
        }
    </style>""", unsafe_allow_html=True
)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'chats' not in st.session_state:
    st.session_state['chats'] = []
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []

# User input section
with current_layout:
    with st.form(key='my_form', clear_on_submit=True):
        input_text = st.text_area(
            "You:", placeholder="Ask me anything...", height=120, 
            max_chars=300, help="Enter a message and press submit.", key="input"
        )
        submitted = st.form_submit_button(label="Submit", help="Click to send your message.", type="primary")

# Process input when submitted
if submitted and input_text.strip():
    st.session_state['user_input'].append(input_text)  # Store raw input text

    # Get previous chat history within history_length range
    history = "\n".join(st.session_state['history'][-history_length:])
    
    # Create function call input
    function_call_input = f"# Previous chats are:\n {history} \n\nUser input is:\n {input_text}"
    
    all_functions = function_wrapper(selected_functions)

    if openai_api_key:
        response = function_call_api(
            function_call_input, all_functions, openai_api_key, 
            model=selected_model, config_name="prompts.yml", temperature=temperature
        )

        # Process response
        if response.choices[0].message.tool_calls:
            function_name = response.choices[0].message.tool_calls[0].function.name
            args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
            args['max_results'] = max_answers

            api_function_call_output = function_selection(function_name, args)
            answer = "".join([str(api_function_call_output[i]) for i in range(len(api_function_call_output))])

            # Generate final response
            response_llm2 = function_call_final(
                history, answer, input_text, openai_api_key, 
                model=selected_model, config_name="prompts.yml", temperature=temperature
            )

            # Store response in session history
            information = f"User input: {input_text} \n\nResponse: {response_llm2} \n\n"
            st.session_state['history'].append(information)
            st.session_state['chats'].append(response_llm2)
        
        else:
            st.session_state['chats'].append(response.choices[0].message.content.strip())

# Display chat history properly
if st.session_state['chats']:
    with history_layout:
        for c in range(len(st.session_state['chats'])):
            message(st.session_state['user_input'][c], is_user=True, key=f"{c}_user")
            message(st.session_state['chats'][c], key=str(c))
