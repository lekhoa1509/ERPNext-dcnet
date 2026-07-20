"""Trích xuất dữ liệu hóa đơn (PDF / ảnh) bằng LLM tương thích OpenAI Chat Completions.

Quy ước:
- Đọc cấu hình từ Single DocType `Branch Cash Invoice AI Settings`
  (base_url, model, api_key, timeout, enabled).
- Gửi file dưới dạng `image_url` data-URL base64 — endpoint phía bạn (mới yêu cầu)
  cần hỗ trợ multimodal vision content theo chuẩn OpenAI.
- Yêu cầu LLM trả về JSON ĐÚNG schema invoice_loader để map thẳng vào form.
"""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import re
from typing import Any

import frappe
from frappe import _


SETTINGS_DOCTYPE = "Branch Cash Invoice AI Settings"


SUPPORTED_BINARY_EXTS = {
	".pdf",
	".png",
	".jpg",
	".jpeg",
	".webp",
	".gif",
	".bmp",
	".tif",
	".tiff",
	".heic",
	".heif",
}


SYSTEM_PROMPT = (
	"Bạn là trợ lý trích xuất dữ liệu hóa đơn điện tử của Việt Nam. "
	"Hãy đọc file hóa đơn (PDF hoặc ảnh) và trả về DUY NHẤT một JSON đúng schema "
	"do người dùng yêu cầu. Tuyệt đối không trả lời thêm bất kỳ ký tự nào ngoài JSON."
)


USER_INSTRUCTION = """Trích xuất các trường hóa đơn theo schema JSON dưới đây.

Quy ước giá trị:
- Tất cả các trường tiền là SỐ (không có dấu chấm/phẩy phân cách, không kèm đơn vị).
- `invoice_date` định dạng YYYY-MM-DD nếu xác định được, nếu không thì để chuỗi rỗng.
- Nếu không có thông tin, để chuỗi rỗng "" cho text hoặc 0 cho số.
- `invoice_items` là mảng các dòng hàng hóa.

Schema JSON cần trả về:
{
  "invoice_form_no": str,        // Mẫu số (Form)
  "invoice_serial": str,         // Ký hiệu (Serial)
  "invoice_number": str,         // Số (Invoice No)
  "invoice_id": str,             // ID hóa đơn (nếu có)
  "invoice_date": str,           // YYYY-MM-DD
  "invoice_currency": str,       // VND, USD…
  "exchange_rate": float,
  "seller_name": str,
  "seller_tax_code": str,
  "seller_address": str,
  "seller_phone": str,
  "buyer_contact_name": str,     // Họ tên người mua hàng (cá nhân)
  "buyer_company_name": str,     // Tên đơn vị
  "buyer_tax_code": str,
  "buyer_address": str,
  "buyer_warehouse": str,
  "payment_method": str,         // CK / TM / Khác
  "payment_due_date": str,
  "buyer_bank_account": str,
  "buyer_bank_name": str,
  "reference_number": str,
  "total_before_tax": float,     // Cộng tiền hàng
  "tax_rate": str,               // Thuế suất GTGT (vd "10", "8", "KCT")
  "tax_amount": float,
  "total_amount": float,         // Tổng cộng tiền thanh toán
  "total_in_words": str,
  "invoice_items": [
    {
      "item_name": str,
      "item_code": str,
      "uom": str,
      "qty": float,
      "rate": float,
      "amount": float
    }
  ]
}

Chỉ trả về JSON, không markdown fence, không giải thích."""


def get_settings() -> dict[str, Any]:
	doc = frappe.get_cached_doc(SETTINGS_DOCTYPE)
	api_key = doc.get_password("api_key", raise_exception=False) if doc.api_key else ""
	return {
		"enabled": bool(doc.enabled),
		"base_url": (doc.base_url or "").rstrip("/"),
		"model": doc.model or "",
		"api_key": api_key or "",
		"timeout": int(doc.timeout_seconds or 120),
	}


def is_supported_binary(file_path: str) -> bool:
	ext = os.path.splitext(file_path)[1].lower()
	return ext in SUPPORTED_BINARY_EXTS


