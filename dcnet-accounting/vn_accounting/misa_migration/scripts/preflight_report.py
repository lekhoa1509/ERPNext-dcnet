"""Standalone preflight report against real T1/2026 data.

Run from the bench env:

  cd <bench>/sites && ../env/bin/python \
    apps/vn_accounting/vn_accounting/misa_migration/scripts/preflight_report.py

Prints the C13 envelope shape per check + first 5 issues. No DB writes.
Useful as a pre-import sanity gate: confirms that Phase 1+2+3 prep
(Misa Account Mapping populated + Customer/Supplier masters imported)
is sufficient BEFORE the operator commits to the Phase 4 post.

Optional env var:
  PREFLIGHT_REPORT_LIMIT — max issues shown per check (default 5)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import frappe

# Allow run-from-anywhere by pointing into bench
_BENCH = Path('/home/long/long/frappe-bench-dcnet')
_SITES = _BENCH / 'sites'
_APP = _BENCH / 'apps/vn_accounting'
if str(_APP) not in sys.path:
    sys.path.insert(0, str(_APP))

frappe.init(site='dcnet.localhost', sites_path=str(_SITES))
frappe.connect()

from openpyxl import load_workbook

from vn_accounting.misa_migration.parsers import (  # noqa: E402
    nkc_parser, invoice_list_parser,
)
from vn_accounting.misa_migration.importers.preflight import run_preflight  # noqa: E402


_REALDATA = _BENCH / 'docs/accounting-requirements/realdata'
_NKC = _REALDATA / 'so_nhat_ky_chung/So_nhat_ky_chung_01-2026.xlsx'
_BR = (_REALDATA / 'bang_ke_hoa_don_mua_ban'
       / 'Bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_ban_ra_mau_quan_tri 01-2026.xlsx')
_MV = (_REALDATA / 'bang_ke_hoa_don_mua_ban'
       / 'Bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_mua_vao_mau_quan_tri 01-2026.xlsx')

_LIMIT = int(os.environ.get('PREFLIGHT_REPORT_LIMIT', '5'))


def _load(p: Path) -> list[dict]:
    wb = load_workbook(str(p), read_only=True, data_only=True)
    rows = list(wb.active.iter_rows(values_only=True))
    wb.close()
    headers = [str(c).strip() if c else '' for c in rows[3]]
    return [
        {h: (v.isoformat() if hasattr(v, 'isoformat') else v)
         for h, v in zip(headers, r) if h and v is not None}
        for r in rows[4:] if any(c is not None for c in r)
    ]


def main() -> None:
    nkc = _load(_NKC)
    br = _load(_BR)
    mv = _load(_MV)

    vouchers = nkc_parser.parse_nkc_rows(nkc)
    br_inv = {
        i['voucher_no']: i
        for i in invoice_list_parser.parse_invoice_list(br, kind='BR')
        if i.get('voucher_no')
    }
    mv_inv = {
        i['voucher_no']: i
        for i in invoice_list_parser.parse_invoice_list(mv, kind='MV')
        if i.get('voucher_no')
    }

    company = (frappe.defaults.get_global_default('company')
               or frappe.db.get_value('Company', {}, 'name'))

    print(f'Vouchers: {len(vouchers)}  '
          f'BR invoices: {len(br_inv)}  '
          f'MV invoices: {len(mv_inv)}')
    print(f'Company: {company}\n')

    result = run_preflight(vouchers, br_inv, mv_inv, company=company)
    print(f'STATUS: {result["status"]}')
    print(f'block_count: {result["block_count"]}  '
          f'warn_count: {result["warn_count"]}  '
          f'total_issues: {result["issue_count"]}\n')

    print('---- Per-check summary ----')
    for c in result['checks']:
        icon = ('*' if c['passed']
                else 'X' if c['level'] == 'block'
                else '!' if c['level'] == 'warn'
                else 'i')
        status = ('OK' if c['passed']
                  else f'FAIL ({len(c["issues"])} issues)')
        print(f'{icon} [{c["level"]:5}] {c["label"]:50} {status}')
        if not c['passed'] and c['issues']:
            for iss in c['issues'][:_LIMIT]:
                print(f'    - {iss[:140]}')
            if len(c['issues']) > _LIMIT:
                print(f'    ...and {len(c["issues"]) - _LIMIT} more')

    print('\n---- Phase 4 readiness ----')
    if result['status'] == 'ok':
        print('READY: all preflight checks pass. Phase 4 post can proceed.')
    elif result['status'] == 'warn':
        print('WARN: no block-level failures, but ' +
              f'{result["warn_count"]} warnings need operator '
              'acknowledgement before Phase 4 post.')
    else:
        print('BLOCKED: fix the block-level checks above before Phase 4 post.')

    frappe.destroy()


if __name__ == '__main__':
    main()
