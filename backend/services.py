import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)