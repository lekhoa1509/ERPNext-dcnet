# Business Logic — DCNET PAKD

PAKD = "Phương Án Kinh Doanh" — công cụ duyệt phương án và tính hoa hồng nhân viên kinh doanh (NVKD) của DCNET.

> Tài liệu này là **nghiệp vụ thuần tuý** — dành cho Giám đốc Kinh doanh, Kế toán trưởng, Ban Giám đốc đọc để xác nhận "đúng nghiệp vụ chưa". Không chứa mô tả kỹ thuật (DocType, field, code). Chi tiết kỹ thuật nằm ở spec `docs/specs/dcnet_pakd-v3.md`.

---

## 1. Bối cảnh và mục đích

DCNET là nhà cung cấp dịch vụ viễn thông và data center, có hai nhóm doanh thu chính:

- **Recurring (định kỳ):** P2P, MPLS, ILL, FTTH doanh nghiệp, IT Managed Services, FTTH hộ gia đình (HGD). Ký một lần, phát hóa đơn theo nhiều kỳ (6/12/24 tháng), trả trước nhiều tháng hoặc hằng tháng.
- **One-off (một lần):** Bán vật tư thiết bị (VTTB), thi công công trình, dự án tư vấn. Phát hóa đơn một lần.

Mỗi hợp đồng đều có một NVKD phụ trách. Theo quy chế DCNET, NVKD được hưởng hoa hồng theo **cơ sở tiền mặt (cash basis)** — khách trả tiền đến đâu, hoa hồng tính đến đó. Ngoài hoa hồng cho NVKD, mỗi hợp đồng còn mang các khoản **chi cho người ngoài DCNET** (đổi mô tả 2026-05-14 cho khớp Excel mẫu thực):

- **Manager Services (MS):** chi cho 1 người/nhóm trong nội bộ khách hàng đã chịu trách nhiệm cho phép chốt hợp đồng (vd: quản lý IT, trưởng phòng vận hành phía khách). Trả định kỳ theo billing period. Ghi chú trong Excel: *"Chi phí hoa hồng cho khách hàng"*.
- **Add Costs (AC):** chi cho nhóm khác phía khách hàng liên quan đến phần khách kê thêm vào giá HD (vd: kế toán/lãnh đạo phía khách duyệt nâng giá). Trả định kỳ theo billing period. Ghi chú trong Excel: *"Chi phí Khách hàng nâng thêm"*.
- **Referral (External Commission):** chi 1 lần cho người giới thiệu hợp đồng (có thể trong hoặc ngoài khách hàng). Phải khai thuế TNCN tại nguồn nếu trả cá nhân đích danh.
- **Phí GPVT:** phí quyền sử dụng giấy phép viễn thông DCNET phải nộp NN (chỉ áp dụng cho dịch vụ viễn thông định kỳ, tỷ lệ ~2.2%). Hạch toán TK 6425 / 3338 tạm giữ.

Cả MS, AC, Referral đều có thể có hoặc không có **người nhận đích danh** (CCCD/MST) tùy từng case. Khi có đích danh → cần khấu trừ TNCN tại nguồn (10% nếu có MST, 20% nếu chỉ CCCD).

Toàn bộ nghiệp vụ này hiện đang được duy trì thủ công qua hai mẫu Excel: **Mẫu 01** (hợp đồng dịch vụ định kỳ) và **Mẫu 03** (hợp đồng one-off / bán thiết bị / thi công). App `dcnet_pakd` số hóa các mẫu này và tự động hóa việc hạch toán.

> **Bỏ Mẫu 02** (FTTH DN rollup hàng tháng) theo decision 2026-05-14 — mỗi HD FTTH DN cũng là 1 PAKD riêng theo Mẫu 01. Mẫu 02 thay bằng Report "PAKD phát sinh trong tháng" để in cho quản lý ký.

### Vì sao cần một app riêng

ERPNext + `vn_accounting` + `dcnet_contract` đã đáp ứng được gần hết các nhu cầu kế toán, bán hàng, quản lý hợp đồng. Chỉ còn **một nghiệp vụ đặc thù của DCNET chưa có công cụ**: bảng tính commission + quy trình duyệt phương án. Đây là lý do `dcnet_pakd` tồn tại.

