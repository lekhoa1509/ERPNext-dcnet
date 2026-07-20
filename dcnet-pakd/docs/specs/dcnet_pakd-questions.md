# dcnet_contract + dcnet_pakd — Câu hỏi cần DCNET xác nhận

> **Status:** Architecture decided (2026-04-09 discussion); spec v3 pending
> **Liên quan:** `dcnet_contract.md` (new), `dcnet_pakd.md` (rewrite)
> **Nguồn tài liệu gốc:** `docs/accounting-requirements/converted/`
> **Ngày tạo:** 2026-04-08
> **Cập nhật lớn 2026-04-09:** PAKD đã tách thành 2 app — `dcnet_contract` (master contract) + `dcnet_pakd` (thin commission layer). Option D: Contract-first, shadow Sales Order cho One-off có vật tư.
> **Cập nhật lớn 2026-05-14:** Realignment session. 8 decisions chốt — xem `docs/specs/2026-05-14-contract-pakd-vnacc-realignment.md` ở bench-root. Đóng Q5/Q5b, Q7/Q7b, Q8. Open thêm Q19 (TK cụ thể cho MS/AC/Referral sau khi sửa semantic).
> **Người nhận cần trả lời:** Kế toán DCNET (P. Tổng hợp) + BGĐ

---

## Cách dùng file này

- Mỗi câu hỏi có trường **Trạng thái**, **Câu trả lời**, **Người trả lời**, **Ngày**.
- Câu hỏi **Blocking** = phải có câu trả lời trước khi bắt đầu code DocType JSON.
- Câu hỏi **Non-blocking** = đã có default hợp lý trong spec, có thể confirm sau.
- ✅ **Answered (internal)** = trả lời trong discussion session giữa Long và Claude, chưa confirm với kế toán DCNET.
- Khi có câu trả lời → cập nhật trực tiếp vào file này, sau đó đồng bộ vào `dcnet_pakd.md` nếu cần thay đổi thiết kế.

---

## Blocking (6 câu — phải trả lời trước Sprint 1)

### Q1. Commission rates có cố định không?

Hệ số `10% / 75% / 2.2% / 6%` (Manager Services / Add Costs / Phí GPVT / Lương KD) lấy từ Mẫu 01.

**Câu hỏi:**
- Các hệ số này **cố định** cho mọi hợp đồng, hay **thay đổi** theo loại dịch vụ (P2P / MPLS / ILL / FTTH / IT managed)?
- Có khác biệt giữa chi nhánh HCM vs HN không?
- Có khác biệt theo hạng khách hàng (KH lớn / KH nhỏ) không?
- Nếu thay đổi, căn cứ dựa trên đâu?

**Vì sao blocking:** Quyết định data model của `PAKD Commission Rule Template` — có phải thiết kế ma trận `(pakd_type × service_type × branch)` hay một template duy nhất là đủ.

**Default nếu không trả lời:** 1 template mặc định + cho phép kế toán override từng PAKD.

- **Trạng thái:** ⏳ Chờ trả lời
- **Câu trả lời:**
- **Người trả lời:**
- **Ngày:**

---

### Q3. Add Costs — Tài khoản kế toán nào?

Biên bản §5 ghi: *"hoạch toán chi phí ngoài vào tài khoản **không tính thuế**"*.

**Câu hỏi:**
- Xin xác nhận "tài khoản không tính thuế" là **tài khoản không phát sinh VAT đầu vào/đầu ra** (ví dụ một mã TK riêng không mapped vào báo cáo VAT), hay chỉ là tài khoản chi phí bình thường được gắn cờ "không khấu trừ"?
- TK cụ thể là gì trong COA TT99 đã cài? (Gợi ý: có thể là nhóm 642, hoặc một TK chi phí riêng.)
- Add Costs (KH kê thêm) và Manager Services (hoa hồng KH) có dùng **cùng một TK** hay hai TK khác nhau?

**Vì sao blocking:** Quyết định field `taxless_expense_account` trong rule template + quyết định cách sinh Journal Entry (1 dòng hay 2 dòng DR riêng).

**Default nếu không trả lời:** Tạm chỉ 1 field `taxless_expense_account` dùng chung, kế toán chỉnh khi seed production.

