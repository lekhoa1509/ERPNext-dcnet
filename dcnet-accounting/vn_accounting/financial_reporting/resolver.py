"""BCTC resolver engine — evaluate account formulas and line formulas for B01/B02/B03."""
from decimal import Decimal

import frappe
from frappe.utils import getdate


def resolve_bctc_line(company, line, period_start, period_end, resolved_cache=None):
    """Evaluate one BCTC Line for a given period, returning a Decimal value.

    Args:
        company: Company name
        line: dict or frappe._dict with BCTC Line fields (code, value_type,
              account_formula, line_formula)
        period_start: date — start of period
        period_end: date — end of period (= as-of date for balance-sheet lines)
        resolved_cache: dict[code -> Decimal] used for recursive line_formula evaluation

    Returns:
        Decimal value for the line.

    value_type meanings:
        closing_debit  — sum of debit balance at period_end for matching accounts
        closing_credit — sum of credit balance at period_end for matching accounts
        period_debit   — sum of debit movement DURING period_start..period_end
        period_credit  — sum of credit movement DURING period_start..period_end
        formula        — computed from line_formula referencing other line codes
    """
    if resolved_cache is None:
        resolved_cache = {}

    code = line.get("code") or ""
    value_type = line.get("value_type") or "closing_debit"

    if value_type == "formula":
        result = _resolve_line_formula(company, line, period_start, period_end, resolved_cache)
        if code:
            resolved_cache[code] = result
        return result

    account_formula = line.get("account_formula") or ""
    sign_multiplier = int(line.get("sign_multiplier") or 1)

    accounts = _parse_account_formula(account_formula)
    if not accounts:
        return Decimal(0)

    total = Decimal(0)
    for sign, pattern in accounts:
        amount = _query_gl_balance(company, pattern, value_type, period_start, period_end)
        total += sign * amount

    result = total * sign_multiplier
    if code:
        resolved_cache[code] = result
    return result


def _parse_account_formula(formula):
    """Parse '+TK1,+TK2,-TK3' syntax into list of (sign, pattern) tuples.

    Patterns can include SQL wildcard suffix like '511%'.
    """
    if not formula:
        return []
    parts = []
    for token in formula.replace(" ", "").split(","):
        if not token:
            continue
        if token.startswith("-"):
            sign = Decimal(-1)
            pattern = token[1:]
        elif token.startswith("+"):
            sign = Decimal(1)
            pattern = token[1:]
        else:
            sign = Decimal(1)
            pattern = token
        if pattern:
            parts.append((sign, pattern))
    return parts


def _query_gl_balance(company, pattern, value_type, period_start, period_end):
    """Query GL Entry for the given account pattern and value_type."""
    # Build LIKE clause
    like_pattern = pattern if "%" in pattern else f"{pattern}%"

    if value_type == "closing_debit":
        return _balance_as_of(company, like_pattern, period_end, side="debit")
    elif value_type == "closing_credit":
        return _balance_as_of(company, like_pattern, period_end, side="credit")
    elif value_type == "period_debit":
        return _period_movement(company, like_pattern, period_start, period_end, side="debit")
    elif value_type == "period_credit":
        return _period_movement(company, like_pattern, period_start, period_end, side="credit")
    elif value_type == "net_credit":
        # Signed: returns credit - debit (negative when account has Dr balance, e.g. 4211 with loss carryforward).
        return _signed_balance_as_of(company, like_pattern, period_end, side="credit")
    elif value_type == "net_debit":
        return _signed_balance_as_of(company, like_pattern, period_end, side="debit")
    elif value_type == "period_net":
        # Period net change: credit - debit during period. For revenue Cr-Dr=+net,
        # for expense Cr-Dr=-net. Use to compute LN trước thuế in one line.
        return _signed_period_movement(company, like_pattern, period_start, period_end)
    elif value_type == "delta_debit":
        # Change in closing Dr balance over period. Positive = asset grew (e.g.
        # AR/inventory increase → cash out). Use for B03 indirect-method
        # working-capital adjustments with sign=-1 to subtract from cash flow.
        return _delta_balance(company, like_pattern, period_start, period_end, side="debit")
    elif value_type == "delta_credit":
        # Change in closing Cr balance over period. Positive = liability grew
        # (e.g. AP increase → cash kept). Use for B03 with sign=+1 to add to
        # cash flow when liability builds up.
        return _delta_balance(company, like_pattern, period_start, period_end, side="credit")
    return Decimal(0)


def _balance_as_of(company, like_pattern, as_of_date, side):
    """Cumulative balance (debit or credit side) for accounts matching pattern, up to as_of_date."""
    rows = frappe.db.sql(
        """
        SELECT SUM(debit) AS total_debit, SUM(credit) AS total_credit
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND posting_date <= %(as_of_date)s
          AND is_cancelled = 0
          AND account LIKE %(pattern)s
        """,
        {"company": company, "as_of_date": as_of_date, "pattern": like_pattern},
        as_dict=True,
    )
    if not rows:
        return Decimal(0)
    row = rows[0]
    total_debit = Decimal(str(row.total_debit or 0))
    total_credit = Decimal(str(row.total_credit or 0))
    if side == "debit":
        return max(total_debit - total_credit, Decimal(0))
    else:
        return max(total_credit - total_debit, Decimal(0))


def _delta_balance(company, like_pattern, period_start, period_end, side):
    """Closing balance at period_end MINUS closing balance at (period_start - 1 day).
    Returns signed delta:
      side='debit': returns Dr balance change (Dr_end - Dr_start). Positive = asset/expense grew.
      side='credit': returns Cr balance change (Cr_end - Cr_start). Positive = liability/equity grew.
    Use for B03 indirect-method working-capital lines (delta AR/HTK/AP/prepaid).
    """
    from frappe.utils import add_days, getdate
    start_minus_1 = add_days(getdate(period_start), -1)
    end_balance = _balance_as_of(company, like_pattern, period_end, side=side)
    start_balance = _balance_as_of(company, like_pattern, start_minus_1, side=side)
    return end_balance - start_balance


def _signed_balance_as_of(company, like_pattern, as_of_date, side):
    """Signed cumulative balance: (credit - debit) if side='credit', else (debit - credit).
    Can be negative — use for TKs that may have opposite-sign balance (e.g., loss carryforward 4211).
    """
    rows = frappe.db.sql(
        """
        SELECT SUM(debit) AS total_debit, SUM(credit) AS total_credit
        FROM `tabGL Entry`
        WHERE company = %(company)s
          AND posting_date <= %(as_of_date)s
          AND is_cancelled = 0
          AND account LIKE %(pattern)s
        """,
        {"company": company, "as_of_date": as_of_date, "pattern": like_pattern},
        as_dict=True,
    )
    if not rows:
        return Decimal(0)
    row = rows[0]
    total_debit = Decimal(str(row.total_debit or 0))
    total_credit = Decimal(str(row.total_credit or 0))
    return total_credit - total_debit if side == "credit" else total_debit - total_credit


def _signed_period_movement(company, like_pattern, period_start, period_end):
    """Signed period net: credit movement - debit movement during period.
    Revenue Cr-Dr = +net (positive). Expense Cr-Dr = -net (negative).
    Use to compute period P&L in a single line with mixed revenue+expense TKs.

    Excludes:
      - Period Closing Voucher (ERPNext core year-end close)
      - Journal Entries marked `vn_is_period_closing=1` (VN Period Close
        monthly/quarterly close + Misa "Kết chuyển lãi lỗ" NKC vouchers)
    """
    rows = frappe.db.sql(
        """
        SELECT SUM(gle.debit) AS total_debit, SUM(gle.credit) AS total_credit
        FROM `tabGL Entry` gle
        LEFT JOIN `tabJournal Entry` je ON je.name = gle.voucher_no
            AND gle.voucher_type = 'Journal Entry'
        WHERE gle.company = %(company)s
          AND gle.posting_date BETWEEN %(from_date)s AND %(to_date)s
          AND gle.is_cancelled = 0
          AND gle.voucher_type != 'Period Closing Voucher'
          AND COALESCE(je.vn_is_period_closing, 0) = 0
          AND gle.account LIKE %(pattern)s
        """,
        {"company": company, "from_date": period_start, "to_date": period_end, "pattern": like_pattern},
        as_dict=True,
    )
    if not rows:
        return Decimal(0)
    row = rows[0]
    total_debit = Decimal(str(row.total_debit or 0))
    total_credit = Decimal(str(row.total_credit or 0))
    return total_credit - total_debit


