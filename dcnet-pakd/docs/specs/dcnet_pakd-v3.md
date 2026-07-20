# dcnet_pakd — Spec v3 (Post Architecture Split)

> **Status:** Draft spec v3 — rewrites v2 to align with the dcnet_contract/dcnet_pakd architecture split.
> **Target bench:** frappe-bench-dcnet (Frappe v16.12.2 + ERPNext v16.12.0)
> **Depends on:** dcnet_contract >= 0.1.0 (Sprint A1-A5 complete)
> **Created:** 2026-04-13
> **Supersedes:** docs/specs/dcnet_pakd.md (v2, outdated)

---

## 1. What changed from v2

| v2 (monolithic) | v3 (thin layer) |
|---|---|
| PAKD owns billing schedule + monthly projection | dcnet_contract owns billing schedule; PAKD reads via contract_ref |
| Commission posted on PAKD Approved | Commission posted on payment (cash-basis), triggered by dcnet_contract event |
| PAKD Monthly Projection child table (12 rows) | Removed — billing schedule lives in Contract |
| Cutoff by submission_date | Cutoff by payment_date |
| PAKD owns Sales Invoice creation | dcnet_contract auto-invoice scheduler does this |
| 6 DocTypes | 5 DocTypes (removed Monthly Projection) |

**What PAKD still owns:** Commission policy (rule templates), chi phí ngoài (MS/AC/GPVT), approval workflow, commission posting (AS + JE), print formats (Mẫu 01/02/03), workspace.

---

## 2. Why this app exists

DCNET is migrating from Misa to ERPNext. Every other requirement can be met by ERPNext + vn_accounting + dcnet_contract. **One cannot:** the PAKD — sales commission worksheet currently maintained as 3 Excel templates (Mẫu 01/02/03).

PAKD bridges:
```
DCNET Contract (billing_schedule.paid event) → PAKD → HRMS (Additional Salary)
                                                    → Accounting (Journal Entry for chi phí ngoài)
```

---

## 3. Scope

### In scope (Sprint B1-B5)
- DocType Phuong An Kinh Doanh + child tables
- Commission rule engine (configurable rates per service/branch)
- PAKD Commission Line — per billing period × component tracking
- Cash-basis commission posting: PE paid → commission line Posted → AS + JE
- Approval workflow (4 routes: HCM-NV / HCM-BGĐ / HN-NV / HN-BGĐ)
- Chi phí ngoài: Manager Services, Add Costs, Phí GPVT (Journal Entry, draft)
- Cutoff logic (payment_date.day <= 5 → previous payroll month)
- Print formats (3 × Mẫu 01/02/03)
- PAKD Settings (accounts, cutoff day, default template)
- Workspace + reports
- Permissions per role (6 approval roles + Accountant)

### Out of scope
- Billing schedule generation (dcnet_contract)
- Auto-invoice (dcnet_contract)
- Payment Entry hook (dcnet_contract fires event, PAKD listens)
- Shadow SO (dcnet_contract)
- Contract lifecycle (dcnet_contract)
- Multi-currency (VND only)
- Historical Excel PAKD import

---

## 4. Data model

### 4.1 Phuong An Kinh Doanh (main DocType)

**Not submittable.** Uses workflow_state for approval lifecycle (Draft → ... → Approved). docstatus stays 0 throughout — PAKD is a workflow container, not an accounting commitment.

Naming: `PAKD-.YYYY.-.#####`

> **Why:** `PAKD` prefix recognizable in reports. Year-reset keeps numbers short. Not service-type-prefixed because one PAKD may change type during drafting.

**Section: Header**
- `pakd_type` — Select: `Recurring Telecom\nMonthly FTTH Rollup\nOne-off Sale/Project`, reqd
- `contract_ref` — Link DCNET Contract, reqd (replaces v2 "Link Sales Order or free-text")
- `contract_no_external` — Data, fetch_from contract_ref.contract_no_external, read_only
- `customer` — Link Customer, fetch_from contract_ref.customer, read_only
- `customer_name` — Data, fetch_from contract_ref.customer_name, read_only
- `sales_person` — Link Employee, fetch_from contract_ref.sales_person, read_only
- `sales_person_name` — Data, fetch_from contract_ref.sales_person_name, read_only
- `department` — Link Department, fetch_from contract_ref.department, read_only
- `branch` — Link Branch, fetch_from contract_ref.branch, read_only
- `company` — Link Company, fetch_from contract_ref.company, read_only
- `channel` — Select: `Nhân viên\nBGĐ`, reqd (drives approval route)
- `service_type` — Select, fetch_from contract_ref.service_type, read_only
- `project_category` — Select, fetch_from contract_ref.project_category, read_only

