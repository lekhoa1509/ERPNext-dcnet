# Phân tích xung đột giữa kế toán real-time ERPNext và workflow kết chuyển TT99/2025

**Vai trò:** KTT + Architect
**Ngày:** 2026-05-11
**Tổng quan:** Hệ thống kế toán ERPNext **post bút toán real-time** ngay khi document submit. Mọi workflow "kết chuyển cuối kỳ" theo truyền thống VN (TT99/2025, TT200/2014, VAS chung) ở agent vừa viết đều có nguy cơ **double-count / duplicate / không idempotent**. Phải cân nhắc lại trước khi đưa vào production.

---

## 1. Nguyên lý real-time của ERPNext (recap)

| Document submit | GL Entry tự sinh ngay |
|---|---|
| Sales Invoice | Dr 131 / Cr 511 + Cr 3331 |
| Purchase Invoice | Dr 152/156 + Dr 1331 / Cr 331 |
| Stock Entry (Material Issue cho WO) | Dr 621 / Cr 152 |
| Stock Entry (Manufacture) | Dr 155 / Cr 154 (nếu setup đầy đủ) hoặc Dr 155 / Cr 621 trực tiếp |
| Delivery Note / Sales Invoice | Dr 632 / Cr 155 |
| Payment Entry | Dr 111/112 / Cr 131 |
| Landed Cost Voucher submit | Re-post stock GL của Purchase Receipt với valuation_rate mới |
| Period Closing Voucher submit | **Auto** tạo bút toán Dr 5xx-6xx / Cr 421 — kết chuyển toàn bộ P&L → retained earnings (yearly) |

**Hệ quả quan trọng:** `tabGL Entry` luôn có **toàn bộ** giao dịch chi tiết. Báo cáo P&L / Balance Sheet đọc trực tiếp từ GL Entry theo date range — KHÔNG cần "kết chuyển" hàng tháng để hiển thị đúng.

---

## 2. Audit 3 wizard agent vừa viết

### 2.1 `period-closing-911` Wizard — Kết chuyển 5xx/6xx → 911 → 421

**File:** `vn_accounting/period_closing/wizard_api.py` (193 dòng)

**Logic hiện tại:**
```python
JE1: Dr each 5xx / Cr 911                  (zero out revenue)
JE2: Dr 911 / Cr each 6xx                  (zero out expense)
JE3: Dr 911 / Cr 421 (lãi) OR ngược lại    (chuyển kết quả về RE)
```

`period_start = get_first_day(period_end)` → wizard chạy cho 1 tháng chứa `period_end`. Tất cả JE ở draft (KTT phải submit thủ công).

**🔴 Vấn đề 1 — Cancel hóa đơn sau khi kết chuyển sẽ tạo balance âm**

Sequence:
1. 15/1: Sales Invoice 100M submit → 511 balance = +100M (Cr)
2. 31/1: Chạy wizard → JE1 Dr 511 100M / Cr 911 100M → 511 balance = 0
3. 31/1: JE3 Dr 911 100M / Cr 421 100M → 421 balance = +100M, 911 balance = 0
4. **5/2: KTT phát hiện SI sai → cancel** → ERPNext tự tạo reverse GL Dr 511 100M / Cr 131 100M → **511 balance = -100M ❌**
5. Báo cáo P&L tháng 1: doanh thu = 0 (vì closing JE đã reset). Báo cáo P&L tháng 2: doanh thu = -100M ❌
6. **421 vẫn = 100M** — không tự reverse → retained earnings sai số liệu

**🔴 Vấn đề 2 — Không idempotent**

Wizard không check "đã có closing JE cho kỳ này chưa". KTT chạy 2 lần (vô tình hoặc do reload page):
- Tạo 6 JE thay vì 3
- Submit tất cả → 511 = -100M (đã zero ra rồi lại Dr lần 2), 421 = +200M ❌

**🔴 Vấn đề 3 — Duplicate ERPNext native `Period Closing Voucher`**

ERPNext đã có sẵn doctype `Period Closing Voucher`:
- Submit → tự gen GL closing **toàn bộ** P&L accounts về `Closing Account` (default = TK 4211 hoặc Retained Earnings tùy COA)
- Atomic, không cần 3 JE riêng
- Có sẵn idempotency check
- Đã add vào sidebar dưới tên **"Phiếu khóa sổ kỳ"** ở section Tổng hợp (commit `f0c5e42`)

**Wizard period-closing-911 đang LẶP LẠI chức năng PCV nhưng làm sai cách.**

**🟡 Vấn đề 4 — Monthly vs Yearly semantics**

TT99/2025 + thông lệ VN: kết chuyển 5xx/6xx → 911 → 421 thực hiện **cuối năm tài chính**, không phải hàng tháng. Wizard hiện cho phép chạy hàng tháng → trái với thông lệ + tạo các vấn đề trên.

