# Business Logic — Tính giá thành công trình & xuất hóa đơn theo giai đoạn

**Feedback:** FB-00605
**Ngày:** 2026-05-15
**Tham chiếu:** TT99/2025/TT-BTC — hạch toán doanh nghiệp xây lắp / dịch vụ thi công công trình
**Trạng thái:** Spec v0.4 đã được Long (KTT DCNET) xác nhận qua 3 rounds discovery (2026-05-15)
**Phạm vi:** mô tả nghiệp vụ thuần túy, không chứa chi tiết kỹ thuật. Phần kỹ thuật ở file `2026-05-15-project-costing-tech-mapping.md`.

---

## 1. Mục đích

Cho phép DCNET:

1. **Gom chi phí thực tế** của một công trình theo nhiều nhóm (vật tư / đi lại / lương / thuê ngoài) và nhiều giai đoạn.
2. **Tính giá bán linh hoạt** theo nhiều phương pháp markup khác nhau cho mỗi giai đoạn.
3. **Xuất hóa đơn theo từng giai đoạn nghiệm thu** — không bắt buộc 1 công trình = 1 hóa đơn.
4. **Báo cáo lãi/lỗ chi tiết** cho mỗi công trình, mỗi giai đoạn, phân biệt chi phí trực tiếp và chi phí phân bổ.
5. **Sinh bút toán đúng TT99/2025** — chuỗi 627 → 154 → 632 cho doanh nghiệp thi công công trình.

## 2. Vòng đời 1 công trình

```
TẠO          NHẬP CHI PHÍ              PHÂN BỔ      XUẤT HĐ      ĐÓNG
─────────────────────────────────────────────────────────────────────
PM/KTT       Thi công + Văn phòng      PM/KTT       KTT          KTT
tạo Project  + Kế toán viên            pivot tool   tạo SI       chốt
Costing      nhập chứng từ chi phí     pin Common   draft →      lãi/lỗ
+ giai đoạn  hằng ngày (project bắt    → stage      duyệt →      154→0
dự kiến      buộc, stage tùy chọn)                  submit
```

Mỗi giai đoạn đi qua các trạng thái: **Dự kiến** → **Đang thi công** → **Chờ xuất HĐ** → **Đã có SI draft** → **Đã xuất HĐ** → **Đã thu tiền**.

## 3. Quy tắc nhập chi phí

**R3.1.** Mọi chi phí phát sinh có liên quan công trình PHẢI tag công trình. Nếu bỏ trống → không vào báo cáo công trình.

**R3.2.** Tag giai đoạn KHÔNG bắt buộc khi nhập chi phí. Bỏ trống → cost vào **"Common pool"** của công trình (KTT/PM pin vào giai đoạn sau qua Pivot Tool).

**R3.3.** Các nguồn chi phí được tính vào công trình (chỉ những chứng từ phát sinh GL Entry thực tế):
- Xuất kho vật tư (Phiếu xuất kho / Stock Entry purpose Material Issue)
- Phiếu xuất hàng (Delivery Note)
- Mua hàng / dịch vụ (Phiếu mua hàng / Purchase Invoice)
- Hoàn ứng đi lại / ăn ở (Phiếu hoàn ứng / Expense Claim)
- Sửa chữa thiết bị thi công (Asset Repair)
- Bút toán thủ công Dr 154 (Project=X) (Journal Entry — KTT post trực tiếp)
- **Phase 2 sẽ thêm:** Lương kỹ sư on-site (Salary Slip) — không có project field native nên cần Custom Field hoặc đi qua Cost Allocation Run với source = Salary Slip
- **Phase 2 sẽ thêm:** Khấu hao thiết bị thi công (Asset Depreciation) — đi qua Cost Allocation Run

**R3.3.1. Timesheet KHÔNG được tính như chi phí trực tiếp.** Timesheet chỉ ghi nhận thời gian làm việc (labor tracking), KHÔNG phát sinh GL Entry. Lương kỹ sư trực tiếp được hạch toán qua Salary Slip (Dr 622 / Cr 334) tag công trình; lương PM gián tiếp qua Salary Slip Dr 642/627 sau đó phân bổ qua Cost Allocation Run. Timesheet vẫn hữu ích như **bằng chứng** để KTT quyết định tỷ lệ % phân bổ lương vào project khi tạo Allocation Run.

