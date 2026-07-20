from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Iterator


@dataclass
class NormalizedTransaction:
    date: date
    deposit: Decimal         # money in, 0 if debit
    withdrawal: Decimal      # money out, 0 if credit
    description: str
    reference_number: str
    counter_account_no: str = ""
    counter_account_name: str = ""
    raw_row: dict = field(default_factory=dict)

    @property
    def amount(self) -> Decimal:
        return self.deposit if self.deposit > 0 else self.withdrawal

    @property
    def direction(self) -> str:
        return "credit" if self.deposit > 0 else "debit"


class BankDataSource(ABC):
    """Abstract source -- Excel file, bank API, MT940, CAMT053, etc."""
    key: str = ""
    label: str = ""
    requires_credentials: bool = False
    supports_pull: bool = False

    @abstractmethod
    def fetch(self, bank_account: str, from_date, to_date, context: dict) -> Iterator[NormalizedTransaction]:
        ...

    def validate_config(self, bank_account: str) -> list[str]:
        """Return list of error strings if config is invalid; empty list if OK."""
        return []