**Section: PAKD Items**
- `items` — Table PAKD Item, reqd

**Section: Computed Totals** (read_only, server-computed in validate)
- `total_revenue_contract` — Currency
- `total_add_costs` — Currency
- `total_manager_services` — Currency
- `total_license_fee` — Currency (GPVT, only for Recurring Telecom)
- `total_sales_commission` — Currency
- `total_cost` — Currency (sum of 4 above)
- `total_revenue_service` — Currency (total_revenue_contract - total_cost)

**Section: Commission Tracking**
- `commission_lines` — Table PAKD Commission Line, read_only (generated on Approved)

**Section: Status**
- `status` — Select: `Draft\nPending GĐ TT KD\nPending P. Tổng hợp\nPending GĐ CN\nPending BGĐ\nApproved\nRejected`, default Draft
- `workflow_state` — managed by Frappe Workflow

**Section: Payroll**
- `additional_salary` — Link Additional Salary, read_only (back-ref after commission posted)

### 4.2 PAKD Item (child table)

One row = one hạng mục. Shape varies by pakd_type (conditional fields via depends_on).

| Field | Type | Recurring | FTTH Rollup | One-off |
|---|---|---|---|---|
| item_label | Data, reqd | ✓ | ✓ | ✓ |
| uom | Link UOM | HĐ | HĐ | varies |
| qty | Float | 1 | 1 | N |
| unit_price | Currency, reqd | ✓ (monthly) | ✓ | ✓ |
| add_costs_unit_price | Currency | ✓ (user enters) | — | ✓ |
| months_billed | Int | — | ✓ | — |
| months_promo | Int | — | ✓ | — |
| contract_line_ref | Data | — | ✓ (Số HĐ) | — |
| revenue_actual | Currency | — | ✓ (user-entered) | — |
| salary_coefficient | Float | — | ✓ (Hệ số lương KD) | — |

> **Why:** Mẫu 02 (FTTH Rollup) uses a manual coefficient per contract line (column J in Excel) instead of a fixed rate from Rule Template. This reflects DCNET's practice where each FTTH DN contract has a negotiated commission coefficient that varies by deal size and customer relationship. Not automatable from rules alone.
| **Computed (server)** |
| revenue_contract | Currency, read_only | qty × unit_price | revenue_actual | qty × unit_price |
| add_costs | Currency, read_only | rule-based | — | rule-based |
| manager_services | Currency, read_only | rule-based | — | rule-based |
| license_fee | Currency, read_only | rule-based (2.2%) | — | — |
| sales_commission | Currency, read_only | rule-based | coeff × revenue_actual | rule-based |
| total_cost | Currency, read_only | sum of costs | — | sum of costs |
| revenue_service | Currency, read_only | revenue - total_cost | — | revenue - total_cost |

### 4.3 PAKD Commission Line (child table)

1 row = 1 (billing_period × cost_component). Generated when PAKD is Approved. State tracks payment-triggered posting.

> **Why:** Granular tracking (1 line per period × component) enables: (1) partial payment posting (only paid periods get commission), (2) precise reversal on PE cancel (only affected lines revert), (3) prepay handling (1 PE posts all 12 lines at once → 1 AS gom all). Aggregated tracking would lose the period-level linkage needed for cash-basis flow.

| Field | Type | Notes |
|---|---|---|
| billing_schedule_idx | Int | References Contract billing_schedule.month_index |
| component | Select | `Manager Services\nAdd Costs\nPhí GPVT\nLương KD` |
| amount | Currency | Computed from rule engine |
| state | Select | `Pending\nPosted\nCancelled` — Pending=waiting for payment, Posted=AS/JE created |
| payroll_month | Data (YYYY-MM) | Set when Posted, using payment_date cutoff |
| additional_salary | Link Additional Salary | For Lương KD component |
| journal_entry | Link Journal Entry | For MS/AC/GPVT components |
| payment_entry | Link Payment Entry | The PE that triggered this posting |

**State machine:**
```
Pending  → Posted     (billing_period_paid event from dcnet_contract)
Pending  → Cancelled  (contract cancelled / PAKD revision)
Posted   → (terminal)
Cancelled → (terminal)
```

### 4.3.2 Khi nào khác?

