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
        **event,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

