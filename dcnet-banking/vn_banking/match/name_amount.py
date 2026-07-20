from decimal import Decimal

from vn_banking.match.base import BaseMatcher, MatchCandidate
from vn_banking.match.helpers import get_txn_amount, get_txn_description


class NameAmountMatcher(BaseMatcher):
    key = "name_amount"
    label = "Fuzzy Name + Amount"
    default_confidence = "Low"

    RATIO_THRESHOLD = 80

    def applicable(self, txn, ctx) -> bool:
        return bool(get_txn_description(txn)) and bool(ctx.outstanding_invoices)

    def match(self, txn, ctx):
        from rapidfuzz import fuzz
        text = get_txn_description(txn).upper()
        txn_amount = get_txn_amount(txn)
        candidates = []
        for party, invs in ctx.outstanding_invoices.items():
            ratio = fuzz.partial_ratio(party.upper(), text)
            if ratio < self.RATIO_THRESHOLD:
                continue
            for inv in invs:
                if abs(inv.outstanding - txn_amount) <= ctx.tolerance:
                    candidates.append(MatchCandidate(
                        party_type=ctx.party_type, party=party, invoices=[inv],
                        total_allocated=inv.outstanding, difference=txn_amount - inv.outstanding,
                        confidence="Low", matched_by="Name+Amount",
                        explanation=f"Tên '{party}' gần khớp nội dung (ratio {ratio}%). Khớp {inv.name}. Cần xác nhận.",
                    ))
        return candidates
