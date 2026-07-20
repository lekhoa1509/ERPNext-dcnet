"""Markup price calculation — 6 methods per BL §5.

Pure functions. No frappe.throw / no side effects. Bad inputs → return 0.
Validation lives in Stage controller; engine just computes.

Methods:
  coefficient         : cost * hệ_số (vd cost × 1.5)
  percent_cost        : cost * (1 + percent/100)  (vd +30% ⇒ × 1.30)
  fixed_amount        : markup_value (KTT input)
  from_contract       : markup_value (KTT đọc từ contract value/phụ lục)
  percent_contract    : contract_value * percent/100  (vd 30% của HĐ khung)
  cost_to_date_uplift : cost * (1 + percent/100)  (giống percent_cost nhưng
                        ngữ nghĩa khác — "nghiệm thu giữa kỳ theo cost-to-date")
"""
from __future__ import annotations

import frappe
from frappe.utils import flt


MARKUP_METHODS = (
    "Coefficient",
    "Percent on Cost",
    "Fixed Amount",
    "From Contract",
    "Percent of Contract",
    "Cost-to-Date Uplift",
)


def calculate_price(
    *,
    method: str,
    markup_value: float | None = 0,
    cost_pinned: float | None = 0,
    parent_costing: str | None = None,
) -> float:
    """Return suggested price for a stage. Pure function — never raises.

    method        : one of MARKUP_METHODS (case-sensitive)
    markup_value  : interpretation depends on method (see module docstring)
    cost_pinned   : sum of pinned cost on this stage (for cost-based methods)
    parent_costing: Project Costing name — needed for contract-based methods
    """
    cost = flt(cost_pinned)
    mv = flt(markup_value)

    if method == "Coefficient":
        return round(cost * mv, 2)
    if method == "Percent on Cost":
        return round(cost * (1 + mv / 100.0), 2)
    if method == "Fixed Amount":
        return round(mv, 2)
    if method == "From Contract":
        # KTT input directly via markup_value (e.g. số tiền lấy từ phụ lục)
        return round(mv, 2)
    if method == "Percent of Contract":
        contract_value = _resolve_contract_value(parent_costing)
        return round(contract_value * mv / 100.0, 2)
    if method == "Cost-to-Date Uplift":
        return round(cost * (1 + mv / 100.0), 2)
    return 0.0


def _resolve_contract_value(parent_costing: str | None) -> float:
    """Read contract.total_value from Project Costing.contract Link.

    Returns 0 if no contract linked or contract not found.
    """
    if not parent_costing:
        return 0
    contract = frappe.db.get_value("Project Costing", parent_costing, "contract")
    if not contract:
        return 0
    # DCNet Contract.total_value is the canonical field; fallback to grand_total
    # for compat with other contract DocTypes.
    val = frappe.db.get_value("DCNet Contract", contract, "total_value")
    if val is None:
        val = frappe.db.get_value("DCNet Contract", contract, "grand_total")
    return flt(val)
