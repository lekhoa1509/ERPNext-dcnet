"""Unit tests for parsers/invoice_list_parser.py.

Pure-function tests over both BR (sales) and MV (purchase) shapes.
"""

from __future__ import annotations

import unittest

from vn_accounting.misa_migration.parsers.invoice_list_parser import (
    parse_invoice_list,
    parse_tax_rate,
)


def _br_row(voucher_no, item_name, qty, rate, net, tax_pct, tax_amt, **kw):
    """Build a BR (sales) row dict with sensible defaults."""
    d = {
        "Ký hiệu mẫu HĐ": "1",
        "Ký hiệu HĐ": "1C26TDC",
        "Số hóa đơn": "00000001",
        "Ngày hóa đơn": "2026-01-02",
        "Ngày hạch toán": "2026-01-02",
        "Ngày chứng từ": "2026-01-02",
        "Số chứng từ": voucher_no,
        "Diễn giải": item_name,
        "Tên người mua": "TRẦN BÁ CHƯƠNG",
        "Mã số thuế người mua": "",
        "Mặt hàng": item_name,
        "ĐVT": "Tháng",
        "Số lượng": qty,
        "Đơn giá NT": rate,
        "Đơn giá": rate,
        "Doanh số bán chưa có thuế GTGT": net,
        "Thuế suất": tax_pct,
        "Giảm 30% thuế GTGT theo NQ406": "",
        "Tiền thuế GTGT giảm trừ NT": 0,
        "Tiền thuế GTGT giảm trừ": 0,
        "Thuế GTGT NT": tax_amt,
        "Thuế GTGT": tax_amt,
        "Tài khoản thuế": "33311",
        "Chi nhánh": "CÔNG TY CỔ PHẦN VIỄN THÔNG DCN",
    }
    d.update(kw)
    return d


def _mv_row(voucher_no, item_name, qty, rate, net, tax_pct, tax_amt, **kw):
    """Build an MV (purchase) row dict with sensible defaults."""
    d = {
        "Ký hiệu mẫu HĐ": "1",
        "Ký hiệu HĐ": "C26TYY",
        "Số hóa đơn": "00000002",
        "Ngày hóa đơn": "2026-01-01",
        "Ngày hạch toán": "2026-01-01",
        "Ngày chứng từ": "2026-01-01",
        "Số chứng từ": voucher_no,
        "Tên người bán": "Cty Bất động sản T",
        "Mã số thuế người bán": "0102278861",
        "Diễn giải": item_name,
        "Mặt hàng": item_name,
        "ĐVT": "Tháng",
        "Số lượng": qty,
        "Đơn giá NT": rate,
        "Đơn giá": rate,
        "Giá trị HHDV mua vào chưa có thuế GTGT": net,
        "Thuế suất": tax_pct,
        "Thuế GTGT NT": tax_amt,
        "Thuế GTGT": tax_amt,
        "Tài khoản thuế": "1331",
        "Loại chứng từ": "Chứng từ mua dịch vụ chưa thanh toán",
        "Là chứng từ nhập khẩu HHDV": "",
        "Chi nhánh": "CÔNG TY CỔ PHẦN VIỄN THÔNG DCN",
    }
    d.update(kw)
    return d


class TestParseTaxRate(unittest.TestCase):
    def test_percent_with_space(self):
        self.assertEqual(parse_tax_rate("10 %"), 10.0)
        self.assertEqual(parse_tax_rate("8 %"), 8.0)
        self.assertEqual(parse_tax_rate("0 %"), 0.0)
        self.assertEqual(parse_tax_rate("5 %"), 5.0)

    def test_percent_no_space(self):
        self.assertEqual(parse_tax_rate("10%"), 10.0)

    def test_decimal_percent(self):
        self.assertEqual(parse_tax_rate("8.5 %"), 8.5)

    def test_kct_is_zero(self):
        self.assertEqual(parse_tax_rate("KCT"), 0.0)
        self.assertEqual(parse_tax_rate("KKT"), 0.0)

    def test_empty_is_zero(self):
        self.assertEqual(parse_tax_rate(""), 0.0)
        self.assertEqual(parse_tax_rate(None), 0.0)


