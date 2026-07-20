# einvoice — Codebase Detail

Grep-friendly file map. One line per file. Line numbers point to key entry points.

## einvoice/ (inner package root)
- hooks.py → app metadata; `doctype_js`:L19, `doctype_list_js`:L24, `scheduler_events`:L29 (cron `*/15 *`), `after_install`:L46, `fixtures`:L49

## einvoice/einvoice/ (app module)
- __init__.py → `__version__ = "0.0.1"`
- modules.txt → `EInvoice`
- hooks.py → (inner duplicate) app config; `scheduler_events`:L29, `add_to_apps_screen`:L9, `fixtures`:L49
- install.py → `after_install()`:L181, `_create_number_cards()`:L224, `_seed_matbao_provider()`:L234, `_ensure_desktop_icon()`:L190, `after_uninstall()`:L263, constants `CUSTOM_FIELDS`:L5 (SI + PI custom fields), `NUMBER_CARDS`:L108, `MATBAO_PROVIDER`:L163 (demo creds)
- api.py → whitelisted REST endpoints; `has_app_permission()`:L14, `issue_single_invoice()`:L20, `issue_bulk_invoices()`:L27, `get_providers()`:L34, `sync_inward_invoices()`:L49
- exceptions.py → error hierarchy; `EInvoiceError`:L13, `EInvoiceProviderError`:L22, `EInvoiceProviderNotReady`:L30, `EInvoiceValidationError`:L38, `EInvoiceTaxTemplateError`:L43

## einvoice/einvoice/providers/
- __init__.py → Strategy registry; `PROVIDER_MAP`:L7 (Matbao/Viettel/MISA → dotted path), `get_provider_class()`:L14
- base.py → abstract `BaseProvider(ABC)`:L18; `__init__()`:L21, `_cache_key()`:L35, `_get_cached_token()`:L38, `_set_cached_token()`:L42, `authenticate()`:L51, `_do_authenticate_cached()`:L77, `_required_token_types()`:L88, `_api_call()`:L96 (timeout/HTTPError/ConnectionError → EInvoiceProviderError); abstract: `_do_authenticate`:L142, `fetch_inward_invoices`:L153, `parse_inward_invoice`:L158, `get_invoice_templates`:L163, `issue_outward_invoice`:L168, `cancel_invoice`:L173, `map_sales_invoice_to_payload`:L178
- matbao.py → `MatbaoProvider(BaseProvider)`:L18 (only live impl); `_required_token_types()`:L21 (purchase+sales), `_do_authenticate()`:L27, `_authenticate_purchase()`:L38 (POST `/auth/token`), `_authenticate_sales()`:L63 (POST `/api/auth/login`), `_get_auth_headers()`:L89, `fetch_inward_invoices()`:L100 (GET `/hoa-don-dau-vao/load-data-tct`), `parse_inward_invoice()`:L125, `_map_invoice_type()`:L157, `get_invoice_templates()`:L166, `issue_outward_invoice()`:L180 (POST `/api/invoice/create-invoice`), `cancel_invoice()`:L211, `map_sales_invoice_to_payload()`:L226 (TT 78 payload), `_get_item_tax_rate()`:L292
- viettel.py → `ViettelProvider(BaseProvider)`:L7 — stub; every method raises `EInvoiceProviderNotReady("Viettel")`
- misa.py → `MisaProvider(BaseProvider)`:L7 — stub; every method raises `EInvoiceProviderNotReady("MISA")`

## einvoice/einvoice/services/
- __init__.py → empty
- issuance.py → `IssuanceService`:L29; `issue_single()`:L32 (validates docstatus=1 + not yet issued, resolves provider, calls `issue_outward_invoice`, writes SI einvoice_* fields + Issuance Log), `issue_bulk()`:L108 (enforces `bulk_issuance_limit`, enqueues long queue if >5); helpers: `_resolve_provider()`:L152 (by company + Settings.default_provider), `_create_issuance_log()`:L180, `_process_bulk_issuance()`:L195, `log_einvoice_error()`:L19
- sync.py → scheduler entry + sync engine; `FREQ_MAP`:L18 (15min→900s … Weekly→604800s), `run_if_frequency_match()`:L37 (self-throttle + Redis lock `einvoice_sync_running` 300s TTL), `SyncService`:L81 + `run_sync()`:L84, `_sync_provider()`:L173 (fetch → parse → dedupe on lookup_code → insert Inward → try auto-match), `_try_auto_match()`:L235 (Supplier.tax_id + grand_total±tol + posting_date±tol, link only if exactly 1 match), `_create_sync_log()`:L279, `log_einvoice_error()`:L27

## einvoice/einvoice/tasks/
- __init__.py → thin re-export of `run_if_frequency_match` + `SyncService` from services/sync.py; `run_sync()`:L11
- sync_inward_invoices.py → hook entry point target; re-exports `run_if_frequency_match`, `run_sync`:L5

## einvoice/einvoice/doctype/einvoice_provider/
- einvoice_provider.json → DocType schema; fields: provider_name (unique, autoname), provider_type (Select Matbao/Viettel/MISA/Custom), enabled, company (Link), tax_code, api_url, api_url_purchase, auth_method, api_token/api_username/api_password/api_key, default_invoice_pattern, default_invoice_serial, connection_status, last_tested
- einvoice_provider.py → controller; `EInvoiceProvider`:L11, `get_provider_instance()`:L14, module whitelisted: `test_connection(docname)`:L22 (calls provider.authenticate, updates connection_status), `refresh_templates(docname)`:L54
- __init__.py → empty

