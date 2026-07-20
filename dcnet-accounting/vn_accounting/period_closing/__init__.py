"""Period closing — kết chuyển 911 → 421 + khóa sổ kỳ kế toán.

Page: period-closing-911 (Phase 3 — P2 Tổng hợp).

PCV hooks (registered in hooks.py — Phase 3):
    - pcv_validate_vn_requirements  (validate)
    - pcv_audit_log                 (on_submit / on_cancel)

API endpoints (Phase 3):
    - get_closing_preview
    - create_closing_journal_entries
"""