- **PE linked to multiple SIs from different Contracts:** Each SI is processed independently. PAKD PE hook iterates each SI → finds its Contract → finds its PAKD → posts matching commission lines. No cross-contamination.
- **PAKD approved after Contract cancelled:** validate() should check `contract_ref.status != "Cancelled"` before allowing workflow advance to Approved. If Contract cancelled between PAKD creation and approval → reject with error.
- **Two PAKDs for same Contract:** Not valid for pakd_type Recurring/One-off (1:1). Valid for Monthly FTTH Rollup (different months). Enforce unique constraint: `(contract_ref, pakd_type)` for non-Rollup types.
- **Partial payment (PE < SI outstanding):** billing_schedule stays "Invoiced" (dcnet_contract only flips to Paid when SI fully paid). Commission lines stay Pending. No partial commission posting.
- **No template matches at any tier:** Rule engine raises `frappe.throw("Không tìm thấy mẫu quy tắc hoa hồng cho {service_type}/{branch}")`. PAKD cannot be saved without matching rule. Kế toán must create a Rule Template first.
- **`cutoff_day` = payment day (boundary):** Spec says `day <= cutoff_day` → previous month. So day 5 with cutoff=5 → previous month. Day 6 → current month. Boundary is inclusive.

### 4.3.1 Engine data source

The commission rule engine (`utils/engine.py:compute_pakd_line()`) needs Contract-level financial data that is NOT stored on PAKD. At compute time, the engine reads the linked Contract via `frappe.get_cached_doc("DCNET Contract", pakd.contract_ref)` and uses:

- `contract.package_term_months` — total contract duration for per-period allocation
- `contract.payment_mode` — Prepay vs Monthly behavior
- `contract.setup_fee` — for `applies_to_setup_fee` flag on Rule Component
- `contract.unit_price_total` — per-period revenue (base for commission calc)
- `contract.contract_type` — Recurring vs One-off drives pakd_type rule selection
- `contract.billing_schedule` — list of periods for generating Commission Lines

These are accessed at runtime, NOT duplicated on PAKD as fetch_from fields. Single source of truth = Contract.

### 4.4 PAKD Commission Rule Template (standalone)

Configurable rates per (service_type, branch, pakd_type). 4-tier resolution: contract override → branch+service → service → pakd_type default.

| Field | Type |
|---|---|
| template_name | Data |
| valid_from | Date |
| valid_to | Date (optional) |

> **Why:** Effective date range allows DCNET to change commission rates prospectively without affecting historical PAKDs. If two templates overlap for the same scope, the one with the latest `valid_from` wins (most recent policy takes precedence).
| scope_branch | Link Branch (optional) |
| scope_service_type | Select (optional) |
| scope_pakd_type | Select, reqd |
| components | Table PAKD Rule Component |

**PAKD Rule Component** (child table of Rule Template):
| Field | Type |
|---|---|
| component_name | Select: Manager Services / Add Costs / Phí GPVT / Lương KD |
| rate | Percent |
| base_formula | Select: unit_price / unit_price_minus_add_costs / add_costs_gross / revenue_actual |
| applies_to_setup_fee | Check (default 0) |

### 4.5 PAKD Settings (Single DocType)

| Field | Type | Default |
|---|---|---|
| cutoff_day_of_month | Int | 5 |
| default_commission_template | Link PAKD Commission Rule Template | |
| account_manager_services | Link Account | 6418 |
| account_add_costs | Link Account | 6418 |
| account_gpvt | Link Account | 6425 |
| counter_account_manager_services | Link Account | 3388 |
| counter_account_add_costs | Link Account | 3388 |
| salary_component_luong_kd | Link Salary Component | Lương kinh doanh |

---

## 5. Commission flow (cash-basis)

```
1. Contract activated → billing_schedule populated (dcnet_contract)
2. PAKD created referencing Contract → approval workflow starts
3. PAKD Approved → commission_lines generated (1 per billing_period × component)
   All lines in state "Pending"
4. Payment Entry submitted → dcnet_contract PE hook flips billing_schedule → "Paid"
   → dcnet_pakd PE hook (on_submit, runs AFTER dcnet_contract's) finds matching
     commission_lines via Contract link → posts them
5. Commission posting per component:
   - Lương KD → HRMS Additional Salary (1 AS per payment event, gom all periods paid)
   - MS + AC + GPVT → Journal Entry (Draft, kế toán submit)
6. Cutoff: if payment_date.day <= cutoff_day → payroll_month = previous month
```

**Prepaid 12 months:** 1 PE → all 12 billing_schedule rows flip Paid → 12 commission lines Posted → 1 Additional Salary gom all.

### 5.0.1 Khi nào khác?

