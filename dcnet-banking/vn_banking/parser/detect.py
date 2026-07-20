import frappe
from vn_banking.parser.base import read_rows


def detect_format(file_path: str, file_type: str) -> str | None:
    """Match file against all Bank Statement Format entries. Return format_name or None.

    Scoring heuristic:
    1. Bank name appears in first 10 rows of the file → +10 points
    2. Each expected column position has non-empty content in header row → +1 point
    3. For text-based col_* values (not single letters), keyword presence in header → +2 points
    Returns the highest-scoring format, or None if no match.
    """
    candidates = frappe.get_all(
        "Bank Statement Format",
        filters={"file_type": file_type},
        fields=["name", "header_row", "data_start_row", "date_format",
                "col_date", "col_narration", "col_debit", "col_credit", "bank"],
    )
    if not candidates:
        return None

    rows = list(read_rows(file_path, file_type))
    if not rows:
        return None

    # Build text from first N rows for bank name matching
    early_text = " ".join(
        str(c or "") for row in rows[:min(10, len(rows))] for c in row
    ).lower()

    best = None
    best_score = -1

    for fmt in candidates:
        score = 0
        hr = int(fmt.header_row or 1) - 1  # 1-indexed → 0-indexed
        if hr >= len(rows):
            continue

        # Check 1: bank name appears in early rows
        bank_name = (fmt.bank or "").strip().lower()
        if bank_name and bank_name in early_text:
            score += 10

        # Check 2: header row columns
        header = rows[hr]
        for col_ref in [fmt.col_date, fmt.col_narration, fmt.col_debit, fmt.col_credit]:
            if not col_ref:
                continue
            col_ref = col_ref.strip()
            if len(col_ref) == 1 and col_ref.isalpha():
                # Column letter reference (A=0, B=1, ...) — check position has content
                idx = ord(col_ref.upper()) - ord("A")
                if idx < len(header) and header[idx] is not None and str(header[idx]).strip():
                    score += 1
            else:
                # Text-based column name — search in header text
                header_text = " | ".join(str(c or "").strip().lower() for c in header)
                if col_ref.lower() in header_text:
                    score += 2

        # Check 3: first data row has a parseable date at date column
        dsr = int(fmt.data_start_row or (hr + 2)) - 1
        if dsr < len(rows):
            date_col_ref = (fmt.col_date or "").strip()
            if len(date_col_ref) == 1 and date_col_ref.isalpha():
                didx = ord(date_col_ref.upper()) - ord("A")
            else:
                didx = None
            if didx is not None and didx < len(rows[dsr]):
                raw_date = rows[dsr][didx]
                if raw_date is not None and str(raw_date).strip():
                    from vn_banking.parser.normalizer import parse_date
                    try:
                        parse_date(raw_date, fmt.date_format or "%d/%m/%Y")
                        score += 5  # date parses successfully at expected position
                    except Exception:
                        pass  # date doesn't parse — likely wrong format

        if score > best_score:
            best_score = score
            best = fmt.name

    return best if best_score > 0 else None