- **Trạng thái:** ⏳ Chờ trả lời
- **Câu trả lời:**
- **Người trả lời:**
- **Ngày:**

---

### Q4. Ai đang giữ từng vai trò duyệt PAKD?

Workflow spec §6 có 5 role:
- `PAKD Sales Director HCM` (GĐ TT Kinh doanh HCM)
- `PAKD Sales Director HN` (GĐ TT Kinh doanh HN)
- `PAKD General Department` (P. Tổng hợp)
- `PAKD Branch Director HN` (GĐ Chi nhánh HN)
- `PAKD Board` (Ban Giám đốc)

**Câu hỏi:**
- Ai hiện giữ mỗi vai trò? (Cần tên + email để seed User + User Permission trên production.)
- Một người có thể giữ **nhiều** vai trò cùng lúc không? (Vd. BGĐ kiêm GĐ CN HN?)
- Khi một role có **nhiều người**, việc duyệt yêu cầu **bất kỳ một ai** duyệt, hay cần **tất cả** duyệt?
- Có người backup khi người duyệt chính vắng mặt không?

**Vì sao blocking:** Quyết định cách seed User + User Permission, và có cần thiết kế "delegation" không.

**Default nếu không trả lời:** Tạm 1 người/role, không delegation; admin tự thêm User sau.

- **Trạng thái:** ⏳ Chờ trả lời
- **Câu trả lời:**
- **Người trả lời:**
- **Ngày:**

---

### Q5. ~~PAKD Rollup Mẫu 02 — Thêm hợp đồng mới giữa chu kỳ thế nào?~~

**SUPERSEDED** by architecture discussion 2026-04-09. Mẫu 02 is no longer a PAKD type — it's a monthly changelog (`PAKD Monthly Activity`). See Q5b below.

- **Trạng thái:** ✅ Superseded
- **Ngày:** 2026-04-09

---

### Q5b. (NEW) Mẫu 02 = Monthly Activity — Confirm bản chất

**Mẫu 02 chính thức BỎ 2026-05-14.** Mỗi HD FTTH DN cũng là 1 PAKD riêng theo Mẫu 01. Mẫu 02 in form thay bằng **Report mới `PAKD phát sinh trong tháng`** (Script Report, filter month/year/branch, print format có chỗ ký từng dòng cho quản lý duyệt).

NVKD FTTH DN có 30-50 HD/tháng → wizard "Tạo PAKD hàng loạt" là task roadmap riêng sau realignment.

- **Trạng thái:** ✅ CLOSED 2026-05-14 — Mẫu 02 BỎ
- **Quyết định:** Mỗi HD FTTH = 1 PAKD; Report thay Mẫu 02 print
- **Người quyết định:** Long (realignment session 2026-05-14)

---

### Q7. ~~Revision PAKD — Thay thế hay cộng dồn?~~

**SUPERSEDED** by architecture discussion 2026-04-09. See Q7b below.

- **Trạng thái:** ✅ Superseded
- **Ngày:** 2026-04-09

---

### Q7b. (NEW) Revision = new PAKD in chain, supersede future accruals

**SUPERSEDED 2026-05-14.** Model revision chain cũ (mỗi phụ lục → tạo PAKD mới với `amended_from`, PAKD cũ Superseded) đã được thay bằng:

**1 PAKD = 1 Contract suốt đời; phụ lục là child table `PAKD Revision` bên trong PAKD.** Mỗi PAKD Revision có workflow approval chain riêng, snapshot rate riêng, link tới Contract Addendum tương ứng. Engine lookup revision active tại kỳ T (effective_from ≤ period_start) để áp tỷ lệ chính xác cho commission_line + beneficiary_line của kỳ đó.

Pivot view tự nhiên xuyên suốt cả vòng đời HD + tất cả revisions (giải quyết yêu cầu user "pivot ở nhiều tháng xuyên suốt quá trình thực hiện hợp đồng và các phụ lục").

**Câu hỏi còn để mở cho kế toán:** Khi phụ lục có effective_from giữa kỳ và đã sinh SI Invoiced (chưa Paid), có cần auto-create Credit Note không? (Default: manual + alert)

- **Trạng thái:** ✅ CLOSED 2026-05-14 — chuyển từ revision chain sang sub-table model
- **Người quyết định:** Long (realignment session 2026-05-14)

