"""Unit tests for EasyInvoice XML builder pure functions.

No Frappe ORM, no HTTP — runnable standalone.
Run via bench console:
    import unittest
    from einvoice.einvoice.tests.test_easyinvoice_xml import TestEasyInvoiceXML
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(unittest.TestLoader().loadTestsFromTestCase(TestEasyInvoiceXML))
"""
import unittest
from datetime import date, datetime
from xml.etree import ElementTree as ET

from einvoice.einvoice.providers.easyinvoice_xml import (
    build_invoice_xml,
    build_product_xml,
    format_amount,
    format_date_dmy,
    infer_vat_rate_int,
    xml_escape,
)


_FULL_INV = {
    "ikey": "SI-TEST-1",
    "customer_code": "C-001",
    "customer_name": "Cty A & B",
    "address": "Hà Nội",
    "tax_id": "0123456789",
    "email": "test@example.com",
    "phone": "0901234567",
    "payment_method": "TM/CK",
    "arising_date": "07/05/2026",
    "currency": "VND",
    "exchange_rate": 1,
    "products": [
        {"no": 1, "code": "I1", "name": "Sản phẩm 1", "unit": "Cái",
         "qty": 2, "price": 100000, "total": 200000,
         "vat_rate": 10, "vat_amount": 20000, "amount": 220000},
        {"no": 2, "code": "I2", "name": "Sản phẩm 2", "unit": "Hộp",
         "qty": 1, "price": 50000, "total": 50000,
         "vat_rate": 8, "vat_amount": 4000, "amount": 54000},
    ],
    "total": 250000,
    "vat_rate": 10,
    "vat_amount": 24000,
    "amount": 274000,
    "amount_in_words": "Hai trăm bảy mươi bốn nghìn đồng",
}


class TestEasyInvoiceXML(unittest.TestCase):

    # 1
    def test_xml_escape_lt_gt(self):
        self.assertEqual(xml_escape("<a>"), "&lt;a&gt;")

    # 2
    def test_xml_escape_amp(self):
        self.assertEqual(xml_escape("Cty A & B"), "Cty A &amp; B")

    # 3
    def test_xml_escape_quote(self):
        # Both " and ' must be escaped
        self.assertIn("&quot;", xml_escape('say "hi"'))
        self.assertIn("&apos;", xml_escape("it's"))

    # 4
    def test_format_date_dmy_date(self):
        self.assertEqual(format_date_dmy(date(2026, 5, 7)), "07/05/2026")

    # 5
    def test_format_date_dmy_datetime(self):
        self.assertEqual(format_date_dmy(datetime(2026, 5, 7, 12, 30)), "07/05/2026")

    # 6
    def test_format_amount_int(self):
        self.assertEqual(format_amount(100000), "100000")
        self.assertEqual(format_amount(100000.0), "100000")  # strip .0

    # 7
    def test_format_amount_decimal(self):
        self.assertEqual(format_amount(100000.5), "100000.5")
        self.assertEqual(format_amount(12.50), "12.5")

    # 8
    def test_infer_vat_rate_standard(self):
        for r in (0, 5, 8, 10):
            self.assertEqual(infer_vat_rate_int(r), (r, None))
        # Float-form of standard rates also accepted
        self.assertEqual(infer_vat_rate_int(10.0), (10, None))

    # 9
    def test_infer_vat_rate_other(self):
        self.assertEqual(infer_vat_rate_int(15.5), (-3, "15.5"))
        self.assertEqual(infer_vat_rate_int(7.0), (-3, "7"))  # 7 not in {0,5,8,10}

    # 10
    def test_build_invoice_well_formed(self):
        xml_str = build_invoice_xml(_FULL_INV)
        # Strip XML declaration before parsing for ET.fromstring
        if xml_str.startswith("<?xml"):
            xml_str_no_decl = xml_str.split("?>", 1)[1]
        else:
            xml_str_no_decl = xml_str
        root = ET.fromstring(xml_str_no_decl)
        self.assertEqual(root.tag, "Invoices")
        invs = list(root)
        self.assertEqual(len(invs), 1)
        invoice = invs[0].find("Invoice")
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.find("Ikey").text, "SI-TEST-1")
        self.assertEqual(invoice.find("ArisingDate").text, "07/05/2026")
        products = invoice.find("Products").findall("Product")
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].find("Code").text, "I1")
        self.assertEqual(products[1].find("VATRate").text, "8")

    def test_build_product_complete(self):
        prod = _FULL_INV["products"][0]
        xml_str = build_product_xml(prod)
        root = ET.fromstring(xml_str)
        self.assertEqual(root.tag, "Product")
        self.assertEqual(root.find("Code").text, "I1")
        self.assertEqual(root.find("ProdQuantity").text, "2")
        self.assertEqual(root.find("VATRate").text, "10")

    def test_build_invoice_amp_in_customer_name(self):
        """Customer name with & must produce well-formed XML (no parse error)."""
        xml_str = build_invoice_xml(_FULL_INV)
        if xml_str.startswith("<?xml"):
            xml_str = xml_str.split("?>", 1)[1]
        root = ET.fromstring(xml_str)
        cus = root.find("Inv/Invoice/CusName")
        self.assertEqual(cus.text, "Cty A & B")  # ET decodes &amp; back


if __name__ == "__main__":
    unittest.main()
