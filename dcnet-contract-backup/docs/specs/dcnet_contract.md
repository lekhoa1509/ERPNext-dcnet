# dcnet_contract — Spec Sprint A1

> **Scope sprint này:** DocType `DCNet Contract` + `DCNet Contract Item` + `DCNet Contract Billing Schedule` + `DCNet Contract Settings` + state machine contract + hooks sinh billing schedule + proration + permission matrix + test fixtures.
>
> **Ngoài scope A1** (có entry ở cuối file, để reference — KHÔNG code trong A1): auto-invoice scheduler (A2), Payment Entry hook (A2), overdue scheduler (A2), shadow SO sync (A3), revision chain (A4), print format (A4), workspace + reports (A5), toàn bộ PAKD (sprint B).
>
> **Tiền đề đã chốt** (xem `architecture-contract-and-pakd.md` + `dcnet_contract-open-questions-lite.md`): Option D shadow SO, 1 NVKD/contract, cash-basis commission, split repo, Settings DocType pattern, `service_type` 7 giá trị B2B, HCM + HN, VND only.

---

## 1. Mục tiêu Sprint A1

Cuối sprint A1:

1. Cài được app `dcnet_contract` vào bench `frappe-bench-dcnet`, migrate xanh.
2. Kế toán/Sales Manager tạo được 1 `DCNet Contract` Draft, điền header + line item + submit → Active.
3. Hook `on_submit` sinh ra `DCNet Contract Billing Schedule` rows đúng theo `package_term_months` + `payment_mode`, có áp proration cho tháng đầu/cuối khi `acceptance_date` không rơi đúng đầu tháng. (Lý do chọn `on_submit` thay vì `after_insert`: xem §6 — không muốn sinh schedule cho Draft chưa chắc được submit.)
4. `DCNet Contract Settings` (Single) có UI form, kế toán verify + override được các default (grace period, rounding, branch→cost center map, payment terms).
5. `after_install` hook seed defaults vào Settings dựa trên VN COA TT99 (`vn_accounting` phải cài trước).
6. Permission matrix hoạt động: Sales Rep tạo Draft, Sales Manager submit → Active, System Manager cancel.
7. Test suite golden: 3 test case proration (đầu tháng / giữa tháng / cuối tháng) + 2 test state machine (Draft→Active, Active→Cancelled) pass trên `bench run-tests --app dcnet_contract`.

Không có auto-invoice, không có PE hook, không có scheduler trong sprint này. Billing schedule sinh ra nhưng tất cả rows đều ở state `Projected` chờ A2.

---

## 2. App scaffold

```
apps/dcnet_contract/
├── pyproject.toml                          # name=dcnet_contract, deps: frappe, erpnext, vn_accounting
├── README.md
├── .gitignore
└── dcnet_contract/
    ├── __init__.py                         # __version__ = "0.1.0"
    ├── hooks.py
    ├── modules.txt                         # "DCNet Contract"
    ├── patches.txt                         # empty but required
    ├── install.py                          # after_install: seed Settings defaults
    ├── config/
    │   └── desktop.py                      # module entry (A5 fills this out)
    ├── fixtures/                           # empty in A1 (no fixture yet)
    ├── dcnet_contract/
    │   ├── doctype/
    │   │   ├── dcnet_contract/
    │   │   │   ├── dcnet_contract.json
    │   │   │   ├── dcnet_contract.py       # controller
    │   │   │   └── test_dcnet_contract.py  # golden tests
    │   │   ├── dcnet_contract_item/
    │   │   │   ├── dcnet_contract_item.json    # child table
    │   │   │   └── dcnet_contract_item.py
    │   │   ├── dcnet_contract_billing_schedule/
    │   │   │   ├── dcnet_contract_billing_schedule.json    # child table
    │   │   │   └── dcnet_contract_billing_schedule.py
    │   │   └── dcnet_contract_settings/
    │   │       ├── dcnet_contract_settings.json            # Single
    │   │       └── dcnet_contract_settings.py
    │   └── utils/
    │       ├── __init__.py
    │       ├── billing_schedule.py         # pure logic: generate_schedule() + proration
    │       └── state_machine.py            # pure logic: allowed transitions
    └── tests/
        └── test_billing_schedule.py        # pure-function tests (no DB)
```

**Dependency direction:** `dcnet_contract` depends on `frappe`, `erpnext` (cần Customer, Employee, Branch, Cost Center), `vn_accounting` (cần COA TT99 đã cài để seed Settings). KHÔNG depend on `dcnet_pakd` — PAKD sẽ depend ngược lại ở sprint B.

**Dual remote:** `github.com/dcnet-cloud/dcnet-contract`. Không ghi remote cá nhân vào bất kỳ doc/README nào committed lên dcnet-cloud (xem feedback memory `dcnet_no_personal_remote`).

---

## 3. DocType `DCNet Contract`

### 3.1 Naming

- `autoname`: `format:HD-{YYYY}-{#####}` (ví dụ `HD-2026-00001`). Prefix `HD` = "Hợp đồng". Sequence reset theo năm.

> **Why:** `HD` prefix = "Hợp đồng", recognizable to Vietnamese accountants in reports. Year-reset sequence keeps numbers short. Rejected: UUID (not human-readable), autoincrement without year (numbers grow forever).

- Trường `contract_no_external` (Data) chứa số hợp đồng thật từ file giấy (ví dụ `1302/HDDV/DCNET-CBBANK`), dùng cho print format + tham chiếu kế toán cũ. Unique nếu điền.
- Hiển thị ở list view: `name`, `customer`, `service_type`, `status`, `start_date`, `grand_total`.

### 3.2 Fields

Chia thành các section break để UI form gọn.

**Section: Basic Info**
- `customer` — Link Customer, reqd, in_list_view, in_global_search
- `customer_name` — Data, fetch_from `customer.customer_name`, read_only
- `sales_person` — Link Employee, reqd (single NVKD, xem architecture §6)
- `sales_person_name` — Data, fetch_from `sales_person.employee_name`, read_only
- `department` — Link Department, fetch_from `sales_person.department`, read_only
- `branch` — Link Branch, reqd, options filtered to HCM + HN (seeded từ ERPNext Branch master)
- `company` — Link Company, reqd, default from `frappe.defaults.get_user_default("Company")`
- `contract_no_external` — Data, label "Số hợp đồng giấy", unique (sparse), in_list_view

