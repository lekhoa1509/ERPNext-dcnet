"""BaseImporter ABC for Misa Migration entity importers.

Two-phase pipeline matching the wizard flow:

  parse_job → preview_row → (user reviews) → mark_reviewed → post_row

Subclasses implement column_map / dedupe_key / validate / build_doc. The
ABC handles status transitions on Misa Migration Row + counts aggregation.

Status semantics on Misa Migration Row.status:
  New     — fresh from parse, preview not yet run
  Exists  — preview found a match in ERPNext, will skip create
  Conflict — preview found a match but data differs, user must resolve
  Invalid — validation errors, blocked from post
  Skipped — user manually skipped this row
  Ready   — user-confirmed "OK to create" (also default after preview if no
            issues found)
  Posted  — successfully created in ERPNext
  Failed  — exception during create, see error_message
  Reversed — undo job cancelled/deleted the created doc
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any

import frappe
from frappe import _


class BaseImporter(ABC):
    """Abstract base for one Misa entity type (UOM, Bank, Account, Customer, …).

    Subclass contract:
      class_attribute file_type        — Misa file classification string
      class_attribute entity_type      — Misa Migration Row.entity_type value
      class_attribute target_doctype   — ERPNext DocType to create
      class_attribute column_map       — {erpnext_field: Misa header label}
      method dedupe_key(normalized)    — value used as ERPNext doc.name
      method validate(normalized)      — list of error strings (empty = OK)
      method build_doc(normalized)     — dict ready for frappe.get_doc(...).insert()
    """

    # subclass must set these
    file_type: str = ""
    entity_type: str = ""
    target_doctype: str = ""
    column_map: dict[str, str] = {}

    def __init__(self, batch_name: str):
        self.batch_name = batch_name
        self.counts: dict[str, int] = {
            "new": 0, "exists": 0, "conflict": 0, "invalid": 0,
            "ready": 0, "skipped": 0, "posted": 0, "failed": 0, "reversed": 0,
        }

    # ------------------------------------------------------------- helpers

    def normalize(self, raw_payload: dict[str, Any]) -> dict[str, Any]:
        """Map Misa headers → ERPNext field names + strip whitespace."""
        out: dict[str, Any] = {}
        for erpnext_field, misa_header in self.column_map.items():
            val = raw_payload.get(misa_header)
            if val is None:
                continue
            if isinstance(val, str):
                val = val.strip()
                if not val:
                    continue
            out[erpnext_field] = val
        return out

    def _load_raw(self, row_doc) -> dict[str, Any] | None:
        try:
            return json.loads(row_doc.raw_payload or "{}")
        except (ValueError, TypeError):
            self._mark(row_doc, "Invalid", "Lỗi parse raw_payload JSON", {})
            return None

    def _mark(self, row_doc, status: str, error: str | None,
             normalized: dict[str, Any] | None, target_name: str | None = None) -> None:
        row_doc.status = status
        if error is not None:
            row_doc.error_message = error[:500]
        elif row_doc.error_message:
            row_doc.error_message = None
        if normalized is not None:
            row_doc.parsed_payload = json.dumps(normalized, ensure_ascii=False)
        if target_name:
            row_doc.target_doctype = self.target_doctype
            row_doc.target_name = target_name
        row_doc.db_update()

    # ------------------------------------------------------------- abstract

    @abstractmethod
    def dedupe_key(self, normalized: dict[str, Any]) -> str:
        """Return the ERPNext doc.name candidate from normalized row."""

    @abstractmethod
    def validate(self, normalized: dict[str, Any]) -> list[str]:
        """Return list of error messages. Empty list = valid."""

    @abstractmethod
    def build_doc(self, normalized: dict[str, Any]) -> dict[str, Any]:
        """Return dict suitable for frappe.get_doc(...).insert()."""

    def lookup_existing(self, normalized: dict[str, Any]) -> str | None:
        """Return existing ERPNext doc.name for an idempotent re-import,
        or None if no match. Default implementation returns None so
        importers that don't need cross-batch dedupe can ignore this
        method; importers that overlap with existing data should
        override to prevent DuplicateEntryError on insert retry."""
        return None

    # ----------------------------------------------------------- phase API

    def preview_row(self, row_doc) -> str:
        """Classify a parsed row: New → Exists/Conflict/Invalid/Ready.

        Returns the new status. Updates row_doc in DB.
        """
        raw = self._load_raw(row_doc)
        if raw is None:
            self.counts["invalid"] += 1
            return "Invalid"

        normalized = self.normalize(raw)
        errors = self.validate(normalized)
        if errors:
            self._mark(row_doc, "Invalid", "; ".join(errors), normalized)
            self.counts["invalid"] += 1
            return "Invalid"

        # Existence check — importers that can't predict the ERPNext
        # autoname (e.g. Warehouse uses `<name> - <company_abbr>` suffix
        # which we can't compose without the company doc loaded) MUST
        # override lookup_existing() and return None from dedupe_key().
        # In that case, skip dedupe_key Invalid mark and let
        # lookup_existing decide Exists vs Ready.
        name = self.dedupe_key(normalized)
        custom_lookup = self.lookup_existing(normalized)
        if custom_lookup:
            self._mark(row_doc, "Exists", None, normalized,
                       target_name=custom_lookup)
            self.counts["exists"] += 1
            return "Exists"

        if not name:
            # No dedupe_key AND lookup_existing returned None → treat as
            # Ready (new record). post_row will call lookup_existing
            # again to guard against same-loop duplicates. Importers that
            # genuinely need dedupe_key (e.g. by-code idempotency) should
            # return a non-empty key OR override lookup_existing.
            self._mark(row_doc, "Ready", None, normalized)
            self.counts["ready"] += 1
            return "Ready"

        existing = frappe.db.exists(self.target_doctype, name)
        if existing:
            self._mark(row_doc, "Exists", None, normalized, target_name=existing)
            self.counts["exists"] += 1
            return "Exists"

        self._mark(row_doc, "Ready", None, normalized)
        self.counts["ready"] += 1
        return "Ready"

    def post_row(self, row_doc) -> str:
        """Create ERPNext doc for a Ready row. Returns Posted or Failed."""
        if row_doc.status != "Ready":
            return row_doc.status

        try:
            normalized = json.loads(row_doc.parsed_payload or "{}")
        except (ValueError, TypeError):
            normalized = {}

        try:
            # Idempotency: re-check lookup_existing BEFORE insert. If
            # the target already exists (preview was skipped, a sibling
            # row in this same loop inserted it, OR a prior failed-then-
            # retried post is being re-run), mark Exists rather than
            # crash with DuplicateEntryError. lookup_existing returns
            # None for importers that don't override it.
            existing = self.lookup_existing(normalized)
            if existing:
                self._mark(row_doc, "Exists", None, normalized,
                           target_name=existing)
                self.counts["exists"] += 1
                return "Exists"
            payload = self.build_doc(normalized)
            doc = frappe.get_doc(payload)
            doc.insert(ignore_permissions=True)
            self._mark(row_doc, "Posted", None, normalized, target_name=doc.name)
            self.counts["posted"] += 1
            return "Posted"
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            frappe.log_error(title=f"Misa Migration {self.target_doctype} create failed", message=err)
            self._mark(row_doc, "Failed", err, normalized)
            self.counts["failed"] += 1
            return "Failed"

    def undo_row(self, row_doc) -> str:
        """Cancel/delete the doc created from a Posted row. Returns Reversed or status unchanged."""
        if row_doc.status != "Posted" or not row_doc.target_name:
            return row_doc.status
        try:
            if frappe.db.exists(self.target_doctype, row_doc.target_name):
                doc = frappe.get_doc(self.target_doctype, row_doc.target_name)
                # Submittable docs need cancel before delete; refs are usually non-submittable
                if getattr(doc, "docstatus", 0) == 1:
                    doc.flags.ignore_links = True
                    doc.cancel()
                frappe.delete_doc(self.target_doctype, row_doc.target_name,
                                  force=True, ignore_permissions=True)
            row_doc.is_reversed = 1
            self._mark(row_doc, "Reversed", None, None)
            self.counts["reversed"] += 1
            return "Reversed"
        except Exception as exc:
            err = f"{type(exc).__name__}: {exc}"
            row_doc.undo_error = err[:500]
            row_doc.db_update()
            return row_doc.status
