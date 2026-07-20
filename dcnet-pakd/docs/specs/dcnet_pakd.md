# dcnet_pakd — Custom Frappe App Specification

> **Status:** Draft spec (pre-implementation)
> **Target bench:** `frappe-bench-dcnet` (Frappe v16.12.2 + ERPNext v16.12.0)
> **Created:** 2026-04-08
> **Owner:** DCNET ERP migration team
> **Source of truth:** `docs/accounting-requirements/converted/` (biên bản họp 08/04/2026 + 3 mẫu PAKD)

---

## 1. Why this app exists

DCNET is migrating from **Misa** to **ERPNext**. Every other requirement from the 08/04/2026 accounting meeting can be satisfied by ERPNext core + the existing `vn_accounting` app with configuration. **One requirement cannot:** the **Phương Án Kinh Doanh (PAKD)** — DCNET's contract-level profitability + sales commission worksheet, currently maintained as Excel templates (Mẫu số 01/02/03).

PAKD is the bridge between three systems:

```
Sales (Contract/SO) ──► PAKD ──► Accounting (JE on taxless expense accounts)
                            └──► HRMS Payroll (Additional Salary — Lương KD)
```

Without it, the migration blocks on the commission payroll cycle — which happens **every month before the 5th**. This app must ship before DCNET can cut over from Misa.

**Non-goal:** This app is NOT a general sales quoting tool and does NOT replace ERPNext Quotation/Sales Order. PAKD is approved *after* a contract exists; it ratifies the deal's commission economics and posts the payout.

---

## 2. Business domain — what a PAKD is

A PAKD is a signed internal document that answers, for a single sales deal:

1. What is the customer paying? (**Doanh thu hợp đồng**)
2. What concessions were negotiated? (**Chi phí Add Costs** = customer markup kept off-book; **Chi phí Manager Services** = commission paid to the customer side)
3. What regulatory fees apply? (**Phí quyền GPVT + quỹ CIVT** — 2.2% for telecom services only)
4. What commission does the sales rep earn? (**Lương kinh doanh**)
5. What profit is left? (**Doanh thu dịch vụ** = net contribution after all of the above)

