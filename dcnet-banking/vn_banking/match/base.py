from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class InvoiceRef:
    doctype: str
    name: str
    outstanding: Decimal
    allocated: Decimal = Decimal("0")


@dataclass
class MatchCandidate:
    party_type: str
    party: str
    invoices: list[InvoiceRef] = field(default_factory=list)
    total_allocated: Decimal = Decimal("0")
    difference: Decimal = Decimal("0")
    confidence: str = "Medium"
    matched_by: str = ""
    explanation: str = ""


class BaseMatcher(ABC):
    key: str = ""
    label: str = ""
    default_confidence: str = "Medium"

    def __init__(self, rule=None):
        self.rule = rule  # Bank Match Rule child row (may carry overrides)

    @abstractmethod
    def applicable(self, txn, ctx) -> bool:
        ...

    @abstractmethod
    def match(self, txn, ctx) -> list[MatchCandidate]:
        ...
