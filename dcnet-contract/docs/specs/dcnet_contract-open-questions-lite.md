# dcnet_contract + dcnet_pakd — Câu hỏi còn lại (rút gọn, v2)

> **Bản rút gọn v2** sau round đầu tiên với Long (2026-04-10).
> Chỉ còn những gì thực sự chưa biết hoặc chưa confirm với kế toán DCNET.
>
> **Status các decisions đã chốt (Long — 2026-04-10):**
> - ✅ **B1 — Chu kỳ PAKD:** Option A — 1 PAKD / 1 hợp đồng, submit 1 lần
> - ✅ **B2 — Commission rates:** preset 4 tầng (default → service → branch → PAKD manual override)
> - ✅ **B3 — Tài khoản chi phí ngoài:** mặc định trong `PAKD Settings`, kế toán edit được qua UI
> - ❌ **B4 — FTTH cá nhân:** câu hỏi bị loại (DCNET không kinh doanh FTTH hộ gia đình, xem §A.1 dưới)
> - ✅ **B5 — Cash-basis + Add Costs:** commission chỉ post khi khách trả. Add Costs = một loại chi phí ngoài (cùng nhóm MS + GPVT), không phải cơ chế đặc biệt. Cả 3 chi phí ngoài dùng chung schema (rate × base_formula).

## A. Discovery mới (2026-04-10)

### A.1 DCNET chỉ kinh doanh B2B — không có FTTH cá nhân

Re-read kỹ Mẫu 01 ("PAKD này áp dụng cho các dịch vụ viễn thông P2P/MPLS/ILL/**FTTH DN** và các dịch vụ CNTT cho **doanh nghiệp**") và title Mẫu 02 ("PHƯƠNG ÁN KINH DOANH DỊCH VỤ **FTTH DOANH NGHIỆP**"). Không có mention FTTH hộ gia đình ở bất kỳ tài liệu nào.

**Implication:**
- `service_type` enum bỏ "FTTH HGD", giữ: **P2P, MPLS, ILL, FTTH DN, IT Managed, VTTB, Thi công** (7 giá trị)
- Không cần data model đặc biệt cho scale hàng chục ngàn subscribers — tất cả Contract là B2B, số lượng hàng trăm (không phải hàng chục nghìn)
- Mẫu 02 = "N FTTH DN nhỏ/vừa batch trong 1 tháng" (không phải batch subscriber cá nhân). NVKD ký từng dòng cho từng DN nhỏ.
- Đã sửa trong `architecture-contract-and-pakd.md` §1 table.

### A.2 Quyết định B1 có implication kỹ thuật rõ ràng

Option A (1 PAKD/Contract) + cash-basis (B5) nghĩa là:

**State machine commission line (chính thức):**
```
Draft     (PAKD chưa approved)
Pending   (PAKD approved, billing_schedule row chưa Paid)
Posted    (billing_schedule row flip Paid → lương được ghi nhận ngay)
Cancelled (contract cancel / revision supersede)
```

**Payroll_month tính theo payment_date (NOT submission_date):**
```python
payment_date = payment_entry.reference_date
if payment_date.day <= 5:
    payroll_month = payment_date - 1 month  # cutoff: payment đầu tháng → lương tháng trước
else:
    payroll_month = payment_date             # payment sau ngày 5 → lương tháng hiện tại
```

**Spec v2 `dcnet_pakd.md` §7 outdated** — v2 tính cutoff theo submission_date (PAKD approval time). Cần rewrite theo cash-basis + payment_date khi viết spec v3.

**Architecture doc §9 bước 5** đã đúng hướng (state machine 3 trạng thái), nhưng cần đổi Eligible/Posted logic: không cần state Eligible trung gian nữa vì PAKD approved 1 lần là xong — mỗi payment trigger commission post trực tiếp Pending → Posted.

**Prepay trường hợp đặc biệt:** 1 Payment Entry thanh toán trước 12 tháng → 12 billing_schedule rows flip Paid cùng lúc → 12 commission lines Posted cùng lúc → **gom thành 1 Additional Salary duy nhất** cho payroll_month của payment_date (không spread 12 tháng).

→ Tôi sẽ update cả architecture doc §9 để fix state machine mới.

### A.3 Commission Rule Template — schema flexible cho B2

Theo yêu cầu Long "mọi thứ phải linh hoạt", schema PAKD Commission Rule Template:

```
PAKD Commission Rule Template (Standalone DocType)
├── template_name (Data)
├── valid_from (Date)
├── valid_to (Date, optional)
├── scope_branch (Link Branch, optional — blank = tất cả branch)
├── scope_service_type (Select, optional — blank = tất cả service)
├── scope_pakd_type (Select: Recurring Telecom / FTTH Rollup / One-off)
├── components (Child Table)
│   ├── component_name (Select: Manager Services / Add Costs / Phí GPVT / Lương KD)
│   ├── rate (Percent)
│   ├── base_formula (Select: unit_price / unit_price - add_costs / add_costs_gross)
│   └── applies_to_setup_fee (Check, default 0)
```

