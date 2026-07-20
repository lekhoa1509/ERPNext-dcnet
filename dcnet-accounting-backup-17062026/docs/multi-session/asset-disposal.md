# Task: Asset Disposal (Thanh lý TSCĐ)

## Context

vn_accounting is a custom Frappe/ERPNext app providing Vietnamese accounting features (TT99/2025).
The sidebar currently has a "[Pending] Thanh lý" item pointing to an "under-development" placeholder page.
This task implements a dedicated Asset Disposal DocType that wraps ERPNext's depreciation engine with
VN-correct GL entries (separate TK 711 income / TK 811 expense — ERPNet nets to single disposal_account).

Design spec: `docs/superpowers/specs/2026-04-24-asset-disposal-design.md`

## Scope

- Project: `/home/long/long/frappe-bench-dcnet`
- App: `apps/vn_accounting` (inner package: `vn_accounting/vn_accounting/`)
- Branch: create new `feat/asset-disposal` from `main`
- Site: `dcnet.localhost` (port 8001)

### Related Files

**New files to create:**
- `vn_accounting/vn_accounting/doctype/asset_disposal/asset_disposal.json` — DocType schema
- `vn_accounting/vn_accounting/doctype/asset_disposal/asset_disposal.py` — Controller (execute, cancel logic)
- `vn_accounting/vn_accounting/doctype/asset_disposal/asset_disposal.js` — Client script (auto-fill accounts, show/hide fields)
- `vn_accounting/vn_accounting/doctype/asset_disposal/test_asset_disposal.py` — Unit tests
- `vn_accounting/vn_accounting/print_format/asset_disposal_report/asset_disposal_report.json` — Print Format (Biên bản thanh lý)

**Existing files to modify:**
- `vn_accounting/vn_accounting/hooks.py` (~43 lines) — add fixtures for Print Format, doc_events if needed
- `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json` (~170 lines) — add disposal_loss_account + disposal_income_account fields
- `vn_accounting/vn_accounting/setup/company_defaults.py` (~80 lines) — add disposal_account auto-set
- `vn_accounting/vn_accounting/workspace_sidebar/vn_accounting.json` (~800 lines) — update "[Pending] Thanh lý" item
- `vn_accounting/vn_accounting/translations/vi.csv` (~347 lines) — add disposal translations

## Requirements

### Phase 1: Planning

1. Read the design spec at `docs/superpowers/specs/2026-04-24-asset-disposal-design.md`
2. Read ERPNext asset disposal code to understand the API:
   - `apps/erpnext/erpnext/assets/doctype/asset/depreciation.py` — `depreciate_asset()` (line ~474), `scrap_asset()` (line ~362), `reverse_depreciation_entry_made_on_disposal()`, `reset_depreciation_schedule()`, `get_depreciation_accounts()` (line ~710)
   - `apps/erpnext/erpnext/assets/doctype/asset/asset.py` — Asset schema, `make_sales_invoice()` (line ~1093)
3. Write implementation plan to `docs/plans/2026-04-24-asset-disposal-plan.md` with exact file paths, code blocks, and task ordering
4. Self-review plan: check spec coverage (every spec section maps to a task), placeholder scan (no TBD/TODO), type consistency (field names match across tasks)
5. Fix any gaps found in self-review
6. Commit plan file

### Phase 2: DocType Schema + Settings

1. Create `Asset Disposal` DocType JSON with fields as specified in the design spec:
   - **Asset Information section:** asset (Link→Asset, mandatory), asset_name (Data, read only, fetch_from), asset_category (Link→Asset Category, read only), company (Link→Company, read only), disposal_date (Date, mandatory, default today), disposal_type (Select: Sell/Scrap, mandatory), status (Select: Draft/Executed/Cancelled, default Draft)
   - **Asset Values section:** gross_purchase_amount (Currency, read only), accumulated_depreciation (Currency, read only), book_value (Currency, read only)
   - **Sale Details section** (depends_on disposal_type=Sell): selling_amount (Currency, mandatory_depends_on), buyer (Link→Customer, mandatory_depends_on)
   - **Accounting Entries section:** fixed_asset_account (Link→Account), accumulated_depreciation_account (Link→Account), disposal_loss_account (Link→Account), disposal_income_account (Link→Account, depends_on disposal_type=Sell)
   - **Details section:** disposal_reason (Small Text), participants (Small Text)
   - **References section** (read only): journal_entry (Link→Journal Entry), sales_invoice (Link→Sales Invoice)
   - Naming: `AD-.YYYY.-.#####`
   - Permissions: Accounts Manager (full), Accounts User (read, write, create, execute — no delete)
   - Module: VN Accounting
   - All field labels in English (Vietnamese via translations)

