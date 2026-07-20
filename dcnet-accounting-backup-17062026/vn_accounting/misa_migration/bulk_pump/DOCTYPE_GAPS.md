# bulk_pump vs ORM — DocType Coverage Audit

As of feature/misa-migration-perf-and-recovery, post PE-dispatch + Bin-fix.

## Critical gaps (data correctness)

### 1. OB Inventory → Stock Entry (Material Receipt) — NOT IMPLEMENTED
ORM `ob_handlers/opening_inventory.py` builds one Material Receipt SE per
distinct OB Inventory row to establish opening stock balance.
bulk_pump Phase 0 iterates only `OB Fixed Asset` + `OB CCDC` — **`OB Inventory`
(1,149 rows in test data) is silently skipped**.

Without this, the company starts with zero stock and every Material Issue
(PX*, 4,586 vouchers) creates negative balance. Bin will show negatives.

**To implement:** new builder `builders/opening_inventory.py` consuming
OB Inventory Misa rows + creating SE + SED + SLE + GL rows.

### 2. PN prefix → Purchase Receipt + PI(update_stock=1) — INCORRECTLY ROUTED
ORM `nkc_handlers/purchase_receipt.py` creates PI with `update_stock=1`
(which generates both PI GL Entries AND Purchase Receipt SLE effect) for
`PN` prefix vouchers.

bulk_pump currently routes PN → SE (Material Receipt). 2,338 PN vouchers
in test data. PI count will be 2,338 short of ORM parity.

**To implement:** extend `purchase_invoice.py` builder to emit SLE rows
when prefix=="PN" (update_stock semantic). Move PN out of SE_PREFIXES into
its own PI+SLE dispatch branch.

## Acceptable gaps (audit trail only — v1.1)

### 3. Comment rows for orphan/unallocated PEs
ORM `phase_4_orchestrator.py` lines 1010-1023 and 1416-1431 create
audit-trail `Comment` rows on PEs that posted without invoice match.
GL is still correct; comments are explanatory only. Safe to defer.

## Verified non-gaps (ORM does NOT create these)

- Period Closing Voucher — only used in preflight CHECK (not created)
- Asset Movement, Asset Repair, Stock Reservation, Material Request,
  Subscription, Pricing Rule, Tax Withholding Category — never touched
  by Misa migration

## Phase 0 OB rollup coverage

OB file types and how bulk_pump handles them:

| OB file_type | Test rows | Coverage |
|---|---|---|
| OB Account Balance | 47 | ✓ rolled into Opening JE |
| OB Bank Balance | 6 | ✓ rolled into Opening JE |
| OB Customer AR | 64 | ✓ rolled into Opening JE |
| OB Supplier AP | 102 | ✓ rolled into Opening JE |
| OB Employee Advance | 2 | ✓ rolled into Opening JE |
| OB Prepaid Expense | 244 | ✓ rolled into Opening JE |
| OB Fixed Asset | 25 | ✓ → Asset (build_asset_dicts) |
| OB CCDC | 153 | ✓ → Asset (build_asset_dicts, is_ccdc=True) |
| OB Inventory | 1149 | **✗ GAP — see #1 above** |
