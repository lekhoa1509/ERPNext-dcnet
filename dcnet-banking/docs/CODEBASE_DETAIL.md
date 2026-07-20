# vn_banking — Codebase Detail

One line per file, grep-friendly. Organized by directory. Line numbers for key functions are indicative (source may drift between releases).

## Repo root
- `README.md` → install + quickstart
- `FEATURES.md` → Done / In Progress / Planned feature matrix
- `pyproject.toml` → flit_core build config, package metadata
- `.gitignore`, `.github/` → CI config (dcnet-cloud gitflow workflows)

## docs/
- `BUSINESS_LOGIC.md` → pure business workflow (accountant perspective); xuất phát điểm
- `USAGE.md` → end-user step-by-step guide for Bank Reconcile page
- `SETTINGS.md` → Bank Statement Settings field reference
- `specs/` → technical specs YYYY-MM-DD-*.md
- `CODEBASE.md` → summary (this project's index file)
- `CODEBASE_DETAIL.md` → this file

## vn_banking/ (inner package, top level)
- `hooks.py` → app config; after_install/after_migrate; app_include_js/css = bank_reconcile.bundle; fixtures: Format, Matcher Type, Data Source, Custom Field (filtered to Bank Transaction-% and Bank Account-%)
- `install.py` → after_install():L5, after_migrate():L10 — creates custom fields via custom.custom_fields.create_all(), seeds default match rules
- `tasks.py` → scheduler_events stub (commented in hooks, reserved for v2 API sync)
- `test_match_engine.py` → legacy integration test for full match pipeline (341 lines)
- `__init__.py` → `__version__`
- `modules.txt` → "VN Banking"
- `patches.txt` → empty (required for is_frappe_app())

## vn_banking/api/
- `reconcile.py` → all whitelisted HTTP endpoints for Bank Reconcile page
  - `detect_format_and_bank(file_url)`:L24 — auto-detect Format + resolve Bank Account from uploaded file
  - `trigger_import(bank_account, source_type, file_url, ...)`:L45 — ingestion entry; sync (<200 rows) or async via frappe.enqueue
  - `_run_ingest_and_match()`:L101 — fetch → dedupe → insert Bank Transaction → run match engine → publishes realtime progress
  - `get_import_transactions()`:L166 — load txns with suggested_invoices child rows
  - `create_payment_entry()`:L234 — create PE; multi-invoice refs; TT99/2025 fee write-off via Settings.tolerance + difference_account; sets mode_of_payment explicitly
  - `bulk_create_pe()`:L303 — batch PE creation for high-confidence matches; idempotent on Reconciled
  - `explain_match()`:L346 — human-readable explanation of which matcher fired
  - `trigger_rematch()`:L363 — re-run match engine without re-parsing (for config changes)
- `webhook.py` → v2 API source scaffold (not wired); placeholder for Open Banking push integration

## vn_banking/parser/
- `base.py` → file readers: `read_xlsx_rows()`:L6 (openpyxl, NOT read_only to preserve merged cells), `read_xls_rows()`:L21 (xlrd), `read_html_rows()`:L30 (pandas + bs4 for PG Bank HTML-as-xls), `_is_html_disguised_as_xls()`:L51 (checks first 256 bytes for <), `read_rows()`:L59 (dispatcher with auto HTML detection)
- `detect.py` → `detect_format()`:L5 — scoring heuristic: bank name (+10), column positions (+1/+2), date parse (+5); returns best Bank Statement Format record
- `normalizer.py` → `parse_date()`:L8, `parse_amount()`:L18, `compute_dedupe_hash()`:L40 (SHA-256 over date|amount|ref|description)

## vn_banking/source/
- `base.py` → `NormalizedTransaction` dataclass:L9 (date, deposit, withdrawal, description, ref, counter_account_no, counter_account_name); `BankDataSource` ABC:L28 (fetch(), validate_config())
- `excel.py` → `ExcelFileSource`:L28 — reads Bank Statement Format config; resolves columns via `_col_index()`:L12 (letter like "A"/"B" OR header text); yields NormalizedTransaction; skips footer/balance rows

## vn_banking/match/
- `base.py` → `InvoiceRef` dataclass:L7; `MatchCandidate` dataclass:L14 (invoice, allocated_amount, confidence); `BaseMatcher` ABC:L26 (applicable(txn, ctx), match(txn, ctx))
- `context.py` → `MatchContext` dataclass:L11; `build_context()`:L36 — preloads outstanding SI/PI + bank_account_no → party map (one DB hit per import batch)
- `engine.py` → `run_match_engine()`:L60 — first-hit-wins pipeline; `get_enabled_rules_in_priority_order()`:L25, `instantiate_matcher()`:L11 (via handler_path from Bank Matcher Type), `pick_best()`:L33, `apply_to_txn()`:L42 (writes suggested_invoices child rows, sets match_confidence)
- `helpers.py` → field adapters that work on Document or plain dict: `get_txn_amount`, `get_txn_direction`, `get_txn_bank_ref`, `get_txn_description`, `is_matched`
- `invoice_no.py` → `InvoiceNoMatcher`:L8 — regex on description (patterns from Settings.invoice_patterns) → invoice lookup → confidence by amount diff (High/Medium/Low)
- `invoice_amount.py` → `InvoiceAmountMatcher`:L7 — unique outstanding amount match within tolerance; ambiguity guard (returns no match if >1 hit)
- `party_amount.py` → `PartyAmountMatcher`:L8 — uses counter_account_no → party map; supports single invoice or combinations_sum_match multi-invoice combo
- `name_amount.py` → `NameAmountMatcher`:L7 — rapidfuzz partial_ratio (≥80) on description vs party name + amount match; capped at Low confidence
- `combinations.py` → `combinations_sum_match()`:L7 — returns smallest k-combination summing to target within tolerance (itertools.combinations, k=2..4)

## vn_banking/custom/
- `custom_fields.py` → `BANK_TRANSACTION_FIELDS`:L5 (import link, dedupe_hash, match_confidence, matched_by, suggested_invoices Table fieldtype); `BANK_ACCOUNT_FIELDS`:L34 (v2 API sync fields, placeholder); `create_all()`:L51 — creates Custom Field records via frappe.custom.doctype.custom_field.custom_field.create_custom_fields

## vn_banking/fixtures/
- `bank_statement_format.json` → BIDV, MB Bank, Sacombank, PG Bank Format records with column mapping + detection hints
- `bank_matcher_type.json` → registry: invoice_no, invoice_amount, party_amount, name_amount → handler_path Python class
- `bank_data_source.json` → registry: excel (active), api_v2 (scaffold)

## vn_banking/translations/
- `vi.csv` → 100 English → Vietnamese pairs for all UI strings, field labels, Select options

## vn_banking/workspace/
- `banking_vn/banking_vn.json` → desk sidebar: links to Bank Reconcile page + Bank Statement Import + Bank Statement Settings + Bank Statement Format

## vn_banking/page/bank_reconcile/
*Note: this directory is a partial/legacy layout; the actual active page lives under `vn_banking/vn_banking/page/bank_reconcile/`. The components here are kept for reference.*
- `components/bulk_actions_bar.js` → legacy bulk actions bar component (40 lines, superseded by version in vn_banking/vn_banking/page/...)

## vn_banking/vn_banking/page/bank_reconcile/ (the active Frappe Page)
- `bank_reconcile.json` → Page DocType metadata (module, title, standard=Yes)
- `bank_reconcile.py` → Page controller stub (Frappe requires one)
- `bank_reconcile.html` → page shell markup
- `bank_reconcile_main.html` → main body template (header, stat bar placeholder, txn table, side panel)
- `bank_reconcile.css` → page-specific overrides beyond the bundle
- `bank_reconcile.js` → page controller; state init; bank account picker; Upload/Re-match actions; subscribes to realtime progress events; wires components together (153 lines)
- `components/upload_dialog.js` → `open_upload_dialog()`:L4 — file attach widget + auto-detect format/bank on upload + triggers trigger_import (145 lines)
- `components/txn_table.js` → `init_txn_table()`:L4, `load_transactions()`:L11, `render_txns()`:L24 — main transaction table with confidence dots (High=green, Medium=amber, Low=red), selectable rows (306 lines)
- `components/txn_side_panel.js` → `render_side_panel()`:L6 — txn detail + party/invoice selection + Create PE action buttons (6 lines, imports implementation)
- `components/stat_bar.js` → `render_stats()`:L6 — summary strip (matched / suggested / unmatched / difference)
- `components/bulk_actions_bar.js` → `init_bulk_actions()`:L4 — bulk create draft PEs + bulk submit; wired to confidence filter (63 lines)

## vn_banking/vn_banking/doctype/
- `bank_statement_format/bank_statement_format.json|.py` → per-bank parser config DocType (column mapping, date/number formats, data start row)
- `bank_statement_import/bank_statement_import.json|.py` → import batch record (bank_account, file, status, counts); NOT submittable — workflow container
- `bank_statement_settings/bank_statement_settings.json|.js|.py` → Single DocType: tolerance, difference_account (bank fee write-off per TT99/2025 → 6415/6425/6427), default PE action, invoice-number regex patterns
- `bank_match_rule/bank_match_rule.json|.py` → child table row: matcher_type (Link) + priority (Int) + enabled (Check)
- `bank_matcher_type/bank_matcher_type.json|.py` → registry: matcher key + handler_path (Python class dotted path)
- `bank_data_source/bank_data_source.json|.py` → registry: source key + handler_path (Excel now, API v2 scaffold)
- `bank_txn_invoice_suggestion/bank_txn_invoice_suggestion.json|.py` → child table on Bank Transaction: invoice_type, invoice_name, allocated_amount, confidence, selected, explanation

## vn_banking/public/
- `js/bank_reconcile.bundle.js` → 5-line esbuild entry; imports the page controller + components from vn_banking/vn_banking/page/bank_reconcile/
- `css/bank_reconcile.bundle.css` → 1-line entry (imports page CSS)
- `dist/js/bank_reconcile.bundle.<HASH>.js` → built artifact; Frappe auto-looks up via assets.json (do NOT append ?version=)
- `dist/css/bank_reconcile.bundle.<HASH>.css` → built artifact

## vn_banking/tests/
- `__init__.py` → test package marker
- `fixtures/bidv_sample.xls`, `mb_sample.xlsx`, `sacombank_sample.xls`, `pgbank_sample.xls` → real bank export samples used by parser tests
- `test_parser_all_formats.py` → parser tests across 4 bank formats; asserts column mapping + date/amount parsing + dedupe hash (61 lines)
- `test_source_excel.py` → ExcelFileSource integration; uses bank sample fixtures (62 lines)
- `test_dedupe.py` → SHA-256 collision tests + cross-file re-upload dedup (47 lines)
- `test_matcher_invoice_no.py` → regex + confidence tiers (55 lines)
- `test_matcher_invoice_amount.py` → unique amount within tolerance + ambiguity guard (71 lines)
- `test_matcher_party_amount.py` → counter_account → party → single/combo invoices (63 lines)
- `test_matcher_name_amount.py` → rapidfuzz ≥80 + amount (38 lines)
- `test_matcher_combinations.py` → combinations_sum_match k=2..4 (38 lines)
- `test_engine_pipeline.py` → full pipeline first-hit-wins + preload context (36 lines)
- `test_reconcile_api.py` → API endpoint smoke tests (12 lines)
- (legacy) `vn_banking/test_match_engine.py` → older integration test outside the tests/ directory (341 lines)

## scripts/
- Utility scripts for dev (inspect sample files, rebuild fixtures). Not part of the shipped app.
