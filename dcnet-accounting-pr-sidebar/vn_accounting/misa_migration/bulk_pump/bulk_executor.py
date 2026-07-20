"""Bulk INSERT executor — wraps cursor.executemany with batching."""
from __future__ import annotations

import time
from typing import Any

import frappe


def bulk_insert(table: str, rows: list[dict], batch_size: int = 1000) -> int:
    """INSERT ``rows`` into ``tabTable`` via executemany, batched.

    Args:
      table: bare DocType name (e.g. "Sales Invoice") — wrapped to "tabSales Invoice".
      rows: list of dicts, all sharing the same keys. Empty list = no-op.
      batch_size: rows per executemany call.

    Returns:
      Total inserted count.
    """
    if not rows:
        return 0
    # Group rows by their KEY SET signature, then INSERT each group with its
    # own column list. Avoids two failure modes:
    #   (a) first-row-keys strategy: silently drops columns that later rows
    #       set (e.g. s_warehouse on Material Issue SE Detail vs OB Inventory)
    #   (b) union strategy: passes literal NULL for columns a row didn't
    #       provide, which fails NOT NULL constraints (e.g. is_return on
    #       OB Inventory Stock Entry that the regular SE builder sets to 0)
    # Group-by-signature gives each row exactly the columns it declared.
    groups: dict[tuple[str, ...], list[dict]] = {}
    for r in rows:
        sig = tuple(sorted(r.keys()))
        groups.setdefault(sig, []).append(r)

    cur = frappe.db._cursor
    total = 0
    for sig, group_rows in groups.items():
        cols = list(sig)
        col_sql = ", ".join(f"`{c}`" for c in cols)
        ph = ", ".join(["%s"] * len(cols))
        insert_sql = f"INSERT INTO `tab{table}` ({col_sql}) VALUES ({ph})"
        for i in range(0, len(group_rows), batch_size):
            chunk = group_rows[i:i + batch_size]
            values = [tuple(r[c] for c in cols) for r in chunk]
            cur.executemany(insert_sql, values)
            total += len(chunk)
    return total


def bulk_update_field(table: str, name_to_value: dict[str, Any], field: str) -> int:
    """Bulk-update a single field across N rows. Uses INSERT ... ON DUPLICATE
    KEY UPDATE on (name, field) — fast alternative to N UPDATE statements."""
    if not name_to_value:
        return 0
    cur = frappe.db._cursor
    sql = (
        f"INSERT INTO `tab{table}` (`name`, `{field}`) VALUES (%s, %s) "
        f"ON DUPLICATE KEY UPDATE `{field}`=VALUES(`{field}`)"
    )
    values = list(name_to_value.items())
    cur.executemany(sql, values)
    return len(values)


def timed_bulk_insert(table: str, rows: list[dict], batch_size: int = 1000) -> tuple[int, float]:
    """bulk_insert + wall-clock timing for perf reporting."""
    t0 = time.time()
    n = bulk_insert(table, rows, batch_size)
    return n, time.time() - t0
