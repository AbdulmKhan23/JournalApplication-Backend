import os
import json
import httpx

from google.genai import errors
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
MAX_INPUT_TOKENS = 1_000
MAX_OUTPUT_TOKENS = 300

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
http_options=types.HttpOptions(
        timeout=10_000  # 10 seconds, measured in milliseconds
    ),
)
class GeminiUnavailable(Exception):
    pass

class TokenLimitExceeded(Exception):
    pass

def generate_response(entry: str):
    try:
        return client.models.generate_content(
            model="gemini-2.5-flash",
            contents=entry,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

    except errors.ClientError as exc:
        if exc.code == 429:
            raise GeminiUnavailable(
                "Gemini is temporarily unavailable."
            ) from exc
        raise

    except (
        errors.ServerError,
        httpx.TimeoutException,
        httpx.TransportError,
    ) as exc:
        raise GeminiUnavailable(
            "Gemini is temporarily unavailable."
        ) from exc

def analyze_journal(entry: str):

    prompt = f"""
You are an AI journaling assistant.

Analyze the user's journal entry.

Tasks:
1. Detect the user's mood.
2. Give a supportive response.
3. Suggest exactly 2 helpful activities.

Possible moods:

Happy
Sad
Calm
Anxious
Angry
Neutral

Journal Entry:

{entry}

Return ONLY JSON.

{{
    "mood":"",
    "supportive_message":"",
    "suggestions":[
        "",
        ""
    ]
}}
"""
    token_count = client.models.count_tokens(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    if token_count.total_tokens > MAX_INPUT_TOKENS:
        raise TokenLimitExceeded(
            f"Input exceeds the {MAX_INPUT_TOKENS}-token limit."
        )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )



    return json.loads(response.text)