**Resolution order (most specific wins):**
```
1. Contract.commission_override (child table trên Contract, nếu có) — highest priority
2. Template match by (scope_branch + scope_service_type + scope_pakd_type)
3. Template match by (scope_service_type + scope_pakd_type)
4. Template match by (scope_pakd_type)  — default per PAKD type
```

**Override per Contract:** Contract có field `commission_override` (Child Table PAKD Commission Override) cho phép NVKD/Sales Manager override cho hợp đồng đặc biệt. Khi có override → PAKD đọc từ Contract, không đọc template. Audit trail giữ lại: hợp đồng này dùng rate gì, ai approve override, ngày nào.

**Ví dụ flexibility trong thực tế:**
- Default: tất cả recurring dùng 10% MS / 75% AC / 2.2% GPVT / 6% Lương KD
- HN branch template: 10% MS / 75% AC / 2.2% GPVT / **8% Lương KD** (chi nhánh HN có rate lương cao hơn)
- P2P service template: **12% MS** / ... (service P2P hoa hồng khách cao hơn)
- 1 hợp đồng đặc biệt với KH lớn: override riêng 15% Lương KD với approval BGĐ

→ Cơ chế: base template → branch override → service override → contract override. 4 tầng nhưng hầu hết hợp đồng chỉ dùng tầng 1 (base template).

## A.4 Settings DocTypes — config-driven, kế toán edit qua UI

Nguyên tắc chung (từ feedback Long cho B3): **không hard-code account hay config value trong code**. Mọi thứ kế toán có thể cần thay đổi đều sống trong Settings DocType, edit qua UI bình thường, không cần dev động vào code.

Chia thành 2 Settings (theo ranh giới app):

### `DCNET Contract Settings` (Single DocType, trong dcnet_contract)

```
General:
  - default_payment_terms     (Link Payment Terms Template)
  - default_rounding_mode     (Select: Half-up | Banker's) — default Half-up
  - currency_display_unit     (Select: VND | 1000 VND)      — default VND

Billing schedule:
  - overdue_grace_period_days (Int)  — default 15
  - proration_formula         (Select: "days_in_month" | "fixed_30") — default days_in_month

Contract lifecycle:
  - expiry_notification_days  (Int)  — default 30 (email trước khi Expired)
  - auto_renewal_enabled      (Check) — default 0

Default cost centers (per branch mapping):
  - branch_cost_center_map    (Child table: branch → cost_center)
```

### `PAKD Settings` (Single DocType, trong dcnet_pakd)

```
Cutoff:
  - cutoff_day_of_month       (Int)  — default 5
  
Commission defaults (B2 proposal):
  - default_commission_template (Link PAKD Commission Rule Template)

Account mapping cho chi phí ngoài (B3 proposal):
  - account_manager_services  (Link Account)  — mặc định, kế toán có thể đổi
  - account_add_costs         (Link Account)  — mặc định, kế toán có thể đổi
  - account_gpvt              (Link Account)  — mặc định, kế toán có thể đổi
  - account_bad_debt          (Link Account)  — mặc định, kế toán có thể đổi
  - counter_account_add_costs (Link Account)  — TK đối ứng khi trả Add Costs (3388 / 131 / 111 tùy cơ chế)
  - counter_account_manager_services (Link Account)

Additional Salary mapping:
  - salary_component_luong_kd (Link Salary Component) — mặc định "Lương kinh doanh"
```

**Install hook seed defaults:**

Khi cài `dcnet_pakd`, hook `after_install` sẽ seed giá trị mặc định cho `PAKD Settings` dựa trên VN COA TT99 đã cài từ `vn_accounting`:

```python
# dcnet_pakd/install.py
DEFAULT_ACCOUNTS = {
    "account_manager_services": "6418 - Chi phí bằng tiền khác",
    "account_add_costs":         "6418 - Chi phí bằng tiền khác",
    "account_gpvt":              "6425 - Thuế, phí và lệ phí",
    "account_bad_debt":          "811 - Chi phí khác",  # hoặc 642x tùy kế toán
    "counter_account_add_costs": "3388 - Phải trả, phải nộp khác",
    "counter_account_manager_services": "3388 - Phải trả, phải nộp khác",
}
```

Sau khi cài, kế toán DCNET mở **PAKD Settings** form, verify các account đã đúng và override nếu muốn. Không cần dev intervention.

