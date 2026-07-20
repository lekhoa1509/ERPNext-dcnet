# Kiến trúc: dcnet_contract và dcnet_pakd

> Tài liệu nội bộ dev team DCNET. Mục tiêu: chốt chung context về hai app `dcnet_contract` và `dcnet_pakd` — **tại sao** tách đôi, **mô hình dữ liệu**, **luồng nghiệp vụ**, **thứ tự build**, và **hướng mở rộng**. Đọc tài liệu này trước khi đọc spec chi tiết hoặc touch code.

> **CẬP NHẬT 2026-05-14:** Tài liệu này đã được realign theo spec `docs/specs/2026-05-14-contract-pakd-vnacc-realignment.md` ở bench-root. 8 quyết định chốt:
> - D1: MS + AC = chi cho phía khách hàng (sửa semantic, không phải "phí quản lý nội bộ")
> - D2: 3 component khác bản chất giữ riêng — MS / AC / Referral
> - D3: **1 PAKD = 1 Contract suốt đời**; phụ lục là child table `PAKD Revision` bên trong PAKD (KHÔNG còn revision chain)
> - D4: **Bỏ Mẫu 02 PAKD type** — mỗi HD FTTH DN cũng là 1 PAKD riêng theo Mẫu 01; Mẫu 02 thay bằng Report "PAKD phát sinh trong tháng"
> - D5: Custom field `dcnet_contract` + `billing_period_idx` trên SI/PE (owned bởi dcnet_contract)
> - D6: MS/AC line có optional recipient + TNCN (JE 2-leg hoặc 3-leg tùy có recipient)
> - D7: Bi-directional navigation Contract/PAKD ↔ SI/PE
> - D8: **HD hỗn hợp = 1 HD có items mix** (Setup Fee + Recurring Service + One-off Goods) — không tách 2 HD nữa

## TL;DR

- `dcnet_contract` là app primitive sở hữu **hợp đồng + dòng tiền** (billing schedule, auto-invoice, payment tracking, overdue, revision chain).
- `dcnet_pakd` là app mỏng bolt-on, chỉ sở hữu **chính sách** (commission, chi phí ngoài, approval workflow, print format Mẫu 01/02/03).
- Hợp đồng recurring → Contract thuần. Hợp đồng one-off có vật tư → Contract + **shadow Sales Order** đọc-only để dùng lại hệ sinh thái kho của ERPNext.
- Commission theo **cash basis**: khách trả tiền đến đâu, commission post đến đó (HRMS Additional Salary + Journal Entry).
- Hai app, hai repo tách biệt. Contract xây trước, PAKD xây sau. PAKD declare Contract là dependency qua `pyproject.toml`.

## 1. Bối cảnh nghiệp vụ

DCNET là nhà cung cấp viễn thông + data center, có hai nhóm doanh thu chính:

| Nhóm | Ví dụ | Đặc điểm |
|---|---|---|
| **Recurring** | P2P, MPLS, ILL, FTTH doanh nghiệp, IT Managed | Ký 1 lần, phát hóa đơn 6/12/24 kỳ. Prepay hoặc Monthly. Có thể kèm phí lắp đặt. Toàn bộ là B2B — DCNET không kinh doanh FTTH hộ gia đình. |
| **One-off** | Bán VTTB, thi công công trình, dự án tư vấn | Phát hóa đơn một lần. Có hoặc không có vật tư đi kèm. |

Mỗi hợp đồng đều có một NVKD phụ trách. Theo quy chế DCNET, NVKD được hưởng commission theo **cash basis** — khách trả tiền mới tính. Ngoài commission, mỗi hợp đồng còn mang các khoản **chi phí ngoài**: Manager Services (phí quản lý đối tác), Add Costs (chi phí phát sinh), Phí quyền GPVT + quỹ CIVT — chảy vào các tài khoản chi phí không VAT.