**R3.4.** Chi phí nhập sau khi công trình đã đóng → cảnh báo nhưng vẫn ghi nhận. KTT có thể mở lại công trình hoặc treat như chi phí bảo hành/dịch vụ sau bán.

**R3.5. Quy tắc tag công trình trên Phiếu mua hàng (PI):**

| Trường hợp | Cách làm đúng |
|---|---|
| PI mua hàng/dịch vụ **100% cho 1 công trình** (vd: thuê đội ngoài kéo cáp cho project ABC) | Tag PI = project ABC trực tiếp |
| PI mua hàng **vào kho chung** (vd: 200m cable, 50 switch dùng dần) | KHÔNG tag project trên PI. Khi cần dùng cho công trình → tạo Phiếu xuất kho theo số lượng thực tế, tag project trên phiếu đó |

**R3.6. Cảnh báo khi pin sai pattern:**

Nếu KTT/PM thử pin 1 PI vào ≥2 công trình trên Pivot Tool, hệ thống hiển thị dialog cảnh báo (không block):

> ⚠️ PI này đang được pin vào nhiều công trình.
> Nếu hàng hóa thực tế chia ra nhiều công trình theo số lượng, khuyến nghị:
> 1. Hủy thao tác pin này
> 2. Tạo Phiếu xuất kho cho từng công trình theo đúng số lượng dùng
> 3. Pin các Phiếu xuất kho đó (không pin PI gốc)
>
> Lý do: số liệu kho + báo cáo công trình chính xác hơn.

**Khi nào khác?**
- Chi phí hủy (PI/SE cancel): tự động rút khỏi rollup của giai đoạn (nếu đã pin) hoặc Common pool. KTT có thông báo.
- Chi phí backdated sau khi giai đoạn đã có SI submitted: cho phép ghi nhận nhưng FLAG riêng. KTT quyết bù vào giai đoạn sau hoặc write-off.

## 4. Quy tắc phân bổ chi phí — Pivot Tool

**R4.1.** Pivot Tool là nơi DUY NHẤT để KTT/PM thay đổi mapping cost ↔ giai đoạn. Không có 2 đường khác (giảm bug đồng bộ).

**R4.2.** 1 chi phí có thể chia ra ≥1 giai đoạn. Tổng các phần chia phải = nguyên giá chi phí (không cho phép thiếu/dư).

**R4.3.** Khi 1 giai đoạn đã có hóa đơn **submitted**, mọi cost đã pin vào giai đoạn đó **bị khóa** — không edit, không di chuyển sang giai đoạn khác. Đảm bảo truy vết hóa đơn ↔ chi phí.

**R4.4.** Common pool có thể dương cuối công trình. KTT chọn 1 trong 3 cách xử lý:
- Phân nốt vào giai đoạn nào đó (nếu giai đoạn đó chưa submit hóa đơn).
- Tạo "Giai đoạn write-off" và xuất HĐ tượng trưng = 0.
- Bỏ qua → vào báo cáo lãi/lỗ công trình như "chi phí chung không phân bổ" và write-off khi đóng project.

**R4.5.** Common pool KHÔNG được âm (over-allocated). UI block thao tác split > nguyên giá.

**Khi nào khác?**
- Công trình bị hủy giữa chừng + đã có SI submitted ở giai đoạn 1: SI giai đoạn 1 giữ nguyên (đã giao khách). Cost đã pin stage 1 khóa nguyên. Cost trong Common pool + cost stage 2,3 chưa SI → unpin về Common pool của công trình "Đã hủy". KTT viết write-off riêng.

## 5. Quy tắc tính giá xuất hóa đơn — Markup

Mỗi giai đoạn chọn 1 trong 6 phương pháp:

| # | Method | Cách tính | Khi dùng |
|---|---|---|---|
| 1 | **Hệ số** | `chi_phí × hệ_số` (vd 1.5) | Công trình đơn giản, biên lợi nhuận chuẩn |
| 2 | **% trên chi phí** | `chi_phí × (1 + %)` (vd +30%) | Tương đương #1, KTT nghĩ theo % |
| 3 | **Số tiền cố định** | KTT input số tiền (vd 150tr) | Có thỏa thuận cứng, không phụ thuộc chi phí |
| 4 | **Theo HĐ / phụ lục** | Lấy từ contract / phụ lục đã ký | HĐ khung ghi sẵn giá mỗi mốc |
| 5 | **% trên giá trị HĐ khung** | `HĐ_value × %` | Tạm ứng theo % HĐ (vd tạm ứng 30% trước khởi công) |
| 6 | **% trên cost đã phát sinh + uplift** | `cost_to_date × (1 + %)` | Nghiệm thu giữa kỳ — xuất theo tiến độ chi phí thực |

**R5.1.** Mỗi giai đoạn dùng 1 method. Trong cùng 1 công trình, các giai đoạn có thể dùng methods khác nhau.

**R5.2.** Hệ thống tính giá đề xuất theo công thức → KTT có thể OVERRIDE bằng cách type số bất kỳ vào ô "Giá xuất hóa đơn". Lưu log: giá đề xuất, giá thực, người override, lý do.

**R5.3.** Markup âm (giá < chi phí) → CẢNH BÁO nhưng KHÔNG block. KTT có thể bypass với lý do (vd: bán lỗ giành thầu).

**R5.4.** Markup = 0 (cost-only) → cho phép (vd: HĐ phụ kiện không lãi).

**R5.5. Tạm ứng & cuốn chiếu:** Khi 1 công trình có giai đoạn tạm ứng đầu (method 3, 4, hoặc 5):
- Stage tạm ứng có thể tạo hóa đơn TRƯỚC khi mọi chi phí được pin.
- Báo cáo lãi/lỗ stage tạm ứng = giá HĐ - chi phí pin vào stage đó (có thể âm tạm thời nếu chi phí dồn về stage sau).
- KTT có thể tái cân bằng cost giữa các stage CHƯA submit để báo cáo cuối công trình chính xác.

**R5.6. Hiển thị giá đề xuất + giá chốt:** Trên Pivot Tool, mỗi stage hiển thị 3 con số:
- Giá tính theo method (số đề xuất từ công thức)
- Giá KTT chốt (KTT type số bất kỳ)
- Chênh lệch (nếu có)

Audit trail: ai override, khi nào, lý do (free-text).

**Khi nào khác?**
- "Theo HĐ" nhưng chi phí thực > giá HĐ (over-budget): hiển thị cảnh báo đỏ. KTT có thể (a) chấp nhận lỗ, (b) đàm phán phụ lục tăng giá rồi update markup_value, (c) move cost dư sang giai đoạn sau.

## 6. Quy tắc xuất hóa đơn

**R6.1.** 1 giai đoạn → 1 hóa đơn duy nhất. Không cho phép 2 SI cho cùng 1 giai đoạn.

**R6.2.** Khi bấm "Tạo HĐ" → sinh hóa đơn DRAFT với:
- 1 dòng item duy nhất: "[Tên công trình] — [Tên giai đoạn]"
- Số tiền = "Giá xuất hóa đơn" của giai đoạn
- Khách hàng = customer của project
- Link ngược về Project Costing + Stage

**R6.3.** KTT review hóa đơn draft → bấm Submit. Trước Submit có thể:
- Đổi item description
- Tách 1 dòng thành nhiều dòng
- Đổi số tiền (cảnh báo lệch với "Giá xuất HĐ" trong stage)
- Thêm thuế VAT

**R6.4.** Sau Submit, hóa đơn hoạt động bình thường như mọi hóa đơn khác (theo dõi công nợ, ghi nhận thu, GL, …).