## einvoice/einvoice/doctype/einvoice_settings/
- einvoice_settings.json → Single DocType; fields: default_provider (Link), enable_auto_sync (Check), sync_frequency (Select Every 15 Min/Hourly/Every 6 Hours/Daily/Weekly), sync_start_time, default_date_range_days, last_sync_datetime, last_sync_status, last_sync_error, match_total_tolerance_pct, match_date_tolerance_days, default_issue_mode (Draft/Publish), default_payment_method, bulk_issuance_limit, sync_now_btn, test_connection_btn
- einvoice_settings.py → controller; `EInvoiceSettings`:L5, whitelisted `sync_now()`:L9 (enqueue long queue), `test_connection()`:L22
- __init__.py → empty

## einvoice/einvoice/doctype/einvoice_inward/
- einvoice_inward.json → staging record; autoname `EINV-IN-{####}`; fields: company, provider, provider_type, provider_invoice_id, lookup_code (unique), invoice_number/pattern/serial, invoice_date, invoice_type, supplier_name/tax_code/address, total_before_tax/tax_rate/tax_amount/total_amount/currency, status (New/Matched/PI Created/Ignored), linked_purchase_invoice (Link PI), error_message, sync_batch_id, raw_data (JSON), pdf_url
- einvoice_inward.py → controller; `EInvoiceInward`:L6, `validate()`:L9 (auto-calc tax_rate), whitelisted `match_purchase_invoice(pi)`:L18, `create_purchase_invoice()`:L35 (picks tax template, creates Supplier if needed, creates Draft PI, warns on >1% tax diff), `_resolve_tax_template()`:L86 (match by "On Net Total" rate, fallback is_default), `_get_or_create_supplier()`:L152, `ignore_invoice()`:L170
- __init__.py → empty

## einvoice/einvoice/doctype/einvoice_issuance_log/
- einvoice_issuance_log.json → audit log; autoname `ISS-{####}`; fields: provider (Link), sales_invoice (Link), company, issued_at, status (Success/Failed), provider_invoice_number, provider_lookup_code, provider_pdf_url, error_detail
- einvoice_issuance_log.py → stub controller (no business logic)
- __init__.py → empty

## einvoice/einvoice/doctype/einvoice_sync_log/
- einvoice_sync_log.json → audit log; autoname `SYNC-{####}`; fields: provider (Link), company, sync_type (Manual/Scheduled), start_time, end_time, date_from, date_to, total_fetched, new_created, duplicates_skipped, errors, status (Success/Partial/Failed), error_detail
- einvoice_sync_log.py → stub controller (no business logic)
- __init__.py → empty

## einvoice/einvoice/number_card/
- si_chưa_xuất_hđ_đỏ/si_chưa_xuất_hđ_đỏ.json → Number Card "SI chưa xuất HĐ đỏ" — Count Sales Invoice (docstatus=1, einvoice_issued=0)
- si_đã_xuất_hđ_đỏ/si_đã_xuất_hđ_đỏ.json → Number Card "SI đã xuất HĐ đỏ" — Count Sales Invoice (docstatus=1, einvoice_issued=1)
- hđ_mua_vào___chưa_ghép/hđ_mua_vào___chưa_ghép.json → Number Card — Count EInvoice Inward (status=New)
- hđ_mua_vào___đã_ghép/hđ_mua_vào___đã_ghép.json → Number Card — Count EInvoice Inward (status in Matched/PI Created)

## einvoice/einvoice/workspace/einvoice/
- einvoice.json → EInvoice workspace fixture (exported by `fixtures` hook with `module="EInvoice"` filter)

## einvoice/public/js/
- sales_invoice.js → Sales Invoice form script; adds "Xuất hóa đơn đỏ" button when `docstatus==1 && !einvoice_issued` (refresh:L7), headline PDF link when issued (L19), dialog to pick provider + pattern + serial + issue_mode
- sales_invoice_list.js → list view bulk action "Xuất hóa đơn đỏ hàng loạt"; filters selected rows for `docstatus==1 && !einvoice_issued` (L30), enforces single-company (L43), calls `api.get_providers` then `api.issue_bulk_invoices`
- einvoice_provider.js → Provider form script; "Kiểm tra kết nối" button (refresh:L9), "Lấy mẫu hóa đơn" button (L14), warns on stub Viettel/MISA (provider_type handler:L19), `_update_status_color`, `_suggest_provider_name`
- dcnet_inward_invoice_list.js → EInvoice Inward list view; "Cập nhật Hóa đơn đầu vào mới" inner button → `api.sync_inward_invoices` with freeze dialog + result summary

## Top-level repo files
- pyproject.toml → Python packaging (flit_core), name `einvoice`
- README.md → 2-line placeholder
- .gitignore → standard Python ignores
- docs/BUSINESS_LOGIC.md → pure business logic (HĐĐT legal framework, roles, outward/inward rules, provider concept, TT 78/2021 pattern/serial conventions, draft vs publish, bulk rules, sync throttling rules)

## Cross-cutting notes (grep targets)
- Frappe v16 custom field creation → `install.py::CUSTOM_FIELDS` (SI + PI)
- Vietnamese error text (user-facing) → `frappe.throw(...)` / `frappe.msgprint(...)` / `EInvoiceProviderNotReady.__init__` (L33 exceptions.py)
- Redis keys used → `einvoice_token:<provider>:<type>` (base.py:L36), `einvoice_sync_running` (sync.py:L70)
- Permission gate → `frappe.only_for(["System Manager", "Accounts Manager"])` in every whitelisted endpoint
- HTTP timeouts → default 30s (base.py:L112); inward sync uses 60s (matbao.py:L117); outward issue uses 60s (matbao.py:L185)
- Stub provider pattern → raise `EInvoiceProviderNotReady(<name>)` in every abstract method (viettel.py, misa.py)
