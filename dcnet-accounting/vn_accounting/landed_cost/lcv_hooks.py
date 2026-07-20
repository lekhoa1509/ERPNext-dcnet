"""Landed Cost Voucher hooks for VN-specific expense account auto-fill.

Hooks:
  before_validate → lcv_apply_default_expense_account: reads LCV Allocation Settings
    and fills missing expense_account on each charge row by matching expense_type.
  validate        → lcv_validate_import_vat_split: checks VAT split for import LCVs.
  on_submit       → lcv_create_inventory_split_je: creates a balancing JE per VAS
    TT99/2025 to move landed cost from the warehouse account (1561) to the
    designated landed-cost-inventory account (default 1562). Idempotent.
  on_cancel       → lcv_cancel_inventory_split_je: cancels the matching JE.

Whitelisted endpoints (used by public/js/landed_cost_voucher.js):
  get_lcv_expense_types — returns the seeded expense types for client-side
    auto-fill and import-row insertion.
  get_lcv_inventory_split_default — returns the Settings default + last-known
    JE link for a given LCV name.
"""
from __future__ import annotations

import frappe


@frappe.whitelist()
def get_lcv_expense_types() -> list[dict]:
    """Return all LCV Expense Type Settings rows for client-side use.

    Used by landed_cost_voucher.js to:
      - Auto-insert import-only rows when "Hàng nhập khẩu" is toggled on
      - Suggest expense_account when KTT types description in a charge row
    """
    settings = frappe.get_single("LCV Allocation Settings")
    return [
        {
            "expense_type_key": r.expense_type_key,
            "expense_type": r.expense_type,
            "default_expense_account": r.default_expense_account or "",
            "is_import_only": int(r.is_import_only or 0),
            "allocation_method": r.allocation_method or "Amount",
        }
        for r in (settings.expense_types or [])
    ]


# Keys treated as import-only (hidden when vn_is_import_lcv=0)
# Note: "import_vat_deductible" intentionally NOT in this set — VAT NK khấu trừ
# is handled via a separate Journal Entry (Dr 1331 / Cr 33312) created from a
# button on the LCV form. LCV mechanism cannot represent it correctly because
# LCV always capitalizes charges into inventory (Dr 156 / Cr X), but VAT NK
# khấu trừ must NOT increase inventory value per VAS.
_IMPORT_ONLY_KEYS = {
    "import_duty",
    "special_consumption_tax",
    "import_vat_non_deductible",
    "customs_fee",
    "container_demurrage",
    "customs_agent_fee",
}


def lcv_apply_default_expense_account(doc, method=None):
    """before_validate: fill missing expense_account from LCV Allocation Settings.

    Only fills when the row's expense_account is empty, so KTT manual overrides
    are never overwritten.
    """
    if not doc.get("taxes"):
        return

    # Build lookup table from Settings (keyed by expense_type label → account)
    settings = frappe.get_single("LCV Allocation Settings")
    label_to_account: dict[str, str] = {}
    for row in settings.expense_types or []:
        if row.default_expense_account:
            label_to_account[row.expense_type] = row.default_expense_account

    for charge in doc.taxes:
        if charge.expense_account:
            continue  # already set — respect manual entry
        account = label_to_account.get(charge.description or charge.expense_type or "")
        if account:
            charge.expense_account = account


def lcv_validate_import_vat_split(doc, method=None):
    """validate: sanity check on VAT NK (không khấu trừ) charge row.

    Only the non-deductible portion belongs in LCV. Deductible VAT NK is
    handled separately via JE (see helper.create_import_vat_deductible_je).
    """
    if not doc.get("vn_is_import_lcv"):
        return

    non_deductible_label = _get_expense_label("import_vat_non_deductible")
    if not non_deductible_label:
        return

    for charge in (doc.get("taxes") or []):
        desc = (getattr(charge, "description", None) or "").strip()
        if desc == non_deductible_label and flt(getattr(charge, "amount", 0)) < 0:
            frappe.throw(
                frappe._("VAT nhập khẩu không khấu trừ phải ≥ 0. Vui lòng kiểm tra lại dòng chi phí.")
            )


