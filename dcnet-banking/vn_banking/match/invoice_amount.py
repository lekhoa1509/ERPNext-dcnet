from decimal import Decimal

from vn_banking.match.base import BaseMatcher, MatchCandidate
from vn_banking.match.helpers import get_txn_amount


class InvoiceAmountMatcher(BaseMatcher):
    key = "invoice_amount"
    label = "Unique Outstanding Amount"
    default_confidence = "Medium"

    def applicable(self, txn, ctx) -> bool:
        return get_txn_amount(txn) > 0

    def match(self, txn, ctx):
        txn_amount = get_txn_amount(txn)
        hits = []  # (party, invoice)
        for party, invs in ctx.outstanding_invoices.items():
            for inv in invs:
                if abs(inv.outstanding - txn_amount) <= ctx.tolerance:
                    hits.append((party, inv))
        if len(hits) != 1:
            return []
        party, inv = hits[0]
        return [MatchCandidate(
            party_type=ctx.party_type,
            party=party,
            invoices=[inv],
            total_allocated=inv.outstanding,
            difference=txn_amount - inv.outstanding,
            confidence="Medium",
            matched_by="Invoice+Amount",
            explanation=f"Khớp duy nhất với {inv.name} theo số tiền còn nợ {inv.outstanding}.",
        )]