def parse_invoice_with_ai(file_path: str) -> dict[str, Any]:
	"""Đọc file PDF/ảnh và gọi AI để extract.

	PDF được render thành ảnh PNG (mỗi trang 1 ảnh) trước khi gửi vì
	endpoint chỉ hỗ trợ image content. Ảnh thường gửi nguyên file.
	"""
	settings = get_settings()
	if not settings["enabled"]:
		frappe.throw(_("Tính năng AI đọc hóa đơn đang tắt. Bật trong Branch Cash Invoice AI Settings."))
	if not settings["base_url"] or not settings["model"] or not settings["api_key"]:
		frappe.throw(
			_("Vui lòng cấu hình Base URL / Model / API Key trong Branch Cash Invoice AI Settings.")
		)

	image_data_urls = _file_to_image_data_urls(file_path)
	if not image_data_urls:
		frappe.throw(_("Không trích xuất được ảnh từ file hóa đơn."))

	content_blocks: list[dict[str, Any]] = [{"type": "text", "text": USER_INSTRUCTION}]
	for url in image_data_urls:
		content_blocks.append({"type": "image_url", "image_url": {"url": url}})

	payload = {
		"model": settings["model"],
		"stream": False,
		"messages": [
			{"role": "system", "content": SYSTEM_PROMPT},
			{"role": "user", "content": content_blocks},
		],
		"temperature": 0,
	}

	response_json = _call_llm(settings, payload)
	content = _extract_message_content(response_json)
	data = _parse_json_payload(content)
	return _normalize_ai_result(data)


def _file_to_image_data_urls(file_path: str) -> list[str]:
	with open(file_path, "rb") as fh:
		raw = fh.read()
	if not raw:
		frappe.throw(_("File hóa đơn rỗng."))

	ext = os.path.splitext(file_path)[1].lower()
	if ext == ".pdf":
		return _render_pdf_pages(raw)

	mime = mimetypes.guess_type(file_path)[0] or "image/png"
	b64 = base64.b64encode(raw).decode("ascii")
	return [f"data:{mime};base64,{b64}"]


def _render_pdf_pages(raw: bytes, dpi: int = 200, max_pages: int = 5) -> list[str]:
	try:
		import fitz  # PyMuPDF
	except ImportError:
		frappe.throw(
			_("Thiếu thư viện PyMuPDF để xử lý PDF. Hãy cài: bench pip install pymupdf.")
		)
		return []

	document = fitz.open(stream=raw, filetype="pdf")
	try:
		data_urls: list[str] = []
		zoom = dpi / 72.0
		matrix = fitz.Matrix(zoom, zoom)
		for index, page in enumerate(document):
			if index >= max_pages:
				break
			pix = page.get_pixmap(matrix=matrix, alpha=False)
			png_bytes = pix.tobytes("png")
			b64 = base64.b64encode(png_bytes).decode("ascii")
			data_urls.append(f"data:image/png;base64,{b64}")
		return data_urls
	finally:
		document.close()


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _call_llm(settings: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
	import requests  # frappe ships with requests

	url = f"{settings['base_url']}/chat/completions"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {settings['api_key']}",
	}
	try:
		r = requests.post(url, headers=headers, json=payload, timeout=settings["timeout"])
	except requests.RequestException as exc:
		frappe.throw(_("Không gọi được AI: {0}").format(str(exc)))
		return {}

	if r.status_code >= 400:
		# Log nội dung để admin debug, nhưng không lộ API key.
		frappe.log_error(
			message=f"AI invoice extraction failed: HTTP {r.status_code} — {r.text[:2000]}",
			title="Branch Cash Invoice AI",
		)
		frappe.throw(_("AI trả về lỗi {0}. Xem Error Log.").format(r.status_code))

	try:
		return r.json()
	except ValueError:
		frappe.log_error(
			message=(
				f"AI invoice non-JSON response: HTTP {r.status_code}\n"
				f"Content-Type: {r.headers.get('Content-Type', '')}\n"
				f"--- body (truncated) ---\n{r.text[:4000]}"
			),
			title="Branch Cash Invoice AI",
		)
		frappe.throw(_("AI trả về dữ liệu không phải JSON. Xem Error Log."))
		return {}


def _extract_message_content(response_json: dict[str, Any]) -> str:
	choices = response_json.get("choices") or []
	if not choices:
		frappe.throw(_("AI không trả về kết quả nào."))
	msg = choices[0].get("message") or {}
	content = msg.get("content")
	if isinstance(content, list):
		# OpenAI multimodal response: content có thể là list các blocks.
		text_parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
		content = "\n".join(text_parts)
	if not content:
		frappe.throw(_("AI trả về nội dung rỗng."))
	return content


