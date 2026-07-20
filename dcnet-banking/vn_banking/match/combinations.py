from decimal import Decimal
from itertools import combinations

from vn_banking.match.base import InvoiceRef


def combinations_sum_match(invoices: list[InvoiceRef], target: Decimal,
                            tolerance: Decimal, max_k: int = 5) -> list[InvoiceRef]:
    """Find the smallest combination of invoices whose sum is approx target (within tolerance).
    Prefer smaller k, then earliest-name tiebreak.
    Returns the matched invoices, or [] if no combination found.
    """
    for k in range(1, min(max_k, len(invoices)) + 1):
        best = None
        for combo in combinations(invoices, k):
            s = sum((i.outstanding for i in combo), Decimal("0"))
            if abs(s - target) <= tolerance:
                if best is None or sorted(i.name for i in combo) < sorted(i.name for i in best):
                    best = list(combo)
        if best is not None:
            return best
    return []