It must be approved by a 3–4 level chain (routed per branch and per sales channel) before accounting can:
- Pay out the customer-side commission
- Post the sales rep's commission into the next payroll run
- Record the concessions into **taxless expense accounts** (regulatory: these aren't VAT-deductible)

### Three flavours (→ one DocType, three presets)

| Preset | Business line | Time structure | Source template |
|---|---|---|---|
| `Recurring Telecom` | P2P / MPLS / ILL / FTTH DN / IT managed services — monthly billing | 1 contract × up to 12 months, with pro-rating for partial first/last month | Mẫu số 01 |
| `Monthly FTTH Rollup` | Multiple small FTTH DN contracts consolidated into one monthly PAKD | N contracts × 1 month | Mẫu số 02 |
| `One-off Sale/Project` | Equipment sales, construction projects — paid once at handover | N line items × 1 total | Mẫu số 03 |

The field `pakd_type` selects the preset and drives (a) which child tables are visible, (b) which commission rules apply, (c) which print format prints.

---

## 3. Scope

### In scope
- DocType `Phương Án Kinh Doanh` with its child tables and rule-driven calculations
- Commission rule engine (configurable rates per service type + branch)
- Approval workflow (4 routes: HCM-NV / HCM-BGĐ / HN-NV / HN-BGĐ)
- Cut-off logic (PAKD submitted after the 5th → commission shifts to the next payroll month)
- Integration with ERPNext Sales Order / Contract (link back) and HRMS Additional Salary (forward)
- Vietnamese print formats, one per preset, matching the original Excel signature blocks
- Workspace "Phương án Kinh doanh" with list view, dashboard, reports
- Permissions per role (NVKD, GĐ TT KD, P. Tổng hợp, GĐ CN, BGĐ, Kế toán)
- Fixtures: workflow, commission rule templates, default roles, print formats

### Out of scope
- Replacing Sales Order / Contract / Quotation
- Customer-side commission payment automation (Payment Entry generation — handled by accounting manually)
- Mobile app UI (web only for now)
- Historical Excel PAKD import (kế toán will re-enter or spot-check)
- Multi-currency (DCNET operates in VNĐ only based on templates)

---

## 4. Data model

### 4.1 `Phuong An Kinh Doanh` (main DocType)

Naming series: `PAKD-.YYYY.-.####.` with a user-visible display format `PAKD.PL{annex}/HĐ{contract}` rendered in print.

**Header section — identification**
| Field | Type | Notes |
|---|---|---|
| `pakd_type` | Select | `Recurring Telecom` / `Monthly FTTH Rollup` / `One-off Sale/Project` — drives layout via Client Script `depends_on` |
| `branch` | Link → Branch | HCM / HN — drives approval route |
| `channel` | Select | `Nhân viên` / `BGĐ` — drives approval route |
| `sales_employee` | Link → Employee | "Nhân viên kinh doanh" |
| `department` | Link → Department | Auto-fetch from employee |
| `customer` | Link → Customer | |
| `contract_ref` | Link → Sales Order *or* free-text contract number | PAKD must reference a real contract |
| `contract_date` | Date | |
| `annex_no` | Data | "Phụ lục số" |
| `annex_date` | Date | |
| `acceptance_date` | Date | "Ngày nghiệm thu" |
| `payment_cycle` | Select | `Monthly` / `Quarterly` / `Semiannual` / `Annual` / `One-off` |
| `project_type` | Select | `Viễn thông` / `CNTT` / `VTTB` / `Thi công` |
| `service_type` | Select | `P2P` / `MPLS` / `ILL` / `FTTH` / `IT Managed` / `Equipment` / `Construction` |
| `install_location` | Small Text | "Điểm đầu — Điểm cuối" for telecom, địa chỉ cho thi công |
| `revision_no` | Int | Bản thay đổi lần thứ |
| `change_reason` | Small Text | |
| `currency_unit_display` | Select | `VNĐ` / `1000 VNĐ` — display only; DB stores VNĐ |

**Calculation section — totals (read-only, server-computed in `validate`)**
| Field | Type | Formula |
|---|---|---|
| `total_revenue_contract` | Currency | Σ line revenue |
| `total_add_costs` | Currency | Σ line add_costs |
| `total_manager_services` | Currency | Σ line manager_services |
| `total_license_fee` | Currency | Σ line license_fee (only Recurring Telecom) |
| `total_sales_commission` | Currency | Σ line sales_commission |
| `total_cost` | Currency | sum of all cost components above |
| `total_revenue_service` | Currency | `total_revenue_contract - total_cost` |

**Payroll linkage**
| Field | Type | Notes |
|---|---|---|
| `submission_date` | Date | Auto on first submit |
| `effective_payroll_month` | Data (YYYY-MM) | Computed: if `submission_date.day <= 5` → previous month, else current month |
| `is_late_submission` | Check | True if shifted forward |
| `additional_salary` | Link → Additional Salary | Back-reference after commission is pushed to HRMS |

**Child tables**
| Field | Child DocType | Used when |
|---|---|---|
| `items` | `PAKD Item` | Always (one row = one hạng mục / one contract / one line item) |
| `monthly_projection` | `PAKD Monthly Projection` | Only `pakd_type = Recurring Telecom` (12-month breakdown with pro-rating) |

**Workflow fields** — managed by Frappe Workflow, not added manually:
- `workflow_state` (Link → Workflow State)

### 4.2 `PAKD Item` (child table)

Represents one line of the worksheet. Shape changes slightly per `pakd_type` but we keep one child DocType with conditional fields (hide via client script):

| Field | Type | Recurring Telecom | Monthly Rollup | One-off |
|---|---|---|---|---|
| `item_code` | Link → Item (optional) | | ✓ | ✓ |
| `description` | Small Text | ✓ | ✓ | ✓ |
| `uom` | Link → UOM | `HĐ` | `HĐ` | `Cái`/`Gói` |
| `qty` | Float | 1 (usually) | 1 | N |
| `unit_price` | Currency (chưa VAT) | ✓ | ✓ | ✓ |
| `setup_fee` | Currency | ✓ (Phí lắp đặt, col F) | — | — |
| `add_costs_unit_price` | Currency | ✓ (E20 in Mẫu 01) | — | ✓ (E20 in Mẫu 03) |
| `months_billed` | Int | — | ✓ ("Số tháng TT") | — |
| `months_promo` | Int | — | ✓ ("Số tháng KM") | — |
| `contract_line_ref` | Data | — | ✓ (Số HĐ/HĐ của KH) | — |
| `revenue_actual` | Currency | — | ✓ **USER-ENTERED** ("Doanh thu thực", col I) | — |
| `salary_coefficient` | Float | — | ✓ ("Hệ số lương KD", col J) | — |
| **Computed** |
| `revenue_contract` | Currency | `qty * unit_price` | = `revenue_actual` (user-entered) | `qty * unit_price` |
| `add_costs` | Currency | rule-based (see §5) | — | rule-based |
| `manager_services` | Currency | rule-based | — | rule-based |
| `license_fee` | Currency | rule-based (2.2%) | — | — |
| `sales_commission` | Currency | rule-based (6%) | `salary_coefficient * revenue_actual` | rule-based |
| `total_cost` | Currency | Σ of cost fields | — (see Optional Cost below) | Σ of cost fields |
| `revenue_service` | Currency | `revenue_contract - total_cost` | — | `revenue_contract - total_cost` |
| `note` | Small Text | — | ✓ ("Ghi chú") | — |

### 4.2.b `PAKD Optional Cost` (child table, Monthly Rollup only)

Replicates the **IV. Chi phí** section at the bottom of Mẫu số 02 (rows 17–19). This is **optional** — it exists only when DCNET has to pay Manager Services or Add Costs commission for IT partners at the batch level, not per-contract:

| Field | Type | Notes |
|---|---|---|
| `cost_kind` | Select | `Add Costs (IT/Đối tác)` / `Manager Services (IT/Đối tác)` |
| `contract_count` | Int | "Số hợp đồng" (col D in cost section) |
| `revenue_base` | Currency | "Doanh thu" (col G in cost section) — user-entered |
| `cost_coefficient` | Float | "Hệ số CP" (col J) |
| `total_cost` | Currency | computed: `cost_coefficient * revenue_base` — matches `K18 = J18*G18` |

Ghi chú Mẫu 02 quy định: *"Mục IV: Nếu có phát sinh chi HH cho IT/ Đối tác thì điền mục này, không thì có thể delete"* → field `optional_costs` trên PAKD có thể rỗng.

### 4.3 `PAKD Monthly Projection` (child, Recurring only)

Replicates columns F–R of Mẫu số 01 (Phí lắp đặt + 12 months). **Setup fee is modeled as `month_index = 0`** so the same rule engine applies to the setup column — no special case in code.

| Field | Type | Notes |
|---|---|---|
| `month_index` | Int | **0 = Phí lắp đặt (col F)**; 1–12 = tháng 1–12 (col G–R) |
| `year` | Int | For month 1–12; ignored for month 0 |
| `revenue` | Currency | Month 0: `item.setup_fee`; month N: `item.unit_price` (or pro-rated for partial first/last month) |
| `manager_services` | Currency | rule-engine applied per month |
| `add_costs` | Currency | rule-engine applied per month |
| `license_fee` | Currency | rule-engine applied per month |
| `sales_commission` | Currency | rule-engine applied per month |
| `total_cost` | Currency | Σ cost fields |
| `revenue_service` | Currency | `revenue - total_cost` |
| `is_prorated` | Check | True if month has partial billing (first or last month of contract) |
| `actual_days` | Int | For pro-rating first/last month |
| `days_in_month` | Int | |

**Pro-ration formula** (from Mẫu 01 Ghi chú mục I):
```
Tổng cước tháng = round(Cước hàng tháng / số ngày trong tháng, 0) * số ngày thực tế sử dụng trong tháng
```

**Why month 0 for setup fee:** the Excel formula for col F is `F17 = F16 - (F19 + F21 + F20 + F22)` — structurally identical to any other month column (`G17 = G16 - G18` where `G18 = SUM(G19:G22)`). Treating setup as "month 0" lets the rule engine loop over `month_index in [0..12]` uniformly instead of hardcoding a setup-fee branch. Golden test asserts `F17` value directly.

### 4.4 `PAKD Commission Rule Template` (standalone)

Central config — no hardcoded rates. One row per `(service_type, branch)` combination with effective dates:

| Field | Type | Default (from Mẫu 01) |
|---|---|---|
| `rule_name` | Data | e.g. "Recurring Telecom — Default" |
| `pakd_type` | Select | — |
| `service_type` | Select (or "All") | — |
| `branch` | Link → Branch (or "All") | — |
| `effective_from` | Date | |
| `effective_to` | Date (nullable) | |
| `manager_services_rate` | Percent | 10.00 |
| `manager_services_base` | Select | `Revenue` / `Revenue-AddCosts` |
| `add_costs_rate` | Percent | 75.00 |
| `add_costs_base_field` | Select | `custom_unit_price` (from add_costs unit price column) |
| `license_fee_rate` | Percent | 2.20 (only Recurring Telecom) |
| `license_fee_base` | Select | `Revenue` |
| `sales_commission_rate` | Percent | 6.00 |
| `sales_commission_base` | Select (see enum below) | `Revenue - AddCostsUnitPrice` |
| `taxless_expense_account` | Link → Account | The account to hit for Manager Services + Add Costs JE |
| `is_active` | Check | |

**`base` enum** — applies to `manager_services_base`, `license_fee_base`, `sales_commission_base`:

| Value | Formula | Used by |
|---|---|---|
| `Revenue` | `revenue_contract` (gross) | License fee (Mẫu 01: E21 = E16) |
| `Revenue - AddCostsUnitPrice` | `revenue_contract - item.add_costs_unit_price` | Mẫu 01 Manager Services (E19 = E16-E20) and Sales Commission (E22 = E16-E20) |
| `Revenue - AddCostsLineTotal` | `revenue_contract - line.add_costs` | Mẫu 03 Manager Services (F19 = D19*(F16-F20)) |
| `ActualRevenue` | `item.revenue_actual` (user-entered) | Mẫu 02 Sales Commission (K13 = J13*I13) |

**Critical distinction between Mẫu 01 and Mẫu 03:**
- Mẫu 01 subtracts the *unit price* of add costs (E20 = 3000) → base = 10500
- Mẫu 03 subtracts the *line total* of add costs (F20 = 2250) → base = 11250

The two templates look visually similar but use different base formulas for Manager Services. Rule templates seeded for Recurring Telecom use `Revenue - AddCostsUnitPrice`, while One-off use `Revenue - AddCostsLineTotal`. This is a tested invariant in the golden tests.

The rule engine resolves the most specific active rule: `(type + service + branch)` → `(type + service)` → `(type)` → fallback default.

### 4.5 Why not three separate DocTypes?

Considered but rejected. Pros of separate: cleaner field lists, simpler client scripts. Cons (decisive):
- Three print formats anyway — no gain
- Three workflows would need to be kept in sync
- Reports across all PAKD (total commission per sales rep) require UNION queries
- Users think of it as "a PAKD" — one form, three modes matches their mental model

One DocType + `pakd_type` field + `depends_on` client script to hide irrelevant fields wins.

---

## 5. Commission rule engine

A single Python module `dcnet_pakd/rules/engine.py` with a pure function:

```python
def compute_pakd_line(line: dict, header: dict, rule: PAKDCommissionRuleTemplate) -> dict:
    """Given a raw line + header + applicable rule, return the line with all computed cost fields."""
```

Called from:
- `PhuongAnKinhDoanh.validate()` — server-side recompute on every save (source of truth)
- `pakd.js` client script — optimistic preview as user types (UX), overwritten by server on save

**Why centralize:** the Excel formulas (`=$D$22*$E$22`, `=E16-E20`, etc.) are business logic, not display. They must live in one place that's tested and versioned. A mismatch between client JS and server Python would produce "my PAKD saved with different numbers than I saw" bugs — unacceptable for a commission calculator.

### Resolved rule example — Recurring Telecom, FTTH, HCM

For a contract with `unit_price = 13,500` (nghìn đồng), `qty = 1`:

```
add_costs_unit_price = 3,000  (user enters this separately)
add_costs            = 0.75 * 3,000                           = 2,250
manager_services     = 0.10 * (13,500 - 2,250)                = 1,050  ≠ 0.10 * 13,500
license_fee          = 0.022 * 13,500                         =   297   (on gross)
sales_commission     = 0.06 * (13,500 - 2,250)                =   630
total_cost           = 2,250 + 1,050 + 297 + 630              = 4,227
revenue_service      = 13,500 - 4,227                         = 9,273
```

These exactly match the values in `mau-01-PAKD.md` row 16–22, column F. **The test harness replays these rows as golden tests.**

---

## 6. Approval workflow

One Frappe Workflow named `PAKD Approval`. Conditional transitions route by `branch` + `channel`:

### States
1. `Draft` — editable by NVKD
2. `Pending GĐ TT KD` — editable by sales center manager (HCM or HN)
3. `Pending P. Tổng hợp` — editable by general department
4. `Pending GĐ CN` — editable by branch director (HN only)
5. `Pending BGĐ` — editable by board of directors
6. `Approved` — locked, commission posted
7. `Rejected` — locked, editable only after reopen

### Route matrix

| From → To | Condition |
|---|---|
| `Draft → Pending GĐ TT KD` | `channel == 'Nhân viên'` |
| `Draft → Pending P. Tổng hợp` | `channel == 'BGĐ'` |
| `Pending GĐ TT KD → Pending P. Tổng hợp` | always |
| `Pending P. Tổng hợp → Pending GĐ CN` | `branch == 'HN' AND channel == 'Nhân viên'` |
| `Pending P. Tổng hợp → Pending BGĐ` | everything else |
| `Pending GĐ CN → Pending BGĐ` | always (HN NV only) |
| `Pending BGĐ → Approved` | always |
| `any → Rejected` | any approver |

### Roles
- `PAKD Sales Rep` — NVKD, can create + submit to next state
- `PAKD Sales Director HCM` / `PAKD Sales Director HN` — GĐ TT KD, approve first level
- `PAKD General Department` — P. Tổng hợp
- `PAKD Branch Director HN` — GĐ CN HN, only appears in HN-Nhân viên route
- `PAKD Board` — BGĐ, final approval
- `PAKD Accountant` — read-only + post payroll

Names hardcoded in Excel ("DƯƠNG ĐẠI SƠN", "NGUYỄN THỊ MỸ HIỀN"…) are **not** embedded — they're just current holders of the roles, rendered on print via User profile lookup.

---

## 7. Cut-off logic (payroll month assignment)

On the first `Approved` transition, server-side hook computes:

```python
submission_date = today()
if submission_date.day <= 5:
    effective_payroll_month = submission_date.replace(day=1) - relativedelta(months=1)
    is_late_submission = False
else:
    effective_payroll_month = submission_date.replace(day=1)
    is_late_submission = True
```

Then calls `dcnet_pakd.integrations.payroll.push_to_additional_salary(pakd)` which creates an HRMS `Additional Salary`:
- `employee = pakd.sales_employee`
- `salary_component = "Lương kinh doanh"`
- `amount = pakd.total_sales_commission`
- `payroll_date = last_day(effective_payroll_month)`
- `ref_doctype = "Phuong An Kinh Doanh"`, `ref_docname = pakd.name`

The Additional Salary name is stored back on `pakd.additional_salary` for audit traceability.

---

## 8. Accounting integration

On `Approved`, `dcnet_pakd.integrations.accounting.post_journal_entry(pakd)` creates a draft Journal Entry:

```
DR  Chi phí Manager Services (taxless expense account)   total_manager_services
DR  Chi phí Add Costs (taxless expense account)          total_add_costs
DR  Phí quyền GPVT & quỹ CIVT                            total_license_fee
    CR  Phải trả NCC / TK ngân hàng                      (accountant chooses credit side)
```

The JE is **draft** — accountant reviews and submits manually. This matches the biên bản rule: kế toán always has the last word on posting.

Taxless expense account is pulled from the matched `PAKD Commission Rule Template.taxless_expense_account`. Biên bản §5 says explicitly: *"hoạch toán chi phí ngoài vào tài khoản không tính thuế"*.

---

## 9. Print formats

Three print formats, one per `pakd_type`, matching the exact Excel layout of Mẫu 01/02/03 (header block, items table, signature blocks with 3–5 columns depending on route). Implemented as Jinja HTML so line breaks and merged cells render cleanly.

Signature block auto-selects based on `branch + channel`:
- HCM-NV: 4 columns (Người lập / GĐ TT KD HCM / P. Tổng hợp / BGĐ)
- HCM-BGĐ: 3 columns (Người lập / P. Tổng hợp / BGĐ)
- HN-NV: 5 columns (Người lập / GĐ TT KD HN / P. Tổng hợp / GĐ CN HN / BGĐ)
- HN-BGĐ: 3 columns

Name fields resolved at render time from `User.full_name` of users holding each role — not hardcoded.

---

## 10. Reports & workspace

### Workspace `Phương án Kinh doanh` (Vietnamese)
- Shortcut: New PAKD
- List: All PAKD, filterable by state/branch/sales_employee
- Charts:
  - "Lương KD theo tháng × NVKD" (bar, source: PAKD Commission Report)
  - "PAKD pending approval" (heatmap by state)
  - "Doanh thu dịch vụ theo Branch × Service Type" (grouped bar)
- Number cards:
  - Total commission pending approval (VNĐ)
  - PAKD late this month (count)
  - PAKD approved this month (count)

### Reports (Script Reports, not Report Builder)
1. `PAKD Commission Register` — NVKD × month, total commission, late flag
2. `PAKD Profitability by Service` — group by service_type, sum revenue_contract + revenue_service
3. `PAKD Pending Approval` — aging in each state, who's blocking

---

## 11. Permissions

| Role | DocType | Read | Write | Create | Submit | Cancel |
|---|---|---|---|---|---|---|
| PAKD Sales Rep | PAKD | own only | own draft | ✓ | ✓ to next | — |
| PAKD Sales Director HCM | PAKD | branch=HCM | branch=HCM & state=Pending GĐ TT KD | — | ✓ | — |
| PAKD Sales Director HN | PAKD | branch=HN | branch=HN & state=Pending GĐ TT KD | — | ✓ | — |
| PAKD General Department | PAKD | all | state=Pending P. Tổng hợp | — | ✓ | — |
| PAKD Branch Director HN | PAKD | branch=HN | state=Pending GĐ CN | — | ✓ | — |
| PAKD Board | PAKD | all | state=Pending BGĐ | — | ✓ | — |
| PAKD Accountant | PAKD | all | — | — | — | — |
| PAKD Accountant | PAKD Commission Rule Template | ✓ | ✓ | ✓ | — | — |
| System Manager | all | ✓ | ✓ | ✓ | ✓ | ✓ |

User Permission on Branch enforces HCM/HN segregation for Sales Reps and Directors.

---

## 12. Folder structure

```
apps/dcnet_pakd/
├── pyproject.toml
├── README.md
├── license.txt
├── dcnet_pakd/
│   ├── __init__.py            # __version__ = "0.0.1"
│   ├── hooks.py
│   ├── modules.txt            # "DCNET PAKD"
│   ├── patches.txt            # empty (required by Frappe — see rules/frappe.md)
│   ├── boot.py                # optional: workspace defaults for sidebar persistence
│   ├── dcnet_pakd/            # module folder
│   │   ├── __init__.py
│   │   ├── doctype/
│   │   │   ├── phuong_an_kinh_doanh/
│   │   │   │   ├── phuong_an_kinh_doanh.json
│   │   │   │   ├── phuong_an_kinh_doanh.py
│   │   │   │   ├── phuong_an_kinh_doanh.js
│   │   │   │   └── test_phuong_an_kinh_doanh.py
│   │   │   ├── pakd_item/
│   │   │   ├── pakd_monthly_projection/
│   │   │   └── pakd_commission_rule_template/
│   │   ├── workspace/
│   │   │   └── phuong_an_kinh_doanh/phuong_an_kinh_doanh.json
│   │   ├── workflow/
│   │   │   └── pakd_approval/pakd_approval.json
│   │   ├── print_format/
│   │   │   ├── pakd_recurring_telecom/
│   │   │   ├── pakd_monthly_rollup/
│   │   │   └── pakd_one_off/
│   │   └── report/
│   │       ├── pakd_commission_register/
│   │       ├── pakd_profitability_by_service/
│   │       └── pakd_pending_approval/
│   ├── rules/
│   │   ├── __init__.py
│   │   └── engine.py          # compute_pakd_line()
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── payroll.py         # push_to_additional_salary()
│   │   └── accounting.py      # post_journal_entry()
│   ├── install.py             # after_install: seed default commission rules + roles
│   ├── public/
│   │   ├── js/
│   │   │   └── pakd_form.bundle.js
│   │   └── css/
│   │       └── pakd.bundle.css
│   └── fixtures/
│       ├── role.json
│       ├── custom_field.json
│       ├── workflow.json
│       └── pakd_commission_rule_template.json
└── tests/
    ├── golden/
    │   ├── mau_01_fixture.json   # replays Mẫu 01 row 16–22 values
    │   ├── mau_02_fixture.json
    │   └── mau_03_fixture.json
    └── test_rules_engine.py
```

---

## 13. Dependencies

- Frappe v16.12.2
- ERPNext v16.12.0 — uses `Employee`, `Department`, `Branch`, `Sales Order`, `Customer`, `Journal Entry`, `Account`
- HRMS v16.4.5 — uses `Additional Salary`, `Salary Component`
- `vn_accounting` (sibling app) — COA TT99/2025 provides the taxless expense accounts referenced in rule templates

No external Python packages beyond what Frappe already bundles.

---

## 14. Fixtures shipped with the app

- **Roles** (7): as in §11
- **Salary Component**: `Lương kinh doanh` — type `Earning`, `amount_based_on_formula = 0` (we push via Additional Salary, not formula)
- **Workflow**: `PAKD Approval` with all 7 states and conditional transitions
- **Commission Rule Templates** (default set — editable in production):
  - `Recurring Telecom - FTTH DN - Default`: 10% / 75% / 2.2% / 6%
  - `Recurring Telecom - P2P - Default`
  - `Recurring Telecom - MPLS - Default`
  - `Recurring Telecom - ILL - Default`
  - `Monthly FTTH Rollup - Default`
  - `One-off Sale/Project - Equipment - Default`
  - `One-off Sale/Project - Construction - Default`
- **Custom Fields**: none on core DocTypes (everything lives on PAKD DocTypes)

---

## 15. Testing strategy

### Unit tests (golden tests)
`tests/test_rules_engine.py` replays every formula-bearing cell from the three Excel templates and asserts exact match:
- Mẫu 01: 95 formulas (see `mau-01-PAKD.md` lines 88–182) → 12 computed lines × 7 fields per month
- Mẫu 02: 6 formulas → 4 assertions
- Mẫu 03: 8 formulas → 6 assertions

Run: `bench --site dcnet.localhost run-tests --app dcnet_pakd`

### Integration tests
- Create a PAKD → advance through workflow → assert Additional Salary created with correct amount
- Create a PAKD → approve after cut-off → assert `is_late_submission=True` and payroll month is current
- Create a PAKD → reject mid-flow → assert no JE, no Additional Salary

### Manual QA checklist
- Print each format, verify signature block matches Excel layout pixel-close
- Submit a rejected PAKD, edit, resubmit — ensure audit trail intact
- Try to edit a Commission Rule Template mid-flow — ensure existing PAKDs don't recompute retroactively

---

## 16. Deployment notes

- Register app in `sites/apps.txt` **and** run `bench install-app dcnet_pakd --site dcnet.localhost` — otherwise `patches.txt` guard check will not run and DocTypes may be treated as orphaned during migrate (see `rules/frappe.md` → "sites/apps.txt").
- `version` field in `hooks.py`: bump on every material change, use in `app_include_js` cache-bust query string.
- Dual remote push (DCNET cloud + personal goldrag1) per project convention in `CLAUDE.md`.
- First install on production: seed commission rule templates via `install.py`, then kế toán reviews/edits rates before opening to sales reps.

---

## 17. Open questions (BLOCKING before implementation)

Directed at DCNET accounting/BGĐ — must answer before Sprint starts:

1. **Commission rates** — are 10% / 75% / 2.2% / 6% fixed, or do they vary per service type or customer tier? If variable, what drives the variation?
2. **Manager Services payout** — does accounting issue a Payment Entry to the customer for this amount, or is it netted off the invoice? (Affects whether we generate PE or just JE.)
3. **Add Costs VAT treatment** — confirm these hit a **genuinely tax-exempt** account, not a deductible one flagged as "no VAT" (has compliance implications).
4. **Role holders** — who currently holds `PAKD Sales Director HCM`, `PAKD Sales Director HN`, `PAKD General Department`, `PAKD Branch Director HN`, `PAKD Board`? (For seeding Users + User Permissions in production, not hardcoded in print.)
5. **Rollup PAKD (Mẫu 02)** — when a new FTTH contract is signed mid-month after the monthly PAKD has been submitted, does NVKD insert into the existing PAKD (requires reopen) or create a new one?
6. **Pro-ration for first/last month** — formula from Mẫu 01 is `round(monthly/days, 0) * actual_days`. Confirm rounding mode (banker's / half-up / truncate)?
7. **Revision history** — when a PAKD is revised (`revision_no` > 1), does the new version supersede the old in payroll, or are they additive?
8. **Contract link** — PAKD links to `Sales Order` or to a free-text contract number? Does DCNET use ERPNext Sales Order at all, or will they keep contracts in a separate system?
9. **Currency unit display** — some templates use "1000 VNĐ" as display unit. Store raw VNĐ and multiply at display time, or store as entered?
10. **Attachments** — do PAKDs need to carry the scanned signed PDF as an attachment once the physical signature is collected?

---

## 18. Non-goals / explicit deferrals

- **Mobile form** — web only. Defer until v2.
- **Bulk approval** — approvers act on one PAKD at a time. Defer.
- **PAKD amendment workflow** — use the `revision_no` field + create-new pattern; no in-place amendment. Defer proper amendment flow to v2.
- **Auto-generate Sales Invoice from Recurring Telecom PAKD** — the biên bản suggests this is desirable but it crosses into `vn_accounting` territory; handle in a later sprint.
- **Integration with e-sign** — physical signature for now, scanned and attached.

---

## 19. Success criteria

This app is done when:

1. A sales rep can create a Recurring Telecom PAKD for a real FTTH DN contract and the numbers match the Excel template exactly
2. The PAKD flows through the 4-state HCM-Nhân viên approval route with correct role gating at each step
3. On final approval, an HRMS Additional Salary is automatically created with the correct amount and payroll month (respecting the 5th-of-month cut-off)
4. A draft Journal Entry is created hitting the taxless expense account, waiting for accountant review
5. The Vietnamese print format renders with the correct signature block for the route
6. All three presets (Recurring Telecom, Monthly Rollup, One-off) work end-to-end
7. Golden tests pass — every formula from all 3 Excel templates is replicated exactly
8. A kế toán user can run `PAKD Commission Register` report and see exactly what went into last month's payroll, with drill-down to the source PAKD

When items 1–8 pass manual QA and golden tests, the app is ready for DCNET production cutover.

---

## 20. UI technology — how we reproduce the Excel worksheet

### Decision

**Three-layer architecture, no embedded spreadsheet library.**

```
┌──────────────────────────────────────────────────────────────┐
│  LAYER 1 — DATA ENTRY                                        │
│  Frappe standard DocType form + child tables                 │
│  • Header fields in a normal Frappe form                     │
│  • PAKD Item / Optional Cost: Frappe child table grid        │
│  • Monthly Projection: custom HTML field (read-only matrix)  │
│  Tech: vanilla JS + CSS Grid (~200 lines, no framework)      │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│  LAYER 2 — CALCULATION (source of truth)                     │
│  dcnet_pakd/rules/engine.py — pure Python                    │
│  • Called from DocType.validate() on server                  │
│  • Exposed via frappe.call() for client-side live preview    │
│  • 100% of golden tests run against this module, not the UI  │
│  NO client-side formula engine. Ever.                        │
└──────────────────────────────────────────────────────────────┘
                              ↓ on print
┌──────────────────────────────────────────────────────────────┐
│  LAYER 3 — LEGAL DOCUMENT                                    │
│  Jinja HTML print format (one per pakd_type)                 │
│  • Pixel-close to Excel layout                               │
│  • @media print CSS for signed paper copy                    │
│  • Signature block auto-selects by branch × channel          │
│  Tech: Frappe Print Format with Jinja2 + vanilla CSS         │
└──────────────────────────────────────────────────────────────┘
```

### Rejected alternatives

| Option | Why rejected |
|---|---|
| **Embedded Handsontable** | (a) commercial license ≥$900/year/dev, (b) duplicates formula logic on client → drift risk with server rule engine, (c) bypasses Frappe workflow/permission/audit |
| **Embedded Univer / Luckysheet** | MIT-licensed but same drift risk (2MB bundle, client-side HyperFormula duplicates server); maintenance risk on young libraries |
| **x-spreadsheet** | Lightweight but abandoned (last release 2021); same drift concerns |
| **Frappe form only, no custom matrix widget** | 12-month breakdown rendered as a vertical list is unreadable; users reject it |
| **Full React/Vue SPA inside Frappe Desk** | Heavy toolchain, loses Frappe native behavior (workflow actions, permission hooks); not justified for one form |

### The custom HTML matrix widget (Layer 1, detail)

A Frappe "HTML" field on the DocType renders a read-only 12-month (+setup) matrix:

```
                 Setup    T1      T2      T3      ...    T12    Tổng
Doanh thu HĐ     3000     13500   13500   13500   ...    13500  162000
Chi phí MS          0      1050    1050    1050   ...     1050   12600
Chi phí AddCost     0      2250    2250    2250   ...     2250   27000
Phí GPVT            0       297     297     297   ...      297    3564
Lương KD            0       630     630     630   ...      630    7560
─────────────────────────────────────────────────────────────────────
Doanh thu DV     3000      9273    9273    9273   ...     9273  111276
```

Implementation sketch (`public/js/pakd_form.bundle.js`):

```javascript
frappe.ui.form.on('Phuong An Kinh Doanh', {
  refresh(frm) {
    if (frm.doc.pakd_type !== 'Recurring Telecom') return;
    render_monthly_matrix(frm);
  },
  validate(frm) { render_monthly_matrix(frm); }
});

function render_monthly_matrix(frm) {
  const grid = frm.get_field('monthly_matrix_html').$wrapper[0];
  const rows = frm.doc.monthly_projection || [];
  grid.innerHTML = build_matrix_html(rows);  // CSS Grid table
}
```

~150–250 lines of vanilla JS + ~50 lines of CSS. No build step.

### When the user clicks "Save"

1. Client sends raw field values to server (Frappe standard POST)
2. `validate()` runs the rule engine, overwrites all computed fields with canonical values
3. Server returns the recomputed doc
4. Frappe form refreshes → custom widget re-renders from the new values

If client JS showed different numbers than server computes → server wins, user sees the correction, zero drift possible. This is the whole point of not embedding a client formula engine.

### Printing

`frappe --site dcnet.localhost print Phuong\ An\ Kinh\ Doanh PAKD-2026-0001` renders the Jinja template. CSS uses `@page { size: A4 landscape; margin: 15mm; }` to match the Excel landscape A4 layout. Signature block gets 3/4/5 columns via `{% if branch == 'HN' and channel == 'Nhân viên' %}...{% endif %}`.

### Migration of legacy Excel PAKDs

One-shot importer `dcnet_pakd/commands/import_legacy_excel.py`:
1. Reads `.xlsx` with `openpyxl` (already in bench env, see pattern used in `docs/accounting-requirements/converted/`)
2. Maps cells to PAKD fields via a per-template mapping dict
3. Calls `frappe.get_doc({doctype: "Phuong An Kinh Doanh", ...}).insert()`
4. Optionally attaches the original `.xlsx` file to the new doc via Frappe File
5. Runs golden test assertions against the parsed values → flags any mismatch

Not part of Sprint 1 deliverable — deferred unless DCNET needs to import historical data.

### Deferred fallback (v2)

If, after Sprint 1, DCNET users push back and ask for a "真正 Excel-like" editing experience: add a **"Advanced Edit" tab** using **Univer (MIT)** as a *view only* matrix editor. The Univer grid writes back to Frappe doc fields on blur; **server rule engine still owns calculation**. This preserves the single-source-of-truth invariant while giving power users the tactile Excel feel. Scope only if requested.

---

## Appendix A — Formula Verification Matrix

Every formula from the three Excel templates, mapped to the corresponding computation in the rule engine. **Every row here becomes one unit test case** in `tests/test_rules_engine.py`.

### A.1 Mẫu 01 — Recurring Telecom

**Input fixture** (`tests/golden/mau_01_fixture.json`):
```json
{
  "pakd_type": "Recurring Telecom",
  "items": [{
    "qty": 1,
    "unit_price": 13500,
    "setup_fee": 3000,
    "add_costs_unit_price": 3000
  }],
  "rule": {
    "manager_services_rate": 0.10,
    "manager_services_base": "Revenue - AddCostsUnitPrice",
    "add_costs_rate": 0.75,
    "add_costs_base_field": "add_costs_unit_price",
    "license_fee_rate": 0.022,
    "license_fee_base": "Revenue",
    "sales_commission_rate": 0.06,
    "sales_commission_base": "Revenue - AddCostsUnitPrice"
  }
}
```

**Expected values per month (month N, N ∈ [1..12]):**

| Excel cell | Formula | Expected | Rule engine output | Test |
|---|---|---|---|---|
| `E19` | `=E16-E20` | 10500 | `base_ms = unit_price - add_costs_unit_price` | `test_ms_base_mau_01` |
| `E21` | `=E16` | 13500 | `base_lf = unit_price` | `test_lf_base_mau_01` |
| `E22` | `=E16-E20` | 10500 | `base_sc = unit_price - add_costs_unit_price` | `test_sc_base_mau_01` |
| `G16..R16` | `=$E$16` | 13500 ea | `month.revenue = unit_price` | `test_month_revenue_mau_01` |
| `G19` | `=$D$19*$E$19` | 1050 | `ms = 0.10 * 10500` | `test_ms_month_mau_01` |
| `G20` | `=$E$20*$D$20` | 2250 | `ac = 0.75 * 3000` | `test_ac_month_mau_01` |
| `G21` | `=$D$21*$E$21` | 297 | `lf = 0.022 * 13500` | `test_lf_month_mau_01` |
| `G22` | `=$D$22*$E$22` | 630 | `sc = 0.06 * 10500` | `test_sc_month_mau_01` |
| `G18` | `=SUM(G19:G22)` | 4227 | `total_cost = 1050+2250+297+630` | `test_total_cost_month_mau_01` |
| `G17` | `=G16-G18` | 9273 | `revenue_service = 13500 - 4227` | `test_revenue_service_month_mau_01` |
| `S16` | `=SUM(G16:R16)` | 162000 | `sum 12 months` | `test_annual_revenue_mau_01` |
| `S17` | `=SUM(G17:R17)` | 111276 | `sum 12 months` | `test_annual_revenue_service_mau_01` |
| `S18` | `=SUM(G18:R18)` | 50724 | `sum 12 months` | `test_annual_cost_mau_01` |
| `S19..S22` | `=SUM(...)` | 12600/27000/3564/7560 | `sum 12 months each cost` | `test_annual_cost_breakdown_mau_01` |
| `F17` | `=F16-(F19+F21+F20+F22)` | (compute from setup inputs) | `month_0_revenue_service = setup_fee - sum(month_0_costs)` | `test_setup_month_mau_01` |

**Total:** 95 formulas → ~16 unique test cases (the 12-month repetition collapses into one parametrized test).

### A.2 Mẫu 02 — Monthly FTTH Rollup

**Input fixture** (`tests/golden/mau_02_fixture.json`):
```json
{
  "pakd_type": "Monthly FTTH Rollup",
  "items": [
    {"revenue_actual": 5000, "salary_coefficient": 0.06},
    {"revenue_actual": 3000, "salary_coefficient": 0.06}
  ],
  "optional_costs": [
    {"cost_kind": "Add Costs (IT/Đối tác)", "cost_coefficient": 0.75, "revenue_base": 1000},
    {"cost_kind": "Manager Services (IT/Đối tác)", "cost_coefficient": 0.10, "revenue_base": 2000}
  ]
}
```

| Excel cell | Formula | Expected | Rule engine output | Test |
|---|---|---|---|---|
| `K13` | `=J13*I13` | 300 | `item[0].sales_commission = 0.06 * 5000` | `test_item_commission_mau_02_row1` |
| `K14` | `=J14*I14` | 180 | `item[1].sales_commission = 0.06 * 3000` | `test_item_commission_mau_02_row2` |
| `I15` | `=SUM(I12:I13)` | 8000 | `total_revenue = sum(revenue_actual)` | `test_total_actual_revenue_mau_02` |
| `K16` | `=SUM(K13:K14)` | 480 | `total_sales_commission = sum()` | `test_total_commission_mau_02` |
| `K18` | `=J18*G18` | 750 | `optional_cost[0].total = 0.75 * 1000` | `test_optional_ac_mau_02` |
| `K19` | `=J19*G19` | 200 | `optional_cost[1].total = 0.10 * 2000` | `test_optional_ms_mau_02` |

**Total:** 6 formulas → 6 tests. Plus 1 structural test: `test_mau_02_revenue_actual_is_user_entered` (assert rule engine does NOT overwrite `revenue_actual`).

### A.3 Mẫu 03 — One-off Sale/Project

**Input fixture** (`tests/golden/mau_03_fixture.json`):
```json
{
  "pakd_type": "One-off Sale/Project",
  "items": [{
    "qty": 1,
    "unit_price": 13500,
    "add_costs_unit_price": 3000
  }],
  "rule": {
    "manager_services_rate": 0.10,
    "manager_services_base": "Revenue - AddCostsLineTotal",
    "add_costs_rate": 0.75,
    "add_costs_base_field": "add_costs_unit_price",
    "license_fee_rate": 0.00,
    "sales_commission_rate": 0.06,
    "sales_commission_base": "Revenue - AddCostsUnitPrice"
  }
}
```

| Excel cell | Formula | Expected | Rule engine output | Test |
|---|---|---|---|---|
| `F16` | `=E16` | 13500 | `revenue_contract = qty * unit_price` (qty=1) | `test_revenue_mau_03` |
| `F20` | `=E20*D20` | 2250 | `add_costs = 0.75 * 3000` | `test_add_costs_mau_03` |
| `F19` | `=D19*(F16-F20)` | 1125 | `ms = 0.10 * (13500 - 2250)` (base = Revenue − AddCostsLineTotal) | `test_ms_mau_03` **← key distinction** |
| `E21` | `=E16-E20` | 10500 | `base_sc = unit_price - add_costs_unit_price` | `test_sc_base_mau_03` |
| `F21` | `=D21*E21` | 630 | `sc = 0.06 * 10500` | `test_sc_mau_03` |
| `F18` | `=SUM(F19:I21)` | 4005 | `total_cost = 2250 + 1125 + 630` | `test_total_cost_mau_03` |
| `F17` | `=F16-F18` | 9495 | `revenue_service = 13500 - 4005` | `test_revenue_service_mau_03` |

**Total:** 8 formulas → 7 tests.

**The critical assertion:** `test_ms_mau_03` must produce **1125** (not 1050 as in Mẫu 01). If rule engine accidentally uses `Revenue - AddCostsUnitPrice` here, this test fails. This is what prevents the Mẫu 01 ↔ Mẫu 03 base ambiguity from leaking into production.

### A.4 Cross-template invariants

One parametrized test runs against all three fixtures:

| Invariant | Assertion |
|---|---|
| `revenue_contract >= total_cost` | Otherwise PAKD is loss-making — should only warn, not block (DCNET may still want to sign unprofitable deals) |
| `sales_commission >= 0` | Negative commission is always a bug |
| `total_revenue_service = total_revenue_contract - total_cost` | Header totals match item sums |
| `effective_payroll_month` respects cut-off | Submit on day 5 → previous month; day 6 → current month |

### A.5 Running the verification

```bash
cd /home/long/long/frappe-bench-dcnet
bench --site dcnet.localhost run-tests --app dcnet_pakd --module dcnet_pakd.tests.test_rules_engine
```

Expected output: **30+ tests passing, 0 failures**. Any regression in the rule engine — e.g., accidentally swapping `Revenue - AddCostsUnitPrice` for `Revenue - AddCostsLineTotal` — fails immediately with a clear diff.

