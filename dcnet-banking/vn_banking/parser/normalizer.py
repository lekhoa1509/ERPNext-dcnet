import hashlib
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Optional


def parse_date(value, fmt: str) -> date:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if value is None or value == "":
        raise ValueError("empty date")
    return datetime.strptime(str(value).strip(), fmt).date()


def parse_amount(value, decimal_sep: str = ".", thousands_sep: str = ",") -> Decimal:
    """Parse a VN bank amount string. Empty / None -> Decimal('0')."""
    if value is None or value == "":
        return Decimal("0")
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))
    s = str(value).strip()
    if not s:
        return Decimal("0")
    # strip currency symbols and spaces
    s = re.sub(r"[^\d\-.,]", "", s)
    # remove thousands separator then normalize decimal separator to .
    if thousands_sep:
        s = s.replace(thousands_sep, "")
    if decimal_sep != ".":
        s = s.replace(decimal_sep, ".")
    try:
        return Decimal(s)
    except InvalidOperation:
        return Decimal("0")


def compute_dedupe_hash(txn_date: date, amount: Decimal, reference_number: str, description: str) -> str:
    """SHA-256 of normalized (date, amount, ref, description). Used as Bank Transaction.dedupe_hash."""
    payload = f"{txn_date.isoformat()}|{amount.quantize(Decimal('0.01'))}|{(reference_number or '').strip()}|{(description or '').strip()}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