Một số DN VN (đặc biệt DN nhỏ) làm "kết chuyển tháng" để có sổ rõ ràng, nhưng đây là **practice không bắt buộc** và đối nghịch với ERPNext real-time.

### 2.2 `manufacturing-costing-wizard` — Tính giá thành SX

**File:** `vn_accounting/costing/__init__.py` (242 dòng)

**Logic hiện tại:**
```python
Step 2 (aggregate_production_costs): SUM GL Entry 621/622/627 theo cost_center, theo period
Step 3 (calculate_unit_costs): với input WIP Valuation từ user → tính unit_cost
Step 7 (create_costing_journal_entries):
  JE1: Cr 621 + Cr 622 + Cr 627 / Dr 154
  JE2: Cr 154 / Dr 155 (DN SX) hoặc Cr 154 / Dr 632 (DN dịch vụ)
```

**🔴 Vấn đề 1 — Phụ thuộc Stock Settings**

ERPNext Stock Entry "Manufacture" có thể tự sinh GL:
- Setup A: Dr 155 / Cr 621 (skip 154) — nếu Settings.disable_work_in_progress = True
- Setup B: Dr 154 / Cr 621 khi Material Issue, sau đó Dr 155 / Cr 154 khi Manufacture submit — nếu có WIP warehouse

Trong setup B: Wizard JE1 (Cr 621 / Dr 154) sẽ **double-count** vì Stock Entry đã chuyển 621 → 154 rồi.
Trong setup A: Wizard JE1 sẽ chuyển 621 → 154 OK, nhưng JE2 (Cr 154 / Dr 155) bị Stock Entry track double.

**Wizard không biết DN đang dùng setup nào.** Không có pre-check.

**🔴 Vấn đề 2 — Chỉ aggregate, không thực sự phân bổ 627**

Spec §12.3 (BUSINESS_LOGIC.md) yêu cầu **6 tiêu thức phân bổ TK 627**: giờ máy, giờ công, sản lượng, chi phí NVL, chi phí nhân công, tổng chi phí trực tiếp.

Code hiện tại `aggregate_production_costs`:
```python
SUM(... WHEN account = 627 THEN debit - credit) AS overhead
GROUP BY cost_center
```

→ Chỉ tổng overhead **theo cost_center sẵn có trên GL Entry**. Không có logic phân bổ TK 627 từ "khu vực phân xưởng chung" xuống "từng sản phẩm theo giờ máy".

**Wizard này không hoàn thành chức năng spec yêu cầu** — chỉ là báo cáo tổng hợp đẹp hơn, không phải engine tính giá thành thật.

**🟡 Vấn đề 3 — JE2 transfer_mode = 'cogs_direct' (DN dịch vụ) xung đột với ERPNext**

`JE2: Cr 154 / Dr 632` cho DN dịch vụ. NHƯNG TK 632 trong ERPNext có thể được auto-post khi Sales Invoice submit (nếu service item set valuation). Tạo thêm JE Dr 632 → double-count CGS.

### 2.3 LCV (Landed Cost Voucher) hooks

**File:** `vn_accounting/landed_cost/seed.py` + `lcv_hooks.py`

LCV của ERPNext native:
- Submit: cập nhật `valuation_rate` của Purchase Receipt items được phân bổ
- Re-post stock ledger + GL entries với rate mới
- Đã **real-time**

Vn_accounting bổ sung gì? Chỉ là:
- Seed các loại expense_type mặc định (vận chuyển, bốc xếp, thuế NK...)
- Hook trên submit/cancel để validate VAT NK khấu trừ vs không khấu trừ

**✅ Không vi phạm real-time model.** LCV hoạt động đúng pattern ERPNext.

---

## 3. Đề xuất chiến lược

### Option A — Bỏ wizard period-closing-911, dùng ERPNext PCV native (Khuyến nghị)

**Lý do:**
1. ERPNext PCV đã làm đúng việc + idempotent + atomic
2. Tránh hoàn toàn 3 vấn đề: cancel-create-negative-balance, double-run double-count, double-mechanism
3. Một entry point duy nhất "Phiếu khóa sổ kỳ" trên sidebar — đơn giản cho KTT

**Đánh đổi:**
- KTT mất khả năng "kết chuyển tháng" (sổ Nhật ký chung sẽ không có dòng "KC 511 tháng 1 sang 911"). P&L tháng vẫn tính đúng qua report (đọc GL by date range).
- DN nhỏ có thói quen xem JE kết chuyển trên sổ — sẽ phải đổi mindset.

**Hành động:**
- Bỏ sidebar item "Kết chuyển cuối kỳ" → period-closing-911
- Bỏ wizard code + Page (giữ lại trong git history phòng trường hợp đổi ý)
- Cập nhật doc Help: "Cuối năm, dùng Phiếu khóa sổ kỳ thay vì wizard kết chuyển tháng"

### Option B — Giữ wizard period-closing-911 nhưng làm yearly-only + idempotent (Compromise)

