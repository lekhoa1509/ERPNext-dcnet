# einvoice — Codebase Summary

**Lines of code:** ~3,573 (Python: ~1,876 | JS: ~457 | JSON: ~1,240) — excluding docs/tests/__pycache__

## Overview
`einvoice` is a Frappe v16 / ERPNext custom app that integrates ERPNext with Vietnamese e-invoice (HĐĐT) providers. It issues outward invoices from submitted Sales Invoices through provider APIs (signed/filed server-side by the provider per TT 78/2021 & NĐ 123/2020) and periodically syncs inward invoices from provider portals into staging records that can auto-match or create Purchase Invoices. Accountants use it so they never have to log into the provider's web console per invoice.

Current status: Mắt Bão (Mifi) provider is fully implemented. Viettel and MISA are stubs that raise `EInvoiceProviderNotReady` with a Vietnamese error pointing users to contact DCNET.

## Stack
Frappe v16 custom app, Python 3.14, required_apps = `frappe`, `erpnext`. Token cache via Frappe Redis. HTTP via `requests`. No extra pip deps beyond the bench. No JS build bundle — plain client scripts attached via `doctype_js` / `doctype_list_js`.

## Directory tree
```
einvoice/
├── einvoice/                       # inner package (pyproject entry)
│   ├── einvoice/                   # app module (matches modules.txt)
│   │   ├── hooks.py                # app config + scheduler cron
│   │   ├── install.py              # after_install / after_uninstall
│   │   ├── api.py                  # whitelisted API endpoints
│   │   ├── exceptions.py           # EInvoiceError hierarchy
│   │   ├── providers/              # provider strategy plugins
│   │   │   ├── base.py             # BaseProvider (auth cache, HTTP helper, abstract API)
│   │   │   ├── matbao.py           # Mat Bao — full impl (only live provider)
│   │   │   ├── viettel.py          # stub — raises EInvoiceProviderNotReady
│   │   │   └── misa.py             # stub — raises EInvoiceProviderNotReady
│   │   ├── services/
│   │   │   ├── issuance.py         # IssuanceService: single + bulk outward issuance
│   │   │   └── sync.py             # SyncService: scheduled inward sync + auto-match
│   │   ├── tasks/
│   │   │   └── sync_inward_invoices.py   # hook entry point (re-export)
│   │   ├── doctype/                # 5 DocTypes (see Data model)
│   │   ├── number_card/            # 4 KPI cards for workspace
│   │   └── workspace/einvoice/     # EInvoice workspace fixture
│   └── hooks.py                    # (legacy outer — duplicate of inner)
├── docs/
│   └── BUSINESS_LOGIC.md           # pure business rules (TT 78/2021, NĐ 123/2020)
└── (no public/js bundle; JS lives under einvoice/public/js/)
```

## Data model (5 DocTypes)
- **EInvoice Provider** — per-company provider config (tax_code, api_url, api_url_purchase, credentials, default_invoice_pattern/serial, connection_status). One Provider row = one connection to one provider portal for one company.
- **EInvoice Settings** (Single) — global config: default_provider, enable_auto_sync, sync_frequency, match tolerances, default_issue_mode (Draft/Publish), bulk_issuance_limit, default_payment_method, last_sync_*.
- **EInvoice Inward** — staging record for an inward invoice fetched from a provider. Fields: lookup_code (unique key), provider, supplier_name/tax_code, invoice_number/pattern/serial, amounts, status (`New`/`Matched`/`PI Created`/`Ignored`), linked_purchase_invoice.
- **EInvoice Issuance Log** — audit log of outward issuance attempts (success/failure, lookup_code, pdf_url, error_detail).
- **EInvoice Sync Log** — audit log of inward sync runs per provider (fetched/new/dup/errors, date_from/date_to, status).

Custom fields added to core DocTypes by `install.py`:
- Sales Invoice: `einvoice_issued`, `einvoice_provider`, `einvoice_number`, `einvoice_lookup_code`, `einvoice_pdf_url`, `einvoice_issued_at`
- Purchase Invoice: `einvoice_inward` (Link EInvoice Inward), `einvoice_lookup_code`

## Entry points
- `hooks.py`:
  - `scheduler_events.cron["*/15 * * * *"]` → `tasks.sync_inward_invoices.run_if_frequency_match` (also wired to hourly/daily/weekly — the handler itself self-throttles via `FREQ_MAP` + `last_sync_datetime`).
  - `doctype_js`: Sales Invoice + EInvoice Provider form scripts.
  - `doctype_list_js`: Sales Invoice (bulk issue) + EInvoice Inward (manual sync button).
  - `after_install = einvoice.einvoice.install.after_install` — seeds custom fields, Number Cards, default Mat Bao demo provider, Desktop Icon.
  - `add_to_apps_screen` → app card "Hóa đơn điện tử" → `/app/einvoice-settings`, gated by `api.has_app_permission`.
- Whitelisted API (`einvoice.einvoice.api.*`, System Manager + Accounts Manager only):
  - `issue_single_invoice(sales_invoice, provider?, pattern?, serial?, issue_mode?)`
  - `issue_bulk_invoices(sales_invoices, ...)`
  - `get_providers(company?)`
  - `sync_inward_invoices()`