> **Why:** Sparse unique (not reqd) because many contracts don't have a paper contract number yet when created digitally. Unique when filled to prevent duplicate entry of the same paper contract.

- `project_category` — Select, options: `Viễn thông\nCNTT\nVTTB\nThi công`, reqd
- `service_type` — Select, options: `P2P\nMPLS\nILL\nFTTH DN\nFTTH HGD\nIT Managed\nVTTB\nThi công`, reqd. FTTH HGD = hộ gia đình (khách cá nhân, không có MST, cần CMND/CCCD thay vì tax_id).
- `package_name` — Data, label "Tên gói / băng thông", optional (chỉ có cho recurring telecom)
- `installation_address` — Small Text, label "Địa điểm lắp đặt (điểm đầu - điểm cuối)"

**Section: Dates**
- `contract_date` — Date, reqd, label "Ngày ký hợp đồng"
- `acceptance_date` — Date, reqd, label "Ngày nghiệm thu / kích hoạt dịch vụ". Dùng làm `start_date` cho billing schedule.
- `appendix_no` — Data, optional, label "Phụ lục số"
- `appendix_date` — Date, optional
- `end_date` — Date, read_only, computed = `acceptance_date + package_term_months - 1 day` cho recurring, = `acceptance_date` cho one-off.

**Section: Contract Type**
- `contract_type` — Select, options: `Recurring\nOne-off`, reqd. Driven by `service_type`:
  - Recurring: P2P, MPLS, ILL, FTTH DN, FTTH HGD, IT Managed
  - One-off: VTTB, Thi công
  - Validated trong `validate()` — contract_type PHẢI khớp service_type.
- `package_term_months` — Int, mandatory_depends_on `contract_type == "Recurring"`. Options thường gặp: 6, 12, 24. Free int, không enum.
- `payment_mode` — Select, options: `Prepay\nMonthly\nOneOff`, mandatory_depends_on contract_type.
  - Recurring → `Prepay | Monthly`. Monthly nghĩa là xuất hoá đơn hàng tháng. Prepay nghĩa là 1 hoá đơn phủ toàn bộ package_term.
  - One-off → `OneOff`. Xuất đúng 1 hoá đơn.

**Section: Financials**
- `items` — Table `DCNet Contract Item`, reqd (ít nhất 1 row). Chi tiết schema §4.
- `unit_price_total` — Currency, read_only, = `sum(items.amount_per_period)`. Là doanh thu **1 chu kỳ billing** (1 tháng với Monthly, 1 package_term với Prepay, 1 lần với OneOff). Khớp ô `E16` trong Mẫu 01.
- `setup_fee` — Currency, default 0, label "Phí lắp đặt (1 lần)". Cho recurring có phí setup. Hiển thị là `month_index=0` trong billing schedule, KHÔNG phát sinh commission (xem architecture §10 edge case).
- `grand_total` — Currency, read_only, = `unit_price_total × effective_periods + setup_fee`.
  - Recurring Monthly: effective_periods = `package_term_months`
  - Recurring Prepay: effective_periods = `package_term_months` (1 invoice nhưng cover N periods)
  - One-off: effective_periods = 1
- `currency` — Link Currency, reqd, default `VND`, **readonly in v1** (chỉ VND — xem architecture §1).

**Section: Billing schedule**
- `billing_schedule` — Table `DCNet Contract Billing Schedule`, read_only (sinh bởi hook). Chi tiết §5.

**Section: Status**
- `status` — Select, options: `Draft\nActive\nSuspended\nRevised\nCancelled\nExpired`, default `Draft`, read_only (driven bởi state machine trong `on_submit` / custom actions). `Revised` = hợp đồng đã bị thay thế bởi amendment mới (A4 revision chain).
- `amended_from` — Link DCNet Contract, read_only, for Frappe amend workflow (A4 revision chain sẽ build lên đây).

**Not submittable? Có — submittable = 1.** Khác với `Bank Statement Import`, Contract có vòng đời Draft → Active → ... và Frappe `docstatus` matching tự nhiên: Draft = 0, Active = 1, Cancelled = 2. Suspended/Expired là thông tin phụ ghi trong `status` field nhưng `docstatus` vẫn = 1 (Active family).

> **Lưu ý state vs docstatus:** Frappe chỉ có 3 docstatus (0/1/2). Chúng ta dùng docstatus cho Draft/Submitted/Cancelled và thêm `status` field text cho Active/Suspended/Expired subtype trong submitted state. Controller enforce transitions — xem §7.

---

## 4. Child DocType `DCNet Contract Item`

1 row = 1 hạng mục thu/chi tiết trong hợp đồng. Ít nhất 1 row bắt buộc. Mapping trực tiếp từ Mẫu 01 / Mẫu 03 row 16.

**Fields (istable=1):**
- `item_label` — Data, reqd, label "Hạng mục" (ví dụ "Dịch vụ P2P HCM-HN 100Mbps"), in_list_view
- `uom` — Link UOM, default "HĐ" (seed từ ERPNext default), in_list_view
- `qty` — Float, default 1, in_list_view
- `unit_price` — Currency, reqd, in_list_view, label "Đơn giá (chưa VAT)" — **1 period (1 tháng)** cho recurring, 1 lần cho one-off
- `amount_per_period` — Currency, read_only, = `qty × unit_price`, in_list_view
- `erpnext_item` — Link Item, optional. Chỉ bắt buộc cho `parent.contract_type == One-off AND service_type == VTTB` (để A3 shadow SO biết map sang stock item). Recurring + Thi công có thể để trống.
- `description` — Small Text, optional

**Validation:**
- `amount_per_period` auto-compute trong client script (`fetch_from` không được cho cross-field arith, dùng `refresh_field` trong JS).
- Nếu contract_type = One-off AND service_type = VTTB AND erpnext_item trống → validate fail với msg "VTTB contract phải link tới ERPNext Item để sync shadow Sales Order ở sprint A3."