def _period_movement(company, like_pattern, period_start, period_end, side):
    """Total movement (debit or credit) during the period for matching accounts.

    Excludes:
      - Period Closing Voucher (ERPNext core year-end close)
      - JE flagged vn_is_period_closing=1 (VN Period Close / Misa Kết chuyển)
    """
    rows = frappe.db.sql(
        """
        SELECT SUM(gle.debit) AS total_debit, SUM(gle.credit) AS total_credit
        FROM `tabGL Entry` gle
        LEFT JOIN `tabJournal Entry` je ON je.name = gle.voucher_no
            AND gle.voucher_type = 'Journal Entry'
        WHERE gle.company = %(company)s
          AND gle.posting_date BETWEEN %(from_date)s AND %(to_date)s
          AND gle.is_cancelled = 0
          AND gle.voucher_type != 'Period Closing Voucher'
          AND COALESCE(je.vn_is_period_closing, 0) = 0
          AND gle.account LIKE %(pattern)s
        """,
        {"company": company, "from_date": period_start,
         "to_date": period_end, "pattern": like_pattern},
        as_dict=True,
    )
    if not rows:
        return Decimal(0)
    row = rows[0]
    if side == "debit":
        return Decimal(str(row.total_debit or 0))
    else:
        return Decimal(str(row.total_credit or 0))


def _resolve_line_formula(company, line, period_start, period_end, resolved_cache):
    """Evaluate a line_formula like '=10+11-12' where 10/11/12 are line codes."""
    formula = (line.get("line_formula") or "").strip()
    if not formula.startswith("="):
        return Decimal(0)

    expr = formula[1:]  # strip leading '='
    # Tokenize: split by + and - keeping sign
    import re
    tokens = re.split(r"([+\-])", expr)

    total = Decimal(0)
    sign = Decimal(1)
    for tok in tokens:
        tok = tok.strip()
        if tok == "+":
            sign = Decimal(1)
        elif tok == "-":
            sign = Decimal(-1)
        elif tok:
            code = tok
            if code in resolved_cache:
                total += sign * resolved_cache[code]
            # else: code not yet resolved — skip (caller should resolve in order)
    return total


def resolve_all_lines(company, lines, period_start, period_end):
    """Resolve all BCTC lines, returning list of (line, value) pairs.

    Formula lines may have arbitrary depth (270 → 100/200, 100 → 110/120/…).
    Strategy: resolve account-based lines once, then iterate formula
    resolution until no value changes (fixpoint).
    """
    resolved_cache = {}
    results = []
    formula_indices = []

    # Pass 1: account-based lines (their values never change)
    for line in lines:
        if (line.get("value_type") or "closing_debit") != "formula":
            value = resolve_bctc_line(company, line, period_start, period_end, resolved_cache)
            results.append((line, value))
        else:
            results.append((line, Decimal(0)))  # zero placeholder; will refine
            formula_indices.append(len(results) - 1)

    # Pass 2: iterate formula resolution until fixpoint (safety cap 20 iters)
    for _ in range(20):
        changed = False
        for i in formula_indices:
            line, old_value = results[i]
            new_value = resolve_bctc_line(
                company, line, period_start, period_end, resolved_cache
            )
            if new_value != old_value:
                results[i] = (line, new_value)
                changed = True
        if not changed:
            break

    return results
