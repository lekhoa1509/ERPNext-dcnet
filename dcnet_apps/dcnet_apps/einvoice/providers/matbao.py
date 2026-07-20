"""
Mắt Bão (Mifi) E-Invoice Provider Implementation.

API Documentation:
- Purchase (Inward):  POST /auth/token → GET /hoa-don-dau-vao/load-data
- Sales (Outward):    POST /api/auth/login → POST /api/invoice/create-invoice
"""

import json
import requests
import frappe
from frappe.utils import now_datetime, getdate, flt

from dcnet_apps.einvoice.providers.base import BaseProvider


class MatbaoProvider(BaseProvider):
    """Full implementation for Mắt Bão (Mifi) E-Invoice service."""

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    def authenticate(self) -> str:
        """Authenticate with Mắt Bão API.

        Mắt Bão has TWO separate auth flows:
        - Purchase API: POST /auth/token with a static token → JWT
        - Sales API: POST /api/auth/login with MST + username + password → JWT
        """
        # We authenticate with the Sales API by default (more common use case)
        self._sales_token = self._authenticate_sales()
        self._purchase_token = self._authenticate_purchase()
        self._access_token = self._sales_token
        return self._access_token

    def _authenticate_purchase(self) -> str:
        """Authenticate with the Purchase (Inward) API."""
        token = self.provider_doc.get_password("api_token")
        if not token:
            frappe.throw("Matbao: Thiếu token xác thực cho API Hóa đơn mua vào.")

        url = f"{self.api_url_purchase}/auth/token"
        resp = requests.post(
            url,
            json={"token": token},
            timeout=30,
            verify=True,
        )
        resp.raise_for_status()
        data = resp.json()

        # The response contains a JWT in the response body directly
        # Based on Postman: the token is in the response
        jwt_token = data.get("data", {}).get("accessToken") or data.get("token", "")
        if not jwt_token and isinstance(data, str):
            jwt_token = data

        return jwt_token

    def _authenticate_sales(self) -> str:
        """Authenticate with the Sales (Outward) API."""
        username = self.provider_doc.api_username
        password = self.provider_doc.get_password("api_password")

        if not username or not password:
            frappe.throw("Matbao: Thiếu username/password cho API Hóa đơn bán ra.")

        url = f"{self.api_url}/api/auth/login"
        resp = requests.post(
            url,
            json={
                "MST": self.tax_code,
                "TDNhap": username,
                "MKhau": password,
            },
            timeout=30,
            verify=True,
        )
        resp.raise_for_status()
        data = resp.json()

        if not data.get("success"):
            frappe.throw(f"Matbao login failed: {data.get('message', 'Unknown error')}")

        return data["data"]["accessToken"]

    # ------------------------------------------------------------------
    # Inward Invoices (Purchase)
    # ------------------------------------------------------------------
    def fetch_inward_invoices(self, from_date: str, to_date: str) -> list[dict]:
        """Fetch inward invoices from Mắt Bão's Tổng Cục Thuế sync endpoint."""
        if not self._purchase_token:
            self._purchase_token = self._authenticate_purchase()

        url = f"{self.api_url_purchase}/hoa-don-dau-vao/load-data-tct"
        headers = {"Authorization": f"Bearer {self._purchase_token}"}

        body = {
            "comName": "",
            "comTaxCode": "",
            "no": "",
            "fromDateYMD": from_date,
            "toDateYMD": f"{to_date} 23:59:59",
            "trangthai": -1,
            "loaihoadon": -1,
            "pattern": "",
            "serial": "",
        }

        resp = requests.get(url, headers=headers, json=body, timeout=60, verify=True)
        resp.raise_for_status()
        data = resp.json()

        # API returns a list of invoice objects
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "data" in data:
            return data["data"] if isinstance(data["data"], list) else []
        return []

    def parse_inward_invoice(self, raw_data: dict) -> dict:
        """Parse a Mắt Bão inward invoice into standardized format."""
        # Field mapping based on Postman collection analysis
        # The exact field names depend on the API response structure
        return {
            "lookup_code": raw_data.get("maTraCuu", raw_data.get("MaTraCuu", "")),
            "provider_invoice_id": str(raw_data.get("id", raw_data.get("Id", ""))),
            "invoice_number": str(raw_data.get("shDon", raw_data.get("SHDon", ""))),
            "invoice_pattern": raw_data.get("khmshDon", raw_data.get("KHMSHDon", "")),
            "invoice_serial": raw_data.get("khhDon", raw_data.get("KHHDon", "")),
            "invoice_date": raw_data.get("nLap", raw_data.get("NLap", ""))[:10] if raw_data.get("nLap") or raw_data.get("NLap") else None,
            "invoice_type": self._map_invoice_type(raw_data.get("khmshDon", raw_data.get("KHMSHDon", ""))),
            "supplier_name": raw_data.get("tenNBan", raw_data.get("TenNBan", "")),
            "supplier_tax_code": raw_data.get("mstNBan", raw_data.get("MSTNBan", "")),
            "supplier_address": raw_data.get("dchiNBan", raw_data.get("DChiNBan", "")),
            "total_before_tax": flt(raw_data.get("tgTCThue", raw_data.get("TgTCThue", 0))),
            "tax_amount": flt(raw_data.get("tgTThue", raw_data.get("TgTThue", 0))),
            "total_amount": flt(raw_data.get("tgTTTBSo", raw_data.get("TgTTTBSo", 0))),
            "currency": "VND",
            "pdf_url": raw_data.get("urlDownloadPDF", ""),
            "raw_data": json.dumps(raw_data, ensure_ascii=False, default=str),
        }

    @staticmethod
    def _map_invoice_type(khmshdon: str) -> str:
        """Map Mắt Bão invoice pattern to standardized type."""
        mapping = {"1": "GTGT", "2": "Bán hàng"}
        return mapping.get(str(khmshdon), "Khác")

    # ------------------------------------------------------------------
    # Outward Invoices (Sales)
    # ------------------------------------------------------------------
    def get_invoice_templates(self) -> list[dict]:
        """Fetch available invoice templates from Mắt Bão."""
        if not self._sales_token:
            self._sales_token = self._authenticate_sales()

        from datetime import datetime
        year = datetime.now().year

        url = f"{self.api_url}/api/invoice/templates"
        headers = {"Authorization": f"Bearer {self._sales_token}"}
        params = {"year": str(year)}

        resp = requests.get(url, headers=headers, params=params, timeout=30, verify=True)
        resp.raise_for_status()
        data = resp.json()

        if data.get("success"):
            return data.get("data", [])
        return []

    def issue_outward_invoice(self, invoice_data: dict) -> dict:
        """Issue an outward invoice via Mắt Bão API."""
        if not self._sales_token:
            self._sales_token = self._authenticate_sales()

        url = f"{self.api_url}/api/invoice/create-invoice"
        headers = {"Authorization": f"Bearer {self._sales_token}"}

        # API expects a list of invoice objects
        payload = [invoice_data]

        resp = requests.post(url, headers=headers, json=payload, timeout=60, verify=True)
        resp.raise_for_status()
        data = resp.json()

        if not data.get("success"):
            return {
                "success": False,
                "invoice_number": None,
                "lookup_code": None,
                "pdf_url": None,
                "xml_url": None,
                "raw_response": data,
                "error": data.get("message", "Unknown error"),
            }

        # Parse the first result (we send one invoice at a time)
        result = data["data"][0] if data.get("data") else {}
        result_data = result.get("data", {})

        return {
            "success": result.get("success", False),
            "invoice_number": str(result_data.get("shDon", "")),
            "lookup_code": result_data.get("maTraCuu", ""),
            "maso_hdon": result_data.get("maSoHDon", ""),
            "pdf_url": result_data.get("urlDownloadPDF", ""),
            "xml_url": result_data.get("urlDownloadXML", ""),
            "raw_response": data,
        }

    def cancel_invoice(self, invoice_ref: str, reason: str) -> bool:
        """Cancel an invoice on Mắt Bão."""
        if not self._sales_token:
            self._sales_token = self._authenticate_sales()

        url = f"{self.api_url}/api/invoice/cancel-invoice"
        headers = {"Authorization": f"Bearer {self._sales_token}"}

        payload = {
            "MaSoHDon": invoice_ref,
            "LDo": reason,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=30, verify=True)
        resp.raise_for_status()
        data = resp.json()
        return data.get("success", False)

    # ------------------------------------------------------------------
    # Data Mapping
    # ------------------------------------------------------------------
    def map_sales_invoice_to_payload(self, si_doc, settings_doc) -> dict:
        """Convert an ERPNext Sales Invoice into Mắt Bão create-invoice payload."""
        from frappe.utils import formatdate

        provider = self.provider_doc
        issue_mode = 0 if settings_doc.default_issue_mode == "Draft" else 1

        # Build line items
        items = []
        for idx, item in enumerate(si_doc.items, start=1):
            tax_rate = self._get_item_tax_rate(si_doc, item)
            tax_amount = flt(item.amount * tax_rate / 100, 2)

            items.append({
                "TChat": 1,  # 1 = Hàng hóa/dịch vụ
                "STT": idx,
                "MHHDVu": item.item_code or "",
                "THHDVu": item.item_name or "",
                "DVTinh": item.uom or "",
                "SLuong": flt(item.qty),
                "DGia": flt(item.rate),
                "ThTienChuaCK": flt(item.amount),
                "TLCKhau": flt(item.discount_percentage) if hasattr(item, 'discount_percentage') else 0,
                "STCKhau": flt(item.discount_amount) if hasattr(item, 'discount_amount') else 0,
                "ThTien": flt(item.amount),
                "TSuat": tax_rate,
                "TThue": tax_amount,
                "TgTien": flt(item.amount) + tax_amount,
            })

        # Build lookup code from SI name + timestamp
        import hashlib
        lookup = f"{si_doc.name}_{now_datetime().strftime('%Y%m%d%H%M%S')}"

        # Customer info
        customer_tax_id = ""
        if si_doc.tax_id:
            customer_tax_id = si_doc.tax_id
        elif hasattr(si_doc, 'customer'):
            customer_tax_id = frappe.db.get_value("Customer", si_doc.customer, "tax_id") or ""

        payload = {
            "KHMSHDon": provider.default_invoice_pattern or "1",
            "KHHDon": provider.default_invoice_serial or "",
            "MaTraCuu": lookup,
            "MTChieu": lookup,
            "NLap": f"{si_doc.posting_date}T00:00:00",
            "LoaiHDon": issue_mode,
            "TCHDon": 0,  # 0 = Hóa đơn mới
            "LoaiTraHang": 0,
            "DVTTe": 704,  # VND
            "TGia": 1000.00,
            "HTTToan": settings_doc.default_payment_method or "Chuyển khoản",
            "GChu": si_doc.remarks or "",
            "NMua_Ten": si_doc.customer_name or "",
            "NMua_MST": customer_tax_id,
            "NMua_DChi": si_doc.customer_address or frappe.db.get_value(
                "Address",
                si_doc.customer_address,
                "address_line1"
            ) or "",
            "NMua_MKHang": si_doc.customer or "",
            "NMua_SDThoai": getattr(si_doc, "contact_mobile", ""),
            "NMua_DCTDTu": getattr(si_doc, "contact_email", ""),
            "NMua_HVTNMHang": "",
            "NMua_STKNHang": "",
            "NMua_TNHang": "",
            "DSHHDVu": items,
            "TTCKTMai": flt(si_doc.discount_amount) if hasattr(si_doc, 'discount_amount') else 0,
            "TGTKhac": 0,
            "TgThTien": flt(si_doc.total),
            "TgTThue": flt(si_doc.total_taxes_and_charges),
            "TgTTTBSo": flt(si_doc.grand_total),
            "TgTTTBChu": si_doc.in_words or "",
        }

        return payload

    @staticmethod
    def _get_item_tax_rate(si_doc, item):
        """Extract the VAT tax rate for an item from the Sales Invoice tax table."""
        for tax in si_doc.taxes:
            if "VAT" in (tax.description or "").upper() or "GTGT" in (tax.description or "").upper():
                return flt(tax.rate)
        # Fallback: check item_tax_template
        if hasattr(item, 'item_tax_rate') and item.item_tax_rate:
            try:
                rates = json.loads(item.item_tax_rate)
                for account, rate in rates.items():
                    return flt(rate)
            except Exception:
                pass
        return 0
