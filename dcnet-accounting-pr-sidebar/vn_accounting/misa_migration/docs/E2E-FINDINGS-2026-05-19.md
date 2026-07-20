# E2E Real-Data Test Findings — 2026-05-19

Live Playwright run of the full pipeline (Phase 1+2+3 stubs → Phase 3.5
OB → Phase 4 transactions) against a freshly-created `DCNET TEST`
Company with real T1/2026 Misa data. **The pipeline ran end-to-end**
(post_batch completed without crashing) and produced concrete error
messages for the bugs that need fixing.

## Test setup

```
Company:           DCNET TEST  (fresh VND/Vietnam)
COA:               VN Large Enterprise (TT99/2025) — 185 accounts
Warehouse:         Kho Chính - DCT
stock_adjustment_account:  632 - Giá vốn hàng bán - DCT
Misa Account Mapping:  177 TKs (152 exact + 25 nearest-parent-leaf fallback)
Customer:          259 stubs (set_name = Misa Mã)
Supplier:          200 stubs
Employee:          0 (Department setup deferred)
Item:              0 (handler uses MISA-MIGRATION-SVC placeholder)
Batch:             MM-2026-00898  (10,962 rows: 1,792 OB + 9,170 Phase 4)
```

## Run outcome

| Metric | Value |
|---|---|
| post_batch elapsed | 78.4 seconds for 1,564 vouchers |
| docs created | 145 (73 JE + 73 PE) |
| docs failed | 1,419 voucher-level + 1,792 OB row-level |
| Phase 0 status | failed (every category) |
| Phase 4 by_prefix:posted | PBDT=1 / PBPTT=1 / KH=1 / NVK=31 / CTNB=38 / CK=1 / BC=73 |
| Phase 4 by_prefix:failed | BH=303 / MDV=526 / MH=5 / PN=36 / PX=52 / PXHN=21 / PNHN=4 / UNC=147 / PT=15 / PC=58 |

## Bugs surfaced — by priority

### B1 [BLOCKER, fixed] `Company.default_warehouse` doesn't exist in v16

```
MySQLdb.OperationalError: (1054, "Unknown column 'default_warehouse' in 'SELECT'")
  at _company_default_warehouse → frappe.db.get_value("Company", company, "default_warehouse")
```

**Fix shipped in this session.** `_company_default_warehouse` simplified
to query `Warehouse` directly (`company + is_group=0 + disabled=0`).
v16 Company has only `default_in_transit_warehouse` /
`default_wip_warehouse` / `default_fg_warehouse` / `default_scrap_warehouse`
/ `default_warehouse_for_sales_return` — no plain `default_warehouse`.

### B2 [BLOCKER] Multi-Company support — handlers use global default

```
ValidationError: Row #1: Account 33311 - Thuế GTGT đầu ra - DCT does
not belong to company DCNET
```

Every handler (`sales_invoice.py`, `purchase_invoice.py`,
`payment_entry.py`, `journal_entry.py`, `stock_entry.py`,
`purchase_receipt.py`) does:

```python
company = frappe.defaults.get_global_default("company") or \
          frappe.db.get_value("Company", {}, "name")
```

Misa Migration Batch carries `company` field but it's ignored. Workaround
for this session: switched `frappe.db.set_default('company', 'DCNET TEST')`
before the run. Real fix: handlers should accept `company` arg from the
orchestrator OR read it from the batch document.

### B3 [BLOCKER] Customer.default_receivable_account missing on stubs

```
ValidationError: Row 1: Income Account None cannot be same as
Debit To (Party Account) None
ValidationError: Party Account None currency (None) and document
currency (VND) should be same
```

Customer stubs created without `accounts` table (which maps
`account: 131 — AR — DCT`). Sales Invoice handler relies on ERPNext
to resolve `debit_to` from this. Same for Supplier
`default_payable_account`.

**Fix needed:** bootstrap helper must populate Customer.accounts /
Supplier.accounts child rows with the correct AR/AP account per company.

### B4 [BLOCKER] Company.stock_received_but_not_billed missing

```
ValidationError: Please set default Stock Received But Not Billed
in Company DCNET TEST
```

Purchase Invoice with `update_stock=1` requires
Company.stock_received_but_not_billed pointing at TK 3388 / 1561 /
similar suspense account. Company setup checklist for Misa migration
must include this field.

### B5 [BLOCKER] Phase 0 Opening JE — same-account Dr+Cr after TK mapping collapse

```
ValidationError: You cannot credit and debit same account at the
same time
```

Our nearest-parent-leaf fallback for unmapped TKs (B6 below) collapses
5111/5112/51131-51136/5114 all to 511. The aggregated Opening JE then
has both Dr 511 (from inventory cost) AND Cr 511 (from revenue accrual)
in the same JE → ERPNext rejects.

Same issue for 6321-6324 → 632, 3341/3348 → 334, 11210-11219/1121.20-81 → 112.