**Yêu cầu sửa:**
1. Block run nếu `period_end != fiscal_year_end_date`
2. Block run nếu `tabJournal Entry` đã có closing JE với marker `[KC-FY-{year}]` trong period đó
3. Submit JE thay vì để draft → KTT không quên (atomic + locked)
4. **Cancel SI sau closing**: thêm hook on Sales Invoice cancel → throw error "Đã chốt sổ năm X, không thể cancel SI thuộc năm X. Phải tạo Credit Note ở năm hiện hành."

**Đánh đổi:**
- Vẫn duplicate ERPNext PCV (2 cơ chế cùng làm 1 việc)
- Phức tạp hơn — phải maintain logic + edge cases

### Option C — Giữ wizard nhưng monthly-only + warning rõ ràng (Liability)

KHÔNG khuyến nghị. Giữ design hiện tại = giữ các bug đã liệt kê. Chỉ thêm warning UI không fix được bug.

---

### Manufacturing-costing-wizard

**Option M1 — Bỏ hoàn toàn**: ERPNext Stock Entry Manufacture + Work Order đã đủ cho DN SX vừa-nhỏ. DN lớn cần phân bổ 627 → custom solution riêng theo nhu cầu.

**Option M2 — Refactor thành "Báo cáo tập hợp + Manual JE template"**:
- Bỏ logic create_costing_journal_entries
- Page chỉ aggregate + tính unit cost + xuất Excel
- KTT đọc kết quả + tạo JE thủ công nếu cần (vì JE manual dễ kiểm soát + audit)

**Option M3 — Hoàn thiện logic phân bổ 627 + pre-check Stock Settings**:
- Thêm 6 tiêu thức phân bổ 627 thực sự (giờ máy, giờ công, sản lượng...)
- Pre-check Stock Settings để biết DN setup A hay B → skip JE phù hợp
- Phức tạp, đòi hỏi 2-3 ngày dev + test

---

## 4. Tóm tắt khuyến nghị

| Component | Khuyến nghị | Reasoning |
|---|---|---|
| **period-closing-911 wizard** | **Option A: Bỏ** | Duplicate PCV native, có bug nghiêm trọng (cancel/double-run). Khắc phục phức tạp. |
| **Sidebar item "Kết chuyển cuối kỳ"** | **Bỏ** | Hệ quả của Option A |
| **Sidebar item "Phiếu khóa sổ kỳ"** (Period Closing Voucher) | **Giữ (đã add)** | Đây là cơ chế chuẩn ERPNext + đúng yearly |
| **manufacturing-costing-wizard** | **Option M2: Refactor thành report-only** | Vừa-phải, an toàn, KTT có visibility full. Phân bổ 627 thật để pha 2 nếu cần. |
| **Sidebar item "Tính giá thành cuối kỳ"** | **Đổi tên: "Báo cáo tập hợp chi phí SX"** | Phản ánh đúng chức năng mới |
| **LCV** | **Giữ nguyên** | Đã đúng pattern ERPNext real-time |

---

## 5. Action plan đề xuất

### Step 1 (immediate, low-risk)
- Sửa label sidebar "Kết chuyển cuối kỳ" thành **"Kết chuyển cuối năm (cũ, sẽ bỏ)"** — flag để KTT không dùng
- Thêm warning ở wizard page header: "Wizard này có bug đã biết. Dùng 'Phiếu khóa sổ kỳ' thay thế."
- Vẫn giữ code trong git để review tiếp.

### Step 2 (sau khi anh duyệt direction)
- Quyết định Option A vs B cho period-closing
- Quyết định Option M1/M2/M3 cho manufacturing-costing
- Em viết PR riêng cho từng quyết định, có rollback path

### Step 3 (compliance check)
- Test với 1 Company demo trong 1 fiscal year đầy đủ:
  - Tạo Sales Invoices + Purchase Invoices + Stock Entries
  - Submit PCV cuối năm
  - Verify P&L report đúng cho mỗi tháng + cả năm
  - Verify Sổ Nhật ký chung (S03a-DN) có đủ JE cần thiết theo TT99/2025
- Test cancel SI sau PCV submit → confirm ERPNext throw error đúng cách

---

## 6. Câu hỏi cho anh quyết

1. **period-closing-911 wizard**: chọn Option A (bỏ) hay Option B (yearly-only + idempotent)?
2. **manufacturing-costing-wizard**: chọn M1 (bỏ) / M2 (report-only) / M3 (full refactor)?
3. **Sổ Nhật ký chung TT99/2025**: anh có yêu cầu hiển thị các bút toán "Kết chuyển 511 → 911" hàng tháng/năm hay không? Hay chỉ cần Phiếu khóa sổ kỳ yearly là đủ với cơ quan thuế?
4. **DN target của vn_accounting**: DN nhỏ-vừa (SI/PI volume <500/tháng, 1-3 cost center) hay có hướng tới DN lớn (volume cao, nhiều cost center, cần phân bổ 627 nghiêm chỉnh)?
