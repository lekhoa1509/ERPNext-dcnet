"""Orchestrator — dispatch Misa Migration Row rows to the right importer.

DAG (spec §4):
  Phase 1 — refs (no cross-deps, any order):
    UOM, Bank, Department, Warehouse, Item Group, Customer Group,
    Supplier Group, Cost Center, Project, Asset Category, CCDC Category
  Phase 2 — Chart of Accounts (no deps on Phase 1)
  Phase 3 — Master entities (depend on Phase 1+2):
    Item, Customer, Supplier, Employee, Bank Account

Per-row pipeline:
  parsed (status=New)
   → preview_row → Exists / Conflict / Invalid / Ready
   → (user reviews + resolves conflicts, marks Skipped where wanted)
   → mark_reviewed (REVIEWED state)
   → post_row → Posted / Failed
   → (optional later) undo_row → Reversed
"""

from __future__ import annotations

from typing import Iterator

import frappe

from vn_accounting.misa_migration.importers.account import AccountImporter
from vn_accounting.misa_migration.importers.asset_category import AssetCategoryImporter
from vn_accounting.misa_migration.importers.bank import BankImporter
from vn_accounting.misa_migration.importers.bank_account import BankAccountImporter
from vn_accounting.misa_migration.importers.base import BaseImporter
from vn_accounting.misa_migration.importers.ccdc_category import CcdcCategoryImporter
from vn_accounting.misa_migration.importers.cost_center import CostCenterImporter
from vn_accounting.misa_migration.importers.customer import CustomerImporter
from vn_accounting.misa_migration.importers.customer_group import CustomerGroupImporter
from vn_accounting.misa_migration.importers.department import DepartmentImporter
from vn_accounting.misa_migration.importers.employee import EmployeeImporter
from vn_accounting.misa_migration.importers.item import ItemImporter
from vn_accounting.misa_migration.importers.item_group import ItemGroupImporter
from vn_accounting.misa_migration.importers.misa_defaults import MisaDefaultAccountImporter
from vn_accounting.misa_migration.importers.project import ProjectImporter
from vn_accounting.misa_migration.importers.supplier import SupplierImporter
from vn_accounting.misa_migration.importers.supplier_group import SupplierGroupImporter
from vn_accounting.misa_migration.importers.uom import UomImporter
from vn_accounting.misa_migration.importers.warehouse import WarehouseImporter


# Ordered list — declared order is the post run order; undo is reverse.
# Phase 1 (refs) → Phase 2 (Account) → Phase 3 (Master).
PHASE_1_2_3_IMPORTERS: list[type[BaseImporter]] = [
    # Phase 1
    UomImporter,
    BankImporter,
    DepartmentImporter,
    WarehouseImporter,
    ItemGroupImporter,
    CustomerGroupImporter,
    SupplierGroupImporter,
    CostCenterImporter,
    ProjectImporter,
    AssetCategoryImporter,
    CcdcCategoryImporter,
    # Phase 2 — CoA THEN default-account derivations. Order matters:
    # Account inserts must complete BEFORE MisaDefaultAccountImporter
    # tries to resolve TK → Account.name on the target company.
    AccountImporter,
    MisaDefaultAccountImporter,
    # Phase 3
    ItemImporter,
    CustomerImporter,
    SupplierImporter,
    EmployeeImporter,
    BankAccountImporter,
]

# Backward-compatible alias — anything still importing PHASE_1_2_IMPORTERS works
PHASE_1_2_IMPORTERS = PHASE_1_2_3_IMPORTERS


def importer_for_file_type(file_type: str, batch_name: str) -> BaseImporter | None:
    """Return an instantiated importer matching a file_type, or None if unsupported."""
    for cls in PHASE_1_2_IMPORTERS:
        if cls.file_type == file_type:
            return cls(batch_name)
    return None


def _iter_rows_for_status(batch_name: str, status: str | list[str]) -> Iterator:
    """Yield Misa Migration Row docs filtered by status.

    Account rows are sorted by TK length ascending (parents before children)
    so parent group accounts exist as is_group=1 BEFORE their children
    arrive. Without this, ERPNext rejects the child with
    "The root account X must be a group" — child's parent_account
    lookup returns None because the parent code wasn't promoted yet.
    All other file_types stay in row_index order.
    """
    statuses = [status] if isinstance(status, str) else status
    names = frappe.db.sql_list(
        """SELECT name FROM `tabMisa Migration Row`
           WHERE batch=%s AND status IN %s
           ORDER BY
             file_type,
             CASE WHEN file_type='Account'
                  THEN CHAR_LENGTH(COALESCE(JSON_UNQUOTE(JSON_EXTRACT(parsed_payload, '$._tk')), ''))
                  ELSE 0
             END,
             row_index""",
        (batch_name, tuple(statuses)),
    )
    for n in names:
        yield frappe.get_doc("Misa Migration Row", n)


