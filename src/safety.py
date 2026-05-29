import re


REFUSAL_MESSAGE = (
    "Maaf, saya hanya dapat membantu pertanyaan terkait layanan purna jual, "
    "garansi, suku cadang, dan booking servis. Saya tidak dapat membantu permintaan tersebut."
)


TOXIC_PATTERNS = [
    r"\b(bodoh|goblok|tolol|bangsat|anjing|kontol|memek)\b",
    r"\b(stupid|idiot|moron|bastard|fuck(?:ing)?)\b",
]
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|system)\s+instructions",
    r"(reveal|show|print)\s+(the\s+)?(system\s+prompt|hidden\s+prompt)",
    r"jailbreak",
    r"developer\s+mode",
    r"abaikan\s+(semua\s+)?instruksi",
]
IN_SCOPE_KEYWORDS = [
    "garansi",
    "warranty",
    "servis",
    "service",
    "booking",
    "jadwal",
    "suku cadang",
    "spare part",
    "part",
    "harga",
    "filter",
    "oli",
    "klaim",
    "after-sales",
    "purna jual",
]


def check_safety(query: str) -> dict:
    text = query.lower()

    for pattern in TOXIC_PATTERNS:
        if re.search(pattern, text):
            return {"allowed": False, "reason": "toxic_language"}

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text):
            return {"allowed": False, "reason": "prompt_injection"}

    if IN_SCOPE_KEYWORDS and not any(keyword in text for keyword in IN_SCOPE_KEYWORDS):
        return {"allowed": False, "reason": "off_topic"}

    return {"allowed": True, "reason": None}
