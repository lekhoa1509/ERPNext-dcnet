# Task: Term Deposit & Bank Loan — vn_accounting Treasury Feature

## Context
DCNET needs to manage term deposits (tiền gửi có kỳ hạn) at multiple banks and bank loans (khoản vay ngân hàng) with automated interest/repayment journal entry generation. Currently vn_accounting only handles day-to-day banking (receipts, payments, transfers). This feature adds financial instrument tracking with 5 interest types for deposits and 2 repayment types for loans, automated draft JE creation via scheduled job, and maturity alerts.

Design spec: `docs/specs/2026-04-15-vn-treasury-term-deposit-loan-design.md` (in bench root, NOT in app dir)

## Scope
- Project: `/home/long/long/frappe-bench-dcnet/apps/vn_accounting`
- Bench root: `/home/long/long/frappe-bench-dcnet`
- Branch: create new `feature/treasury` from current `main`
- Site: `dcnet.localhost:8001`
- Module: `VN Accounting` (from `vn_accounting/modules.txt`)

### Related files (existing)
| Path | Purpose | Lines |
|------|---------|-------|
| `vn_accounting/hooks.py` | App hooks — need to add scheduler_events, fixtures | ~36 |
| `vn_accounting/__init__.py` | Version + monkey-patches | ~15 |
| `vn_accounting/vn_accounting/report_utils.py` | Account prefixes (BANK_PREFIX="112%", etc.) + GL helpers | ~133 |
| `vn_accounting/boot.py` | boot_session hook — workspace sidebar defaults | ~50 |
| `vn_accounting/install.py` | after_install/after_migrate hooks | ~40 |
| `vn_accounting/workspace_sidebar/vn_accounting.json` | Sidebar fixture — 14 sections | ~930 |
| `vn_accounting/translations/vi.csv` | Vietnamese translations | ~16 |
| `vn_accounting/setup/company_defaults.py` | Company on_update defaults | ~80 |

### Files to create (new)
| Path | Purpose |
|------|---------|
| `vn_accounting/vn_accounting/doctype/term_deposit/` | Term Deposit DocType (JSON + controller) |
| `vn_accounting/vn_accounting/doctype/term_deposit_interest/` | Child table: interest schedule rows |
| `vn_accounting/vn_accounting/doctype/bank_loan/` | Bank Loan DocType (JSON + controller) |
| `vn_accounting/vn_accounting/doctype/bank_loan_repayment/` | Child table: repayment schedule rows |
| `vn_accounting/vn_accounting/doctype/vn_accounting_settings/` | Settings Single DocType |
| `vn_accounting/treasury/` | Module: calculators, JE builder, scheduled job |
| `vn_accounting/treasury/__init__.py` | Package init |
| `vn_accounting/treasury/interest_calculator.py` | Pure functions: 5 interest schedule types |
| `vn_accounting/treasury/repayment_calculator.py` | Pure functions: 2 repayment schedule types |
| `vn_accounting/treasury/journal_entry_builder.py` | Build draft JE for deposit/loan events |
| `vn_accounting/treasury/scheduled.py` | Daily scheduled job: process_treasury_schedules |
| `vn_accounting/vn_accounting/page/vn_treasury_guide/` | Help page with user guide |

## Requirements

### Phase 1: Session 1 — Implementation Plan
Read the design spec at `docs/specs/2026-04-15-vn-treasury-term-deposit-loan-design.md` and write a detailed implementation plan using the `writing-plans` skill. The plan should cover all phases below with exact file paths, code structure, and task ordering. Save plan to `docs/plans/2026-04-15-vn-treasury-plan.md`.

### Phase 2: DocTypes & Settings
1. **VN Accounting Settings** — Single DocType with fields for default accounts (deposit_account → "1281%", interest_income_account → "515%", loan_account → "3411%", interest_expense_account → "635%") and alert days. Account fields use `Link → Account` with `get_query` filtering by company. Seed defaults in `after_install` by looking up accounts matching those prefixes.