Toàn bộ nghiệp vụ này hiện đang sống trong 3 file Excel "Phương Án Kinh Doanh" (Mẫu 01/02/03), maintain tay. Đây là thứ chúng ta đang số hóa.

### ERPNext core không đủ

ERPNext cung cấp sẵn Sales Order → Delivery Note → Sales Invoice → Payment Entry cho bán vật tư, HRMS Additional Salary cho commission payout, và Subscription (theo lý thuyết) cho recurring. Nhưng:

- **Subscription** không mô hình được prepay nhiều tháng, không có package term, không tách được setup fee, không có revision chain cho upgrade/downgrade. Kế thừa sẽ phải override ~80% hành vi.
- **Sales Order** phù hợp cho bán đứt có vật tư, nhưng không phải là "hợp đồng" — không có vòng đời dài hạn (Active/Suspended/Expired), không có billing schedule nhiều kỳ.
- **Không có khái niệm "Contract"** như một master tài liệu sống song song với SO, có vòng đời riêng và có thể tái dùng cho in ấn, SLA, portal khách hàng.

Chúng ta cần một primitive mới: `DCNET Contract`.

## 2. Vì sao phải tách đôi

Dồn mọi thứ vào một app duy nhất (ví dụ chỉ có `dcnet_pakd`) sẽ khiến một DocType phải gánh cả hai concern không liên quan:

**Concern A — Hợp đồng:** lifecycle Draft → Active → Suspended → Cancelled/Expired, billing schedule N kỳ, auto-invoice, payment tracking, overdue, revision chain, print format hợp đồng chuẩn.

**Concern B — Phương án kinh doanh:** lifecycle Draft → Review → Approved → Archived, tỷ lệ commission, chi phí ngoài, rule template, workflow phê duyệt, print format Mẫu 01/02/03.

Hai concern này khác nhau ở **5 chiều**:

1. **Vòng đời khác nhau.** Hợp đồng sống nhiều năm, có nhiều trạng thái. Phương án được phê duyệt một lần rồi đóng. Gộp state machine → ~10 trạng thái lai, rất dễ bug, rất khó review.
2. **Tính bất biến khác nhau.** Dữ liệu hợp đồng phải bất biến theo thời gian (audit — 3 năm sau vẫn phải đúng). Chính sách commission thì **sẽ thay đổi** theo năm (tỷ lệ theo dịch vụ, chi nhánh, cấp bậc). Trộn lẫn → mỗi lần đổi chính sách có nguy cơ động vào schema data lịch sử.
3. **Quan hệ N-1 với Mẫu 02.** PAKD Mẫu 02 (Monthly FTTH Rollup) là **một phương án tham chiếu nhiều hợp đồng FTTH nhỏ** trong một tháng — NVKD ký từng dòng. Nếu PAKD = Contract thì quan hệ N-1 này không mô hình nổi.
4. **Khả năng tái dùng.** Contract cần được tái dùng cho: in hợp đồng mẫu chuẩn, customer portal, SLA tracking, báo cáo công nợ, cảnh báo hết hạn. Tất cả không dính líu gì đến commission. Nếu Contract bị chôn bên dưới PAKD, mỗi use case mới đều phải refactor.
5. **Scope của chi phí ngoài khác scope hợp đồng.** Chi phí ngoài là chính sách thương lượng giữa DCNET với đối tác/khách trong một lần ký, không phải thuộc tính cốt lõi của hợp đồng. Nhốt chung khiến Contract schema phình theo mỗi loại chi phí mới.

Kết luận: tách thành hai app là bắt buộc để mỗi bên giữ được single responsibility.

## 3. Phân chia trách nhiệm (cập nhật 2026-05-14)