---

### Q8. Liên kết hợp đồng — Sales Order hay free-text?

**CLOSED 2026-05-14.** Tạo DocType `DCNET Contract` riêng (option 3 trong câu hỏi gốc). PAKD `contract_ref` Link → DCNET Contract. Sales Order trở thành **shadow SO** ẩn cho phần items One-off Goods có stock (xem architecture spec §4).

Custom field `dcnet_contract` + `billing_period_idx` thêm trên Sales Invoice + Payment Entry để kế toán mở SI/PE thấy ngay hợp đồng nào, kỳ nào — liên kết explicit thay vì derive qua billing_schedule.sales_invoice lookup.

- **Trạng thái:** ✅ CLOSED 2026-05-14
- **Câu trả lời:** DCNET Contract DocType riêng + Custom field SI/PE
- **Người quyết định:** Long (realignment session 2026-05-14)

---

## Non-blocking (4 câu — có default, confirm sau cũng được)

### Q2. Manager Services — Sinh Payment Entry tự động không?

**Câu hỏi:**
- Kế toán có thực sự **xuất Payment Entry** để trả số tiền Manager Services (hoa hồng) cho khách hàng, hay đây chỉ là **khoản giảm trừ** trên hóa đơn bán ra?
- Nếu có trả — trả 1 lần/tháng gom các PAKD lại, hay trả từng PAKD?

**Default trong spec:** Chỉ sinh **Journal Entry draft**, không sinh Payment Entry. Kế toán tự tạo PE khi thực sự thanh toán.

- **Trạng thái:** ⏳ Default applied
- **Câu trả lời:**
- **Người trả lời:**
- **Ngày:**

---

### Q6. Pro-ration tháng đầu/cuối — Rounding mode nào?

Mẫu 01 Ghi chú mục I: *"Tổng cước = Round(Cước hàng tháng / số ngày trong tháng, 0) * số ngày thực tế sử dụng trong tháng"*.

**Câu hỏi:**
- Excel mặc định dùng **half-away-from-zero** (2.5 → 3). Python `round()` dùng **banker's rounding** (2.5 → 2). Với DCNET, rounding mode nào đúng?
- Có cần tuân thủ quy định thuế nào về rounding không?

**Default trong spec:** Half-up (ROUND_HALF_UP của Python `decimal.Decimal`) để khớp Excel.

- **Trạng thái:** ⏳ Default applied
- **Câu trả lời:**
- **Người trả lời:**
- **Ngày:**

---

### Q9. Đơn vị hiển thị — 1000 VNĐ hay VNĐ?

Mẫu 01 và Mẫu 02 ghi "Đơn vị: 1000 VNĐ" — người dùng nhập số tiền ở đơn vị nghìn.

**Câu hỏi:**
- DB lưu raw VNĐ (nhân với 1000 khi save), hay lưu đúng số user nhập (ở đơn vị nghìn)?
- Báo cáo tổng hợp + tích hợp Journal Entry / Additional Salary dùng đơn vị gì? (Bắt buộc là VNĐ raw vì ERPNext core dùng VNĐ.)

**Default trong spec:** DB lưu **raw VNĐ**. Trên form có field `currency_unit_display` cho phép hiển thị ở dạng "1000 VNĐ" (client JS tự chia). Khi save → nhân lên raw VNĐ.

- **Trạng thái:** ⏳ Default applied
- **Câu trả lời:**
- **Người trả lời:**
- **Ngày:**

---

### Q10. File scan PDF đã ký — Đính kèm không?

Sau khi PAKD được duyệt qua hệ thống, thực tế sẽ in ra và ký tay 4-5 chữ ký.

**Câu hỏi:**
- Sau khi ký tay, bản scan PDF có cần **upload lên hệ thống** và link với PAKD gốc không?
- Có cần validate "chưa upload scan → không coi là hoàn tất"?

**Default trong spec:** Frappe `File` attachment có sẵn — cho phép upload nhưng không bắt buộc. Không có state "Signed Physical" riêng; PAKD coi là hoàn tất ngay khi approved trong hệ thống.

- **Trạng thái:** ⏳ Default applied
- **Câu trả lời:**
- **Người trả lời:**
- **Ngày:**

---

## Tracker tổng hợp