---

## 5. Child DocType `DCNet Contract Billing Schedule`

1 row = 1 chu kỳ thu tiền. Sinh bởi hook, không cho user sửa trực tiếp (read_only ở client).

**Fields (istable=1):**
- `month_index` — Int, reqd, in_list_view. `0` = setup fee row (nếu có). `1..N` = billing period 1..N.
- `period_start` — Date, reqd, in_list_view
- `period_end` — Date, reqd, in_list_view
- `due_date` — Date, reqd, in_list_view. Default = `period_end` (A2 có thể override theo payment_terms).

> **Why:** Default `due_date = period_end` — payment due at end of billing period (standard Vietnamese telecom billing). A2 will override per `payment_terms_template` if configured in Settings.

- `item_type` — Select: `Setup Fee\nService`. `month_index=0` → `Setup Fee`, rest → `Service`.
- `amount` — Currency, reqd, in_list_view. Với proration, amount đã được round theo formula Mẫu 01 (xem §6).
- `is_prorated` — Check, read_only. True nếu period không đủ 1 tháng lịch (tháng đầu kích hoạt giữa tháng, hoặc tháng cuối cắt giữa chừng).
- `state` — Select, reqd, options: `Projected\nInvoiced\nPaid\nOverdue\nCancelled\nWritten Off`, default `Projected`, in_list_view.
  - Sprint A1 chỉ sinh rows với state `Projected`. Các transition khác thuộc A2 (Invoiced, Paid, Overdue) + cancellation flow A4 (Cancelled, Written Off).
- `sales_invoice` — Link Sales Invoice, read_only, sparse. A2 sẽ điền.
- `payment_entry` — Link Payment Entry, read_only, sparse. A2 sẽ điền.

**Uniqueness:** Composite unique `(parent, month_index)` enforced ở controller `validate()`.

---

## 6. Hook `after_insert` / `on_submit` — sinh billing schedule

**Trigger:** Sprint A1 sinh billing schedule ở `on_submit` (khi Contract chuyển Draft → Active). Sinh ở `after_insert` sẽ tạo rows cho Draft contract chưa chắc được submit — lãng phí. Dùng `on_submit`.

Logic pure function `dcnet_contract/utils/billing_schedule.py:generate_schedule()` — không đụng `frappe.db`, nhận input là dict/dataclass, trả list of dict. Lý do tách: golden test (§9) cần test công thức mà không cần bench.

### 6.1 Signature

```python
# dcnet_contract/utils/billing_schedule.py
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from calendar import monthrange

@dataclass
class ScheduleInput:
    contract_type: str              # "Recurring" | "One-off"
    payment_mode: str               # "Prepay" | "Monthly" | "OneOff"
    package_term_months: int | None # None if One-off
    acceptance_date: date
    unit_price_total: Decimal       # per-period amount for Recurring, total for One-off
    setup_fee: Decimal              # 0 if none
    rounding_mode: str              # "Half-up" (default) | "Bankers"

@dataclass
class ScheduleRow:
    month_index: int                # 0 = setup fee, 1..N = service periods
    period_start: date
    period_end: date
    due_date: date
    item_type: str                  # "Setup Fee" | "Service"
    amount: Decimal
    is_prorated: bool
    state: str = "Projected"

def generate_schedule(inp: ScheduleInput) -> list[ScheduleRow]:
    ...
```

### 6.2 Pseudo-implementation

```
rows = []

# Step 1: setup fee row (if any)
if inp.setup_fee > 0:
    rows.append(ScheduleRow(
        month_index=0,
        period_start=inp.acceptance_date,
        period_end=inp.acceptance_date,
        due_date=inp.acceptance_date,
        item_type="Setup Fee",
        amount=inp.setup_fee,
        is_prorated=False,
    ))

# Step 2: service rows
if inp.contract_type == "One-off":
    rows.append(ScheduleRow(
        month_index=1,
        period_start=inp.acceptance_date,
        period_end=inp.acceptance_date,
        due_date=inp.acceptance_date,
        item_type="Service",
        amount=inp.unit_price_total,
        is_prorated=False,
    ))
    return rows

# Recurring
first_period_start = inp.acceptance_date
last_period_end = add_months(first_period_start, inp.package_term_months) - 1 day

if inp.payment_mode == "Prepay":
    # 1 row covers entire term
    rows.append(ScheduleRow(
        month_index=1,
        period_start=first_period_start,
        period_end=last_period_end,
        due_date=first_period_start,   # prepay → due at start
        item_type="Service",
        amount=inp.unit_price_total * inp.package_term_months,  # no proration for prepay block
        is_prorated=False,
    ))
    return rows

# Monthly recurring
for idx in 1..package_term_months:
    p_start, p_end, prorated = compute_period(idx, first_period_start, inp.package_term_months)
    amt = compute_amount(p_start, p_end, inp.unit_price_total, inp.rounding_mode)
    rows.append(ScheduleRow(
        month_index=idx,
        period_start=p_start,
        period_end=p_end,
        due_date=p_end,  # default — A2 may override per payment_terms_template
        item_type="Service",
        amount=amt,
        is_prorated=prorated,
    ))
return rows
```

### 6.3 Proration formula (nguyên văn Mẫu 01)

Footnote Mẫu 01 dòng 45:

> "Tổng cước = Round(Cước hàng tháng / số ngày trong tháng, 0) × số ngày thực tế sử dụng trong tháng"

Công thức pure function:

```python
def compute_amount(period_start: date, period_end: date, monthly_price: Decimal, rounding_mode: str) -> Decimal:
    days_in_month = monthrange(period_start.year, period_start.month)[1]
    actual_days = (period_end - period_start).days + 1
    if actual_days == days_in_month:
        return monthly_price                              # full month — no rounding surprise
    # Partial month — apply Mẫu 01 formula
    daily_rate = (monthly_price / days_in_month).quantize(
        Decimal("1"),                                     # "Round(..., 0)" = round to integer VND
        rounding=ROUND_HALF_UP if rounding_mode == "Half-up" else "ROUND_HALF_EVEN"
    )
    return daily_rate * actual_days
```