def run_preview(batch_name: str) -> dict:
    """Run preview_row on all New rows in a batch. Updates counts on Batch.

    Returns aggregated counts per file_type.
    """
    summary: dict[str, dict[str, int]] = {}
    # Process each file_type group with its importer
    file_types_in_batch = frappe.db.sql_list(
        "SELECT DISTINCT file_type FROM `tabMisa Migration Row` WHERE batch=%s",
        (batch_name,),
    )
    for ft in file_types_in_batch:
        importer = importer_for_file_type(ft, batch_name)
        if not importer:
            continue
        for row in _iter_rows_for_status(batch_name, "New"):
            if row.file_type != ft:
                continue
            importer.preview_row(row)
        summary[ft] = dict(importer.counts)
        frappe.db.commit()
    return summary


def run_post(batch_name: str) -> dict:
    """Run post_row on all Ready rows. Returns per-file_type counts."""
    summary: dict[str, dict[str, int]] = {}
    file_types_in_batch = frappe.db.sql_list(
        "SELECT DISTINCT file_type FROM `tabMisa Migration Row` WHERE batch=%s AND status='Ready'",
        (batch_name,),
    )
    # Phase ordering — iterate importers in declared order, post matching file_types only
    declared_order = [cls.file_type for cls in PHASE_1_2_IMPORTERS]
    ordered_fts = [ft for ft in declared_order if ft in file_types_in_batch]
    for ft in ordered_fts:
        importer = importer_for_file_type(ft, batch_name)
        if not importer:
            continue
        for row in _iter_rows_for_status(batch_name, "Ready"):
            if row.file_type != ft:
                continue
            importer.post_row(row)
        # Per-batch finalize hook — currently only MisaDefaultAccountImporter
        # uses it (aggregates collected TK candidates → writes Company +
        # VN Accounting Settings defaults after all rows iterated).
        finalize = getattr(importer, "finalize", None)
        if callable(finalize):
            try:
                fin_result = finalize()
                if fin_result:
                    summary.setdefault(ft, dict(importer.counts))
                    summary[ft]["finalize"] = fin_result
            except Exception as exc:
                frappe.log_error(
                    title=f"Misa finalize failed: {ft}",
                    message=str(exc),
                )
        summary[ft] = summary.get(ft) or dict(importer.counts)
        if "finalize" not in summary[ft]:
            summary[ft].update(dict(importer.counts))
        frappe.db.commit()
    return summary


def run_undo(batch_name: str) -> dict:
    """Run undo_row on all Posted rows. Reverse declared order."""
    summary: dict[str, dict[str, int]] = {}
    file_types_in_batch = frappe.db.sql_list(
        "SELECT DISTINCT file_type FROM `tabMisa Migration Row` WHERE batch=%s AND status='Posted'",
        (batch_name,),
    )
    declared_order_rev = list(reversed([cls.file_type for cls in PHASE_1_2_IMPORTERS]))
    ordered_fts = [ft for ft in declared_order_rev if ft in file_types_in_batch]
    for ft in ordered_fts:
        importer = importer_for_file_type(ft, batch_name)
        if not importer:
            continue
        for row in _iter_rows_for_status(batch_name, "Posted"):
            if row.file_type != ft:
                continue
            importer.undo_row(row)
        summary[ft] = dict(importer.counts)
        frappe.db.commit()
    return summary


def get_counts(batch_name: str) -> dict:
    """Aggregate counts per file_type × status for Review tab headers."""
    rows = frappe.db.sql(
        """SELECT file_type, status, COUNT(*) as n
           FROM `tabMisa Migration Row`
           WHERE batch=%s
           GROUP BY file_type, status""",
        (batch_name,),
        as_dict=1,
    )
    out: dict[str, dict[str, int]] = {}
    for r in rows:
        out.setdefault(r.file_type, {})[r.status] = r.n
    return out