2. Add 2 fields to VN Accounting Settings JSON after the `forecast_section`:
   - New section break: "Asset Disposal" 
   - `disposal_loss_account` (Link→Account, label "Disposal Loss Account", description "Default TK 811")
   - Column break
   - `disposal_income_account` (Link→Account, label "Disposal Income Account", description "Default TK 711")

3. Add `disposal_account` auto-set in `company_defaults.py`:
   - In both `_get_defaults_large()` and `_get_defaults_small()`, add `"disposal_account": "811"`
   - This ensures Company.disposal_account is set for ERPNet compatibility

4. Run `bench migrate` and verify DocType created successfully

### Phase 3: Controller (Python)

1. Create `asset_disposal.py` with controller class `AssetDisposal`:
   - `validate()`: check asset is submitted (docstatus=1), not already Sold/Scrapped, disposal_date not in future, disposal_date >= asset.purchase_date. If Sell: validate selling_amount > 0 and buyer is set.
   - `execute()` (@frappe.whitelist method): the main action button handler
     - **For both Sell and Scrap:**
       - Import `depreciate_asset` from `erpnext.assets.doctype.asset.depreciation`
       - Call `depreciate_asset(asset_doc, self.disposal_date, "Asset disposed via Asset Disposal")` for pro-rata depreciation
       - Reload asset to get updated values
       - Create writeoff JE using account fields from the form (NOT from Company/Settings):
         ```
         Debit: accumulated_depreciation_account = accumulated_depreciation_amount
         Debit: disposal_loss_account = book_value (only if book_value > 0)
         Credit: fixed_asset_account = gross_purchase_amount
         ```
       - Submit JE
       - Update Asset: `disposal_date`, `journal_entry_for_scrap = je.name`
       - Set asset status: "Scrapped" (scrap) or "Sold" (sell) via `asset.db_set("status", ...)`
     - **For Sell only (after JE):**
       - Create SI (Draft, NOT submitted — kế toán reviews first):
         - item_code from asset.item_code (or create generic service item if missing)
         - income_account = self.disposal_income_account (TK 711 from form)
         - customer = self.buyer
         - rate = self.selling_amount
         - Do NOT set is_fixed_asset on SI item (avoid ERPNet disposal double-booking)
       - Save `self.sales_invoice = si.name`
     - Save `self.journal_entry = je.name`, `self.status = "Executed"`
   - `cancel_disposal()` (@frappe.whitelist method): reverse everything
     - If Sell: validate SI is cancelled first (if exists and submitted)
     - Cancel JE
     - Import `reverse_depreciation_entry_made_on_disposal`, `reset_depreciation_schedule` from ERPNet
     - Call both to restore depreciation state
     - Clear Asset: `disposal_date`, `journal_entry_for_scrap`, restore status
     - Set `self.status = "Cancelled"`

2. Keep controller under 300 lines. If longer, extract JE/SI creation into a helper module `disposal_utils.py`.

### Phase 4: Client Script (JS)

1. Create `asset_disposal.js`:
   - On `asset` change: fetch asset data (asset_name, asset_category, company, gross_purchase_amount, value_after_depreciation), calculate book_value, fetch accounts from Asset Category via `get_depreciation_accounts` and from VN Accounting Settings
   - On `disposal_type` change: show/hide Sale Details section and disposal_income_account field
   - Add **"Execute"** custom button (visible when status=Draft): calls `execute` method
   - Add **"Cancel"** custom button (visible when status=Executed): calls `cancel_disposal` method
   - Filter `asset` field: `[["docstatus", "=", 1], ["status", "not in", ["Sold", "Scrapped", "Capitalized"]]]`
   - Filter account fields: `[["company", "=", frm.doc.company], ["is_group", "=", 0]]`

