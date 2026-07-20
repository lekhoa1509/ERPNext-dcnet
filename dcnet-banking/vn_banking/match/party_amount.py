from decimal import Decimal

from vn_banking.match.base import BaseMatcher, MatchCandidate
from vn_banking.match.combinations import combinations_sum_match
from vn_banking.match.helpers import get_txn_amount


class PartyAmountMatcher(BaseMatcher):
    key = "party_amount"
    label = "Party (by bank account) + Amount"
    default_confidence = "Medium"

    def applicable(self, txn, ctx) -> bool:
        counter = getattr(txn, "counter_account_no", None) or ""
        return bool(counter) and counter in ctx.party_by_bank_account

    def match(self, txn, ctx):
        counter = getattr(txn, "counter_account_no", "")
        party = ctx.party_by_bank_account.get(counter)
        if not party:
            return []
        invs = ctx.outstanding_invoices.get(party, [])
        if not invs:
            return []
        txn_amount = get_txn_amount(txn)
        # single invoice exact/tolerance
        for inv in invs:
            if abs(inv.outstanding - txn_amount) <= ctx.tolerance:
                return [MatchCandidate(
                    party_type=ctx.party_type, party=party, invoices=[inv],
                    total_allocated=inv.outstanding, difference=txn_amount - inv.outstanding,
                    confidence="Medium", matched_by="Party+Amount",
                    explanation=f"Party {party} theo số tài khoản đối ứng. Khớp hoá đơn {inv.name}.",
                )]
        # multi-invoice combo (if enabled)
        if ctx.settings and getattr(ctx.settings, "enable_multi_invoice_match", False):
            max_k = int(getattr(ctx.settings, "multi_invoice_max_combinations", 5) or 5)
            combo = combinations_sum_match(invs, txn_amount, ctx.tolerance, max_k=max_k)
            if combo:
                total = sum((i.outstanding for i in combo), Decimal("0"))
                names = ", ".join(i.name for i in combo)
                return [MatchCandidate(
                    party_type=ctx.party_type, party=party, invoices=list(combo),
                    total_allocated=total, difference=txn_amount - total,
                    confidence="Medium", matched_by="Party+Amount",
                    explanation=f"Party {party}. Gợi ý tổ hợp {len(combo)} hoá đơn: {names}.",
                )]
        return []