- **PE amended (not cancelled):** Frappe doesn't support PE amendment after submit. PE can only be cancelled and re-created. So this case doesn't exist.
- **AS already in submitted Payroll Entry when PE cancelled:** Commission line stays Posted (cannot auto-reverse submitted payroll). Alert shown: "Lương KD đã nằm trong bảng lương đã duyệt. Liên hệ kế toán để điều chỉnh thủ công." PE cancellation is NOT blocked — just warns.
- **PAKD re-opened after Rejection:** Allowed — workflow supports Rejected → Draft transition. Commission lines from previous approval (if any) are already Cancelled when PAKD was rejected. New approval generates fresh commission lines.

### 5.1 Integration mechanism (CRITICAL — NOT publish_realtime)

dcnet_contract uses `frappe.publish_realtime("dcnet_contract.billing_period_paid", ...)` — this is a **browser WebSocket event**, NOT a server-side hook. PAKD cannot "listen" to it from Python.

**Correct mechanism:** PAKD registers its own `doc_events` hook on Payment Entry:

```python
# dcnet_pakd/hooks.py
doc_events = {
    "Payment Entry": {
        "on_submit": "dcnet_pakd.dcnet_pakd.events.on_payment_entry_submit",
        "on_cancel": "dcnet_pakd.dcnet_pakd.events.on_payment_entry_cancel",
    },
    "DCNET Contract": {
        "on_cancel": "dcnet_pakd.dcnet_pakd.events.on_contract_cancel",
    },
}
```

Frappe runs ALL registered doc_event hooks — dcnet_contract's PE hook runs first (flips billing_schedule to Paid), then dcnet_pakd's PE hook runs (finds Paid rows, posts commission). Order guaranteed by app dependency (dcnet_pakd depends on dcnet_contract → loads after).

### 5.2 Contract cancel → commission cancel

When a DCNET Contract is cancelled, PAKD's `on_contract_cancel` hook:
- Finds all PAKD referencing this contract via `contract_ref`
- Flips all Pending commission_lines → Cancelled
- Already-Posted lines are NOT reversed (immutable — accountant handles manually)

### 5.3 Payment Entry cancel → commission reversal

When a PE is cancelled:
- dcnet_contract's PE on_cancel hook reverts billing_schedule rows (Paid → Invoiced)
- dcnet_pakd's PE on_cancel hook finds commission_lines that were Posted by this PE (via `payment_entry` link) and:
  - Cancels the linked Additional Salary (if not yet in submitted Payroll Entry)
  - Cancels the linked Journal Entry (if still Draft)
  - Flips commission_line state: Posted → Cancelled
  - If AS/JE already submitted by accountant → show alert "Manual reversal needed"

### 5.4 Contract expiry → no commission impact

When a Contract expires (Active → Expired), no commission_lines change. Expired means the contract ran its full term — all billing periods should already be Paid. If some are still Invoiced/Overdue, they stay Pending on the commission side until paid or written off.

---

## 6. Approval workflow

Same as v2 §6. One Frappe Workflow "PAKD Approval" with 7 states, 4 routes (HCM-NV, HCM-BGĐ, HN-NV, HN-BGĐ). 6 custom roles.

---

## 7. Accounting integration