### Phase 5: Print Format + Sidebar + Translations

1. Create Print Format `asset_disposal_report`:
   - Jinja template with `custom_format = 1`
   - Layout per design spec: header (CHXHCNVN), biên bản title, asset info table, disposal details, signature block
   - Follow existing `cash_count_report` pattern for JSON structure
   - Embed HTML directly in the JSON `html` field (not separate .html file — required for fixture import per CLAUDE.md rules)

2. Update workspace sidebar JSON:
   - Find the item with `"label": "[Pending] Thanh lý"` 
   - Change to: `"label": "Thanh lý"`, `"link_to": "Asset Disposal"`, `"link_type": "DocType"`

3. Add translations to `vi.csv`:
   ```
   Asset Disposal,Thanh lý TSCĐ
   Disposal Type,Hình thức thanh lý
   Sell,Bán
   Scrap,Hủy
   Book Value,Giá trị còn lại
   Gross Purchase Amount,Nguyên giá
   Accumulated Depreciation,Khấu hao lũy kế
   Disposal Reason,Lý do thanh lý
   Participants,Thành viên hội đồng thanh lý
   Selling Amount,Giá bán
   Buyer,Người mua
   Disposal Loss Account,TK chi phí thanh lý
   Disposal Income Account,TK thu nhập thanh lý
   Fixed Asset Account,TK tài sản cố định
   Accumulated Depreciation Account,TK hao mòn lũy kế
   Execute,Thực hiện thanh lý
   Asset Disposal Report,Biên bản thanh lý TSCĐ
   Disposal Date,Ngày thanh lý
   Sale Details,Chi tiết bán
   Accounting Entries,Tài khoản hạch toán
   Asset Information,Thông tin tài sản
   Asset Values,Giá trị tài sản
   ```

4. Update `hooks.py`:
   - Add Print Format fixture: `{"dt": "Print Format", "filters": [["doc_type", "=", "Asset Disposal"]]}`
   - Add to `app_include_js` if needed (likely not — standard DocType form)

5. Run `bench build --app vn_accounting && bench migrate && bench clear-cache`

### Phase 6: QA + Fix Bugs

1. Login to `dcnet.localhost:8001` via Playwright MCP tools
2. Navigate to Asset Disposal list view — verify it loads
3. Create a new Asset Disposal:
   - Select an existing submitted Asset
   - Verify auto-fill: asset_name, company, gross_purchase_amount, accumulated_depreciation, book_value, accounts
   - Verify account fields are editable
4. Test Scrap flow:
   - Set disposal_type = Scrap, click Execute
   - Verify JE created with correct accounts (check GL entries)
   - Verify Asset status = "Scrapped"
   - Verify Asset Disposal status = "Executed"
   - Test Cancel: verify JE cancelled, Asset restored
5. Test Sell flow:
   - Create new Asset Disposal, disposal_type = Sell
   - Set selling_amount and buyer
   - Click Execute
   - Verify JE (writeoff) + SI (draft) created
   - Verify SI has correct income_account (711) and customer
   - Verify Asset status = "Sold"
6. Test Print Format:
   - Open Asset Disposal, Menu → Print → select "Biên bản thanh lý TSCĐ"
   - Verify layout renders correctly
7. Verify sidebar: "Thanh lý" item navigates to Asset Disposal list
8. Fix any bugs found — commit each fix atomically

### Phase 7: Design QA

1. Navigate each key screen via Playwright MCP (form view, list view, print preview)
2. Review across 4 dimensions: layout, UX, edge cases visual, console errors
3. Implement cosmetic fixes autonomously (spacing, labels, alignment)
4. Log structural UX proposals to `docs/design-qa-proposals/asset-disposal.md`
5. Commit fixes atomically

## Acceptance Criteria