2. **Term Deposit Interest** (child) — fields: `due_date` (Date), `interest_amount` (Currency), `principal_at_start` (Currency), `status` (Select: Pending/Draft Created/Booked), `journal_entry` (Link → Journal Entry). NOT submittable (child of Term Deposit).

3. **Term Deposit** — fields per spec §2.1. `interest_type` Select with options: `End of Term\nMonthly\nQuarterly\nPrepaid\nCompound`. Child table `interest_schedule` of type `Term Deposit Interest`. Controller: `validate()` computes maturity_date from start_date + term_months, calls `interest_calculator.build_interest_schedule()` to populate child table. `on_submit()` creates JE for deposit (Nợ deposit_account / Có bank_account via 112x). For Prepaid type: 3-leg JE (Nợ 1281 / Có 112x partial / Có 515 interest). Status workflow: Draft → Active → Matured → Settled.

4. **Bank Loan Repayment** (child) — fields: `due_date`, `principal_amount`, `interest_amount`, `total_amount`, `outstanding_after`, `status`, `journal_entry`. Same pattern as Term Deposit Interest.

5. **Bank Loan** — fields per spec §3.1. `repayment_type` Select: `Interest Only\nEMI`. `repayment_frequency` Select: `Monthly\nQuarterly`. Controller: `validate()` calls `repayment_calculator.build_repayment_schedule()`. `on_submit()` creates JE for disbursement (Nợ 112x / Có 3411).

### Phase 3: Calculator Pure Functions (TDD required)
1. **interest_calculator.py** — `build_interest_schedule(principal, rate, interest_type, start_date, maturity_date) → list[dict]`. Must handle all 5 types. Interest formula: `principal × (rate/100) × (days/365)` for simple; compound reinvests each period. Each dict: `{"due_date": date, "interest_amount": float, "principal_at_start": float}`.

2. **repayment_calculator.py** — `build_repayment_schedule(amount, rate, repayment_type, frequency, start_date, maturity_date) → list[dict]`. Interest Only: interest each period + full principal last period. EMI: `PMT = P × r / (1 - (1+r)^-n)` where r = rate/100/12 (monthly) or rate/100/4 (quarterly). Each dict: `{"due_date": date, "principal_amount": float, "interest_amount": float, "total_amount": float, "outstanding_after": float}`.

3. **calculate_early_settlement(doc, settlement_date) → dict** — Pro-rata interest to settlement_date using applicable rate (early_withdrawal_rate for deposits, loan rate for loans).

### Phase 4: Journal Entry Builder & Scheduled Job
1. **journal_entry_builder.py** — Functions: `create_deposit_je(term_deposit)`, `create_interest_je(term_deposit, schedule_row)`, `create_settlement_je(term_deposit, settlement_date=None)`, `create_disbursement_je(bank_loan)`, `create_repayment_je(bank_loan, schedule_row)`, `create_loan_settlement_je(bank_loan, settlement_date)`. All create Draft JE using `frappe.get_doc({"doctype": "Journal Entry", ...}).insert()`. Set `voucher_type = "Bank Entry"`.

2. **scheduled.py** — `process_treasury_schedules()`: query active Term Deposits + Bank Loans, find schedule rows with `due_date <= today` and `status = "Pending"`, create draft JE, update row status to "Draft Created". Also: check maturity dates → update status to "Matured" + create settlement draft. Check alert thresholds → create Notification Log.

3. **hooks.py** — Add `scheduler_events = {"daily": ["vn_accounting.treasury.scheduled.process_treasury_schedules"]}`.