On each payment event (not on PAKD Approved — that's the v2 change):

**For Lương KD:** Create Additional Salary
- employee = PAKD.sales_person
- salary_component = Settings.salary_component_luong_kd
- amount = sum of commission_lines being posted where component="Lương KD"
- payroll_date = last day of payroll_month

**For MS/AC/GPVT:** Create draft Journal Entry
- DR Settings.account_manager_services — total MS for these periods
- DR Settings.account_add_costs — total AC
- DR Settings.account_gpvt — total GPVT
- CR Settings.counter_account_* — matching credit side
- JE is Draft — accountant reviews and submits

---

## 8. Print formats

Three Jinja HTML print formats matching Excel Mẫu 01/02/03. Same as v2 §9.

---

## 9. Sprint plan

| Sprint | Scope | Depends on |
|---|---|---|
| B1 | Rule engine + golden tests (replay Excel formulas) | A1 complete |
| B2 | PAKD DocType + Commission Line + approval workflow | B1 |
| B3 | Payment event listener + commission posting (AS + JE) | B2 + A2 (PE hook) |
| B4 | Print formats (3 × Mẫu) + workspace + reports | B3 |
| B5 | Integration testing full chain | B4 |

---

## 10. App scaffold

```
apps/dcnet_pakd/
  pyproject.toml          # depends: frappe, erpnext, dcnet_contract, hrms
  README.md
  .gitignore
  dcnet_pakd/
    __init__.py
    hooks.py
    modules.txt            # "DCNET PAKD"
    patches.txt
    install.py
    dcnet_pakd/
      doctype/
        phuong_an_kinh_doanh/
        pakd_item/
        pakd_commission_line/
        pakd_commission_rule_template/
        pakd_rule_component/
        pakd_settings/
      utils/
        engine.py           # pure: compute_pakd_line()
      events.py             # listener for billing_period_paid
      integrations/
        payroll.py          # push_to_additional_salary()
        accounting.py       # post_journal_entry()
    tests/
      test_engine.py        # pure golden tests
      test_commission_flow.py
      helpers.py
```

---

## 11. Permissions

| Role | Read | Write | Create | Workflow Advance |
|---|---|---|---|---|
| PAKD Sales Rep | own only | own Draft | ✓ | → Pending GĐ TT KD |
| PAKD Sales Director HCM | branch=HCM | Pending GĐ TT KD | — | → Pending P. Tổng hợp |
| PAKD Sales Director HN | branch=HN | Pending GĐ TT KD | — | → Pending P. Tổng hợp |
| PAKD General Department | all | Pending P. Tổng hợp | — | → Pending GĐ CN / BGĐ |
| PAKD Branch Director HN | branch=HN | Pending GĐ CN | — | → Pending BGĐ |
| PAKD Board | all | Pending BGĐ | — | → Approved |
| PAKD Accountant | all | — | — | — (read-only + post payroll) |
| System Manager | all | all | ✓ | all |

PAKD Commission Rule Template: PAKD Accountant + System Manager can create/edit. Others read-only.
PAKD Settings: PAKD Accountant + System Manager only.

User Permission on Branch enforces HCM/HN segregation.

---

## 12. Decisions locked

1. **Thin layer** — PAKD only owns commission policy + approval, not billing/cash flow
2. **Cash-basis** — commission posts on payment, not on PAKD approval
3. **1 NVKD per contract** — no co-sales split
4. **3 pakd_types in 1 DocType** — conditional fields via depends_on
5. **Split repo** — dcnet-cloud/dcnet-pakd, depends dcnet_contract >= 0.1.0
6. **Settings DocType** — all accounts configurable via UI
7. **Cutoff by payment_date** — NOT submission_date (v2 was wrong)
8. **Commission Line per billing_period × component** — granular tracking
9. **Setup fee excluded from commission** — month_index=0, item_type=Setup Fee skipped
10. **PE on_cancel needed on dcnet_contract side** — dcnet_contract A2 only hooks PE on_submit; A2 patch needed to add on_cancel that reverts billing_schedule Paid → Invoiced. PAKD B3 adds its own PE on_cancel for commission reversal.
11. **English-first workflow states** — All workflow states MUST be English in source (Draft, Pending Sales Director, Pending General Dept, Pending Branch Director, Pending Board, Approved, Rejected). Vietnamese display via translations/vi.csv. Current Vietnamese states in code violate the English-first rule and must be refactored.
12. **Commission JE always Draft** — All commission Journal Entries created as Draft. Kế toán reviews and submits manually. Not year-end specific.
13. **Revenue recognized immediately on SI** — dcnet_contract recognizes revenue (CR 5113) at invoice date, even for prepay. No deferred revenue (TK 3387). PAKD commission is cash-basis (posts on PE, not on SI).
14. **Cutoff no fiscal year override** — Payment month = commission month. No special handling at fiscal year boundary. "Lương thưởng tháng nào trả hạch toán vào tháng đấy."
15. **FTTH HGD valid service_type** — 8 service types total. HGD customers are individuals (no MST). Individual SI per customer mandatory for vn_banking auto-match.
16. **"Tạo PAKD" button on Contract form** — When Contract is Active, show button to create PAKD pre-filled with contract_ref. Implemented in dcnet_contract client script or dcnet_pakd doc_events.

---

## 13. Deployment checklist

### Install
1. `bench get-app https://github.com/dcnet-cloud/dcnet-pakd`
2. `bench --site dcnet.localhost install-app dcnet_pakd`
3. `bench --site dcnet.localhost migrate`
4. Verify: `bench --site dcnet.localhost execute "frappe.get_installed_apps()"` contains dcnet_pakd
5. Verify: PAKD Settings singleton exists with default accounts
6. Verify: 3 Rule Templates seeded
7. Verify: "PAKD Approval" workflow exists with 7 states

### Rollback
1. `bench --site dcnet.localhost uninstall-app dcnet_pakd --yes`
2. `pip uninstall dcnet_pakd`
3. Remove `dcnet_pakd` from `sites/apps.txt`
4. `bench --site dcnet.localhost migrate`
Note: dcnet_contract is NOT affected by PAKD uninstall (no reverse dependency).

### Post-deploy verify
- Create a test PAKD referencing an existing Contract → validate computes costs
- Advance through workflow → commission lines generated on Approved
- Check PAKD Settings accounts match VN COA
