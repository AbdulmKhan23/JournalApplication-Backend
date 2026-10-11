from pydantic import BaseModel, Field


class JournalRequest(BaseModel):
    entry: str


class JournalResponse(BaseModel):
    mood: str
    supportive_message: str
    suggestions: list[str]

class DailyQuoteResponse(BaseModel):
    quote: str
    date: str

class ReflectQuestionRequest(BaseModel):
    excluded_questions: list[str] = Field(default_factory=list)


class ReflectQuestionResponse(BaseModel):
    question: str