**Quan trọng:** Round daily_rate trước, rồi nhân số ngày — KHÔNG round tổng cuối. Đây là cách Excel Mẫu 01 đang làm (ô `Round(X/Y, 0)*Z`). Test §9 sẽ nhốt ngữ nghĩa này.

**Rounding mode** lấy từ `DCNet Contract Settings.default_rounding_mode`. Default `Half-up` (khớp Excel Vietnam — confirm trong §C4 của open-questions).

### 6.4 Period boundaries

```python
def compute_period(idx: int, first_start: date, total_months: int) -> tuple[date, date, bool]:
    """Return (period_start, period_end, is_prorated) for service month idx in [1..total_months]."""
    if idx == 1:
        p_start = first_start
        p_end = last_day_of_month(first_start)
        if p_start.day == 1:
            # Full month
            return p_start, p_end, False
        return p_start, p_end, True   # first month prorated
    # idx 2..total_months-1: full calendar months
    p_start = first_day_of_next_month(first_start, offset=idx-1)
    p_end = last_day_of_month(p_start)
    if idx == total_months:
        # Last month: end at first_start + total_months months - 1 day
        last_end = add_months(first_start, total_months) - timedelta(days=1)
        p_end = last_end
        prorated = (p_end.day != last_day_of_month(p_start).day)
        return p_start, p_end, prorated
    return p_start, p_end, False
```

**Edge case test matrix (§9 golden):**

| Case | acceptance_date | term | first_month amount (cước 10.500) | last_month amount |
|---|---|---|---|---|
| Full month start | 2026-01-01 | 12 | 10.500 | 10.500 |
| Mid-month start | 2026-01-15 | 12 | `round(10500/31)×17 = 339×17 = 5.763` | `round(10500/31)×14 = 339×14 = 4.746` (period 2026-12-15 → 2027-01-14) wait this crosses year |
| End-month start | 2026-01-31 | 12 | `339×1 = 339` | full Jan 2027 trừ 1 ngày |

Test cụ thể sẽ có expected value fixed — dev copy từ Excel thật khi có sample hợp đồng. Trong test fixture ở §9 seed 3 case deterministic.

### 6.3.1 Khi nào khác?

- **Feb 28/29 leap year:** `acceptance_date = 2028-02-29`, `package_term_months = 12`. `_add_months(2028-02-29, 12)` clamps to `2029-02-28`. Last period is 1 day shorter than expected. Test covers this.
- **`package_term_months = 1` with Monthly:** Degenerate case — generates exactly 1 billing row. If `acceptance_date` is mid-month, that single row is prorated. Valid scenario (1-month trial contract).
- **`unit_price_total = 0`:** Free trial or promotional period. Proration of 0 = 0. Billing schedule rows created with amount=0. Valid — auto-invoice will create SI with 0 total (kế toán decides whether to skip).
- **`qty = 0` or negative `unit_price`:** Validate rejects — `unit_price` must be > 0, `qty` must be >= 1. Added to `_validate_items()`.

### 6.5 Controller wiring

```python
# dcnet_contract/doctype/dcnet_contract/dcnet_contract.py
from frappe.model.document import Document
from dcnet_contract.utils.billing_schedule import generate_schedule, ScheduleInput
from dcnet_contract.utils.state_machine import assert_transition

class DCNetContract(Document):
    def validate(self):
        self._validate_contract_type_matches_service()
        self._validate_one_off_vttb_needs_item()
        self._compute_totals()

    def on_submit(self):
        # Draft -> Active
        self.status = "Active"
        self._generate_billing_schedule()

    def on_update_after_submit(self):
        # Allow status transitions Active -> Suspended -> Active -> Expired
        # Block amendments to financial fields after submit (Frappe default)
        pass

    def on_cancel(self):
        # docstatus 1 -> 2
        self.status = "Cancelled"
        # A4 will handle cascade cancel of billing_schedule rows

    def _generate_billing_schedule(self):
        settings = frappe.get_cached_doc("DCNet Contract Settings")
        inp = ScheduleInput(
            contract_type=self.contract_type,
            payment_mode=self.payment_mode,
            package_term_months=self.package_term_months,
            acceptance_date=self.acceptance_date,
            unit_price_total=Decimal(str(self.unit_price_total)),
            setup_fee=Decimal(str(self.setup_fee or 0)),
            rounding_mode=settings.default_rounding_mode,
        )
        rows = generate_schedule(inp)
        self.set("billing_schedule", [])
        for r in rows:
            self.append("billing_schedule", {
                "month_index": r.month_index,
                "period_start": r.period_start,
                "period_end": r.period_end,
                "due_date": r.due_date,
                "item_type": r.item_type,
                "amount": str(r.amount),
                "is_prorated": 1 if r.is_prorated else 0,
                "state": r.state,
            })
        self.db_update_all()
```

**`db_update_all()`** thay vì `save()` để tránh re-entrance (controller đang ở trong `on_submit`).

---

## 7. State machine Contract

Tách ra `utils/state_machine.py` để test được độc lập + reuse cho sprint A4 (revision).

### 7.1 Allowed transitions

```
Draft       --submit-->  Active
Active      --suspend--> Suspended
Suspended   --resume-->  Active
Active      --expire-->  Expired        (scheduler trigger ở A2, A1 chỉ để slot)
Suspended   --expire-->  Expired
Active      --cancel-->  Cancelled      (Frappe on_cancel → docstatus=2)
Suspended   --cancel-->  Cancelled
Draft       --cancel-->  Cancelled      (Frappe delete/discard)
Active      --revise-->  Revised        (A4: amendment submitted, old contract marked Revised)
Cancelled   --revise-->  Revised        (edge case: cancel then amend)
```

**Terminal states:** Expired, Revised. Cancelled can transition to Revised (amend from cancelled).

### 7.1.1 Khi nào khác?