class TestParseBR(unittest.TestCase):
    def test_single_line_invoice(self):
        rows = [
            _br_row("BH20260001", "Cước phí Internet FTTH", 7, 190909.14, 1336364, "10 %", 133636),
        ]
        invoices = parse_invoice_list(rows, kind="BR")
        self.assertEqual(len(invoices), 1)
        inv = invoices[0]
        self.assertEqual(inv["voucher_no"], "BH20260001")
        self.assertEqual(inv["kind"], "BR")
        self.assertEqual(inv["invoice_no"], "00000001")
        self.assertEqual(inv["party_name"], "TRẦN BÁ CHƯƠNG")
        self.assertEqual(len(inv["line_items"]), 1)
        li = inv["line_items"][0]
        self.assertEqual(li["qty"], 7.0)
        self.assertEqual(li["rate"], 190909.14)
        self.assertEqual(li["net_amount"], 1336364.0)
        self.assertEqual(li["tax_rate"], 10.0)
        self.assertEqual(li["tax_amount"], 133636.0)
        self.assertEqual(inv["total_net"], 1336364.0)
        self.assertEqual(inv["total_tax"], 133636.0)
        self.assertEqual(inv["total_gross"], 1336364.0 + 133636.0)

    def test_multi_line_invoice_groups(self):
        # Real BH20260003 from Pharma customer — 3 store-codes as 3 separate line items
        rows = [
            _br_row("BH20260003", "mã cửa hàng TCV", 7, 338571.43, 2370000, "10 %", 237000),
            _br_row("BH20260003", "mã cửa hàng SGPMC281", 7, 338571.43, 2370000, "10 %", 237000),
            _br_row("BH20260003", "mã cửa hàng SGPMC333", 7, 338571.43, 2370000, "10 %", 237000),
        ]
        invoices = parse_invoice_list(rows, kind="BR")
        self.assertEqual(len(invoices), 1)
        inv = invoices[0]
        self.assertEqual(len(inv["line_items"]), 3)
        self.assertEqual(inv["total_net"], 7110000.0)
        self.assertEqual(inv["total_tax"], 711000.0)

    def test_group_summary_rows_skipped(self):
        # First row is a group summary marker — must NOT become a line item
        rows = [
            {
                "Ký hiệu mẫu HĐ": "Nhóm HHDV: 2. Hàng hóa, dịch vụ",
                "Số chứng từ": None,
                "Số lượng": 0,
            },
            _br_row("BH20260001", "Cước phí", 1, 100000, 100000, "10 %", 10000),
            {
                "Ký hiệu mẫu HĐ": "Nhóm HHDV: 4. Hàng hóa, dịch vụ",
                "Số chứng từ": None,
                "Số lượng": "8151",
            },
            _br_row("BH20260002", "Cước phí 2", 1, 200000, 200000, "10 %", 20000),
        ]
        invoices = parse_invoice_list(rows, kind="BR")
        self.assertEqual(len(invoices), 2)
        self.assertEqual([inv["voucher_no"] for inv in invoices],
                         ["BH20260001", "BH20260002"])

    def test_zero_qty_zero_amount_line_preserved(self):
        # Real data: BH20260033 has qty=0, net=0 — keep as a line item
        rows = [
            _br_row("BH20260033", "Cước phí kênh thuê riêng", 0, 0, 0, "0 %", 0),
        ]
        invoices = parse_invoice_list(rows, kind="BR")
        self.assertEqual(len(invoices), 1)
        self.assertEqual(len(invoices[0]["line_items"]), 1)
        self.assertEqual(invoices[0]["line_items"][0]["qty"], 0.0)
        self.assertEqual(invoices[0]["total_net"], 0.0)

    def test_mixed_vat_rates_per_invoice_supported(self):
        # Some invoices mix 10% and 8% lines (NQ406 reduction)
        rows = [
            _br_row("BH20260010", "Service A", 1, 1000000, 1000000, "10 %", 100000),
            _br_row("BH20260010", "Service B", 1, 1000000, 1000000, "8 %", 80000),
        ]
        invoices = parse_invoice_list(rows, kind="BR")
        rates = [li["tax_rate"] for li in invoices[0]["line_items"]]
        self.assertEqual(rates, [10.0, 8.0])
        self.assertEqual(invoices[0]["total_tax"], 180000.0)


class TestParseMV(unittest.TestCase):
    def test_single_line_purchase(self):
        rows = [
            _mv_row("MDV20260015", "Cước chuyển phát T12/2025", 1, 763240, 763240, "8 %", 61059,
                    **{"Tên người bán": "TỔNG CÔNG TY CP BƯU CHÍNH",
                       "Mã số thuế người bán": "0104093672"}),
        ]
        invoices = parse_invoice_list(rows, kind="MV")
        inv = invoices[0]
        self.assertEqual(inv["kind"], "MV")
        self.assertEqual(inv["party_name"], "TỔNG CÔNG TY CP BƯU CHÍNH")
        self.assertEqual(inv["party_tax_id"], "0104093672")
        self.assertEqual(inv["doc_type_note"], "Chứng từ mua dịch vụ chưa thanh toán")
        self.assertEqual(inv["line_items"][0]["tax_account"], "1331")
        self.assertEqual(inv["line_items"][0]["tax_rate"], 8.0)
        self.assertEqual(inv["total_net"], 763240.0)

    def test_mv_pn_purchase_receipt_line(self):
        # Real PN20260002 — Cáp quang nhập kho
        rows = [
            _mv_row("PN20260002", "Cáp quang thuê bao ngầm 4FO", 4000, 2050, 8200000, "8 %", 656000,
                    **{"Tên người bán": "CÔNG TY TNHH CÔNG NGHỆ GIGA-NE",
                       "Mã số thuế người bán": "0314359174",
                       "ĐVT": "Mét",
                       "Loại chứng từ": "Mua hàng trong nước nhập kho chưa thanh toán"}),
        ]
        invoices = parse_invoice_list(rows, kind="MV")
        inv = invoices[0]
        self.assertEqual(inv["voucher_no"], "PN20260002")
        self.assertEqual(inv["line_items"][0]["uom"], "Mét")
        self.assertEqual(inv["line_items"][0]["qty"], 4000.0)
        self.assertEqual(inv["total_net"], 8200000.0)

    def test_kind_validation(self):
        with self.assertRaises(ValueError):
            parse_invoice_list([], kind="XX")


if __name__ == "__main__":
    unittest.main()
