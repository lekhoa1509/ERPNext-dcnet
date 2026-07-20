"""Parse hóa đơn điện tử (XML/HTML) phục vụ form Phiếu quỹ chi nhánh.

Hỗ trợ:
- XML chuẩn TCT (TT78/2022): root `HDon` → `DLHDon` → `TTChung`/`NDHDon`/`TToan`.
- HTML "bản thể hiện" của các nhà cung cấp HĐĐT (FPT, MISA, VNPT…) — dò theo
  nhãn tiếng Việt phổ biến (Mẫu số, Ký hiệu, Số, Ngày, Mã số thuế, Tên đơn vị,
  Cộng tiền hàng, Tổng cộng tiền thanh toán…).

Trả về dict phẳng dùng `set_value` từ phía client, kèm key đặc biệt
`invoice_items` là list dict child rows (item_name, item_code, uom, qty,
rate, amount).
"""

from __future__ import annotations

import os
import re
from typing import Any
from xml.etree import ElementTree as ET

import frappe
from frappe import _
from frappe.utils import get_files_path, get_site_path

DATE_RE_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
DATE_RE_DMY = re.compile(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})")


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


def parse_invoice_file(file_url: str) -> dict[str, Any]:
	path = _resolve_file_path(file_url)
	if not path or not os.path.exists(path):
		frappe.throw(_("Không tìm thấy file hóa đơn: {0}").format(file_url))

	ext = os.path.splitext(path)[1].lower()

	# PDF / ảnh → ủy quyền cho AI parser.
	from vn_accounting.branch_cash.ai_invoice_parser import (
		SUPPORTED_BINARY_EXTS,
		parse_invoice_with_ai,
	)

	if ext in SUPPORTED_BINARY_EXTS:
		return parse_invoice_with_ai(path)

	content = _decode_text_file(path)
	if ext == ".xml" or content.lstrip().startswith("<?xml"):
		return _parse_xml(content)
	if ext in (".html", ".htm"):
		return _parse_html(content)

	stripped = content.lstrip()
	if stripped.startswith("<?xml") or "<HDon" in stripped[:512] or "<DLHDon" in stripped[:512]:
		return _parse_xml(content)
	return _parse_html(content)


def _decode_text_file(path: str) -> str:
	with open(path, "rb") as fh:
		raw = fh.read()
	for encoding in ("utf-8-sig", "utf-8", "cp1258", "latin-1"):
		try:
			return raw.decode(encoding)
		except UnicodeDecodeError:
			continue
	frappe.throw(_("Không đọc được encoding của file hóa đơn."))
	return ""


# ---------------------------------------------------------------------------
# File reading
# ---------------------------------------------------------------------------


def _resolve_file_path(file_url: str) -> str | None:
	if file_url.startswith("/private/files/"):
		return os.path.join(get_site_path(), "private", "files", file_url[len("/private/files/") :])
	if file_url.startswith("/files/"):
		return os.path.join(get_files_path(), file_url[len("/files/") :])
	if os.path.isabs(file_url) and os.path.exists(file_url):
		return file_url

	doc_name = frappe.db.get_value("File", {"file_url": file_url}, "name")
	if doc_name:
		return frappe.get_doc("File", doc_name).get_full_path()
	return None


# ---------------------------------------------------------------------------
# XML
# ---------------------------------------------------------------------------