### Ranh giới với `dcnet_contract`

DCNET đã có app `dcnet_contract` quản lý vòng đời hợp đồng và dòng tiền (billing schedule, auto-invoice, thu tiền, công nợ quá hạn). PAKD là **lớp mỏng** bên trên Contract:

- Contract sở hữu **dòng tiền**: ai trả, trả bao nhiêu, khi nào, còn nợ bao nhiêu.
- PAKD sở hữu **chính sách**: phương án này hoa hồng bao nhiêu, chi phí ngoài như thế nào, ai duyệt.
- PAKD chỉ **đọc** dữ liệu dòng tiền từ Contract, không sửa.

---

## 2. Phạm vi nghiệp vụ

### Trong phạm vi

- Bảng tính phương án (worksheet) với các công thức tính doanh thu, chi phí, lãi gộp, hoa hồng
- Quy trình duyệt phương án qua nhiều cấp (sales rep → trưởng phòng → P. Tổng hợp → GĐ chi nhánh → BGĐ)
- Hạch toán hoa hồng khi khách đã thanh toán (cash-basis)
- Hạch toán các khoản chi phí ngoài (MS, AC, Phí GPVT) qua Bút toán nhật ký ở trạng thái **Nháp** để kế toán rà soát
- Tạo Bổ sung lương (Additional Salary) cho phần "Lương KD" để nhập vào bảng lương hằng tháng
- Quy tắc chốt kỳ (cutoff) theo ngày khách trả tiền
- In ba biểu mẫu: Mẫu 01, Mẫu 02, Mẫu 03
- Cấu hình tỷ lệ hoa hồng theo loại dịch vụ / chi nhánh
- Phân quyền theo vai trò (7 vai trò: 6 cấp duyệt + Kế toán)

### Ngoài phạm vi

- Sinh hóa đơn tự động — thuộc `dcnet_contract`
- Quản lý billing schedule — thuộc `dcnet_contract`
- Quản lý vòng đời hợp đồng, gia hạn, chấm dứt — thuộc `dcnet_contract`
- Tích hợp trực tiếp với module chấm công / timekeeping
- Đa ngoại tệ — chỉ xử lý VND
- Import dữ liệu PAKD lịch sử từ Excel
- Co-sales (chia hoa hồng giữa nhiều NVKD) — mỗi hợp đồng chỉ có một NVKD
- Clawback (truy thu hoa hồng) tự động — xử lý thủ công

---

## 3. Vai trò và người dùng

| Vai trò | Trách nhiệm |
|---|---|
| **NVKD (Sales Rep)** | Tạo PAKD cho phương án mới; nhập dữ liệu bảng tính; gửi đi duyệt |
| **Giám đốc Trung tâm Kinh doanh (HCM / HN)** | Duyệt cấp đầu tiên — kiểm tra giá bán, chi phí, phương án có hợp lý không |
| **Phòng Tổng hợp** | Duyệt cấp hai — kiểm tra công thức hoa hồng, khớp quy chế, định tuyến lên cấp tiếp theo |
| **Giám đốc Chi nhánh HN** | Duyệt PAKD phát sinh ở chi nhánh HN (cấp ba khi cần) |
| **Ban Giám đốc** | Duyệt cuối cùng cho phương án có giá trị lớn hoặc cần BGĐ quyết |
| **Kế toán (PAKD Accountant)** | Rà soát và submit các Bút toán nhật ký liên quan chi phí ngoài; xử lý hoa hồng vào bảng lương; xử lý tình huống ngoại lệ (hợp đồng chấm dứt sớm, PE bị hủy) |
| **Admin hệ thống** | Cấu hình tỷ lệ hoa hồng, tài khoản kế toán mặc định, ngày chốt kỳ |

Phân quyền theo chi nhánh (HCM / HN) để đảm bảo GĐ chi nhánh chỉ thấy phương án của chi nhánh mình.

---

## 4. Hai loại PAKD (đổi 2026-05-14 — bỏ Mẫu 02)