_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.+?)\s*```", re.DOTALL | re.IGNORECASE)


def _parse_json_payload(content: str) -> dict[str, Any]:
	text = content.strip()
	# Cắt markdown fence nếu có.
	m = _JSON_FENCE_RE.search(text)
	if m:
		text = m.group(1).strip()
	# Nếu vẫn không phải JSON object, lấy chuỗi từ "{" đầu tới "}" cuối.
	if not text.startswith("{"):
		start = text.find("{")
		end = text.rfind("}")
		if start != -1 and end != -1 and end > start:
			text = text[start : end + 1]
	try:
		return json.loads(text)
	except json.JSONDecodeError as exc:
		frappe.log_error(
			message=f"AI invoice JSON parse failed: {exc}\n--- raw ---\n{content[:4000]}",
			title="Branch Cash Invoice AI",
		)
		frappe.throw(_("AI trả về JSON không hợp lệ. Xem Error Log để biết chi tiết."))
		return {}


def _normalize_ai_result(data: dict[str, Any]) -> dict[str, Any]:
	"""Chuẩn hóa output AI về đúng kiểu mà form mong đợi."""

	def _str(value: Any) -> str:
		if value is None:
			return ""
		if isinstance(value, (int, float)):
			return str(value)
		return str(value).strip()

	def _num(value: Any) -> float:
		if value is None or value == "":
			return 0
		if isinstance(value, (int, float)):
			return float(value)
		s = str(value).strip().replace(" ", "")
		# Format VN dạng "127.579.889" hoặc "127.579.889,50".
		if "," in s and "." in s:
			s = s.replace(".", "").replace(",", ".")
		elif "," in s:
			parts = s.split(",")
			if len(parts[-1]) == 3 and len(parts) > 1:
				s = s.replace(",", "")
			else:
				s = s.replace(",", ".")
		else:
			# Chỉ có "." có thể là thousand sep VN — bỏ.
			if s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[-1]) == 3):
				s = s.replace(".", "")
		try:
			return float(s)
		except ValueError:
			return 0

	items_in = data.get("invoice_items") or []
	items_out = []
	for it in items_in:
		if not isinstance(it, dict):
			continue
		items_out.append(
			{
				"item_name": _str(it.get("item_name")),
				"item_code": _str(it.get("item_code")),
				"uom": _str(it.get("uom")),
				"qty": _num(it.get("qty")),
				"rate": _num(it.get("rate")),
				"amount": _num(it.get("amount")),
			}
		)

	return {
		"invoice_form_no": _str(data.get("invoice_form_no")),
		"invoice_serial": _str(data.get("invoice_serial")),
		"invoice_number": _str(data.get("invoice_number")),
		"invoice_id": _str(data.get("invoice_id")),
		"invoice_date": _str(data.get("invoice_date")) or None,
		"invoice_currency": _str(data.get("invoice_currency")) or "VND",
		"exchange_rate": _num(data.get("exchange_rate")) or 1,
		"seller_name": _str(data.get("seller_name")),
		"seller_tax_code": _str(data.get("seller_tax_code")),
		"seller_address": _str(data.get("seller_address")),
		"seller_phone": _str(data.get("seller_phone")),
		"buyer_contact_name": _str(data.get("buyer_contact_name")),
		"buyer_company_name": _str(data.get("buyer_company_name")),
		"buyer_tax_code": _str(data.get("buyer_tax_code")),
		"buyer_address": _str(data.get("buyer_address")),
		"buyer_warehouse": _str(data.get("buyer_warehouse")),
		"payment_method": _str(data.get("payment_method")),
		"payment_due_date": _str(data.get("payment_due_date")),
		"buyer_bank_account": _str(data.get("buyer_bank_account")),
		"buyer_bank_name": _str(data.get("buyer_bank_name")),
		"reference_number": _str(data.get("reference_number")),
		"total_before_tax": _num(data.get("total_before_tax")),
		"tax_rate": _str(data.get("tax_rate")),
		"tax_amount": _num(data.get("tax_amount")),
		"total_amount": _num(data.get("total_amount")),
		"total_in_words": _str(data.get("total_in_words")),
		"invoice_items": items_out,
	}