**R6.5.** Nếu hóa đơn bị Cancel sau Submit:
- Stage status quay về "Chờ xuất HĐ"
- Cost của stage **mở khóa** (có thể edit lại)
- Bút toán giá vốn của stage tự động cancel (đảo dấu)
- KTT có thể tạo hóa đơn mới cho stage

**R6.6. Quyền submit hóa đơn:**
- **KTT** được submit mặc định (mọi mức tiền).
- **Giám đốc** cũng được submit mặc định (mọi mức tiền). Không bắt buộc 2-tier.
- 1 trong 2 submit là đủ.
- **Optional cho công ty muốn 2-tier:** bật workflow "Hóa đơn > X tr cần GĐ duyệt trước KTT submit". Cấu hình ngưỡng trong Settings. Mặc định TẮT.

## 7. Đóng / hủy công trình

**R7.1. Đóng (normal completion):** mọi giai đoạn có hóa đơn submitted. KTT bấm "Đóng" → công trình chuyển trạng thái "Đã hoàn thành". Hệ thống kiểm tra số dư WIP còn lại:
- Nếu = 0: chỉ đổi status.
- Nếu > 0 (cost còn dư): dialog cho KTT chọn xử lý (write-off vào 642 Chi phí QLDN, hoặc 632 Giá vốn không phân bổ, hoặc hủy thao tác đóng).

**R7.2. Hủy (cancellation midway):**
- Giai đoạn đã có hóa đơn submitted: KHÔNG cancel hóa đơn (đã giao khách). Cost giữ nguyên.
- Giai đoạn chưa có hóa đơn: status → "Đã hủy". Cost của các stages này quay về Common pool.
- Common pool toàn bộ → KTT write-off (vào chi phí khác phù hợp) hoặc treo trên project "Đã hủy".

**R7.3. Mở lại công trình đã đóng:** cho phép (vd: chi phí phát sinh sau bảo hành, KTT bù hóa đơn mới hoặc bù giai đoạn bảo hành).

## 8. Báo cáo

### 8.1 Bảng tập hợp chi phí công trình (mới)
- Filter: công trình + giai đoạn + nhóm chi phí + thời gian
- Cột: chi phí thực × markup × giá bán × lãi/lỗ
- Drill-down: click số → list các chi phí gốc

### 8.2 Bảng lãi/lỗ công trình (mở rộng từ Project Profitability có sẵn)
- Filter thêm: theo giai đoạn
- Hiển thị Common pool riêng
- Phân tách 2 cột: Chi phí trực tiếp vs Chi phí phân bổ
- 2 chỉ số: Lãi gộp (doanh thu - trực tiếp) + Lãi ròng (doanh thu - tổng)

### 8.3 Bảng tiến độ xuất hóa đơn (mới)
- Theo dõi giai đoạn nào sắp đến hạn xuất hóa đơn, đã xuất chưa
- Nhắc theo `expected_date` của stage

## 9. Phân quyền

| Vai trò | Nhập CP | Pin stage | Markup | Tạo SI draft | Submit SI | Đóng project |
|---|---|---|---|---|---|---|
| Thi công / Văn phòng | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Kế toán viên | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Project Manager | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Kế toán trưởng | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Giám đốc | (view) | (view) | (view) | ❌ | ✅ | ❌ |

## 10. Chi phí trực tiếp vs Chi phí phân bổ

### 10.1 Phân loại

Mỗi chứng từ chi phí có field "Loại chi phí" với 2 giá trị:

| Loại | Định nghĩa | Ví dụ |
|---|---|---|
| **Trực tiếp** | Phát sinh hoàn toàn vì 1 công trình. Hủy công trình thì hủy chi phí. | Vật tư mua riêng project, lương kỹ sư on-site, thuê đội ngoài |
| **Phân bổ** | Phát sinh chung, chia ra nhiều công trình theo công thức. Không có công trình thì vẫn phát sinh. | Lương quản lý dự án, văn phòng phẩm chung, chi phí xe công ty, khấu hao thiết bị thi công |

**R10.1.** Mặc định chứng từ tag project = **Trực tiếp**. KTT đổi sang "Phân bổ" nếu cần.

