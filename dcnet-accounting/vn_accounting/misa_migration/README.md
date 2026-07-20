# Misa SME → ERPNext Migration

Module-internal docs for `vn_accounting.misa_migration` — the 4-phase
import pipeline that brings Misa SME accounting data into ERPNext.

**Spec:** `docs/superpowers/specs/2026-05-19-misa-migration-framework-design.md`
**Roadmap:** `docs/superpowers/plans/2026-05-19-misa-migration-roadmap.md`

## What it imports

| Phase | Misa data | ERPNext target |
|-------|-----------|----------------|
| 1 | Reference masters (13 files: UOM, Bank, Department, Warehouse, Item Group, Customer/Supplier Group, Cost Center, Project, Asset Category, CCDC Category) | matching DocTypes |
| 2 | Chart of Accounts (~260 rows) | `Account` with `account_number` |
| 3 | Master entities (Item, Customer, Supplier, Employee, Bank Account) | `doc.name = Misa Mã` directly |
| 4 | Transactions: NKC (Nhật ký chung), bảng kê BR/MV | SI / PI / PE / JE / SE per voucher prefix |

Phase 4 routes vouchers by 17-character prefix (BH/MDV/MH/PN/PNHN/PX/PXHN/BC/UNC/PT/PC/CTNB/NVK/PBDT/PBPTT/KH/CK)
through `importers/voucher_router.py` to handlers in `importers/nkc_handlers/*.py`.

## End-user flow

1. **Upload** 3 transaction files + (optional) master sidecars via
   `/app/misa-migration-hub`. Files land in `tabFile` → `Misa Migration File`
   child rows attach to a new `Misa Migration Batch` (status: UPLOADED).
2. **Parse** runs `parsers/nkc_parser.py` + `parsers/invoice_list_parser.py`
   in a background RQ job. Each row becomes a `Misa Migration Row` with
   `status='New'`, `raw_payload` JSON-encoded. Batch → PARSED.
3. **Review** shows 4 phase tabs with sub-tabs per file_type. Operator
   resolves Conflict / Invalid rows via `ConflictDialog`. Phase E adds a
   yellow banner when `dcnet_sample` data is present (offers wipe / coexist
   / new Company). Batch → REVIEWED after `mark_reviewed`.
4. **Post** runs `jobs/post_job.post_batch` which:
   - runs Phase 1+2 importers via `orchestrator.run_post`
   - runs Phase 4 dispatch via `importers/phase_4_orchestrator.run_phase_4_post`
   - publishes `misa_migration:post_progress` realtime events
   - transitions REVIEWED → POSTING → POSTED (or STUCK on fatal)
5. **Undo** (optional) — cancels + deletes all batch-created docs via
   `jobs/undo_job.undo_batch`. Phase E adds external-dependent
   constraint check; pass `force=true` to bypass.

## Pre-flight (10 checks)

`importers/preflight.py:run_preflight` is the gate before Post. Returns
`{status: ok|warn|block, checks: [...], block_count, warn_count}`.
Block-level failures prevent Post; warn-level requires confirmation.

| Check | Level | What it verifies |
|-------|-------|------------------|
| `nkc_balance` | block | Every NKC voucher Dr = Cr |
| `bh_has_br_match` | warn | Every BH has bảng kê BR row |
| `mdv_mh_pn_has_mv_match` | warn | Every MDV/MH/PN has bảng kê MV row |
| `party_code_uniqueness` | warn | Same `Mã đối tượng` not on both 131 + 331 |
| `tk_mapping` | block | Every Misa TK resolves to ERPNext Account |
| `item_lookup` | info | Placeholder Item used in v1 |
| `posting_period_not_locked` | block | No PCV covers the voucher dates |
| `company_vnd_default` | block | Company default_currency = VND |
| `no_existing_posted` | block | No voucher_no collision in SI/PI/PE/JE/SE |
| `party_masters_present` | block | Customer / Supplier exists per party_code |

## Pre-import preparation checklist

Phase 4 expects Phase 3 done. Before running Post on a real T1/2026 batch:

```bash
# 1. Confirm masters are imported
bench --site <site> execute frappe.db.count --kwargs '{"doctype":"Customer"}'
bench --site <site> execute frappe.db.count --kwargs '{"doctype":"Supplier"}'
bench --site <site> execute frappe.db.count --kwargs '{"doctype":"Item"}'

# 2. Confirm Misa Account Mapping populated
bench --site <site> execute vn_accounting.misa_migration.api.demo_data.detect_demo_data

# 3. If dcnet_sample present, wipe it first (UI flow recommended).
# CLI fallback:
bench --site <site> execute dcnet_sample.setup.teardown_all
```

## Environment-gated tests

| Env var | Test class | Effect |
|---------|-----------|--------|
| `MISA_E2E=1` | `test_e2e_phase_d.TestE2EPhaseDT1_2026` | Runs real-data parser + full posting against the live site |
| `MISA_TB=1` | `test_trial_balance_t1_2026.TestTrialBalanceT1_2026Compare` | Compares ERPNext TB at end-of-period vs Misa fixture (1k VND tolerance) |
| `MISA_TB_FIXTURE=<path>` | (same) | Override the default `Danh_sach_so_du_tai_khoan.xlsx` fixture |
| `MISA_TB_END=YYYY-MM-DD` | (same) | Override the period end date (default 2026-01-31) |

Always-on tests cover 244+ helper paths; the gated tests do real DB writes.

