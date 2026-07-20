# Task: Implement Cash Count (Kiểm kê quỹ tiền mặt)

## Context

vn_accounting app needs a Cash Count feature — cashiers physically count cash in the vault, compare with GL book balance, and record differences. When discrepancies exist, the system creates Journal Entries following the VAS 2-step process: Step 1 records the difference to pending accounts (1381/3381), Step 2 resolves it (employee compensation, management expense, other income, or return). This is a mandatory accounting procedure per Vietnamese regulations (Mẫu 08a-TT200/2014).

## Scope

- Project: `/home/long/long/frappe-bench-dcnet/apps/vn_accounting`
- Branch: create new `feature/cash-count` from `main`
- Design spec: `docs/superpowers/specs/2026-04-16-cash-count-design.md` (read this FIRST)

### Related files

| File | Purpose | Action |
|------|---------|--------|
| `vn_accounting/vn_accounting/doctype/` | DocType directory | Create `cash_count/` and `cash_count_denomination/` |
| `vn_accounting/vn_accounting/doctype/vn_accounting_settings/vn_accounting_settings.json` | Settings DocType (14 fields) | Add 5 new fields (cash_surplus_account, cash_deficit_account, employee_receivable_account, management_expense_account, other_income_account) |
| `vn_accounting/vn_accounting/report_utils.py` (~101 lines) | Shared GL query utils | Reuse `get_opening_balance(accounts, from_date, company)` at L86 |
| `vn_accounting/treasury/journal_entry_builder.py` (~239 lines) | JE creation pattern | Reuse `_create_je(company, posting_date, accounts, remark, ...)` at L15 |
| `vn_accounting/hooks.py` (~40 lines) | App hooks | No doc_events needed (Cash Count is regular, not submittable) |
| `vn_accounting/workspace_sidebar/vn_accounting.json` | Sidebar nav | Insert "Kiểm kê quỹ" item in Quỹ tiền mặt section |
| `vn_accounting/translations/vi.csv` (119 lines) | Vietnamese translations | Add ~32 new entries |
| `vn_accounting/vn_accounting/doctype/term_deposit/term_deposit.py` | Reference pattern | Status transitions via `db_set()`, whitelisted methods |
| `vn_accounting/vn_accounting/doctype/term_deposit/term_deposit.js` | Reference pattern | Button addition via `frm.add_custom_button()` |

## Requirements

### Phase 1: Write Implementation Plan

Read the design spec at `docs/superpowers/specs/2026-04-16-cash-count-design.md`. Write a detailed implementation plan to `docs/superpowers/plans/2026-04-16-cash-count-plan.md` with:
- Ordered task list with exact file paths and code outlines
- Self-review the plan (3-point checklist: spec coverage, placeholder scan, type consistency)
- Fix any issues found inline
- Commit the plan

### Phase 2: DocTypes + Settings

**Cash Count Denomination** (child table):
- Fields: `denomination` (Int, reqd), `quantity` (Int, reqd), `amount` (Currency, read_only, formula)
- Module: VN Accounting

**Cash Count** (regular DocType, NOT submittable):
- All fields per spec §2.1 (company, cash_account, count_date, count_type, reason, book_balance, show_denomination, denominations, actual_amount, difference, difference_type, difference_account, save_as_default, pending_je, resolution_je, resolution_status, resolution_type, resolution_target_account, cashier, chief_accountant, director, remarks, status)
- Status options: `Draft\nCounted\nApproved\nClosed\nPending Resolution\nResolved`
- Permissions: Accounts User (read+write+create, write only if status=Draft), Accounts Manager (full)
- Module: VN Accounting
- Naming: `CC-.YYYY.-.#####`

**VN Accounting Settings** — add new section "Cash Count" after alerts_section:
- `cash_count_section` (Section Break, label "Cash Count")
- `cash_surplus_account` (Link → Account, label "Cash Surplus Account")
- `cash_deficit_account` (Link → Account, label "Cash Deficit Account")
- `column_break_cash_count`
- `employee_receivable_account` (Link → Account, label "Employee Receivable Account")
- `management_expense_account` (Link → Account, label "Management Expense Account")
- `other_income_account` (Link → Account, label "Other Income Account")

After creating DocTypes: `bench --site dcnet.localhost migrate`

### Phase 3: Controller (cash_count.py)

**Python controller** at `vn_accounting/vn_accounting/doctype/cash_count/cash_count.py`:

1. **`validate()`**:
   - Recalc `book_balance` from GL (reuse `report_utils.get_opening_balance`)
   - If `show_denomination`: sum denominations → `actual_amount`
   - Calc `difference = actual_amount - book_balance`
   - Set `difference_type`: Balanced (==0), Surplus (>0), Deficit (<0)
   - Auto-fill `difference_account` from Settings based on `difference_type`
   - If `save_as_default` and `difference_account`: write back to Settings
   - If `count_type == "Unscheduled"` and no `reason`: throw
   - Auto-set `resolution_status`: "Not Applicable" if balanced, "Pending" if not

2. **`get_book_balance()`** — `@frappe.whitelist()` standalone method (not on class):
   - Params: `cash_account`, `count_date`, `company`
   - Query GL balance for single account up to count_date
   - Return float

3. **Status transition methods** (all `@frappe.whitelist()` on controller):
   - `mark_counted()`: validate actual_amount is set + cashier filled → `db_set("status", "Counted")`
   - `approve()`: validate chief_accountant + director filled → `db_set("status", "Approved")`. If difference==0 → auto `db_set("status", "Closed")`
   - `record_difference()`: validate status==Approved, difference!=0, difference_account set → create draft JE (Step 1), link to `pending_je`. Use `_create_je()` pattern from treasury. Voucher_type="Cash Entry". When pending_je submitted → `db_set("status", "Pending Resolution")`
   - `resolve_difference()`: validate status=="Pending Resolution", resolution_type set, resolution_target_account set → create draft JE (Step 2) based on resolution_type, link to `resolution_je`. When resolution_je submitted → `db_set("status", "Resolved")`

4. **JE accounting entries** (Step 1):
   - Deficit: Nợ difference_account (1381) / Có cash_account (111x) for abs(difference)
   - Surplus: Nợ cash_account (111x) / Có difference_account (3381) for abs(difference)

5. **JE accounting entries** (Step 2 — resolution):
   - Employee Compensation (deficit): Nợ 1388 / Có 1381
   - Management Expense (deficit): Nợ 6425 / Có 1381
   - Return to Owner (surplus): Nợ 3381 / Có cash_account
   - Other Income (surplus): Nợ 3381 / Có 711

### Phase 4: Client Script (cash_count.js)

**JS at `vn_accounting/vn_accounting/doctype/cash_count/cash_count.js`**:

1. **`refresh()`**: Show/hide buttons based on status:
   - Draft → "Mark as Counted" button
   - Counted → "Approve" button
   - Approved + difference!=0 → "Record Difference" button
   - Pending Resolution → "Resolve Difference" button (with prompt for resolution_type)

2. **`cash_account` / `count_date` change**: `frappe.call` to `get_book_balance`, update field

3. **`show_denomination` change**: toggle denominations table visibility. When turned on, pre-populate 9 rows (500k, 200k, 100k, 50k, 20k, 10k, 5k, 2k, 1k) if table empty

4. **denomination `quantity` change**: recalc row `amount`, recalc `actual_amount` total

5. **`resolution_type` change**: auto-fill `resolution_target_account` from Settings

6. **`difference_type` change**: auto-fill `difference_account` from Settings, filter `resolution_type` options (only show deficit options if deficit, surplus options if surplus)

### Phase 5: Print Format (Mẫu 08a)

**Jinja HTML Print Format** at `vn_accounting/vn_accounting/print_format/cash_count_report/`:
- `cash_count_report.json` — Print Format definition (print_format_type="Jinja", doc_type="Cash Count")
- `cash_count_report.html` — Jinja template per spec §4:
  - Header: company name + address (from Company doc) + "Mẫu số 08a"
  - Title: "BIÊN BẢN KIỂM KÊ QUỸ TIỀN MẶT"
  - Conditional denomination table (only if show_denomination)
  - Chênh lệch section (Thừa/Thiếu)
  - 3-column signature block (Giám đốc / Kế toán trưởng / Thủ quỹ)
  - Font: Times New Roman, A4 portrait, VND format with dot separator

### Phase 6: Sidebar + Translations + Wiring

1. **Sidebar**: Add item to `workspace_sidebar/vn_accounting.json` in Quỹ tiền mặt section, before "Tạo bút toán tiền mặt":
   ```json
   {"child":1,"label":"Kiểm kê quỹ","link_to":"Cash Count","link_type":"DocType","type":"Link"}
   ```
   Bump sidebar `modified` timestamp.

2. **Translations**: Add ~32 entries to `vn_accounting/translations/vi.csv` per spec §7 + resolution entries.

