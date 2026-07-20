# dcnet_contract — Codebase Summary

**Lines of code:** ~7,200 (Python: 3,228 | Tests: 1,407 | JS: 532 | JSON: 1,880 | HTML: 87) — excluding docs

## Overview

Master Contract management for DCNet (ISP + Data Center, B2B-only): recurring services (P2P, MPLS, ILL, FTTH DN/HGD, IT Managed, Colocation) and one-off sales (VTTB equipment, Thi công). The Contract DocType owns the billing schedule, pro-rata calculation, DOCX/HTML template engine, print formats, approval workflow, and emits "customer paid" events for `dcnet_pakd` to compute commission.

Architecture: **Option D** — a pure Contract DocType is the master for recurring; for One-off VTTB a hidden "shadow" Sales Order is auto-created on submit to reuse ERPNext's Delivery Note + stock flow.

## Stack

Frappe v16 + ERPNext v16. Python 3.14. Submittable DocType. DOCX/PDF via python-docx + LibreOffice subprocess. Dual-language (EN/VI) placeholder engine using unidecode.

## Directory tree

```
dcnet_contract/
  README.md
  FEATURES.md
  pyproject.toml
  docs/
    BUSINESS_LOGIC.md
    CODEBASE.md            ← this file
    CODEBASE_DETAIL.md     ← per-file detail
    specs/
    plans/
  dcnet_contract/
    hooks.py               ← scheduler, doc_events, permission_query
    install.py             ← after_install / after_migrate (438 LOC)
    number_card_methods.py
    patches.txt
    modules.txt
    dcnet_contract/        ← inner module (Frappe nested package layout)
      events.py            ← Payment Entry on_submit / on_cancel
      tasks.py             ← daily cron: auto_invoice, overdue, expire
      shadow_so.py         ← shadow Sales Order for One-off VTTB
      permissions.py       ← permission_query_conditions for Sales Order
      doctype/
        dcnet_contract/                       ← master (406 LOC controller)
        dcnet_contract_template/              ← DOCX/HTML template master
        dcnet_contract_billing_schedule/      ← child table (periods)
        dcnet_contract_item/                  ← child table (line items)
        dcnet_contract_template_item/         ← child (template line items)
        dcnet_contract_template_placeholder/  ← child (placeholder registry)
        dcnet_contract_branch_cc_map/         ← child (branch → cost center)
        dcnet_contract_settings/              ← Single (defaults, accounts)
      utils/
        billing_schedule.py     ← pure schedule generator (pro-rata)
        state_machine.py        ← allowed transitions
        template_engine.py      ← HTML placeholder fill
        docx_generator.py       ← DOCX fill + PDF export (676 LOC)
        placeholder_engine.py   ← EN/VI dual-language placeholder map
      report/
        contract_expiry_report/
        outstanding_receivables_by_contract/
      print_format/
        hop_dong_chuan/         ← standard contract
        phu_luc_hop_dong/       ← contract appendix
      templates/docx/           ← 6 .docx boilerplate files (FTTH HGD/DN, ILL, MPLS, P2P, dich vu)
      dashboard_chart/          ← contracts_by_status, monthly_contract_value, revenue_by_service_type
      number_card/              ← active_contracts, overdue_amount, expiring_this_month, total_monthly_revenue
      workspace/dcnet_contract/
      translations/
    tests/                       ← 6 test modules, ~1,407 LOC
    translations/vi.csv
    workspace_sidebar/dcnet_contract.json
```

## Data model (7 DocTypes + 1 Single)

- **DCNet Contract** — master, submittable. Status: Draft / Active / Suspended / Cancelled / Expired / Revised.
- **DCNet Contract Item** — child table of line items (service/product, qty, unit_price, item_label).
- **DCNet Contract Billing Schedule** — child table; one row per billing period (setup fee row = month_index=0, service rows = 1..N). State: Projected → Invoiced → Paid.
- **DCNet Contract Template** — master; stores `template_html` + optional `template_docx` file. Admin/legal owned.
- **DCNet Contract Template Item** — child of Template (default line items).
- **DCNet Contract Template Placeholder** — child of Template (registered placeholder keys).
- **DCNet Contract Branch CC Map** — child of Settings (branch → cost center mapping).
- **DCNet Contract Settings** (Single) — default accounts, VAT, rounding mode, grace period, etc.

## Entry points

- **hooks.py** (dcnet_contract/hooks.py):
  - `scheduler_events.daily`: `tasks.run_auto_invoice`, `run_overdue_check`, `run_expire_contracts`
  - `doc_events["Payment Entry"]`: `events.on_payment_entry_submit`, `events.on_payment_entry_cancel`
  - `permission_query_conditions["Sales Order"]`: hide shadow SO from non-admin
  - `after_install` / `after_migrate`: seed templates, settings, custom fields, roles, workspace, desktop icon
