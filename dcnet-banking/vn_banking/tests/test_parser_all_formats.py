from pathlib import Path

import frappe
from frappe.tests.utils import FrappeTestCase

from vn_banking.source.excel import ExcelFileSource


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _ensure_bank(name: str):
    if not frappe.db.exists("Bank", name):
        frappe.get_doc({"doctype": "Bank", "bank_name": name}).insert(ignore_permissions=True)


class TestParserAllFormats(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for b in ["BIDV", "MB Bank", "Sacombank", "PG Bank"]:
            _ensure_bank(b)

    def _fetch(self, sample_file: str, format_name: str):
        path = FIXTURES_DIR / sample_file
        self.assertTrue(path.exists(), f"Missing fixture: {path}")
        self.assertTrue(frappe.db.exists("Bank Statement Format", format_name),
                        f"Missing format fixture: {format_name}")
        src = ExcelFileSource()
        return list(src.fetch(
            bank_account=None, from_date=None, to_date=None,
            context={"file_path": str(path), "format_name": format_name},
        ))

    def test_bidv_parses(self):
        txns = self._fetch("bidv_sample.xls", "BIDV - Sao k\u00ea t\u00e0i kho\u1ea3n")
        self.assertGreater(len(txns), 0, "Expected at least 1 BIDV transaction")
        first = txns[0]
        self.assertEqual(first.direction, "debit")
        self.assertTrue(first.reference_number.startswith("FT26"))
        self.assertIn("TESTCO", first.description)

    def test_mb_parses(self):
        txns = self._fetch("mb_sample.xlsx", "MB Bank - Sao k\u00ea chi ti\u1ebft")
        self.assertGreater(len(txns), 0)
        first = txns[0]
        self.assertEqual(first.direction, "debit")
        self.assertEqual(int(first.withdrawal), 126000000)

    def test_sacombank_parses(self):
        txns = self._fetch("sacombank_sample.xls", "Sacombank - Sao k\u00ea giao d\u1ecbch")
        self.assertGreater(len(txns), 0)
        first = txns[0]
        self.assertEqual(first.direction, "debit")

    def test_pgbank_parses(self):
        txns = self._fetch("pgbank_sample.xls", "PG Bank - Transaction Detail")
        self.assertGreater(len(txns), 0)
        for t in txns:
            self.assertNotIn("S\u1ed1 d\u01b0 cu\u1ed1i ng\u00e0y", t.description)
            self.assertTrue(t.reference_number)