**R10.2.** Cost "Phân bổ" KHÔNG tag project trực tiếp. KTT tạo **"Đợt phân bổ chi phí"** (Cost Allocation Run) định kỳ (cuối tháng) để chia ra các project con.

### 10.2 Đợt phân bổ chi phí — Cost Allocation Run

KTT tạo **manual** (không scheduler tự động). Mỗi đợt:

```
Đợt phân bổ chi phí #2026-05
─────────────────────────────────────────────────────────
Kỳ: 01/05/2026 → 31/05/2026
Người tạo: KTT
Trạng thái: [Draft / Đã tính / Đã phân bổ / Đã hủy]

Nguồn chi phí cần phân bổ:
  PI-2026-00150 — Văn phòng phẩm tháng 5      8.000.000
  SS-2026-00088 — Lương PM Tuấn (50%)        25.000.000
  EXP-00067    — Bảo dưỡng xe công ty          3.000.000
                                            ─────────────
                                  TỔNG       36.000.000

Phương pháp phân bổ:
  ⚫ Đều cho mọi project active trong kỳ
  ⚪ KTT input % thủ công

Phân bổ ra projects:
  PROJ-AGRIBANK-DC      25%     9.000.000
  PROJ-IDC-CMC          25%     9.000.000
  PROJ-CAMERA-XYZ       25%     9.000.000
  PROJ-MPLS-ABC         25%     9.000.000
                              ─────────────
                       100%    36.000.000

[Tính lại theo phương pháp]  [Duyệt + phân bổ]
```

**R10.3. Phương pháp phân bổ:**

| Method | Công thức |
|---|---|
| **Đều** | `total ÷ N_projects_active` |
| **Thủ công** | KTT input % từng project, tổng phải = 100% |

Nếu KTT muốn phân bổ theo % HĐ hoặc % cost trực tiếp → tính tay rồi input % thủ công. Không hỗ trợ auto-tính 2 phương pháp đó (tránh bug công thức + giảm phức tạp UI).

**R10.4.** Sau khi "Duyệt + phân bổ":
- Mỗi share sinh 1 entry "Chi phí phân bổ" gắn project (lưu link ngược về Allocation Run).
- Vào báo cáo project ở cột **Chi phí phân bổ** (KHÔNG vào Common pool, vì đã có project đích rõ).
- Common pool chỉ chứa cost trực tiếp chưa pin stage.

**R10.5.** Edit/hủy Allocation Run sau khi đã phân bổ:
- Cho phép NẾU mọi project đích chưa có hóa đơn submitted trong kỳ.
- Nếu ≥1 project đã submit hóa đơn → block, KTT phải bù bằng 1 Allocation Run đảo dấu.

### 10.3 Báo cáo P&L có 3 nhóm cột mới

| Project | Doanh thu | Chi phí trực tiếp | Chi phí phân bổ | Tổng chi phí | Lãi gộp | Lãi ròng |
|---|---|---|---|---|---|---|

- "Lãi gộp" = doanh thu - trực tiếp.
- "Lãi ròng" = doanh thu - tổng (trực tiếp + phân bổ).

KTT tracking cả 2: project có "lãi gộp tốt" nhưng "lãi ròng âm" → đáng báo động về tỷ lệ chi phí gián tiếp.

## 11. Bút toán theo TT99/2025

Theo TT99/2025/TT-BTC, doanh nghiệp xây lắp / thi công công trình BẮT BUỘC dùng TK 627 (Chi phí sản xuất chung) cho chi phí gián tiếp, KHÔNG dùng thẳng TK 642. Chuỗi bút toán đầy đủ:

### 11.1 Chi phí TRỰC TIẾP (vật tư, lương kỹ sư on-site, thầu phụ) — tag project

```
Vật tư xuất kho cho project:
    Nợ 154 (Project=X) / Có 152

Lương kỹ sư on-site (Salary Slip allocated to project):
    Nợ 154 (Project=X) / Có 334

Thầu phụ (PI tag project):
    Nợ 154 (Project=X) / Có 331
```

