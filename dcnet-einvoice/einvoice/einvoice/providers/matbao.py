"""
Mắt Bão (Mifi) E-Invoice Provider Implementation.

API Documentation:
- Purchase (Inward):  POST /auth/token → GET /hoa-don-dau-vao/load-data-tct
- Sales (Outward):    POST /api/auth/login → POST /api/invoice/create-invoice
"""

import json

import frappe
from frappe.utils import now_datetime, flt

from einvoice.einvoice.providers.base import BaseProvider
from einvoice.einvoice.exceptions import EInvoiceProviderError


class MatbaoProvider(BaseProvider):
    """Full implementation for Mắt Bão (Mifi) E-Invoice service."""

    def _required_token_types(self):
        """Token types based on enable_inward / enable_outward toggles.

        Mắt Bão API:
        - Inward (HĐ mua vào): chỉ hỗ trợ Token → ['purchase']
        - Outward (HĐ bán ra): chỉ hỗ trợ Username-Password → ['sales']

        Provider chỉ trả về directions đã bật. Nếu cả 2 đều tắt → [] (sẽ
        được _do_authenticate() raise lỗi rõ ràng).
        """
        types = []
        if self.provider_doc.get("enable_inward"):
            types.append("purchase")
        if self.provider_doc.get("enable_outward"):
            types.append("sales")
        return types

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    def _do_authenticate(self) -> dict:
        """Authenticate with Mắt Bão APIs.

        Auth riêng từng token type theo `_required_token_types()`. Nếu 1 type
        fail (vd sales thiếu credential) thì skip type đó — không block các
        type khác. At least 1 type phải thành công.
        """
        tokens = []
        errors = []
        required = self._required_token_types()

        if not required:
            raise EInvoiceProviderError(
                "Provider chưa bật chế độ nào. Tick 'Bật chế độ hóa đơn đầu vào' "
                "và/hoặc 'Bật chế độ hóa đơn đầu ra' trên form Provider.",
                provider=self.provider_name,
            )

        if "purchase" in required:
            try:
                tokens.append({"type": "purchase", "token": self._authenticate_purchase(), "ttl": 3500})
            except EInvoiceProviderError as e:
                errors.append(f"purchase: {e}")

        if "sales" in required:
            try:
                tokens.append({"type": "sales", "token": self._authenticate_sales(), "ttl": 3500})
            except EInvoiceProviderError as e:
                errors.append(f"sales: {e}")

        if not tokens:
            raise EInvoiceProviderError(
                f"Không auth được token nào. Lỗi: {'; '.join(errors)}",
                provider=self.provider_name,
            )
        return {"tokens": tokens}

    def _authenticate_purchase(self) -> str:
        """Authenticate with the Purchase (Inward) API.

        Mắt Bão wrapper: {Success, CustomData, Data, ErrorCode}
        Spec mới: Data = JWT string ở root.
        Legacy: Data có thể là {accessToken: ...} (giữ backward-compat).
        """
        api_token = self.provider_doc.get_password("api_token")
        if not api_token:
            raise EInvoiceProviderError(
                "Thiếu API Token cho HĐ mua vào.",
                provider=self.provider_name,
            )

        url = f"{self.api_url_purchase}/auth/token"
        data = self._api_call("POST", url, json={"token": api_token})

        if isinstance(data, dict):
            success = data.get("Success", data.get("success"))
            err_code_raw = data.get("ErrorCode", data.get("errorCode"))
            err_code = str(err_code_raw).strip() if err_code_raw not in (None, "") else ""
            if success is False or (err_code and err_code != "200"):
                raise EInvoiceProviderError(
                    f"Auth thất bại: {data.get('Data', data.get('data', 'Unknown'))} (ErrorCode={err_code or 'unset'})",
                    provider=self.provider_name,
                    detail=str(data)[:500],
                )
            jwt_token = data.get("Data") or data.get("data")
            if isinstance(jwt_token, dict):
                jwt_token = jwt_token.get("accessToken") or jwt_token.get("token")
        elif isinstance(data, str):
            jwt_token = data
        else:
            jwt_token = None

        if isinstance(jwt_token, str) and jwt_token:
            return jwt_token

        raise EInvoiceProviderError(
            "Không nhận được JWT từ Mắt Bão.",
            provider=self.provider_name,
            detail=str(data)[:500],
        )

    def _authenticate_sales(self) -> str:
        """Authenticate with the Sales (Outward) API."""
        username = self.provider_doc.api_username
        password = self.provider_doc.get_password("api_password")

        if not username or not password:
            raise EInvoiceProviderError(
                "Thiếu username/password cho API Hóa đơn bán ra.",
                provider=self.provider_name,
            )

        url = f"{self.api_url}/api/auth/login"
        data = self._api_call("POST", url, json={
            "MST": self.tax_code,
            "TDNhap": username,
            "MKhau": password,
        })

        if not data.get("success"):
            raise EInvoiceProviderError(
                f"Login thất bại: {data.get('message', 'Lỗi không xác định')}",
                provider=self.provider_name,
            )

        return data["data"]["accessToken"]

    def _get_auth_headers(self, token_type):
        """Get Authorization header for the given token type."""
        token = self._get_cached_token(token_type)
        if not token:
            self.authenticate()
            token = self._get_cached_token(token_type)
        return {"Authorization": f"Bearer {token}"}

    # ------------------------------------------------------------------
    # Inward Invoices (Purchase)
    # ------------------------------------------------------------------
    def fetch_inward_invoices(self, from_date: str, to_date: str) -> list[dict]:
        """Fetch inward invoices from Mắt Bão's TCT sync endpoint.

        Mắt Bão wrapper: {Success, CustomData, Data, ErrorCode}.
        Raise nếu Success=false hoặc ErrorCode != "200" (silent fail trước đây).
        """
        if not self.provider_doc.get("enable_inward"):
            raise EInvoiceProviderError(
                "Provider chưa bật chế độ hóa đơn đầu vào. "
                "Tick 'Bật chế độ hóa đơn đầu vào' trên form Provider.",
                provider=self.provider_name,
            )
        headers = self._get_auth_headers("purchase")
        url = f"{self.api_url_purchase}/hoa-don-dau-vao/load-data-tct"

        body = {
            "comName": "",
            "comTaxCode": "",
            "no": 0,
            "fromDateYMD": from_date,
            "toDateYMD": f"{to_date} 23:59:59",
            "trangthai": -1,
            "loaihoadon": -1,
            "pattern": "",
            "serial": "",
            "typeDataPDF": 0,
        }

        data = self._api_call("GET", url, headers=headers, json=body, timeout=60)

        if isinstance(data, dict):
            success = data.get("Success", data.get("success"))
            err_code_raw = data.get("ErrorCode", data.get("errorCode"))
            err_code = str(err_code_raw).strip() if err_code_raw not in (None, "") else ""
            if success is False or (err_code and err_code != "200"):
                raise EInvoiceProviderError(
                    f"Fetch thất bại: {str(data.get('Data', data.get('data', '')))[:200]} (ErrorCode={err_code or 'unset'})",
                    provider=self.provider_name,
                )
            payload = data.get("Data", data.get("data", []))
            if isinstance(payload, list):
                return payload
        if isinstance(data, list):
            return data
        return []

    def parse_inward_invoice(self, raw_data: dict) -> dict:
        """Parse a Mắt Bão inward invoice into standardized format.

        Schema mới (load-data-tct v2): NBan* prefix, LinkDownload* links, MCCQT,
        NKy, TThai, LoaiHoaDon, MHSo, MSTTCGP, TGia, HTTToan, TTCKTMai, TGTKhac.
        Backward-compat với schema cũ: tenNBan/mstNBan/urlDownloadPDF...
        """
        def g(*keys):
            for k in keys:
                v = raw_data.get(k)
                if v not in (None, ""):
                    return v
            return None

        total_before_tax = flt(g("TgTCThue", "tgTCThue") or 0)
        tax_amount = flt(g("TgTThue", "tgTThue") or 0)
        tax_rate = flt(g("ThueSuat", "thueSuat") or 0)
        if not tax_rate and total_before_tax:
            tax_rate = round(tax_amount / total_before_tax * 100, 0)

        nlap = str(g("NLap", "nLap") or "")
        nky = str(g("NKy", "nKy") or "")
        khmshdon = g("KHMSHDon", "khmshDon") or ""

        return {
            # Core fields
            "lookup_code": g("MCCQT", "MaTraCuu", "maTraCuu") or "",
            "provider_invoice_id": str(g("InvID", "Id", "id") or ""),
            "invoice_number": str(g("SHDon", "shDon") or ""),
            "invoice_pattern": khmshdon,
            "invoice_serial": g("KHHDon", "khhDon") or "",
            "invoice_date": nlap[:10] or None,
            "signed_date": nky[:19].replace("T", " ") if nky else None,
            "invoice_type": self._map_invoice_type(khmshdon),
            # Legal/TCT
            "tct_status": self._map_tct_status(g("KQPhanTich", "kqPhanTich")),
            "lifecycle_status": str(g("TenTThai", "tenTThai") or "")[:140],
            "e_invoice_type": self._map_e_invoice_type(g("LoaiHoaDon", "loaiHoaDon")),
            "profile_code": g("MHSo", "mhSo") or "",
            "tvan_tax_code": g("MSTTCGP", "msttcgp") or "",
            # Supplier
            "supplier_name": g("NBanTen", "tenNBan", "TenNBan") or "",
            "supplier_tax_code": g("NBanMST", "mstNBan", "MSTNBan") or "",
            "supplier_address": g("NBanDChi", "dchiNBan", "DChiNBan") or "",
            # Amount
            "total_before_tax": total_before_tax,
            "tax_rate": tax_rate,
            "exchange_rate": flt(g("TGia", "tGia") or 1),
            "tax_amount": tax_amount,
            "total_amount": flt(g("TgTTTBSo", "tgTTTBSo") or 0),
            "currency": g("DVTTe", "dvtTe") or "VND",
            # Discount/payment
            "payment_method": g("HTTToan", "httToan") or "",
            "trade_discount": flt(g("TTCKTMai", "ttcktMai") or 0),
            "other_reduce": flt(g("TGTKhac", "tgtKhac") or 0),
            "total_in_words": g("TgTTTBChu", "tgTTTBChu") or "",
            # Links
            "pdf_url": g("LinkDownloadPDF", "linkDownloadPDF", "urlDownloadPDF") or "",
            "xml_url": g("LinkDownloadXML", "linkDownloadXML") or "",
            # Line items (DSHHDVu array)
            "items": self._parse_inward_items(raw_data.get("DSHHDVu") or raw_data.get("dshhdVu") or []),
            "raw_data": json.dumps(raw_data, ensure_ascii=False, default=str),
        }

    @staticmethod
    def _parse_inward_items(rows) -> list[dict]:
        """Parse DSHHDVu array (line items) into child table format.

        Mỗi row spec: TChat, STT, MHHDVu, THHDVu, DVTinh, SLuong, DGia,
        TLCKhau (% chiết khấu), STCKhau (tiền chiết khấu), ThTien (thành tiền),
        TSuat (thuế suất - text), TThue (tiền thuế nếu có).
        """
        if not isinstance(rows, list):
            return []
        items = []
        for r in rows:
            if not isinstance(r, dict):
                continue
            def rg(*keys):
                for k in keys:
                    v = r.get(k)
                    if v not in (None, ""):
                        return v
                return None
            items.append({
                "item_no": int(rg("STT", "stt") or 0),
                "item_code": str(rg("MHHDVu", "mhhdVu") or "")[:140],
                "item_name": str(rg("THHDVu", "thhdVu") or "")[:140],
                "uom": str(rg("DVTinh", "dvTinh") or "")[:140],
                "qty": flt(rg("SLuong", "sLuong") or 0),
                "rate": flt(rg("DGia", "dGia") or 0),
                "discount_pct": flt(rg("TLCKhau", "tlcKhau") or 0),
                "discount_amount": flt(rg("STCKhau", "stcKhau") or 0),
                "amount": flt(rg("ThTien", "thTien") or 0),
                "tax_rate_text": str(rg("TSuat", "tSuat") or "")[:140],
                "tax_amount": flt(rg("TThue", "tThue") or 0),
            })
        return items

    def fetch_invoice_validation(self, xml_url: str) -> dict:
        """Fetch KTra (validation checks) chi tiết cho 1 HĐ.

        Flow: download XML từ LinkDownloadXML (Mắt Bão TCT URL, hoadon.online
        SSL cert thường hết hạn → verify=False) → base64 encode → POST /detail-by-xml
        với kiem_tra_hop_le=1 → parse KTra section.

        Returns dict:
        - status: "ok" | "skipped" | "error"
        - summary: human-readable tóm tắt sai sót (vd "Không trùng tên người bán")
        - issues: list[str] các check fail
        - raw: dict KTra gốc (cho audit)
        """
        import base64
        import requests
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if not xml_url:
            return {"status": "skipped", "summary": "Thiếu LinkDownloadXML", "issues": [], "raw": {}}

        # Step 1: download XML (verify=False vì hoadon.online SSL cert hết hạn)
        headers = self._get_auth_headers("purchase")
        try:
            r = requests.get(xml_url, headers=headers, timeout=30, verify=False)
            if not r.ok or not r.content:
                return {"status": "error", "summary": f"Download XML fail: HTTP {r.status_code}", "issues": [], "raw": {}}
        except Exception as e:
            return {"status": "error", "summary": f"Download XML exception: {type(e).__name__}: {e}", "issues": [], "raw": {}}

        # Step 2: base64 + call /detail-by-xml
        xml_b64 = base64.b64encode(r.content).decode("ascii")
        url = f"{self.api_url_purchase}/hoa-don-dau-vao/detail-by-xml"
        try:
            data = self._api_call("POST", url, headers=headers,
                json={"data": xml_b64, "kiem_tra_hop_le": 1}, timeout=60)
        except EInvoiceProviderError as e:
            return {"status": "error", "summary": f"detail-by-xml fail: {e}", "issues": [], "raw": {}}

        if not isinstance(data, dict) or not data.get("Success"):
            return {"status": "error", "summary": str(data.get("Data", "Unknown"))[:200], "issues": [], "raw": {}}

        payload = data.get("Data") or {}
        ktra = payload.get("KTra") if isinstance(payload, dict) else None
        if not isinstance(ktra, dict):
            return {"status": "error", "summary": "KTra section missing", "issues": [], "raw": {}}

        # Step 3: parse KTra → identify fail checks
        issues = self._extract_validation_issues(ktra)
        summary = "; ".join(issues) if issues else "Không phát hiện sai sót cụ thể"
        return {"status": "ok", "summary": summary[:500], "issues": issues, "raw": ktra}

    def download_attachment(self, attach_url: str, kind: str) -> bytes:
        """Download PDF/XML từ Mắt Bão, retry 3 lần với backoff [1,5,15]s.

        - HTTP 401 → invalidate cached purchase token + re-auth, không tốn attempt
          (cap max-401-refresh = 2 mỗi call để tránh infinite loop).
        - HTTP 404 → raise ngay (link đã bị xóa, không retry).
        - HTTP 5xx / network / content empty → consume attempt, sleep, retry.
        - Sanity check: PDF phải start với b"%PDF", XML phải có b"<" trong 200 byte đầu.
        """
        import time
        import requests
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if kind not in ("pdf", "xml"):
            raise EInvoiceProviderError(
                f"kind phải là 'pdf' hoặc 'xml', got {kind!r}",
                provider=self.provider_name,
            )

        last_err = None
        refresh_used = 0
        for attempt, backoff in enumerate([1, 5, 15], start=1):
            headers = self._get_auth_headers("purchase")
            try:
                r = requests.get(attach_url, headers=headers, timeout=30, verify=False)
            except Exception as e:
                last_err = f"{type(e).__name__}: {e}"
                time.sleep(backoff)
                continue

            if r.status_code == 401:
                if refresh_used >= 2:
                    last_err = "HTTP 401 sau khi refresh token"
                    time.sleep(backoff)
                    continue
                self._invalidate_cached_token("purchase")
                self.authenticate()
                refresh_used += 1
                # Không tính attempt — retry ngay với token mới (không sleep dài)
                continue

            if r.status_code == 404:
                raise EInvoiceProviderError(
                    f"{kind.upper()} không tồn tại (404)",
                    provider=self.provider_name,
                )

            if r.status_code >= 500:
                last_err = f"HTTP {r.status_code}"
                time.sleep(backoff)
                continue

            if not r.ok or not r.content:
                last_err = f"HTTP {r.status_code} content empty"
                time.sleep(backoff)
                continue

            if kind == "pdf" and not r.content.startswith(b"%PDF"):
                last_err = "Response không phải PDF (header check)"
                time.sleep(backoff)
                continue
            if kind == "xml" and b"<" not in r.content[:200]:
                last_err = "Response không phải XML"
                time.sleep(backoff)
                continue

            return r.content

        raise EInvoiceProviderError(
            f"Tải {kind.upper()} thất bại sau 3 lần: {last_err}",
            provider=self.provider_name,
        )

    @staticmethod
    def _extract_validation_issues(ktra: dict) -> list[str]:
        """Identify check fails từ KTra section.

        Logic: explicit OK whitelist trước (skip), rồi check FAIL patterns.
        "Không có sự chênh lệch" = OK (whitelist) — không nhầm với "có sự chênh lệch".
        """
        OK_EXACT = {
            "không có sự chênh lệch",
            "trùng tên người bán",
            "trùng mã số thuế người bán",
            "trùng địa chỉ người bán",
            "trùng tên người mua",
            "trùng mã số thuế người mua",
            "trùng địa chỉ người mua",
            "trùng mã số thuế của chữ ký số",
            "chữ ký số còn hiệu lực tại thời điểm ký",
            "cơ quan thuế đã cấp mã",
            "hóa đơn hợp lệ",
        }
        FAIL_PATTERNS = [
            ("không trùng", "❌"),
            ("hết hiệu lực", "❌"),
            ("không hoạt động", "❌"),
            ("không hợp lệ", "❌"),
            ("chưa cấp mã", "⚠️"),
        ]
        # Special: "có sự chênh lệch" only fails khi không có "không" trước
        LABEL_MAP = {
            "NBanTen": "Tên NCC",
            "NBanMST": "MST NCC",
            "NBanDChi": "Địa chỉ NCC",
            "NBanTrangThaiHDMST": "Trạng thái HĐ MST NCC",
            "NMuaTen": "Tên người mua",
            "NMuaMST": "MST người mua",
            "NMuaDChi": "Địa chỉ người mua",
            "NMuaTrangThaiHDMST": "Trạng thái HĐ MST người mua",
            "TgTCThue": "Tổng tiền chưa thuế",
            "TgTThue": "Tổng tiền thuế",
            "TgTPhi": "Tổng phí",
            "TgTTTBSo": "Tổng thanh toán",
            "TTCKTMai": "Chiết khấu thương mại",
            "ChuKyMST": "Chữ ký số (MST)",
            "ChuKyHieuLuc": "Chữ ký số (hiệu lực)",
            "ChuKyTGianHieuLuc": "Chữ ký số (thời gian)",
            "ThoiDiemKy": "Thời điểm ký",
            "MCCQT": "Mã CQT",
            "TrangThai": "Trạng thái HĐ",
            "NguyenVen": "Tính nguyên vẹn",
        }
        issues = []
        for key, value in ktra.items():
            if value is None or not isinstance(value, (str, bool, int)):
                continue
            v_str = str(value).strip()
            v_low = v_str.lower()

            # Whitelist OK first — startswith để không match "không trùng" như là "trùng"
            if any(v_low.startswith(ok) for ok in OK_EXACT):
                continue
            # Boolean True or "đã/được/còn ..." prefix → OK
            if value is True or v_low.startswith(("đã ", "được ", "còn ", "nnt đang hoạt động")):
                continue

            label = LABEL_MAP.get(key, key)
            matched = False
            for pattern, icon in FAIL_PATTERNS:
                if pattern in v_low:
                    issues.append(f"{icon} {label}: {v_str[:200]}")
                    matched = True
                    break
            # Special case "có sự chênh lệch" without "không có"
            if not matched and "chênh lệch" in v_low and "không có" not in v_low:
                issues.append(f"⚠️ {label}: {v_str[:200]}")
        return issues

    @staticmethod
    def _map_invoice_type(khmshdon: str) -> str:
        """Map Mắt Bão invoice pattern to standardized type."""
        mapping = {"1": "GTGT", "2": "Bán hàng"}
        return mapping.get(str(khmshdon), "Khác")

    @staticmethod
    def _map_tct_status(kq_phan_tich) -> str:
        """Map KQPhanTich (kết quả phân tích Mắt Bão) → DocType Select option.

        Live data thực tế trả 2 giá trị:
        - "Hóa đơn hợp lệ" (~96% records)
        - "Hóa đơn có sai sót" (~4% — đánh dấu đỏ trên admin Mắt Bão)
        """
        if not kq_phan_tich:
            return "Unknown"
        s = str(kq_phan_tich).strip()
        if "hợp lệ" in s.lower():
            return "Hóa đơn hợp lệ"
        if "sai sót" in s.lower():
            return "Hóa đơn có sai sót"
        return "Unknown"

    @staticmethod
    def _map_e_invoice_type(loai_hoa_don) -> str:
        """Map LoaiHoaDon numeric code → DocType Select option.

        Spec: 1=có mã CQT, 2=không mã, 3=máy tính tiền.
        """
        if loai_hoa_don is None or loai_hoa_don == "":
            return ""
        mapping = {1: "Coded", 2: "Uncoded", 3: "Cashier"}
        try:
            return mapping.get(int(loai_hoa_don), "Other")
        except (TypeError, ValueError):
            return "Other"

    # ------------------------------------------------------------------
    # Outward Invoices (Sales)
    # ------------------------------------------------------------------
    def _require_outward(self):
        if not self.provider_doc.get("enable_outward"):
            raise EInvoiceProviderError(
                "Provider chưa bật chế độ hóa đơn đầu ra. "
                "Tick 'Bật chế độ hóa đơn đầu ra' trên form Provider.",
                provider=self.provider_name,
            )

    def get_invoice_templates(self) -> list[dict]:
        """Fetch available invoice templates from Mắt Bão."""
        from datetime import datetime

        self._require_outward()
        headers = self._get_auth_headers("sales")
        url = f"{self.api_url}/api/invoice/templates"
        params = {"year": str(datetime.now().year)}

        data = self._api_call("GET", url, headers=headers, params=params)

        if data.get("success"):
            return data.get("data", [])
        return []

    def issue_outward_invoice(self, invoice_data: dict) -> dict:
        """Issue an outward invoice via Mắt Bão API."""
        self._require_outward()
        headers = self._get_auth_headers("sales")
        url = f"{self.api_url}/api/invoice/create-invoice"

        data = self._api_call("POST", url, headers=headers, json=[invoice_data], timeout=60)

        if not data.get("success"):
            return {
                "success": False,
                "invoice_number": None,
                "lookup_code": None,
                "pdf_url": None,
                "xml_url": None,
                "raw_response": data,
                "error": data.get("message", "Lỗi không xác định"),
            }

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
        self._require_outward()
        headers = self._get_auth_headers("sales")
        url = f"{self.api_url}/api/invoice/cancel-invoice"

        data = self._api_call("POST", url, headers=headers, json={
            "MaSoHDon": invoice_ref,
            "LDo": reason,
        })

        return data.get("success", False)

    # ------------------------------------------------------------------
    # Data Mapping
    # ------------------------------------------------------------------
    def map_sales_invoice_to_payload(self, si_doc, settings_doc) -> dict:
        """Convert an ERPNext Sales Invoice into Mắt Bão create-invoice payload."""
        provider = self.provider_doc
        issue_mode = 0 if settings_doc.default_issue_mode == "Draft" else 1

        items = []
        for idx, item in enumerate(si_doc.items, start=1):
            tax_rate = self._get_item_tax_rate(si_doc, item)
            tax_amount = flt(item.amount * tax_rate / 100, 2)

            items.append({
                "TChat": 1,
                "STT": idx,
                "MHHDVu": item.item_code or "",
                "THHDVu": item.item_name or "",
                "DVTinh": item.uom or "",
                "SLuong": flt(item.qty),
                "DGia": flt(item.rate),
                "ThTienChuaCK": flt(item.amount),
                "TLCKhau": flt(item.discount_percentage) if hasattr(item, "discount_percentage") else 0,
                "STCKhau": flt(item.discount_amount) if hasattr(item, "discount_amount") else 0,
                "ThTien": flt(item.amount),
                "TSuat": tax_rate,
                "TThue": tax_amount,
                "TgTien": flt(item.amount) + tax_amount,
            })

        lookup = f"{si_doc.name}_{now_datetime().strftime('%Y%m%d%H%M%S')}"

        customer_tax_id = si_doc.tax_id or ""
        if not customer_tax_id and si_doc.customer:
            customer_tax_id = frappe.db.get_value("Customer", si_doc.customer, "tax_id") or ""

        return {
            "KHMSHDon": provider.default_invoice_pattern or "1",
            "KHHDon": provider.default_invoice_serial or "",
            "MaTraCuu": lookup,
            "MTChieu": lookup,
            "NLap": f"{si_doc.posting_date}T00:00:00",
            "LoaiHDon": issue_mode,
            "TCHDon": 0,
            "LoaiTraHang": 0,
            "DVTTe": 704,
            "TGia": 1000.00,
            "HTTToan": settings_doc.default_payment_method or "Chuyển khoản",
            "GChu": si_doc.remarks or "",
            "NMua_Ten": si_doc.customer_name or "",
            "NMua_MST": customer_tax_id,
            "NMua_DChi": si_doc.customer_address or frappe.db.get_value(
                "Address", si_doc.customer_address, "address_line1"
            ) or "",
            "NMua_MKHang": si_doc.customer or "",
            "NMua_SDThoai": getattr(si_doc, "contact_mobile", ""),
            "NMua_DCTDTu": getattr(si_doc, "contact_email", ""),
            "NMua_HVTNMHang": "",
            "NMua_STKNHang": "",
            "NMua_TNHang": "",
            "DSHHDVu": items,
            "TTCKTMai": flt(si_doc.discount_amount) if hasattr(si_doc, "discount_amount") else 0,
            "TGTKhac": 0,
            "TgThTien": flt(si_doc.total),
            "TgTThue": flt(si_doc.total_taxes_and_charges),
            "TgTTTBSo": flt(si_doc.grand_total),
            "TgTTTBChu": si_doc.in_words or "",
        }

    @staticmethod
    def _get_item_tax_rate(si_doc, item):
        """Extract the VAT tax rate for an item from the Sales Invoice tax table."""
        for tax in si_doc.taxes:
            if "VAT" in (tax.description or "").upper() or "GTGT" in (tax.description or "").upper():
                return flt(tax.rate)
        if hasattr(item, "item_tax_rate") and item.item_tax_rate:
            try:
                rates = json.loads(item.item_tax_rate)
                for account, rate in rates.items():
                    return flt(rate)
            except Exception:
                pass
        return 0