Mỗi PAKD thuộc một trong **hai** loại, phản ánh hai mẫu Excel còn dùng. Loại được chọn tại thời điểm tạo PAKD và không đổi trong suốt vòng đời.

### 4.1 Recurring Telecom (tương ứng Mẫu 01)

- **Áp dụng cho:** hợp đồng có item Recurring Service (P2P, MPLS, ILL, FTTH DN, IT Managed) hoặc hợp đồng hỗn hợp (Recurring + Setup Fee + One-off Goods cùng lúc).
- **Đặc điểm:** một phương án cho một hợp đồng (1 PAKD = 1 HD, suốt đời); cước hằng tháng/quý theo `payment_mode` của từng item; có thể kèm phí lắp đặt + bán thiết bị 1 lần.
- **Cách tính hoa hồng NVKD:** theo bộ quy tắc (rule template) — tỷ lệ % trên cước định kỳ, áp dụng cho từng kỳ thanh toán. Phí lắp đặt không tính hoa hồng.
- **Chi cho phía khách:** MS + AC (Beneficiary Lines), recurrence = Per Period; tùy chọn Referral 1 lần.
- **Phí GPVT:** 2.2% (chỉ khi `service_type` là dịch vụ viễn thông).

### 4.2 One-off Sale / Project (tương ứng Mẫu 03)

- **Áp dụng cho:** hợp đồng chỉ có item One-off Goods (bán VTTB, thi công công trình, dự án tư vấn 1 lần).
- **Đặc điểm:** nhiều hạng mục trong một phương án; mỗi hạng mục có số lượng × đơn giá; có thể có vật tư + dịch vụ hỗn hợp.
- **Cách tính hoa hồng NVKD:** theo bộ quy tắc — tỷ lệ % trên doanh thu, có thể áp dụng sàn/trần.
- **Chi cho phía khách:** MS + AC (Beneficiary Lines), recurrence = One-off (vì chỉ có 1 kỳ billing); tùy chọn Referral.
- **Không có Phí GPVT.**

### 4.3 ~~Monthly FTTH Rollup~~ (BỎ 2026-05-14)

Mẫu 02 trước đây là "1 PAKD gom N hợp đồng FTTH DN trong 1 tháng". Sau realignment, **mỗi HD FTTH DN cũng là 1 PAKD riêng theo Mẫu 01** — không còn rollup.

Mẫu 02 print form thay bằng **Report "PAKD phát sinh trong tháng"** (Script Report mới): filter month/year/branch, list các PAKD đã tạo, có print format chỗ ký từng dòng để quản lý duyệt — giữ được nghi thức ký tay hàng tháng mà không cần DocType riêng.

Vì NVKD FTTH DN có thể có 30-50 HD/tháng → wizard "Tạo PAKD hàng loạt" sẽ là task riêng trong roadmap để bulk-create PAKD draft từ list Contract.

---

## 5. Quy tắc nghiệp vụ chính

### 5.1 Bảng tính phương án (Worksheet)

Mỗi PAKD có một bảng hạng mục (PAKD Items) + một bảng Beneficiary Lines + một bảng Revisions:

- **PAKD Items** (auto-sync từ DCNET Contract Items): mô tả hạng mục, đơn vị, số lượng, đơn giá, đơn giá Add Costs (nếu có), doanh thu hợp đồng.
- **PAKD Beneficiary Lines** (mới 2026-05-14): mỗi dòng = 1 thành phần chi cho người ngoài DCNET (MS/AC/Referral) với optional recipient info + TNCN.
- **PAKD Revisions** (mới 2026-05-14): mỗi dòng = 1 phụ lục HD áp dụng cho PAKD này, có snapshot rate + workflow state riêng.

NVKD **chỉ nhập input** (đơn giá, số lượng, đơn giá AC, tỷ lệ override nếu khác mẫu). Các trường còn lại (tổng MS, AC, Phí GPVT, Lương KD, total_cost, doanh thu dịch vụ) là **kết quả tính từ server** — không cho sửa tay.

> Nguyên tắc: **server là nguồn sự thật duy nhất** cho mọi công thức tài chính. Không có engine công thức ở phía client song song với server.

