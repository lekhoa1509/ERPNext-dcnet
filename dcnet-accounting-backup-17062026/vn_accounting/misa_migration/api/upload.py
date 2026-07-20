"""Misa Migration upload API — whitelisted endpoints.

Creates Misa Migration Batch, attaches uploaded files, transitions
DRAFT → UPLOADED via state machine. All mutating endpoints acquire a
per-company lock from vn_accounting.misa_migration.state.
"""

from __future__ import annotations

import re
from typing import Any

import frappe
from frappe import _

from vn_accounting.misa_migration import state as st

DOCTYPE_BATCH = "Misa Migration Batch"


# -------------- filename → file_type auto-detect (UX Gap 2)

# Maps Misa SDK xlsx filename PATTERNS to file_type. Operator can still
# override via the dropdown after upload — this just sets a sane default
# so the common case (drop 9 OB files and click parse) works without
# manual tagging. Patterns are case-insensitive substring matches against
# the basename (without extension or path).
#
# Order matters: more specific patterns FIRST, generic LAST.
_FILENAME_TYPE_PATTERNS: list[tuple[re.Pattern, str]] = [
    # Phase 4 — transactions
    (re.compile(r"so[_ ]?nhat[_ ]?ky[_ ]?chung", re.I),     "NKC"),
    (re.compile(r"bang[_ ]?ke.*ban[_ ]?ra", re.I),          "Bang ke BR"),
    (re.compile(r"bang[_ ]?ke.*mua[_ ]?vao", re.I),         "Bang ke MV"),
    (re.compile(r"so[_ ]?chi[_ ]?tiet[_ ]?vat[_ ]?tu", re.I), "SCT"),
    # Phase 0 — opening balances (the 9 OB files)
    (re.compile(r"so[_ ]?du[_ ]?tai[_ ]?khoan[_ ]?ngan[_ ]?hang", re.I),
                                                              "OB Bank Balance"),
    (re.compile(r"so[_ ]?du[_ ]?tai[_ ]?khoan", re.I),       "OB Account Balance"),
    # BCDTK = Bảng cân đối tài khoản — Misa "mẫu quản trị" export.
    # Contains Đầu kỳ + Phát sinh + Cuối kỳ columns for every account.
    # OB loader extracts only Đầu kỳ (parser auto-detects 7+ col layout).
    (re.compile(r"bang[_ ]?can[_ ]?doi[_ ]?tai[_ ]?khoan", re.I),
                                                              "OB Account Balance"),
    (re.compile(r"cong[_ ]?no[_ ]?khach[_ ]?hang", re.I),   "OB Customer AR"),
    (re.compile(r"cong[_ ]?no[_ ]?nha[_ ]?cung[_ ]?cap", re.I),
                                                              "OB Supplier AP"),
    (re.compile(r"cong[_ ]?no[_ ]?nhan[_ ]?vien", re.I),    "OB Employee Advance"),
    (re.compile(r"chi[_ ]?phi[_ ]?tra[_ ]?truoc", re.I),    "OB Prepaid Expense"),
    (re.compile(r"ton[_ ]?kho", re.I),                      "OB Inventory"),
    (re.compile(r"tai[_ ]?san[_ ]?co[_ ]?dinh[_ ]?dau[_ ]?ky", re.I),
                                                              "OB Fixed Asset"),
    (re.compile(r"cong[_ ]?cu[_ ]?dung[_ ]?cu[_ ]?dau[_ ]?ky", re.I),
                                                              "OB CCDC"),
    # ----- Phase 1 — reference master GROUPS (must fire BEFORE plain
    # Customer/Supplier/Item patterns because Misa exports the group
    # file as "Danh_sach_nhom_khach_hang_nha_cung_cap.xlsx" which would
    # otherwise match the Customer regex first via partial substring).
    (re.compile(r"danh[_ ]?sach[_ ]?nhom[_ ]?(khach[_ ]?hang|nha[_ ]?cung[_ ]?cap)", re.I),
                                                              "Customer Group"),
    (re.compile(r"danh[_ ]?sach[_ ]?nhom[_ ]?vat[_ ]?tu", re.I),
                                                              "Item Group"),
    # Bank Account (TK ngân hàng — more specific than Bank)
    (re.compile(r"danh[_ ]?sach[_ ]?tai[_ ]?khoan[_ ]?ngan[_ ]?hang", re.I),
                                                              "Bank Account"),
    # Phase 2 — default & closing rule accounts (more specific FIRST,
    # they share "tai_khoan_ngam_dinh" / "tai_khoan_ket_chuyen" prefix
    # and would otherwise collapse into "Account" via he_thong below)
    (re.compile(r"danh[_ ]?sach[_ ]?tai[_ ]?khoan[_ ]?ngam[_ ]?dinh", re.I),
                                                              "Misa Default Account"),
    (re.compile(r"danh[_ ]?sach[_ ]?tai[_ ]?khoan[_ ]?ket[_ ]?chuyen", re.I),
                                                              "Misa Closing Rule"),
    # Phase 2 — Chart of Accounts (more specific than Bank)
    (re.compile(r"danh[_ ]?sach[_ ]?he[_ ]?thong[_ ]?tai[_ ]?khoan", re.I),
                                                              "Account"),
    # ----- Phase 3 — master entities (after groups)
    (re.compile(r"danh[_ ]?sach[_ ]?khach[_ ]?hang", re.I), "Customer"),
    (re.compile(r"danh[_ ]?sach[_ ]?nha[_ ]?cung[_ ]?cap", re.I),
                                                              "Supplier"),
    (re.compile(r"danh[_ ]?sach[_ ]?nhan[_ ]?vien", re.I),  "Employee"),
    (re.compile(r"danh[_ ]?sach[_ ]?hang[_ ]?hoa", re.I),   "Item"),
    # ----- Phase 1 — reference masters
    (re.compile(r"danh[_ ]?sach[_ ]?ngan[_ ]?hang", re.I),  "Bank"),
    (re.compile(r"danh[_ ]?sach[_ ]?don[_ ]?vi[_ ]?tinh", re.I),
                                                              "UOM"),
    (re.compile(r"danh[_ ]?sach[_ ]?kho\b", re.I),          "Warehouse"),
    (re.compile(r"danh[_ ]?sach[_ ]?co[_ ]?cau[_ ]?to[_ ]?chuc", re.I),
                                                              "Department"),
    (re.compile(r"danh[_ ]?sach[_ ]?cong[_ ]?trinh", re.I), "Project"),
    (re.compile(r"danh[_ ]?sach[_ ]?loai[_ ]?tai[_ ]?san[_ ]?co[_ ]?dinh", re.I),
                                                              "Asset Category"),
    (re.compile(r"danh[_ ]?sach[_ ]?loai[_ ]?cong[_ ]?cu[_ ]?dung[_ ]?cu", re.I),
                                                              "CCDC Category"),
    # ----- Cost Center alias (Misa: "Doi_tuong_tap_hop_chi_phi")
    (re.compile(r"doi[_ ]?tuong[_ ]?tap[_ ]?hop[_ ]?chi[_ ]?phi", re.I),
                                                              "Cost Center"),
]


