import re


REFUSAL_MESSAGE = (
    "Maaf, saya hanya dapat membantu pertanyaan terkait layanan purna jual, "
    "garansi, suku cadang, dan booking servis. Saya tidak dapat membantu permintaan tersebut."
)


# TODO(STAGE 1): Add toxic, prompt-injection, and off-topic rules.
TOXIC_PATTERNS = []
PROMPT_INJECTION_PATTERNS = []
IN_SCOPE_KEYWORDS = []


def check_safety(query: str) -> dict:
    text = query.lower()

    # TODO(STAGE 1): Return {"allowed": False, "reason": "toxic_language"} for toxic inputs.
    for pattern in TOXIC_PATTERNS:
        if re.search(pattern, text):
            return {"allowed": False, "reason": "toxic_language"}

    # TODO(STAGE 1): Return {"allowed": False, "reason": "prompt_injection"} for injection attempts.
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text):
            return {"allowed": False, "reason": "prompt_injection"}

    # TODO(STAGE 1): Return off_topic if the query is outside after-sales topics.
    if IN_SCOPE_KEYWORDS and not any(keyword in text for keyword in IN_SCOPE_KEYWORDS):
        return {"allowed": False, "reason": "off_topic"}

    return {"allowed": True, "reason": None}