def _parse_xml(content: str) -> dict[str, Any]:
	try:
		root = ET.fromstring(content)
	except ET.ParseError as exc:
		frappe.throw(_("File XML hóa đơn không hợp lệ: {0}").format(str(exc)))

	for el in root.iter():
		if "}" in el.tag:
			el.tag = el.tag.split("}", 1)[1]

	dl = root.find(".//DLHDon") or root
	tt_chung = dl.find("TTChung")
	nd = dl.find("NDHDon")

	def text(parent, path: str) -> str:
		if parent is None:
			return ""
		el = parent.find(path)
		return (el.text or "").strip() if el is not None and el.text else ""

	nban = nd.find("Nban") if nd is not None else None
	nmua = nd.find("NMua") if nd is not None else None
	t_toan = nd.find("TToan") if nd is not None else None

	items: list[dict[str, Any]] = []
	if nd is not None:
		for hh in nd.findall("DSHHDVu/HHDVu"):
			items.append(
				{
					"item_name": text(hh, "THHDVu"),
					"item_code": text(hh, "MSo"),
					"uom": text(hh, "DVTinh"),
					"qty": _parse_amount(text(hh, "SLuong")),
					"rate": _parse_amount(text(hh, "DGia")),
					"amount": _parse_amount(text(hh, "TTien")),
				}
			)

	return {
		"invoice_form_no": text(tt_chung, "MSHDon"),
		"invoice_serial": text(tt_chung, "KHHDon"),
		"invoice_number": text(tt_chung, "SHDon"),
		"invoice_id": text(tt_chung, "IDHDon"),
		"invoice_date": _normalize_date(text(tt_chung, "TDLap")),
		"invoice_currency": text(tt_chung, "DVTTe") or "VND",
		"exchange_rate": _parse_amount(text(tt_chung, "TGia")) or 1,
		"seller_name": text(nban, "NBTen"),
		"seller_tax_code": text(nban, "NBMST"),
		"seller_address": text(nban, "NBDChi"),
		"seller_phone": text(nban, "NBDThoai"),
		"buyer_contact_name": text(nmua, "Ten"),
		"buyer_company_name": text(nmua, "TDVi"),
		"buyer_tax_code": text(nmua, "MST"),
		"buyer_address": text(nmua, "DChi"),
		"buyer_warehouse": text(nmua, "XTKho"),
		"payment_method": text(nmua, "HTTToan"),
		"payment_due_date": text(nmua, "HTToan"),
		"buyer_bank_account": text(nmua, "STKhoan"),
		"buyer_bank_name": text(nmua, "Tai"),
		"reference_number": text(nmua, "STChieu"),
		"total_before_tax": _parse_amount(text(t_toan, "TgTCThue")),
		"tax_rate": text(t_toan, "TSGTGTang"),
		"tax_amount": _parse_amount(text(t_toan, "TgTThue")),
		"total_amount": _parse_amount(text(t_toan, "TgTTTBSo")),
		"total_in_words": text(t_toan, "TgTTTBChu"),
		"invoice_items": items,
	}


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

# Block "Mẫu số / Ký hiệu / Số" — label nằm trong td span.labelNormal,
# value nằm trong td.labelBold liền kề.
_FORM_META_RE = re.compile(
    r'<td[^>]*>\s*<span[^>]*class="labelNormal"[^>]*>\s*'
    r'{label}\s*\(<span[^>]*class="labelEnglish"[^>]*>[^<]*</span>\)\s*:\s*</span>\s*</td>\s*'
    r'<td[^>]*class="[^"]*labelBold[^"]*"[^>]*>\s*([^<]+?)\s*</td>',
    re.DOTALL | re.IGNORECASE,
)

# Block người bán: tên = labelBoldHeader, các trường con = labelNormalHeader.
_SELLER_NAME_RE = re.compile(
    r'<span[^>]*class="labelBoldHeader"[^>]*>\s*([^<]+?)\s*</span>',
    re.DOTALL | re.IGNORECASE,
)
_SELLER_FIELD_RE = re.compile(
    r'<span[^>]*class="labelNormalHeader"[^>]*>\s*'
    r'{label}\s*\(<span[^>]*class="labelEnglish"[^>]*>[^<]*</span>\)\s*:\s*'
    r'<span[^>]*class="labelNormalHeader"[^>]*>\s*([^<]*?)\s*</span>',
    re.DOTALL | re.IGNORECASE,
)

# Block người mua / thanh toán / tham chiếu: labelNormal bao quanh, value trong itemNormal/labelNormal.
_BUYER_FIELD_RE = re.compile(
    r'<span[^>]*class="labelNormal"[^>]*>\s*'
    r'{label}\s*\(<span[^>]*class="labelEnglish"[^>]*>[^<]*</span>\)\s*:\s*'
    r'<span[^>]*class="(?:itemNormal|labelNormal)"[^>]*>\s*([^<]*?)\s*</span>',
    re.DOTALL | re.IGNORECASE,
)

# Ngày (date) D tháng (month) M năm (year) Y trên header.
_DATE_RE = re.compile(
    r"Ngày\s*\(\s*<span[^>]*labelEnglish[^>]*>\s*date\s*</span>\s*\)"
    r'\s*<span[^>]*labelBold[^>]*>\s*(\d{1,2})\s*</span>.*?'
    r"tháng\s*\(\s*<span[^>]*labelEnglish[^>]*>\s*month\s*</span>\s*\)"
    r'\s*<span[^>]*labelBold[^>]*>\s*(\d{1,2})\s*</span>.*?'
    r"năm\s*\(\s*<span[^>]*labelEnglish[^>]*>\s*year\s*</span>\s*\)"
    r'\s*<span[^>]*labelBold[^>]*>\s*(\d{4})\s*</span>',
    re.DOTALL | re.IGNORECASE,
)