| # | Câu hỏi | Loại | Trạng thái | Deadline cần trả lời |
|---|---|---|---|---|
| Q1 | Commission rates cố định? | Blocking | ⏳ | Trước Sprint 1 |
| Q2 | Manager Services — sinh PE? | Non-blocking | Default | Trước go-live |
| Q3 | TK kế toán cho Add Costs | Blocking | ⏳ | Trước Sprint 1 |
| Q4 | Ai giữ các role duyệt | Blocking | ⏳ | Trước Sprint 2 (workflow) |
| Q5 | Rollup — thêm HĐ giữa chu kỳ | Blocking | ⏳ | Trước Sprint 1 |
| Q6 | Rounding mode pro-ration | Non-blocking | Default | Trước go-live |
| Q7 | Revision — thay thế hay cộng dồn | Blocking | ⏳ | Trước Sprint 1 |
| Q8 | Link hợp đồng — SO hay free-text | Blocking | ⏳ | Trước Sprint 1 |
| Q9 | Đơn vị hiển thị 1000 VNĐ | Non-blocking | Default | Trước go-live |
| Q10 | Đính kèm PDF scan | Non-blocking | Default | Trước go-live |

**Tổng:** 6 blocking + 4 non-blocking.

---

## New questions from architecture discussion (2026-04-09)

### Q11. Commission trigger = Payment Entry — confirm

**Decided (internal):** Commission is posted only when Payment Entry is submitted, not when PAKD is approved. "Cash in → commission out." Prepaid 12 months → all 12 months' commission posted at once into the same payroll_month.

**Confirm with kế toán:** Is there any scenario where commission should be accrued (recognized) before cash is received? (e.g., revenue recognition rules)

**Default:** Cash-basis only. No accrual-based commission recognition.

- **Trạng thái:** ✅ Answered (internal)
- **Ngày:** 2026-04-09

---

### Q12. Auto-invoice mode — confirm with kế toán

**Decided (internal):** PAKD Settings has `invoice_generation_mode` = Off / Draft / Auto Submit. Daily scheduler creates Sales Invoices for due accruals. Has `auto_submit_ceiling` safety brake.

**Confirm with kế toán:**
- Starting mode preference: Draft (safer) or Auto Submit (more automated)?
- What ceiling amount (if any) for auto-submit?
- Is there an existing invoicing workflow they want to preserve, or is this greenfield?

**Default:** Draft mode initially.

- **Trạng thái:** ✅ Answered (internal)
- **Ngày:** 2026-04-09

---

### Q13. Bad debt / Overdue — grace period

**Decided (internal):** Scheduler flips Invoiced accruals to Overdue after grace_period_days. Email alert to kế toán. Written Off = manual terminal state.

**Confirm with kế toán:**
- What grace period (days)? 15? 30? 60?
- Who receives overdue alerts? (P. Tổng hợp? Kế toán trưởng?)

**Default:** 15 days, alert to PAKD Accountant role.

- **Trạng thái:** ⏳ Need kế toán input
- **Ngày:** 2026-04-09

---

### Q14. Contract cancellation — Credit Note for Invoiced accruals?

When a recurring contract is cancelled and some accruals are already `Invoiced` (SI exists but unpaid):

**Confirm with kế toán:**
- System auto-creates Credit Note drafts for those SIs?
- Or kế toán handles manually with just an alert?

**Default:** Manual — system marks accrual `Cancelled`, shows alert.

- **Trạng thái:** ⏳ Need kế toán input
- **Ngày:** 2026-04-09

---

## Tracker tổng hợp (updated 2026-05-14)

