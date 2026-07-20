"""Non-deductible expense helper — Pattern A (per-voucher tag).

Cross-cutting helper used by:
- Phase 1: dcnet_pakd.integrations.accounting (post_beneficiary_je, post_journal_entry)
- Phase 2: PI/EC/Asset/Payroll source-doc on_submit propagation hooks
- Phase 3: Form 03/TNDN B4 aggregation, B09 reconciliation

Spec: apps/vn_accounting/docs/specs/2026-05-25-non-deductible-expense-tracking.md
"""
from __future__ import annotations

REASON_NO_INVOICE = "Không HĐ hợp lệ"
REASON_OVER_LIMIT = "Vượt định mức quy định"
REASON_NOT_SXKD = "Không liên quan SXKD"
REASON_PENALTY = "Tiền phạt (thuế / BHXH / hợp đồng)"
REASON_RELATED_PARTY = "Related-party không TP doc"
REASON_OTHER = "Khác"

VALID_REASONS = {
	REASON_NO_INVOICE,
	REASON_OVER_LIMIT,
	REASON_NOT_SXKD,
	REASON_PENALTY,
	REASON_RELATED_PARTY,
	REASON_OTHER,
}


def mark_non_deductible(row, reason: str) -> None:
	"""Mark a child row (JE Account / PI Item / EC Detail / Salary Detail) as non-deductible.

	Idempotent — calling with same reason twice is a no-op.
	Caller is responsible for picking a reason that fits the schema's Select options.
	"""
	if reason not in VALID_REASONS:
		raise ValueError(f"Invalid non-deductible reason: {reason!r}. Allowed: {sorted(VALID_REASONS)}")
	row.is_non_deductible = 1
	row.non_deductible_reason = reason


def is_marked(row) -> bool:
	"""True if row has the flag set (handles 0/1/None defensively)."""
	return bool(getattr(row, "is_non_deductible", 0))


def get_reason(row) -> str:
	"""Return the reason string (empty if not flagged)."""
	return getattr(row, "non_deductible_reason", "") or ""
