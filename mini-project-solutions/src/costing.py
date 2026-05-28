from src.config import settings


def estimate_cost_idr(input_tokens: int, output_tokens: int) -> float:
    input_usd = (input_tokens / 1_000_000) * settings.input_usd_per_1m_tokens
    output_usd = (output_tokens / 1_000_000) * settings.output_usd_per_1m_tokens
    infra_buffer_idr = 1.0
    return round((input_usd + output_usd) * settings.idr_per_usd + infra_buffer_idr, 4)

