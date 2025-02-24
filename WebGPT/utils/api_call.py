import openai
import yaml
from openai import OpenAI
import os

def function_call_api(query, all_functions, key, model = "gpt-4o", config_name = "prompts.yml", temperature = 0):
    current_folder = os.getcwd()
    config_folder = os.path.join(current_folder, "utils", config_name)
    
    with open(config_folder, 'r') as file:
        yaml_content = yaml.safe_load(file)
        
    prompt_function_call = yaml_content['prompt_function_call']
    
    client = OpenAI(api_key = key)
    
    response = client.chat.completions.create(
        model = model,
        messages = [
            {"role": "system", "content":prompt_function_call},
            {"role": "user", "content":query}
        ],
        temperature = temperature,
        tools = all_functions,
    )
       
    return response

def function_call_final(history, web_search, query, key, model = "gpt-4o", config_name = "prompts.yml", temperature = 0):
    current_folder = os.getcwd()
    config_folder = os.path.join(current_folder, "utils", config_name)
    
    with open(config_folder, 'r') as file:
        yaml_content = yaml.safe_load(file)
        
    prompt_system_role = yaml_content['prompt_system_role']
    
    client = OpenAI(api_key = key)
    
    response = client.chat.completions.create(
        model = model,
        messages = [
            {"role": "system", "content":prompt_system_role},
            {"role": "user", "content":history + web_search + query}
        ],
        temperature = temperature
    )
       
    return response.choices[0].message.content.strip()      