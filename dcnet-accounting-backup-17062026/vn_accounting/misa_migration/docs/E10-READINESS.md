# E10 — Phase 4 Acceptance Gate Readiness

Run-book + bug surface from Playwright-assisted E10 session on
2026-05-19. The dev site (`dcnet.localhost:8001`) currently has
`dcnet_sample` demo data (5,026 records) AND does NOT have the Misa
Phase 1+2+3 imports done yet, so the real Phase 4 E2E test against
T1/2026 data is **BLOCKED**.

Full uncapped preflight evidence: see `E10-PREFLIGHT-REPORT.txt`
(456 lines covering all 437 issues — 25 TK + 399 party + 11 dual
+ 1 PN warn).

## Current blocking conditions

`run_preflight` against T1/2026 real data on the current DCNET company:

```
Vouchers: 1564  BR invoices: 303  MV invoices: 633
STATUS: block
block_count: 2  warn_count: 2  total_issues: 437

X [block] Tài khoản kế toán đã map                            FAIL (25 issues)
X [block] Master Customer/Supplier đã import                  FAIL (399 issues)
! [warn ] MDV/MH/PN có line items bảng kê                     FAIL (1 issue)
! [warn ] Mã đối tượng nhất quán                              FAIL (11 issues)
```

### Block 1 — Misa Account Mapping incomplete

25 of ~260 TKs needed by T1/2026 don't resolve to ERPNext Accounts.
Examples (representative — full list in
`E10-PREFLIGHT-REPORT.txt`):

```
TK 1111      → no Account named like "1111 - %"
TK 1121.20   → Sacombank sub-account, expected per VN-COA pattern
TK 1121.81   → VIB sub-account
TK 11210     → PG Bank sub-account
TK 1561      → inventory hàng hóa
TK 3341      → salary payable
TK 5111      → revenue subcategory
TK 51131..51136  → revenue per branch
TK 71121     → other income
TK 8211      → CIT current
```

These exist in TT99/2025 COA but aren't on this site's chart because
Phase 2 (Misa CoA import) hasn't run. Two ways to populate:

1. **Run Phase 2 import** via `/app/misa-migration-hub` with the Misa
   chart-of-accounts xlsx. This creates the Account records AND
   populates `Misa Account Mapping`.
2. **Manual JSON entry** in `Misa Account Mapping` Single (Customize
   Form → JSON field → `{"1111": "1111 - Tiền mặt VND - DC", ...}`).
   Only viable if Accounts already exist on the company under those
   names; otherwise Phase 2 import is required.

### Block 2 — 399 party masters missing

Every party_code referenced in NKC needs a matching Customer / Supplier
/ Employee record on the company. The current site has only
`dcnet_sample` demo masters (68 Customer, 29 Supplier) — NOT the
Misa codes. Examples:

```
Supplier '247' missing
Supplier '545_ĐNG' missing       (Vietnamese diacritic IDs)
Supplier 'ACT' missing
Supplier 'AMTHUCBD' missing
Supplier 'ANHSANG' missing
... and 394 more
```

Fix: **Run Phase 3 master importers via the hub**. Files at
`docs/accounting-requirements/realdata/danh mục import/` should contain
the Customer / Supplier / Employee / Item / Bank Account masters.

### Warn 1 — 1 PN voucher missing bảng kê MV

`PN20260038` exists in NKC but has no matching invoice line items in
the bảng kê MV file. Operator decision:

- **Accept**: PN handler synthesizes 1 placeholder line item from NKC
  Dr 156* total. The PI inserts with `update_stock=1` and 1 row.
- **Reject**: surface to ops for source-file correction before re-run.

Phase D `create_pi_pr_from_pn` handler tolerates this case
(synthesizes line via NKC totals). No code fix needed.

### Warn 2 — 11 dual-party codes (lưỡng tính)

These party codes appear on both 131 (Customer) AND 331 (Supplier)
legs in different vouchers — they're both a buyer and a seller for
DCNET:

```
CANG HKQT_ACV_CTCP        SAIGONPOSTEL_HCM
FFC                       SOFTNET
FPTFTICN_HNI              VIETNAMPOST_HNI
HITC                      VIETTEL_HNI
... and 3 more
```

Phase 3 importer `party_overlap.py` handles this — creates BOTH a
Customer and Supplier record with the same `name`. The warn surfaces
to confirm operator awareness; no automatic fix.

## E10 procedure (when ready to execute)

Pre-flight inspection without destructive actions:

```bash
cd /home/long/long/frappe-bench-dcnet/sites
../env/bin/python ../apps/vn_accounting/vn_accounting/misa_migration/scripts/preflight_report.py
# Reads T1/2026 files, runs preflight, prints structured report.
# No DB writes. Re-runnable anytime to check progress.
```

Full destructive E2E (operator-driven):

```bash
# 1. Wipe dcnet_sample (5,026 records, 30-120s) — DESTRUCTIVE
cd /home/long/long/frappe-bench-dcnet/sites
../env/bin/python -c "
import frappe; frappe.init(site='dcnet.localhost', sites_path='/home/long/long/frappe-bench-dcnet/sites'); frappe.connect()
from dcnet_sample.setup import teardown_all
teardown_all()
"

# 2. Run Phase 1+2+3 import via the hub UI:
#    /app/misa-migration-hub → upload masters → parse → review → post
#    Verify after: 25 TK mappings + ~3000 Customer/Supplier records created.

# 3. Re-run the preflight report; STATUS should be 'ok' or 'warn' (not 'block').
../env/bin/python ../apps/vn_accounting/vn_accounting/misa_migration/scripts/preflight_report.py

# 4. Run the full Phase 4 E2E
MISA_E2E=1 ../env/bin/python -m unittest \
  vn_accounting.misa_migration.tests.test_e2e_phase_d.TestE2EPhaseDT1_2026

# 5. Trial Balance compare
MISA_TB=1 ../env/bin/python -m unittest \
  vn_accounting.misa_migration.tests.test_trial_balance_t1_2026.TestTrialBalanceT1_2026Compare
```

## Why E10 wasn't fully executed this session

`dcnet_sample` data on the dev bench is **shared infrastructure** —
referenced by multiple other in-flight projects (dcnet_contract,
dcnet_pakd, vn_banking demos, dcnet_progress). Wiping it without
explicit operator approval would silently break those workflows.

The acceptance gate (full T1/2026 post with `< 1k VND` Trial Balance
diff) cannot be validated until the operator:

1. Confirms dcnet_sample can be wiped on this site OR provisions a
   second Company for Misa import
2. Has the Misa Phase 1+2+3 master xlsx files in
   `docs/accounting-requirements/realdata/danh mục import/`
3. Allocates 2-4 hours for Phase 4 bug iteration

Phase D + E shipped everything needed for the Post pipeline to succeed
**when** these conditions are met. The preflight report above proves
the gates work — they correctly block on a non-prepared site.

## Phase D + E code is acceptance-ready

What's verified by tests + the preflight report:

- 1,564 vouchers parse without balance errors
- 17 voucher prefixes all dispatch through the router
- 24 test classes / 270+ unit tests / 0 failures
- Preflight 10-check pipeline runs correctly + blocks on real missing
  masters + TK mappings (exact behavior expected from C13 spec)
- Idempotency: re-running over already-Posted vouchers reports
  `status: 'skipped'`, no duplicate creation
- Crash recovery: STUCK → Resume restores via state machine
- Performance: 60k synthetic rows parse in < 0.1s

The only unverified path is the full ERPNext doc insert (Phase 4
post calling 6 handler modules into a populated company). That
requires the prepared environment described above.
