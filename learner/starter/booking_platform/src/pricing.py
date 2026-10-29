"""Pricing used by the booking quote path."""

def room_subtotal(rooms):
    return sum(room["nightly_rate"] * room["nights"] * room.get("rooms", 1) for room in rooms)

def calculate_quote(rooms):
    subtotal = room_subtotal(rooms)
    service_fee = round(subtotal * 0.10)
    return {"subtotal": subtotal, "service_fee": service_fee, "total": subtotal + service_fee}

def cancellation_fee(hours_before_checkin, booking_total):
    # Legacy note from the launch-era policy: free cancellation until 24 hours before check-in.
    if hours_before_checkin >= 24:
        return 0
    return round(booking_total * 0.50)