- **Submit with `end_date` in the past:** Allowed — historical contract entry (backdate). Billing schedule generates normally. Expire scheduler will flip to Expired on next daily run.
- **`acceptance_date > contract_date`:** Valid — contract signed before service activated (common for telecom installation delay).
- **Cancel from Suspended:** Allowed (transition exists). Billing schedule future rows → Cancelled same as cancel from Active.

### 7.2 Enforcement

```python
# dcnet_contract/utils/state_machine.py
ALLOWED = {
    ("Draft", "Active"): "submit",
    ("Active", "Suspended"): "suspend",
    ("Suspended", "Active"): "resume",
    ("Active", "Expired"): "expire",
    ("Suspended", "Expired"): "expire",
    ("Active", "Cancelled"): "cancel",
    ("Suspended", "Cancelled"): "cancel",
    ("Draft", "Cancelled"): "cancel",
    ("Active", "Revised"): "revise",
    ("Cancelled", "Revised"): "revise",
}

def assert_transition(current: str, target: str) -> None:
    if (current, target) not in ALLOWED:
        raise frappe.ValidationError(f"Không được chuyển {current} → {target}")
```

Controller gọi `assert_transition` trong:
- `on_submit` (Draft → Active)
- `on_cancel` (any → Cancelled)
- Custom actions `suspend_contract()` / `resume_contract()` / `expire_contract()` exposed qua `@frappe.whitelist()` — implement shell trong A1, logic phần body để A2 fill (hoặc A1 implement luôn suspend/resume, còn expire để A2 scheduler).

### 7.3 Actions v1

Implement trong Sprint A1:
- `submit` (native Frappe)
- `cancel` (native Frappe)
- `suspend_contract(name, reason)` — sets status=Suspended, logs reason in Comment
- `resume_contract(name)` — sets status=Active if prior was Suspended

**Permission enforcement:** Both actions check `frappe.has_permission("DCNet Contract", "write", doc=name)` before executing. Only users who can write the Contract (Sales Manager+) can suspend/resume. Sales Rep (if_owner, Draft only) cannot suspend Active contracts.

Để A2:
- `expire_contract(name)` — scheduler auto-calls khi `end_date < today AND status=Active`

---

## 8. Single DocType `DCNet Contract Settings`

Config-driven (xem open-questions §A.4). Kế toán edit qua UI, không cần dev.

### 8.1 Fields

**Section: General**
- `default_payment_terms` — Link Payment Terms Template, optional. A2 sẽ dùng để tính `due_date`.
- `default_rounding_mode` — Select, options `Half-up\nBankers`, default `Half-up`
- `currency_display_unit` — Select, options `VND\n1000 VND`, default `VND`. Chỉ ảnh hưởng print format (A4), không ảnh hưởng storage.

**Section: Billing schedule**
- `overdue_grace_period_days` — Int, default 15. A2 overdue scheduler đọc.
- `proration_formula` — Select, options `days_in_month\nfixed_30`, default `days_in_month`. `days_in_month` = công thức Mẫu 01 (§6.3). `fixed_30` là giả thiết tương lai.
- `include_setup_fee_in_first_period_row` — Check, default 0. Nếu 1 → không sinh month_index=0 riêng, cộng setup_fee vào row month_index=1. Default 0 (mỗi khoản 1 row — audit dễ hơn).

**Section: Contract lifecycle**
- `expiry_notification_days` — Int, default 30. A2 reminder scheduler.
- `auto_renewal_enabled` — Check, default 0. A5 renewal flow.

**Section: Branch cost center map** (Child Table `DCNet Contract Branch CC Map`)
- `branch` — Link Branch, reqd
- `cost_center` — Link Cost Center, reqd

Dùng bởi A2 khi tạo Sales Invoice (cost_center = map[contract.branch]). A1 chỉ cần field + child table DocType, không cần dùng.

### 8.2 Child DocType `DCNet Contract Branch CC Map`

Simple istable:
- `branch` — Link Branch, in_list_view
- `cost_center` — Link Cost Center, in_list_view

### 8.3 `after_install` seed

```python
# dcnet_contract/install.py
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def after_install():
    _ensure_settings_singleton()
    _seed_settings_defaults()

def after_migrate():
    _ensure_settings_singleton()

def _ensure_settings_singleton():
    if not frappe.db.exists("DCNet Contract Settings", "DCNet Contract Settings"):
        doc = frappe.new_doc("DCNet Contract Settings")
        doc.insert(ignore_permissions=True)

def _seed_settings_defaults():
    settings = frappe.get_doc("DCNet Contract Settings", "DCNet Contract Settings")

    # Only seed if blank (idempotent — don't overwrite manual edits)
    if not settings.default_rounding_mode:
        settings.default_rounding_mode = "Half-up"
    if not settings.overdue_grace_period_days:
        settings.overdue_grace_period_days = 15
    if not settings.expiry_notification_days:
        settings.expiry_notification_days = 30
    if not settings.proration_formula:
        settings.proration_formula = "days_in_month"

    # Try to pick default Payment Terms Template if exists
    if not settings.default_payment_terms:
        pt = frappe.db.get_value("Payment Terms Template", {"disabled": 0}, "name")
        if pt:
            settings.default_payment_terms = pt

    # Seed branch cost center map if ERPNext branches exist + cost centers exist
    if not settings.get("branch_cost_center_map"):
        for branch_name in ["HCM", "HN"]:
            if frappe.db.exists("Branch", branch_name):
                cc = frappe.db.get_value("Cost Center", {"branch": branch_name}, "name")
                if cc:
                    settings.append("branch_cost_center_map", {"branch": branch_name, "cost_center": cc})

    settings.db_update()
    settings.save(ignore_permissions=True)
    frappe.db.commit()
```

**App không áp đặt** COA TT99 phải có — `vn_accounting` đã cài mới chạy `_seed_settings_defaults()` làm nhiệm vụ riêng của nó. Nếu `vn_accounting` chưa cài, seed vẫn chạy nhưng các Link field để trống, kế toán tự điền sau.

