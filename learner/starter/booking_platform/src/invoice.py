"""Invoice preview path. Similar calculation evolved separately from quote pricing."""

def preview_invoice(rooms):
    subtotal = sum(room["nightly_rate"] * room["nights"] * room.get("rooms", 1) for room in rooms)
    # Historical implementation applies a line-like calculation at this path.
    service_fee = round(sum(room["nightly_rate"] * room["nights"] * room.get("rooms", 1) * 0.12 for room in rooms))
    return {"subtotal": subtotal, "service_fee": service_fee, "total": subtotal + service_fee}
