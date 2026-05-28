import re


REFUSAL_MESSAGE = (
    "Maaf, saya hanya dapat membantu pertanyaan terkait layanan purna jual, "
    "garansi, suku cadang, dan booking servis. Saya tidak dapat membantu permintaan tersebut."
)


TOXIC_PATTERNS = [
    r"\b(bodoh|tolol|bangsat|anjing|goblok)\b",
    r"\b(stupid|idiot|hate|kill yourself)\b",
]

PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions",
    r"abaikan (semua )?instruksi",
    r"system prompt",
    r"developer message",
    r"hidden prompt",
    r"reveal your instructions",
    r"bocorkan instruksi",
    r"tampilkan instruksi",
    r"jangan ikuti aturan",
]

IN_SCOPE_KEYWORDS = [
    "servis",
    "service",
    "warranty",
    "garansi",
    "spare",
    "part",
    "suku",
    "cadang",
    "booking",
    "dealer",
    "manual",
    "oli",
    "oil",
    "brake",
    "rem",
    "mitsubishi",
    "xpander",
    "pajero",
    "triton",
    "outlander",
    "filter",
    "kampas",
    "jadwal",
    "interval",
    "klaim",
    "claim",
    "maintenance",
    "ban",
    "tire",
    "tekanan",
    "pressure",
    "aki",
    "battery",
    "inspeksi",
    "inspection",
]


def check_safety(query: str) -> dict:
    text = query.lower()

    for pattern in TOXIC_PATTERNS:
        if re.search(pattern, text):
            return {"allowed": False, "reason": "toxic_language"}

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text):
            return {"allowed": False, "reason": "prompt_injection"}

    if not any(keyword in text for keyword in IN_SCOPE_KEYWORDS):
        return {"allowed": False, "reason": "off_topic"}

    return {"allowed": True, "reason": None}