Kế hoạch tổng (header) có các tổng số tự động: tổng doanh thu hợp đồng, tổng Add Costs, tổng Manager Services, tổng Phí GPVT, tổng Referral, tổng Lương KD, tổng chi phí, doanh thu dịch vụ.

### 5.2 Rule engine — cấu hình tỷ lệ hoa hồng

Admin cấu hình các **mẫu quy tắc (Commission Rule Template)** nêu rõ: với loại dịch vụ X, chi nhánh Y, loại PAKD Z, thì tỷ lệ MS / AC / Phí GPVT / Lương KD là bao nhiêu, áp dụng trên cơ sở nào (trên đơn giá, trên đơn giá trừ AC, trên AC gross, trên doanh thu thực tế).

**Thứ tự tìm template áp dụng cho một PAKD cụ thể (4 tầng):**

1. Quy tắc ghi đè trực tiếp trên Contract (nếu có)
2. Quy tắc khớp đồng thời chi nhánh + loại dịch vụ
3. Quy tắc khớp loại dịch vụ (không ràng buộc chi nhánh)
4. Quy tắc mặc định theo loại PAKD

Nếu không tìm thấy template nào khớp → hệ thống báo lỗi, yêu cầu kế toán tạo template trước. PAKD không lưu được.

**Ngày hiệu lực:** mỗi template có `valid_from` và `valid_to`. Khi đổi tỷ lệ hoa hồng, tạo template mới với ngày hiệu lực tương lai — các PAKD lịch sử vẫn giữ nguyên tỷ lệ cũ của kỳ đã duyệt.

Khi PAKD có phụ lục (PAKD Revision child row), rate có thể đổi cho revision đó — engine lookup revision active tại kỳ T (effective_from ≤ period_start ≤ revision tiếp theo) để biết rate nào áp dụng cho commission line / beneficiary line của kỳ đó.

### 5.3 Workflow duyệt phương án

Gồm 7 trạng thái và 4 tuyến duyệt (HCM-NV, HCM-BGĐ, HN-NV, HN-BGĐ tùy theo channel NVKD hay BGĐ khởi tạo):

1. **Draft (Nháp):** NVKD soạn. Chỉ NVKD và admin thấy.
2. **Pending GĐ TT KD:** chờ Giám đốc Trung tâm Kinh doanh duyệt (HCM hoặc HN tùy chi nhánh)
3. **Pending P. Tổng hợp:** chờ Phòng Tổng hợp rà soát
4. **Pending GĐ CN:** chờ GĐ Chi nhánh (HN) — chỉ với PAKD HN
5. **Pending BGĐ:** chờ Ban Giám đốc duyệt cuối
6. **Approved (Đã duyệt):** phương án sẵn sàng áp dụng; các dòng hoa hồng (commission line) được sinh ra ở trạng thái "Pending" (chờ khách trả tiền)
7. **Rejected (Từ chối):** có lý do; cho phép NVKD sửa và gửi lại (quay về Draft)

Một PAKD có thể mở lại từ Rejected về Draft để sửa và duyệt lại. Khi bị Reject, các commission line từ lần duyệt trước (nếu có) sẽ bị Cancelled.

### 5.4 Liên kết với Contract — 1 PAKD = 1 Contract suốt đời (đổi 2026-05-14)

- Một PAKD luôn tham chiếu đến **một Contract duy nhất** (qua `contract_ref`). Unique constraint per Contract — KHÔNG tạo PAKD thứ 2 cho cùng 1 Contract.
- Khi Contract có phụ lục → thêm 1 row vào `PAKD Revisions` child table của PAKD đang sống (KHÔNG tạo PAKD mới). Mỗi revision có workflow approval chain riêng.
- Bỏ "Monthly FTTH Rollup" — mỗi HD FTTH DN cũng có PAKD riêng theo Mẫu 01.

Thông tin khách hàng, NVKD, chi nhánh, loại dịch vụ được **kéo tự động** từ Contract — không cho sửa tay trong PAKD để tránh lệch dữ liệu.

Khi Contract ở trạng thái Active, form Contract hiển thị nút "Tạo PAKD" để tạo phương án đã điền sẵn thông tin.

