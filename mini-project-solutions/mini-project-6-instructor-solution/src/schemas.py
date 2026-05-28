from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(default="anonymous", max_length=128)


class Source(BaseModel):
    filename: str
    chunk_id: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    refusal: bool
    latency_ms: int
    status: str