# Items table.
_ITEM_TABLE_RE = re.compile(
    r'<tbody[^>]*id="tbody_pageTmp"[^>]*>(.*?)</tbody>',
    re.DOTALL | re.IGNORECASE,
)
_ITEM_ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)

# Totals.
_TOTAL_BEFORE_TAX_RE = re.compile(
    r"<tr[^>]*>(?P<row>[^<]*<td[^>]*>\s*<span[^>]*class=\"labelBold\"[^>]*>\s*Cộng tiền hàng.*?)</tr>",
    re.DOTALL | re.IGNORECASE,
)
_TAX_RATE_RE = re.compile(
    r'Thuế suất GTGT[^<]*<span[^>]*class="labelEnglishNormal"[^>]*>[^<]*</span>'
    r'\s*<span[^>]*class="labelBold"[^>]*>\s*([\d.,]+)\s*</span>',
    re.DOTALL | re.IGNORECASE,
)
_TAX_AMOUNT_RE = re.compile(
    r'Tiền thuế GTGT.*?<span[^>]*class="floatRight"[^>]*>\s*([\-\d.,]+)\s*</span>',
    re.DOTALL | re.IGNORECASE,
)
_TOTAL_AMOUNT_RE = re.compile(
    r'Tổng cộng tiền thanh toán.*?<span[^>]*class="itemNormal floatRight"[^>]*>\s*([\-\d.,]+)\s*</span>',
    re.DOTALL | re.IGNORECASE,
)
_TOTAL_IN_WORDS_RE = re.compile(
    r'Số tiền viết bằng chữ.*?</span>\s*<span[^>]*class="labelBold"[^>]*>\s*([^<]+?)\s*</span>',
    re.DOTALL | re.IGNORECASE,
)


def _form_meta(html: str, label: str) -> str:
	pattern = re.compile(
		_FORM_META_RE.pattern.format(label=re.escape(label)),
		_FORM_META_RE.flags,
	)
	m = pattern.search(html)
	return _strip_tags(m.group(1)).strip() if m else ""


def _seller_field(html: str, label: str) -> str:
	pattern = re.compile(
		_SELLER_FIELD_RE.pattern.format(label=re.escape(label)),
		_SELLER_FIELD_RE.flags,
	)
	m = pattern.search(html)
	return _strip_tags(m.group(1)).strip() if m else ""


def _buyer_field(html: str, label: str) -> str:
	pattern = re.compile(
		_BUYER_FIELD_RE.pattern.format(label=re.escape(label)),
		_BUYER_FIELD_RE.flags,
	)
	m = pattern.search(html)
	return _strip_tags(m.group(1)).strip() if m else ""


def _strip_tags(value: str) -> str:
	return re.sub(r"<[^>]+>", "", value or "").strip()


