# dcnet_pakd — Codebase Summary

**Lines of code:** 3,220 (Python: 1,201 | Tests: 418 | JS: 62 | JSON: 1,135 | HTML: 404) — excluding docs

## Overview
PAKD (Phương Án Kinh Doanh) — sales commission worksheet for DCNET, digitizing 3 legacy Excel templates (Mẫu 01/02/03). Thin-layer architecture on top of `dcnet_contract`: Contract owns billing schedule & cash collection, PAKD owns commission policy + approval workflow + cash-basis commission posting. Rule engine computes commission server-side (single source of truth — no client-side formula engine). Posts commission via Additional Salary (Lương KD) + draft Journal Entry (Manager Services / Add Costs / Phí GPVT), triggered by Payment Entry submission on the linked Contract's Sales Invoices.

## Stack
Frappe v16 + ERPNext v16 + required apps: `dcnet_contract >= 0.1.0`, `hrms`

## Directory tree
```
dcnet_pakd/
├── docs/
│   ├── BUSINESS_LOGIC.md                       # nghiệp vụ thuần tuý (dành cho GĐKD/KTT/BGĐ)
│   └── specs/                                   # spec kỹ thuật (dcnet_pakd-v3.md ...)
├── FEATURES.md                                  # Done / In Progress / Planned matrix
├── README.md
├── pyproject.toml
└── dcnet_pakd/                                  # outer package
    ├── hooks.py                                 # app config, doc_events on Payment Entry + Contract
    ├── install.py                               # after_install/after_migrate: roles, settings, default rules, workflow
    ├── modules.txt · patches.txt · __init__.py
    ├── tests/
    │   ├── test_engine.py                       # rule engine pure function tests
    │   └── test_chains_b_c.py                   # commission posting chain (PE→AS+JE) + cancel flow
    ├── translations/vi.csv                      # English-first i18n
    ├── utils/engine.py                          # pure rule engine (no frappe import)
    ├── workspace_sidebar/dcnet_pakd.json
    └── dcnet_pakd/                              # inner module package
        ├── events.py                            # on_payment_entry_submit/cancel, on_contract_cancel
        ├── doctype/
        │   ├── phuong_an_kinh_doanh/            # main DocType (workflow_state, not submittable)
        │   ├── pakd_item/                       # child: worksheet line items
        │   ├── pakd_commission_line/            # child: (period × component) tracking
        │   ├── pakd_commission_rule_template/   # rate templates (service/branch/pakd_type)
        │   ├── pakd_rule_component/             # child: rate components (MS/AC/GPVT/Lương KD)
        │   └── pakd_settings/                   # singleton: cutoff, accounts, defaults
        ├── integrations/
        │   ├── accounting.py                    # Journal Entry draft creation for MS/AC/GPVT
        │   └── payroll.py                       # Additional Salary creation for Lương KD
        ├── print_format/
        │   ├── pakd_mau_01/pakd_mau_01.html    # Recurring Telecom
        │   ├── pakd_mau_02/pakd_mau_02.html    # Monthly FTTH Rollup
        │   └── pakd_mau_03/pakd_mau_03.html    # One-off Sale / Project
        ├── report/
        │   ├── commission_register/             # hoa hồng đã ghi nhận
        │   ├── pending_pakd_aging/              # PAKD chờ duyệt theo tuổi
        │   └── profitability_by_service/       # lãi gộp theo loại dịch vụ
        └── workspace/pakd_module/               # Desk workspace layout
```

## Data model (6 DocTypes)
- **Phuong An Kinh Doanh** — master worksheet. Naming `PAKD-.YYYY.-.#####`. Not submittable (uses `workflow_state`). `contract_ref` → DCNET Contract, `pakd_type` in {Recurring Telecom, Monthly FTTH Rollup, One-off Sale/Project}, fetched fields: customer / sales_person / branch / service_type / company.
- **PAKD Item** (child) — worksheet rows. Input: qty, unit_price, add_costs_unit_price (+ revenue_actual, salary_coefficient for FTTH Rollup). Computed (server-only): revenue_contract, add_costs, manager_services, license_fee, sales_commission, total_cost, revenue_service.
- **PAKD Commission Line** (child) — one row per (billing_period × component). State: Pending → Posted → Cancelled. Tracks `payment_entry`, `additional_salary`, `journal_entry` per line for granular reversal.
- **PAKD Commission Rule Template** — rate config scoped by (pakd_type, service_type, branch), date-bounded (valid_from/valid_to). 4-tier resolution: contract override → branch+service → service → pakd_type default.
- **PAKD Rule Component** (child of rule template) — per-component rate (Manager Services / Add Costs / Phí GPVT / Lương KD) with `base_formula` in {unit_price, unit_price_minus_add_costs, add_costs_gross, revenue_actual}.
- **PAKD Settings** (Single) — cutoff_day_of_month, default accounts (6418/6425/3388), `salary_component` name, default rule template.