- [ ] `Asset Disposal` DocType exists and `bench migrate` passes
- [ ] `bench build --app vn_accounting` completes without errors
- [ ] VN Accounting Settings has `disposal_loss_account` and `disposal_income_account` fields
- [ ] Company defaults auto-set `disposal_account = 811` for VN companies
- [ ] Scrap flow: Execute creates JE with Nợ 214 + Nợ 811 / Có 211, Asset status = "Scrapped"
- [ ] Scrap flow: Cancel reverses JE, restores Asset status and depreciation schedule
- [ ] Sell flow: Execute creates writeoff JE (Nợ 214 + Nợ 811 / Có 211) + draft SI (income_account = 711)
- [ ] Sell flow: SI does NOT have is_fixed_asset set (no ERPNet double-booking)
- [ ] Account fields on form are editable and auto-filled from Asset Category + Settings
- [ ] Print Format "Biên bản thanh lý TSCĐ" renders with correct layout
- [ ] Sidebar item changed from "[Pending] Thanh lý" to "Thanh lý" → DocType link
- [ ] Translations added to vi.csv for all new user-visible strings
- [ ] QA with Playwright MCP: verify form load, execute scrap, execute sell, print preview, sidebar navigation on dcnet.localhost:8001
- [ ] Design QA (`/design-qa`): exploratory review of Asset Disposal form, list view, print preview via Playwright MCP. Implement cosmetic fixes autonomously. Append structural UX proposals to `docs/design-qa-proposals/asset-disposal.md` (with `## Session YYYY-MM-DD` header). Commit fixes atomically.
- [ ] All changes committed with descriptive messages

## Constraints

- Do NOT modify ERPNet core files (`apps/erpnext/`, `apps/frappe/`)
- Do NOT use `is_fixed_asset` on SI items created for sell flow (prevents ERPNet double-booking)
- Do NOT hardcode account numbers in Python — always read from form fields (which are auto-filled from Settings/Category but editable)
- Controller file must stay under 500 lines — extract helpers if needed
- All field labels in English, Vietnamese via translations/vi.csv only
- Print Format HTML must be embedded in the JSON fixture `html` field (not separate .html file)
- Workspace sidebar JSON update must use `link_type: "DocType"` (not Page or URL)

## Verification Commands

```bash
cd /home/long/long/frappe-bench-dcnet && bench build --app vn_accounting
cd /home/long/long/frappe-bench-dcnet && bench --site dcnet.localhost migrate
cd /home/long/long/frappe-bench-dcnet && bench --site dcnet.localhost execute "frappe.get_meta('Asset Disposal').fields"
cd /home/long/long/frappe-bench-dcnet && bench --site dcnet.localhost execute "frappe.get_single_value('VN Accounting Settings', 'disposal_loss_account')"
```

## Agent Persona

You are a senior Frappe/ERPNext developer building Vietnamese accounting features. Key rules:
- Stay at bench root (`/home/long/long/frappe-bench-dcnet`). Use absolute paths.
- `bench migrate` after any DocType JSON changes. `bench build --app vn_accounting` after JS/CSS changes. `bench clear-cache` after hooks.py changes.
- All field labels in English. Vietnamese only in translations/vi.csv and workspace sidebar labels.
- Use `frappe.db.sql("... WHERE x=%s", [val])` parameterized queries, never f-strings in SQL.
- Read the design spec first: `apps/vn_accounting/docs/superpowers/specs/2026-04-24-asset-disposal-design.md`
- For ERPNet API: import from `erpnext.assets.doctype.asset.depreciation` — functions `depreciate_asset`, `get_depreciation_accounts`, `reverse_depreciation_entry_made_on_disposal`, `reset_depreciation_schedule`.
- Print Format fixture: embed HTML in JSON `html` field. Fixture import does NOT run load_code_properties.
- `frappe.db.set_value()` bypasses on_update hooks — use `doc.db_set()` for same effect but be aware of cache implications.
- Commit early, commit often. Don't batch all commits to end of session.

## Model

auto

## Time Budget

- Session minutes: 25
- Max sessions: 6
