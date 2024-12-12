import time
import openai
from openai import OpenAI
import os

def embed_batch(batch, api_key = 'OPENAI_API_KEY', model="text-embedding-ada-002"):
    embeddings = []
    client = OpenAI(
        api_key=os.environ[api_key],  # this is also the default, it can be omitted
        )
    for _ in range(3):  # Retry up to 3 times
        try:
            response = client.embeddings.create(
                model=model,
                input=batch
            )
            for i in range(len(batch)):
                embeddings.append(response.data[i].embedding)
            return embeddings
        except openai.error.RateLimitError:
            print("Rate limit exceeded. Retrying in 10 seconds...")
            time.sleep(2)
        except openai.error.APIError as e:
            print(f"API error: {e}. Retrying in 5 seconds...")
            time.sleep(2)
        except Exception as e:
            print(f"Unexpected error in embedding batch: {e}")
            break
    return []