- DocType-level whitelist methods:
  - `EInvoice Provider.test_connection(docname)`, `refresh_templates(docname)`
  - `EInvoice Settings.sync_now()`, `test_connection()`
  - `EInvoice Inward.match_purchase_invoice(pi)`, `create_purchase_invoice()`, `ignore_invoice()`

## Core flows

1. **Issue outward invoice (single)**
   SI (docstatus=1, not yet issued) → form "Xuất hóa đơn đỏ" button →
   `api.issue_single_invoice` → `IssuanceService.issue_single` →
   `_resolve_provider` (by company + Settings.default_provider) →
   `provider.authenticate()` (Redis token cache, TTL ~3500s) →
   `provider.map_sales_invoice_to_payload()` → `provider.issue_outward_invoice()` →
   write `einvoice_*` fields on SI + insert `EInvoice Issuance Log`.

2. **Issue outward invoice (bulk)**
   Sales Invoice list → bulk action → `api.issue_bulk_invoices` →
   `IssuanceService.issue_bulk` → enforce `Settings.bulk_issuance_limit` (default 50) →
   if >5 invoices enqueue `long` queue (timeout 1200s) else run sync →
   loop calling `issue_single` per invoice, collect results.

3. **Sync inward invoices (scheduled)**
   Scheduler every 15 min → `tasks.sync_inward_invoices.run_if_frequency_match` →
   guard: Settings exists + `enable_auto_sync` + elapsed ≥ `FREQ_MAP[sync_frequency]` + Redis distributed lock (key `einvoice_sync_running`, 300s TTL) →
   `SyncService.run_sync(sync_type="Scheduled")` → per enabled provider:
   `fetch_inward_invoices(from_date, to_date)` (default last 30 days) →
   `parse_inward_invoice` → dedupe on `lookup_code` →
   insert `EInvoice Inward` (status=New) →
   `_try_auto_match` on Supplier.tax_id + grand_total within tolerance + posting_date within tolerance → if exactly 1 candidate, set status=Matched + write-back to PI.

4. **Manual sync / manual match / manual create PI**
   EInvoice Inward list has "Cập nhật Hóa đơn đầu vào mới" button calling `api.sync_inward_invoices`.
   On an Inward row, `create_purchase_invoice` picks a Purchase Taxes Template matching the inward tax_rate (fallback: is_default), generates the Supplier if missing, creates a Draft PI with a single line item for the pre-tax total, and alerts the accountant if calculated vs HĐĐT tax differ by >1%.

5. **Cancel outward invoice** — controller method available on provider (`cancel_invoice(invoice_ref, reason)`); UI hook exists in the form script for already-issued invoices. Cancel is permanent in Vietnamese tax law — a replacement is a new independent HĐĐT.

## Provider contract (base.py)
Subclasses must implement: `_do_authenticate`, `fetch_inward_invoices`, `parse_inward_invoice`, `get_invoice_templates`, `issue_outward_invoice`, `cancel_invoice`, `map_sales_invoice_to_payload`. Optional: override `_required_token_types` (Mat Bao uses two: `purchase` + `sales`). All API I/O must go through `self._api_call()` which standardises timeout/HTTP error handling into `EInvoiceProviderError`. Stubs (Viettel, MISA) simply raise `EInvoiceProviderNotReady` everywhere.

## Read first (devs)
1. `docs/BUSINESS_LOGIC.md` — nghiệp vụ HĐĐT Việt Nam, vai trò người dùng, scope, rules outward/inward.
2. `einvoice/einvoice/hooks.py` — app config and scheduler wiring.
3. `einvoice/einvoice/providers/base.py` — the Strategy interface every provider must satisfy.
4. `einvoice/einvoice/providers/matbao.py` — the only complete implementation; use as the template when adding a new provider.
5. `einvoice/einvoice/services/issuance.py` + `services/sync.py` — the two core business flows.
6. `einvoice/einvoice/install.py` — custom fields, Number Cards, and Mat Bao demo credentials that appear on a fresh install.

## Notes & gotchas
- Desktop Icon label is hard-coded `"EInvoice"` ASCII (not Vietnamese) — Frappe v16 `desktop.js` does `workspace_sidebar_item[label.toLowerCase()]` using ASCII keys; Vietnamese would silently disappear.
- Number Card internal names contain Vietnamese diacritics (`SI chưa xuất HĐ đỏ`…), which is fine because Frappe does not slug Number Card names into URLs.
- The bulk issuance "limit" and the "enqueue-if >5" thresholds are independent — the limit rejects the request, the threshold picks sync vs background.
- `_try_auto_match` only links if exactly ONE Purchase Invoice candidate matches (supplier tax_id + grand_total ± tolerance + posting_date ± tolerance). Two candidates = no auto-link, accountant decides manually.
- `_resolve_tax_template` in `EInvoice Inward.create_purchase_invoice` matches by "On Net Total" rate; if it cannot find an exact rate match it falls back to the company's default template and shows a warning — never silently picks the wrong rate.
- All providers share one Redis cache key prefix (`einvoice_token:<provider_name>:<token_type>`), so token invalidation is per-provider.
