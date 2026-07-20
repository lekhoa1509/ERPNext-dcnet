# dcnet_contract — Câu hỏi cần xác nhận trước khi viết spec

> **Status:** Architecture decided (xem `architecture-contract-and-pakd.md`); spec chi tiết Sprint A1 chưa viết.
> **Nguồn:** `docs/accounting-requirements/converted/mau-01-PAKD.md`, `mau-02-PAKD.md`, `mau-03-PAKD.md`
> **File chị em:** `dcnet_pakd-questions.md` (commission policy + workflow chi tiết PAKD)
> **Ngày tạo:** 2026-04-10
> **Người trả lời cần:** Kế toán DCNet (P. Tổng hợp) + BGĐ + 1 sales lead (xác nhận flow nghiệp vụ)

## Cách dùng file này

- Tổng cộng **16 câu** chia 3 nhóm: **Blocking** (phải trả lời trước Sprint A1), **Soft-blocking** (có default, confirm để khỏi rework), **Soft** (có thể chốt trong spec).
- Mỗi câu có **Đáp án gợi ý từ templates** (nếu có) — khi đã có gợi ý, người trả lời chỉ cần ✅ confirm hoặc ❌ override.
- Khi câu được trả lời → tick vào checkbox + ghi tên người + ngày → đồng bộ vào spec.

---

## Nhóm A: BLOCKING (10 câu — phải trả lời trước Sprint A1)

### Q1. Schema header DCNet Contract — đủ chưa?

**Đáp án gợi ý từ Mẫu 01 + 03:**

```
Header fields (chung cho cả 2 loại):
- customer (Link Customer)
- sales_person (Link Employee)
- department (Link Department)
- branch (Link Branch — HCM | HN)
- loai_du_an (Select: Viễn thông | CNTT | Mua bán VTTB | Thi công)
- service_type (Select: P2P | MPLS | ILL | FTTH DN | FTTH HGD | IT Managed | VTTB | Thi công)
- package_name (Data — tên gói/băng thông/FO)
- contract_no (Data, unique)
- contract_date (Date)
- phu_luc_no (Data, optional)
- phu_luc_date (Date, optional)
- acceptance_date (Date — ngày nghiệm thu)
- prepared_date (Date — ngày lập bảng)
- revision_count (Int — "thay đổi lần")
- revision_reason (Select: Gia hạn dịch vụ | Gia hạn hợp đồng | Điều chỉnh nội dung)

Recurring-only:
- service_address (Data — "điểm đầu - điểm cuối")
- payment_cycle (Select: Hàng tháng | 6 tháng | 12 tháng)
- term_months (Int — số tháng tổng của hợp đồng)
- unit_price (Currency — cước hàng tháng, đơn vị 1000 VNĐ?)
- setup_fee (Currency — phí lắp đặt 1 lần)

One-off-only:
- delivery_address (Data — địa chỉ giao hàng/thi công)
- goods_name (Data — tên thiết bị/gói thi công)
- payment_date (Date — ngày thanh toán; trùng acceptance_date trong nhiều case)
```

**Câu hỏi:**
1. Có thiếu field nào quan trọng từ thực tế không?
2. `term_months` có cần thiết không, hay đã suy ra từ `start_date` + `end_date`?
3. Đơn vị tiền là **1000 VNĐ** (như Mẫu 01/03 ghi) hay **VNĐ** (như Mẫu 02 ghi)? Khác nhau giữa các loại?
4. `acceptance_date` (ngày nghiệm thu) là ngày bắt đầu tính cước, hay là một ngày khác?

- [ ] Trả lời: ___ — ngày: ___

---

### Q2. State machine DCNet Contract — đủ chưa?

**Đáp án gợi ý:**

```
Draft       → Active       (khi submit, nếu acceptance_date hợp lệ)
Active      → Suspended    (manual: kế toán/BGĐ tạm ngưng dịch vụ)
Active      → Cancelled    (manual: chấm dứt sớm)
Active      → Expired      (auto: scheduler kiểm tra end_date)
Suspended   → Active       (manual: khôi phục)
Suspended   → Cancelled    (manual)
Cancelled   → (terminal)
Expired     → (terminal)
```

**Câu hỏi:**
1. Có cần state riêng cho **"Chờ lắp đặt"** (sau khi ký hợp đồng nhưng chưa nghiệm thu)? Hay vẫn dùng Draft?
2. Trigger **Suspended** là **manual** (kế toán click) hay **auto** (khách nợ X ngày)? Nếu auto, X là bao nhiêu?
3. **"Tạm dừng dịch vụ vì khách yêu cầu"** vs **"Tạm dừng vì khách nợ"** — cần 2 state khác nhau, hay chung Suspended với reason?
4. Có cần state **"Pending Cancellation"** (đã yêu cầu hủy, chưa hoàn tất) không?

