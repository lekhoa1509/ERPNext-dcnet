from __future__ import annotations

import frappe


def ensure_bctc_mapping_for_company(doc, method):
    """Company.on_update hook — auto-create BCTC Mapping for VN companies."""
    if doc.country != "Vietnam":
        return

    mapping_name = f"BCTC Mapping {doc.name}"
    if frappe.db.exists("BCTC Mapping", mapping_name):
        return

    coa_template = _detect_coa_template(doc.name)
    _clone_template_to_company(doc.name, coa_template)


def _detect_coa_template(company: str) -> str:
    """Detect COA template by checking presence of manufacturing accounts.
    Returns 'vn_large_enterprise' if TK 621/622/627 (production cost) exist,
    else 'vn_small_trade' (DN nhỏ-vừa thương mại/dịch vụ — simpler ~30 lines).
    """
    from frappe.query_builder import DocType

    Account = DocType("Account")
    large_enterprise_indicators = ["621", "622", "627"]

    for prefix in large_enterprise_indicators:
        # Use both account_number AND name-prefix to handle COAs where
        # account_number is NULL (account name like "621 - ... - DC").
        by_num = (
            frappe.qb.from_(Account).select(Account.name)
            .where(Account.company == company)
            .where(Account.account_number.like(f"{prefix}%"))
            .limit(1).run()
        )
        by_name = (
            frappe.qb.from_(Account).select(Account.name)
            .where(Account.company == company)
            .where(Account.name.like(f"{prefix} -%"))
            .limit(1).run()
        )
        if by_num or by_name:
            return "vn_large_enterprise"

    return "vn_small_trade"


def _clone_template_to_company(company: str, coa_template: str) -> None:
    """Clone BCTC Mapping Template rows into a new per-company BCTC Mapping."""
    mapping = frappe.new_doc("BCTC Mapping")
    mapping.company = company
    mapping.coa_template = coa_template

    for report in ("b01", "b02", "b03"):
        template_name = f"{coa_template}_{report}"
        if not frappe.db.exists("BCTC Mapping Template", template_name):
            continue
        template = frappe.get_doc("BCTC Mapping Template", template_name)
        table_field = f"{report}_lines"
        for row in template.get(table_field) or []:
            mapping.append(table_field, row.as_dict())

    mapping.insert(ignore_permissions=True)
    frappe.db.commit()