Ghi rõ trong README: `dcnet_contract` depends on `vn_accounting` **cho việc seed defaults**, không phải cho việc migrate. `bench --site X install-app dcnet_contract` vẫn chạy được trên bench chưa có `vn_accounting`, chỉ là Settings trống.

---

## 9. Test fixtures & golden tests

### 9.1 Pure function tests (no DB, fast)

`tests/test_billing_schedule.py` — pure `pytest` style, không cần bench context.

```python
# tests/test_billing_schedule.py
from datetime import date
from decimal import Decimal
from dcnet_contract.utils.billing_schedule import generate_schedule, ScheduleInput

def _inp(**over):
    base = dict(
        contract_type="Recurring",
        payment_mode="Monthly",
        package_term_months=12,
        acceptance_date=date(2026, 1, 1),
        unit_price_total=Decimal("10500"),
        setup_fee=Decimal("0"),
        rounding_mode="Half-up",
    )
    base.update(over)
    return ScheduleInput(**base)

class TestBillingSchedule:
    def test_full_month_start_12_rows(self):
        rows = generate_schedule(_inp())
        assert len(rows) == 12
        assert all(r.amount == Decimal("10500") for r in rows)
        assert all(not r.is_prorated for r in rows)

    def test_mid_month_start_proration_first_and_last(self):
        rows = generate_schedule(_inp(acceptance_date=date(2026, 1, 15)))
        # Month 1: 2026-01-15 → 2026-01-31, 17 days in a 31-day month
        # daily = round(10500/31, 0) = 339
        # amount = 339 × 17 = 5763
        assert rows[0].month_index == 1
        assert rows[0].is_prorated is True
        assert rows[0].amount == Decimal("5763")
        # Month 12: 2026-12-15 → 2027-01-14, partial → prorated
        assert rows[11].month_index == 12
        assert rows[11].is_prorated is True

    def test_end_of_month_start_single_day_first_period(self):
        rows = generate_schedule(_inp(acceptance_date=date(2026, 1, 31)))
        # Month 1: just 2026-01-31, 1 day
        # daily = round(10500/31) = 339
        assert rows[0].amount == Decimal("339")
        assert rows[0].is_prorated is True

    def test_setup_fee_row_prepended(self):
        rows = generate_schedule(_inp(setup_fee=Decimal("3000")))
        assert rows[0].month_index == 0
        assert rows[0].item_type == "Setup Fee"
        assert rows[0].amount == Decimal("3000")
        assert rows[1].month_index == 1

    def test_prepay_single_row_full_term(self):
        rows = generate_schedule(_inp(payment_mode="Prepay", setup_fee=Decimal("0")))
        assert len(rows) == 1
        assert rows[0].amount == Decimal("10500") * 12  # full term
        assert not rows[0].is_prorated

    def test_one_off_single_row(self):
        rows = generate_schedule(_inp(
            contract_type="One-off",
            payment_mode="OneOff",
            package_term_months=None,
            unit_price_total=Decimal("13500"),
        ))
        assert len(rows) == 1
        assert rows[0].item_type == "Service"
        assert rows[0].amount == Decimal("13500")
```

### 9.2 Frappe integration tests (uses DB)

`dcnet_contract/doctype/dcnet_contract/test_dcnet_contract.py`:

```python
import frappe
from frappe.tests.utils import FrappeTestCase

class TestDCNetContract(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = _ensure_customer("_Test DCNet Customer")
        cls.sales_person = _ensure_employee("_Test Sales Rep HCM")
        _ensure_branch("HCM")

    def test_draft_to_active_generates_schedule(self):
        doc = frappe.get_doc({
            "doctype": "DCNet Contract",
            "customer": self.customer,
            "sales_person": self.sales_person,
            "branch": "HCM",
            "contract_type": "Recurring",
            "service_type": "P2P",
            "project_category": "Viễn thông",
            "payment_mode": "Monthly",
            "package_term_months": 12,
            "contract_date": "2026-01-01",
            "acceptance_date": "2026-01-01",
            "items": [
                {"item_label": "P2P HCM-HN 100M", "qty": 1, "unit_price": 10500},
            ],
        }).insert()
        self.assertEqual(doc.status, "Draft")
        self.assertEqual(doc.unit_price_total, 10500)
        self.assertEqual(len(doc.billing_schedule), 0)  # not yet submitted

        doc.submit()
        doc.reload()
        self.assertEqual(doc.status, "Active")
        self.assertEqual(len(doc.billing_schedule), 12)
        self.assertTrue(all(r.state == "Projected" for r in doc.billing_schedule))

    def test_cancel_from_active(self):
        doc = _make_active_contract(self.customer, self.sales_person)
        doc.cancel()
        doc.reload()
        self.assertEqual(doc.status, "Cancelled")
        self.assertEqual(doc.docstatus, 2)

    def test_vttb_without_item_link_fails(self):
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "DCNet Contract",
                "customer": self.customer,
                "sales_person": self.sales_person,
                "branch": "HCM",
                "contract_type": "One-off",
                "service_type": "VTTB",
                "project_category": "VTTB",
                "payment_mode": "OneOff",
                "contract_date": "2026-01-01",
                "acceptance_date": "2026-01-01",
                "items": [
                    {"item_label": "Router Cisco", "qty": 1, "unit_price": 50000},
                    # Missing erpnext_item — should fail validate
                ],
            }).insert()

    def test_settings_singleton_seeded(self):
        s = frappe.get_doc("DCNet Contract Settings")
        self.assertEqual(s.default_rounding_mode, "Half-up")
        self.assertEqual(s.overdue_grace_period_days, 15)
```

### 9.3 Test data helpers

`tests/helpers.py` — reusable `_ensure_customer`, `_ensure_employee`, `_ensure_branch`, `_make_active_contract`. Kept tiny — use `frappe.db.exists` + `insert` idempotent.

### 9.4 Run command

```bash
bench --site dcnet.localhost run-tests --app dcnet_contract
```

Expected: all green. 6 test cases in integration + 6 pure unit tests = 12 total. Runtime < 30s.

---

## 10. Permission matrix

Sprint A1 chỉ cần 4 role. Phức tạp hơn (PAKD approval matrix HCM/HN × Nhân viên/BGĐ) để sprint B.

