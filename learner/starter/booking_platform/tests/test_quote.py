import unittest
from src.api import create_quote

class QuoteTests(unittest.TestCase):
    def test_one_room_quote(self):
        result = create_quote([{"nightly_rate": 100, "nights": 2}])
        self.assertEqual(result, {"subtotal": 200, "service_fee": 20, "total": 220})

    def test_quote_response_keys(self):
        self.assertEqual(set(create_quote([])), {"subtotal", "service_fee", "total"})
