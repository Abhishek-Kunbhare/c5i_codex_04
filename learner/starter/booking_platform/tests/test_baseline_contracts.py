import unittest
from src.api import create_quote
from src.invoice import preview_invoice

class BaselineContracts(unittest.TestCase):
    def test_empty_inputs_preserve_numeric_shape(self):
        for result in (create_quote([]), preview_invoice([])):
            self.assertEqual(result["subtotal"], 0)
            self.assertEqual(result["total"], 0)
            self.assertIsInstance(result["service_fee"], int)