**Về phân loại "được trừ thuế TNDN" hay không:** Đây là policy của kế toán, không phải thuộc tính account trong COA. Cách xử lý tối giản cho v1:
- `PAKD Settings` chỉ điền **account code mặc định**, không quan tâm deductible/non-deductible.
- Nếu kế toán DCNET sau này muốn track rõ, họ có thể:
  - Option 1: tạo thêm sub-account `6418.1` / `6418.2` trong VN COA (qua UI), rồi edit `PAKD Settings` trỏ tới account mới.
  - Option 2: dùng Cost Center đặc biệt để mark non-deductible.
  - Không cần code change cho cả hai option.

→ App **không áp đặt chính sách thuế**. App chỉ cung cấp mapping configurable. Kế toán tự quyết.

## B. Câu hỏi BLOCKING còn lại (0 câu — tất cả đã close)

### ~~B3. Tài khoản chi phí không được trừ thuế TNDN~~

**✅ CLOSED 2026-04-10.** Đã giải quyết bằng Settings DocType pattern — xem §A.4. Kế toán DCNET mở `PAKD Settings` sau khi cài app, verify các account mặc định và edit nếu cần.

---

### ~~B5. Add Costs semantics~~

**✅ CLOSED 2026-04-10** (simplified sau feedback Long).

**Hiểu đúng:** Add Costs là **một loại chi phí ngoài** — cùng nhóm với Manager Services và Phí GPVT. Không phải cơ chế kickback đặc biệt. 4 dòng trong "Mục III. Chi phí" của Mẫu 01 tất cả đều là các khoản chi DCNET thực chi ra, chỉ khác nhau về **mục đích chi** và **công thức tính**:

| Khoản chi | Bản chất | Công thức (ví dụ Mẫu 01) |
|---|---|---|
| **Manager Services** | Hoa hồng cho người phụ trách bên khách | rate × (đơn_giá - add_costs) |
| **Add Costs** | Chi phí phụ trội khách yêu cầu nâng cấp/thêm | rate × add_costs_gross |
| **Phí GPVT + CIVT** | Phí quyền viễn thông bắt buộc theo quy định | rate × đơn_giá |
| **Lương kinh doanh** | Commission NVKD (đây là payout cho nhân viên, không phải chi phí ngoài) | rate × (đơn_giá - add_costs) |

**Implication cho schema:** Cả 3 chi phí ngoài (MS, AC, GPVT) dùng **cùng một model** — mỗi khoản có:
- `rate` (Percent) — tỷ lệ
- `base_formula` (Select) — công thức tính base amount: `unit_price` / `unit_price - add_costs` / `add_costs_gross`
- `account` — lấy từ `PAKD Settings` (có thể override per rule template)
- `counter_account` — lấy từ `PAKD Settings` (tài khoản đối ứng khi post JE)

Không cần đặc biệt hóa Add Costs. Schema §A.3 đã cover đủ.

**Rate 0.75 trong ví dụ Mẫu 01 chỉ là rate cho hợp đồng cụ thể đó** — không phải quy luật. Hợp đồng khác có thể là 0.5, 0.8, hoặc khác. Rate này sẽ sống trong `PAKD Commission Rule Template` (cho preset) hoặc `Contract.commission_override` (cho override per hợp đồng) — chính xác như đã thiết kế ở §A.3.

**Các chi tiết nghiệp vụ còn lại** (cơ chế trả thực tế, tài khoản đối ứng chính xác, tần suất trả) → **xin sample hợp đồng + PAKD thật** (xem §E) sẽ trả lời cụ thể hơn bất kỳ câu hỏi lý thuyết nào. Không block Sprint A1.

---

### B2 (follow-up, non-blocking). Seed data cho commission template

Long đã chốt schema (xem §A.3). Không block Sprint A1 — có thể seed 1 default template theo Mẫu 01 (10% MS / 75% AC / 2.2% GPVT / 6% Lương KD) và kế toán tự tạo thêm template khác qua UI khi cần.

**Câu hỏi tùy chọn gửi DCNET (để seed đầy đủ ngay từ đầu, không bắt buộc):**

Hiện tại DCNET có sẵn bảng rate commission theo service_type / branch khác với default không?

```
Matrix mẫu:
                   P2P   MPLS   ILL   FTTH DN   IT Managed   VTTB   Thi công
Manager Services   ?     ?      ?     ?         ?            ?      ?
Add Costs          ?     ?      ?     ?         ?            ?      ?
Phí GPVT           ?     ?      ?     —(không)  —            —      —
Lương KD           ?     ?      ?     ?         ?            ?      ?
```

Nếu chưa có matrix rõ → Long seed 1 default template theo Mẫu 01. Nếu đã có → gửi để seed full templates ngay.

