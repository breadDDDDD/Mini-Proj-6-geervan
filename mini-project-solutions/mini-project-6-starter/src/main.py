import time
import uuid

from fastapi import FastAPI

from src.config import settings
from src.costing import estimate_cost_idr
from src.generator import build_context, get_generator
from src.logger import query_hash, write_log
from src.retriever import LocalRetriever
from src.safety import REFUSAL_MESSAGE, check_safety
from src.schemas import ChatRequest, ChatResponse, Source
from src.text_utils import estimate_tokens


app = FastAPI(title="Mini Project 6 Starter")
retriever = LocalRetriever()
generator = get_generator()


@app.get("/health")
def health() -> dict:
    retriever.ensure_loaded()
    return {
        "status": "ok",
        "generator_mode": settings.generator_mode,
        "indexed_chunks": len(retriever.chunks),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    started = time.perf_counter()
    request_id = f"req_{uuid.uuid4().hex[:12]}"
    safety = check_safety(request.query)

    if not safety["allowed"]:
        latency_ms = int((time.perf_counter() - started) * 1000)
        # TODO(STAGE 2): Log refused requests.
        write_log(
            {
                "request_id": request_id,
                "session_id": request.session_id,
                "query_hash": query_hash(request.query),
                "status": "refused",
                "latency_ms": latency_ms,
                "refusal": True,
                "refusal_reason": safety["reason"],
            }
        )
        return ChatResponse(
            answer=REFUSAL_MESSAGE,
            sources=[],
            refusal=True,
            latency_ms=latency_ms,
            status="refused",
        )

    chunks = retriever.search(request.query, top_k=settings.top_k)
    answer = generator.generate(request.query, chunks)
    latency_ms = int((time.perf_counter() - started) * 1000)

    context = build_context(chunks)
    input_tokens = estimate_tokens(request.query + "\n" + context)
    output_tokens = estimate_tokens(answer)

    sources = [
        Source(filename=chunk.filename, chunk_id=chunk.chunk_id, score=chunk.score)
        for chunk in chunks
    ]

    # TODO(STAGE 2): Complete structured logging fields.
    write_log(
        {
            "request_id": request_id,
            "session_id": request.session_id,
            "query_hash": query_hash(request.query),
            "status": "ok",
            "model": settings.llm_model,
            "latency_ms": latency_ms,
            "input_tokens_est": input_tokens,
            "output_tokens_est": output_tokens,
            "retrieved_chunks": len(chunks),
            "sources": [source.filename for source in sources],
            "refusal": False,
            "estimated_cost_idr": estimate_cost_idr(input_tokens, output_tokens),
        }
    )

    return ChatResponse(
        answer=answer,
        sources=sources,
        refusal=False,
        latency_ms=latency_ms,
        status="ok",
    )

