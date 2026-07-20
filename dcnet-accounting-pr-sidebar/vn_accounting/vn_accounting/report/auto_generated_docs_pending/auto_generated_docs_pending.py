"""Tài liệu tự động — Worklist of auto-generated SI/JE.

Architecture-clean: queries `Auto Generated Doc Registry` (the central registry
populated by every app's auto-gen code path via `vn_accounting.auto_source.register`).
Source metadata (label, action, description, needs_approval) merged from each
app's `auto_generated_doc_sources` hook entry.

When a new auto-gen source ships, it self-registers via the hook + a single
`register()` call at the source's call site. NO change to this report needed.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import add_days, getdate, today

from vn_accounting.auto_source import get_sources_registry


_DS_TO_STATUS_LABEL = {0: "Bản nháp", 1: "Đã ghi sổ", 2: "Đã hủy"}
_STATUS_LABEL_TO_DS = {"Bản nháp": 0, "Đã ghi sổ": 1, "Đã hủy": 2}


def execute(filters=None):
	filters = filters or {}
	_normalize_filters(filters)
	sources = get_sources_registry()

	columns = _columns()
	data = _query_registry(filters, sources)

	if filters.get("only_overdue"):
		threshold = int(filters.get("overdue_days") or 7)
		cutoff = getdate(add_days(today(), -threshold))
		data = [r for r in data if r.get("docstatus") == 0 and r["posting_date"] <= cutoff]

	report_summary = _summary(data)

	if data:
		data.append({
			"loai": _("Tổng cộng"),
			"doctype": None,
			"doc_name": None,
			"status_label": None,
			"action": None,
			"posting_date": None,
			"source": None,
			"amount": sum(r["amount"] for r in data),
			"days_waiting": None,
			"remark": None,
			"currency": data[0].get("currency", "VND"),
			"docstatus": None,
		})

	return columns, data, _help_message(sources), None, report_summary


# --------------------------------------------------------------------------- #
# Filters + columns
# --------------------------------------------------------------------------- #

def _normalize_filters(f):
	if not f.get("company"):
		f["company"] = frappe.defaults.get_user_default("Company")
	if not f.get("from_date"):
		f["from_date"] = add_days(today(), -90)
	if not f.get("to_date"):
		f["to_date"] = today()
	status = f.get("doc_status")
	if not status:
		f["docstatus_in"] = [0]
	elif isinstance(status, str):
		f["docstatus_in"] = [_STATUS_LABEL_TO_DS.get(status, 0)]
	else:
		f["docstatus_in"] = [_STATUS_LABEL_TO_DS.get(s, 0) for s in status]


def _columns():
	return [
		{"label": _("Loại"), "fieldname": "loai", "fieldtype": "Data", "width": 220},
		{"label": _("Mã"), "fieldname": "doc_name", "fieldtype": "Dynamic Link",
		 "options": "doctype", "width": 200},
		{"label": _("Doctype"), "fieldname": "doctype", "fieldtype": "Data", "width": 1,
		 "hidden": 1},
		{"label": _("Trạng thái"), "fieldname": "status_label", "fieldtype": "Data", "width": 100},
		{"label": _("Hành động"), "fieldname": "action", "fieldtype": "Data", "width": 240},
		{"label": _("Ngày"), "fieldname": "posting_date", "fieldtype": "Date", "width": 95},
		{"label": _("Nguồn / Khách hàng / Tài sản"), "fieldname": "source", "fieldtype": "Data",
		 "width": 240},
		{"label": _("Tổng tiền"), "fieldname": "amount", "fieldtype": "Currency", "width": 140,
		 "options": "currency"},
		{"label": _("Số ngày chờ"), "fieldname": "days_waiting", "fieldtype": "Int", "width": 100},
		{"label": _("Ghi chú"), "fieldname": "remark", "fieldtype": "Small Text", "width": 220},
		{"label": _("Currency"), "fieldname": "currency", "fieldtype": "Link",
		 "options": "Currency", "width": 1, "hidden": 1},
		{"label": _("docstatus"), "fieldname": "docstatus", "fieldtype": "Int", "width": 1,
		 "hidden": 1},
	]


# --------------------------------------------------------------------------- #
# Registry query — single source of truth
# --------------------------------------------------------------------------- #

def _query_registry(filters, sources):
	"""LEFT JOIN registry to all known target doctypes. The registry is the source
	of truth; we read live docstatus + amount from the target."""
	rows = frappe.db.sql(
		"""
		SELECT
			r.source_key, r.target_doctype, r.target_name, r.posting_date,
			COALESCE(si.docstatus, je.docstatus) AS docstatus,
			COALESCE(si.grand_total, je.total_debit) AS amount,
			COALESCE(si.customer_name, si.customer, '') AS si_party,
			COALESCE(si.currency, 'VND') AS si_currency,
			COALESCE(je.user_remark, '') AS je_remark,
			COALESCE(si.remarks, '') AS si_remark,
			(SELECT MIN(jea.reference_type) FROM `tabJournal Entry Account` jea
			   WHERE jea.parent = je.name AND jea.reference_type != '') AS je_ref_type,
			(SELECT MIN(jea.reference_name) FROM `tabJournal Entry Account` jea
			   WHERE jea.parent = je.name AND jea.reference_type != '') AS je_ref_name
		FROM `tabAuto Generated Doc Registry` r
		LEFT JOIN `tabSales Invoice` si
		  ON r.target_doctype = 'Sales Invoice' AND r.target_name = si.name
		LEFT JOIN `tabJournal Entry` je
		  ON r.target_doctype = 'Journal Entry' AND r.target_name = je.name
		WHERE r.company = %(company)s
		  AND r.posting_date BETWEEN %(from_date)s AND %(to_date)s
		  AND COALESCE(si.docstatus, je.docstatus) IN %(docstatus_in)s
		  AND (si.name IS NOT NULL OR je.name IS NOT NULL)
		ORDER BY r.posting_date DESC
		""",
		filters,
		as_dict=True,
	)

	type_filter = filters.get("loai") or []
	today_d = getdate(today())
	out = []
	for r in rows:
		meta = sources.get(r.source_key, {})
		loai = meta.get("label", r.source_key)
		if type_filter and loai not in type_filter:
			continue
		ds = int(r.docstatus or 0)
		source_text = _source_text(r)
		remark = r.si_remark if r.target_doctype == "Sales Invoice" else r.je_remark
		out.append({
			"loai": loai,
			"doctype": r.target_doctype,
			"doc_name": r.target_name,
			"posting_date": r.posting_date,
			"source": source_text,
			"amount": float(r.amount or 0),
			"days_waiting": (today_d - getdate(r.posting_date)).days,
			"remark": (remark or "")[:200],
			"currency": r.si_currency or "VND",
			"docstatus": ds,
			"status_label": _DS_TO_STATUS_LABEL.get(ds, ""),
			"action": _action_for(meta, ds),
		})
	return out


def _source_text(r) -> str:
	if r.target_doctype == "Sales Invoice":
		return r.si_party or ""
	# Journal Entry: prefer ref_doctype:ref_name pair, fall back to remark
	if r.je_ref_type and r.je_ref_name:
		return f"{r.je_ref_type}: {r.je_ref_name}"
	return (r.je_remark or "")[:120]


def _action_for(meta: dict, docstatus: int) -> str:
	if docstatus == 0:
		return meta.get("action_draft") or "Duyệt và ghi sổ"
	if docstatus == 1:
		return meta.get("action_submitted") or "Đã hoàn tất — xem lại khi cần"
	if docstatus == 2:
		return meta.get("action_cancelled") or "Đã hủy — kiểm tra lý do"
	return ""


# --------------------------------------------------------------------------- #
# Summary cards + inline help (auto-built from registry hooks)
# --------------------------------------------------------------------------- #

def _summary(data):
	total_amount = sum(r["amount"] for r in data)
	drafts = [r for r in data if r.get("docstatus") == 0]
	submitted = [r for r in data if r.get("docstatus") == 1]
	cancelled = [r for r in data if r.get("docstatus") == 2]
	overdue_7 = sum(1 for r in drafts if r["days_waiting"] >= 7)
	overdue_30 = sum(1 for r in drafts if r["days_waiting"] >= 30)
	return [
		{"label": _("Bản nháp (chờ duyệt)"), "value": len(drafts),
		 "datatype": "Int", "indicator": "Blue"},
		{"label": _("Đã ghi sổ"), "value": len(submitted),
		 "datatype": "Int", "indicator": "Green" if submitted else "Gray"},
		{"label": _("Đã hủy"), "value": len(cancelled),
		 "datatype": "Int", "indicator": "Red" if cancelled else "Gray"},
		{"label": _("Tổng giá trị (toàn bộ trong phạm vi lọc)"), "value": total_amount,
		 "datatype": "Currency", "indicator": "Blue"},
		{"label": _("Bản nháp quá 7 ngày"), "value": overdue_7,
		 "datatype": "Int", "indicator": "Orange" if overdue_7 else "Gray"},
		{"label": _("Bản nháp quá 30 ngày"), "value": overdue_30,
		 "datatype": "Int", "indicator": "Red" if overdue_30 else "Gray"},
	]


def _help_message(sources: dict) -> str:
	"""Khối hướng dẫn — tự dựng từ phần mô tả của mỗi nguồn tự sinh.

	Khi một nguồn mới được khai báo qua hook, mô tả của nguồn đó tự xuất
	hiện ở đây. Không cần sửa báo cáo.
	"""
	# Chia 2 nhóm theo cờ "cần duyệt"
	need_review = []
	auto_post = []
	for key, meta in sorted(sources.items(), key=lambda kv: (not kv[1].get("needs_approval"), kv[1].get("label", kv[0]))):
		if meta.get("needs_approval"):
			need_review.append((key, meta))
		else:
			auto_post.append((key, meta))

	def _bullet(key, meta):
		label = frappe.utils.escape_html(meta.get("label", key))
		desc = meta.get("description", "")
		return f"<li><b>{label}</b> — {desc}</li>"

	need_review_html = "".join(_bullet(k, m) for k, m in need_review)
	auto_post_html = "".join(_bullet(k, m) for k, m in auto_post)

	# <details> mặc định thu gọn. CSS của Frappe áp lên mọi con dưới
	# <details> nên phải override mới ẩn được khi đóng (xem
	# frappe-v16-ui.md "Frappe global CSS forces details > * display:block").
	return _(
		"""<style>
