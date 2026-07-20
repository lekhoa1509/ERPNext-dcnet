# dcnet_contract — Codebase Detail

Per-file catalog. One line per file. See `CODEBASE.md` for high-level architecture.

## Repo root

- `pyproject.toml` — flit_core build, Python 3.14, ruff config (line-length 110)
- `README.md` — install + quick start
- `FEATURES.md` — Done / In Progress / Planned matrix
- `docs/BUSINESS_LOGIC.md` — canonical Vietnamese business spec (roles, contract types, lifecycle, pro-rata rules)
- `docs/specs/` — technical specs (DocType schema, API contracts, edge cases)
- `docs/plans/` — implementation plans per sprint
- `docs/CODEBASE.md` — codebase summary
- `docs/CODEBASE_DETAIL.md` — this file

## dcnet_contract/ (outer package)

- `__init__.py` — `__version__ = "0.1.0"`
- `hooks.py` — app config; scheduler (daily: auto_invoice, overdue_check, expire_contracts); Payment Entry doc_events; Sales Order permission_query; after_install/after_migrate
- `install.py` (438 LOC) — seed roles (DCNet Sales Rep, Sales Manager, Contract Template Manager), Settings Single, shadow SO custom field, Customer CMND fields, contract templates, DOCX templates, workspace/sidebar/desktop icon; dual-format template migration
- `number_card_methods.py` (48 LOC) — Python methods backing the 4 number cards
- `modules.txt` — "DCNet Contract"
- `patches.txt` — empty (required by Frappe)

## dcnet_contract/dcnet_contract/ (inner module)

### Top-level Python

- `events.py` (96 LOC) — `on_payment_entry_submit(doc, method)` flips billing_schedule rows Invoiced→Paid for SIs paid fully; `on_payment_entry_cancel` reverts Paid→Invoiced; `_process_si_payment(si_name, pe_name)` per-SI matcher
- `tasks.py` (190 LOC) — `run_auto_invoice()` creates SIs grouped by contract from due Projected rows; `run_overdue_check()` flags overdue billing; `run_expire_contracts()` transitions Active→Expired past end_date
- `shadow_so.py` (82 LOC) — `create_shadow_so(contract)` for One-off VTTB; `cancel_shadow_so(contract)`; `_should_create_shadow_so()` gate (One-off + VTTB)
- `permissions.py` (17 LOC) — `so_permission_query(user)` hides `is_shadow_contract=1` SOs from non-admin users

### DocTypes (8 total)

#### dcnet_contract/ (master, submittable)

- `dcnet_contract.json` — master schema (customer, branch, service_type, contract_type, payment_mode, package_term_months, acceptance_date, unit_price_total, setup_fee, currency, items, billing_schedule, status, contract_html, template, amended_from, cost_center, etc.)
- `dcnet_contract.py` (406 LOC) — DCNetContract controller: validate (items, service↔type, value>0), before_submit (acceptance_date required), on_submit (Draft→Active, generate schedule, shadow SO, sync customer, revise old), on_cancel (cancel schedule + SO), before_print (render HTML/appendix); constants `RECURRING_SERVICES`, `ONEOFF_SERVICES`
- `dcnet_contract.js` (327 LOC) — form UI: status badges, action buttons (Suspend/Resume/Expire/Cancel/Renew), print/export buttons, placeholder guide dialog, items table helpers
- `dcnet_contract_template_integration.js` (85 LOC) — template picker + "Apply Template" flow (fills `contract_html`)

#### dcnet_contract_template/ (master)

- `dcnet_contract_template.json` — schema (template_name, service_type, contract_type, template_html, template_docx, items, placeholders, is_active)
- `dcnet_contract_template.py` (197 LOC) — DCNetContractTemplate controller: validate placeholders, auto-populate placeholder list from template_html, expose `apply_to_contract(contract_name)`
- `dcnet_contract_template.js` (54 LOC) — template form UI, placeholder guide button

#### Child tables

