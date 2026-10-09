from pydantic import BaseModel

class JournalRequest(BaseModel):
    entry: str


class JournalResponse(BaseModel):
    mood: str
    supportive_message: str
    suggestions: list[str]

class DailyQuoteResponse(BaseModel):
    quote: str
    date: str