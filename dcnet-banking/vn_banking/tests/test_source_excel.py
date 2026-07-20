from pathlib import Path

import frappe
from frappe.tests.utils import FrappeTestCase
from openpyxl import Workbook

from vn_banking.source.excel import ExcelFileSource


def _make_mock_xlsx(path: Path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Ngày", "Diễn giải", "Số tiền ghi nợ", "Số tiền ghi có", "Số dư", "Số tham chiếu"])
    ws.append(["08/04/2026", "TT HD SI-0123", "", "12500000", "50000000", "FT123"])
    ws.append(["08/04/2026", "PHI CHUYEN TIEN", "11000", "", "49989000", "FEE01"])
    wb.save(path)


class TestExcelSource(FrappeTestCase):
    """Unit test for ExcelFileSource using a self-contained synthetic xlsx.
    Real bank format tests live in test_parser_all_formats.py (T6)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not frappe.db.exists("Bank", "Test Bank"):
            frappe.get_doc({"doctype": "Bank", "bank_name": "Test Bank"}).insert(ignore_permissions=True)
        if not frappe.db.exists("Bank Statement Format", "TEST-FORMAT"):
            frappe.get_doc({
                "doctype": "Bank Statement Format",
                "format_name": "TEST-FORMAT",
                "bank": "Test Bank",
                "file_type": "xlsx",
                "sheet_index": 0,
                "header_row": 1,
                "data_start_row": 2,
                "col_date": "Ngày",
                "col_narration": "Diễn giải",
                "col_debit": "Số tiền ghi nợ",
                "col_credit": "Số tiền ghi có",
                "col_ref": "Số tham chiếu",
                "date_format": "%d/%m/%Y",
                "decimal_separator": ".",
                "thousands_separator": ",",
            }).insert(ignore_permissions=True)

    def test_parses_synthetic_xlsx(self):
        tmp = Path(frappe.get_site_path("private", "files"))
        tmp.mkdir(parents=True, exist_ok=True)
        p = tmp / "synthetic_test.xlsx"
        _make_mock_xlsx(p)
        src = ExcelFileSource()
        txns = list(src.fetch(
            bank_account=None, from_date=None, to_date=None,
            context={"file_path": str(p), "format_name": "TEST-FORMAT"},
        ))
        self.assertEqual(len(txns), 2)
        self.assertEqual(str(txns[0].deposit), "12500000")
        self.assertEqual(txns[0].direction, "credit")
        self.assertEqual(str(txns[1].withdrawal), "11000")
        self.assertEqual(txns[1].direction, "debit")
        self.assertEqual(txns[0].reference_number, "FT123")