```
┌─────────────────────────────┐        ┌─────────────────────────────┐
│      dcnet_contract         │        │        dcnet_pakd           │
│   (primitive, reusable)     │        │     (thin, analytical)      │
├─────────────────────────────┤        ├─────────────────────────────┤
│ - DCNET Contract            │◄───────│ - Phuong An Kinh Doanh      │
│ - Contract Item (item_kind) │  ref   │   (1 PAKD/HD unique)        │
│ - Billing Schedule          │        │ - PAKD Item                 │
│ - Contract Addendum *NEW*   │◄───────│ - PAKD Revision *NEW*       │
│ - Contract Template         │        │   (ref Contract Addendum)   │
│                             │        │ - PAKD Beneficiary Line     │
│ Owns:                       │        │   *NEW unified MS+AC+Ref*   │
│ - Contract lifecycle        │        │ - PAKD Commission Line      │
│ - Billing schedule gen      │        │   (SC + License Fee only)   │
│   (per item_kind)           │        │ - Commission Rule Template  │
│ - Auto-invoice scheduler    │        │ - PAKD Settings             │
│ - Payment Entry hook + fire │        │ Owns:                       │
│   billing_period_paid event │        │ - Commission policy         │
│ - Overdue scheduler         │        │ - Commission calc + posting │
│ - Shadow SO sync (when item │        │ - Chi phía khách hàng       │
│   is One-off Goods +stock)  │        │   (MS/AC/Referral + TNCN)   │
│ - Custom field SI+PE:       │        │ - Approval workflow         │
│   dcnet_contract + period   │        │   (per revision)            │
│ - Contract print format     │        │ - Pivot xuyên revisions     │
│ - bi-directional nav links  │        │ - Mẫu 01/03 print format    │
│                             │        │   (Mẫu 02 → Report mới)     │
└─────────────────────────────┘        └─────────────────────────────┘
         ▲                                        │
         │ doc_event: billing_period_paid         │
         │  (contract, period_idx, pe_doc)        │
         └────────────────────────────────────────┘
                         (cash-in → commission-out)
```

Hai nguyên tắc vàng:

- **Contract sở hữu dòng tiền.** Mọi thứ liên quan đến cash — hóa đơn, nợ, thu, overdue — sống trong `dcnet_contract`.
- **PAKD sở hữu chính sách.** Tỷ lệ commission, chi phí ngoài, rule template, approval workflow. PAKD chỉ **đọc** dòng tiền từ Contract qua event, không sửa.

Không có hai master: một hợp đồng trong hệ thống = chính xác một `DCNET Contract`. PAKD link tới qua `contract_ref`, không sao chép dữ liệu.

## 4. Quyết định: Option D — Contract-first, shadow SO (cập nhật cho HD hỗn hợp 2026-05-14)

Với hợp đồng chỉ có items recurring service (không vật tư): **Contract thuần**. Không có Sales Order nào. Billing schedule sinh Sales Invoice trực tiếp.

Với hợp đồng có **ít nhất 1 item kind=One-off Goods** mà item đó có `is_stock_item=1`: **Contract + shadow Sales Order**. Khi Contract Activate, hook tự tạo một SO ẩn cho các item One-off Goods — user không thấy, không sửa được — làm cánh tay nối dài vào hệ thống kho ERPNext (Delivery Note, Stock Entry, Batch, Serial, tax template). Kế toán vẫn tạo DN + SI từ SO như bình thường. Sync 1 chiều Contract → SO qua doc_event, cascade delete khi Contract xoá.

**HD hỗn hợp:** 1 HD có thể có cả Setup Fee + Recurring Service + One-off Goods items cùng lúc. Shadow SO chỉ chứa item One-off Goods; Setup Fee + Recurring Service vẫn sinh BS row trực tiếp như recurring thuần. Mỗi item_kind có lifecycle billing riêng.

Hai phương án khác đã cân nhắc và loại:

| Option | Mô tả | Vì sao loại |
|---|---|---|
| **C — Pure sibling** | Contract tự implement lại DN/Stock Entry/tax, không đụng SO | Công việc khổng lồ, sẽ không bao giờ đồng bộ nổi khi ERPNext upgrade |
| **F — Rename SO + custom fields** | Đổi tên Sales Order thành "Hợp đồng", thêm custom field | Anti-pattern: breaks upgrade path (override core DocType), đổi tên không tự thêm semantics "vòng đời dài hạn" hay "revision chain", mỗi release ERPNext sẽ đụng conflict |
| **D — Shadow SO** ✅ | Contract là master, SO là cánh tay technical | UX sạch, hệ sinh thái ERPNext vẫn chạy, upgrade-safe |

Rủi ro duy nhất của Option D là **sync lệch giữa Contract và shadow SO**. Giảm thiểu bằng:

1. **SO permission-locked** — non-admin role không nhìn thấy shadow SO trong list view, không mở trực tiếp được. Chỉ hook của Contract có quyền ghi.
2. **Single source of truth** — mỗi field quan trọng chỉ có 1 hướng sync: Contract → SO. Không có sửa ngược.
3. **Cascade delete** — Contract xoá → shadow SO xoá theo → không bao giờ có SO mồ côi.
4. **Integration test bắt buộc** — mỗi lần đổi schema Contract phải chạy suite test đầy đủ chuỗi Contract → SO → DN → SI → PE.

Bounded, không phải vô hạn như Option C.

## 5. Quyết định: tách repo

Hai app nằm ở **hai repo riêng** trong GitHub org `dcnet-cloud`:

- `dcnet-cloud/dcnet-contract`
- `dcnet-cloud/dcnet-pakd`

`dcnet_pakd/pyproject.toml` declare:

```toml
dependencies = ["dcnet_contract>=0.1.0", ...]
```

Lý do tách repo (thay vì mono-repo một app có 2 module):

- **Independent release cycle.** Contract sẽ ít thay đổi sau khi stable, PAKD sẽ thay đổi mỗi lần DCNET tinh chỉnh chính sách commission. Tách repo = mỗi bên bump version riêng, không phải deploy kèm.
- **Quyền truy cập tách biệt.** Về sau nếu mở Contract cho đối tác/đại lý tích hợp (API, customer portal), có thể mở read-only repo Contract mà không lộ logic commission nội bộ.
- **Clear dependency direction.** `pyproject.toml` khai báo explicit: PAKD phụ thuộc Contract, Contract không biết gì về PAKD. Buộc dev không tạo vòng phụ thuộc ngược.
- **Upgrade path an toàn.** Khi Contract bump major version (ví dụ đổi schema Billing Schedule), PAKD bump theo ở lần release tiếp theo — lock bằng version range trong pyproject.

Chi phí tách repo: setup ban đầu mất thêm khoảng 1 ngày (2 repo, 2 CI, 2 pyproject). Đã accept.

## 6. Quyết định: 1 NVKD / 1 hợp đồng (cho v1)

Hiện tại quy chế DCNET quy định **mỗi hợp đồng có đúng 1 NVKD phụ trách** — hoa hồng không chia. Chúng ta giữ nguyên ràng buộc này trong v1:

- Contract field `sales_person` là Link đơn, không phải child table.
- PAKD field `sales_person` auto-fill từ Contract, read-only.
- Commission rule template chỉ cần tra cứu 1 chiều (service_type → rate), không cần split logic.

**Tại sao chốt 1 NVKD cho v1 (thay vì thiết kế sẵn cho co-sales):**

- YAGNI — DCNET chưa có chính sách co-sales. Thiết kế sẵn child table Sales Rep Split cho case không tồn tại sẽ tạo schema phức tạp không cần thiết, và PAKD commission calc phải handle tất cả edge case của việc chia tỷ lệ (ai ký PAKD? quorum? bất đồng?).
- Migration path rõ ràng — nếu sau này DCNET ra chính sách co-sales, việc chuyển từ "1 NVKD" sang "N NVKD với split" là một migration bounded: thêm child table `PAKD Sales Rep Split`, giữ field `sales_person` làm primary (default 100%), backfill data cũ. Không cần break Contract schema.
- Đơn giản hoá approval workflow — 1 NVKD nghĩa là 1 người ký phần NVKD trong workflow. Nhiều NVKD sẽ kéo theo quyết định "tất cả phải ký" hay "một người đại diện ký" — đó là discussion chính sách, không phải kỹ thuật.