### Phase 5: Sidebar, Translations, Guide Page
1. **workspace_sidebar/vn_accounting.json** — Add 2 items under "Ngân hàng" section: "Tiền gửi có kỳ hạn" (link_type: DocType, link_to: Term Deposit) and "Khoản vay ngân hàng" (link_type: DocType, link_to: Bank Loan). Add 1 item under "Thiết lập": "Cài đặt ngân hàng" (link_type: DocType, link_to: VN Accounting Settings). Bump `modified` timestamp.

2. **translations/vi.csv** — Add translations for ALL user-visible English strings. CRITICAL: every field label, Select option, description, introduction, status, button text, error message MUST have a vi.csv entry. This is enforced by project CLAUDE.md. Minimum required entries:

   **DocType names:** Term Deposit → Tiền Gửi Có Kỳ Hạn, Bank Loan → Khoản Vay Ngân Hàng, Term Deposit Interest → Lịch Trả Lãi Tiền Gửi, Bank Loan Repayment → Lịch Trả Nợ Vay, VN Accounting Settings → Cài Đặt Kế Toán VN

   **Term Deposit fields:** Principal Amount → Số tiền gốc, Interest Rate → Lãi suất (%/năm), Interest Type → Kiểu trả lãi, Start Date → Ngày gửi, Maturity Date → Ngày đáo hạn, Term (Months) → Kỳ hạn (tháng), Early Withdrawal Rate → Lãi suất tất toán trước hạn, Alert Days Before Maturity → Cảnh báo trước (ngày), Total Interest → Tổng lãi dự kiến, Deposit Number → Số sổ tiền gửi, Deposit Account → TK tiền gửi có kỳ hạn, Interest Income Account → TK doanh thu lãi

   **Term Deposit Select options:** End of Term → Lãi cuối kỳ, Monthly → Hàng tháng, Quarterly → Hàng quý, Prepaid → Lãi trả trước, Compound → Lãi nhập gốc

   **Term Deposit statuses:** Active → Đang hoạt động, Matured → Đã đáo hạn, Settled → Đã tất toán, Early Settled → Tất toán trước hạn

   **Bank Loan fields:** Loan Amount → Số tiền vay, Outstanding Amount → Dư nợ hiện tại, Rate Type → Loại lãi suất, Repayment Type → Kiểu trả nợ, Repayment Frequency → Tần suất trả, Loan Number → Số hợp đồng vay, Loan Account → TK nợ vay, Interest Expense Account → TK chi phí lãi vay, Total Repayment → Tổng trả (gốc+lãi)

   **Bank Loan Select options:** Interest Only → Trả lãi hàng kỳ + gốc cuối kỳ, EMI → Trả đều (gốc + lãi), Fixed → Cố định, Floating → Thả nổi

   **Shared fields/statuses:** Pending → Chờ xử lý, Draft Created → Đã tạo nháp, Booked → Đã hạch toán, Due Date → Ngày đến hạn, Interest Amount → Tiền lãi, Principal at Start → Gốc đầu kỳ, Outstanding After → Dư nợ sau trả

   **Form introductions + descriptions:** add entries for all `description` and `introduction` text on DocType forms.

   **Error messages:** add entries for all `frappe.throw(__("..."))` messages in controllers.

   Total: ~60-80 translation entries. Agent MUST enumerate every string added to source code and add corresponding vi.csv entry in the same commit.

3. **Form introductions** — Set `introduction` on Term Deposit and Bank Loan DocType JSONs with ENGLISH help text (Vietnamese via vi.csv translation).

4. **vn_treasury_guide Page** — Frappe Page with HTML guide content: 5 interest types explained with examples, 2 repayment types with examples, usage flow, edge cases (early settlement, renewal, rate change).

### Phase 6: QA & Bug Fixes
1. `bench build --app vn_accounting` succeeds
2. `bench --site dcnet.localhost migrate` succeeds — all DocTypes synced
3. Browser QA: create Term Deposit with each interest type → verify schedule generated correctly
4. Browser QA: create Bank Loan with each repayment type → verify schedule
5. Verify sidebar items visible after login
6. Fix any bugs found during QA

