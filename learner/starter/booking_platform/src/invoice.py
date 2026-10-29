"""Invoice preview path using the shared service-fee calculation."""
from src.shared.pricing import calculate_service_fee

def preview_invoice(rooms):
    subtotal = sum(room["nightly_rate"] * room["nights"] * room.get("rooms", 1) for room in rooms)
    service_fee = calculate_service_fee(subtotal)
    return {"subtotal": subtotal, "service_fee": service_fee, "total": subtotal + service_fee}