Ràng buộc này chỉ liên quan PAKD. Contract về mặt data vẫn lưu field đơn; nếu co-sales xuất hiện, Contract không phải đổi, chỉ PAKD thêm layer split ở trên.

## 7. Quyết định: cash-basis commission, không hỗ trợ accrual (v1)

Commission chỉ được post **khi Payment Entry submit** (tức là khi billing_schedule row chuyển sang Paid). Không có trường hợp nào commission được post tại thời điểm Sales Invoice hay tại thời điểm billing schedule generation.

**Tại sao cash-basis cho v1:**

- **Khớp quy chế DCNET hiện tại.** Đây là cách công ty đang thực sự trả commission trong Excel — khách trả tiền mới tính lương KD. Nếu chúng ta tự ý hỗ trợ accrual, code sẽ expose một chế độ mà business không yêu cầu, dev sẽ phải duy trì logic không ai dùng.
- **Tránh bad debt ảnh hưởng commission.** Nếu post commission theo accrual (tại SI), khi khách không trả → phải reverse Additional Salary → phức tạp hoá HRMS payroll của tháng trước đó → kế toán không chịu. Cash-basis tự nhiên an toàn với bad debt: không trả = không commission.
- **Event model đơn giản.** Cash-basis nghĩa là commission lines chỉ lắng nghe **một** event: `contract_billing_period_paid`. Accrual sẽ thêm event thứ hai (`invoiced`) và logic reconcile giữa hai trạng thái, double logic.
- **Audit rõ ràng.** Mỗi commission line có một Payment Entry reference làm bằng chứng cash-in. Kế toán check ngược từ bảng lương về PE rất đơn giản.

**Điều quan trọng — không đóng cửa với accrual:** nếu sau này DCNET đổi chính sách (hiếm, nhưng có thể — ví dụ NVKD muốn được tạm ứng commission ngay khi ký hợp đồng prepay), việc thêm chế độ accrual chỉ cần:

1. Thêm listener thứ hai vào event `contract_billing_period_invoiced` (đã có sẵn từ flow invoice).
2. Thêm trạng thái `Advance` cho commission line (giữa Pending và Posted).
3. Thêm nút reverse khi bad debt.

Contract **không đổi dòng nào** — chỉ PAKD thêm code. Đây là lợi ích trực tiếp của việc tách đôi app: đổi policy không phải đụng primitive.

v1 không làm, nhưng kiến trúc không chặn.

## 8. Quyết định: sprint order — Contract xong hẳn, sau đó PAKD, không song song

Thứ tự build bắt buộc:

```
Sprint A1: DCNET Contract DocType + Billing Schedule + state machine
Sprint A2: Auto-invoice scheduler + Payment Entry hook + Overdue scheduler
Sprint A3: Shadow SO sync + permission lockdown (one-off goods flow)
Sprint A4: Revision chain + cancellation flow + print format
Sprint A5: Workspace + reports
─────────────────────── gate: Contract v0.1.0 released ───────────────────────
Sprint B1: Rule engine + golden tests (replay Excel formulas cell-by-cell)
Sprint B2: PAKD DocType + Commission Line + approval workflow
Sprint B3: Payment Entry event listener + commission posting (AS + JE)
Sprint B4: Print formats Mẫu 01/02/03 + workspace + reports
Sprint B5: Integration testing full chain
```

**Vì sao không song song A và B:**