- [ ] Trả lời (optional): ___

## C. Xác nhận defaults (8 mục — giảm 1 vì B4 bỏ)

| # | Mục | Default | ✅ OK / Override |
|---|---|---|---|
| C1 | **Grace period Overdue** | 15 ngày sau due_date | ___ |
| C2 | **Bad debt write-off** | Manual button, role Accounts Manager | ___ |
| C3 | **Credit Note khi cancel/revision** | Manual, system alert | ___ |
| C4 | **Rounding mode proration** | Half-up (khớp Excel) | ___ |
| C5 | **Suspended trigger** | Manual, không auto theo số ngày nợ | ___ |
| C6 | **Revision proration** | Áp giá mới từ kỳ billing kế tiếp | ___ |
| C7 | **Contract workflow** | Draft → Active chỉ cần Sales Manager submit, không approval chain riêng | ___ |
| C8 | **Contract Template count** | 1 base + 1 per service_type (tổng 8) | ___ |
| C9 | **Auto-renewal hết hạn** | Không auto-renew, chỉ email cảnh báo 30 ngày trước | ___ |

## D. Workflow approver — danh sách tên + email (giữ nguyên)

Spec v2 `dcnet_pakd.md` §6 đã fix 6 role. Cần DCNET điền tên thật để seed User + User Permission:

| Role | Tên từ Excel | Email + backup |
|---|---|---|
| `PAKD Sales Rep` (NVKD) | (mỗi sales rep 1 user) | ___ |
| `PAKD Sales Director HCM` | Lê Thị Hồng | ___ |
| `PAKD Sales Director HN` | Nguyễn Tuấn Anh | ___ |
| `PAKD General Department` (P. Tổng hợp) | Nguyễn Thị Mỹ Hiền | ___ |
| `PAKD Branch Director HN` | Lê Văn Phong | ___ |
| `PAKD Board` (BGĐ) | Dương Đại Sơn, Đỗ Trung Hiếu | ___ |
| `PAKD Accountant` | ? | ___ |

+ 2 câu phụ: 1 người giữ nhiều role được không? Backup khi vắng?

## E. Yêu cầu sample (giữ nguyên)

4 bộ hợp đồng + PAKD kèm (anonymized):

1. **1 P2P hoặc MPLS** + Mẫu 01
2. **1 FTTH DN** + Mẫu 01 hoặc Mẫu 02
3. **1 VTTB hoặc thi công** + Mẫu 03
4. **1 hợp đồng đã revision** + 2 PAKD trước/sau

Anonymize: tên KH → "Công ty ABC", MST → fake, địa chỉ → quận/thành phố. Giá giữ nguyên.

## Tóm tắt status

| Trạng thái | Số mục | Chi tiết |
|---|---|---|
| ✅ Đã chốt | 5/5 câu gốc | B1 Option A, B2 flexible schema (§A.3), B3 Settings DocType (§A.4), B4 loại bỏ, B5 Add Costs = chi phí ngoài thông thường |
| ⏳ Non-blocking, nice-to-have | 1 | B2-followup (matrix rate — nếu DCNET có sẵn thì seed đầy đủ, không có thì dùng default) |
| ⏳ Defaults cần tick | 9 | C1-C9 |
| ⏳ Tên approver | 6 role | + 2 câu phụ về delegation |
| ⏳ Sample hợp đồng | 4 bộ | Anonymize, xem §E |

**Không còn câu nào blocking.** Tất cả 5 câu gốc B1-B5 đã được giải quyết hoặc pattern-hoá thành design decision:

- **Spec Sprint A1 + A2** có thể viết và code ngay — tất cả config sống trong Settings DocType với default seed tự động.
- **Sprint B3** (commission posting + JE) không cần đợi kế toán. Hook `after_install` seed default account dựa trên VN COA TT99 hiện có. Kế toán verify/override sau khi deploy qua UI của Settings.
- **Sprint B2** (workflow) cần 6 tên approver để seed User — hỏi song song với coding.
- **Sprint A4** (print format) + **Sprint B1** (golden test rule engine) cần sample hợp đồng thật để đối chiếu layout và số liệu.

**Hành động tiếp theo:**

1. Long gửi 1 email/Zalo gọn cho kế toán DCNET xin:
   - 4 bộ sample hợp đồng + PAKD đã approved (§E)
   - Danh sách 6 approver kèm email (§D)
   - Verify 9 defaults C1-C9 (§C)
   - Optional: matrix commission rate nếu có sẵn (§B2-followup)
2. Song song, Long bắt đầu viết spec chi tiết Sprint A1 (Contract DocType + Billing Schedule + state machine + 2 Settings DocType). Không chờ.
3. Khi DCNET trả lời → seed data vào Settings production thay cho default.