.ag-help-block:not([open]) > *:not(summary) {{ display: none !important; }}
.ag-help-block > summary {{ list-style: none; }}
.ag-help-block > summary::-webkit-details-marker {{ display: none; }}
.ag-help-block > summary::before {{ content: "▸ "; color: #0366d6; font-weight: 700; }}
.ag-help-block[open] > summary::before {{ content: "▾ "; }}
</style>
<details class="ag-help-block" style="margin-bottom:8px; background:#f6f8fa; border-left:3px solid #0366d6;">
<summary style="cursor:pointer; padding:8px 12px; font-weight:600; user-select:none; font-size:12.5px;">
Hướng dẫn — Giải thích các loại tài liệu tự sinh (bấm để mở)
</summary>
<div style="padding:0 12px 10px 12px; font-size:12.5px; line-height:1.6;">
<div style="margin:0 0 6px 0;">
Báo cáo tập hợp các tài liệu kế toán do hệ thống tự sinh. Mặc định chỉ hiện tài liệu ở trạng thái <b>Bản nháp</b> để kế toán duyệt và ghi sổ. Đổi bộ lọc <i>Trạng thái</i> để xem thêm tài liệu <b>Đã ghi sổ</b> hoặc <b>Đã hủy</b>.
</div>
<b>Nhóm 1 — Cần kế toán duyệt và ghi sổ:</b>
<ul style="margin:6px 0 0 18px; padding:0;">{need_review_html}</ul>
<div style="margin-top:10px;"><b>Nhóm 2 — Hệ thống tự ghi sổ ngay (để biết và kiểm tra):</b></div>
<ul style="margin:6px 0 0 18px; padding:0;">{auto_post_html}</ul>
</div>
</details>"""
	).format(need_review_html=need_review_html, auto_post_html=auto_post_html)