- **PAKD phụ thuộc cứng vào Contract.** Toàn bộ commission flow của PAKD (B3) được kích bởi event từ Billing Schedule (A2). Nếu B bắt đầu trước khi A2 xong, B3 phải stub event ra, đến khi A2 ra thì phải rewrite logic — công làm lại.
- **Rule engine B1 cần data thật từ Contract.** Golden test replay Excel cần dataset contract thật để so kết quả. Không có Contract DocType thì không có dataset, không có golden test nghiêm túc.
- **Shadow SO sync (A3) là nơi rủi ro cao nhất.** Muốn biết shadow SO có stable không, phải chạy thực tế bán VTTB end-to-end. Nếu PAKD đã build trên Contract chưa stable, test fail ở A3 sẽ kéo theo fix cả PAKD.
- **Approval workflow (B2) phải biết Contract đã Active.** PAKD Approved xong cần đảm bảo Contract đã Active để sinh commission_lines matching các billing period. Luồng state này muốn test được thì Contract phải chạy trước.
- **Budget review tốt hơn.** Contract ra xong là một deliverable độc lập có value riêng (đã có thể quản lý hợp đồng, xuất hóa đơn, theo dõi payment). DCNET có thể dùng Contract trước trong khi PAKD đang build — không bị kẹt toàn bộ phase số hoá.

**Không song song, nhưng có thể overlap cuối sprint A:** B1 (rule engine + golden test) là thuần business logic không phụ thuộc Contract DocType. Có thể bắt đầu B1 song song từ **cuối A4** (khi Contract đã đủ stable để cung cấp test fixture). B2..B5 vẫn phải chờ A5 xong.

Gate chuyển từ A sang B: **Contract v0.1.0 released** nghĩa là A1..A5 đã merge, CI xanh, đã migrate và smoke test trên bench dcnet. Không có gate mềm.

## 9. Luồng cash-basis commission (reference flow)

```
1. Sales rep ký hợp đồng
   → Tạo DCNET Contract (Draft)
   → Điền package term, payment mode, unit price, setup fee
   → Submit → Active
   → Hook sinh billing_schedule: N dòng (month_index 0..N-1), state Projected

2. NVKD tạo PAKD cho hợp đồng này
   → PAKD.contract_ref = Contract
   → Chọn commission rule template
   → Điền chi phí ngoài (Manager Services, Add Costs, Phí GPVT)
   → Submit → approval workflow (Draft → TP → BGĐ → Approved)
   → Khi Approved: sinh commission_lines (1 per billing_period × component),
     state Pending

3. Đến kỳ billing (ví dụ tháng 1)
   → dcnet_contract scheduler chạy
   → billing_schedule row tháng 1: Projected → Invoiced
   → Sinh Sales Invoice tự động
   → (Nếu quá hạn: Invoiced → Overdue sau grace period)

4. Khách thanh toán
   → Kế toán tạo Payment Entry (reference đến SI)
   → PE submit → dcnet_contract hook:
     - billing_schedule row tháng 1: Invoiced → Paid
     - Fire event contract_billing_period_paid
   → dcnet_pakd listener bắt event:
     - Tìm commission_lines matching (contract, period)
     - Nếu PAKD.workflow_state == Approved: Pending → Eligible → Posted
       (xem §5 cho logic cutoff chọn payroll_month)
     - Nếu PAKD chưa Approved: Pending → Eligible pending approval
       (sẽ auto-post khi PAKD chuyển Approved, nếu vẫn còn trong cutoff)
   → Khi post:
     - Sales Commission → HRMS Additional Salary
     - Manager Services + Add Costs + Phí GPVT → Journal Entry (Draft,
       kế toán tự submit)

5. Cutoff ngày 5 (quy chế PAKD, không phải quy chế Payment)
   → Commission chỉ được post vào kỳ lương tháng N-1 nếu PAKD tương ứng
     đã Approved trước ngày 05/N.
   → Nếu PAKD Approved sau 05/N → commission post vào kỳ lương tháng N.
   → Implication state machine commission line:
       Pending   (PAKD chưa Approved)
       Eligible  (PAKD Approved + billing_schedule row Paid)
       Posted    (đã tạo Additional Salary / Journal Entry)
   → payroll_month được tính tại thời điểm chuyển Eligible → Posted:
       approved_at < 05 ngày tháng(payment_date) + 1  → payroll = tháng(payment)
       approved_at >= 05 ngày tháng(payment_date) + 1 → payroll = tháng kế tiếp

6. Prepay 12 tháng
   → 1 Payment Entry → 12 billing_schedule rows flip Paid cùng lúc
   → 12 commission_lines post cùng lúc
   → Gom thành 1 Additional Salary duy nhất
```

