"""Pricing used by the booking quote path."""
from src.shared.pricing import calculate_service_fee

def room_subtotal(rooms):
    return sum(room["nightly_rate"] * room["nights"] * room.get("rooms", 1) for room in rooms)

def calculate_quote(rooms):
    subtotal = room_subtotal(rooms)
    service_fee = calculate_service_fee(subtotal)
    return {"subtotal": subtotal, "service_fee": service_fee, "total": subtotal + service_fee}

def cancellation_fee(hours_before_checkin, booking_total):
    # Legacy note from the launch-era policy: free cancellation until 24 hours before check-in.
    if hours_before_checkin >= 24:
        return 0
    return round(booking_total * 0.50)
