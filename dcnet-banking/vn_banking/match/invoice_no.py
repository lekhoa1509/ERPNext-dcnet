import re
from decimal import Decimal

from vn_banking.match.base import BaseMatcher, MatchCandidate, InvoiceRef
from vn_banking.match.helpers import get_txn_amount, get_txn_description


class InvoiceNoMatcher(BaseMatcher):
    key = "invoice_no"
    label = "Invoice No in Narration"
    default_confidence = "High"

    def applicable(self, txn, ctx) -> bool:
        return bool(get_txn_description(txn))

    def match(self, txn, ctx) -> list[MatchCandidate]:
        text = get_txn_description(txn)
        patterns = self._get_patterns(ctx)
        hits: set[str] = set()
        for pat in patterns:
            try:
                for m in re.finditer(pat, text, flags=re.IGNORECASE):
                    hits.add(m.group(0))
            except re.error:
                continue
        if not hits:
            return []

        # Lookup each hit in the outstanding_invoices map (flat scan since we don't have name→party index)
        found: dict[str, list[InvoiceRef]] = {}  # party → invoices
        for party, invs in ctx.outstanding_invoices.items():
            for inv in invs:
                if inv.name in hits or any(h.upper() in inv.name.upper() for h in hits):
                    found.setdefault(party, []).append(inv)

        candidates: list[MatchCandidate] = []
        txn_amount = get_txn_amount(txn)
        for party, invs in found.items():
            total = sum((i.outstanding for i in invs), Decimal("0"))
            diff = abs(total - txn_amount)
            if diff == 0:
                confidence = "High"
            elif diff <= ctx.tolerance:
                confidence = "Medium"
            else:
                confidence = "Low"
            candidates.append(MatchCandidate(
                party_type=ctx.party_type,
                party=party,
                invoices=invs,
                total_allocated=total,
                difference=txn_amount - total,
                confidence=confidence,
                matched_by="Invoice No",
                explanation=f"Tìm thấy {', '.join(sorted(hits))} trong nội dung giao dịch. "
                            f"Tổng {len(invs)} hoá đơn = {total}, chênh lệch {diff}.",
            ))
        return candidates

    def _get_patterns(self, ctx) -> list[str]:
        raw = (ctx.settings.invoice_number_patterns or "") if ctx.settings else ""
        return [line.strip() for line in raw.splitlines() if line.strip()]
