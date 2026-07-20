import importlib
from decimal import Decimal

import frappe

from vn_banking.match.base import BaseMatcher, MatchCandidate
from vn_banking.match.context import build_context
from vn_banking.match.helpers import get_txn_direction, get_txn_amount, get_txn_description
from vn_banking.match.party_extract import find_party_in_description


def instantiate_matcher(rule) -> BaseMatcher | None:
    mt = frappe.db.get_value("Bank Matcher Type", rule.rule_key,
                             ["handler_path", "default_confidence"], as_dict=True)
    if not mt:
        return None
    module_path, cls_name = mt.handler_path.rsplit(".", 1)
    mod = importlib.import_module(module_path)
    cls = getattr(mod, cls_name)
    matcher = cls(rule=rule)
    if not matcher.default_confidence:
        matcher.default_confidence = mt.default_confidence
    return matcher


def get_enabled_rules_in_priority_order():
    settings = frappe.get_single("Bank Statement Settings")
    return sorted(
        [r for r in settings.rules if r.enabled],
        key=lambda r: int(r.priority or 9999),
    )


def pick_best(candidates: list[MatchCandidate]) -> MatchCandidate:
    """Rank: High > Medium > Low; then smallest |difference|; then fewest invoices."""
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(
        candidates,
        key=lambda c: (order.get(c.confidence, 99), abs(c.difference), len(c.invoices)),
    )[0]


def apply_to_txn(txn, cand: MatchCandidate, rule):
    confidence = rule.confidence_override or cand.confidence
    txn.match_confidence = confidence
    txn.matched_by = cand.matched_by
    txn.suggested_party_type = cand.party_type
    txn.suggested_party = cand.party
    txn.difference_amount = float(cand.difference)
    txn.set("suggested_invoices", [])
    for inv in cand.invoices:
        txn.append("suggested_invoices", {
            "invoice_type": inv.doctype,
            "invoice_name": inv.name,
            "outstanding_amount": float(inv.outstanding),
            "allocated_amount": float(inv.allocated or inv.outstanding),
            "selected": 1,
        })


def run_match_engine(import_name: str):
    from datetime import date, timedelta
    from frappe.utils import getdate

    import_doc = frappe.get_doc("Bank Statement Import", import_name)
    settings = frappe.get_single("Bank Statement Settings")
    rules = get_enabled_rules_in_priority_order()

    # Guard None dates — user may upload a file without specifying a period.
    # Default to "last 90 days" window so invoice lookup has a sane range.
    from_date = getdate(import_doc.from_date) if import_doc.from_date else (date.today() - timedelta(days=90))
    to_date = getdate(import_doc.to_date) if import_doc.to_date else date.today()

    # Pre-build both directions once (credit + debit).
    ctx_credit = build_context(import_doc.bank_account, from_date, to_date,
                                direction="credit", settings=settings)
    ctx_debit = build_context(import_doc.bank_account, from_date, to_date,
                               direction="debit", settings=settings)

    txn_names = frappe.get_all("Bank Transaction",
                               filters={"bank_statement_import": import_name},
                               pluck="name")
    # FB-522 — preload candidate party names (independent of outstanding
    # invoices) for fuzzy fallback. Two pools by direction, queried once.
    company = ctx_credit.company
    customer_names = frappe.get_all("Customer",
                                    filters={"disabled": 0},
                                    pluck="name") or []
    supplier_names = frappe.get_all("Supplier",
                                    filters={"disabled": 0},
                                    pluck="name") or []
    matched = unmatched = 0
    for n in txn_names:
        txn = frappe.get_doc("Bank Transaction", n)
        direction = get_txn_direction(txn)
        ctx = ctx_credit if direction == "credit" else ctx_debit
        hit = False
        for rule in rules:
            if rule.bank_account and rule.bank_account != import_doc.bank_account:
                continue
            matcher = instantiate_matcher(rule)
            if matcher is None:
                continue
            if not matcher.applicable(txn, ctx):
                continue
            cands = matcher.match(txn, ctx)
            if cands:
                apply_to_txn(txn, pick_best(cands), rule)
                hit = True
                break  # first-hit-wins
        if not hit:
            txn.match_confidence = "None"
            txn.matched_by = "None"
            # FB-522 fallback — even without an invoice match, surface
            # the party if its name appears in the description. Keeps
            # match_confidence=None (no invoice) but populates
            # suggested_party so the user sees the link.
            desc = get_txn_description(txn)
            if desc and not txn.suggested_party:
                pool = customer_names if direction == "credit" else supplier_names
                found = find_party_in_description(desc, pool, threshold=80)
                if found:
                    txn.suggested_party = found[0]
                    txn.suggested_party_type = "Customer" if direction == "credit" else "Supplier"
                    txn.matched_by = "NameOnly"
        txn.save(ignore_permissions=True)
        if hit:
            matched += 1
        else:
            unmatched += 1

    import_doc.matched_rows = matched
    import_doc.unmatched_rows = unmatched
    import_doc.status = "Parsed"
    import_doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"matched": matched, "unmatched": unmatched}