**Fix needed (2 options):**

A. Aggregate same-account rows: collapse multiple rows with the same
   `account` into one net Dr/Cr (subtract opposite side).
B. Set Dr/Cr on different `party` per row (ERPNext allows same account
   if party differs). Only works for AR/AP though.

Option A is more general. Implement in `opening_journal.post_opening_journal`
right before payload assembly.

### B6 [WARN] TK leaf gaps in VN-COA template

The TT99/2025 template ships TK 511 as a leaf, not a group. But Misa
files include 5111/5112/51131-51136/5114 — these would need child
sub-accounts under TK 511 (which means promoting 511 to a group first).
Same for 632, 334, 1121, 156.

**Decision:** v1 keeps the collapse-to-parent fallback (B5 fix
sufficient). v2 may auto-promote-and-extend the COA template based on
Misa file scan. Current behavior is acceptable — Trial Balance compare
at TK 511 level (sum of all 511x) will still match Misa.

### B7 [BLOCKER] UNC handler missing classification path

```
UNC20260185: no Dr 331 / Dr 141 leg — route to JE handler
```

UNC handler's leg classifier missed some UNC patterns. 147 of 220 UNC
vouchers fail this way. Need to inspect a sample and extend
`_split_unc_legs`.

### B8 [BLOCKER] NKC rows status update — only 1645/7847 marked Posted

The Phase 4 orchestrator's `_update_nkc_row_status_by_voucher` uses
`JSON_EXTRACT` on Số chứng từ. For most failed vouchers it correctly
marks Failed. But the screenshot shows 7846/7847 ✗6202 — i.e. 6202
rows got error_message set. The 1645 difference (7847 − 6202) suggests
some rows didn't get the error message propagated. Worth verifying
the SQL path on a smaller batch.

### B9 [INFO] Phase 0 row count expansion

The screenshot shows "NKC 7846/7847 ✗6202" but `total_vouchers` from
Phase 4 was 1,564. The row count is the leg count (7847 NKC rows). The
voucher-level count (1,564) only updates the rows for THAT voucher.
This is expected behavior but the UI labels could distinguish leg
vs voucher more clearly.

## What worked

1. **Pipeline ran end-to-end** — post_batch completed in 78s without
   crashing, even with 1,419 voucher errors. Per-row try/except in
   handlers prevents cascade failures.
2. **State machine** — REVIEWED → POSTING → POSTED transitions ran
   correctly. STUCK recovery (after the first crash from B1) worked
   via direct status reset.
3. **JE handlers all work**: PBDT 1,260-leg / PBPTT / KH / NVK / CTNB /
   CK all created successfully. The 1:1 leg mapping in `_create_je_1to1`
   is production-ready.
4. **Simple PE handlers work**: BC (Bank Cash) 73/73 ✅.
5. **Preflight pipeline** correctly identified all 437 prereqs upfront,
   then accepted the bootstrapped state with status=warn (no blocks).
6. **FailedRowsModal** shows the 7,994 failed rows with truncated error
   messages — diagnosable at a glance (TK problem vs party-account vs
   warehouse vs etc.).

## Next session — bug-fix priorities

In suggested order:

1. **B5 same-account aggregation** (opening_journal) — unblocks all
   1,792 OB rows. Single function change. ~30 LOC + tests.
2. **B3 Customer/Supplier accounts table** (bootstrap helper) —
   unblocks all 829 SI + PI vouchers. Update bootstrap to populate
   `customer.accounts = [{company, account: 131-...}]`. ~50 LOC.
3. **B4 Company.stock_received_but_not_billed** — 1-line config
   addition in the Company setup workflow.
4. **B7 UNC classification** — inspect sample UNC and extend
   `_split_unc_legs`. Surface a few more leg patterns.
5. **B2 Multi-Company support** — proper fix for handlers reading
   `company` from batch. Touches 6 handler modules + orchestrator
   contract change. Larger refactor; could defer if global-default
   workaround acceptable per session.

After these 5 fixes, expected outcome: 1,500+ of 1,564 Phase 4
vouchers post + all 1,792 OB rows post. Trial Balance compare should
move from "BLOCKED 437 issues" to within 1k VND tolerance.

## Screenshots captured

- `11-e2e-review-step.png` — Review with all 5 phase tabs + 10,962 rows
- `12-e2e-post-step-preflight.png` — initial preflight (BLOCKED)
- `13-e2e-preflight-dialog.png` — detailed C13 checks
- `14-e2e-post-after-bootstrap.png` — still blocked (TK mapping gap)
- `15-e2e-preflight-ok.png` — preflight WARN (no blocks)
- `16-e2e-actual-posted.png` — POSTED state, per-entity bars showing
  73 JE / 73 PE successes + 7,994 failures
- `17-e2e-failed-rows.png` — FailedRowsModal with real error messages
