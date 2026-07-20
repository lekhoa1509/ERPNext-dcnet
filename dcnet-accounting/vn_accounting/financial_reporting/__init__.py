"""Financial reporting — BCTC (B01/B02/B03/B09-DN) theo TT99/2025.

Reports (Phase 4 — P3 BCTC):
    - b01_dn_bao_cao_tinh_hinh_tai_chinh  (Script Report)
    - b02_dn_bao_cao_kqhdkd               (Script Report)
    - b03_dn_bao_cao_lctt                 (Script Report, indirect method only)
    - b09_dn_generator                    (Page → multi-sheet Excel)

Core engine (resolver.py — Phase 4):
    - resolve_bctc_line(company, line, period_start, period_end)
"""
