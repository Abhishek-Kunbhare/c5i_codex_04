import unittest
from src.invoice import preview_invoice

class InvoiceTests(unittest.TestCase):
    def test_one_room_invoice_uses_approved_fee(self):
        result = preview_invoice([{"nightly_rate": 100, "nights": 2}])
        self.assertEqual(result, {"subtotal": 200, "service_fee": 20, "total": 220})

    def test_multiple_lines_preserve_subtotal_and_total_relationship(self):
        rooms = [
            {"nightly_rate": 100, "nights": 2, "rooms": 2},
            {"nightly_rate": 50, "nights": 1},
        ]
        result = preview_invoice(rooms)
        self.assertEqual(result["subtotal"], 450)
        self.assertEqual(set(result), {"subtotal", "service_fee", "total"})
        self.assertEqual(result["total"], result["subtotal"] + result["service_fee"])