- **DCNetContract controller** (`doctype/dcnet_contract/dcnet_contract.py`):
  - `validate()` → item/type/service/value validations + totals + end_date
  - `before_print()` → render `contract_html_rendered` + `appendix_html`
  - `on_submit()` → transition Draft→Active, generate billing schedule, create shadow SO (if VTTB), sync customer data, revise old contract if amended_from
  - `on_cancel()` → cancel schedule + shadow SO, status → Cancelled
- **Template engine** — HTML fill (`utils/template_engine.py`), DOCX fill + LibreOffice PDF (`utils/docx_generator.py`), EN/VI placeholder resolver (`utils/placeholder_engine.py`)
- **Billing schedule generator** — pure function `utils/billing_schedule.py::generate_schedule(ScheduleInput) → [ScheduleRow]`
- **Whitelisted JS helpers** — `dcnet_contract.js` + `dcnet_contract_template_integration.js` (client-side template apply, placeholder guide, print buttons)

## Core flows

1. **Contract creation (template → doc)** — NVKD picks a DCNet Contract Template → `apply_template` fills `contract_html` with `{{EN}}` / `{{VI}}` placeholders via `placeholder_engine.resolve_placeholder` + `template_engine.fill_html_placeholders`. Sales can edit the HTML inline.
2. **Submit (Draft → Active)** — `validate()` + `before_submit()` (acceptance_date required) + `on_submit()`: `billing_schedule.generate_schedule()` produces setup fee row + N service rows with pro-rata for first/last month; `shadow_so.create_shadow_so()` runs for One-off VTTB; customer CMND/address synced.
3. **Recurring billing (daily cron)** — `tasks.run_auto_invoice` queries `billing_schedule` rows where `state='Projected' AND due_date <= today AND c.docstatus=1 AND c.status='Active'`, groups by contract, creates Sales Invoice(s), flips rows `Projected → Invoiced`.
4. **Payment received** — `events.on_payment_entry_submit` finds SIs in PE references; flips matching billing_schedule rows `Invoiced → Paid` when SI fully paid (Prepay: all rows flip together since they share one SI). `on_payment_entry_cancel` reverts.
5. **One-off sale** — Contract + shadow SO created on submit → operations uses SO to create Delivery Note → SI → PE. SO is read-only, hidden from non-admin via `permission_query_conditions`.
6. **Print / DOCX export** — `before_print()` sets `contract_html_rendered`; print format `hop_dong_chuan` renders HTML; `docx_generator.export_docx()` fills .docx template and converts to PDF via LibreOffice.
7. **State lifecycle** — `utils/state_machine.ALLOWED` enforces transitions (Active→Suspended, Suspended→Active, Active→Expired via `run_expire_contracts` cron, Active→Cancelled via `on_cancel`, Active→Revised via `amended_from`).

## Tests (1,407 LOC, 6 modules)

- `test_billing_schedule.py` — pro-rata, rounding, prepay vs monthly
- `test_state_machine.py` — allowed/disallowed transitions
- `test_placeholder_engine.py` — EN/VI dual-lookup, typo detection
- `test_template_engine.py` — HTML placeholder fill
- `test_docx_generator.py` — DOCX fill, items table cloning, number-to-words
- `test_tasks_and_events.py` — auto_invoice, overdue, expire, PE payment events

## Read first (when onboarding)

1. `docs/BUSINESS_LOGIC.md` — full Vietnamese business spec (canonical)
2. `dcnet_contract/hooks.py` — scheduler + event wiring
3. `dcnet_contract/dcnet_contract/doctype/dcnet_contract/dcnet_contract.py` — master controller
4. `dcnet_contract/dcnet_contract/utils/billing_schedule.py` — pure schedule generator
5. `dcnet_contract/dcnet_contract/tasks.py` + `events.py` — daily cron + PE integration
6. `dcnet_contract/dcnet_contract/utils/placeholder_engine.py` — EN/VI placeholder map
7. `docs/CODEBASE_DETAIL.md` — per-file catalog

## Conventions

- English-first for all labels/options/messages; Vietnamese via `translations/vi.csv`.
- Workspace/desktop icon: `title = name` (ASCII), `link_to` must be set on Desktop Icon.
- `before_print` precomputes HTML on doc (Jinja sandbox cannot call Python).
- Seed functions (`install.py::_seed_docx_templates`) compare disk vs DB content before skipping.
- Shadow SO hidden via `permission_query_conditions`, NOT by role — one source of truth on the Contract.
