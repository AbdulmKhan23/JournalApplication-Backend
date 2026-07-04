from fastapi import FastAPI, HTTPException

from models import JournalRequest, JournalResponse
from services import analyze_journal

app = FastAPI(
    title="AI Journal API"
)


@app.get("/")
def home():
    return {
        "message": "AI Journal API is running."
    }


@app.post("/analyze", response_model=JournalResponse)
def analyze(request: JournalRequest):

    if len(request.entry.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Journal entry cannot be empty."
        )

    if len(request.entry.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Journal entry is too short."
        )

    try:

        result = analyze_journal(request.entry)

        return JournalResponse(
            mood=result.get("mood", ""),
            supportive_message=result.get(
                "supportive_message",
                ""
            ),
            suggestions=result.get(
                "suggestions",
                []
            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )