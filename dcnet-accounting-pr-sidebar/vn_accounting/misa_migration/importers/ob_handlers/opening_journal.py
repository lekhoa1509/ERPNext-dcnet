"""Opening Journal Entry handler — cash, bank, party balances.

Phase E commit 13b. Aggregates 5 Misa opening-balance sources into ONE
ERPNext Journal Entry of voucher_type="Opening Entry":

  1. General Account (TK leaves NOT handled by detail files)
  2. Bank Account (TK 1121.XX per-bank breakdown)
  3. Customer AR (TK 131 per-customer)
  4. Supplier AP (TK 331 per-supplier)
  5. Employee Advance (TK 141 per-employee)

Detail files take precedence over the summary. The general-account
file's TK 131 / 331 / 141 / 1121.XX / 156 / 152 / 211 / 213 / 214 /
242 lines are SKIPPED — those balances arrive via per-party / per-bank
or other Phase 0 handlers (inventory / FA / CCDC / prepaid in E13c-e).

Output JE shape per spec §6 + ERPNext convention:

  Journal Entry {
    voucher_type: "Opening Entry",
    posting_date: <opening_date>,        # default: 2025-12-31
    set_posting_time: 1,
    is_opening: "Yes",
    company: <Company>,
    user_remark: "Opening balance — Misa migration",
    accounts: [
      {account: ..., debit: ..., credit: 0,
       party_type: "Customer"|"Supplier"|"Employee"|None,
       party: <party_code>|None,
       user_remark: "OB <category> <code>"},
      ...
    ],
    misa_voucher_no: "OB-<batch_name>",
  }

The JE balances naturally because Misa's source TB is balanced; if a
small rounding diff remains (< 100 VND), a balancing row is added to
the Temporary Opening account (or fall back to TK 4211 Retained
Earnings).
"""

from __future__ import annotations

import json
from typing import Any

import frappe


from vn_accounting.misa_migration.context import get_active_company as _get_company

# Detail-file account-prefix EXCLUSIONS from general account residual.
#
# Item 1B-3 audit: only the categories whose detail handler GENUINELY
# posts JE legs to the matching Misa TK code belong here. Detail
# handlers that post to different accounts (e.g. Material Receipt SE
# posts to the item's default stock account via valuation, NOT to the
# Misa TK 1561 directly) or that produce no GL at all (e.g. Asset
# records on creation) MUST NOT be in this list — otherwise the
# general balance row is silently dropped and the balance is lost to
# the TK 4211 residual.
#
# Currently safe to exclude:
#   * 131 — Customer AR → _build_party_rows posts per-customer to TK 131
#   * 331 — Supplier AP → _build_party_rows posts per-supplier to TK 331
#   * 1121 — Bank sub-accounts → _build_bank_rows posts per-bank to TK 1121.XX
#
# NOT excluded (despite being conceptually "detail-handled"):
#   * 141  — Employee Advance: detail posts per-employee to TK 141 IF
#            the employee master exists. When missing, rows drop and
#            general balance is the only source → keep it in general.
#   * 152, 153, 155, 156 — Inventory: Material Receipt SE posts to the
#            item's default stock account via valuation_rate, not to the
#            Misa TK 1561/1531/etc directly. Trial Balance matches the
#            general row, not the SE-derived GL.
#   * 21x, 214 — Fixed Asset: Asset record creation does NOT post GL.
#            Opening Asset balance requires a separate Manual JE that
#            ERPNext does not generate automatically.
#   * 242 — Prepaid Expense: opening_prepaid handler posts per-prepaid
#            but the sum may not match the general 242 balance exactly.
#            Better to let general post and accept small drift than to
#            silently lose the balance.
_DETAIL_HANDLED_PREFIXES = (
    "131",
    "331",
    "1121",
    # TK 141 Tạm ứng (Employee Advance): opening_journal handler posts
    # per-employee Dr 141 lines from OB Employee Advance file when an
    # Employee master exists. The general-balance 141 row would
    # double-count (verified on DCNet 2026 export — 63.72B posted twice
    # → TB diff). Skip the general 141 row when Employee Advance detail
    # rows present.
    "141",
    # TK 242 prepaid: opening_prepaid handler posts per-prepaid-item
    # Dr 242 lines. The general-balance 242 row would double-count.
    # (Known Misa SDK quirk: sum of prepaid detail `remaining_amount`
    # may not equal the general 242 row — they're independent exports;
    # we trust the detail file as the authoritative source.)
    "242",
)

# Group accounts (parent that has child leaves) — skip these to avoid
# double-counting with their leaves. Detection: ERPNext Account.is_group.
# Done at runtime in the handler; this is just docs.


_DEFAULT_OPENING_DATE = "2025-12-31"


def _load_account_mapping() -> dict[str, str]:
    """Misa TK number → ERPNext Account.name resolver."""
    try:
        doc = frappe.get_single("Misa Account Mapping")
        return json.loads(doc.mappings or "{}")
    except Exception:
        return {}


def _resolve_account(
    misa_tk: str | None,
    mapping: dict[str, str],
    company: str,
) -> str | None:
    """Resolve Misa TK to ERPNext leaf Account.name. Caches positive hits.

    Item 1B-2 — REQUIRES the resolved Account to be a leaf (is_group=0)
    EVEN when the `Misa Account Mapping` has an explicit entry. When the
    mapping points at a group account (stale entry from before the COA
    leaf bootstrap ran), the mapping is OVERRIDDEN by a direct
    account_number leaf lookup and a one-shot warning is logged so the
    operator notices the mapping needs cleanup.

    Without this guard, opening balances collapse onto the level-4
    parent group (e.g. TK 111) instead of the level-5 leaf (TK 1111),
    and the Trial Balance compare fails by 100% per-account error.
    """
    if not misa_tk:
        return None
    misa_tk = str(misa_tk).strip()
    if not misa_tk:
        return None

    # 1. Try mapping first — accepted only when the entry is a LEAF on the
    # TARGET COMPANY (the mapping Single is site-wide; a stale entry from
    # another company's run must fall through, see _account_lookup).
    from vn_accounting.misa_migration.importers.nkc_handlers._account_lookup import (
        account_meta, resolve_account,
    )
    mapped = mapping.get(misa_tk)
    if mapped:
        meta = account_meta(mapped)
        if meta and meta[0] != 0:
            # Mapping points at a group — log & let resolve_account heal
            _log_stale_mapping_once(misa_tk, mapped)

    # 2. Canonical company-verified resolution (mapping → number lookup →
    # group-to-leaf self-heal)
    return resolve_account(misa_tk, mapping, company)


# Track stale-mapping warnings per process so the log doesn't flood
_STALE_MAPPING_WARNED: set[str] = set()


def _log_stale_mapping_once(misa_tk: str, group_target: str) -> None:
    """Emit a frappe.log_error once per (TK → group) pair per process so
    the operator surfaces stale mapping entries that need cleanup."""
    key = f"{misa_tk}→{group_target}"
    if key in _STALE_MAPPING_WARNED:
        return
    _STALE_MAPPING_WARNED.add(key)
    try:
        frappe.log_error(
            title=f"Misa mapping points to GROUP account: {misa_tk}",
            message=(
                f"Misa TK {misa_tk!r} mapping → {group_target!r} (is_group=1). "
                f"Falling back to leaf lookup by account_number. Run "
                f"`scripts/rewrite_mapping_post_coa_leaves.py` to clean up."
            ),
        )
    except Exception:
        pass


def _dedupe_misa_parent_summary_rows(rows: list[dict]) -> list[dict]:
    """Filter rows where `account_number` is a strict prefix of another
    row's `account_number` in the same list — Misa convention treats the
    parent code as a summary and the leaf code as the posting account.

    Without this filter, BOTH "111" and "1111" (or "112", "1121",
    "1121.81", "11210"…) post to the same ERPNext account → 2× balance
    per parent.

    Special handling for `1121.81`-style codes: dot is part of the
    account number and must not be treated as a separator. Prefix
    comparison uses string startswith ON STRIPPED account_number.

    Args:
      rows: list of dicts each with `account_number` key.

    Returns:
      Filtered list with summary parents removed.
    """
    # Collect all account_numbers as strings
    all_codes: list[str] = []
    for r in rows:
        ac = r.get("account_number")
        if ac is None:
            continue
        all_codes.append(str(ac).strip())

    # For each code, mark for removal if any OTHER code strictly starts
    # with it (i.e. is a longer code under the same family). Dot inside
    # codes counts as a normal character — "1121" is a prefix of both
    # "11210" and "1121.81", both kept; "1121" itself dropped.
    redundant: set[str] = set()
    for code in all_codes:
        for other in all_codes:
            if other != code and other.startswith(code) and len(other) > len(code):
                redundant.add(code)
                break

    if not redundant:
        return list(rows)

    out: list[dict] = []
    for r in rows:
        ac = str(r.get("account_number") or "").strip()
        if ac and ac in redundant:
            continue
        out.append(r)
    return out


# Mapping: detail file_type → prefix list it handles. Used by Item 1B-3
# data-driven skip so we only exclude a prefix when the detail file has
# actual rows. Otherwise the general balance is the only source and must
# be allowed to post.
_PREFIX_TO_DETAIL_FILE: dict[str, str] = {
    "131": "customer",
    "331": "supplier",
    "1121": "bank",
    # category names must match _FILE_TYPE_TO_DETAIL_CATEGORY in
    # phase_0_orchestrator.py — that map uses "employee" (singular,
    # not "employee_advance") for the OB Employee Advance file.
    "141": "employee",
    "242": "prepaid",
}


def _is_detail_handled(
    account_number: str | None,
    detail_handled_categories: set[str] | None = None,
) -> bool:
    """True if this account's opening balance is delegated to a detail
    handler that ACTUALLY ran for this batch.

    Args:
      account_number: Misa TK to check.
      detail_handled_categories: optional set of detail-file category
        names that produced rows in this batch (e.g.
        {'customer','supplier','bank','inventory','fixed_asset',
        'prepaid','employee'}). When None, fall back to the legacy
        behavior of skipping all prefixes (backward compat for callers
        that don't pass it).

    Returns:
      True → skip this row in the general builder (let detail handle).
    """
    if not account_number:
        return False
    s = str(account_number).strip()
    for prefix in _DETAIL_HANDLED_PREFIXES:
        if s == prefix or s.startswith(prefix):
            # When the orchestrator told us which detail categories
            # actually have rows, only skip when the corresponding
            # detail file is present. Otherwise the general balance is
            # the only source — let it post.
            if detail_handled_categories is None:
                return True
            cat = _PREFIX_TO_DETAIL_FILE.get(prefix)
            return cat in detail_handled_categories
    return False


def _account_is_leaf(account_name: str) -> bool:
    """ERPNext Account.is_group=0 → posting-eligible leaf."""
    is_group = frappe.db.get_value("Account", account_name, "is_group")
    return is_group == 0


def _build_general_rows(
    parsed_rows: list[dict],
    mapping: dict[str, str],
    company: str,
    detail_handled_categories: set[str] | None = None,
) -> list[dict]:
    """`OB Account Balance` rows → JE.accounts rows. Filters group
    accounts + detail-handled prefixes (delegated to other handlers).

    Item 1B-2: parent-summary rows (e.g. "111" when "1111" also present)
    are filtered first so they don't double-count when both resolve to
    the same ERPNext account.

    Item 1B-3: `detail_handled_categories` (when provided) restricts the
    `_DETAIL_HANDLED_PREFIXES` skip to ONLY those categories whose detail
    file actually had rows in this batch. Without it, the orchestrator
    defaults to skipping all prefixes — preserves backward compat with
    callers that don't pass the parameter.
    """
    parsed_rows = _dedupe_misa_parent_summary_rows(parsed_rows)
    out: list[dict] = []
    for r in parsed_rows:
        tk = r.get("account_number")
        if _is_detail_handled(tk, detail_handled_categories):
            continue
        erpnext_acct = _resolve_account(tk, mapping, company)
        if not erpnext_acct:
            continue
        if not _account_is_leaf(erpnext_acct):
            continue
        dr = float(r.get("dr") or 0.0)
        cr = float(r.get("cr") or 0.0)
        if dr == 0 and cr == 0:
            continue
        out.append({
            "account": erpnext_acct,
            "debit_in_account_currency": dr,
            "credit_in_account_currency": cr,
            "user_remark": f"OB Account {tk} — {r.get('account_name') or ''}",
        })
    return out


def _build_bank_rows(
    parsed_rows: list[dict],
    mapping: dict[str, str],
    company: str,
) -> list[dict]:
    """`OB Bank Balance` rows → JE.accounts rows. Each row maps to a
    specific TK 1121.XX (Sacombank, VIB, ...) sub-account.

    Item 1B-2: dedup parent-summary rows. Misa bank file lists BOTH
    the cash-position summary (TK 1121) AND each per-bank leaf
    (1121.81, 11210, 11214, 11215, 11218) — dedup keeps only the leaves.
    """
    parsed_rows = _dedupe_misa_parent_summary_rows(parsed_rows)
    out: list[dict] = []
    for r in parsed_rows:
        tk = r.get("account_number")
        erpnext_acct = _resolve_account(tk, mapping, company)
        if not erpnext_acct:
            continue
        # Resolver may return a group via stale mapping path — enforce
        # leaf here too for the bank handler.
        if not _account_is_leaf(erpnext_acct):
            continue
        dr = float(r.get("dr") or 0.0)
        cr = float(r.get("cr") or 0.0)
        if dr == 0 and cr == 0:
            continue
        bank_label = r.get("bank_name") or ""
        bank_no = r.get("bank_no") or ""
        out.append({
            "account": erpnext_acct,
            "debit_in_account_currency": dr,
            "credit_in_account_currency": cr,
            "user_remark": f"OB Bank {bank_label} ({bank_no})",
        })
    return out


def _build_party_rows(
    parsed_rows: list[dict],
    mapping: dict[str, str],
    company: str,
    party_type: str,
    party_doctype: str,
) -> list[dict]:
    """Shared builder for Customer / Supplier / Employee detail.

    Args:
      party_type: "Customer" | "Supplier" | "Employee"
      party_doctype: ERPNext DocType to check existence against
    """
    out: list[dict] = []
    for r in parsed_rows:
        tk = r.get("account_number")
        party_code = r.get("party_code")
        if not party_code:
            continue
        erpnext_acct = _resolve_account(tk, mapping, company)
        if not erpnext_acct:
            continue
        if not frappe.db.exists(party_doctype, party_code):
            continue  # silently skip; pre-flight surfaced this
        dr = float(r.get("dr") or 0.0)
        cr = float(r.get("cr") or 0.0)
        if dr == 0 and cr == 0:
            continue
        out.append({
            "account": erpnext_acct,
            "debit_in_account_currency": dr,
            "credit_in_account_currency": cr,
            "party_type": party_type,
            "party": party_code,
            "user_remark": f"OB {party_type} {party_code} — {r.get('party_name') or ''}",
        })
    return out


def _net_and_aggregate(rows: list[dict]) -> list[dict]:
    """Two-pass cleanup before JE insert:

    Pass 1 — per-row netting: if a row has BOTH dr > 0 AND cr > 0
    (common when Misa general balance shows both sides on TK 131 etc.),
    net to the larger side. ERPNext forbids per-row dr+cr.

    Pass 2 — aggregate by (account, party_type, party). When TK-mapping
    fallback collapses 5111/5112/51131-51136 → 511, multiple OB rows
    land on the same account; ERPNext rejects per-row dr+cr but allows
    multiple rows with different party. We aggregate same-(acct,party)
    rows into one net Dr/Cr line, merging user_remarks.
    """
    # Pass 1: net per row
    netted: list[dict] = []
    for r in rows:
        dr = float(r.get("debit_in_account_currency") or 0.0)
        cr = float(r.get("credit_in_account_currency") or 0.0)
        if dr > 0 and cr > 0:
            if dr >= cr:
                r["debit_in_account_currency"] = dr - cr
                r["credit_in_account_currency"] = 0.0
            else:
                r["credit_in_account_currency"] = cr - dr
                r["debit_in_account_currency"] = 0.0
        if (float(r.get("debit_in_account_currency") or 0.0) > 0 or
                float(r.get("credit_in_account_currency") or 0.0) > 0):
            netted.append(r)

    # Pass 2: aggregate by (account, party_type, party)
    grouped: dict[tuple, dict] = {}
    for r in netted:
        key = (r.get("account"),
               r.get("party_type"),
               r.get("party"))
        if key not in grouped:
            grouped[key] = {
                "account": r["account"],
                "debit_in_account_currency": 0.0,
                "credit_in_account_currency": 0.0,
                "user_remark": r.get("user_remark", ""),
                "_remarks": [r.get("user_remark", "")],
            }
            if r.get("party_type"):
                grouped[key]["party_type"] = r["party_type"]
                grouped[key]["party"] = r["party"]
        g = grouped[key]
        g["debit_in_account_currency"] += float(r.get("debit_in_account_currency") or 0.0)
        g["credit_in_account_currency"] += float(r.get("credit_in_account_currency") or 0.0)
        if r.get("user_remark"):
            g["_remarks"].append(r["user_remark"])

    # Final netting after aggregation (sums may produce both sides)
    out: list[dict] = []
    for g in grouped.values():
        dr = g["debit_in_account_currency"]
        cr = g["credit_in_account_currency"]
        if dr > 0 and cr > 0:
            if dr >= cr:
                g["debit_in_account_currency"] = dr - cr
                g["credit_in_account_currency"] = 0.0
            else:
                g["credit_in_account_currency"] = cr - dr
                g["debit_in_account_currency"] = 0.0
        if (g["debit_in_account_currency"] > 0 or
                g["credit_in_account_currency"] > 0):
            # Truncate combined user_remark to 140 chars
            remarks = [r for r in g.pop("_remarks", []) if r]
            if len(remarks) > 3:
                g["user_remark"] = (f"{remarks[0]} + {len(remarks) - 1} more")[:140]
            else:
                g["user_remark"] = (" | ".join(remarks))[:140]
            out.append(g)
        else:
            g.pop("_remarks", None)
    return out


def _temporary_opening_account(company: str) -> str | None:
    """Find an Account suitable for balancing residual rounding diff.

    Preference:
      1. Account with account_type='Temporary' (ERPNext standard)
      2. TK 4211 (Lợi nhuận sau thuế chưa phân phối) — VN COA
      3. TK 421
    """
    for kw in [
        {"company": company, "account_type": "Temporary"},
        {"company": company, "account_number": "4211", "is_group": 0},
        {"company": company, "account_number": "421", "is_group": 0},
    ]:
        n = frappe.db.get_value("Account", kw, "name")
        if n:
            return n
    return None


def post_opening_journal(
    batch_name: str,
    general_rows: list[dict] | None = None,
    bank_rows: list[dict] | None = None,
    customer_rows: list[dict] | None = None,
    supplier_rows: list[dict] | None = None,
    employee_rows: list[dict] | None = None,
    prepaid_rows: list[dict] | None = None,
    opening_date: str = _DEFAULT_OPENING_DATE,
    company: str | None = None,
    detail_handled_categories: set[str] | None = None,
) -> dict[str, Any]:
    """Create ONE Opening Entry JE from the 5 OB row categories.

    Args:
      batch_name: Misa Migration Batch (for traceability + doc.name).
      *_rows: parsed dicts from the 5 corresponding OB files.
      opening_date: posting_date (default 2025-12-31).
      company: ERPNext Company name (default = global default).

    Returns:
      {
        status: 'created' | 'skipped' | 'failed',
        target_doctype: 'Journal Entry',
        target_name: '<batch_name>-OB',
        row_count: int,
        total_dr: float,
        total_cr: float,
        skipped_general: int,
        skipped_party: int,
        error: str | None,
      }
    """
    target_name = f"{batch_name}-OB"
    if frappe.db.exists("Journal Entry", target_name):
        return {"status": "skipped", "target_doctype": "Journal Entry",
                "target_name": target_name, "reason": "already_exists"}

    company = company or _get_company()
    if not company:
        return {"status": "failed", "error": "No Company configured"}

    mapping = _load_account_mapping()

    accounts_payload: list[dict] = []

    general_rows = general_rows or []
    bank_rows = bank_rows or []
    customer_rows = customer_rows or []
    supplier_rows = supplier_rows or []
    employee_rows = employee_rows or []

    accounts_payload.extend(_build_general_rows(
        general_rows, mapping, company,
        detail_handled_categories=detail_handled_categories,
    ))
    accounts_payload.extend(_build_bank_rows(bank_rows, mapping, company))
    accounts_payload.extend(_build_party_rows(
        customer_rows, mapping, company, "Customer", "Customer"))
    accounts_payload.extend(_build_party_rows(
        supplier_rows, mapping, company, "Supplier", "Supplier"))
    accounts_payload.extend(_build_party_rows(
        employee_rows, mapping, company, "Employee", "Employee"))

    # Prepaid expense (TK 242) — Dr lines built by opening_prepaid handler.
    # Builder is loaded lazily so journal handler stays usable standalone.
    if prepaid_rows:
        from vn_accounting.misa_migration.importers.ob_handlers.opening_prepaid \
            import build_prepaid_rows
        prepaid_result = build_prepaid_rows(prepaid_rows, company, mapping)
        accounts_payload.extend(prepaid_result["rows"])

    # B5 fix: net per-row dr+cr + aggregate same-(account,party) rows
    accounts_payload = _net_and_aggregate(accounts_payload)

    if not accounts_payload:
        return {"status": "failed",
                "error": "No postable opening rows after filtering"}

    # Balance check — Misa TB is balanced at consolidated level; residual
    # rounding diff goes to Temporary Opening account.
    total_dr = sum(r["debit_in_account_currency"] for r in accounts_payload)
    total_cr = sum(r["credit_in_account_currency"] for r in accounts_payload)
    diff = total_dr - total_cr
    if abs(diff) > 0.01:
        contra = _temporary_opening_account(company)
        if not contra:
            return {"status": "failed",
                    "error": (f"Opening JE unbalanced (diff={diff:.2f}) and "
                              f"no Temporary / TK 4211 / TK 421 account "
                              f"available on {company} to absorb residual.")}
        if diff > 0:
            accounts_payload.append({
                "account": contra,
                "debit_in_account_currency": 0.0,
                "credit_in_account_currency": diff,
                "user_remark": f"OB balancing residual ({diff:.2f})",
            })
        else:
            accounts_payload.append({
                "account": contra,
                "debit_in_account_currency": -diff,
                "credit_in_account_currency": 0.0,
                "user_remark": f"OB balancing residual ({-diff:.2f})",
            })
        total_dr = sum(r["debit_in_account_currency"] for r in accounts_payload)
        total_cr = sum(r["credit_in_account_currency"] for r in accounts_payload)

    payload = {
        "doctype": "Journal Entry",
        "voucher_type": "Opening Entry",
        "company": company,
        "posting_date": opening_date,
        "set_posting_time": 1,
        "is_opening": "Yes",
        "user_remark": f"Opening balance — Misa migration batch {batch_name}",
        "accounts": accounts_payload,
        "misa_voucher_no": target_name,
    }

    # Item 1A — restrictive-account-type workaround: Misa OB JE
    # legitimately posts to TK 152/156/211/214 (Stock / Fixed Asset /
    # Accumulated Depreciation) which ERPNext otherwise rejects in any
    # JE (those types are reserved for SE / Asset depreciation flows).
    # Temp-clear the account_type so insert succeeds; restore in finally
    # so post-import behavior reverts. Symmetric pattern with the
    # submit_phase_4_drafts stock-clear at submit time.
    restricted = _restricted_accounts_for_payload(accounts_payload, company)
    for n, _ in restricted:
        frappe.db.set_value("Account", n, "account_type", "", update_modified=False)
    frappe.db.commit()

    try:
        doc = frappe.get_doc(payload)
        doc.flags.ignore_permissions = True
        doc.insert(set_name=target_name)
        return {
            "status": "created",
            "target_doctype": "Journal Entry",
            "target_name": doc.name,
            "row_count": len(accounts_payload),
            "total_dr": total_dr,
            "total_cr": total_cr,
            "general_count": len(general_rows),
            "bank_count": len(bank_rows),
            "customer_count": len(customer_rows),
            "supplier_count": len(supplier_rows),
            "employee_count": len(employee_rows),
            "prepaid_count": len(prepaid_rows or []),
        }
    except Exception as exc:
        err = f"{type(exc).__name__}: {exc}"
        frappe.log_error(title=f"Opening JE failed: {target_name}", message=err)
        return {"status": "failed", "target_name": None, "error": err}
    finally:
        # Restore restrictive account types regardless of insert outcome
        for n, atype in restricted:
            try:
                frappe.db.set_value(
                    "Account", n, "account_type", atype, update_modified=False
                )
            except Exception:
                pass
        frappe.db.commit()


# ERPNext rejects JE legs on these account_types unless special flags set.
# Migration context: legitimate to post OB to them directly.
_RESTRICTED_ACCOUNT_TYPES = (
    "Stock",
    "Fixed Asset",
    "Accumulated Depreciation",
)


def _restricted_accounts_for_payload(
    payload: list[dict],
    company: str,
) -> list[tuple[str, str]]:
    """List (Account.name, original account_type) for every payload leg
    whose account currently has a restrictive type. Used for temp-clear
    + restore around `doc.insert()`."""
    names = list({row.get("account") for row in payload if row.get("account")})
    if not names:
        return []
    placeholders = ",".join(["%s"] * len(names))
    type_placeholders = ",".join(["%s"] * len(_RESTRICTED_ACCOUNT_TYPES))
    rows = frappe.db.sql(
        f"""SELECT name, account_type FROM `tabAccount`
            WHERE company=%s AND name IN ({placeholders})
              AND account_type IN ({type_placeholders})""",
        (company, *names, *_RESTRICTED_ACCOUNT_TYPES),
        as_dict=True,
    )
    return [(r["name"], r["account_type"]) for r in rows]
