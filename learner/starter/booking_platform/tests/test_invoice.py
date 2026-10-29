import unittest
from src.invoice import preview_invoice

class InvoiceTests(unittest.TestCase):
    def test_legacy_invoice_example(self):
        # Historical test fixture; this expectation is not the approved business policy.
        result = preview_invoice([{"nightly_rate": 100, "nights": 2}])
        self.assertEqual(result, {"subtotal": 200, "service_fee": 24, "total": 224})