def detect_file_type_from_name(filename: str | None) -> str:
    """Return best-guess file_type for a Misa SDK filename, or 'Unknown'.

    Strips path + extension + any leading/trailing whitespace, then
    matches against the FIRST regex in _FILENAME_TYPE_PATTERNS that
    fires. Vietnamese diacritics are NOT stripped (Misa filenames are
    ASCII), but the underscore-vs-space tolerance allows for either.

    Operator can override via update_file_type endpoint at any time
    before Parse runs.
    """
    if not filename:
        return "Unknown"
    base = filename.rsplit("/", 1)[-1]
    # Drop extension
    base = re.sub(r"\.(xlsx|xls|csv)$", "", base, flags=re.I)
    base = base.strip()
    if not base:
        return "Unknown"
    for pattern, file_type in _FILENAME_TYPE_PATTERNS:
        if pattern.search(base):
            return file_type
    return "Unknown"


# ---------------------------------------------------------------------- helpers

def _serialize(batch_name: str) -> dict[str, Any]:
    """Return a lean dict for the Vue store (no internal Frappe meta)."""
    if not frappe.db.exists(DOCTYPE_BATCH, batch_name):
        frappe.throw(_("Không tìm thấy batch: {0}").format(batch_name))
    doc = frappe.get_doc(DOCTYPE_BATCH, batch_name)
    return {
        "name": doc.name,
        "batch_title": doc.batch_title,
        "company": doc.company,
        "status": doc.status,
        "files": [
            {
                "name": f.name,
                "idx": f.idx,
                "file_type": f.file_type,
                "file_url": f.file_url,
                "original_filename": f.original_filename,
                "size_bytes": f.size_bytes,
                "row_count": f.row_count,
                "total_rows_expected": f.get("total_rows_expected") or 0,
                "parse_status": f.parse_status,
                "parse_error": f.parse_error,
            }
            for f in (doc.files or [])
        ],
        "total_files": doc.total_files or 0,
        "total_rows": doc.total_rows or 0,
        "posted_docs_count": doc.posted_docs_count or 0,
        "failed_rows_count": doc.failed_rows_count or 0,
        "job_id": doc.job_id,
        "stuck_at": doc.stuck_at,
        "created_on": str(doc.created_on) if doc.created_on else None,
        "started_on": str(doc.started_on) if doc.started_on else None,
        "parsed_on": str(doc.parsed_on) if doc.parsed_on else None,
        "posted_on": str(doc.posted_on) if doc.posted_on else None,
        "reversed_on": str(doc.reversed_on) if doc.reversed_on else None,
        "notes": doc.notes or "",
    }