7 custom roles: `PAKD Sales Rep`, `PAKD Sales Director HCM`, `PAKD Sales Director HN`, `PAKD General Department`, `PAKD Branch Director HN`, `PAKD Board`, `PAKD Accountant`.

## Entry points
- **hooks.py** — `doc_events`:
  - `Payment Entry.on_submit` → `events.on_payment_entry_submit` (post commission lines for paid SI)
  - `Payment Entry.on_cancel` → `events.on_payment_entry_cancel` (reverse posted commission)
  - `DCNET Contract.on_cancel` → `events.on_contract_cancel` (cancel pending commission)
  - `after_install` / `after_migrate` → `install.*` (seed roles, settings singleton, default rule templates, approval workflow)
  - Fixtures exported: Workspace, Report, Print Format (module = "DCNET PAKD")
- **Rule engine** — `utils/engine.py`:
  - `resolve_rule(pakd_type, service_type, branch, rules_list)` — 4-tier most-specific match (pure function, no DB)
  - `compute_pakd_line(...)` — per-line cost computation; pure Python, no frappe import (fully unit-testable)
- **Controller** — `doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.py`:
  - `validate()` → contract-not-cancelled + unique-PAKD-per-contract + `_compute_items()` + `_compute_totals()`
  - `on_update()` → on `workflow_state == "Approved"` generates commission lines (Pending state)
- **Integrations** — `integrations/accounting.py` (Journal Entry draft for MS/AC/GPVT), `integrations/payroll.py` (Additional Salary for Lương KD)
- **Client JS** — `phuong_an_kinh_doanh.js` (62 lines) — form UX only, no formula logic

## Core flows

1. **Create PAKD** — NVKD picks `pakd_type` + `contract_ref` → form fetches customer/sales_person/branch/service_type from Contract → fills items (input-only: qty, unit_price, add_costs_unit_price, or revenue_actual + salary_coefficient for FTTH Rollup) → on save, server rule engine resolves template and computes all cost fields on items + header totals.
2. **Submit & approve** — Draft → Pending GĐ TT KD → Pending P. Tổng hợp → (Pending GĐ CN HN for HN-branch) → Pending BGĐ → Approved. On Approved, `on_update()` generates PAKD Commission Lines (one per billing_period × component, state=Pending). Rejected returns to Draft; any earlier commission lines are Cancelled.
3. **Post commission (cash-basis, via Payment Entry)** — When a PE is submitted and pays a Sales Invoice tied to the Contract's billing schedule row (state=Paid):
   - For each affected billing period, find Approved PAKD's Commission Lines for that period.
   - Lương KD lines → aggregated into one Additional Salary (component = "Lương kinh doanh"), `payroll_date` = cutoff of the month covering the PE date.
   - Manager Services / Add Costs / Phí GPVT lines → one Journal Entry in **Draft** (Dr expense acct 6418/6425, Cr 3388) for accountant review.
   - Commission Lines flip Pending → Posted, storing `payment_entry`, `additional_salary`, `journal_entry` refs.
   - PE cancel reverses: cancels AS if fully unused, cancels JE, flips lines Posted → Cancelled.
4. **Print Mẫu 01 / 02 / 03** — one Jinja HTML template per `pakd_type`. Computed HTML matrix injected via `before_print` hook on the controller (to bypass the Frappe sandboxed Jinja limitation for heavy computation). Rendered tables mirror the legacy Excel layout for legal continuity.

## Read first
1. `docs/BUSINESS_LOGIC.md` — nghiệp vụ thuần tuý (3 loại PAKD, workflow, cash-basis rule, TT99/2025 accounts)
2. `dcnet_pakd/hooks.py` — doc_events wiring + fixtures
3. `dcnet_pakd/dcnet_pakd/doctype/phuong_an_kinh_doanh/phuong_an_kinh_doanh.py` — main controller
4. `dcnet_pakd/utils/engine.py` — pure rule engine (`resolve_rule`, `compute_pakd_line`)
5. `dcnet_pakd/dcnet_pakd/events.py` — PE→commission posting chain (the hardest flow)
6. `dcnet_pakd/dcnet_pakd/integrations/{accounting,payroll}.py` — AS + JE creation
7. `dcnet_pakd/dcnet_pakd/print_format/pakd_mau_*/pakd_mau_*.html` — 3 print layouts