### 5.4b Bi-directional navigation (mới 2026-05-14)

Form PAKD hiển thị section "Hóa đơn & Thanh toán" — bảng tích hợp các SI + PE thuộc Contract:
- Mỗi kỳ billing: hóa đơn (link SI), trạng thái thu, phiếu thu (link PE), trạng thái commission/beneficiary của kỳ.
- Click → mở SI/PE trong tab mới.

Ngược lại, SI/PE có 2 custom field `dcnet_contract` + `billing_period_idx` cho phép kế toán mở SI/PE thấy ngay Contract + kỳ → suy ra PAKD.

### 5.5 Chu trình hoa hồng theo cash-basis (CRITICAL)

Đây là quy tắc cốt lõi. Hoa hồng **chỉ được hạch toán khi khách đã thực trả tiền**, không phải khi xuất hóa đơn.

**Chu trình đầy đủ:**

1. Contract được kích hoạt → billing schedule được sinh (bên Contract quản lý)
2. PAKD được tạo tham chiếu đến Contract → đi qua workflow duyệt
3. PAKD được Approved → các commission line được sinh ra (mỗi kỳ thanh toán × mỗi thành phần chi phí = 1 dòng), tất cả ở trạng thái **Pending**
4. Kế toán ghi nhận Payment Entry (khách trả tiền) → billing schedule bên Contract chuyển kỳ đó sang **Paid**
5. Cùng sự kiện đó trigger PAKD: tìm các commission_line + beneficiary_line tương ứng với kỳ vừa được thanh toán → chuyển sang **Posted**:
   - **Lương KD (Sales Commission)** → tạo một Bổ sung lương (Additional Salary) cho NVKD, cộng dồn các kỳ vừa được thanh toán trong cùng event
   - **Phí GPVT (License Fee)** → tạo một Bút toán nhật ký Nháp: DR 6425 / CR 3338 (tạm giữ chờ nộp NN), kế toán rà soát rồi submit
   - **Manager Services / Add Costs / Referral (Beneficiary Lines)** → mỗi dòng tạo bút toán Nháp:
     - **Không có recipient đích danh** → JE 2-leg: DR TK chi phí / CR 3388 phải trả khác
     - **Có recipient + MST/CCCD** → JE 3-leg: DR TK chi phí gross / CR 3388 net (gốc − TNCN) / CR 3335 TNCN tạm giữ
   - Engine ưu tiên revision active tại kỳ T (effective_from ≤ period_start) để áp tỷ lệ chính xác

**Trường hợp trả trước nhiều tháng (prepay 12 tháng):**
- Một Payment Entry → tất cả 12 kỳ billing schedule chuyển sang Paid cùng lúc → tất cả 12 commission line + beneficiary line chuyển sang Posted → **một Additional Salary gom cả 12 kỳ** cho Sales Commission, hạch toán vào tháng lương tương ứng với ngày trả tiền (xem quy tắc cutoff ở 5.7).

> Nguyên tắc: **"Tiền vào → hoa hồng ra"**. Không trả hoa hồng dựa trên hóa đơn đã xuất mà khách chưa trả.

### 5.6 Bút toán hoa hồng + chi phí (TT99/2025, đổi 2026-05-14)

**Phí GPVT (License Fee) — JE 2-leg Nháp:**

- DR 6425 (Chi phí khác bằng tiền bộ phận bán hàng)
- CR 3338 (Phí, lệ phí và các khoản phải nộp NN khác — tạm giữ chờ nộp)

**Manager Services / Add Costs / Referral (Beneficiary Lines):**

Mỗi dòng có 2 dạng JE Nháp tùy theo có người nhận đích danh hay không:

| Có recipient + TNCN_pct > 0 | Không có recipient |
|---|---|
| DR `account_<kind>` gross (vd 6418/6427) | DR `account_<kind>` amount |
| CR `account_<kind>_payable` net (3388) | CR 3388 amount |
| CR 3335 (Thuế TNCN tạm giữ) pit | (chỉ 2 leg) |

