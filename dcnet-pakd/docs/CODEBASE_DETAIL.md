# dcnet_pakd — Codebase Detail

File-by-file map. One line per file: purpose + key entry points with line numbers where useful. For narrative overview see `CODEBASE.md`.

## Repo root

- `pyproject.toml` → flit_core build config; declares `required_apps = frappe, erpnext, dcnet_contract, hrms`
- `README.md` → minimal one-liner ("PAKD module")
- `FEATURES.md` → Done / In Progress / Planned matrix. Sections A1 (data model+engine), A2 (3 PAKD types), A3 (approval workflow), A4 (commission posting), A5 (print/reports), A6 (integration tests), A7 (i18n)
- `docs/BUSINESS_LOGIC.md` → pure business doc (roles, 3 PAKD types, workflow, cash-basis rule, TT99/2025 accounts, cutoff, edge cases)
- `docs/specs/` → technical specs (dcnet_pakd-v3.md etc.)

## Outer package `dcnet_pakd/`

- `__init__.py` → `__version__ = "0.1.0"`
- `hooks.py` → app metadata; `required_apps`; `after_install`/`after_migrate` → `install.*`; fixtures (Workspace/Report/Print Format filtered by module "DCNET PAKD"); `doc_events`: Payment Entry.on_submit/on_cancel, DCNET Contract.on_cancel all → `dcnet_pakd.dcnet_pakd.events.*`
- `modules.txt` → single line `DCNET PAKD`
- `patches.txt` → empty (required for `is_frappe_app()` to return True)
- `install.py` (326 L) → `after_install()` / `after_migrate()`:
  - `_ensure_custom_roles()` → creates 7 PAKD Roles
  - `_ensure_settings_singleton()` → initializes PAKD Settings singleton
  - `_seed_settings_defaults()` → cutoff_day, account 6418/6425/3388, salary_component defaults
  - `_seed_default_rule_templates()` → ships baseline Commission Rule Templates
  - `_ensure_pakd_approval_workflow()` → 7-state + 4-route approval Workflow with role permissions

### `dcnet_pakd/tests/`

- `__init__.py` → empty
- `test_engine.py` (155 L) → unit tests for `utils/engine.py` (pure-Python, no bench needed): rule resolution priority, component computation per `base_formula`, edge cases (missing rule, service-only match, contract override)
- `test_chains_b_c.py` (263 L) → integration tests: chain B (PE submit → Commission Line posted, AS + JE draft created), chain C (PE cancel → AS cancel if unused, JE cancel, lines Cancelled). Requires bench test site

### `dcnet_pakd/translations/`

- `vi.csv` → English source → Vietnamese translation pairs for DocType labels, Select options, error messages, button labels (English-first i18n rule per bench CLAUDE.md)

### `dcnet_pakd/utils/`

- `engine.py` (129 L) → **pure rule engine**, no frappe import
  - `resolve_rule(pakd_type, service_type, branch, rules_list)` → 4-tier most-specific match; scoring: pakd_type=1, +service=2, +branch=4, returns highest-scoring rule
  - `compute_pakd_line(...)` → returns dict of per-line cost components (manager_services, add_costs, license_fee, sales_commission, total_cost, revenue_contract, revenue_service). Handles 3 pakd_types (Recurring / FTTH Rollup / One-off). `base_formula` switch: `unit_price` | `unit_price_minus_add_costs` | `add_costs_gross` | `revenue_actual`

### `dcnet_pakd/workspace_sidebar/`

- `dcnet_pakd.json` → Workspace Sidebar fixture. Items: Overview (Workspace=PAKD Module), All PAKD (DocType), Commission Register/Pending PAKD Aging/Profitability reports, Rule Templates, PAKD Settings. Labels in Vietnamese Unicode (sidebar exception per English-first rule)

## Inner module `dcnet_pakd/dcnet_pakd/`

- `__init__.py` → empty
- `events.py` (216 L) → Payment Entry + Contract document event handlers
  - `on_payment_entry_submit(doc, method)` → filters PE Receive type → scans SI references → `_post_commission_for_si()`
  - `on_payment_entry_cancel(doc, method)` → finds Posted Commission Lines with this PE → `_cancel_commission_line()` + `_maybe_cancel_additional_salary()` per affected PAKD
  - `on_contract_cancel(doc, method)` → cancels all Pending Commission Lines on Approved PAKDs linked to the cancelled Contract
  - Internal: `_post_commission_for_si()` finds billing schedule row (state=Paid) → Approved PAKDs → flips Commission Lines (group Lương KD → AS via `integrations.payroll`, group MS/AC/GPVT → draft JE via `integrations.accounting`)