# ---------------------------------------------------------------------- endpoints

@frappe.whitelist()
def create_batch(company: str, batch_title: str | None = None,
                 ob_posting_date: str | None = None,
                 shard_token: str | None = None) -> dict[str, Any]:
    """Create a new Misa Migration Batch in DRAFT.

    Args:
        company: Company name (required).
        batch_title: User-friendly label, optional.
        ob_posting_date: posting_date for OB JE + OB SEs. Misa "đầu kỳ"
            files don't carry the date — operator MUST specify which
            period start the OB represents. For "đầu kỳ 2025" pass
            "2024-12-31"; for "đầu kỳ 2026" pass "2025-12-31".
        shard_token: Optional shard label. When empty (default) the legacy
            "one active batch per Company" rule applies. When non-empty,
            two batches with DIFFERENT non-empty shard_tokens for the same
            Company can coexist in active state — used for two-batch
            parallel posting (one shard → long queue, other → default).
            Token is normalized via ``.strip()``.

    Returns:
        Serialized batch dict for the Vue store.
    """
    if not company:
        frappe.throw(_("Phải chọn Company."))
    if not frappe.db.exists("Company", company):
        frappe.throw(_("Company không tồn tại: {0}").format(company))

    # Normalize shard_token: empty / whitespace → None
    shard_token = (shard_token or "").strip() or None
    if shard_token and len(shard_token) > 32:
        frappe.throw(_("shard_token tối đa 32 ký tự."))

    existing = st.find_active_batch(company, shard_token=shard_token)
    if existing:
        if shard_token:
            frappe.throw(
                _("Đã có batch đang chạy cho Company {0} shard '{1}': {2}.").format(
                    company, shard_token, existing,
                )
            )
        frappe.throw(
            _("Đã có batch đang chạy cho Company {0}: {1}. Vui lòng hoàn tất hoặc Undo trước khi tạo mới.").format(
                company, existing,
            )
        )

    # Acquire (company, shard_token)-scoped lock for the creation window
    # so two parallel create_batch calls don't both win the active-batch
    # race for the same shard slot.
    with st.lock_for_company(company, shard_token=shard_token):
        # Re-check inside the lock — another caller may have created.
        existing = st.find_active_batch(company, shard_token=shard_token)
        if existing:
            frappe.throw(
                _("Đã có batch đang chạy cho Company {0}: {1}.").format(company, existing)
            )
        doc = frappe.get_doc({
            "doctype": DOCTYPE_BATCH,
            "company": company,
            "batch_title": (batch_title or "").strip() or None,
            "ob_posting_date": ob_posting_date or None,
            "shard_token": shard_token or "",
            "status": st.DRAFT,
        })
        doc.insert(ignore_permissions=False)
        frappe.db.commit()
    return _serialize(doc.name)