`<kind>` ∈ {Manager Services, Add Costs, Referral}. Tỷ lệ TNCN mặc định 10% nếu có MST, 20% nếu chỉ CCCD. Tất cả tài khoản đều cấu hình qua PAKD Settings.

**Lương KD (Sales Commission, qua Additional Salary):**

- Additional Salary với thành phần "Lương kinh doanh" (tên thành phần lương cấu hình được)
- NVKD = sales_person trên PAKD
- Số tiền = tổng Lương KD của các commission line đang được post trong lần thanh toán này
- `payroll_date` = ngày cuối của tháng chốt (payroll_month) theo quy tắc cutoff

Khi Additional Salary được nhập vào Payroll Entry và Salary Slip, bút toán lương sẽ được ERPNext/HRMS tự sinh:
- DR 6421 (Chi phí nhân viên bán hàng)
- CR 334 (Phải trả người lao động)

Hoa hồng là thu nhập chịu thuế TNCN — xử lý theo module Payroll chuẩn (qua salary slip TNCN withholding).

> **Lưu ý:** Bypass HRMS mode (`use_hrms_for_commission=0`) sinh JE party=Employee thay vì Additional Salary — không qua bảng lương, hạch toán trực tiếp DR 6421 / CR 334.

### 5.7 Quy tắc chốt kỳ (cutoff)

Xác định hoa hồng thuộc tháng lương nào dựa vào **ngày khách trả tiền** (`posting_date` của Payment Entry):

- Nếu ngày trả tiền ≤ ngày cutoff (mặc định ngày 5) → hoa hồng thuộc **tháng trước**
- Ngược lại → hoa hồng thuộc **tháng hiện tại** của ngày trả

Ví dụ với cutoff = 5:
- PE ngày 3/6 → thuộc tháng lương 5
- PE ngày 5/6 → vẫn thuộc tháng 5 (ngày 5 là biên, tính tháng trước)
- PE ngày 6/6 → thuộc tháng 6

Ngày cutoff cấu hình được. Nguyên tắc: **payment month = commission month**, không có xử lý đặc biệt ở biên năm tài chính. "Lương thưởng tháng nào trả thì hạch toán vào tháng đó."

### 5.8 Tình huống ngược: Payment Entry bị hủy

Khi một Payment Entry đã submit bị cancel:

1. Bên Contract: các kỳ billing schedule liên quan chuyển từ **Paid** về **Invoiced**
2. Bên PAKD: các commission line tương ứng với PE đó chuyển từ **Posted** về **Cancelled**
3. Additional Salary liên quan:
   - Nếu AS **chưa nằm trong Payroll Entry đã duyệt** → hệ thống tự cancel AS
   - Nếu AS **đã nằm trong Payroll Entry đã duyệt** → không tự động đảo bút toán. Hệ thống hiển thị cảnh báo cho kế toán "AS đã nằm trong bảng lương đã duyệt, cần điều chỉnh thủ công"
4. Bút toán nhật ký (MS/AC/GPVT) liên quan:
   - Nếu còn Draft → tự cancel
   - Nếu đã submit → cảnh báo kế toán xử lý thủ công

Việc cancel PE **không bị chặn** — chỉ có cảnh báo.

### 5.9 Tình huống ngược: Contract chấm dứt sớm

Khi Contract bị Cancelled:

1. Các commission line + beneficiary line **đang Pending** (chưa được post vì khách chưa trả) → chuyển sang **Cancelled**
2. Các commission line + beneficiary line **đã Posted** (đã chi trả) → **không tự động đảo**. Kế toán xử lý thủ công nếu cần clawback.

Nếu có hóa đơn đã xuất nhưng khách chưa trả (SI ở trạng thái Invoiced): hệ thống báo cho kế toán để quyết định có lập Hóa đơn điều chỉnh (Credit Note) hay không — xử lý thủ công, không tự tạo CN.

### 5.10 In biểu mẫu (đổi 2026-05-14 — bỏ Mẫu 02)

Hai biểu mẫu dạng PDF/HTML (có thể xuất Word):