@frappe.whitelist()
def create_import_vat_deductible_je(
    lcv_name: str, deductible_amount: float, posting_date: str | None = None
) -> str:
    """Create a draft Journal Entry for VAT NK khấu trừ.

    GL: Dr 1331 (VAT khấu trừ) / Cr 33312 (VAT NK phải nộp)

    Called from the LCV form's "Tạo phiếu VAT NK khấu trừ" button. KTT enters
    the deductible amount in a dialog; this endpoint validates + creates the JE
    in draft so KTT can review + submit.

    Returns: name of created Journal Entry.
    """
    deductible_amount = flt(deductible_amount)
    if deductible_amount <= 0:
        frappe.throw(frappe._("Số tiền VAT NK khấu trừ phải > 0."))

    lcv = frappe.get_doc("Landed Cost Voucher", lcv_name)
    if not lcv.get("vn_is_import_lcv"):
        frappe.throw(frappe._("Chỉ áp dụng cho phiếu phân bổ với 'Hàng nhập khẩu' = ✓."))

    company = lcv.company
    deductible_account = frappe.db.get_value(
        "Account",
        {"account_number": "1331", "company": company, "is_group": 0},
        "name",
    )
    payable_account = frappe.db.get_value(
        "Account",
        {"account_number": "33312", "company": company, "is_group": 0},
        "name",
    )
    if not deductible_account or not payable_account:
        frappe.throw(
            frappe._("Không tìm thấy TK 1331 hoặc 33312 cho Công ty {0}. Kiểm tra Hệ thống tài khoản.").format(company)
        )

    je = frappe.new_doc("Journal Entry")
    je.company = company
    je.posting_date = posting_date or lcv.posting_date or frappe.utils.nowdate()
    je.voucher_type = "Journal Entry"
    je.user_remark = frappe._("VAT NK khấu trừ từ phiếu phân bổ chi phí mua hàng {0}").format(lcv_name)
    je.append(
        "accounts",
        {
            "account": deductible_account,
            "debit_in_account_currency": deductible_amount,
            "user_remark": frappe._("VAT NK khấu trừ — LCV {0}").format(lcv_name),
        },
    )
    je.append(
        "accounts",
        {
            "account": payable_account,
            "credit_in_account_currency": deductible_amount,
            "user_remark": frappe._("VAT NK phải nộp — LCV {0}").format(lcv_name),
        },
    )
    je.insert(ignore_permissions=True)
    from vn_accounting.auto_source import register
    register("Journal Entry", je.name, "vn_accounting.lcv_vat_deductible",
             registered_by="vn_accounting.landed_cost.lcv_hooks")
    return je.name


# ── helpers ──────────────────────────────────────────────────────────────────

def _get_expense_label(expense_type_key: str) -> str:
    """Look up the expense_type label for a given key from Settings."""
    try:
        settings = frappe.get_single("LCV Allocation Settings")
        for row in settings.expense_types or []:
            if row.expense_type_key == expense_type_key:
                return row.expense_type
    except Exception:
        pass
    return ""


def flt(val) -> float:
    """Safe float conversion — avoids importing from frappe.utils in hooks."""
    try:
        return float(val or 0)
    except (TypeError, ValueError):
        return 0.0


# ── inventory-split JE (VAS TT99/2025) ──────────────────────────────────────

# Marker prefix embedded in JE.user_remark for idempotency + cancel lookup.
# Must contain the LCV name; SQL LIKE search uses this exact format.
_INV_SPLIT_MARKER = "LCV-INV-SPLIT"


def _inv_split_marker(lcv_name: str) -> str:
    return f"[{_INV_SPLIT_MARKER}:{lcv_name}]"


