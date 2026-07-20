from decimal import Decimal


def get_txn_amount(txn) -> Decimal:
    """Absolute transaction amount -- works whether txn is a Document or a dict."""
    deposit = _get(txn, "deposit") or 0
    withdrawal = _get(txn, "withdrawal") or 0
    return Decimal(str(deposit)) if deposit else Decimal(str(withdrawal))


def get_txn_direction(txn) -> str:
    deposit = _get(txn, "deposit") or 0
    return "credit" if Decimal(str(deposit)) > 0 else "debit"


def get_txn_bank_ref(txn) -> str:
    return _get(txn, "reference_number") or ""


def get_txn_description(txn) -> str:
    return _get(txn, "description") or ""


def is_txn_matched(txn) -> bool:
    return _get(txn, "match_confidence") in ("High", "Medium", "Low")


def _get(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)
