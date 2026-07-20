"""EasyInvoice (SoftDreams) E-Invoice Provider Implementation.

API Documentation:
- Domain (chung từ 01/01/2026): https://api.easyinvoice.vn
- Auth: per-request MD5 signature, KHÔNG cache token.
- Header: Authentication = signature:nonce:timestamp:username:password:taxCode

Implemented endpoints (Phase A):
- API #1  api/publish/importInvoice         — push draft invoice (Phase 4)
- API #25 api/publish/getInvoicesByIkeys    — sync state (Phase 5) [verified 2026-05-08]
- API #24 api/publish/getInvoicePdf         — download PDF (Phase 5) [verified 2026-05-08]
                                            — XML download endpoint chưa xác định, contact SoftDreams
"""
import base64
import hashlib
import secrets
import time

import frappe
from frappe.utils import flt, now_datetime

from einvoice.einvoice.exceptions import EInvoiceProviderError
from einvoice.einvoice.providers.base import BaseProvider
from einvoice.einvoice.providers.easyinvoice_xml import build_invoice_xml, infer_vat_rate_int


# InvoiceStatus → human-readable text (per spec §3)
_STATUS_CODE_MAP = {
    0: "Đã đẩy, chờ ký",
    -1: "Đã đẩy, chờ ký",
    1: "Đã ký, chờ khai thuế",
    2: "Đã ký, đã khai thuế",
    3: "Đã thay thế (xem trên EasyInvoice)",
    4: "Đã điều chỉnh (xem trên EasyInvoice)",
    5: "Đã hủy trên EasyInvoice",
    6: "Đã đẩy, chờ ký",
}


