import unittest
from vn_accounting.forecast.aggregator import validate_entry


class TestValidateEntry(unittest.TestCase):
    def _valid_entry(self):
        return {
            "expected_date": "2026-06-15",
            "amount": 15000000.0,
            "direction": "inflow",
            "category": "Contract Service",
            "confidence": "committed",
            "source_doctype": "DCNet Contract",
            "source_name": "CTR-001",
        }

    def test_valid_entry_accepted(self):
        result = validate_entry(self._valid_entry(), "test.provider")
        self.assertIsNotNone(result)

    def test_valid_entry_with_optionals(self):
        entry = self._valid_entry()
        entry.update({"party_type": "Customer", "party": "VNPT", "description": "Service fee"})
        result = validate_entry(entry, "test.provider")
        self.assertIsNotNone(result)

    def test_missing_required_field(self):
        entry = self._valid_entry()
        del entry["expected_date"]
        result = validate_entry(entry, "test.provider")
        self.assertIsNone(result)

    def test_negative_amount(self):
        entry = self._valid_entry()
        entry["amount"] = -100
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_zero_amount(self):
        entry = self._valid_entry()
        entry["amount"] = 0
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_invalid_direction(self):
        entry = self._valid_entry()
        entry["direction"] = "credit"
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_invalid_confidence(self):
        entry = self._valid_entry()
        entry["confidence"] = "maybe"
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_overdue_confidence_accepted(self):
        entry = self._valid_entry()
        entry["confidence"] = "overdue"
        self.assertIsNotNone(validate_entry(entry, "test.provider"))

    def test_bad_date_format(self):
        entry = self._valid_entry()
        entry["expected_date"] = "15/06/2026"
        self.assertIsNone(validate_entry(entry, "test.provider"))

    def test_amount_not_number(self):
        entry = self._valid_entry()
        entry["amount"] = "fifteen million"
        self.assertIsNone(validate_entry(entry, "test.provider"))


if __name__ == "__main__":
    unittest.main()