## 10. Edge case

| Edge case | Cách xử lý |
|---|---|
| **Hủy giữa chừng** | Contract → Cancelled. Future billing_schedule rows → Cancelled. Đã Paid → untouched. Commission_lines chưa Posted → Cancelled. |
| **Upgrade/downgrade** | Tạo Contract Revision (link tới Contract cha). Billing_schedule cũ đóng tại ngày revision. PAKD tạo revision mới, approve lại, sinh commission_lines mới cho future periods. |
| **Bad debt** | Billing_schedule stuck ở Overdue. PAKD hiện alert nhưng không Post commission. Khi kế toán Write Off → row chuyển Written Off, commission_line matching → Cancelled. |
| **Phí lắp đặt 1 lần trên hợp đồng recurring** | Lưu trong `setup_fee` field của Contract. Xuất hiện như month_index 0 trong billing_schedule. **Không phát sinh commission cho NVKD** và **không phát sinh chi phí ngoài** (Manager Services / Add Costs / Phí GPVT). Setup fee chảy thẳng vào doanh thu net. Rule template không có rate cho setup_fee. |
| **Mẫu 02 — FTTH rollup** | 1 PAKD references N Contracts (thường vài chục FTTH nhỏ trong tháng). Commission_lines sinh theo N × periods. Print format Mẫu 02 render dạng bảng danh sách hợp đồng, NVKD ký từng dòng. |
| **Multi-company** | Contract bắt buộc có `company` field từ đầu. Commission rule template có thể scope theo company. |

## 11. Hướng mở rộng tương lai

Tách đôi kiến trúc không chỉ để "đẹp code" — nó mở ra loạt use case mà thiết kế dồn-làm-một không hỗ trợ:

### 11.1 Ngắn hạn (3-6 tháng sau v1)

- **In hợp đồng mẫu chuẩn** — `DCNET Contract Template` + Jinja → xuất DOCX/PDF. Chỉ đụng Contract.
- **Báo cáo tồn đọng công nợ theo hợp đồng** — query `Billing Schedule` theo state Overdue. Kế toán đã xin.
- **KPI dashboard theo sales rep** — tổng contract active, doanh thu recurring đã ký, tỷ lệ Paid/Overdue. Query từ Contract, không cần PAKD.
- **Cảnh báo hết hạn** — scheduler đọc Contract.end_date, 30 ngày trước gửi email NVKD + khách. Hoàn toàn trong Contract.

### 11.2 Trung hạn (6-12 tháng)

- **Customer portal** — khách đăng nhập xem hợp đồng + hóa đơn + lịch sử thanh toán. Expose Contract + Billing Schedule với permission theo customer. Đây là lý do lớn nhất để Contract phải tái dùng được.
- **SLA tracking** — DocType `Contract SLA` link tới Contract, monitor uptime/response time. Bolt-on, Contract không đổi schema.
- **Commission policy đổi theo năm** — thêm `Commission Rule Template` mới với `valid_from`. Data hợp đồng cũ không đụng. Revision/commission cũ vẫn tính theo template tại thời điểm approve.
- **Co-sales (nhiều NVKD per contract)** — thêm child table `PAKD Sales Rep Split` trong PAKD. Contract không đổi.
- **Renewal flow** — sau khi Contract Expired, nút "Renew" tạo Contract mới từ template cũ, kéo theo PAKD mới. Khác với revision chain.

