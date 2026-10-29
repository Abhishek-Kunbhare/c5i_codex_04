"""HTTP-facing quote orchestration (network layer omitted in training lab)."""
from src.pricing import calculate_quote

def create_quote(rooms):
    """Return the response body used by the booking quote route."""
    result = calculate_quote(rooms)
    return {"subtotal": result["subtotal"], "service_fee": result["service_fee"], "total": result["total"]}