### 11.2 Chi phí GIÁN TIẾP (lương PM, khấu hao thiết bị thi công, văn phòng phẩm)

```
Phát sinh ban đầu (CHƯA gắn project):
    Nợ 627 / Có 152, 334, 214, ...

Cuối kỳ Allocation Run phân bổ về projects:
    Nợ 154 (Project=A) / Có 627    (per share)
    Nợ 154 (Project=B) / Có 627
    Nợ 154 (Project=C) / Có 627
    ...
```

### 11.3 Stage SI submit → ghi nhận doanh thu + giá vốn

```
Doanh thu (ERPNext core auto):
    Nợ 131 (KH=Y) / Có 511 + Có 3331

Giá vốn (custom hook):
    Nợ 632 / Có 154 (Project=X)
    Amount = tổng cost pin vào stage này
```

### 11.4 Đóng project — 154 (Project=X) phải về 0

```
Nếu còn dư cuối project (Common pool chưa pin hoặc vượt budget):
    Nợ 642 (hoặc 632) / Có 154 (Project=X)   write-off, KTT chốt
```

### 11.5 Vượt công suất (Phase 2, không làm ngay)

TT99/2025 quy định: phần CP sản xuất chung cố định vượt công suất bình thường → Dr 632 thẳng, không qua 154. Tính "công suất bình thường" cho service company khó (không có đơn vị sản phẩm cố định). **Phase 1**: bỏ qua. Toàn bộ 627 phân bổ về 154. **Phase 2 (tương lai)**: thêm field "Phần vượt công suất" trên Allocation Run, KTT tách thủ công nếu cần.

## 12. Override tài khoản WIP per chứng từ

Trên các chứng từ chi phí khi có `project` tag → hiển thị field **"Tài khoản tập hợp chi phí"**:

| Loại chứng từ | Default từ Settings | KTT override |
|---|---|---|
| Stock Entry purpose="Material Issue" | `wip_account_project_costing` (154) | ✅ |
| Delivery Note | `wip_account_project_costing` (154) | ✅ |
| Purchase Invoice (per row) | `wip_account_project_costing` (154) | ✅ |
| Expense Claim | `wip_account_project_costing` (154) | ✅ |
| Salary Slip allocation thủ công | `wip_account_project_costing` (154) | ✅ |

**R12.1.** Field này chỉ hiển thị khi có `project` tag. Nếu bỏ trống → ERPNext default (Dr 632 / Cr 152 cho DN, Dr expense_acc / Cr 331 cho PI...).

**R12.2.** Override hook chạy ở GL post (on_submit) — không động ERPNext core, chỉ tạo bút toán bù 2-layer (giống pattern LCV bù trong vn_accounting đã có):
- Layer 1: ERPNext core post Dr `<default_account>` / Cr `<source>`
- Layer 2: Custom hook post bút toán bù `Dr <override_account>` / Cr `<default_account>` với marker.

Tradeoff: 2 bút toán thay vì 1 (cosmetic noise trên Sổ chi tiết), nhưng an toàn khi upgrade ERPNext + linh hoạt override.

## 13. Truy vết bút toán — JE Traceability

**R13.1.** Mọi bút toán sinh ra bởi công cụ này PHẢI:
- Có ≥1 row trong JE Account với `reference_type="Project Costing"` + `reference_name=<project-costing-doc>`.
- Có `user_remark` chứa marker phân loại: `[PROJECT_COSTING:<costing-name>][TYPE:<type>]` với `<type>` ∈ `{ALLOCATION_RUN, STAGE_COGS, WIP_OVERRIDE, CLOSE_WRITEOFF}`.

**R13.2.** Property Setter mở rộng `Journal Entry Account.reference_type` Select options: thêm `"Project Costing"` vào danh sách (SI/PI/JE/SO/PO/Asset/Loan/...).

**R13.3.** Embedded section trên form Project Costing — "Bút toán liên quan" (tab Chi tiết, không phải Connections):