- `dcnet_contract_billing_schedule/dcnet_contract_billing_schedule.json` — child (month_index, period_start, period_end, due_date, item_type, amount, state, is_prorated, sales_invoice, payment_entry)
- `dcnet_contract_billing_schedule/dcnet_contract_billing_schedule.py` (8 LOC) — stub controller (logic lives in billing_schedule.py + tasks.py)
- `dcnet_contract_item/dcnet_contract_item.{json,py}` (6 LOC) — child (item_label, qty, unit_price, item_code, amount)
- `dcnet_contract_template_item/dcnet_contract_template_item.{json,py}` (5 LOC) — child (item_label, default_qty, default_unit_price)
- `dcnet_contract_template_placeholder/dcnet_contract_template_placeholder.{json,py}` (6 LOC) — child (key_en, key_vi, source, example, group)
- `dcnet_contract_branch_cc_map/dcnet_contract_branch_cc_map.{json,py}` (6 LOC) — child of Settings (branch, cost_center)

#### Settings (Single)

- `dcnet_contract_settings/dcnet_contract_settings.json` — Single schema (default_income_account, default_receivable_account, default_cost_center, default_vat_rate, rounding_mode, grace_period_days, branch_cc_mapping)
- `dcnet_contract_settings/dcnet_contract_settings.py` (9 LOC) — stub controller

### utils/ (pure logic, TDD)

- `billing_schedule.py` (137 LOC) — `ScheduleInput`, `ScheduleRow` dataclasses; `generate_schedule(inp)` → list[ScheduleRow]; `_add_months()`, pro-rata calc (ROUND_HALF_UP / ROUND_HALF_EVEN), setup fee row (month_index=0)
- `state_machine.py` (17 LOC) — `ALLOWED: dict[(current, target), action]` + `assert_transition(current, target)`; covers Draft/Active/Suspended/Cancelled/Expired/Revised
- `template_engine.py` (125 LOC) — `fill_html_placeholders(html, values)` regex replace `{{key}}`; `collect_contract_values(contract)` builds value dict from contract + customer + company
- `placeholder_engine.py` (474 LOC) — `PLACEHOLDER_MAP` (EN key → {vi label, source, example, group}); `resolve_placeholder(raw_key)` handles EN + VI + unidecode typo detection; `generate_bilingual_guide()` for UI; grouping (Bên A / Bên B / Hợp đồng / Dịch vụ / Thanh toán)
- `docx_generator.py` (676 LOC) — DOCX template fill via python-docx: paragraph + table placeholder replace, items table row cloning, Vietnamese `number_to_words()`, LibreOffice subprocess → PDF; `generate_html_for_print()` + `generate_appendix_html_for_print()` fallback for contracts without template
- `__init__.py` — empty

### Reports

- `report/contract_expiry_report/contract_expiry_report.{json,js,py}` (80 LOC py) — Script Report: contracts expiring in next N days, filters by company/branch/status
- `report/outstanding_receivables_by_contract/outstanding_receivables_by_contract.{json,js,py}` (75 LOC py) — Script Report: unpaid billing_schedule rows grouped by contract + customer, aging buckets

### Print formats

- `print_format/hop_dong_chuan/hop_dong_chuan.{json,html}` — standard contract print: renders `{{ doc.contract_html_rendered }}` pre-computed in `before_print()`
- `print_format/phu_luc_hop_dong/phu_luc_hop_dong.{json,html}` — contract appendix (phụ lục): renders `{{ doc.appendix_html }}`

### DOCX templates (seeded into File DocType)

- `templates/docx/hd-dich-vu-vien-thong.docx` — generic telecom service contract
- `templates/docx/hd-ftth-doanh-nghiep.docx` — FTTH business contract
- `templates/docx/hd-ftth-ho-gia-dinh.docx` — FTTH household (valid per 2026-04-16 review)
- `templates/docx/pl-internet-leased-line-ill.docx` — ILL appendix
- `templates/docx/pl-kenh-thue-rieng-p2p.docx` — P2P appendix
- `templates/docx/pl-truyen-so-lieu-mpls.docx` — MPLS appendix