def lcv_create_inventory_split_je(doc, method=None):
    """on_submit: create + submit a balancing JE that moves landed cost from
    the warehouse account (1561) to the designated landed-cost-inventory
    account (default 1562) per VAS TT99/2025.

    GL after the bù JE:
      Dr <landed_cost_inventory_account per row, fallback header, fallback Settings>  [+landed cost]
      Cr <warehouse account of Items>  [-landed cost]
    Net: original LCV's Dr 1561 is offset by the bù Cr 1561, and Dr 1562 grows
    by total landed cost — matching VAS sub-account semantics.

    Idempotent: skips if a JE with the LCV marker already exists in non-cancelled
    state. Posts the JE name back as a Comment on the LCV with a clickable link.
    """
    if doc.docstatus != 1:
        return
    if not _is_inv_split_enabled():
        return
    if not doc.get("items"):
        return
    if not doc.get("taxes"):
        return  # nothing to allocate

    # Idempotency
    if _find_inv_split_je(doc.name):
        return

    # Resolve TK đích (Dr) per charge row, fallback to header, fallback to Settings.
    header_inv_acc = (
        getattr(doc, "landed_cost_inventory_account", None)
        or _settings_default_inventory_account(doc.company)
    )
    if not header_inv_acc:
        # No target configured — skip gracefully (don't break LCV submit).
        frappe.msgprint(
            frappe._(
                "Bỏ qua bút toán bù phụ phí: chưa cấu hình TK 1562 cho Công ty {0}. "
                "Mở 'LCV Allocation Settings' để thiết lập."
            ).format(doc.company),
            indicator="orange",
            alert=True,
        )
        return

    # Group landed cost by Dr account (per-row override or header default).
    dr_buckets: dict[str, float] = {}
    for charge in doc.get("taxes") or []:
        amount = flt(getattr(charge, "amount", 0))
        if amount <= 0:
            continue
        inv_acc = getattr(charge, "landed_cost_inventory_account", None) or header_inv_acc
        dr_buckets[inv_acc] = dr_buckets.get(inv_acc, 0) + amount

    total_landed = sum(dr_buckets.values())
    if total_landed <= 0:
        return

    # Cr side: aggregate by warehouse account of each Item, scaled by
    # applicable_charges (ERPNext distributes total_taxes_and_charges per Item).
    cr_buckets: dict[str, float] = {}
    items_total_charges = sum(flt(it.applicable_charges or 0) for it in doc.items)
    if items_total_charges <= 0:
        # Fallback: split equally across items (rare — usually applicable_charges is set)
        per_item = total_landed / len(doc.items)
        item_shares = [(it, per_item) for it in doc.items]
    else:
        # Scale so that sum of item shares == total_landed (handle rounding drift)
        item_shares = [
            (it, total_landed * flt(it.applicable_charges) / items_total_charges)
            for it in doc.items
        ]

    for item_row, share in item_shares:
        if share <= 0:
            continue
        wh_acc = _resolve_warehouse_account(item_row, doc.company)
        if not wh_acc:
            continue
        cr_buckets[wh_acc] = cr_buckets.get(wh_acc, 0) + share

    # Drift fix: round to 2 dp and force Σ Cr == Σ Dr (move difference into largest bucket)
    dr_buckets = {k: round(v, 2) for k, v in dr_buckets.items()}
    cr_buckets = {k: round(v, 2) for k, v in cr_buckets.items()}
    dr_total = round(sum(dr_buckets.values()), 2)
    cr_total = round(sum(cr_buckets.values()), 2)
    drift = round(dr_total - cr_total, 2)
    if drift and cr_buckets:
        largest = max(cr_buckets, key=cr_buckets.get)
        cr_buckets[largest] = round(cr_buckets[largest] + drift, 2)

    # Skip no-op JE when Dr and Cr land on the same accounts with same amounts
    # (e.g. unmigrated tenant where inventory account == warehouse account, both
    # are still flat TK 156).
    net = {k: dr_buckets.get(k, 0) - cr_buckets.get(k, 0) for k in set(dr_buckets) | set(cr_buckets)}
    if all(abs(v) < 0.01 for v in net.values()):
        return

    # Build + submit JE
    je = frappe.new_doc("Journal Entry")
    je.posting_date = doc.posting_date
    je.company = doc.company
    je.voucher_type = "Journal Entry"
    je.user_remark = (
        f"{_inv_split_marker(doc.name)} "
        + frappe._("Bút toán bù phụ phí mua hàng theo VAS TT99/2025 từ {0}").format(doc.name)
    )
    for acc, amount in dr_buckets.items():
        if amount <= 0:
            continue
        je.append("accounts", {
            "account": acc,
            "debit_in_account_currency": amount,
            "reference_type": "Landed Cost Voucher",
            "reference_name": doc.name,
            "user_remark": frappe._("Phụ phí mua hàng — LCV {0}").format(doc.name),
        })
    for acc, amount in cr_buckets.items():
        if amount <= 0:
            continue
        je.append("accounts", {
            "account": acc,
            "credit_in_account_currency": amount,
            "reference_type": "Landed Cost Voucher",
            "reference_name": doc.name,
            "user_remark": frappe._("Đảo phụ phí khỏi TK kho — LCV {0}").format(doc.name),
        })

    je.flags.ignore_permissions = True
    je.insert()
    je.submit()

    # Add comment on LCV with clickable JE link
    je_link = f'<a href="/app/journal-entry/{je.name}">{je.name}</a>'
    doc.add_comment(
        comment_type="Info",
        text=frappe._("Đã tạo Bút toán bù phụ phí (VAS TT99/2025): {0}").format(je_link),
    )


