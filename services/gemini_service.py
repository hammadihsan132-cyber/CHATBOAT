import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Models in priority order — try the first, fall back if overloaded
MODEL_FALLBACK_CHAIN = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.5-flash-lite",
]

def get_chat_response(messages: list):
    contents = []
    for m in messages:
        role = "model" if m["role"] == "assistant" else "user"
        contents.append(
            types.Content(role=role, parts=[types.Part(text=m["content"])])
        )

    last_error = None

    for model_name in MODEL_FALLBACK_CHAIN:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents
                )
                return response.text
            except ServerError as e:
                last_error = e
                time.sleep(2 ** attempt)  # 1s, 2s backoff
                continue
        # this model failed both attempts, try the next model

    raise last_error