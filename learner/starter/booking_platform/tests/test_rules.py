import unittest
from src.rules import cancellation_fee_due

class RuleTests(unittest.TestCase):
    def test_legacy_cancellation_boundary(self):
        self.assertEqual(cancellation_fee_due(24, 200), 0)
        self.assertEqual(cancellation_fee_due(23, 200), 100)