def lcv_cancel_inventory_split_je(doc, method=None):
    """on_cancel: cancel the matching bù JE if present."""
    je_name = _find_inv_split_je(doc.name, include_cancelled=False)
    if not je_name:
        return
    je = frappe.get_doc("Journal Entry", je_name)
    if je.docstatus == 1:
        je.flags.ignore_permissions = True
        je.cancel()
        doc.add_comment(
            comment_type="Info",
            text=frappe._("Đã hủy Bút toán bù phụ phí kèm theo: {0}").format(je_name),
        )


def _is_inv_split_enabled() -> bool:
    try:
        return bool(int(
            frappe.db.get_single_value("LCV Allocation Settings", "auto_create_inventory_split_je") or 0
        ))
    except Exception:
        return True  # default ON if Settings unavailable


def _settings_default_inventory_account(company: str) -> str | None:
    """Settings field stores account NAME (Link), already company-scoped at form
    save time. Verify it still belongs to the LCV's company; fallback otherwise.
    """
    try:
        acc = frappe.db.get_single_value(
            "LCV Allocation Settings", "default_landed_cost_inventory_account"
        )
    except Exception:
        acc = None
    if acc and frappe.db.get_value("Account", acc, "company") == company:
        return acc
    # Fallback: probe TK 1562 for this company
    return frappe.db.get_value(
        "Account",
        {"account_number": "1562", "company": company, "is_group": 0},
        "name",
    )


def _resolve_warehouse_account(item_row, company: str) -> str | None:
    """Return the GL account used by ERPNext for the warehouse of an LCV Item row.

    Lookup order: Warehouse.account → Company.default_inventory_account.
    """
    wh = getattr(item_row, "warehouse", None) or getattr(item_row, "to_warehouse", None)
    if wh:
        wh_acc = frappe.db.get_value("Warehouse", wh, "account")
        if wh_acc:
            return wh_acc
    return frappe.db.get_value("Company", company, "default_inventory_account")


def _find_inv_split_je(lcv_name: str, include_cancelled: bool = False) -> str | None:
    """Find the bù JE for an LCV via marker in user_remark."""
    marker = _inv_split_marker(lcv_name)
    filters = {"user_remark": ["like", f"%{marker}%"]}
    if not include_cancelled:
        filters["docstatus"] = ["!=", 2]
    return frappe.db.get_value("Journal Entry", filters, "name")


@frappe.whitelist()
def get_lcv_inventory_split_default(company: str | None = None) -> dict:
    """Return the Settings default + auto-create flag for a company.

    Used by landed_cost_voucher.js to pre-fill the header field on new LCVs.
    """
    if not company:
        return {"default_account": None, "auto_create": False}
    return {
        "default_account": _settings_default_inventory_account(company),
        "auto_create": _is_inv_split_enabled(),
    }