@frappe.whitelist()
def attach_file(
    batch_name: str,
    file_url: str,
    file_type: str = "Unknown",
    original_filename: str | None = None,
    size_bytes: int = 0,
) -> dict[str, Any]:
    """Attach an uploaded file to a Misa Migration Batch.

    Transitions status DRAFT → UPLOADED on first attachment. Subsequent
    attachments keep status at UPLOADED.

    The `file_url` should reference an already-uploaded File doc (created
    via Frappe's standard /api/method/upload_file endpoint before calling).
    """
    if not batch_name or not file_url:
        frappe.throw(_("batch_name và file_url là bắt buộc."))

    doc = frappe.get_doc(DOCTYPE_BATCH, batch_name)
    if doc.status not in (st.DRAFT, st.UPLOADED):
        frappe.throw(
            _("Không thể thêm file ở trạng thái {0}. Chỉ thêm được khi DRAFT hoặc UPLOADED.").format(doc.status)
        )

    # UX Gap 2: when caller didn't specify a file_type (or passed
    # "Unknown"), auto-detect from filename. Operator can override later.
    resolved_filename = original_filename or file_url.rsplit("/", 1)[-1]
    if not file_type or file_type == "Unknown":
        file_type = detect_file_type_from_name(resolved_filename)

    with st.lock_for_batch(doc):
        # Re-read inside the lock to avoid TOCTOU.
        doc = frappe.get_doc(DOCTYPE_BATCH, batch_name)
        doc.append("files", {
            "file_type": file_type or "Unknown",
            "file_url": file_url,
            "original_filename": resolved_filename,
            "size_bytes": int(size_bytes or 0),
            "parse_status": "Pending",
        })
        if doc.status == st.DRAFT:
            st.transition(doc, st.UPLOADED, reason="first file attached")
        doc.save(ignore_permissions=False)
        frappe.db.commit()
    return _serialize(doc.name)


@frappe.whitelist()
def remove_file(batch_name: str, file_row_name: str) -> dict[str, Any]:
    """Remove a Misa Migration File child row before parse starts.

    Allowed only while batch is DRAFT or UPLOADED.
    """
    doc = frappe.get_doc(DOCTYPE_BATCH, batch_name)
    if doc.status not in (st.DRAFT, st.UPLOADED):
        frappe.throw(_("Không thể xóa file ở trạng thái {0}.").format(doc.status))

    with st.lock_for_batch(doc):
        doc = frappe.get_doc(DOCTYPE_BATCH, batch_name)
        new_files = [f for f in (doc.files or []) if f.name != file_row_name]
        if len(new_files) == len(doc.files or []):
            frappe.throw(_("Không tìm thấy file row: {0}").format(file_row_name))
        doc.set("files", new_files)
        if not new_files and doc.status == st.UPLOADED:
            st.transition(doc, st.DRAFT, reason="last file removed")
        doc.save(ignore_permissions=False)
        frappe.db.commit()
    return _serialize(doc.name)


@frappe.whitelist()
def get_batch(batch_name: str) -> dict[str, Any]:
    """Return current state of a batch for store hydration."""
    return _serialize(batch_name)


