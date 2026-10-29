"""Approved service-fee behavior for both public calculation paths."""

from src.api import create_quote
from src.invoice import preview_invoice


PUBLIC_PATHS = (create_quote, preview_invoice)
RESPONSE_KEYS = {"subtotal", "service_fee", "total"}


def test_one_line_uses_ten_percent_after_subtotal():
    rooms = [{"nightly_rate": 100, "nights": 2}]
    for calculate in PUBLIC_PATHS:
        result = calculate(rooms)
        assert result == {"subtotal": 200, "service_fee": 20, "total": 220}


def test_multiple_lines_and_optional_room_count():
    rooms = [
        {"nightly_rate": 100, "nights": 2, "rooms": 2},
        {"nightly_rate": 50, "nights": 1},
    ]
    for calculate in PUBLIC_PATHS:
        result = calculate(rooms)
        assert result == {"subtotal": 450, "service_fee": 45, "total": 495}


def test_aggregate_fee_is_rounded_once():
    rooms = [
        {"nightly_rate": 5, "nights": 1},
        {"nightly_rate": 5, "nights": 1},
    ]
    for calculate in PUBLIC_PATHS:
        result = calculate(rooms)
        assert result == {"subtotal": 10, "service_fee": 1, "total": 11}


def test_zero_subtotal_and_response_keys():
    for calculate in PUBLIC_PATHS:
        result = calculate([])
        assert set(result) == RESPONSE_KEYS
        assert result == {"subtotal": 0, "service_fee": 0, "total": 0}