```
▼ Phân bổ chi phí gián tiếp (3 đợt)
  2026-05-31  JV-2026-00045  ALLOCATION_RUN-2026-05
              Dr 154 (Project=X) / Cr 627       16.200.000  [→]
  ...
                                            Tổng phân bổ:   38.500.000

▼ Bù tài khoản WIP từ chứng từ chi phí (12 bút toán)
  2026-04-15  JV-2026-00027  WIP_OVERRIDE  từ PI-2026-00150
              Dr 154 / Cr 632                   85.000.000  [→]
  ...
                                                Tổng bù:  540.000.000

▼ Giá vốn ghi nhận theo stage (2 stage đã xuất HĐ)
  2026-04-20  JV-2026-00032  STAGE_COGS  Stage 1 ↔ SINV-001
              Dr 632 / Cr 154 (Project=X)       12.750.000  [→]
  ...
                                               Tổng COGS: 235.050.000

▼ Kết chuyển / Write-off cuối project (chưa có)

──────────────────────────────────────────────────────────────────
Số dư TK 154 hiện tại (Project=X):    343.450.000
```

Mỗi dòng có nút `[→]` mở thẳng JE detail. Sub-section collapsible. Tổng cuối check balance qua GL Entry.

**R13.4. Reverse trace từ JE → Project Costing:** mở 1 JE bất kỳ → field `user_remark` chứa marker → KTT click marker → navigate sang Project Costing form.

## 14. Edge cases tổng hợp

| ID | Tình huống | Xử lý |
|---|---|---|
| EC1 | Cancel SI sau khi đã recognize COGS | JE COGS auto-cancel (đảo dấu). Cost trên stage mở khóa. Stage status quay về "Chờ xuất HĐ" |
| EC2 | Stage có cost = 0 (vd "Tạm ứng đầu") | Không sinh JE COGS (Cr 154 = 0 sẽ lỗi DB). SI vẫn submit bình thường, chỉ có Dr 131 / Cr 511 + 3331 |
| EC3 | Allocation Run cho kỳ đã đóng sổ (PCV) | Block tạo cho kỳ trước PCV. Buộc KTT lùi vào kỳ sau hoặc mở PCV |
| EC4 | Project chỉ có cost phân bổ, không có cost direct | Cho phép. P&L hiển thị "Trực tiếp = 0, Phân bổ > 0". Recognize COGS: rút từ phần allocated |
| EC5 | KTT để trống "Tài khoản tập hợp chi phí" trên Stock Entry tag project | Cảnh báo "Chi phí này sẽ vào TK mặc định, không tập hợp vào 154 công trình. Anh chắc chứ?" |
| EC6 | Backdated chi phí sau khi stage đã có SI submitted | Cho phép ghi nhận nhưng FLAG riêng. KTT quyết bù stage sau hay write-off |
| EC7 | Project hủy giữa chừng + đã có SI submitted ở stage 1 | SI stage 1 giữ nguyên. Cost stage 1 khóa. Cost stage 2,3 chưa SI + Common pool → unpin về Common pool "Đã hủy". KTT write-off |

## 15. Settings — 4 trường tài khoản mặc định

`VN Accounting Settings` thêm 4 fields:

| Field | Mặc định | Note |
|---|---|---|
| `wip_account_project_costing` | TK 154 | Tài khoản WIP công trình |
| `overhead_collector_account` | TK 627 | Tài khoản gom chi phí gián tiếp |
| `cogs_account_project_costing` | TK 632 | TK giá vốn (recognize khi SI submit) |
| `writeoff_account_project_costing` | TK 642 | TK write-off default khi đóng project có dư |

KTT có thể override per Settings (không hardcode trong code, tuân thủ rule `feedback_vn_accounting_no_hardcoded_accounts.md`).

---

## Tham chiếu

- TT99/2025/TT-BTC, hiệu lực 01/01/2026, thay thế TT200/2014 và TT133/2016.
- ERPNext Project + Project Profitability Report (tận dụng phần lõi).
- vn_accounting LCV bù pattern (mẫu cho 2-layer GL override).
- vn_accounting Deferred Expense feature (FB-00834, 2026-05-15) — mẫu cho embedded section + GL traceability.