### `doctype/phuong_an_kinh_doanh/` — master DocType

- `phuong_an_kinh_doanh.json` → field order: header (pakd_type, contract_ref, contract_no_external, channel, customer/sales_person/branch/service_type, project_category, company), items (Table → PAKD Item), totals (total_revenue_contract + 7 computed aggregates), commission_lines child table, workflow_state. Not submittable.
- `phuong_an_kinh_doanh.py` →
  - `validate()` — `_validate_contract_not_cancelled`, `_validate_unique_pakd_per_contract` (skipped for Monthly FTTH Rollup), `_sync_commission_overrides`, `_compute_items`, `_compute_totals`, `_sync_commission_lines`
  - `_compute_items()` — resolves rule via `utils/engine.resolve_rule`, builds per-component override map from `commission_overrides` (truthy `override_rate` only), calls `compute_pakd_line` per item with overrides, overwrites computed fields
  - `_compute_totals()` — sums item-level fields into header totals; computes `margin_pct`, `effective_commission_pct` (= total_sales_commission / total_revenue_contract × 100), then `_compute_external_commission()`
  - `_compute_external_commission()` — when `external_commission_recipient_name` is set: if rate filled, computes `external_commission_amount` = rate × total_revenue_contract / 100; then `external_commission_pit` = amount × tax_pct / 100; `external_commission_net` = amount − PIT. Zeroes all three when no recipient.
  - `_sync_commission_overrides()` — keeps `commission_overrides` child table in sync with the matched rule template. Clears the table for Monthly FTTH Rollup (template bypassed). Otherwise ensures one row per component, refreshing `template_rate` from the current rule. User-entered `override_rate` values are preserved (treated as "use template" when 0 or blank since Frappe Percent round-trips empty as 0).
  - `_sync_commission_lines()` — idempotent: keeps `commission_lines` in sync with Contract `billing_schedule` × component totals on every save so Pending preview rows are visible on Draft. Posted rows are preserved untouched; Pending rows are updated in place or dropped when no longer needed. 1 line per (billing_period × component), skipping `month_index=0` (setup fee).
  - `before_print(settings=None)` (inferred, per CLAUDE.md rule) — pre-computes matrix HTML to inject into sandboxed Jinja
- `phuong_an_kinh_doanh.js` (62 L) → form UX only (no formula logic): toggles item columns per `pakd_type`, filters `contract_ref`, refreshes totals readonly

### `doctype/pakd_item/` — worksheet line

- `pakd_item.json` → Child Table. Fields: item_label, uom, qty, unit_price, add_costs_unit_price (for Recurring/One-off); months_billed, months_promo, contract_line_ref, revenue_actual, salary_coefficient (for FTTH Rollup); computed-only (read_only=1): revenue_contract, add_costs, manager_services, license_fee, sales_commission, total_cost, revenue_service
- `pakd_item.py` → 6 L skeleton (no custom logic; all computation happens in parent controller via engine)

### `doctype/pakd_commission_line/` — (period × component)

- `pakd_commission_line.json` → Child Table. Fields: billing_period (month), component (Select: Manager Services / Add Costs / License Fee / Sales Commission), amount, state (Pending / Posted / Cancelled), payment_entry, additional_salary, journal_entry, posted_on
- `pakd_commission_line.py` → 6 L skeleton

### `doctype/pakd_commission_rule_template/` — rate templates

- `pakd_commission_rule_template.json` → scope_pakd_type, scope_service_type, scope_branch, valid_from, valid_to, components (Table → PAKD Rule Component). Date-bounded, 4-tier resolution handled by engine
- `pakd_commission_rule_template.py` → 6 L skeleton

### `doctype/pakd_rule_component/` — rate per component

- `pakd_rule_component.json` → Child Table. component_name (Select: Manager Services / Add Costs / License Fee / Sales Commission), rate (Percent), base_formula (Select: unit_price / unit_price_minus_add_costs / add_costs_gross / revenue_actual)
- `pakd_rule_component.py` → 6 L skeleton

### `doctype/pakd_commission_override/` — per-PAKD rate adjustment

- `pakd_commission_override.json` → Child Table on Phuong An Kinh Doanh. component (Select, same options as PAKD Rule Component), template_rate (Percent, read-only — synced from rule template on every save), override_rate (Percent, optional — blank = use template). Rendered in "Tỷ lệ hoa hồng áp dụng" section, hidden when pakd_type=Monthly FTTH Rollup.
- `pakd_commission_override.py` → skeleton

### `doctype/pakd_settings/` — Single DocType

