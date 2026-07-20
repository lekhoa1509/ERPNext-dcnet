# Rà soát sidebar 3 mục Giá thành / Tổng hợp / Báo cáo tài chính

**Vai trò:** Kế toán trưởng (KTT)
**Ngày:** 2026-05-11
**Phạm vi:** 3 sections cuối của sidebar `Kế Toán VN` — `Giá thành` (7 items), `Tổng hợp` (8 items), `Báo cáo tài chính` (14 items) = **29 items thực tế**
**Đối chiếu:** spec §5 (`docs/specs/2026-05-11-giathanh-tonghop-bctc.md`) yêu cầu **15 items mới** (5 + 4 + 5) cộng các items đã có.

---

## Tóm tắt nhanh

| Vấn đề | Số lượng | Mức độ |
|---|---|---|
| **Trùng lặp khái niệm** (cùng nghiệp vụ, 2 báo cáo khác nhau cùng xuất hiện) | 4 | 🔴 Cao — KTT nhầm lẫn |
| **Sai đối tượng link** (link_to trỏ sang record không khớp tên) | 2 | 🟡 Trung — UX khó hiểu |
| **Đặt sai section** (item thuộc nghiệp vụ khác) | 3 | 🟡 Trung — tăng nhiễu |
| **Báo cáo phân tích lẫn vào BCTC chuẩn** | 6 | 🟡 Trung — vi phạm tinh thần TT99/2025 |
| **Thiếu items so với spec** | 2 | 🔴 Cao — workflow gap |
| **Tổng số item bị đề xuất thay đổi** | **17 / 29** | |

---

## 1. Section "Giá thành" (hiện 7 items)

> **Nhận định tổng:** Section đang trộn 2 nghiệp vụ khác nhau: **(a) Giá vốn hàng mua/nhập (LCV)** và **(b) Giá thành sản xuất**. Đây là 2 concept VAS phân biệt: LCV là **TK 156/152 cộng phụ phí**, còn Giá thành SX là **TK 154 → 155**. Trộn vào 1 section khiến KTT của DN thương mại thấy quá nhiều item không dùng đến, và DN sản xuất thấy LCV "lạc loài".

### Review từng item

| # | Label hiện tại | link_to | Đánh giá | Đề xuất |
|---|---|---|---|---|
| 1 | `Định mức vật tư (BOM)` | BOM | ❌ **Sai section**. BOM là định mức KỸ THUẬT (kỹ sư SX quản lý), không phải bút toán kế toán. KTT không thao tác trực tiếp. | **CHUYỂN** sang section "Sản xuất" hoặc "Danh mục". Nếu không có section nào phù hợp, đặt indent=1 dưới mục tổng để rõ vai trò tham chiếu. |
| 2 | `Tính giá thành` | Work Order | ❌ **Label sai bản chất**. `Work Order` là "Lệnh sản xuất" (đối tượng tập hợp chi phí), không phải "tính giá thành". Tính giá thành ở wizard riêng. | **ĐỔI LABEL** thành `Lệnh sản xuất` để khớp với target. Hoặc **BỎ** — Lệnh sản xuất có thể đặt ở section "Sản xuất" riêng. |
| 3 | `Wizard tính giá thành SX` | manufacturing-costing-wizard | ⚠️ Đúng vai trò (kết chuyển 621/622/627 → 154 → 155) nhưng từ "Wizard" nghe tech, KTT trên 50 tuổi khó hiểu. | **ĐỔI LABEL** thành `Tính giá thành cuối kỳ` (chuẩn TT99/2025) hoặc theo spec gốc `Bảng tính giá thành`. |
| 4 | `Bảng tính giá thành` | Work In Progress Valuation | ⚠️ Trùng label với item #3 nếu rename. WIP Valuation lưu **kết quả** tính giá thành đã chốt. | **ĐỔI LABEL** thành `Kết quả tính giá thành` hoặc `Bảng kê giá thành đã chốt` để phân biệt với wizard. |
| 5 | `Tập hợp chi phí SX` | Production Cost Aggregation | ✅ Đúng. | Thêm hậu tố `kỳ` → `Tập hợp chi phí SX kỳ` (như spec gốc) để làm rõ ngữ cảnh "tập hợp theo kỳ kế toán". |
| 6 | `Phân bổ chi phí mua hàng` | Landed Cost Voucher | ✅ Đúng nghiệp vụ LCV. | Giữ. |
| 7 | `Chi phí chờ phân bổ` | Landed Cost Pending Allocation | ✅ Báo cáo monitoring cho LCV chưa duyệt. | Giữ. |
| ❌ | **Thiếu** | landed-cost-allocation-settings | Spec §5 yêu cầu item `Cấu hình phân bổ` để KTT cấu hình mặc định tài khoản phụ phí (vận chuyển, bốc xếp, thuế NK, VAT NK khấu trừ/không). | **THÊM** item: `Cấu hình phân bổ chi phí mua hàng` → `LCV Allocation Settings` (Single DocType). |

### Đề xuất cấu trúc mới (8 items, 2 sub-group)

```
Giá vốn & Giá thành     (rename section)
├─ Phân bổ chi phí mua hàng       → Landed Cost Voucher
├─ Chi phí chờ phân bổ            → Landed Cost Pending Allocation (Report)
├─ Cấu hình phân bổ chi phí mua hàng → LCV Allocation Settings (Single DocType)
├─ ─── (sub-divider) ───
├─ Tính giá thành cuối kỳ         → manufacturing-costing-wizard (Page)
├─ Kết quả tính giá thành         → Work In Progress Valuation
├─ Tập hợp chi phí SX kỳ          → Production Cost Aggregation (Report)
└─ Lệnh sản xuất                  → Work Order (nếu giữ ở đây; nếu không có section "Sản xuất" riêng)
```

`Định mức vật tư (BOM)` → chuyển sang section "Danh mục" hoặc section "Sản xuất".

---

## 2. Section "Tổng hợp" (hiện 8 items)

> **Nhận định tổng:** Section này là **trái tim của kế toán tổng hợp** — chứa sổ sách chính (Nhật ký chung, Sổ cái, Bảng CĐSP) và wizard khóa sổ. Hiện đa số đúng, nhưng có 1 **duplicate "Sổ cái"** dễ gây nhầm lẫn nghiêm trọng, và **thiếu 1 entry point** cho Phiếu khóa sổ kỳ (Period Closing Voucher) — bắt buộc theo VAS cuối năm.

### Review từng item

| # | Label hiện tại | link_to | Đánh giá | Đề xuất |
|---|---|---|---|---|
| 1 | `Kết chuyển cuối kỳ` | period-closing-911 (Page) | ✅ Đúng. Wizard kết chuyển TK 5xx/6xx/7xx/8xx → 911. | Giữ. |
| 2 | `Đánh giá lại ngoại tệ` | Exchange Rate Revaluation | ✅ Đúng nghiệp vụ cuối kỳ (đánh giá số dư TK ngoại tệ theo tỷ giá cuối kỳ). Spec không liệt kê nhưng cần. | Giữ. Cân nhắc thêm route_options `{"posting_date": "{today}"}` để default theo ngày hôm nay. |
| 3 | `Sổ nhật ký chung (S03a-DN)` | S03a-DN So Nhat Ky Chung | ✅ Đúng form code TT99/2025. | Giữ. |
| 4 | `Sổ cái (S03b-DN)` | S03b-DN So Cai | ✅ Đúng. Mỗi TK 1 trang. | Giữ. |
| 5 | `Sổ cái` | General Ledger (ERPNext core) | 🔴 **DUPLICATE LABEL với #4**. Cả 2 cùng label "Sổ cái" nhưng trỏ 2 báo cáo khác nhau: #4 = S03b-DN VN format, #5 = General Ledger ERPNext format (khác layout, khác cột). **KTT click bừa sẽ ra báo cáo sai định dạng.** | **BỎ** item này. Lý do: chỉ giữ duy nhất S03b-DN làm canonical. ERPNext General Ledger vẫn dùng được qua URL trực tiếp (hoặc Search bar) cho dev/debug, không cần xuất hiện ở sidebar KTT. |
| 6 | `Sổ chi tiết tài khoản` | Account Detail Ledger | ✅ Đúng (S03b-DN chỉ 1 TK / trang; Account Detail Ledger linh hoạt hơn cho phân tích). | Giữ. |
| 7 | `Bảng cân đối số phát sinh` | Trial Balance Sheet | ✅ Đúng tên TT99/2025. | Giữ. |
| 8 | `Khóa kỳ kế toán` | Accounting Period | ⚠️ **Label gây hiểu nhầm**. `Accounting Period` là MASTER định nghĩa kỳ (start/end date, fiscal year), KHÔNG phải bút toán khóa. Tên "Khóa kỳ kế toán" gợi ý đây là action khóa → KTT click vào không thấy nút "Khóa" thực sự. | **ĐỔI LABEL** thành `Định nghĩa kỳ kế toán` hoặc `Khai báo kỳ kế toán`. |
| ❌ | **Thiếu** | Period Closing Voucher | Spec §3.6 và §4.1 yêu cầu **Phiếu khóa sổ kỳ** (PCV) — bút toán kết chuyển kết quả 911 → 421 cuối năm (VAS bắt buộc). Hiện không có entry point trên sidebar. | **THÊM** item: `Phiếu khóa sổ kỳ` → `Period Closing Voucher` (DocType), `route_options: {"docstatus": ["=", 1]}` cho default list xem các phiếu đã khóa. |