@frappe.whitelist()
def get_voucher_submit_progress(batch_name: str) -> dict[str, Any]:
    """Per-doctype voucher submit progress for the Phase 4 submit phase.

    During Phase 4, NKC vouchers are first inserted as Drafts (docstatus=0)
    then `submit_phase_4_drafts` submits them (→ docstatus=1) which creates
    GL entries. The Migration Row.status flag does NOT track this — only
    the ERPNext doctype docstatus does. This endpoint exposes the per-
    doctype submit % so the UI can show real-time progress during the
    submit phase that otherwise looks frozen for ~30-60 minutes.
    """
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    if not company:
        return {"doctypes": []}
    out = []
    for dt in ("Sales Invoice", "Purchase Invoice", "Payment Entry",
               "Stock Entry", "Journal Entry"):
        n = frappe.db.sql(
            f"SELECT SUM(docstatus=1), COUNT(*) FROM `tab{dt}` WHERE company=%s",
            (company,),
        )[0]
        sub = int(n[0] or 0)
        tot = int(n[1] or 0)
        pct = round(sub * 100 / tot) if tot else 0
        out.append({
            "doctype": dt,
            "submitted": sub,
            "total": tot,
            "pct": pct,
        })
    return {"doctypes": out, "company": company}


@frappe.whitelist()
def get_post_progress_live(batch_name: str) -> dict[str, Any]:
    """Real-time progress snapshot during POSTING/REVERSING.

    Unlike Misa Migration Batch.posted_docs_count (only updated at the
    END of the post_batch run), this endpoint queries Migration Row
    statuses live + computes a meaningful % based on Posted vs total
    that-creates-a-doc rows (excludes subsidiary lookups Bang ke /
    SCT that intentionally never transition to Posted).

    Returns:
      {
        "batch": str,
        "status": str (batch status),
        "posted": int,
        "failed": int,
        "ready": int,
        "total": int,
        "pct": int (0-100),
        "phase_hint": str (UPLOAD / PHASE_0_4_BUILD / PHASE_4_SUBMIT / DONE),
      }
    """
    batch_status = frappe.db.get_value("Misa Migration Batch", batch_name, "status")
    counts = dict(frappe.db.sql(
        """SELECT status, COUNT(*) FROM `tabMisa Migration Row`
           WHERE batch=%s GROUP BY status""",
        (batch_name,),
    ))
    posted = int(counts.get("Posted", 0))
    failed = int(counts.get("Failed", 0))
    ready = int(counts.get("Ready", 0))
    new_count = int(counts.get("New", 0))
    # Total "productive" rows (those that should reach Posted) — exclude
    # Skipped/Invalid which are intentionally not counted as work-to-do.
    total_productive = posted + failed + ready + new_count
    if total_productive == 0:
        pct = 0
    else:
        pct = round((posted + failed) * 100 / total_productive)

    # GL Entry growth is the proxy for Phase 4 submit progress
    company = frappe.db.get_value("Misa Migration Batch", batch_name, "company")
    gl_count = 0
    if company:
        gl_count = frappe.db.sql(
            "SELECT COUNT(*) FROM `tabGL Entry` WHERE company=%s AND is_cancelled=0",
            (company,),
        )[0][0]

    # Phase hint based on state
    if batch_status not in ("POSTING", "REVERSING"):
        phase_hint = batch_status or "UNKNOWN"
    elif posted < total_productive * 0.8:
        phase_hint = "PHASE_0_4_BUILD"  # creating rows
    elif gl_count < 50000:
        phase_hint = "PHASE_4_SUBMIT"  # submitting drafts
    else:
        phase_hint = "PHASE_4_FINALIZE"

    return {
        "batch": batch_name,
        "status": batch_status,
        "posted": posted,
        "failed": failed,
        "ready": ready,
        "new": new_count,
        "total": total_productive,
        "pct": pct,
        "gl_count": gl_count,
        "phase_hint": phase_hint,
    }


