import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
MAX_INPUT_TOKENS = 1_000
MAX_OUTPUT_TOKENS = 300

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

class TokenLimitExceeded(Exception):
    pass

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
Stressed
Motivated
Calm
Anxious
Lonely
Excited
Overwhelmed

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
