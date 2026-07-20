# vn_banking — Codebase Summary

**Lines of code:** ~2,784 (Python: 1,546 | JS: 777 | JSON: 390 | CSS: 71) — excluding tests (~1,165 LOC), docs, built dist bundles, and the 100-row `vi.csv`.

## Overview

Vietnamese bank statement import + auto-match Sales Invoice / Purchase Invoice + inline Payment Entry creation for DCNet.

Pipeline: accountant uploads a bank Excel/HTML sao kê → app detects the format → parses rows → normalizes + dedupes → inserts Bank Transaction records → runs a priority match engine (invoice-no, invoice-amount, party-amount, name-amount, combinations) → surfaces suggestions in a custom `bank-reconcile` desk page → accountant confirms → a draft Payment Entry is created (single or bulk) with TT99/2025-compliant fee write-off on small differences.

Supports 4 banks locked for v1: **BIDV, MB Bank, Sacombank, PG Bank** (PG Bank export is HTML-disguised-as-.xls).

## Stack

Frappe v16 + ERPNext v16. Extends ERPNext `Bank Transaction` (via Custom Fields) rather than introducing a parallel transaction model. Pure Python parsers (openpyxl, xlrd, pandas + bs4 for HTML fallback, rapidfuzz for fuzzy party-name matching). Vanilla JS desk Page for the reconcile UI (no React/Vue). Dual-remote: `goldrag1/vn_banking` (personal) + `dcnet-cloud` (DCNET).

## Directory tree

```
apps/vn_banking/
├── README.md, FEATURES.md, pyproject.toml
├── docs/                              # BUSINESS_LOGIC, USAGE, SETTINGS, specs/
├── scripts/                           # utility scripts (dev only)
└── vn_banking/                        # inner package
    ├── hooks.py, install.py, tasks.py, modules.txt, patches.txt
    ├── api/                           # whitelisted HTTP endpoints
    │   ├── reconcile.py               # main API surface for Bank Reconcile page
    │   └── webhook.py                 # v2 API scaffold (not wired)
    ├── parser/                        # file readers (xlsx/xls/html dispatcher)
    ├── source/                        # NormalizedTransaction + BankDataSource ABC
    │   └── excel.py                   # ExcelFileSource (uses Bank Statement Format config)
    ├── match/                         # priority matcher pipeline + engine
    │   ├── engine.py, context.py, helpers.py, base.py, combinations.py
    │   └── invoice_no / invoice_amount / party_amount / name_amount .py
    ├── custom/custom_fields.py        # Bank Transaction + Bank Account custom fields
    ├── fixtures/                      # seed Format / Matcher Type / Data Source
    ├── page/bank_reconcile/           # page-level helper components (partial)
    ├── public/                        # entry bundles (built under dist/)
    ├── translations/vi.csv            # 100 entries English → Vietnamese
    ├── tests/                         # unit + integration tests + sample bank files
    ├── workspace/banking_vn/          # desk workspace sidebar fixture
    └── vn_banking/
        ├── doctype/                   # 7 DocTypes (see Data model)
        └── page/bank_reconcile/       # actual Frappe Page (js/css/html/py + components)
```

## Data model

- **Bank Statement Format** — per-bank parser config: bank name, file type, data start row, column mapping (letters or header text), date/number formats. Seeded via fixture for BIDV/MB/Sacombank/PG Bank.
- **Bank Statement Import** — batch upload container: bank_account, source file, status, total/duplicate/inserted counts. NOT submittable (workflow container).
- **Bank Statement Settings** — Single DocType: tolerance, difference account (bank fee write-off per TT99/2025), default PE action, invoice-number regex patterns.
- **Bank Match Rule** — child rule registry row: matcher_type + priority + enabled flag (admins re-order + toggle).
- **Bank Matcher Type** — registry: matcher key → Python handler class path (pluggable).
- **Bank Data Source** — registry: source key → Python handler (Excel now; API v2 scaffold).
- **Bank Txn Invoice Suggestion** — child table on Bank Transaction: invoice_type, invoice_name, allocated_amount, confidence, selected flag.
- **ERPNext Bank Transaction** — extended (not replaced) via `Custom Field`: dedupe_hash, import link, match fields, suggested_invoices child table.

## Entry points

- **`hooks.py`** — `after_install`/`after_migrate` → `vn_banking.install` (creates custom fields, seeds match rules); `app_include_js/css` → `bank_reconcile.bundle.js/css`; fixtures export for Format/Matcher Type/Data Source + filtered Custom Field records.
- **Whitelisted API** (`vn_banking/api/reconcile.py`) — detect_format_and_bank, trigger_import, get_import_transactions, create_payment_entry, bulk_create_pe, explain_match, trigger_rematch.
- **Desk Page** `bank-reconcile` — custom Frappe Page (not a workspace), page.js + 5 component modules; published realtime progress for async imports.
- **Sidebar** — `workspace/banking_vn/banking_vn.json` provides sidebar navigation into the reconcile page + related DocTypes.

## Core flows

1. **Upload statement** — user opens Bank Reconcile page → drag/drop file in upload dialog → `detect_format_and_bank()` returns best Format + resolved Bank Account → `trigger_import()` runs sync (<200 rows) or enqueues async → parser reads file → normalizer computes SHA-256 dedupe hash → new rows become Bank Transaction records; duplicates counted + skipped.
2. **Auto-match** — `run_match_engine()` (first-hit-wins) walks enabled rules in priority order: InvoiceNoMatcher (regex on description) → InvoiceAmountMatcher (unique amount within tolerance) → PartyAmountMatcher (counter_account_no → party → single/combo invoices) → NameAmountMatcher (rapidfuzz ≥80 + amount) → combinations_sum_match (smallest k-combination within tolerance). Each candidate gets High/Medium/Low confidence and is written to the txn's `suggested_invoices` child table.
3. **Create Payment Entry inline** — user confirms suggestion in txn side panel → `create_payment_entry()` builds PE with `mode_of_payment="Bank Draft"` explicitly set (avoids NULL trap), multi-invoice references, and writes small fee differences to Settings.difference_account per TT99/2025.
4. **Bulk PE creation** — `bulk_create_pe()` creates draft PEs for all High-confidence txns; idempotent (skips txns already Reconciled).
5. **Dedupe** — same file re-upload: hash collision skips insert. Hash = `sha256(date|amount|ref|description)`; survives cross-file duplicates.
6. **Re-match** — `trigger_rematch()` clears suggestions + re-runs engine without re-parsing (used after config / rule priority changes).

## Read first

1. `docs/BUSINESS_LOGIC.md` — accounting workflow, roles, scope, confidence tiers, fee write-off rules.
2. `vn_banking/hooks.py` — app wiring.
3. `vn_banking/install.py` — `after_install` / `after_migrate` custom-field + rule seeding.
4. `vn_banking/api/reconcile.py` — full HTTP surface; map UI actions to handlers.
5. `vn_banking/match/engine.py` + `match/context.py` — pipeline + preload logic.
6. `vn_banking/source/excel.py` + `vn_banking/parser/base.py` — format-driven parsing, HTML-as-xls trap handling.
7. `vn_banking/vn_banking/page/bank_reconcile/bank_reconcile.js` — desk Page controller + component wiring.

See `docs/CODEBASE_DETAIL.md` for one-line-per-file breakdown with key function line numbers.