3. **hooks.py**: No doc_events needed (status managed via controller methods, not on_submit). No changes unless JE submit/cancel needs to update Cash Count status — in that case, extend `je_hooks.py` to check if JE is linked from a Cash Count's `pending_je` or `resolution_je` field.

4. **`bench --site dcnet.localhost clear-cache`** after sidebar/translation changes.
5. **`bench build --app vn_accounting`** after JS changes.

### Phase 7: QA + Bug Fixes

QA on `http://dcnet.localhost:8001` with Playwright MCP tools:
1. Create a Cash Count → verify book_balance auto-fetches
2. Toggle denomination detail → verify rows pre-populate
3. Enter quantities → verify actual_amount sums correctly
4. Mark as Counted → Approve → verify status transitions
5. Record Difference → verify draft JE created with correct accounts
6. Print → verify Mẫu 08a renders correctly
7. Check sidebar → "Kiểm kê quỹ" visible in Quỹ tiền mặt section
8. Check Vietnamese translations render (user language = vi)
9. Fix any bugs found, commit each fix atomically

## Acceptance Criteria

- [ ] `bench --site dcnet.localhost migrate` succeeds (DocTypes created)
- [ ] `bench build --app vn_accounting` succeeds (JS bundled)
- [ ] Cash Count form loads at `/desk/cash-count/new-cash-count-1`
- [ ] `book_balance` auto-fetches from GL when cash_account + count_date set
- [ ] Denomination toggle works: pre-populates 9 VND rows, sums to actual_amount
- [ ] Status transitions: Draft → Counted → Approved → Closed (when balanced)
- [ ] Status transitions: Approved → [Record Difference] → Pending Resolution → [Resolve Difference] → Resolved
- [ ] "Record Difference" creates correct draft JE (deficit: Nợ 1381/Có 111, surplus: Nợ 111/Có 3381)
- [ ] "Resolve Difference" creates correct draft JE based on resolution_type
- [ ] VN Accounting Settings has 5 new fields in Cash Count section
- [ ] `save_as_default` writes back to Settings
- [ ] Print Format "Mẫu 08a" renders with conditional denomination table and 3-column signatures
- [ ] Sidebar shows "Kiểm kê quỹ" in Quỹ tiền mặt section
- [ ] Vietnamese translations render when user language = vi (check form labels)
- [ ] All changes committed with descriptive messages on `feature/cash-count` branch

## Constraints

- Do NOT modify existing DocTypes (Term Deposit, Bank Loan) or their controllers
- Do NOT modify `report_utils.py` — reuse `get_opening_balance()` as-is
- Do NOT modify `journal_entry_builder.py` — create a separate `cash_count_je_builder.py` if needed, or call `_create_je()` directly
- Do NOT modify Frappe core or ERPNext
- All field labels in English (Vietnamese via translations/vi.csv only)
- No file >500 lines
- Cash Count is NOT submittable — do not set `is_submittable=1`

## Verification Commands
bench --site dcnet.localhost migrate 2>&1 | tail -5
bench build --app vn_accounting 2>&1 | tail -5
bench --site dcnet.localhost execute "frappe.get_meta('Cash Count').fields" 2>&1 | head -5
bench --site dcnet.localhost execute "frappe.get_meta('Cash Count Denomination').fields" 2>&1 | head -5
bench --site dcnet.localhost execute "frappe.get_doc('VN Accounting Settings').cash_surplus_account or 'field exists'" 2>&1
cd /home/long/long/frappe-bench-dcnet && env/bin/python -m pytest apps/vn_accounting/vn_accounting/cash_count/ -v --tb=short 2>&1 | tail -20

## Agent Persona

You are a senior Frappe v16 developer building a Vietnamese accounting feature. Key conventions:
- Read the design spec FIRST: `docs/superpowers/specs/2026-04-16-cash-count-design.md`
- Reuse `report_utils.get_opening_balance()` for GL balance queries — don't rewrite
- Follow the `term_deposit.py` pattern for status transitions (db_set + whitelisted methods)
- Follow the `term_deposit.js` pattern for buttons (frm.add_custom_button in refresh)
- Follow `_create_je()` in `journal_entry_builder.py` for JE creation
- All labels English, Vietnamese via `translations/vi.csv`
- After DocType JSON changes: `bench --site dcnet.localhost migrate`
- After JS changes: `bench build --app vn_accounting`
- After hooks/sidebar changes: `bench --site dcnet.localhost clear-cache`
- Commit early and often — don't batch all commits at the end
- The bench root is `/home/long/long/frappe-bench-dcnet` — run bench commands from there

## Model
auto

## Time Budget
- Max hours: 3
- Max sessions: 8