def _parse_html(content: str) -> dict[str, Any]:
	# Dùng nội dung "trang đầu" (đến hết phần ký) — nhiều mẫu lặp lại trang in.
	# Cắt tại lần xuất hiện thứ 2 của <body…</section-to-print> không chắc chắn,
	# nên ta dùng full content nhưng các regex .search() chỉ lấy match đầu tiên.

	# Ngày lập.
	invoice_date = None
	m = _DATE_RE.search(content)
	if m:
		d, mo, y = m.groups()
		invoice_date = f"{int(y):04d}-{int(mo):02d}-{int(d):02d}"

	# Người bán.
	seller_name = ""
	seller_match = _SELLER_NAME_RE.search(content)
	if seller_match:
		seller_name = _strip_tags(seller_match.group(1)).strip()

	# Items.
	items = _extract_items(content)

	# Totals.
	def amt(pattern: re.Pattern[str]) -> float:
		m = pattern.search(content)
		return _parse_amount(m.group(1)) if m else 0

	total_before_tax = 0
	mb = _TOTAL_BEFORE_TAX_RE.search(content)
	if mb:
		# row chứa nhiều td — số tổng nằm ở td cuối có nội dung số.
		row = mb.group("row")
		amounts = re.findall(r"<td[^>]*class=\"boxSmall itemNormal\"[^>]*>\s*([\-\d.,]+)\s*</td>", row)
		if amounts:
			total_before_tax = _parse_amount(amounts[-1])

	tax_rate_m = _TAX_RATE_RE.search(content)
	tax_rate = tax_rate_m.group(1).strip() if tax_rate_m else ""

	in_words = ""
	miw = _TOTAL_IN_WORDS_RE.search(content)
	if miw:
		in_words = _strip_tags(miw.group(1)).strip()

	# Đồng tiền — tìm cụm "Đồng tiền thanh toán(Currency code): VNĐ".
	currency = ""
	mc = re.search(
		r'Đồng tiền thanh toán\s*\(<span[^>]*class="labelEnglish"[^>]*>[^<]*</span>\)\s*:\s*'
		r'<span[^>]*class="labelNormal"[^>]*>\s*([^<]+?)\s*</span>',
		content,
		re.DOTALL | re.IGNORECASE,
	)
	if mc:
		currency = mc.group(1).strip()

	return {
		"invoice_form_no": _form_meta(content, "Mẫu số"),
		"invoice_serial": _form_meta(content, "Ký hiệu"),
		"invoice_number": _form_meta(content, "Số"),
		"invoice_id": "",
		"invoice_date": invoice_date,
		"invoice_currency": currency or "VND",
		"exchange_rate": 1,
		"seller_name": seller_name,
		"seller_tax_code": _seller_field(content, "Mã số thuế"),
		"seller_address": _seller_field(content, "Địa chỉ"),
		"seller_phone": _seller_field(content, "Điện thoại"),
		"buyer_contact_name": _buyer_field(content, "Họ tên người mua hàng"),
		"buyer_company_name": _buyer_field(content, "Tên đơn vị"),
		"buyer_tax_code": _buyer_field(content, "Mã số thuế"),
		"buyer_address": _buyer_field(content, "Địa chỉ"),
		"buyer_warehouse": _buyer_field(content, "Xuất tại kho"),
		"payment_method": _buyer_field(content, "Hình thức thanh toán"),
		"payment_due_date": _buyer_field(content, "Hạn thanh toán"),
		"buyer_bank_account": _buyer_field(content, "Số tài khoản"),
		"buyer_bank_name": _buyer_field(content, "Tại"),
		"reference_number": _buyer_field(content, "Số tham chiếu"),
		"total_before_tax": total_before_tax,
		"tax_rate": tax_rate,
		"tax_amount": amt(_TAX_AMOUNT_RE),
		"total_amount": amt(_TOTAL_AMOUNT_RE),
		"total_in_words": in_words,
		"invoice_items": items,
	}


def _extract_items(html: str) -> list[dict[str, Any]]:
	body = _ITEM_TABLE_RE.search(html)
	if not body:
		return []
	items: list[dict[str, Any]] = []
	for row_match in _ITEM_ROW_RE.finditer(body.group(1)):
		cells = [_strip_tags(c).strip() for c in _TD_RE.findall(row_match.group(1))]
		if len(cells) < 7:
			continue
		# STT, Tên, Mã, ĐVT, SL, ĐG, TT
		stt = cells[0]
		if not re.fullmatch(r"\d+", stt or ""):
			continue
		items.append(
			{
				"item_name": _decode_html_entities(cells[1]),
				"item_code": cells[2],
				"uom": cells[3],
				"qty": _parse_amount(cells[4]),
				"rate": _parse_amount(cells[5]),
				"amount": _parse_amount(cells[6]),
			}
		)
	return items


def _decode_html_entities(value: str) -> str:
	from html import unescape

	return unescape(value or "")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_date(value: str) -> str | None:
	if not value:
		return None
	m = DATE_RE_ISO.match(value)
	if m:
		return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
	m = DATE_RE_DMY.search(value)
	if m:
		day, month, year = m.groups()
		return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
	return None


def _parse_amount(value: str) -> float:
	if not value:
		return 0
	cleaned = value.strip().replace(" ", "")
	if "," in cleaned and "." in cleaned:
		# 127.579.889,50 → 127579889.50
		cleaned = cleaned.replace(".", "").replace(",", ".")
	elif "," in cleaned:
		parts = cleaned.split(",")
		if len(parts[-1]) == 3 and len(parts) > 1:
			cleaned = cleaned.replace(",", "")
		else:
			cleaned = cleaned.replace(",", ".")
	else:
		# Chỉ có dấu chấm — định dạng VN dùng "." làm thousand separator nếu
		# không có dấu phẩy decimal.
		cleaned = cleaned.replace(".", "")
	try:
		return float(cleaned)
	except ValueError:
		return 0
