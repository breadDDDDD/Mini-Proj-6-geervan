import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import settings


def query_hash(query: str) -> str:
    digest = hashlib.sha256(query.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def write_log(event: dict[str, Any], path: Path | None = None) -> None:
    log_path = path or settings.app_log_path
    log_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": event.get("request_id"),
        "status": event.get("status"),
        "latency_ms": event.get("latency_ms", 0),
        "input_tokens_est": event.get("input_tokens_est", 0),
        "output_tokens_est": event.get("output_tokens_est", 0),
        "sources": event.get("sources", []),
        "refusal_reason": event.get("refusal_reason"),
        **event,
    }

    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
