from datetime import date

from fastapi import FastAPI, HTTPException, Query

from backend.models import JournalRequest, JournalResponse
from backend.services import GeminiUnavailable
from backend.services import analyze_journal, TokenLimitExceeded
from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from backend.models import DailyQuoteResponse
from backend.services import get_daily_quote


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="AI Journal API"
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

@app.get("/")
@limiter.limit("30/minute")
def home(request: Request):
    return {
        "message": "AI Journal API is running."
    }

@app.get("/daily-quote", response_model=DailyQuoteResponse)
@limiter.limit("30/minute")
def daily_quote(
    request: Request,
    day: date = Query(alias="date"),
):
    try:
        return get_daily_quote(day.isoformat())
    except GeminiUnavailable as exc:
        raise HTTPException(
            status_code=503,
            detail="Today's quote is temporarily unavailable.",
            headers={"Retry-After": "30"},
        ) from exc

@app.post("/analyze", response_model=JournalResponse)
@limiter.limit("5/minute")
def analyze(request: Request, journal: JournalRequest):

    if len(journal.entry.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Journal entry cannot be empty."
        )

    if len(journal.entry.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Journal entry is too short."
        )

    try:

        result = analyze_journal(journal.entry)

        return JournalResponse(
            mood=result.get("mood", ""),
            supportive_message=result.get( "supportive_message",""),
            suggestions=result.get("suggestions",[])
        )

    except TokenLimitExceeded as exc:
        raise HTTPException(
            status_code=413,
            detail=str(exc),
        ) from exc

    except GeminiUnavailable as exc:
        raise HTTPException(
            status_code=503,
            detail="AI analysis is temporarily unavailable. Please try again later.",
            headers={"Retry-After": "30"},
        ) from exc
    except Exception as e:
        raise HTTPException(
             status_code=500,
             detail=str(e)
            )