- **Mẫu 01 — Phương án kinh doanh (Recurring Telecom):** tờ trình phương án cho hợp đồng dịch vụ định kỳ, dùng đưa đi duyệt các cấp
- **Mẫu 03 — Phương án dự án / bán thiết bị:** tờ trình phương án cho hợp đồng one-off

Mỗi mẫu thích nghi theo items của hợp đồng — nếu hợp đồng có cả Recurring + One-off Goods + Setup Fee, mẫu in sẽ hiện cả 3 section.

Cộng thêm **Report mới** `PAKD phát sinh trong tháng` (thay cho Mẫu 02 cũ): filter month/year/branch, list các PAKD đã tạo, print format có chỗ ký từng dòng cho quản lý duyệt — giữ nghi thức tháng của Mẫu 02 cũ.

---

## 6. Edge cases nghiệp vụ

Các tình huống đặc thù cần xử lý rõ (đã được rà soát trong quá trình thiết kế):

- **PAKD đã duyệt nhưng sau đó Contract bị cancel:** hệ thống ngăn tiếp tục advance workflow. Nếu đã Approved rồi, các commission/beneficiary line Pending → Cancelled (xem 5.9).
- **Hợp đồng ký giá khác với PAKD đã duyệt:** thêm PAKD Revision child row tham chiếu Contract Addendum tương ứng, đi qua duyệt riêng cho revision đó. PAKD parent vẫn sống, không tạo mới.
- **Khách trả một phần hóa đơn (partial payment):** hệ thống chỉ flip kỳ sang Paid khi hóa đơn được thanh toán đầy đủ. Commission line vẫn Pending, không hạch toán một phần.
- **Hóa đơn nhiều Contract được gom một PE:** mỗi hóa đơn được xử lý độc lập — tìm Contract của hóa đơn (qua custom field `dcnet_contract`) → tìm PAKD tương ứng → post commission line. Không bị lẫn lộn giữa các Contract.
- **NVKD nghỉ việc:** hoa hồng tồn đọng Pending → xử lý theo chính sách nhân sự (thường clawback hoặc giữ để trả khi quyết toán). Hoa hồng đã Posted không bị tác động.
- **NVKD chuyển phòng/chi nhánh:** PAKD vẫn thuộc về NVKD ban đầu (sales_person fix); chỉ HD mới tính theo phân công mới.
- **Hợp đồng dài nhiều năm có nhiều phụ lục:** hoa hồng tính theo toàn bộ vòng đời hợp đồng + tất cả phụ lục đã approved. Engine lookup revision active tại kỳ T để áp tỷ lệ chính xác. Pivot view hiển thị xuyên suốt revisions.
- **Hai PAKD cho cùng một Contract:** không hợp lệ. Hệ thống ràng buộc unique constraint trên `contract_ref`.
- **Không tìm thấy rule template khớp:** báo lỗi rõ ràng, yêu cầu kế toán tạo template trước. PAKD không lưu được.
- **Ngày cutoff = ngày trả tiền (boundary):** tính thuộc tháng trước (biên bao gồm, ví dụ cutoff=5 thì ngày 5 thuộc tháng trước).
- **Khách hủy hợp đồng sau khi đã trả một kỳ:** phần hoa hồng đã Posted không tự đảo — clawback nếu có là thao tác thủ công của kế toán.
- **Recipient không có MST chỉ có CCCD:** TNCN khấu trừ 20% thay vì 10%. PAKD Settings có `default_external_tax_pct` cấu hình; mỗi beneficiary line cũng có thể override.

---

## 7. Tham chiếu pháp lý và tài liệu

- **Luật Lao động Việt Nam** — hoa hồng là một phần thu nhập, áp dụng các quy định về trả lương và kỳ trả
- **Luật Thuế TNCN** — hoa hồng là thu nhập chịu thuế TNCN (khấu trừ qua module Payroll của ERPNext/HRMS)
- **Thông tư 99/2025/TT-BTC (TT99/2025)** — hệ thống tài khoản kế toán doanh nghiệp:
  - TK 6418 — Chi phí dịch vụ mua ngoài bộ phận bán hàng (mặc định cho MS, AC)
  - TK 6421 — Chi phí nhân viên bán hàng (tương ứng phần Lương KD qua payroll)
  - TK 6425 — Chi phí khác bằng tiền bộ phận bán hàng (mặc định cho Phí GPVT)
  - TK 3388 — Phải trả, phải nộp khác (TK đối ứng mặc định cho chi phí ngoài)
  - TK 334 — Phải trả người lao động (qua HRMS payroll)