## Acceptance Criteria
- [ ] `bench build --app vn_accounting` succeeds with 0 errors
- [ ] `bench --site dcnet.localhost migrate` succeeds — Term Deposit, Bank Loan, VN Accounting Settings DocTypes created
- [ ] Term Deposit: create with interest_type="Monthly", 12-month term → 12 interest schedule rows generated with correct amounts
- [ ] Term Deposit: create with interest_type="Compound" → principal_at_start increases each period
- [ ] Term Deposit: submit → draft JE created (Nợ 1281 / Có 112x)
- [ ] Bank Loan: create with repayment_type="EMI", monthly → schedule rows sum to loan_amount (principal) + total interest
- [ ] Bank Loan: create with repayment_type="Interest Only" → last row principal = full loan amount
- [ ] Bank Loan: submit → draft JE created (Nợ 112x / Có 3411)
- [ ] VN Accounting Settings: default accounts populated from VN COA on install
- [ ] Scheduled job `process_treasury_schedules` runs without error (test via `bench execute`)
- [ ] Sidebar shows "Tiền gửi có kỳ hạn" and "Khoản vay ngân hàng" under Ngân hàng
- [ ] Sidebar shows "Cài đặt ngân hàng" under Thiết lập
- [ ] Pure function tests pass for all 5 interest types and 2 repayment types
- [ ] QA with headed browser: create Term Deposit + Bank Loan, verify schedules, check sidebar navigation
- [ ] English-first i18n: ALL DocType field labels, Select options, descriptions, introductions are English in JSON source
- [ ] translations/vi.csv contains entries for every user-visible string added (DocType names, field labels, Select options, statuses, error messages, form introductions) — minimum 60 entries
- [ ] With user language=vi, Term Deposit form shows all labels in Vietnamese (verify via browser)
- [ ] All changes committed with descriptive messages on `feature/treasury` branch

## Constraints
- Do NOT modify Frappe core or ERPNext code
- Do NOT hardcode account numbers — always read from VN Accounting Settings, with fallback to prefix match (e.g., "1281%")
- Do NOT write Vietnamese in DocType JSON field labels, Select options, or descriptions — English only, Vietnamese via vi.csv
- Do NOT auto-submit Journal Entries — always create as Draft
- Keep each Python file under 500 lines
- Follow existing vn_accounting patterns: use `report_utils.py` helpers where applicable
- Do NOT modify existing reports, dashboard, or sidebar items — only ADD new items
- Interest calculation: use actual/365 day-count convention (VN banking standard)

## Verification Commands
bench build --app vn_accounting
bench --site dcnet.localhost migrate
bench --site dcnet.localhost execute "frappe.get_doc('VN Accounting Settings').as_dict()"
bench --site dcnet.localhost execute "frappe.db.count('Term Deposit')"
bench --site dcnet.localhost execute "frappe.db.count('Bank Loan')"

## Agent Persona
You are a senior Frappe developer with expertise in Vietnamese corporate finance (TT99/2025 chart of accounts). Key rules:
- Read the design spec FIRST: `docs/specs/2026-04-15-vn-treasury-term-deposit-loan-design.md` (relative to bench root `/home/long/long/frappe-bench-dcnet`)
- Session 1: write implementation plan using `writing-plans` skill, save to `docs/plans/`
- Sessions 2+: execute the plan phase by phase
- Use `frappe.get_doc()` not raw SQL for document operations
- `bench --site dcnet.localhost migrate` after creating/modifying DocType JSONs
- `bench build --app vn_accounting` after JS/CSS changes
- Commit after each logical unit of work (not at end of session)
- For calculator pure functions: write tests first (TDD), then implement
- For DocType controllers: the server is the ONLY source of truth for interest/repayment calculations — no client-side formula engine

## Model
auto

## Time Budget
- Max hours: 4
- Max sessions: 10
