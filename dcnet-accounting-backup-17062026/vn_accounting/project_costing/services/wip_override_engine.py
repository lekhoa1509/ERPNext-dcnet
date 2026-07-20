"""WIP Account Override engine — JE bù 2-layer pattern per BL §12.

When KTT sets `wip_override_account` on a cost source (PI / SE / DN / EC) for
a project, ERPNext core posts to its default account; this engine then posts
a balancing JE Dr <override> / Cr <default> with project ref + marker, so the
override TK ends up holding the cost balance per VAS TT99/2025.

Mirrors LCV bù pattern (`vn_accounting/landed_cost/lcv_hooks.py`). Idempotent
via marker substring `[PROJECT_COSTING:<project>][TYPE:WIP_OVERRIDE]` in
JE.user_remark.

Auto-creates Project Costing master for the project on first cost submit, so
KTT không phải tạo Project Costing thủ công trước.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt

_MARKER_PREFIX = "PROJECT_COSTING"
_TYPE = "WIP_OVERRIDE"


def _marker(project: str) -> str:
    return f"[{_MARKER_PREFIX}:{project}][TYPE:{_TYPE}]"


def _marker_with_src(project: str, src_dt: str, src_name: str) -> str:
    return f"{_marker(project)}[SRC:{src_dt}:{src_name}]"


def _get_settings_wip_account(company: str) -> str | None:
    """Resolve company-scoped default WIP account from VN Accounting Settings."""
    from vn_accounting.utils.account_resolver import resolve_account

    return resolve_account("wip_account_project_costing", company)


def _ensure_project_costing(project: str) -> str | None:
    """Idempotent: return Project Costing.name for `project`; create if missing.

    Returns None if project not found.
    """
    if not project:
        return None
    if frappe.db.exists("Project Costing", project):
        return project
    p = frappe.db.get_value(
        "Project", project, ["project_name", "customer", "company"], as_dict=True
    )
    if not p:
        return None
    pc = frappe.new_doc("Project Costing")
    pc.project = project
    pc.project_name = p.project_name
    pc.customer = p.customer
    pc.company = p.company
    pc.flags.ignore_permissions = True
    pc.insert()
    return pc.name


def _find_existing_je(project: str, src_dt: str, src_name: str, *, include_cancelled: bool = False) -> str | None:
    """Locate JE bù by marker. Substring match in user_remark."""
    marker = _marker_with_src(project, src_dt, src_name)
    filters = {"user_remark": ["like", f"%{marker}%"]}
    if not include_cancelled:
        filters["docstatus"] = 1
    return frappe.db.get_value("Journal Entry", filters, "name")


def _post_wip_override_je(
    *,
    company: str,
    posting_date,
    src_dt: str,
    src_name: str,
    overrides: list[dict],
) -> str | None:
    """Build + submit JE bù from collected overrides.

    Each override = {"project": ..., "default_account": ..., "override_account": ..., "amount": ...}.
    Aggregates by (project, default, override). Skips if Σ ≤ 0 or no diff.
    """
    # Skip if any project already has an active JE for this source (idempotent)
    seen_projects = {o["project"] for o in overrides}
    for project in seen_projects:
        if _find_existing_je(project, src_dt, src_name):
            return None  # already posted

    # Aggregate
    by_key: dict[tuple[str, str, str], float] = {}
    for o in overrides:
        if o["default_account"] == o["override_account"]:
            continue  # no-op
        amt = flt(o["amount"])
        if amt <= 0:
            continue
        key = (o["project"], o["default_account"], o["override_account"])
        by_key[key] = by_key.get(key, 0) + amt

    if not by_key:
        return None

    je = frappe.new_doc("Journal Entry")
    je.posting_date = posting_date
    je.company = company
    je.voucher_type = "Journal Entry"
    primary_project = sorted(seen_projects)[0]
    je.user_remark = (
        f"{_marker_with_src(primary_project, src_dt, src_name)} "
        + _("Bù tài khoản WIP công trình từ {0} {1}").format(src_dt, src_name)
    )

    for (project, default_acc, override_acc), amt in by_key.items():
        je.append("accounts", {
            "account": override_acc,
            "debit_in_account_currency": amt,
            "project": project,
            "reference_type": "Project Costing",
            "reference_name": project,
            "user_remark": _("Tập hợp chi phí công trình {0}").format(project),
        })
        je.append("accounts", {
            "account": default_acc,
            "credit_in_account_currency": amt,
            "project": project,
            "reference_type": "Project Costing",
            "reference_name": project,
            "user_remark": _("Đảo TK mặc định"),
        })

    je.flags.ignore_permissions = True
    je.insert()
    je.submit()
    return je.name


def _cancel_je_for_source(src_dt: str, src_name: str) -> int:
    """Cancel ALL active JE bù for this source (across any project).

    Returns count cancelled. Pattern: substring match `[SRC:<dt>:<name>]`.
    """
    src_pat = f"[SRC:{src_dt}:{src_name}]"
    je_names = frappe.db.sql_list(
        """SELECT name FROM `tabJournal Entry`
           WHERE docstatus = 1 AND user_remark LIKE %s""",
        (f"%{src_pat}%",),
    )
    n = 0
    for name in je_names:
        je = frappe.get_doc("Journal Entry", name)
        je.flags.ignore_permissions = True
        je.cancel()
        n += 1
    return n


# ─────────────────────────────────────────────────────────────────────────────
# Per-DocType handlers — wired in hooks.py doc_events
# ─────────────────────────────────────────────────────────────────────────────


def on_purchase_invoice_submit(doc, method=None):
    """PI: each Item row with project → amount = row.base_net_amount.

    KTT sets PI.wip_override_account once (parent level); applies to all rows
    sharing a project. Multi-project PI: split happens per row's project tag.
    """
    # TIER 1 PERF: short-circuit during Misa migration — NKC already has these legs
    if getattr(frappe.flags, "misa_migration_active", False):
        return
    if doc.docstatus != 1:
        return
    override = doc.get("wip_override_account")
    if not override:
        return
    default = _get_settings_wip_account(doc.company)
    if not default or default == override:
        return

    overrides: list[dict] = []
    parent_project = (doc.get("project") or "").strip()
    for item in (doc.items or []):
        # Parent.project (Accounting Dimension header) WINS over Item.project —
        # user's explicit header tag is authoritative; Item.project is often
        # auto-filled from Item Default (stale). Fallback to Item.project only
        # when parent header is blank.
        proj = parent_project or (item.get("project") or "").strip()
        if not proj:
            continue
        _ensure_project_costing(proj)
        amt = flt(item.get("base_net_amount") or item.get("net_amount") or item.get("amount"))
        if amt <= 0:
            continue
        overrides.append({
            "project": proj,
            "default_account": default,
            "override_account": override,
            "amount": amt,
        })

    if overrides:
        _post_wip_override_je(
            company=doc.company,
            posting_date=doc.posting_date,
            src_dt="Purchase Invoice",
            src_name=doc.name,
            overrides=overrides,
        )


def on_purchase_invoice_cancel(doc, method=None):
    _cancel_je_for_source("Purchase Invoice", doc.name)


def on_stock_entry_submit(doc, method=None):
    """SE Material Issue: amount = doc.total_outgoing_value.

    SE.project is at parent level (1 SE = 1 project per Frappe core). All cost
    of issued stock goes to the single project.
    """
    # TIER 1 PERF: short-circuit during Misa migration — NKC already has these legs
    if getattr(frappe.flags, "misa_migration_active", False):
        return
    if doc.docstatus != 1:
        return
    if doc.stock_entry_type and doc.stock_entry_type not in ("Material Issue",):
        # Phase 2 chỉ handle Material Issue. Material Transfer / Manufacture phase 3+.
        return
    override = doc.get("wip_override_account")
    if not override:
        return
    default = _get_settings_wip_account(doc.company)
    if not default or default == override:
        return

    # Parent.project header wins; fallback to row-level if header blank.
    # Aggregate per project across rows for accurate split.
    parent_project = (doc.get("project") or "").strip()
    by_project: dict[str, float] = {}
    if parent_project:
        # Header set → all cost belongs to this project
        amt = flt(doc.total_outgoing_value)
        if amt > 0:
            by_project[parent_project] = amt
    else:
        # Fallback: sum row amounts per row.project
        for item in (doc.items or []):
            row_proj = (item.get("project") or "").strip()
            if not row_proj:
                continue
            by_project[row_proj] = by_project.get(row_proj, 0) + flt(
                item.get("amount") or item.get("basic_amount") or 0
            )

    if not by_project:
        return

    overrides = []
    for project, amount in by_project.items():
        if amount <= 0:
            continue
        _ensure_project_costing(project)
        overrides.append({
            "project": project,
            "default_account": default,
            "override_account": override,
            "amount": amount,
        })

    if overrides:
        _post_wip_override_je(
            company=doc.company,
            posting_date=doc.posting_date,
            src_dt="Stock Entry",
            src_name=doc.name,
            overrides=overrides,
        )


def on_stock_entry_cancel(doc, method=None):
    _cancel_je_for_source("Stock Entry", doc.name)


def on_delivery_note_submit(doc, method=None):
    """DN: each Item row with project → amount = row.base_net_amount.

    Same shape as PI: parent-level override, per-row project tag.
    """
    # TIER 1 PERF: short-circuit during Misa migration — NKC already has these legs
    if getattr(frappe.flags, "misa_migration_active", False):
        return
    if doc.docstatus != 1:
        return
    override = doc.get("wip_override_account")
    if not override:
        return
    default = _get_settings_wip_account(doc.company)
    if not default or default == override:
        return

    overrides: list[dict] = []
    for item in (doc.items or []):
        proj = (doc.get("project") or "").strip() or (item.get("project") or "").strip()
        if not proj:
            continue
        _ensure_project_costing(proj)
        amt = flt(item.get("base_net_amount") or item.get("net_amount") or item.get("amount"))
        if amt <= 0:
            continue
        overrides.append({
            "project": proj,
            "default_account": default,
            "override_account": override,
            "amount": amt,
        })

    if overrides:
        _post_wip_override_je(
            company=doc.company,
            posting_date=doc.posting_date,
            src_dt="Delivery Note",
            src_name=doc.name,
            overrides=overrides,
        )


def on_delivery_note_cancel(doc, method=None):
    _cancel_je_for_source("Delivery Note", doc.name)


def on_expense_claim_submit(doc, method=None):
    """Expense Claim: parent.project header wins, fallback row-level."""
    # TIER 1 PERF: short-circuit during Misa migration — NKC already has these legs
    if getattr(frappe.flags, "misa_migration_active", False):
        return
    if doc.docstatus != 1:
        return
    override = doc.get("wip_override_account")
    if not override:
        return
    default = _get_settings_wip_account(doc.company)
    if not default or default == override:
        return

    parent_project = (doc.get("project") or "").strip()
    by_project: dict[str, float] = {}
    if parent_project:
        amt = flt(doc.total_claimed_amount or doc.grand_total)
        if amt > 0:
            by_project[parent_project] = amt
    else:
        for exp in (doc.expenses or []):
            row_proj = (exp.get("project") or "").strip()
            if not row_proj:
                continue
            by_project[row_proj] = by_project.get(row_proj, 0) + flt(exp.get("amount") or 0)

    if not by_project:
        return

    overrides = []
    for project, amount in by_project.items():
        if amount <= 0:
            continue
        _ensure_project_costing(project)
        overrides.append({
            "project": project,
            "default_account": default,
            "override_account": override,
            "amount": amount,
        })

    if overrides:
        _post_wip_override_je(
            company=doc.company,
            posting_date=doc.posting_date,
            src_dt="Expense Claim",
            src_name=doc.name,
            overrides=overrides,
        )


def on_expense_claim_cancel(doc, method=None):
    _cancel_je_for_source("Expense Claim", doc.name)
