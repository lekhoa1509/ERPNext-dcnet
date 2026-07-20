import io
from pathlib import Path
from typing import Iterator


def read_xlsx_rows(file_path: str, sheet_index: int = 0) -> Iterator[list]:
    """Yield each row as a list of cell values. Uses openpyxl (data_only=True).

    IMPORTANT: do NOT use read_only=True -- MB Bank statements have heavy merged
    cells, and read-only mode yields `None` for secondary cells of merged regions
    which breaks header detection. Full-workbook mode is slower but correct.
    """
    from openpyxl import load_workbook
    wb = load_workbook(file_path, data_only=True)
    ws = wb.worksheets[sheet_index]
    for row in ws.iter_rows(values_only=True):
        yield list(row)
    wb.close()


def read_xls_rows(file_path: str, sheet_index: int = 0) -> Iterator[list]:
    """Legacy .xls via xlrd."""
    import xlrd
    book = xlrd.open_workbook(file_path)
    sheet = book.sheet_by_index(sheet_index)
    for r in range(sheet.nrows):
        yield [sheet.cell_value(r, c) for c in range(sheet.ncols)]


def read_html_rows(file_path: str, table_index: int = 0) -> Iterator[list]:
    """HTML-as-xls (PG Bank exports HTML document with .xls extension).

    Reads raw bytes, decodes UTF-8 explicitly (pandas auto-detect often wrong
    on Vietnamese files), then parses the first `<table>` via pandas.read_html.
    Yields each row as a list of cell values; NaN -> None.
    """
    import pandas as pd
    raw = Path(file_path).read_bytes()
    try:
        html = raw.decode("utf-8")
    except UnicodeDecodeError:
        html = raw.decode("latin-1")
    tables = pd.read_html(io.StringIO(html), flavor="bs4")
    if not tables:
        return
    df = tables[table_index]
    for _, row in df.iterrows():
        yield [None if pd.isna(v) else v for v in row.tolist()]


def _is_html_disguised_as_xls(file_path: str) -> bool:
    """Some banks (PG Bank / Petrolimex) export an HTML document with .xls ext.
    Detect by looking for HTML/table tags in the first 256 bytes."""
    with open(file_path, "rb") as f:
        head = f.read(256).lower().lstrip()
    return head.startswith(b"<") or b"<html" in head or b"<table" in head


def read_rows(file_path: str, file_type: str, sheet_index: int = 0) -> Iterator[list]:
    ft = file_type.lower()
    if ft == "xlsx":
        yield from read_xlsx_rows(file_path, sheet_index)
    elif ft == "xls":
        # Auto-detect HTML-masquerading-as-xls (PG Bank case)
        if _is_html_disguised_as_xls(file_path):
            yield from read_html_rows(file_path, sheet_index)
        else:
            yield from read_xls_rows(file_path, sheet_index)
    elif ft == "html":
        yield from read_html_rows(file_path, sheet_index)
    else:
        raise ValueError(f"Unsupported file_type: {file_type}")