| # | Câu hỏi | Loại | Trạng thái | Notes |
|---|---|---|---|---|
| Q1 | Commission rates cố định? | Blocking | ⏳ | Cần kế toán DCNET |
| Q2 | Manager Services — sinh PE? | Non-blocking | Default | |
| Q3 | TK kế toán cho Add Costs | Blocking | ⏳ → Q19 | Replaced by Q19 (semantic mới) |
| Q4 | Ai giữ các role duyệt | Blocking | ⏳ | Cần HR/BGĐ DCNET |
| Q5 | ~~Rollup — thêm HĐ giữa chu kỳ~~ | ~~Blocking~~ | ✅ Closed | Mẫu 02 BỎ 2026-05-14 |
| Q5b | Mẫu 02 = Monthly Activity confirm | Non-blocking | ✅ Closed | Mẫu 02 BỎ, Report thay |
| Q6 | Rounding mode pro-ration | Non-blocking | Default | |
| Q7 | ~~Revision — thay thế hay cộng dồn~~ | ~~Blocking~~ | ✅ Closed | Sub-table model |
| Q7b | Revision — chain model | ~~Non-blocking~~ | ✅ Closed | Đổi sang sub-table 2026-05-14 |
| Q8 | Link hợp đồng — SO hay free-text | Blocking | ✅ Closed | DCNET Contract + custom field SI/PE |
| Q9 | Đơn vị hiển thị 1000 VNĐ | Non-blocking | Default | |
| Q10 | Đính kèm PDF scan | Non-blocking | Default | |
| Q11 | Commission trigger = Payment Entry | Non-blocking | ✅ Internal | Cash-basis confirmed |
| Q12 | Auto-invoice mode | Non-blocking | ✅ Internal | Draft mode default |
| Q13 | Bad debt grace period | Non-blocking | ⏳ | Need kế toán input |
| Q14 | Cancellation Credit Note | Non-blocking | ⏳ | Need kế toán input |
| Q15 | One-off shadow SO requirement | Non-blocking | ✅ Updated | Per item_kind=One-off Goods + is_stock_item |
| Q16 | Contract workflow approval | Non-blocking | ⏳ | Cần BGĐ DCNET |
| Q17 | Contract Template count | Non-blocking | ⏳ | |
| Q18 | FTTH cá nhân | Blocking | ⏳ | DCNET không có FTTH HGD, chỉ B2B → can skip? |
| Q19 | (NEW) TK MS/AC/Referral cụ thể | Blocking | ⏳ | Sửa semantic D1; cần kế toán pick 6418 vs 6427, TNCN default |

**Blocking count: 4** (Q1, Q4, Q18, Q19). Q3 superseded by Q19. Q5/Q5b/Q7/Q7b/Q8 closed.

---

## New questions from 2026-04-09 discussion (architecture split)

### Q15. One-off contract có phải luôn cần shadow Sales Order?

**Decided (internal):** Shadow SO tạo tự động khi Contract `contract_type = One-off` AND có `items` với `is_stock_item = 1`. One-off service (consulting, không có vật tư) → không tạo shadow SO.

**Confirm với kế toán/kho vận:**
- DCNET có bán service One-off thuần (không vật tư) không? Ví dụ tư vấn, khảo sát.
- Thi công công trình có tính là "có vật tư" không (thực ra là mix dịch vụ + vật tư)?

**Default:** Mix cases → có shadow SO để tận dụng stock integration.

- **Trạng thái:** ⏳ Cần confirm
- **Ngày:** 2026-04-09

---

### Q16. Contract có cần workflow approval riêng không?

Contract có 2 lớp approval khả dĩ:
- (a) Contract Draft → Active cần chữ ký của BGĐ (contract là pháp nhân)
- (b) Contract chỉ cần active tự động, PAKD mới cần workflow (PAKD duyệt economics)

**Câu hỏi:** Hiện tại DCNET ký hợp đồng với khách trước hay ký PAKD trước? Contract document nào có chữ ký pháp lý?

**Default:** Contract có workflow đơn giản (Draft → Active) với chữ ký 1 cấp. PAKD workflow phức tạp hơn (3–5 cấp) cho economics.

- **Trạng thái:** ⏳ Cần confirm
- **Ngày:** 2026-04-09

---

### Q17. Module dcnet_contract có cần Contract Template cho print không?

Mục đích: in nhanh hợp đồng chuẩn theo mẫu công ty (thay cho Word template) từ thông tin đã nhập trong Contract.

**Câu hỏi:** DCNET hiện có bao nhiêu mẫu hợp đồng chuẩn? (theo service_type? theo branch? theo customer type?)

**Default:** 1 mẫu base + variation theo service_type.

- **Trạng thái:** ⏳ Cần confirm
- **Ngày:** 2026-04-09

---

### Q18. FTTH cá nhân có ký hợp đồng trên hệ thống không?