class EasyInvoiceProvider(BaseProvider):
    """SoftDreams EasyInvoice — outward only, push-draft flow."""

    OUTWARD_CAPABILITY = "push-draft"  # ERP đẩy nháp, user ký USB trên app.easyinvoice.vn

    def _required_token_types(self):
        # EasyInvoice signs per-request, không cache token. Trả empty
        # để authenticate() không throw, không cache anything.
        return []

    def _do_authenticate(self) -> dict:
        # No-op: EasyInvoice không cần auth handshake.
        # Kiểm tra credentials có đầy đủ ở đây để fail-fast khi
        # provider chưa cấu hình.
        if not self.provider_doc.get("api_username"):
            raise EInvoiceProviderError(
                "Thiếu API Username (cần 'API_ERP' cho EasyInvoice).",
                provider=self.provider_name,
            )
        if not self.provider_doc.get_password("api_password"):
            raise EInvoiceProviderError(
                "Thiếu API Password.",
                provider=self.provider_name,
            )
        if not self.tax_code:
            raise EInvoiceProviderError(
                "Thiếu Tax Code trên Provider doc.",
                provider=self.provider_name,
            )
        return {"tokens": []}

    # ------------------------------------------------------------------
    # Per-request MD5 signature auth
    # ------------------------------------------------------------------
    def _build_auth_header(self, method: str) -> str:
        """Build per-request Authentication header.

        Format: signature:nonce:timestamp:username:password:taxCode
        signature = base64(MD5(METHOD.upper() + timestamp + nonce))
        """
        ts = str(int(time.time()))
        nonce = secrets.token_hex(16)
        raw = f"{method.upper()}{ts}{nonce}".encode("utf-8")
        sig = base64.b64encode(hashlib.md5(raw).digest()).decode("ascii")
        username = self.provider_doc.api_username
        password = self.provider_doc.get_password("api_password")
        return f"{sig}:{nonce}:{ts}:{username}:{password}:{self.tax_code}"

    def _api_call_easy(self, method: str, resource: str, **kwargs):
        """Wrapper inject Authentication header.

        resource = path relative to api_url (e.g. "api/publish/importInvoice").
        """
        url = f"{self.api_url.rstrip('/')}/{resource.lstrip('/')}"
        headers = kwargs.pop("headers", {}) or {}
        headers["Authentication"] = self._build_auth_header(method)
        headers.setdefault("Content-Type", "application/json; charset=utf-8")
        return self._api_call(method, url, headers=headers, **kwargs)

    # ------------------------------------------------------------------
    # Phase 4 — Map SI → payload + push draft
    # ------------------------------------------------------------------
    def map_sales_invoice_to_payload(self, si_doc, settings_doc) -> dict:
        """Map a Frappe Sales Invoice document to EasyInvoice push-draft payload.

        Returns dict with keys: pattern, serial, invoice_dict (ready for build_invoice_xml).
        Raises EInvoiceProviderError if Provider missing Pattern. Serial may be empty —
        SoftDreams xác nhận 2026-05-08 chỉ cần Pattern, Serial gửi rỗng.
        """
        pattern = (self.provider_doc.get("default_invoice_pattern") or "").strip()
        serial = (self.provider_doc.get("default_invoice_serial") or "").strip()
        if not pattern:
            raise EInvoiceProviderError(
                "Vui lòng cấu hình Pattern trên EInvoice Provider trước khi đẩy hóa đơn.",
                provider=self.provider_name,
            )

        # Customer info
        customer_name = si_doc.customer_name or si_doc.customer or ""
        tax_id = ""
        email = si_doc.get("contact_email") or ""
        phone = si_doc.get("contact_mobile") or ""

        if si_doc.customer:
            cust = frappe.db.get_value(
                "Customer", si_doc.customer,
                ["customer_name", "tax_id", "email_id", "mobile_no"],
                as_dict=True,
            )
            if cust:
                customer_name = cust.get("customer_name") or customer_name
                tax_id = cust.get("tax_id") or ""
                if not email:
                    email = cust.get("email_id") or ""
                if not phone:
                    phone = cust.get("mobile_no") or ""

        # Address
        address = ""
        if si_doc.get("customer_address"):
            addr = frappe.db.get_value(
                "Address", si_doc.customer_address, "address_line1"
            )
            address = addr or ""

        # VAT rate from taxes table (first GTGT/VAT row)
        invoice_vat_rate = _extract_si_vat_rate(si_doc, settings_doc)

        # Products
        products = []
        for idx, item in enumerate(si_doc.items, start=1):
            item_vat_rate = _extract_item_vat_rate(item, si_doc, settings_doc, invoice_vat_rate)
            vat_int, vat_other = infer_vat_rate_int(item_vat_rate)
            if vat_int is None:
                vat_int = -1  # không chịu thuế

            pre_tax = flt(item.get("net_amount") or flt(item.qty) * flt(item.rate), 2)
            vat_amount = round(pre_tax * flt(item_vat_rate or 0) / 100, 2)
            amount_with_tax = pre_tax + vat_amount

            prod = {
                "no": idx,
                "code": item.item_code or "",
                "name": item.item_name or item.item_code or "",
                "unit": item.uom or "Cái",
                "qty": flt(item.qty),
                "price": flt(item.rate),
                "total": pre_tax,
                "vat_rate": vat_int,
                "vat_amount": vat_amount,
                "amount": amount_with_tax,
                "feature": 1,
            }
            if vat_other is not None:
                prod["vat_rate_other"] = vat_other
            products.append(prod)

        # Invoice-level totals
        net_total = flt(si_doc.net_total, 2)
        grand_total = flt(si_doc.grand_total, 2)
        total_tax = flt(si_doc.total_taxes_and_charges or grand_total - net_total, 2)

        # Root invoice VAT rate (most common in products)
        inv_vat_int, inv_vat_other = infer_vat_rate_int(invoice_vat_rate)
        if inv_vat_int is None:
            inv_vat_int = -1

        # AmountInWords
        amount_in_words = frappe.utils.money_in_words(grand_total, si_doc.currency or "VND")

        payment_method = (
            (settings_doc.get("default_payment_method") if settings_doc else None)
            or "TM/CK"
        )

        invoice_dict = {
            "ikey": f"SI-{si_doc.name}",
            "customer_code": si_doc.customer or "",
            "customer_name": customer_name,
            "address": address,
            "tax_id": tax_id,
            "email": email,
            "phone": phone,
            "payment_method": payment_method,
            "arising_date": si_doc.posting_date,
            "currency": si_doc.currency or "VND",
            "exchange_rate": flt(si_doc.conversion_rate) or 1,
            "products": products,
            "total": net_total,
            "vat_rate": inv_vat_int,
            "vat_amount": total_tax,
            "amount": grand_total,
            "discount_amount": flt(si_doc.get("discount_amount") or 0),
            "amount_in_words": amount_in_words,
        }
        if inv_vat_other is not None:
            invoice_dict["vat_rate_other"] = inv_vat_other

        return {
            "pattern": pattern,
            "serial": serial,
            "invoice_dict": invoice_dict,
        }

    def push_draft_invoice(self, payload: dict) -> dict:
        """POST API #1 importInvoice — push draft (unverified) invoice.

        Returns dict: {success, ikey, status_code, status_text, error}.
        Raises EInvoiceProviderError on HTTP failure.
        """
        xml_data = build_invoice_xml(payload["invoice_dict"])
        body = {
            "XmlData": xml_data,
            "Pattern": payload["pattern"],
            "Serial": payload["serial"],
        }
        resp = self._api_call_easy("POST", "api/publish/importInvoice", json=body)
        return self._parse_import_response(resp, payload["invoice_dict"]["ikey"])

    def _parse_import_response(self, resp: dict, ikey: str) -> dict:
        """Parse API #1 response into canonical result dict."""
        status = resp.get("Status")
        if status == 2:
            # Success: extract ikey + invoice status from Data.Invoices[0]
            data = resp.get("Data") or {}
            invoices = data.get("Invoices") or []
            inv_item = invoices[0] if invoices else {}
            returned_ikey = inv_item.get("Ikey") or ikey
            inv_status = inv_item.get("InvoiceStatus", 0)
            status_text = _STATUS_CODE_MAP.get(inv_status, "Đã đẩy, chờ ký")
            return {
                "success": True,
                "ikey": returned_ikey,
                "status_code": inv_status,
                "status_text": status_text,
                "error": None,
            }
        # Non-success: extract per-ikey error message
        data = resp.get("Data") or {}
        key_msg = data.get("KeyInvoiceMsg") or {}
        per_key_error = key_msg.get(ikey) or key_msg.get(f"['{ikey}']") or ""
        if not per_key_error and isinstance(key_msg, dict):
            per_key_error = "; ".join(str(v) for v in key_msg.values() if v)
        if not per_key_error:
            per_key_error = resp.get("Message") or f"Status={status}"
        return {
            "success": False,
            "ikey": ikey,
            "status_code": status,
            "status_text": f"Lỗi: {per_key_error}",
            "error": per_key_error,
        }

    # ------------------------------------------------------------------
    # Phase 5 — Sync state + download attachment
    # ------------------------------------------------------------------
    def _map_status_code_to_text(self, code: int) -> str:
        """Map InvoiceStatus integer to human-readable Vietnamese text."""
        return _STATUS_CODE_MAP.get(code, f"Trạng thái {code}")

    def sync_invoice_state(self, ikeys: list) -> dict:
        """POST API #25 queryInvoicesByIkeys — returns per-ikey state dicts.

        Returns: {ikey: {invoice_status, status_text, no, lookup_code, link_view, error}}
        """
        body = {"Ikeys": ikeys}
        resp = self._api_call_easy("POST", "api/publish/getInvoicesByIkeys", json=body)
        result = {}
        if resp.get("Status") != 2:
            error_msg = resp.get("Message") or f"Status={resp.get('Status')}"
            for ik in ikeys:
                result[ik] = {"invoice_status": None, "status_text": f"Lỗi: {error_msg}", "error": error_msg}
            return result

        data = resp.get("Data") or {}
        invoices = data.get("Invoices") or []

        # Index returned invoices by Ikey
        by_ikey = {}
        for inv in invoices:
            ik = inv.get("Ikey") or inv.get("IKey") or ""
            if ik:
                by_ikey[ik] = inv

        for ik in ikeys:
            inv = by_ikey.get(ik)
            if not inv:
                result[ik] = {
                    "invoice_status": None,
                    "status_text": "Không tìm thấy trên EasyInvoice",
                    "error": "not_found",
                }
                continue
            code = inv.get("InvoiceStatus")
            result[ik] = {
                "invoice_status": code,
                "ikey": ik,
                "status_text": self._map_status_code_to_text(code) if code is not None else "Không rõ",
                "no": inv.get("InvoiceNo") or inv.get("No") or "",
                "lookup_code": inv.get("LookupCode") or inv.get("MaCQT") or "",
                "link_view": inv.get("LinkView") or inv.get("UrlView") or "",
                "error": None,
            }
        return result

    def download_attachment(self, ikey: str, kind: str) -> bytes:
        """POST API #24 — returns raw bytes (PDF only for now).

        kind: 'pdf' or 'xml'. PDF dùng api/publish/getInvoicePdf (verified
        2026-05-08). XML chưa xác định endpoint, sẽ raise EInvoiceProviderError
        cho đến khi SoftDreams confirm.
        Raises EInvoiceProviderError if Status!=2 or magic bytes mismatch.
        """
        if kind == "xml":
            raise EInvoiceProviderError(
                "EasyInvoice XML download endpoint chưa xác định — "
                "cần contact SoftDreams để bổ sung. PDF download vẫn hoạt động.",
                provider=self.provider_name,
            )
        if kind != "pdf":
            raise EInvoiceProviderError(
                f"kind không hỗ trợ: {kind!r}. Chỉ accept 'pdf' hoặc 'xml'.",
                provider=self.provider_name,
            )
        body = {"Ikey": ikey}
        resp = self._api_call_easy("POST", "api/publish/getInvoicePdf", json=body)

        # Response may be raw bytes dict OR {Status, Data: {Content: base64}}
        if resp.get("Status") == 2:
            data = resp.get("Data") or {}
            content_b64 = data.get("Content") or data.get("FileContent")
            if content_b64:
                import base64 as _b64
                content = _b64.b64decode(content_b64)
            else:
                # Try raw bytes from response content field
                content = resp.get("__raw_bytes__") or b""
        elif isinstance(resp, (bytes, bytearray)):
            content = bytes(resp)
        else:
            err = resp.get("Message") or f"Status={resp.get('Status')}"
            raise EInvoiceProviderError(
                f"Download {kind} thất bại: {err}", provider=self.provider_name
            )

        # Magic bytes validation
        if kind == "pdf" and not content[:4] == b"%PDF":
            raise EInvoiceProviderError(
                f"File tải về không phải PDF (magic bytes sai). ikey={ikey}",
                provider=self.provider_name,
            )
        if kind == "xml" and b"<" not in content[:200]:
            raise EInvoiceProviderError(
                f"File tải về không phải XML. ikey={ikey}",
                provider=self.provider_name,
            )
        return content

    # ------------------------------------------------------------------
    # Stubs for abstract methods — outward-only, không dùng inward
    # ------------------------------------------------------------------
    def fetch_inward_invoices(self, from_date, to_date):
        raise NotImplementedError("EasyInvoice: outward-only, không dùng inward")

    def parse_inward_invoice(self, raw_data):
        raise NotImplementedError("EasyInvoice: outward-only")

    def get_invoice_templates(self):
        return []

    def issue_outward_invoice(self, invoice_data: dict) -> dict:
        # Phase B sẽ implement (ký server). Hiện push_draft thay thế.
        raise NotImplementedError("Use push_draft_invoice (HTS giữ ký USB)")

    def cancel_invoice(self, invoice_ref: str, reason: str) -> bool:
        raise NotImplementedError("Phase B — user hủy trên web admin")


# ------------------------------------------------------------------
# Module-level helpers (pure, no Frappe ORM)
# ------------------------------------------------------------------

def _extract_si_vat_rate(si_doc, settings_doc) -> float:
    """Extract primary VAT rate from SI taxes table.

    Returns float rate (e.g. 8.0, 10.0) or default from settings.
    """
    for row in (si_doc.get("taxes") or []):
        acct = (row.get("account_head") or "").upper()
        if "GTGT" in acct or "VAT" in acct:
            return flt(row.rate or 0)
    # Fallback to settings default
    if settings_doc:
        return flt(settings_doc.get("default_vat_rate") or 0)
    return 10.0


def _extract_item_vat_rate(item, si_doc, settings_doc, invoice_vat_rate) -> float:
    """Extract VAT rate for a single item row.

    Priority: item_tax_template on the row > invoice-level > settings default.
    """
    # item_tax_template on item row if present
    if item.get("item_tax_rate"):
        try:
            import json
            rates = json.loads(item.item_tax_rate)
            if rates:
                return flt(list(rates.values())[0])
        except Exception:
            pass
    return invoice_vat_rate