| Role | Read | Write | Create | Submit | Cancel | Amend | Set User Permission |
|---|---|---|---|---|---|---|---|
| **DCNet Sales Rep** | ✅ (own) | ✅ (Draft only) | ✅ | ❌ | ❌ | ❌ | ❌ |
| **DCNet Sales Manager** | ✅ (branch) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Accounts Manager** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **System Manager** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**"own" / "branch" filter:**
- Sales Rep: `if_owner = 1` — chỉ thấy doc mình là `owner` (= người tạo). Có thể edit chỉ khi `docstatus=0` (Draft).
- Sales Manager: User Permission `Branch` — seed bởi admin khi add user.

**Settings DocType permission:** chỉ `Accounts Manager` + `System Manager` write. Sales không đụng.

JSON excerpt:

```json
"permissions": [
  {"role": "DCNet Sales Rep", "read": 1, "write": 1, "create": 1, "if_owner": 1},
  {"role": "DCNet Sales Manager", "read": 1, "write": 1, "create": 1, "submit": 1},
  {"role": "Accounts Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1},
  {"role": "System Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1}
]
```

Role `DCNet Sales Rep` và `DCNet Sales Manager` là custom — seed trong `after_install` nếu chưa tồn tại.

---

## 11. Hooks wiring

```python
# dcnet_contract/hooks.py
app_name = "dcnet_contract"
app_title = "DCNet Contract"
app_publisher = "DCNet"
app_description = "Hợp đồng DCNet — primitive cho recurring + one-off, billing schedule, cash flow ownership"
app_email = "dev@dcnet.vn"
app_license = "MIT"
app_version = "0.1.0"

required_apps = ["frappe", "erpnext"]

after_install = "dcnet_contract.install.after_install"
after_migrate = "dcnet_contract.install.after_migrate"

# A2 will add:
# scheduler_events = {"daily": ["dcnet_contract.tasks.run_billing_cycle", ...]}

# A3 will add:
# doc_events = {"DCNet Contract": {"on_update": "...shadow_so_sync"}}

fixtures = []  # empty in A1
```

**Không cần `doc_events`** ở A1. Controller hooks (validate/on_submit/on_cancel) đủ.

---

## 12. Migration + verification checklist

End of Sprint A1, dev phải verify:

- [ ] `bench get-app https://github.com/dcnet-cloud/dcnet-contract` succeed
- [ ] `bench --site dcnet.localhost install-app dcnet_contract` succeed
- [ ] `bench --site dcnet.localhost migrate` xanh, 4 DocTypes + 2 child tables created
- [ ] `bench --site dcnet.localhost execute "frappe.get_installed_apps()"` chứa `dcnet_contract`
- [ ] DCNet Contract Settings singleton tồn tại với `default_rounding_mode = Half-up`
- [ ] Tạo 1 DCNet Contract qua UI: header → items → save → submit → billing_schedule hiện ra 12 rows
- [ ] Cancel contract → status = Cancelled, docstatus = 2
- [ ] `bench --site dcnet.localhost run-tests --app dcnet_contract` all green
- [ ] Custom roles `DCNet Sales Rep` + `DCNet Sales Manager` tồn tại trong `tabRole`
- [ ] Commit + push lên `dcnet-cloud/dcnet-contract`, CI xanh
- [ ] Tag `v0.1.0-a1`

Gate chuyển Sprint A2: **tất cả ✅ + Long manual QA 1 contract recurring + 1 contract one-off**.

### 12.1 Rollback nếu cài thất bại

1. `bench --site dcnet.localhost uninstall-app dcnet_contract --yes` — removes all DocTypes + data
2. `pip uninstall dcnet_contract` — removes Python package
3. Remove `dcnet_contract` from `sites/apps.txt`
4. `bench --site dcnet.localhost migrate` — clean up orphan references

---

## 13. Ngoài scope A1 (reference)

Để dev khỏi nhầm, liệt kê rõ những gì **KHÔNG làm** trong A1, chuyển sprint sau.

| Feature | Sprint | Ghi chú |
|---|---|---|
| Auto-invoice scheduler (Projected → Invoiced → Sales Invoice) | A2 | Daily scheduler đọc billing_schedule, tạo SI khi đến due_date |
| Payment Entry hook (Invoiced → Paid) | A2 | `doc_events` on PE submit, map SI → billing_schedule row |
| Overdue scheduler (Invoiced → Overdue sau grace period) | A2 | Daily scheduler dùng `overdue_grace_period_days` |
| `expire_contract` scheduler | A2 | Daily check `end_date < today AND status=Active` |
| Shadow Sales Order sync (one-off VTTB flow) | A3 | `doc_events` on Contract submit → tạo hidden SO linked, cascade delete |
| SO permission lockdown (non-admin không thấy shadow SO) | A3 | `permission_query_conditions` hook |
| Contract Revision chain (upgrade/downgrade, amended_from) | A4 | Build trên Frappe amend pattern |
| Cancel mid-term + credit note alert | A4 | Cancel future rows → Cancelled, show toast "Credit note needed" |
| Print format "Hợp đồng chuẩn" | A4 | Jinja template từ `DCNet Contract Template` |
| Contract Template DocType | A4 | Pre-filled templates per service_type |
| Workspace `DCNet Contract` sidebar | A5 | Link cards, shortcut tạo contract nhanh |
| Script Report: outstanding receivables theo contract | A5 | Query Paid/Invoiced/Overdue schedule |
| KPI dashboard sales rep | A5 | Frappe Dashboard Chart |
| Commission calc | sprint B | Toàn bộ — PAKD app |
| Chi phí ngoài (MS/AC/GPVT) | sprint B | — |

---

## 14. Decisions locked (không re-decide trong A1)