Run regression (no env vars):
```bash
cd <bench>/sites
../env/bin/python -c "
import frappe; frappe.init(site='<site>', sites_path='<bench>/sites'); frappe.connect()
import unittest
modules = ['test_base_importer','test_item_importer','test_party_overlap',
           'test_party_type_detect','test_nkc_parser','test_invoice_list_parser',
           'test_voucher_router','test_si_handler_helpers','test_vat_extractor',
           'test_pi_handler_helpers','test_pe_handler_helpers','test_pe_multileg',
           'test_je_handler','test_je_pbdt_large','test_je_depreciation',
           'test_pn_handler','test_se_handler','test_preflight',
           'test_e2e_phase_d','test_trial_balance_t1_2026',
           'test_demo_data_api','test_resume_retry_api',
           'test_watchdog','test_undo_constraint']
loader = unittest.TestLoader(); total=0; fail=0; skipped=0
for m in modules:
    s = loader.loadTestsFromName(f'vn_accounting.misa_migration.tests.{m}')
    r = unittest.TextTestRunner(verbosity=0).run(s)
    total += r.testsRun; skipped += len(r.skipped)
    if not r.wasSuccessful(): fail += 1
print(f'{total} tests, {skipped} skipped, {fail} module(s) failed')
"
```

## Troubleshooting

### "TK X: không tìm thấy Account" in pre-flight

Misa Account Mapping is incomplete. Two paths:
1. **Re-run Phase 2 import** with the full CoA file.
2. **Manual mapping** via `Misa Account Mapping` Single — add `{misa_tk: erpnext_account_name}` to the `mappings` JSON.

### "Supplier 'X' not found — run Phase 3 first"

The Phase 3 master import didn't include this code. Re-upload the supplier
sidecar file or manually create the Supplier with `name = Misa Mã`.

### Batch stuck in POSTING

The RQ worker died or got blocked. Phase E watchdog marks it STUCK after
10 minutes of `modified` idle; manual fast-path:
```bash
bench --site <site> execute vn_accounting.misa_migration.jobs.watchdog.check_stuck_batches --kwargs '{"idle_minutes": 0}'
```
Then click **Tiếp tục Post** in the ResumeBanner. Handlers are idempotent
(via `frappe.db.exists` on target `doc.name`) so already-Posted vouchers
skip on the second pass.

### "Đăng" button stays disabled in PostStep

`preflightData.blocked.length > 0` or `n_ready === 0`. Open the
preflight detail dialog (button below the action row) to see which
check failed.

### Failed rows after Post completes

PostStep shows "Xem & Retry (N dòng Failed)" — opens
`FailedRowsModal.vue` listing each failure with error_message.
"Retry tất cả" resets just those rows back to Ready and re-runs the
pipeline. Fix the root cause (TK mapping, missing master, etc.) BEFORE
retry or it will fail again identically.

### Undo refuses with "force=true để bỏ qua"

Some doc OUTSIDE the batch is referencing a batch-created doc (e.g.
an operator manually allocated a Payment Entry to a batch-created Sales
Invoice). The block lists up to 10 such dependents; confirming the
follow-up dialog calls `start_undo(force=True)` which proceeds and
logs a warning. Downstream references will now point at cancelled docs
— resolve manually after.

## Source layout

```
misa_migration/
├── README.md                         (this file)
├── api/
│   ├── upload.py
│   ├── parse.py
│   ├── review.py
│   ├── post.py                       (preflight wraps Phase D checks)
│   ├── undo.py                       (constraint_check + force flag)
│   ├── demo_data.py                  (dcnet_sample detection + wipe)
│   └── resume.py                     (resume_post + retry_failed_rows)
├── doctype/                          (5 DocTypes: Batch, File, Row, Field Mapping, Account Mapping)
├── importers/
│   ├── base.py                       (BaseImporter ABC)
│   ├── orchestrator.py               (Phase 1+2)
│   ├── phase_4_orchestrator.py       (NKC → router dispatch)
│   ├── voucher_router.py             (17-prefix → handler)
│   ├── nkc_handlers/                 (6 modules: SI, PI, PR, PE, SE, JE)
│   ├── vat_extractor.py
│   ├── party_type_detect.py
│   ├── party_overlap.py
│   ├── preflight.py                  (10 pre-Post checks)
│   └── <reference / Phase 3 importers>
├── jobs/
│   ├── parse_job.py
│   ├── post_job.py                   (Phase 1+2 + Phase 4 wired)
│   ├── undo_job.py
│   └── watchdog.py                   (cron, marks STUCK on idle)
├── parsers/
│   ├── nkc_parser.py
│   └── invoice_list_parser.py
├── page/misa_migration_hub/          (Frappe Page entry point)
├── public/js/misa_migration_hub/     (Vue 3 SFC app, esbuild bundled)
└── tests/                            (24 modules, 259+ tests)
```

## Spec deltas (notable deviations)

| Spec wording | Actual implementation | Reason |
|---|---|---|
| PN → PI + PR sibling | Single PI with `update_stock=1` | ERPNext SLE handles stock inline; no sibling PR needed |
| Phase 4 PBDT split-by-revenue-account default | Single big JE default; `split_by_revenue_account=True` opt-in | Spec §5 says faithful to Misa; split is the v2 escape hatch |
| Item lookup via fuzzy-match | Placeholder Item `MISA-MIGRATION-SVC` | v1 trades accuracy for safety; Phase E may revisit |