### Workspace & UI fixtures

- `workspace/dcnet_contract/dcnet_contract.json` — workspace layout (number cards, charts, shortcuts); `title` = `name` (ASCII)
- `dashboard_chart/contracts_by_status/` — chart (Group By status)
- `dashboard_chart/monthly_contract_value/` — chart (Sum unit_price_total by month)
- `dashboard_chart/revenue_by_service_type/` — chart (Sum by service_type)
- `number_card/active_contracts/` — count docstatus=1 status=Active
- `number_card/contracts_expiring_this_month/` — count end_date in current month
- `number_card/overdue_amount/` — sum overdue billing_schedule rows
- `number_card/total_monthly_revenue/` — sum SI for current month linked to contracts

### Translations

- `translations/vi.csv` — EN→VI translations for all user-facing strings (field labels, Select options, error messages, button labels); merged by Frappe at runtime

## dcnet_contract/workspace_sidebar/

- `dcnet_contract.json` — sidebar fixture: entries for Contracts, Templates, Billing Schedule (list view), Reports, Settings; label in VN Unicode, link_to ASCII

## dcnet_contract/translations/

- `vi.csv` — alternate location for translations (app-level); Frappe loads from both

## dcnet_contract/tests/ (1,407 LOC, 6 modules)

- `tests/__init__.py` — empty
- `tests/helpers.py` (94 LOC) — fixture builders: `make_customer()`, `make_contract(service_type, contract_type, ...)`, `make_template()`, cleanup helpers
- `tests/test_billing_schedule.py` (175 LOC) — pure generator: Monthly pro-rata first/last month, Prepay single row, OneOff, setup fee row, rounding modes (Half-up vs Bankers), edge cases (acceptance on 1st of month, 31-day months, leap Feb)
- `tests/test_state_machine.py` (62 LOC) — allowed transitions happy path, disallowed transitions raise ValueError
- `tests/test_placeholder_engine.py` (108 LOC) — EN lookup, VI lookup, unidecode typo fallback (e.g. "ten khach hang" → "customer_name"), unknown key passthrough
- `tests/test_template_engine.py` (53 LOC) — `fill_html_placeholders` with EN+VI mixed, `collect_contract_values` structure
- `tests/test_docx_generator.py` (226 LOC) — paragraph fill, table fill, items row cloning, Vietnamese number-to-words, PDF export via LibreOffice (skipped if `soffice` not in PATH)
- `tests/test_tasks_and_events.py` (401 LOC) — integration: `run_auto_invoice` creates SI for due Projected rows, groups by contract; `run_overdue_check` flags overdue; `run_expire_contracts` transitions past-end contracts; PE submit flips rows to Paid; PE cancel reverts; Prepay all-rows-flip-together

## Key file hotspots

- Largest source files: `docx_generator.py` (676), `placeholder_engine.py` (474), `install.py` (438), `dcnet_contract.py` controller (406), `tasks.py` (190), `dcnet_contract_template.py` (197)
- Largest test: `test_tasks_and_events.py` (401 LOC — most integration coverage)
- Most hit-every-session: `hooks.py`, `doctype/dcnet_contract/dcnet_contract.py`, `utils/billing_schedule.py`, `tasks.py`, `events.py`

## External integrations

- **ERPNext Sales Invoice** — created by `tasks.run_auto_invoice` from billing_schedule rows
- **ERPNext Payment Entry** — consumed via `events.on_payment_entry_submit/cancel`
- **ERPNext Sales Order** — shadow SO for One-off VTTB (read-only, hidden via permission_query)
- **ERPNext Customer** — synced CMND/CCCD + address fields via custom fields (seeded in `install.py`)
- **LibreOffice (soffice)** — subprocess for DOCX → PDF in `docx_generator.py`
- **python-docx** — DOCX manipulation
- **unidecode** — Vietnamese diacritic normalization for placeholder typo detection
- **dcnet_pakd** (downstream consumer) — listens to "customer paid" signal (via Payment Entry doc_events chain, not direct coupling)