1. **Option D shadow SO** — chỉ design, implement A3. A1 chỉ cần field `erpnext_item` trên Contract Item sẵn sàng link.
2. **1 NVKD/Contract** — field `sales_person` là Link đơn, không child table.
3. **Cash-basis commission** — Contract không quan tâm commission. Chỉ cần fire event khi PE (A2) update billing_schedule. Event name: `dcnet_contract.billing_period_paid` (register ở A2).
4. **Settings DocType pattern** — `DCNet Contract Settings` Single, seed defaults ở `after_install`, kế toán edit qua UI.
5. **`service_type` enum 8 giá trị** — P2P, MPLS, ILL, FTTH DN, FTTH HGD, IT Managed, VTTB, Thi công. FTTH HGD = khách cá nhân (hộ gia đình), không có MST, cần CMND/CCCD.
6. **Branch enum** — HCM, HN. Link Branch (seed ERPNext Branch master trong test fixture nếu chưa có).
7. **Currency** — VND only (field `currency` readonly default VND trong v1).
8. **Proration formula** — nguyên văn Mẫu 01: `Round(monthly/days_in_month, 0) × actual_days`. Round daily trước, nhân ngày sau. Half-up rounding mode default.
9. **Submittable DocType** — dùng `docstatus` cho Draft/Submitted/Cancelled; `status` field phụ cho Active/Suspended/Expired sub-state trong docstatus=1.
10. **Split repo** — `dcnet-cloud/dcnet-contract` độc lập. `pyproject.toml` declare depends frappe + erpnext. `vn_accounting` soft-dependency (seed defaults khi có, bỏ qua khi không).
11. **Setup fee không phát sinh commission/chi phí ngoài** — riêng một row `month_index=0`, item_type=Setup Fee. PAKD sprint B sẽ skip rows có `item_type=Setup Fee` khi tính commission.
12. **Payment mode enum** — Prepay | Monthly | OneOff. Prepay sinh 1 row duy nhất gộp toàn bộ term. Monthly sinh N rows. OneOff sinh 1 row.
13. **Revenue recognition** — Ghi nhận doanh thu ngay khi xuất SI (CR 5113), kể cả prepay 12 tháng. Không defer sang TK 3387. Nghĩa vụ dịch vụ tiếp diễn ghi chú trong thuyết minh BCTC. Billing schedule amounts là VAT-exclusive; VAT tính khi tạo SI qua Item Tax Template.
14. **FTTH HGD customer** — Khách cá nhân không có MST. Customer form: `tax_id` optional khi `service_type=FTTH HGD`. Cần fields bổ sung: `customer_id_number` (CMND/CCCD), `customer_id_date`, `customer_id_place`, `customer_dob`. Đã seed custom fields trong `install.py:_ensure_customer_cmnd_fields()`.
15. **"Tạo PAKD" button** — Contract form (khi status=Active) hiển thị button "Tạo PAKD" → navigate sang PAKD form pre-filled với `contract_ref`. UX cho NVKD tạo PAKD liền mạch sau khi submit contract.
16. **Billing schedule per customer per SI** — Mỗi billing period tạo 1 SI riêng cho 1 khách hàng. Không gộp nhiều KH vào 1 SI. Bắt buộc để vn_banking auto-match per SI.

---

## 15. Open items cần confirm với kế toán DCNet (non-blocking A1)

Không block A1 — dev có thể viết code với default, kế toán override qua Settings UI khi trả lời.

1. **C1 Grace period Overdue** — default 15 ngày. Kế toán xác nhận?
2. **C4 Rounding mode** — Half-up default (khớp Excel). Confirm?
3. **C7 Contract workflow** — default chỉ cần Sales Manager submit, không có approval chain riêng cho Contract. Confirm? (PAKD có chain riêng ở sprint B.)
4. **Branch master data** — ERPNext Branch có sẵn "HCM" + "HN" chưa? Nếu chưa, `after_install` có nên seed không? (Hiện spec chỉ assume tồn tại.)
5. **Cost Center mapping HCM/HN → CC name** — dev cần biết tên CC thật để seed `branch_cost_center_map` default. Nếu chưa có → seed empty, kế toán tự fill.
6. **Sample hợp đồng thật** — 2 contract recurring (P2P + FTTH DN) + 1 one-off (VTTB hoặc Thi công) để chạy manual QA §12. Anonymized. Cần trước khi gate sprint A1.

Các câu trên được track trong `dcnet_contract-open-questions-lite.md`. Không viết lại ở đây để tránh drift.

---

## 16. Ước lượng effort

| Item | Effort |
|---|---|
| App scaffold + install + Settings singleton | 0.5 day |
| 4 DocType JSON + controllers | 1 day |
| `billing_schedule.py` pure function + proration | 0.5 day |
| Pure unit tests (6 cases) | 0.5 day |
| Frappe integration tests (6 cases) | 0.5 day |
| State machine + transition enforcement | 0.25 day |
| Permission matrix + seed custom roles | 0.25 day |
| `after_install` seed + ensure idempotent | 0.25 day |
| Manual QA 2 contracts (recurring + one-off) | 0.25 day |
| CI setup + first push + tag | 0.5 day |
| **Total** | **~4.5 days** |

Buffer 1 day cho bug fix → **Sprint A1 = 1 tuần 1 người**.

Sprint A2 (scheduler + PE hook + overdue) ước lượng tương đương ~1 tuần. Sprint A3 (shadow SO) rủi ro cao hơn, ~1.5 tuần.

---

## 17. References

- `docs/specs/architecture-contract-and-pakd.md` — vì sao tách app, Option D, sprint order
- `docs/specs/dcnet_contract-open-questions-lite.md` — §A.3 commission rule template schema (dùng ở sprint B), §A.4 Settings DocType pattern
- `docs/accounting-requirements/converted/mau-01-PAKD.md` — field header + proration formula gốc
- `docs/accounting-requirements/converted/mau-03-PAKD.md` — field header one-off
- `docs/specs/dcnet_pakd.md` §4-§6, §11 — PAKD schema cũ (reference only, §7 cutoff OUTDATED — sẽ rewrite ở spec PAKD v3)
- Memory: `project_dcnet_contract.md`, `project_dcnet_pakd.md`, `feedback_dcnet_no_personal_remote.md`
- Rules: `~/.claude/rules/frappe.md` (required files, custom app scaffold, db.set_value caveat)
