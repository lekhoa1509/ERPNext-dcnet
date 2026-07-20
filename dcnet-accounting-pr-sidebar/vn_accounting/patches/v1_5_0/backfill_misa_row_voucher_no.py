"""Backfill Misa Migration Row.voucher_no from raw_payload (Tier 1.6).

Older Misa Migration Row records (every row inserted before parse_job
started populating voucher_no) leave the column NULL. The orchestrator's
new index-driven UPDATE-by-voucher path needs this column populated for
historical rows too, or those rows silently skip the status update.

Strategy: one UPDATE per file_type that pulls the voucher_no out of the
raw_payload JSON. Single bulk UPDATE per file_type — runs once at
migrate, idempotent (skips rows already populated).
"""

from __future__ import annotations

import frappe


def execute():
    # NKC: voucher number lives in the Vietnamese header "Số chứng từ"
    nkc_updated = frappe.db.sql(
        """
        UPDATE `tabMisa Migration Row`
        SET voucher_no = LEFT(JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"')), 140)
        WHERE file_type = 'NKC'
          AND (voucher_no IS NULL OR voucher_no = '')
          AND raw_payload LIKE '%Số chứng từ%'
        """
    )
    # SCT: sct_parser already emits voucher_no in the line dict
    sct_updated = frappe.db.sql(
        """
        UPDATE `tabMisa Migration Row`
        SET voucher_no = LEFT(COALESCE(
              JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$.voucher_no')),
              JSON_UNQUOTE(JSON_EXTRACT(raw_payload, '$."Số chứng từ"'))
        ), 140)
        WHERE file_type = 'SCT'
          AND (voucher_no IS NULL OR voucher_no = '')
        """
    )
    frappe.db.commit()
