from datetime import date
from decimal import Decimal
from typing import Iterator

import frappe

from vn_banking.source.base import BankDataSource, NormalizedTransaction
from vn_banking.parser.base import read_rows
from vn_banking.parser.normalizer import parse_amount, parse_date


def _col_index(header: list[str], col_name: str) -> int | None:
    """col_name may be a letter ('A') or a header text. Return 0-indexed column or None."""
    if not col_name:
        return None
    col_name = col_name.strip()
    # single-letter column (A, B, C, ...)
    if len(col_name) == 1 and col_name.isalpha():
        return ord(col_name.upper()) - ord("A")
    # match by header text (case-insensitive contains)
    target = col_name.lower()
    for i, h in enumerate(header):
        if target in str(h or "").strip().lower():
            return i
    return None


class ExcelFileSource(BankDataSource):
    key = "excel_upload"
    label = "Excel File Upload"
    requires_credentials = False
    supports_pull = False

    def fetch(self, bank_account, from_date, to_date, context) -> Iterator[NormalizedTransaction]:
        file_path = context["file_path"]
        format_name = context["format_name"]
        fmt = frappe.get_doc("Bank Statement Format", format_name)

        rows = list(read_rows(file_path, fmt.file_type, sheet_index=int(fmt.sheet_index or 0)))
        if not rows:
            return

        header_row = int(fmt.header_row or 1) - 1
        data_start = int(fmt.data_start_row or 2) - 1
        header = [str(c or "").strip() for c in rows[header_row]]

        idx_date = _col_index(header, fmt.col_date)
        idx_narr = _col_index(header, fmt.col_narration)
        idx_debit = _col_index(header, fmt.col_debit)
        idx_credit = _col_index(header, fmt.col_credit)
        idx_ref = _col_index(header, fmt.col_ref)
        idx_counter_no = _col_index(header, fmt.col_counter_account)
        idx_counter_name = _col_index(header, fmt.col_counter_name)

        if idx_date is None or idx_narr is None:
            raise ValueError(f"Format {format_name}: required columns not found in header")

        for r in rows[data_start:]:
            if not r or all((c is None or c == "") for c in r):
                continue
            raw_date = r[idx_date] if idx_date < len(r) else None
            if raw_date is None or raw_date == "":
                continue  # likely a footer row
            try:
                d = parse_date(raw_date, fmt.date_format or "%d/%m/%Y")
            except Exception:
                continue  # footer/subtotal rows
            deposit = parse_amount(
                r[idx_credit] if idx_credit is not None and idx_credit < len(r) else None,
                decimal_sep=fmt.decimal_separator or ".",
                thousands_sep=fmt.thousands_separator or ",",
            )
            withdrawal = parse_amount(
                r[idx_debit] if idx_debit is not None and idx_debit < len(r) else None,
                decimal_sep=fmt.decimal_separator or ".",
                thousands_sep=fmt.thousands_separator or ",",
            )
            if deposit == 0 and withdrawal == 0:
                continue
            narration = str(r[idx_narr] or "").strip()
            ref = str(r[idx_ref] or "").strip() if idx_ref is not None and idx_ref < len(r) else ""
            # PG Bank: "Số dư cuối ngày" rows have a balance but no ref
            if not ref and "số dư" in narration.lower():
                continue
            cno = str(r[idx_counter_no] or "").strip() if idx_counter_no is not None and idx_counter_no < len(r) else ""
            cname = str(r[idx_counter_name] or "").strip() if idx_counter_name is not None and idx_counter_name < len(r) else ""
            yield NormalizedTransaction(
                date=d,
                deposit=deposit,
                withdrawal=withdrawal,
                description=narration,
                reference_number=ref,
                counter_account_no=cno,
                counter_account_name=cname,
                raw_row={"row": list(r)},
            )