Với scale hàng chục ngàn subscriber/tháng:
- (a) Mỗi subscriber cá nhân tạo 1 DCNET Contract riêng?
- (b) Chỉ tạo Contract cho FTTH DN; FTTH cá nhân xử lý batch qua subscription system khác?
- (c) Tạo Contract aggregate theo NVKD theo tháng (batch)?

**Default:** (a) 1 Contract per subscriber — dùng bulk entry UI + import Excel để giảm friction.

- **Trạng thái:** ⏳ Quan trọng, blocking cho data volume sizing
- **Ngày:** 2026-04-09

---

## Next steps

1. **Write specs v3** — 2 specs mới/sửa:
   - `docs/specs/dcnet_contract.md` (NEW)
   - `docs/specs/dcnet_pakd.md` (REWRITE thin)
2. Create 2 GitHub repos following dual-remote pattern: `dcnet-cloud/dcnet-contract`, `dcnet-cloud/dcnet-pakd`
3. **Sprint A1 can start** for dcnet_contract with defaults — Contract DocType + Billing Schedule + state machine don't need confirmed accounts/rates
4. Confirm Q1/Q3/Q4/Q8/Q13/Q14/Q15/Q16/Q17/Q18 with kế toán + BGĐ DCNET before workflow-heavy sprints
5. Non-blocking questions → confirm before go-live

---

## Realignment 2026-05-14 decisions (D1-D8)

Brainstorm session 2026-05-14 rà soát mối tương quan Contract ↔ PAKD ↔ vn_accounting. Chốt 8 decisions để xử lý 5 phát hiện "khó hiểu, sai hoặc thừa" trong codebase v0.1.0. Chi tiết: `docs/specs/2026-05-14-contract-pakd-vnacc-realignment.md` ở bench-root.

| # | Decision | Closes |
|---|---|---|
| D1 | MS + AC = chi cho phía khách hàng (sửa semantic) | Open question (semantic mismatch) |
| D2 | 3 component giữ riêng: MS (định kỳ) / AC (định kỳ) / Referral (1 lần) | Open question (consolidation) |
| D3 | 1 PAKD = 1 Contract suốt đời; phụ lục = `PAKD Revision` child table | Q7/Q7b |
| D4 | Bỏ Mẫu 02 PAKD type; thay Report "PAKD phát sinh trong tháng" | Q5/Q5b |
| D5 | Custom field `dcnet_contract` + `billing_period_idx` trên SI/PE | Q8 (deeper) |
| D6 | MS/AC line có optional recipient + TNCN (JE 2-leg hoặc 3-leg) | Open question (TNCN) |
| D7 | Bi-directional navigation Contract/PAKD ↔ SI/PE | Open question (linkage) |
| D8 | HD hỗn hợp = 1 HD có items mix (Setup Fee + Recurring + One-off Goods) | BUSINESS_LOGIC §4.3 |

### Q19. (NEW 2026-05-14) TK cụ thể cho MS/AC/Referral

Realignment D1 sửa semantic MS/AC = "chi cho phía khách hàng" thay vì "phí quản lý nội bộ". Default đề xuất:

| Component | DR (chi phí) | CR (đối ứng) | TNCN nếu có recipient |
|---|---|---|---|
| Manager Services | 6418 hoặc 6427 | 3388 (no recipient) / 3388 net + 3335 (recipient) | 10%/20% |
| Add Costs | 6418 hoặc 6427 | 3388 / 3388 net + 3335 | 10%/20% |
| Referral | 6427 | 3388 / 3388 net + 3335 | 10%/20% |
| License Fee (GPVT) | 6425 | 3338 | — |
| Sales Commission (bypass HRMS) | 6421 | 334 (party=Employee) | qua salary slip |

**Câu hỏi cần kế toán DCNET xác nhận:**
- 6418 hay 6427 cho MS/AC/Referral? (TT99 cho phép cả hai — 6418 nghiêng về "dịch vụ mua ngoài", 6427 nghiêng về "chi phí khác bằng tiền")
- 3388 hay TK khác cho phải trả người ngoài DCNET?
- Default TNCN 10% (có MST) hay 20% (CCCD) — DCNET thực tế nhận chứng từ nào nhiều hơn?

- **Trạng thái:** ⏳ Cần kế toán DCNET pick
- **Ngày:** 2026-05-14