- [ ] Trả lời: ___ — ngày: ___

---

### Q3. Term vs Payment cycle — có thể khác nhau không?

**Bối cảnh:** Mẫu 01 ghi `payment_cycle` enum {Hàng tháng, 6 tháng, 12 tháng}. Bảng 12 cột tháng gợi ý `term_months = 12` mặc định.

**Câu hỏi:**
1. Một hợp đồng `term_months = 24` có thể có `payment_cycle = 6 tháng` (4 lần thanh toán)? Hay term luôn = 12?
2. Nếu term ≠ cycle, billing_schedule sinh ra theo cycle hay theo tháng?
   - **Option A:** Mỗi tháng 1 row (12 rows cho term=12). PE thanh toán cycle 6 tháng → flip 6 rows cùng lúc.
   - **Option B:** Mỗi cycle 1 row (2 rows cho term=12, cycle=6). Đơn giản nhưng mất chi tiết theo tháng.
3. Có hợp đồng nào prepay TOÀN BỘ term (1 lần thanh toán cho 12 tháng)? Đây có phải là `payment_mode = Prepay` thay vì `payment_cycle = 12 tháng`?

**Recommend:** Option A — luôn 1 row/tháng để nhất quán với Mẫu 01 (12 cột); cycle quyết định N rows được flip cùng lúc khi PE submit.

- [ ] Trả lời: ___ — ngày: ___

---

### Q4. Acceptance date logic — billing bắt đầu từ đâu?

**Bối cảnh:** Mẫu 01 ghi nguyên văn:

> "Doanh thu của tháng đầu tiên điền theo thực tế phát sinh (theo hóa đơn đã xuất) nếu như ngày bắt đầu tính cước dịch vụ không trọn tháng. Công thức tính cước cho tháng đầu và tháng cuối: `Tổng cước = Round(cước_hàng_tháng / số_ngày_trong_tháng, 0) × số_ngày_thực_tế_sử_dụng`"

**Câu hỏi:**
1. Confirm công thức proration trên đúng — billing_schedule row đầu tiên (tháng có acceptance_date) phải tính theo công thức này, không phải full price.
2. Round to **0** decimal nghĩa là làm tròn về VND nguyên — confirm?
3. Tháng cuối (nếu term không trọn tháng) cũng proration tương tự?
4. Setup_fee có phụ thuộc proration không, hay luôn full price tại month_index 0?

**Recommend default:** Áp dụng công thức proration cho cả tháng đầu và tháng cuối; setup_fee luôn full.

- [ ] Trả lời: ___ — ngày: ___

---

### Q5. Grace period Overdue

**Câu hỏi:** Sales Invoice quá hạn bao nhiêu ngày thì billing_schedule row chuyển từ `Invoiced` → `Overdue`?

**Recommend:** **15 ngày** (configurable trong `DCNet Contract Settings`, có thể override per Contract).

**Phụ:** Khi Overdue, hệ thống có gửi email tự động không? Đến ai (NVKD? customer? cả hai)?

- [ ] Trả lời: ___ — ngày: ___

---

### Q6. Bad debt write-off flow

**Câu hỏi:** Khi billing_schedule row stuck ở Overdue quá lâu, ai quyết định Write Off?

**Recommend:**
- Manual button "Write Off" trên billing_schedule row (chỉ role Accounts Manager).
- Click → state Overdue → Written Off → tạo Journal Entry Draft (Dr Bad Debt Expense, Cr AR).
- Commission line matching → Cancelled (NVKD không nhận commission).

**Câu hỏi phụ:** Account "Chi phí nợ khó đòi" trong VN COA TT99 là số nào? (642?)

- [ ] Trả lời: ___ — ngày: ___

---

### Q7. Revision chain semantics — proration?

**Bối cảnh:** Mẫu 01 đã có sẵn field `revision_count` + `revision_reason`. Confirm revision có sẵn trong quy chế.

**Câu hỏi:** Khi hợp đồng được Revision (ví dụ: tháng 6 upgrade từ 100Mbps lên 200Mbps, đơn giá tăng 50%):
- **Option A — Proration:** Tháng 6 split thành 2 dòng billing (15 ngày @ giá cũ + 15 ngày @ giá mới). Phức tạp.
- **Option B — Áp dụng từ kỳ kế tiếp:** Tháng 6 vẫn full giá cũ. Tháng 7 trở đi giá mới.
- **Option C — Áp dụng từ ngày revision:** Tháng 6 = full giá mới (DCNet ưu đãi cho khách).