- `pakd_settings.json` → issubmittable=0, issingle=1. Fields: cutoff_day_of_month, account_manager_services (default 6418), account_add_costs (default 6418), account_license_fee (default 6425), account_offset (default 3388), default_commission_template, salary_component (default "Lương kinh doanh")
- `pakd_settings.py` → 6 L skeleton

### `integrations/`

- `__init__.py` → empty
- `accounting.py` (74 L) → Journal Entry draft creation for non-salary commission components. Groups MS/AC/GPVT lines by period + debit account (from PAKD Settings), creates one draft JE per event: Dr expense acct, Cr offset acct 3388. Writes `journal_entry` ref back to each Commission Line. Does NOT submit — accountant reviews then submits
- `payroll.py` (50 L) → Additional Salary creation for Lương KD lines. Aggregates Sales Commission lines across periods in the same event, creates one Additional Salary for sales_person with `salary_component` from Settings; `payroll_date` = last day of month containing PE date (per cutoff rule). Writes `additional_salary` ref back to each Commission Line. Cancel path: cancels AS if all its linked lines are now Cancelled

### `print_format/` — 3 Jinja templates matching legacy Excel

- `pakd_mau_01/pakd_mau_01.html` (138 L) + `.json` — Mẫu 01: Recurring Telecom. Header block (customer/contract/period), item table with monthly recurring columns, commission calc block, signatures
- `pakd_mau_02/pakd_mau_02.html` (129 L) + `.json` — Mẫu 02: Monthly FTTH Rollup. Multi-contract table, per-row salary_coefficient, monthly totals, branch-level signature
- `pakd_mau_03/pakd_mau_03.html` (137 L) + `.json` — Mẫu 03: One-off Sale / Project. Multi-item table with qty × unit_price, MS/AC breakdown, commission calc, signatures
- All three templates consume the `doc.matrix_html` (or similar) property computed by controller `before_print` to sidestep Frappe's sandboxed Jinja restrictions on `frappe.get_attr`

### `report/` — 3 Script Reports

- `commission_register/commission_register.py` (65 L) + `.json` — recorded commission ledger: filters by date range + sales_person + branch; joins PAKD Commission Line (state=Posted) with PAKD + AS + JE
- `pending_pakd_aging/pending_pakd_aging.py` (63 L) + `.json` — aging of PAKDs in non-terminal workflow states (Draft / Pending *); groups by workflow_state + age bucket (<7 / 7-14 / 14-30 / >30 days)
- `profitability_by_service/profitability_by_service.py` (70 L) + `.json` — gross margin per service_type + branch over period (revenue_contract – total_cost); source is Approved PAKDs only

### `workspace/pakd_module/`

- `pakd_module.json` → Desk Workspace layout: shortcuts (new PAKD, Commission Register), number cards (Pending PAKD count, This-month Commission), links to rule templates + settings. Fixture exported via `hooks.fixtures` module filter

## Dependency graph (at a glance)

```
events.py ──→ integrations/payroll.py ──→ HRMS Additional Salary
          └→ integrations/accounting.py ──→ ERPNext Journal Entry (draft)
          └→ Phuong An Kinh Doanh (find Approved PAKDs, flip Commission Lines)

phuong_an_kinh_doanh.py
    └→ utils/engine.py  (pure: resolve_rule + compute_pakd_line)
    └→ DCNET Contract  (read-only: billing_schedule, package_term_months, ...)

install.py ──→ PAKD Settings (seed), Commission Rule Templates (seed),
                Roles (7), Workflow (7 states, 4 routes)
```

## Non-obvious relationships

- **Contract cancel** → `events.on_contract_cancel` cancels Pending lines only (already Posted lines are preserved — reversal happens via PE cancel).
- **PE cancel** cascades to AS cancel **only if** every other line pointing to that AS is also now Cancelled — partial reversal leaves AS submitted but with flipped line states, which a human must reconcile.
- **Commission Rule Template resolution** is date-filtered *by the caller* before handing the list to `resolve_rule()` — this keeps `engine.py` pure (no frappe import). Controller does the DB filter.
- **FTTH Rollup exception** — `_validate_unique_pakd_per_contract` is skipped for `pakd_type == "Monthly FTTH Rollup"` because one Contract can appear in many monthly rollup PAKDs. Engine also uses `revenue_actual × salary_coefficient` instead of rule-based computation for this type.
- **Sandboxed Jinja workaround** — Print format HTML consumes pre-computed matrix HTML from the doc object via `before_print`, because `frappe.get_attr` / `frappe.call` are unavailable in print Jinja context (bench CLAUDE.md rule).
- **No client-side formula engine** — `phuong_an_kinh_doanh.js` intentionally does not mirror server formulas; all cost fields are read-only and refreshed from server `validate()` on save (single source of truth rule).