### 11.3 Dài hạn (năm thứ 2+)

- **API cho đại lý** — đại lý FTTH tự tạo Contract qua REST API, đi qua workflow duyệt DCNET. Contract đã là primitive độc lập nên expose API đơn giản.
- **Forecast dòng tiền** — feed Billing Schedule vào model dự báo cash flow. Data sạch vì schedule đã chuẩn hoá state machine.
- **Chuyển sang accrual commission** — chỉ cần thêm listener thứ hai vào event `billing_schedule.invoiced`. Contract không đổi một dòng nào. (Xem §7.)
- **Tách PAKD cho từng policy set khác nhau** — nếu DCNET muốn bán app này cho công ty con hoặc đối tác, mỗi bên có PAKD policy riêng chia sẻ cùng `dcnet_contract` base. Split repo đã hỗ trợ chuyện này.

## 12. FAQ

**Q: Tách đôi có làm chậm dev không?**
Ngắn hạn: chậm hơn 1-2 ngày setup. Trung hạn: nhanh hơn đáng kể vì mỗi khi chính sách commission đổi hoặc UX Contract đổi, chỉ sửa một bên. Sau vài lần đổi, chi phí setup đã hoàn vốn.

**Q: Tại sao không dùng ERPNext Subscription cho recurring?**
Đã trả lời ở §1 — Subscription không mô hình được prepay, package term, setup fee tách biệt, revision chain. Override 80% sẽ đắt hơn viết mới.

**Q: Shadow SO có phức tạp không? Rủi ro gì?**
Đã trả lời ở §4 — rủi ro sync lệch là bounded, mitigate bằng 4 biện pháp (permission lock, single source of truth, cascade delete, integration test). Không phải vô hạn như Option C.

**Q: Mẫu 01/03 Excel khác nhau. Một PAKD DocType có cover cả 2 được không?**
Có. Enum `pakd_type` (Recurring Telecom / One-off Sale) quyết định print format nào render. Approval workflow và commission calc dùng chung. **Mẫu 02 đã bị bỏ 2026-05-14** — thay bằng Report "PAKD phát sinh trong tháng" có print format ký từng dòng.

**Q: Vì sao PAKD không phải là child table của Contract?**
Vì PAKD có vòng đời và approval workflow độc lập. Một Contract có thể có 0 PAKD (chưa trình) hoặc 1 PAKD (sau realignment 2026-05-14: unique constraint). Child table không mô hình nổi vòng đời độc lập với approval chain. Phụ lục HD nay được mô hình trong PAKD Revision child table BÊN TRONG 1 PAKD parent, không tạo PAKD mới.

**Q: Commission rule template nên nằm trong Contract hay PAKD?**
PAKD. Template là chính sách DCNET, không phải thuộc tính hợp đồng. Nhiều hợp đồng dùng chung template. Khi DCNET đổi tỷ lệ, tạo template mới với `valid_from` — hợp đồng cũ vẫn trỏ tới template cũ (immutable by version).

**Q: Làm sao chắc dev khác không tự tạo shadow SO tay?**
Permission lockdown ở `permission_query_conditions` cho non-admin role + comment rõ ở entry point hook + tài liệu này. Shadow SO không xuất hiện trong list view bình thường. Không có magic, phải trust dev đọc doc.

**Q: Nếu Contract cần break schema (major version), PAKD có bị vỡ không?**
PAKD pin version range của Contract trong `pyproject.toml`. Contract bump major → PAKD bump ở release tiếp theo, CI chặn nếu version không tương thích. Đây là lợi ích trực tiếp của việc tách repo + khai báo dependency tường minh.