**Recommend:** Option B (đơn giản, dễ giải thích cho khách + kế toán). Confirm?

- [ ] Trả lời: ___ — ngày: ___

---

### Q8. Shadow Sales Order — field mapping cụ thể

**Bối cảnh:** Khi Contract one-off có vật tư được Active, hook tự tạo shadow SO. Cần chốt mapping.

**Đáp án gợi ý:**

| Contract field | → Shadow SO field |
|---|---|
| `customer` | `customer` |
| `company` | `company` |
| `acceptance_date` | `transaction_date` |
| `delivery_address` | `shipping_address_name` (tạo Address mới nếu chưa có) |
| `branch` | `cost_center` (lookup từ branch → CC) |
| `contract_items` (child table) | `items` (child table) |
| `taxes_and_charges_template` | `taxes_and_charges` (Sales Taxes Template) |

**Câu hỏi:**
1. Tax template lấy từ đâu: từ Contract field, từ Customer Group, từ Customer.tax_template, hay từ Company default?
2. Shadow SO có cần `delivery_date`? Nếu có, lấy từ field nào của Contract?
3. Cost center mapping branch → CC: cần Long config tay 1 lần (HCM Branch → HCM Cost Center, HN Branch → HN Cost Center)?
4. Project link (nếu có): Contract.project → SO.project?

- [ ] Trả lời: ___ — ngày: ___

---

### Q9. Account posting cho chi phí ngoài (VN COA TT99)

**Bối cảnh:** PAKD post 3 chi phí ngoài (Manager Services, Add Costs, Phí GPVT) thành Journal Entry Draft. Cần biết account VN COA cho mỗi loại.

**Câu hỏi:** Trong VN COA TT99 (đã import qua `vn_accounting`), 3 chi phí ngoài đi vào account nào?

**Suggest** (cần kế toán confirm):
- **Manager Services** (hoa hồng cho khách): account `641` (Chi phí bán hàng) hoặc `6418` (Chi phí khác bằng tiền)?
- **Add Costs** (kê thêm trả khách): cùng `641` hay `6418`?
- **Phí GPVT + CIVT** (phí quyền viễn thông): có account riêng theo TT99 không, hay gộp `642` (Chi phí quản lý DN)?

**Cost center:** Lấy từ `Contract.branch` hay PAKD chỉ định?

- [ ] Trả lời: ___ — ngày: ___

---

### Q10. Chu kỳ submit PAKD vs số PAKD per Contract

**Bối cảnh:** Quy chế ghi "PAKD tháng N-1 phải gửi trước 05/N". Mẫu 01 có 12 cột tháng (cả năm). Mâu thuẫn?

**Câu hỏi mấu chốt:** Một hợp đồng recurring 12 tháng có:
- **Option A — 1 PAKD duy nhất:** Submit lần đầu khi ký, projection cả 12 tháng. Lương KD post tự động hàng tháng theo cash basis. Không cần submit PAKD lại trừ khi revision.
- **Option B — 12 PAKD:** Mỗi tháng submit 1 PAKD (Mẫu 01 mỗi tháng filter theo doanh thu thực tế tháng đó). Cutoff ngày 5 áp dụng cho từng tháng.
- **Option C — Lai:** 1 PAKD chính làm projection, mỗi tháng kế toán "chấp nhận" để trigger lương — không cần re-approve.

**Recommend:** Option A. Cutoff ngày 5 chỉ áp PAKD MỚI (bao gồm cả Mẫu 02 monthly rollup và Mẫu 03 one-off). Hợp đồng recurring có Mẫu 01 đã approved 1 lần thì lương auto-post hàng tháng không cần resubmit.

**Vì sao mấu chốt:** Quyết định toàn bộ workflow PAKD và state machine commission line. Sai hướng → rewrite cả Sprint B2-B3.

- [ ] Trả lời: ___ — ngày: ___

---

## Nhóm B: SOFT-BLOCKING (4 câu — có default, confirm để khỏi rework)

### Q11. Multi-currency

**Recommend:** v1 chỉ VND. Confirm không có hợp đồng USD hoặc khách nước ngoài?

- [ ] Trả lời: ___ — ngày: ___

---

### Q12. Permission matrix

**Recommend:**