@frappe.whitelist()
def find_active_batch(company: str | None = None) -> dict[str, Any] | None:
    """Find an in-flight Misa Migration Batch for resume-on-page-reload.

    Returns the most recently active batch (POSTING/REVERSING/STUCK or
    upload-in-progress: DRAFT/UPLOADED/PARSED/REVIEWED) for the given
    company. When `company` is None, looks across all companies the
    user has access to.

    Used by the hub UI when localStorage is empty (cleared, different
    browser, incognito) so the operator doesn't lose track of an
    in-flight migration after navigating away.

    Returns serialized batch dict or None if no active batch found.
    """
    active_statuses = (
        st.DRAFT, st.UPLOADED, st.PARSED, st.REVIEWED,
        st.POSTING, st.REVERSING, st.STUCK,
    )
    filters: dict = {"status": ["in", active_statuses]}
    if company:
        filters["company"] = company
    rows = frappe.db.get_all(
        DOCTYPE_BATCH,
        filters=filters,
        fields=["name", "status", "company", "modified"],
        order_by="modified desc",
        limit=1,
    )
    if not rows:
        return None
    return _serialize(rows[0]["name"])


@frappe.whitelist()
def update_file_type(batch_name: str, file_row_name: str, file_type: str) -> dict[str, Any]:
    """Update file_type classification on a Misa Migration File row.

    Useful when auto-detect picked Unknown and user manually chooses
    (NKC / Bang ke BR / etc.).
    """
    doc = frappe.get_doc(DOCTYPE_BATCH, batch_name)
    if doc.status not in (st.DRAFT, st.UPLOADED):
        frappe.throw(_("Không thể đổi loại file ở trạng thái {0}.").format(doc.status))
    with st.lock_for_batch(doc):
        doc = frappe.get_doc(DOCTYPE_BATCH, batch_name)
        found = False
        for f in (doc.files or []):
            if f.name == file_row_name:
                f.file_type = file_type or "Unknown"
                found = True
                break
        if not found:
            frappe.throw(_("Không tìm thấy file row: {0}").format(file_row_name))
        doc.save(ignore_permissions=False)
        frappe.db.commit()
    return _serialize(doc.name)


@frappe.whitelist()
def get_failed_rows_grouped(batch_name: str, entity_type: str | None = None,
                            limit_per_group: int = 5,
                            max_groups: int = 12) -> dict[str, Any]:
    """Return Failed rows grouped by error_message (first 200 chars) with sample voucher_nos.

    Used by PostStep.vue tooltip on the Failed count — operator clicks the
    red number, sees up to `max_groups` distinct error reasons with the
    voucher_no of the first `limit_per_group` rows per error. Frontend
    matches each error against FAILED_ACTION_RULES to suggest remediation.
    """
    filters = ["batch=%s", "status='Failed'"]
    params: list[Any] = [batch_name]
    if entity_type:
        # Frontend passes entity_type which maps to file_type in some cases
        # and entity_type in others. Match either.
        filters.append("(file_type=%s OR entity_type=%s)")
        params.extend([entity_type, entity_type])
    where = " AND ".join(filters)
    rows = frappe.db.sql(
        f"""SELECT LEFT(error_message, 200) AS err, COUNT(*) AS n,
                   GROUP_CONCAT(COALESCE(NULLIF(voucher_no, ''), name)
                                ORDER BY name SEPARATOR '|') AS samples
           FROM `tabMisa Migration Row`
           WHERE {where} AND error_message IS NOT NULL AND error_message != ''
           GROUP BY LEFT(error_message, 200)
           ORDER BY n DESC
           LIMIT {max_groups}""",
        tuple(params),
        as_dict=True,
    )
    groups = []
    for r in rows:
        samples_raw = r.get("samples") or ""
        sample_list = [s.strip() for s in samples_raw.split("|") if s.strip()][:limit_per_group]
        groups.append({
            "error": r["err"],
            "count": int(r["n"]),
            "sample": sample_list,
        })
    total = sum(g["count"] for g in groups)
    return {
        "batch": batch_name,
        "entity_type": entity_type,
        "groups": groups,
        "total_in_groups": total,
    }