Tất cả tài khoản trên đều cấu hình được để phù hợp với thực tế áp dụng tại DCNET.

---

## 8. Ngoài phạm vi phiên bản hiện tại (v0.1.0)

Những việc **đã có kế hoạch nhưng chưa implement** hoặc **cố ý loại khỏi v1**:

- **Tích hợp trực tiếp vào quy trình Payroll Entry tự động:** hiện Additional Salary được tạo, kế toán vẫn phải include AS vào Payroll Entry hằng tháng theo quy trình chuẩn của HRMS. Chưa có scheduler tự gom.
- **Clawback hoa hồng tự động:** các tình huống cần truy thu (NVKD nghỉ việc, Contract cancel sau khi hoa hồng đã Posted, PE cancel sau khi AS đã vào bảng lương đã duyệt) — hiện đều xử lý thủ công với cảnh báo rõ ràng trên hệ thống.
- **Auto-create Credit Note khi Contract cancel:** hiện chỉ cảnh báo, kế toán tự lập CN nếu cần.
- **Co-sales (chia hoa hồng giữa nhiều NVKD):** mỗi hợp đồng chỉ có một NVKD, không hỗ trợ chia.
- **Import PAKD lịch sử từ Excel:** không có công cụ migration. Các phương án cũ vẫn giữ nguyên ở Excel; chỉ PAKD phát sinh mới sau go-live được tạo trên hệ thống.
- **Wizard "Tạo PAKD hàng loạt":** NVKD FTTH DN có thể có 30-50 HD/tháng — wizard bulk-create là task roadmap riêng sau realignment.
- **Đa ngoại tệ:** chỉ xử lý VND.
- **Cơ chế delegation (người duyệt vắng mặt ủy quyền cho người khác):** không hỗ trợ. Khi người duyệt vắng mặt, admin tạm chuyển quyền bằng cách thêm vai trò cho backup user.
- **Bonus theo quý/năm ngoài commission:** không nằm trong app này — xử lý thủ công qua Additional Salary chuẩn của HRMS.
- **UI cấu hình rule engine phức tạp (nested conditions, time-weighted formulas):** hiện chỉ hỗ trợ rule dạng bảng phẳng (component × rate × base formula). Các logic phức tạp hơn cần dev can thiệp.
- **Portal cho NVKD tự xem commission dashboard:** chưa có. NVKD xem qua list view tiêu chuẩn của Frappe/ERPNext.

---

## 9. Các câu hỏi nghiệp vụ còn mở

Một số điểm đã có default hợp lý trong thiết kế nhưng **cần kế toán DCNET xác nhận chính thức** trước khi go-live:

- Tỷ lệ hoa hồng chính xác cho từng loại dịch vụ × chi nhánh (hiện dùng 10% / 75% / 2.2% / 6% từ Mẫu 01 làm default)
- Tài khoản kế toán cụ thể cho Add Costs và Manager Services (hiện default 6418)
- Danh sách người cụ thể giữ từng vai trò duyệt (để seed User và User Permission)
- Thời gian ân hạn (grace period) cho hóa đơn quá hạn (default 15 ngày)
- Cách xử lý Credit Note khi Contract cancel có hóa đơn chưa trả (default: thủ công, có cảnh báo)
- Đơn vị hiển thị trên form: VND thô hay nghìn VND (Excel hiện dùng nghìn; default DB lưu VND thô, UI có thể chuyển hiển thị)
- Quy tắc làm tròn (rounding) cho pro-rate tháng đầu/cuối (default half-up theo Excel)
- FTTH hộ gia đình: một hợp đồng cho mỗi thuê bao hay gom batch theo tháng (default: mỗi thuê bao một hợp đồng)

Các câu hỏi này có thể trả lời dần trong quá trình chạy UAT và điều chỉnh cấu hình, không block việc triển khai hệ thống.