| Role | Tạo Contract | Submit Active | Cancel | Tạo PAKD | Approve PAKD |
|---|---|---|---|---|---|
| Sales Rep | ✅ (own only) | ❌ | ❌ | ✅ (own only) | ❌ |
| Sales Manager (GĐ TT KD) | ✅ | ✅ | ❌ | ✅ | ✅ (cấp 1) |
| Branch Manager (GĐ CN HN) | ✅ | ✅ | ❌ | ❌ | ✅ (cấp 2 — chỉ HN) |
| P. Tổng hợp | ❌ | ❌ | ❌ | ❌ | ✅ (cấp 3) |
| BGĐ | ✅ | ✅ | ✅ | ❌ | ✅ (cấp cuối) |
| Accounts Manager | ❌ | ❌ | ❌ | ❌ | ❌ (chỉ post JE) |

Confirm? Có role nào thiếu?

- [ ] Trả lời: ___ — ngày: ___

---

### Q13. Renewal flow

**Câu hỏi:** Hợp đồng Expired có cần feature "Renew" trong v1 không, hay user tạo Contract mới từ template?

**Recommend:** v1 KHÔNG có nút Renew. User dùng `DCNet Contract Template` + duplicate. v2 thêm nút "Renew" tự động copy data + tăng `revision_count`.

- [ ] Trả lời: ___ — ngày: ___

---

### Q14. Notification rules

**Recommend:**

| Sự kiện | Người nhận | Channel |
|---|---|---|
| Contract Active | NVKD + Customer | Email |
| Billing schedule row Invoiced | NVKD + Customer | Email + system notification |
| Overdue | NVKD + Accounts Manager | Email |
| 30 ngày trước Expired | NVKD + Customer + BGĐ | Email |
| PAKD chuyển trạng thái workflow | NVKD + approver tiếp theo | System notification |

Confirm? Có notification nào thiếu hoặc thừa?

- [ ] Trả lời: ___ — ngày: ___

---

## Nhóm C: SOFT (2 câu — chốt trong spec, không cần kế toán)

### Q15. Reports v1 — chốt 5 reports đầu tiên

**Recommend** cho Sprint A5:

1. **Contract Listing** — danh sách Contract theo branch/sales_person/state, có filter date.
2. **Billing Schedule Aging** — báo cáo công nợ theo tuổi nợ (current / 1-30 / 31-60 / 60+).
3. **Recurring Revenue Forecast** — tổng doanh thu projected theo tháng tới (12 tháng).
4. **Contract Renewal Pipeline** — Contract sẽ Expired trong 60 ngày tới.
5. **Sales Rep Performance** — số contract Active + tổng giá trị + tỷ lệ Paid/Overdue per NVKD.

Cộng thêm cho Sprint B4 (PAKD reports):

6. **Commission Summary** — commission đã post per NVKD per tháng.
7. **PAKD Approval Queue** — các PAKD đang chờ duyệt theo cấp.

Có report nào bị thiếu trong "must-have v1"?

- [ ] Trả lời: ___ — ngày: ___

---

### Q16. Workspace layout

**Recommend** cho Sprint A5:

```
Workspace "Hợp đồng" (dcnet_contract):
  Sidebar:
    - DCNet Contract (list)
    - Billing Schedule (list, cross-contract)
    - Sales Invoice (filter where contract_ref is set)
    - Payment Entry (filter where contract_ref is set)
    - Contract Template
  Number cards:
    - Contract Active count
    - Tổng MRR (Monthly Recurring Revenue)
    - Tổng AR Outstanding
    - Overdue count
  Charts:
    - Revenue trend 12 tháng
    - Contract by state pie
```

Confirm layout?

- [ ] Trả lời: ___ — ngày: ___

---

## Tóm tắt đầu vào cần từ DCNet trước Sprint A1

| Loại | Yêu cầu |
|---|---|
| **Trả lời 10 câu Blocking** (Q1–Q10) | Người trả: kế toán + BGĐ |
| **Confirm 4 câu Soft-blocking** (Q11–Q14) | Người trả: 1 sales lead |
| **Chốt 2 câu Soft** (Q15–Q16) | Long quyết, không cần ngoài |
| **Danh sách service_type chính thức** | Lấy từ kế toán/sales — list tên + mã, tối thiểu 8 enum |
| **1-2 hợp đồng thật ẩn danh** mỗi loại | Recurring + One-off → làm test fixture cho golden test B1 |
| **Mã account TT99 chính thức** cho 3 chi phí ngoài + 1 bad debt account | Kế toán confirm |
| **Mapping Branch → Cost Center** | Long config tay sau khi kế toán xác nhận tên CC trong VN COA |

Khi đủ 7 input trên + 10 câu blocking đã trả lời → Long viết spec chi tiết Sprint A1+A2 và bắt đầu code.