### Đề xuất cấu trúc mới (9 items, theo workflow cuối kỳ)

```
Tổng hợp
├─ ─── [Workflow cuối kỳ] ─────────────────────
├─ Kết chuyển cuối kỳ              → period-closing-911 (Page)
├─ Đánh giá lại ngoại tệ           → Exchange Rate Revaluation
├─ Phiếu khóa sổ kỳ                → Period Closing Voucher  ★ THÊM
├─ Định nghĩa kỳ kế toán           → Accounting Period       (rename từ "Khóa kỳ kế toán")
├─ ─── [Sổ sách kế toán] ─────────────────────
├─ Sổ nhật ký chung (S03a-DN)      → S03a-DN So Nhat Ky Chung
├─ Sổ cái (S03b-DN)                → S03b-DN So Cai
├─ Sổ chi tiết tài khoản           → Account Detail Ledger
└─ Bảng cân đối số phát sinh       → Trial Balance Sheet
```

`Sổ cái → General Ledger` (item #5) — BỎ.

---

## 3. Section "Báo cáo tài chính" (hiện 14 items)

> **Nhận định tổng:** Section này **nghiêm trọng nhất**. Vi phạm 3 nguyên tắc:
> 1. **Duplicate báo cáo BCTC**: cùng 1 báo cáo (B01/B02/B03) xuất hiện 2 lần, 1 phiên bản ERPNext core + 1 phiên bản TT99/2025 — KTT lúng túng không biết click cái nào để xuất cho cơ quan thuế.
> 2. **Trộn báo cáo BCTC chuẩn (TT99/2025) với báo cáo quản trị/phân tích** — vi phạm tinh thần TT99/2025. "Báo cáo tài chính" trong tiếng Việt có nghĩa rất cụ thể: B01/B02/B03/B09 cho cơ quan thuế. Các báo cáo phân tích (Lợi nhuận gộp, Chỉ số tài chính) thuộc về quản trị nội bộ, KHÔNG nộp cơ quan thuế.
> 3. **Có báo cáo không phù hợp default**: `BC hợp nhất` chỉ áp dụng cho tập đoàn — DN single-entity không dùng đến.

### Review từng item

| # | Label hiện tại | link_to | Đánh giá | Đề xuất |
|---|---|---|---|---|
| 1 | `Bảng CĐKT (B01-DN)` | Balance Sheet (ERPNext core) | 🔴 **DUPLICATE với #4**. Tên hiển thị có "(B01-DN)" nhưng target là **ERPNext core Balance Sheet** — khác format, khác mã dòng so với TT99/2025 B01-DN. Tên TT99/2025 không còn là "Bảng CĐKT" mà là **"Báo cáo tình hình tài chính"** (xem `rules/tt99_2025_form_codes.md`). | **BỎ.** |
| 2 | `BC Kết quả HĐKD (B02-DN)` | Profit and Loss Statement | 🔴 **DUPLICATE với #5**. ERPNext P&L không khớp B02-DN format. | **BỎ.** |
| 3 | `BC Lưu chuyển tiền tệ (B03-DN)` | Cash Flow | 🔴 **DUPLICATE với #6**. ERPNext Cash Flow không khớp B03-DN format (TT99/2025 yêu cầu phương pháp trực tiếp/gián tiếp có cấu trúc dòng cụ thể). | **BỎ.** |
| 4 | `Báo cáo tình hình tài chính (B01-DN)` | B01-DN Bao Cao Tinh Hinh Tai Chinh | ✅ Đúng TT99/2025 (tên mới của Bảng CĐKT). Custom VN report. | Giữ. |
| 5 | `Báo cáo kết quả HĐKD (B02-DN)` | B02-DN Bao Cao KQHDKD | ✅ Đúng TT99/2025. | Giữ. |
| 6 | `Báo cáo lưu chuyển tiền tệ (B03-DN)` | B03-DN Bao Cao LCTT | ✅ Đúng TT99/2025. | Giữ. |
| 7 | `Thuyết minh BCTC (B09-DN)` | b09-dn-generator (Page) | ✅ Đúng. Page multi-sheet Excel generator. | Giữ. |
| 8 | `Cấu hình BCTC Mapping` | BCTC Mapping | ✅ Đúng. KTT cấu hình mapping TK → dòng BCTC theo từng Company. | Giữ. Cân nhắc move sang section "Thiết lập" (item config), nhưng để ở BCTC cũng OK vì KTT thường tra cứu khi rà số. |
| 9 | `Cân đối thử` | Trial Balance | 🔴 **DUPLICATE concept với "Bảng cân đối số phát sinh" ở Tổng hợp**. "Cân đối thử" và "Bảng cân đối số phát sinh" là **đồng nghĩa** trong tiếng Việt kế toán. KTT thấy 2 link "cùng nghĩa khác chỗ" → nghi ngờ tính nhất quán hệ thống. | **BỎ.** |
| 10 | `Lợi nhuận gộp` | Gross Profit | ⚠️ **Báo cáo phân tích, KHÔNG phải BCTC chuẩn TT99/2025**. Đây là báo cáo quản trị nội bộ. | **CHUYỂN** sang section mới "Phân tích & Quản trị" (hoặc bỏ — DN có thể tự xem trong Báo cáo kết quả HĐKD). |
| 11 | `Lãi/Lỗ gộp & ròng` | Gross and Net Profit Report | ⚠️ Tương tự, báo cáo quản trị. | **CHUYỂN** hoặc bỏ. |
| 12 | `Chỉ số tài chính` | Financial Ratios | ⚠️ Báo cáo phân tích (ROA, ROE, current ratio, ...). | **CHUYỂN** sang section "Phân tích & Quản trị". |
| 13 | `Phân tích lợi nhuận` | Profitability Analysis | ⚠️ Báo cáo phân tích. | **CHUYỂN** sang section "Phân tích & Quản trị". |
| 14 | `BC hợp nhất` | Consolidated Financial Statement | ⚠️ **Chỉ áp dụng cho tập đoàn có công ty con/liên kết**. DN đơn lẻ KHÔNG dùng. | **ẨN có điều kiện** — chỉ hiển thị nếu Company hiện tại có `parent_company` (là công ty con) hoặc có ít nhất 1 Company khác `parent_company = this`. Hoặc gắn role "Group Accountant" để hiển thị. |

### Đề xuất cấu trúc mới — chia thành 2 sections

#### Section "Báo cáo tài chính" (5 items — BCTC chuẩn TT99/2025 only)

```
Báo cáo tài chính
├─ Báo cáo tình hình tài chính (B01-DN)   → B01-DN Bao Cao Tinh Hinh Tai Chinh
├─ Báo cáo kết quả HĐKD (B02-DN)          → B02-DN Bao Cao KQHDKD
├─ Báo cáo lưu chuyển tiền tệ (B03-DN)    → B03-DN Bao Cao LCTT
├─ Thuyết minh BCTC (B09-DN)              → b09-dn-generator (Page)
└─ Cấu hình BCTC Mapping                  → BCTC Mapping
```

**Loại bỏ 9 items**: 3 ERPNext core duplicate (#1, #2, #3), Cân đối thử (#9), 4 báo cáo phân tích (#10-13), BC hợp nhất (#14 — ẩn theo điều kiện).

#### Section MỚI "Phân tích & Quản trị" (4 items)

```
Phân tích & Quản trị         ★ SECTION MỚI
├─ Lợi nhuận gộp             → Gross Profit
├─ Lãi/Lỗ gộp & ròng         → Gross and Net Profit Report
├─ Phân tích lợi nhuận       → Profitability Analysis
└─ Chỉ số tài chính          → Financial Ratios
```

Section này có audience khác (BGĐ + KTT báo cáo nội bộ), không phải kế toán viên xuất BCTC ra cơ quan thuế.

**BC hợp nhất**: implement conditional visibility (Server Script hoặc role-gated).

---

## Tổng kết đề xuất

### Bảng thay đổi (29 items → 18 items chính + 4 items phân tích section riêng + 1 ẩn có điều kiện)

| Hành động | Số items | Chi tiết |
|---|---|---|
| 🟢 **Giữ nguyên** | 12 | Items đúng nghiệp vụ và format |
| 🟡 **Đổi label** | 4 | Tính giá thành/Bảng tính giá thành/Khóa kỳ KT (rename theo nghiệp vụ đúng) |
| 🔵 **Thêm mới** | 2 | Cấu hình phân bổ LCV + Phiếu khóa sổ kỳ |
| 🔴 **Bỏ khỏi sidebar** | 5 | 3 ERPNext core duplicate + Cân đối thử + Sổ cái duplicate |
| 🟣 **Chuyển section** | 5 | BOM → Danh mục; 4 báo cáo phân tích → section "Phân tích" mới |
| ⚫ **Ẩn có điều kiện** | 1 | BC hợp nhất — chỉ hiện khi có sub-company |

### Patch script (sẽ tạo riêng sau khi anh duyệt)

Sẽ ra file Python idempotent gọi qua `bench --site dcnet.localhost execute vn_accounting.utils.sidebar_review_patch_2026_05_11.apply`:

1. Lọc 5 items cần bỏ qua `DELETE FROM \`tabWorkspace Sidebar Item\``.
2. Update 4 labels bằng `frappe.db.set_value`.
3. Insert 2 items mới với idx phù hợp.
4. Chuyển section: insert items mới ở section đích, delete khỏi section cũ.
5. Tạo Section Break "Phân tích & Quản trị" nếu chưa có.
6. Set route_options `{"fiscal_year": "{current}"}` cho 3 BCTC reports để default ra năm hiện hành (đã có route_options nhưng giá trị rỗng).
7. Update workspace_sidebar JSON fixture tương ứng (để migrate tiếp theo idempotent).
8. Cuối cùng: `bench --site dcnet.localhost clear-cache`.

### Câu hỏi cần anh quyết trước khi em viết patch

1. **Section "Phân tích & Quản trị"** có nên tạo mới, hay gộp các báo cáo phân tích vào section "Tổng hợp" hiện có (làm sub-group)?
2. **BC hợp nhất**: ẩn hoàn toàn cho lần này, hay cài conditional visibility?
3. **Định mức vật tư (BOM)**: chuyển vào section nào — "Danh mục" hay tạo section "Sản xuất" mới?
4. **Lệnh sản xuất (Work Order)**: giữ ở sidebar hay bỏ? (BOM + Work Order là tooling cho bộ phận SX, KTT thường không trực tiếp thao tác.)

Trả lời 4 câu trên xong em viết patch + verify trên browser.
