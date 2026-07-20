# Spec: Giá thành — Tổng hợp — Báo cáo tài chính (TT99/2025)

**Date:** 2026-05-11
**Branch:** `feature/giathanh-tonghop-bctc` (apps/vn_accounting)
**Author:** Long
**Status:** Draft for eng/design review
**Related:** BUSINESS_LOGIC.md §11–§14, FEATURES.md §C7–§C10

---

## 1. Vấn đề & Mục tiêu

### 1.1 Vấn đề hiện tại

Sidebar vn_accounting có 3 sections rỗng / thiếu nghiệp vụ cốt lõi:

- **Giá thành** — chưa có item nào. DN thương mại không có phân bổ chi phí mua hàng (vận chuyển, nhập khẩu, thuế NK) → giá vốn méo. DN sản xuất không có cơ chế tính giá thành theo TT99/2025.
- **Tổng hợp** — đã có Sổ chi tiết tài khoản (A2.2) + Bảng cân đối số phát sinh (A2.1) nhưng thiếu Sổ nhật ký chung (S03a-DN), Sổ cái (S03b-DN, khác Sổ chi tiết về format), Kết chuyển cuối kỳ (911 → 421), Khóa sổ kỳ.
- **Báo cáo tài chính** — chưa có. 4 báo cáo bắt buộc theo TT99/2025 (B01/B02/B03/B09-DN) đều thiếu.

Đồng thời:
- TT99/2025 đổi tên **B01-DN** từ "Bảng cân đối kế toán" → **"Báo cáo tình hình tài chính"**. Tài liệu cũ trong FEATURES.md còn tên cũ.
- Mọi feature kế toán phải **hiện TK định khoản + cho phép sửa**, không hardcode TK trong code. Đây là yêu cầu cross-cutting (xem `~/.claude/projects/.../feedback_vn_accounting_no_hardcoded_accounts.md`).

### 1.2 Mục tiêu

1. **15 sidebar items mới** triển khai theo phase, ưu tiên LCV (universal) → Tổng hợp → BCTC → Giá thành SX.
2. **Foundation no-hardcoded-TK**: tất cả TK mapping qua Settings DocType (sửa được), với default seed theo TT99/2025.
3. **TT99/2025 đúng**: form codes (B01/B02/B03/B09/S03a/S03b-DN), tên báo cáo, layout Excel theo Phụ lục IV.
4. **Drill-down**: mỗi số trên báo cáo BCTC click được xuống chứng từ gốc (Phiếu kế toán / Hóa đơn).
5. **Excel xuất đúng layout TT99/2025** — nộp thuế trực tiếp không cần chỉnh.

### 1.3 Phạm vi (Phase 1)

**Trong phạm vi:**
- 15 items đã chốt (BL §11-14, FEATURES C7-C10)
- 4 báo cáo BCTC cho **DN hoạt động liên tục** (B01/B02/B03/B09-DN)
- LCV cho cả mua trong nước + nhập khẩu
- Giá thành sản xuất cơ bản (621/622/627 → 154 → 155)
- Kết chuyển cuối kỳ (911) + Khóa sổ kỳ (Period Closing Voucher)

**Ngoài phạm vi (phase sau):**
- Bộ DN không liên tục (B01/B02/B03/B09-DNKLT) — chờ Company thực tế cần dùng
- B03-DN phương pháp trực tiếp (gián tiếp đủ cho 95% DN)
- BCTC hợp nhất công ty con
- BCTC theo IFRS song song
- Giá thành xây lắp / công đoạn nhiều cấp
- Tờ khai thuế (GTGT, TNDN, TNCN) — section riêng `C3`

---

## 2. Quyết định thiết kế (chốt)

| # | Quyết định | Lý do |
|---|---|---|
| D1 | **No hardcoded TK** xuyên suốt. Mọi TK qua Settings DocType (single-source-of-truth) | Cross-cutting feedback rule, DN có COA chi tiết khác nhau |
| D2 | **4 Settings DocTypes mới**: `LCV Allocation Settings` (Single), `Manufacturing Costing Settings` (Single), `BCTC Mapping` (per-Company), `Period Closing Account Settings` (extend VN Accounting Settings existing) | Tách scope theo nghiệp vụ, dễ maintain |
| D3 | **BCTC Mapping per-Company** (không phải Single) — clone từ template TT99/2025 khi tạo Company VN | DN có thể tùy chỉnh độc lập, không share toàn site |
| D4 | **Mapping formula syntax đơn giản**: `+TK,+TK,-TK` với wildcard `511%`. Loại số liệu: `closing_debit / closing_credit / period_debit / period_credit / formula` | Kế toán phải đọc được, không phải dev. Tránh expression engine phức tạp |
| D5 | **Reuse ERPNext LCV** thay vì viết DocType mới | LCV đã có đầy đủ logic phân bổ; vn_accounting chỉ wire-up defaults + giao diện VN |
| D6 | **Reuse ERPNext Period Closing Voucher** cho Khóa sổ | Đã có sẵn check + lock; vn_accounting bổ sung validation cân đối + audit log |
| D7 | **Wizard kết chuyển 911 = Page (không phải DocType)** | Wizard không lưu state — chỉ preview + sinh JE nháp |
| D8 | **Wizard tính giá thành = Page** | Tương tự — sinh JE nháp + cập nhật Stock Entry nhập kho TP |
| D9 | **B01-DN tên mới "Báo cáo tình hình tài chính"** trong mọi UI surface (sidebar, report title, Excel filename, translations) | TT99/2025 mandatory |
| D10 | **Click-through drill** trên báo cáo BCTC: click số → list chứng từ gốc filtered theo công thức của mã chỉ tiêu | Audit/kiểm toán cần truy vết |
| D11 | **Phase order**: Foundation Settings → LCV → Tổng hợp → BCTC → Giá thành SX → Sidebar wire-up | LCV universal nhất, build trước; Giá thành SX phụ thuộc Settings + only manufacturing DN cần |
| D12 | **Sidebar mỗi item link DocType + route_options sticky** (theo pattern A3.4) | Pattern đã chốt cho vn_accounting |
| D13 | **English source + vi.csv translations** (pattern A8.1) | i18n convention đã chốt |
| D14 | **B09-DN sinh Excel đa sheet (option B)**: Sheet 1 "Phần I-IV+VI văn xuôi" + Sheet 2-N "Phần V chi tiết khoản mục" (mỗi sheet 1 bảng) | Phần V có nhiều dòng (vd: chi tiết 131 có thể 500 KH) → 1 sheet riêng dễ filter/sort. Excel mạnh hơn Word cho bảng số liệu |
| D15 | **Excel xuất qua openpyxl** với template layout từng báo cáo | Layout TT99/2025 cố định, không cần dynamic styling phức tạp |
| D16 | **B03-DN phase 1 chỉ làm phương pháp gián tiếp.** Trực tiếp ra phase 2 khi có DN niêm yết yêu cầu | 90% DN VN dùng gián tiếp. Trực tiếp cần mapping TK đối ứng → loại dòng tiền (3-4 sessions decompose) — không tương xứng nếu chưa có user |
| D17 | **Wizard kết chuyển default Select all** — toàn bộ TK 511/515/711/632/635/641/642/811/821 tích sẵn. TK không phát sinh tự skip. TK loại trừ vĩnh viễn cấu hình trong Settings, không bắt uncheck mỗi kỳ | 99% kỳ kết chuyển hết. Select none làm chậm + tăng nguy cơ kế toán quên 1 TK |
| D18 | **3333 thuế NK là TK trung gian phải nộp NSNN**, luôn cộng vào giá vốn theo luật VAS. Có toggle "Có chịu thuế nhập khẩu?" cho DN khu chế xuất / tạm nhập tái xuất / gia công XK | Đính chính nhầm lẫn trong bản draft đầu — 3333 không trực tiếp là cost account, mà là liability TK với cơ chế Dr 156 / Cr 3333 |
| D19 | **BCTC Mapping per-Company** (đã chốt) + 2 nút trợ giúp: "Copy mapping từ Company khác" + "Khôi phục mặc định TT99/2025" (per-line + per-report) | Mỗi DN có COA chi tiết khác → cần độc lập. RAM cost vài MB không là vấn đề. 2 nút trợ giúp giải quyết case sync nhiều Company cùng nhóm |
| D20 | **Khóa sổ kỳ — chỉ Role "Accounts Manager" (KTT) được Submit + Cancel.** System Manager + Accounts User chỉ xem. Bắt buộc nhập "Lý do" khi submit/cancel. Audit log không xóa được | User yêu cầu — chỉ KTT là master accounting có quyền |
| D21 | **UI inline guidance mandatory** trên mọi surface: field descriptions, button tooltips, wizard help panels, report column hints, settings example values, empty states, error messages. Link "Xem hướng dẫn chi tiết" mở vn_help article | Cross-cutting feedback rule (xem `feedback_ui_inline_guidance.md`): phần mềm mới, users chưa quen |

---

## 3. Schema thay đổi

### 3.1 LCV Allocation Settings (Single DocType — mới)

**Module:** `vn_accounting/landed_cost`

**Fields:**

| Fieldname | Type | Reqd | Default | Description |
|---|---|---|---|---|
| expense_types | Table (child: LCV Expense Type Setting) | 1 | (seeded) | Danh sách 12 loại phụ phí + TK mặc định |
| auto_apply_settings_on_new_lcv | Check | 0 | 1 | Tự fill TK khi tạo LCV mới |
| import_vat_default_deductible_pct | Float | 1 | 100 | % VAT nhập khẩu mặc định được khấu trừ |

**Child DocType: LCV Expense Type Setting**

| Fieldname | Type | Description |
|---|---|---|
| expense_type | Data | "Vận chuyển" / "Bảo hiểm" / "Thuế NK" / ... |
| expense_type_key | Data | Stable key: `shipping` / `insurance` / `import_duty` / ... |
| default_expense_account | Link (Account) | TK mặc định (cộng giá vốn hoặc khấu trừ) |
| is_import_only | Check | 1 nếu loại này chỉ dùng cho nhập khẩu |
| allocation_method | Select (Amount / Qty / Weight / Volume) | Tiêu thức phân bổ gợi ý |

**Seed defaults (12 dòng):**

| key | expense_type | default_account_role | is_import_only | method |
|---|---|---|---|---|
| shipping | Vận chuyển | Stock account (156/152 tùy item) | 0 | Weight hoặc Amount |
| handling | Bốc xếp | Stock account | 0 | Amount |
| insurance | Bảo hiểm hàng hóa | Stock account | 0 | Amount |
| storage | Lưu kho, lưu bãi | Stock account | 0 | Amount |
| commission | Hoa hồng mua hàng | Stock account | 0 | Amount |
| import_duty | Thuế nhập khẩu | **3333 (TK trung gian phải nộp NSNN)** | 1 | Amount |
| special_consumption_tax | Thuế TTĐB nhập khẩu | **3332 (TK trung gian phải nộp NSNN)** | 1 | Amount |
| import_vat_deductible | VAT NK (khấu trừ) | 1331 (TK thuế GTGT đầu vào được khấu trừ) | 1 | Amount |
| import_vat_non_deductible | VAT NK (không khấu trừ) | Stock account | 1 | Amount |
| customs_fee | Phí hải quan, kiểm dịch | Stock account | 1 | Amount |
| container_demurrage | Phí lưu cont, lưu bãi | Stock account | 1 | Amount |
| customs_agent_fee | Phí đại lý hải quan | Stock account | 1 | Amount |

**Quan trọng — cơ chế bút toán LCV cho thuế NK + TTĐB (đính chính bản draft):**

TK 3333 (thuế NK) và 3332 (TTĐB NK) là **TK PHẢI TRẢ NSNN**, không phải cost account. Cơ chế bút toán LCV sinh ra:

```
Khi nhập khẩu (LCV submit):
Nợ 156/152 (giá CIF + thuế NK + TTĐB + phí phụ cộng giá vốn)
    Có 331 (phải trả NCC nước ngoài) — phần giá CIF
    Có 3333 (thuế NK chờ nộp NSNN)
    Có 3332 (thuế TTĐB chờ nộp NSNN)
    Có 1331 (VAT NK được khấu trừ — phần khấu trừ)

Khi nộp thuế cho NSNN (giao dịch RIÊNG, không qua LCV):
Nợ 3333 / Có 111 hoặc 112
```

Vậy thuế NK + TTĐB **LUÔN cộng vào giá vốn** (theo VAS — yêu cầu pháp lý), KHÔNG có toggle tắt. Toggle chỉ có ở mức "có chịu thuế NK hay không" (3 trường hợp đặc thù dưới).

**Lookup logic "Stock account":** lookup từ Item của dòng LCV (`item.default_inventory_account` per company → fallback Company `stock_received_but_not_billed`). Khi user thay TK trên LCV row, override per-row.

**Toggle "Có chịu thuế nhập khẩu?" trên LCV nhập khẩu:**

Field mới trên Landed Cost Voucher (Custom Field): `vn_is_subject_to_import_duty` (Check, default=1, depends_on=`is_import_lcv`).

Khi uncheck → ẩn 2 dòng `import_duty` + `special_consumption_tax` khỏi grid LCV expenses. Áp dụng cho:

| Trường hợp | Lý do |
|---|---|
| DN trong khu chế xuất / khu thương mại tự do | Miễn thuế NK theo Luật Thuế XK-NK |
| Tạm nhập tái xuất | Không thuộc đối tượng nộp |
| Hàng nhập về để gia công xuất khẩu | Miễn / hoàn thuế NK |

UI guidance: tooltip trên toggle: "Mặc định DN nhập khẩu thông thường phải nộp thuế NK. Bỏ tick nếu DN trong khu chế xuất, tạm nhập tái xuất, hoặc nhập NVL để gia công xuất khẩu."

### 3.2 Manufacturing Costing Settings (Single DocType — mới)

**Module:** `vn_accounting/costing`

**Fields:**

| Fieldname | Type | Reqd | Default | Description |
|---|---|---|---|---|
| direct_material_account | Link (Account) | 1 | 621 lookup | TK NVL trực tiếp |
| direct_labor_account | Link (Account) | 1 | 622 lookup | TK nhân công trực tiếp |
| manufacturing_overhead_account | Link (Account) | 1 | 627 lookup | TK SXC |
| work_in_progress_account | Link (Account) | 1 | 154 lookup | TK SP dở dang |
| finished_goods_account | Link (Account) | 1 | 155 lookup | TK thành phẩm |
| cost_of_goods_sold_account | Link (Account) | 1 | 632 lookup | TK giá vốn |
| cost_object | Select | 1 | "Item" | "Item" / "Work Order" / "Project" / "Customer" / "Sales Order" |
| overhead_allocation_basis | Select | 1 | "Machine Hours" | "Machine Hours" / "Direct Labor Hours" / "Production Volume" / "Direct Material Cost" / "Direct Labor Cost" / "Total Direct Cost" |
| wip_valuation_method | Select | 1 | "Equivalent Production" | "Equivalent Production" / "Direct Material Only" / "50% Conversion Cost" |
| auto_hide_for_small_enterprise | Check | 1 | 1 | Tự ẩn 621/622/627 nếu Company dùng mẫu COA nhỏ |
| transfer_to_finished_goods | Check | 1 | 1 | DN sản xuất hàng hóa → tick (kết chuyển 154 → 155). DN dịch vụ / xây lắp → untick (kết chuyển 154 → 632 trực tiếp, không qua 155) |
| services_cogs_account | Link (Account) | 0 | 632 lookup | Chỉ dùng khi `transfer_to_finished_goods=0`. TK giá vốn dịch vụ/xây lắp |

**Lookup helper:** mỗi field có giá trị mặc định lookup TK theo prefix code khi tạo Company VN.

### 3.3 Period Closing Account Settings (Extend VN Accounting Settings)

**Module:** `vn_accounting/settings`

**Fields mới thêm vào DocType `VN Accounting Settings` (Single, đã tồn tại):**

| Fieldname | Type | Reqd | Default | Description |
|---|---|---|---|---|
| pnl_account_911 | Link (Account) | 1 | 911 lookup | TK xác định KQKD |
| retained_earnings_current_year | Link (Account) | 1 | 4212 lookup | TK lãi/lỗ kỳ |
| retained_earnings_prior_year | Link (Account) | 1 | 4211 lookup | TK lãi/lỗ năm trước |
| revenue_accounts_to_close | Table (child: Account List Item) | 1 | (seeded 511,512,515,711) | TK doanh thu kết chuyển |
| expense_accounts_to_close_periodic | Table (child: Account List Item) | 1 | (seeded 632,635,641,642,811) | TK chi phí kết chuyển hàng kỳ (tháng/quý) — **KHÔNG bao gồm 821** |
| corporate_income_tax_account | Link (Account) | 1 | 821 lookup | TK chi phí thuế TNDN — chỉ kết chuyển vào kỳ NĂM TÀI CHÍNH |
| period_closing_balance_tolerance | Currency | 0 | 1 | Sai số cho phép khi check cân đối (đơn vị tiền) |

**Lý do tách 821:** TK 821 (chi phí thuế TNDN) thường tích lũy cả năm và kết chuyển 1 lần vào cuối năm tài chính. Workflow chuẩn:

- **Kết chuyển hàng kỳ (tháng/quý):** doanh thu (511/512/515/711) + chi phí (632/635/641/642/811) trừ 821 → 911 → 4212. 821 KHÔNG xuất hiện trong wizard.
- **Kết chuyển năm tài chính:** chạy thêm lần riêng. Trước đó kế toán đã ghi JE TNDN (Nợ 821 / Có 3334) bằng tay. Wizard kết chuyển năm tự include 821 vào danh sách.

Wizard sẽ tự detect kỳ kết chuyển = năm tài chính hay không → include hoặc exclude 821 tương ứng.

**Child DocType: Account List Item** (reusable child)

| Fieldname | Type |
|---|---|
| account | Link (Account) |
| note | Small Text (optional) |

### 3.4 BCTC Mapping (per-Company DocType — mới)

**Module:** `vn_accounting/financial_reporting`

**Naming:** `BCTC Mapping {company}` — 1 record per Company, auto-created khi Company set country=Vietnam.

**Fields:**

| Fieldname | Type | Description |
|---|---|---|
| company | Link (Company) | Reqd, unique |
| coa_template | Data | "vn_large_enterprise" / "vn_small_enterprise" — auto-detect |
| b01_lines | Table (child: BCTC Line) | Mapping cho B01-DN (~50 mã chỉ tiêu) |
| b02_lines | Table (child: BCTC Line) | Mapping cho B02-DN (~18 mã) |
| b03_lines | Table (child: BCTC Line) | Mapping cho B03-DN (~30 mã) |
| b09_template_path | Data | Đường dẫn template Word cho B09 (mặc định: app's template/b09_dn_template.docx) |
| last_restored_from_default | Datetime | Lần cuối "Khôi phục mặc định TT99/2025" |

**Child DocType: BCTC Line**

| Fieldname | Type | Description |
|---|---|---|
| code | Data | "110", "01", ... — read-only sau khi seed |
| name | Data | "Tiền và các khoản tương đương tiền" — read-only |
| section | Data | "TÀI SẢN NGẮN HẠN", "DOANH THU", ... — heading group |
| value_type | Select | `closing_debit` / `closing_credit` / `period_debit` / `period_credit` / `formula` |
| account_formula | Long Text | `+111,+112,+113` hoặc `+511%,-521%` — wildcard supported |
| line_formula | Long Text | Nếu value_type=formula: `=10-11` (mã 10 trừ mã 11) |
| display_indent | Int | 0,1,2,3 — độ thụt lề khi render |
| is_subtotal | Check | 1 nếu là dòng tổng (in đậm trong báo cáo) |
| sign_multiplier | Select | `+1` / `-1` — đảo dấu nếu cần |
| note | Small Text | Diễn giải cho kế toán đọc khi cấu hình |

**Seeding:**
- File fixture: `vn_accounting/fixtures/bctc_template_b01_large.json` + tương tự cho b02, b03 và bộ small_enterprise.
- Seed function chạy 1 lần khi cài app → lưu vào DocType ẩn `BCTC Mapping Template` (1 record per template).
- Khi tạo Company → clone template tương ứng vào `BCTC Mapping {company}`.

**2 nút trợ giúp trên form BCTC Mapping** (custom button):

| Nút | Hành vi | UI guidance |
|---|---|---|
| **"Copy mapping từ Company khác"** | Mở dialog chọn source Company → preview diff (mã chỉ tiêu nào sẽ thay đổi) → xác nhận overwrite | Tooltip: "Sao chép toàn bộ công thức mapping từ một Công ty khác. Hữu ích khi nhiều Công ty trong nhóm dùng cùng cấu trúc tài khoản. Có thể preview trước khi áp dụng." |
| **"Khôi phục mặc định TT99/2025"** | Có 2 mode: "Toàn bộ báo cáo" (chọn B01/B02/B03) hoặc "Riêng dòng này" (mode row-level). Confirm trước khi rollback | Tooltip: "Khôi phục công thức mã chỉ tiêu về mặc định TT99/2025 nếu sửa nhầm. Có thể rollback toàn bộ báo cáo hoặc chỉ 1 dòng." |

### 3.5 Work In Progress Valuation (DocType — mới)

**Module:** `vn_accounting/costing`

**Naming:** `WIP-{YYYY-MM}-{cost_object_short}` — 1 record per cost object per period.

**Fields:**

| Fieldname | Type | Reqd | Description |
|---|---|---|---|
| company | Link (Company) | 1 | |
| posting_date | Date | 1 | Ngày kết thúc kỳ |
| cost_object_type | Select | 1 | Same as Manufacturing Costing Settings.cost_object |
| cost_object_id | Dynamic Link | 1 | Item / Work Order / Project / ... |
| period_start | Date | 1 | |
| period_end | Date | 1 | |
| valuation_method | Select | 1 | Inherited from Settings |
| opening_wip_value | Currency | 0 | Số dư DD đầu kỳ (auto lookup) |
| period_direct_material | Currency | 0 | 621 phát sinh kỳ |
| period_direct_labor | Currency | 0 | 622 phát sinh kỳ |
| period_overhead_allocated | Currency | 0 | 627 phân bổ vào đối tượng |
| closing_wip_value | Currency | 1 | Số DD cuối kỳ (kế toán nhập trực tiếp HOẶC computed từ equivalent production fields dưới) |
| valuation_method | Select | 1 | "Direct Input" / "Equivalent Production" / "Direct Material Only" / "50% Conversion Cost" — inherited from Settings, override per record |
| physical_units_in_progress | Float | 0 | (Chỉ dùng nếu valuation_method=Equivalent Production) Số SP dở dang vật lý |
| equivalent_completion_pct | Percent | 0 | (Chỉ dùng nếu valuation_method=Equivalent Production) Tỷ lệ % hoàn thành chi phí chế biến của SP dở dang. Vd: 60% nghĩa là DDCK đã hoàn thành 60% công đoạn |
| computed_closing_wip | Currency | 0 | (Read-only, auto-compute) Theo phương pháp: Direct Input → = closing_wip_value (manual); Equivalent Production → = physical_units × completion_pct × period_unit_cost_estimate; Direct Material Only → = physical_units × material_cost_per_unit; 50% Conversion Cost → = physical_units × (material_cost + 50% × conversion_cost) |
| completed_quantity | Float | 1 | Sản lượng hoàn thành |
| unit_cost | Currency | (computed) | (open+pd+pl+oh-closing)/completed_qty |
| total_finished_goods_value | Currency | (computed) | unit_cost × completed_quantity |
| linked_costing_je | Link (Journal Entry) | 0 | JE 621/622/627 → 154 |
| linked_fg_je | Link (Journal Entry) | 0 | JE 154 → 155 |
| status | Select | 1 | "Draft" / "Calculated" / "Posted" / "Cancelled" |

**Submittable: No** (chỉ status workflow, không docstatus). 

### 3.6 Phiếu khóa sổ kỳ — extend ERPNext `Period Closing Voucher`

Không thêm DocType mới. Bổ sung:

1. **Custom Field `vn_lock_unlock_reason` (Long Text, reqd=1)** — bắt buộc nhập lý do khi Submit (khóa) hoặc Cancel (mở khóa). Lý do được ghi vĩnh viễn vào Comment + Activity Log.

2. **Hook `validate`** trên Period Closing Voucher:
   - Reject nếu có JE nháp trong kỳ (`docstatus=0`)
   - Reject nếu Bảng cân đối số phát sinh lệch quá `tolerance` (Settings)
   - Reject nếu chưa có JE kết chuyển 911 trong kỳ (check theo posting_date + memo tag `[KETCHUYEN-911]`)
   - Reject nếu `vn_lock_unlock_reason` trống

3. **Hook `on_submit`:** ghi audit log entry vào Comment với người ký + ngày + lý do (clone từ `vn_lock_unlock_reason`).

4. **Hook `on_cancel`:** validate lý do mở khóa đã nhập + ghi audit log.

5. **DocPerm (override qua Property Setter hoặc Custom DocPerm fixture):**
   ```
   Period Closing Voucher:
     Accounts Manager: read=1, write=1, create=1, submit=1, cancel=1, delete=0
     System Manager: read=1, write=0, create=0, submit=0, cancel=0, delete=0
     Accounts User: read=1, others=0
   ```
   - **Chỉ Accounts Manager (Kế toán trưởng) khóa/mở khóa.** System Manager xem-only.
   - delete=0 cho tất cả — phiếu khóa sổ không xóa được, chỉ cancel.

6. **Custom Field trên Company:** `vn_operating_status` (Select: "Going Concern" / "Dissolution" / "Bankruptcy" / "Ceased Operations") — phục vụ phase sau cho bộ KLT.

7. **UI guidance trên form Period Closing Voucher:**
   - Header help panel: "Phiếu khóa sổ kỳ kế toán — chỉ Kế toán trưởng được tạo/duyệt/hủy. Khi khóa, mọi chứng từ trong kỳ không thể sửa hoặc xóa. Mở khóa chỉ trong trường hợp đặc biệt (kiểm toán phát hiện sai sót lớn). Mọi thao tác đều có audit log không thể xóa."
   - Field `vn_lock_unlock_reason` description: "Bắt buộc. Nhập lý do khóa/mở khóa kỳ. Lý do được lưu vĩnh viễn để truy vết kiểm toán. Vd: 'Khóa sổ tháng 4/2026 sau khi đối chiếu xong số liệu' hoặc 'Mở khóa tháng 3/2026 do kiểm toán Big4 phát hiện sai sót định khoản TK 632 cần điều chỉnh'."
   - Tooltip nút Submit: "Khóa sổ kỳ này. Sau khi khóa, chứng từ trong kỳ không sửa/xóa được. Chỉ Kế toán trưởng được mở khóa lại."
   - Tooltip nút Cancel: "Mở khóa kỳ đã đóng. Chỉ dùng khi có lý do nghiệp vụ (kiểm toán, sai sót lớn). Phải nhập lý do."

---

## 4. Wizards & Reports

### 4.1 Wizard Kết chuyển cuối kỳ (Page `period-closing-911`)

**Module:** `vn_accounting/period_closing/page/period_closing_911`

**Layout:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Kết chuyển cuối kỳ                       [Cấu hình tài khoản ⚙]│
├─────────────────────────────────────────────────────────────────┤
│ Công ty: [DCNET ▼]    Kỳ: [Tháng 04/2026 ▼]    Ngày: [30/04/26]│
├─────────────────────────────────────────────────────────────────┤
│ BƯỚC 1 — KẾT CHUYỂN DOANH THU & THU NHẬP VỀ 911                │
│ ┌──┬───────┬─────────┬─────────┬──────────┬───────────┬──────┐│
│ │☑│TK     │Tên      │Dư Có    │TK đích   │Loại trừ?  │Sửa  ││
│ ├──┼───────┼─────────┼─────────┼──────────┼───────────┼──────┤│
│ │☑│511    │Doanh... │125.000K │911       │ ☐         │ ✎    ││
│ │☑│515    │DT TC    │  3.500K │911       │ ☐         │ ✎    ││
│ │☑│711    │Thu khác │    800K │911       │ ☐         │ ✎    ││
│ └──┴───────┴─────────┴─────────┴──────────┴───────────┴──────┘│
│ BƯỚC 2 — KẾT CHUYỂN CHI PHÍ VỀ 911                            │
│ (bảng tương tự)                                                │
│ BƯỚC 3 — XÁC ĐỊNH KẾT QUẢ — KQKD = +XX,XXX → Nợ 911/Có 4212  │
├─────────────────────────────────────────────────────────────────┤
│ [Preview JE]    [Tạo 3 JE nháp]                                │
└─────────────────────────────────────────────────────────────────┘
```

**Auto-detect kỳ — include 821 hay không:**

Khi mở wizard, hệ thống kiểm tra `period_end` có trùng với ngày cuối năm tài chính của Company không:

- `period_end == fiscal_year_end_date` → **kỳ NĂM TÀI CHÍNH**: wizard include 821 vào danh sách kết chuyển. Banner: "Kết chuyển năm tài chính. TK 821 (chi phí thuế TNDN) sẽ được kết chuyển. Đảm bảo đã ghi JE TNDN tạm tính + quyết toán trước khi chạy wizard này."
- `period_end != fiscal_year_end_date` → **kỳ tháng/quý**: wizard EXCLUDE 821. Banner: "Kết chuyển kỳ tháng/quý. TK 821 sẽ KHÔNG kết chuyển trong kỳ này (chỉ kết chuyển vào cuối năm tài chính)."

Wizard có override checkbox "Bao gồm TK 821 trong kỳ này?" (default theo auto-detect) — KTT có thể tick/untick nếu DN có quy ước riêng.

**API endpoints:**

- `vn_accounting.period_closing.get_closing_preview(company, period_start, period_end)` → returns:
  - `is_fiscal_year_end: bool` (auto-detected)
  - `revenue_je_preview` — bút toán doanh thu → 911
  - `expense_je_preview` — bút toán chi phí → 911 (include/exclude 821 theo auto-detect)
  - `result_je_preview` — bút toán 911 → 4212
- `vn_accounting.period_closing.create_closing_journal_entries(company, period_end, mappings, include_tax_account)` → creates 3 draft JE, returns names

**Validation:**
- Mỗi TK trong revenue/expense list có số dư = 0 trong kỳ → tự skip (không tạo row vô nghĩa trong JE)
- Kế toán có thể loại trừ TK bằng checkbox (ghi nhớ trong session, không lưu vào Settings)
- Trước khi tạo: cảnh báo nếu có TK ngoại tệ chưa đánh giá lại (lookup `JE.memo like '[FX-REVAL]%'` trong kỳ)
  - **Phase 1 không có wizard "Đánh giá lại tỷ giá ngoại tệ"**. KTT làm thủ công qua Phiếu kế toán: Nợ/Có 413 ↔ TK gốc ngoại tệ (1112, 1122, 131, 331). Phase 2 sẽ có wizard riêng. Banner cảnh báo có link tới article vn_help giải thích cách làm thủ công.
- Nếu là kỳ năm tài chính: cảnh báo nếu chưa có JE TNDN tạm tính (lookup `JE.memo like '[TNDN-%]%'` hoặc check phát sinh Nợ 821 trong kỳ = 0)

### 4.2 Wizard Tính giá thành (Page `manufacturing-costing-wizard`)

**Module:** `vn_accounting/costing/page/manufacturing_costing_wizard`

**Flow (rẽ nhánh theo `transfer_to_finished_goods` setting):**

```
Step 1: Chọn kỳ + đối tượng (auto-detect transfer_to_finished_goods từ Settings)
Step 2: Kiểm tra tập hợp 621/622/627 (báo cáo inline)
Step 3: Nhập WIP Valuation (1 row per cost object) — chọn valuation_method, nhập số liệu DDCK
Step 4: Phân bổ 627 (tự động theo basis từ Settings, có thể override)
Step 5: Bảng tính giá thành — preview unit_cost per object
Step 6: Preview JE (rẽ nhánh):
        - transfer_to_finished_goods=1 (DN sản xuất): 2 JE (621/622/627 → 154 + 154 → 155)
        - transfer_to_finished_goods=0 (DN dịch vụ/xây lắp): 2 JE (621/622/627 → 154 + 154 → 632 services_cogs_account)
        Mỗi dòng có nút "Sửa TK" để override per-record
Step 7a (DN sản xuất): Sinh 2 JE nháp + N Stock Entry nhập kho thành phẩm
Step 7b (DN dịch vụ/xây lắp): Sinh 2 JE nháp (KHÔNG có Stock Entry)
```

**UI guidance trên Step 6 banner:**
- Nếu DN sản xuất: "Kết chuyển giá thành về thành phẩm (TK 155). Sản phẩm hoàn thành sẽ được nhập kho TP, sẵn sàng xuất bán."
- Nếu DN dịch vụ/xây lắp: "Kết chuyển giá thành về giá vốn dịch vụ/xây lắp (TK 632) trực tiếp, không qua thành phẩm. Áp dụng cho dịch vụ đã cung cấp hoặc công trình đã nghiệm thu trong kỳ."

**Xử lý nghiệm thu công trình từng phần (xây lắp):**

Trên Step 3, kế toán có thể tick "Kết chuyển toàn bộ đối tượng này" hay không:
- Tick: closing_wip_value = 0 (toàn bộ ra 632)
- Untick: nhập closing_wip_value > 0 (phần dở dang còn lại). Phần `(opening + period_costs − closing) / completed_qty` × completed_qty ra 632.

Tham chiếu §4.7 cho hướng dẫn Project setup xây lắp đầy đủ.

**API endpoints:**
- `vn_accounting.costing.aggregate_production_costs(company, period_start, period_end, cost_object_type)` → bảng tập hợp
- `vn_accounting.costing.calculate_unit_costs(wip_valuations: list)` → bảng giá thành đơn vị + auto-compute closing_wip nếu valuation_method != "Direct Input"
- `vn_accounting.costing.create_costing_journal_entries(company, posting_date, calculations, account_overrides, transfer_mode)` → JE + N Stock Entry nháp (nếu transfer_mode="finished_goods") hoặc chỉ JE (nếu transfer_mode="cogs_direct")

### 4.3 Báo cáo BCTC engine

**Module:** `vn_accounting/financial_reporting/report`

**Core function:**

```python
def resolve_bctc_line(company, line: BCTCLine, period_start, period_end):
    """
    Returns: Decimal value for this line in this period.
    Recursive for line_formula referencing other line codes.
    Uses account_formula syntax: +TK,+TK,-TK (with wildcard).
    """
```

**4 Reports (Script Report type, không Query Report):**

1. `b01_dn_bao_cao_tinh_hinh_tai_chinh` — module/report/b01_dn_bao_cao_tinh_hinh_tai_chinh/
2. `b02_dn_bao_cao_kqhdkd`
3. `b03_dn_bao_cao_lctt`
4. `b09_dn_thuyet_minh_bctc` — sinh Word output, không phải bảng

Mỗi report:
- Filter: Company + Period (Year/Quarter/Month) + As-of-date (B01) hoặc Period-range (B02, B03)
- Columns: Mã | Tên chỉ tiêu | Kỳ này | Kỳ trước
- Hover icon ℹ → hiện công thức (`+111,+112,+113` → "Tổng số dư Nợ cuối kỳ TK 111+112+113")
- Click số → drill xuống danh sách GL Entry filtered theo công thức
- Nút **"Cấu hình mapping"** → mở BCTC Mapping của Company
- Nút **"Xuất Excel"** → file XLSX layout TT99/2025

### 4.4 Sổ nhật ký chung (S03a-DN) & Sổ cái (S03b-DN)

**2 báo cáo mới** (Script Report):

1. `s03a_dn_so_nhat_ky_chung`
   - Cols: Ngày | Số CT | Loại CT | Diễn giải | TK Nợ | TK Có | PS Nợ | PS Có
   - Filter: Company + Period
   - Sort: posting_date ASC, sau đó creation ASC
   - Layout xuất Excel theo Phụ lục III TT99/2025

2. `s03b_dn_so_cai`
   - Layout 1 TK / trang (hoặc filter chọn TK)
   - Cols: Ngày | Số CT | Diễn giải | TK đối ứng | PS Nợ | PS Có | Dư Nợ | Dư Có (lũy kế)
   - Differs from existing A2.2 `Account Detail Ledger`: A2.2 dùng cho mọi format, S03b-DN có cấu trúc cố định TT99/2025 + xuất Excel đúng mẫu.

### 4.5 Báo cáo phụ trợ

- **`landed_cost_pending_allocation`** (Script Report) — list các chi phí treo trên 1388/331 chưa link tới Phiếu nhập mua. Cols: Ngày | Số CT | Nhà cung cấp | Số tiền | TK | Diễn giải | [Tạo LCV]
- **`production_cost_aggregation`** (Script Report) — 621/622/627 theo cost object kỳ.

### 4.6 B09-DN Excel multi-sheet generator (option B chốt từ D14)

**Module:** `vn_accounting/financial_reporting/b09_dn`

**Page:** `b09-dn-generator` (Frappe Page, không phải Script Report vì output là file Excel)

**Flow:**
1. Kế toán mở page → chọn Company + Kỳ (Năm tài chính / Quý).
2. Nhấn "Sinh file B09-DN" → backend dùng `openpyxl` build file Excel theo cấu trúc dưới.
3. File tải về máy → kế toán mở, điền văn xuôi, đối chiếu chi tiết, lưu lại để nộp.

**Cấu trúc Excel output:**

| Sheet | Tên hiển thị | Nội dung | Trạng thái cell |
|---|---|---|---|
| 1 | `1_Van_xuoi` | Phần I (Đặc điểm hoạt động DN) + II (Kỳ kế toán, đơn vị tiền tệ) + III (Chuẩn mực và chế độ kế toán áp dụng) + IV (Chính sách kế toán chi tiết — khấu hao, dự phòng, đánh giá ngoại tệ...) + VI (Sự kiện sau ngày kết thúc niên độ + cam kết quan trọng) | Cell merged. App fill **khung mẫu chuẩn TT99/2025** với placeholder `[Kế toán điền: tên đầy đủ + địa chỉ DN + ngành nghề chính]`. Kế toán xóa placeholder, điền văn xuôi |
| 2 | `5.1_Chi_tiet_phai_thu` | Phần V.1 — chi tiết TK 131 theo từng khách hàng + tuổi nợ (0-30 / 31-60 / 61-90 / >90 ngày) + dự phòng 2293 | App auto-fill từ GL + customer aging report. Read-only cho cột số liệu, editable cho cột "Ghi chú" |
| 3 | `5.2_Chi_tiet_phai_tra` | Phần V.2 — chi tiết TK 331 theo nhà cung cấp + tuổi nợ | Auto-fill |
| 4 | `5.3_Bien_dong_TSCD` | Phần V.3 — bảng biến động TSCĐ kỳ theo nhóm (nhà cửa / máy móc / phương tiện / TBVP / TSCĐ khác): nguyên giá đầu kỳ + tăng + giảm + cuối kỳ; tương tự cho khấu hao luỹ kế + giá trị còn lại | Auto-fill từ Asset module + Asset Movement |
| 5 | `5.4_Bien_dong_HTK` | Phần V.4 — chi tiết tồn kho TK 151/152/153/154/155/156/157 theo nhóm/SKU + dự phòng giảm giá 2294 | Auto-fill từ Stock + Item Group |
| 6 | `5.5_Chi_tiet_vay` | Phần V.5 — chi tiết khoản vay (3411 + 3412): NH/đối tác cho vay, hạn trả, lãi suất, dư nợ đầu kỳ + tăng + giảm + cuối kỳ | Auto-fill từ Bank Loan |
| 7 | `5.6_Bien_dong_VCSH` | Phần V.6 — biến động vốn chủ sở hữu (TK 411, 412, 414, 418, 421...) trong kỳ: số đầu kỳ + tăng (góp vốn, bổ sung từ LNST) + giảm (chia cổ tức, chia LN) + cuối kỳ | Auto-fill |
| 8-N | `5.7_...` đến `5.X_...` | Các mục V khác có dữ liệu trong kỳ: chi phí trả trước, dự phòng phải trả, ngoại bảng 001-008 | Auto-fill conditional (chỉ sinh sheet nếu có dữ liệu) |

**UI guidance:**
- Header help panel trên page: "Sinh khung Thuyết minh BCTC (B09-DN) theo TT99/2025. App tự fill phần số liệu (sheet 5.x). Kế toán trưởng điền văn xuôi vào sheet 1 (đặc điểm DN, chính sách kế toán) trước khi nộp."
- Mỗi sheet có row đầu là tiêu đề + ghi chú "Hướng dẫn điền: ..." để kế toán biết cell nào cần edit, cell nào auto-fill (đừng đè).
- Cell auto-fill có background xám nhạt + lock không cho edit (`worksheet.protection.enable()`); cell kế toán điền background trắng + không lock.

### 4.7 Project setup guide cho DN xây lắp (chốt từ Q5)

DN xây lắp dùng `cost_object_type = "Project"` trong Manufacturing Costing Settings. Em ship 1 hướng dẫn step-by-step + auto-validation hỗ trợ.

**Module:** `vn_accounting/costing/project_setup_guide`

**Tạo Article trong vn_help:** `vn_help/articles/co/du-an-xay-lap-setup.md` — đầy đủ hướng dẫn + screenshot. UI tab "Costing" trên Project form có link "Xem hướng dẫn chi tiết" → mở article.

**Quy ước đặt tên Project (gợi ý trong UI guidance):**
- Naming: `{Năm}-{Mã CT}-{Tên ngắn}` — vd: `2026-NS01-NhaXuongDCNET`
- Sub-project = hạng mục công trình: `{Mã CT}-{Hạng mục}` — vd: `2026-NS01-Mong`, `2026-NS01-Than`, `2026-NS01-HoanThien`

**Custom Field trên Project** (vn_accounting Custom Fields fixture):

| Fieldname | Type | Description |
|---|---|---|
| `vn_is_construction_project` | Check | "Tick nếu đây là công trình xây lắp — kích hoạt logic tính giá thành theo project" |
| `vn_contract_value` | Currency | "Giá trị hợp đồng đã ký với chủ đầu tư" |
| `vn_handover_percentage` | Percent | "Tỷ lệ nghiệm thu/bàn giao đến nay (%). Dùng để tính DD cuối kỳ" |
| `vn_construction_phase` | Select | "Giai đoạn: Chuẩn bị / Thi công / Nghiệm thu / Hoàn thành / Bảo hành" |

**Wire-up cho 4 nghiệp vụ liên kết Project (UI guidance đi kèm trên từng form):**

| Nghiệp vụ | Trường liên kết | Auto-link logic |
|---|---|---|
| Mua NVL cho công trình | `Purchase Receipt.project` / `Purchase Invoice.project` | Stock Entry tự inherit project. Form PR/PI có hint: "Chọn Project nếu mua NVL/vật tư cho một công trình cụ thể. Giá vốn sẽ tự gắn vào TK 621 của công trình." |
| Lương công nhân theo công trình | `Timesheet.project` hoặc `Salary Slip.project` | JE lương vào 622 của project. Hint: "Mỗi Timesheet/Salary Slip nếu có project sẽ tính chi phí lao động vào công trình tương ứng." |
| Xuất kho NVL ra công trình | `Stock Entry.project` | Hạch toán Nợ 621 / Có 152, 153 của project. Hint: "Chọn project khi xuất NVL/CCDC đi thi công." |
| Phân bổ chi phí chung công trình (627) | JE với cost_center = project's cost_center | Phân bổ vào project theo basis cấu hình (giờ máy / giờ công / sản lượng) |

**Quy trình tính giá thành công trình cuối kỳ (Wizard §4.2 mở rộng):**
1. Wizard `manufacturing-costing-wizard` chạy với `cost_object_type = "Project"`.
2. Bảng tập hợp chi phí: mỗi project có 1 row, hiện 621 + 622 + 627 trong kỳ + DD đầu kỳ.
3. Kế toán nhập **`vn_handover_percentage`** cho mỗi project → hệ thống tính DD cuối kỳ = `vn_contract_value × (1 − handover_percentage)`. Hoặc kế toán nhập trực tiếp DD cuối kỳ.
4. Khi project có `vn_construction_phase = "Hoàn thành"` (hoặc kế toán tick "Kết chuyển toàn bộ"): wizard sinh JE `Nợ 632 / Có 154` (giá vốn dịch vụ xây lắp), KHÔNG qua 155 thành phẩm.
5. Nghiệm thu từng hạng mục: kế toán có thể chọn sub-project + tick "Kết chuyển hạng mục này" → JE 632 ↔ 154 cho riêng sub-project.

**Edge cases xây lắp** (bổ sung BUSINESS_LOGIC §12.6):
- Công trình kéo dài nhiều năm → DD cuối năm A tự thành DD đầu năm B (rollover).
- Hợp đồng nghiệm thu theo tiến độ → SI sinh từng đợt, mỗi đợt có `project` link để khớp doanh thu ↔ giá thành kỳ tương ứng.
- Công trình bị hủy / đình chỉ thi công → kế toán mở Project → tick "Hủy bỏ" → wizard cho phép kết chuyển 154 → 632 (lỗ) hoặc 154 → 138x (treo chờ xử lý) tùy quyết định ban GĐ.

---

## 5. Sidebar wire-up

Thêm 15 items vào sidebar `Kế Toán VN`. Sections:

### Section "Giá thành" (5 items mới)

| Label | link_type | link_to | route_options |
|---|---|---|---|
| Phân bổ chi phí mua hàng | DocType | Landed Cost Voucher | {} (default list) |
| Cấu hình phân bổ | Page | landed-cost-allocation-settings | — |
| Chi phí chờ phân bổ | Report | Landed Cost Pending Allocation | — |
| Tập hợp chi phí SX kỳ | Report | Production Cost Aggregation | — |
| Bảng tính giá thành | Page | manufacturing-costing-wizard | — |

### Section "Tổng hợp" (4 items mới; 2 đã có ở section khác)

| Label | link_type | link_to |
|---|---|---|
| Sổ nhật ký chung (S03a-DN) | Report | S03a-DN Sổ Nhật Ký Chung |
| Sổ cái (S03b-DN) | Report | S03b-DN Sổ Cái |
| Kết chuyển cuối kỳ | Page | period-closing-911 |
| Khóa sổ kỳ kế toán | DocType | Period Closing Voucher |

(Bảng cân đối số phát sinh A2.1 + Sổ chi tiết tài khoản A2.2 đã có, chỉ check sidebar đã có chưa.)

### Section "Báo cáo tài chính" (4 items mới + 1 cấu hình)

| Label | link_type | link_to | route_options (default) |
|---|---|---|---|
| Báo cáo tình hình tài chính (B01-DN) | Report | B01-DN Bao Cao Tinh Hinh Tai Chinh | `{"fiscal_year": "{current}", "as_on_date": "{today}"}` |
| Báo cáo kết quả HĐKD (B02-DN) | Report | B02-DN Bao Cao KQHDKD | `{"fiscal_year": "{current}"}` |
| Báo cáo lưu chuyển tiền tệ (B03-DN) | Report | B03-DN Bao Cao LCTT | `{"fiscal_year": "{current}"}` |
| Thuyết minh BCTC (B09-DN) | Page | b09-dn-generator | — |
| Cấu hình mapping BCTC | DocType | BCTC Mapping | — |

**Default filter:** Sidebar items dùng helper `{current}` resolve sang fiscal year hiện tại + `{today}` resolve sang ngày hôm nay khi user click. Click vào sidebar → mở báo cáo có sẵn số liệu năm/ngày hiện hành, không cần KTT pick filter (tránh empty state).

Workspace sidebar JSON: `vn_accounting/fixtures/workspace_sidebar_ketoanvn.json` — append 15 items vào 3 sections tương ứng.

---

## 6. Hooks & lifecycle

### 6.1 `after_install`

```python
def after_install():
    # ... existing code ...
    seed_lcv_allocation_settings()           # 12 expense types
    seed_manufacturing_costing_settings()    # defaults TT99/2025
    seed_period_closing_account_settings()   # 911, 4212, revenue/expense lists
    seed_bctc_mapping_templates()            # 2 templates (large + small) × 3 reports
```

### 6.2 `Company.on_update` (extend existing)

```python
def on_company_update(doc, method):
    # ... existing vn_accounting code ...
    if doc.country == "Vietnam":
        ensure_bctc_mapping_for_company(doc)  # Clone template → per-company record
```

### 6.3 Landed Cost Voucher hooks

```python
"Landed Cost Voucher": {
    "before_validate": "vn_accounting.landed_cost.lcv_apply_default_expense_account",
    "validate": "vn_accounting.landed_cost.lcv_validate_import_vat_split",
}
```

### 6.4 Period Closing Voucher hooks

```python
"Period Closing Voucher": {
    "validate": "vn_accounting.period_closing.pcv_validate_vn_requirements",
    "on_submit": "vn_accounting.period_closing.pcv_audit_log",
}
```

---

## 7. Translations

Append vào `vn_accounting/translations/vi.csv`:

| English | Vietnamese |
|---|---|
| Landed Cost Allocation | Phân bổ chi phí mua hàng |
| Pending Allocation | Chi phí chờ phân bổ |
| Production Cost Aggregation | Tập hợp chi phí sản xuất |
| Manufacturing Costing | Tính giá thành sản xuất |
| Work In Progress Valuation | Đánh giá sản phẩm dở dang |
| Period Closing 911 | Kết chuyển cuối kỳ |
| Period Closing Voucher | Phiếu khóa sổ kỳ |
| S03a-DN General Journal | Sổ nhật ký chung (S03a-DN) |
| S03b-DN General Ledger | Sổ cái (S03b-DN) |
| B01-DN Statement of Financial Position | Báo cáo tình hình tài chính (B01-DN) |
| B02-DN Income Statement | Báo cáo kết quả HĐKD (B02-DN) |
| B03-DN Cash Flow Statement | Báo cáo lưu chuyển tiền tệ (B03-DN) |
| B09-DN Notes to Financial Statements | Thuyết minh BCTC (B09-DN) |
| BCTC Mapping | Cấu hình mapping BCTC |
| Restore TT99/2025 Defaults | Khôi phục mặc định TT99/2025 |
| ... | ... |

Tổng ~140 entries (LCV 25 + Costing 30 + Period Closing 20 + BCTC 40 + sổ 10 + common 15).

---

## 8. Tests

### 8.1 Unit tests (pure functions)

| Module | Test |
|---|---|
| `landed_cost/test_lcv_defaults.py` | Default expense account lookup, import vs domestic |
| `landed_cost/test_lcv_validation.py` | Import VAT split (50/50, 100/0, 0/100), invalid % rejected |
| `costing/test_unit_cost_calculation.py` | (open+dm+dl+oh-closing)/qty, edge cases (0 qty, 0 closing) |
| `costing/test_overhead_allocation.py` | 6 allocation bases, validation tổng phân bổ = 627 |
| `period_closing/test_911_je_generation.py` | 3 JE structure correct, debit=credit per JE, sign per account type |
| `period_closing/test_pcv_validation.py` | Reject draft JE, reject unbalanced, accept clean state |
| `financial_reporting/test_bctc_resolver.py` | account_formula parser (+TK,-TK, wildcard), value_type per direction, line_formula recursion |
| `financial_reporting/test_b01_equation.py` | Mã 270 = mã 440 for seeded test company |

### 8.2 Integration tests

| Test |
|---|
| Full flow: Company VN → mapping cloned → run B01 with sample GL → result matches expected |
| LCV end-to-end: Purchase Receipt → LCV with shipping + customs → giá vốn 156 increased correctly |
| Period closing: 3 wizard steps → 3 JE → submit → PCV blocks if balance off → unblocks after correction |
| Manufacturing costing: WIP valuation + costing wizard → 2 JE + Stock Entry nhập kho |

### 8.3 No-hardcoded-TK regression test

Test scan: grep `apps/vn_accounting/vn_accounting/` cho regex `["']\b[1-9]\d{2,4}["']` trong code Python (số TK 3-5 chữ số) → assert mọi match nằm trong: fixture seeds, test fixtures, lookup defaults (commented). KHÔNG trong controller logic.

### 8.4 UI guidance regression test (`test_doctype_field_descriptions.py`)

Test scan tự động trên DocType JSON cho các DocType phase này tạo:
- Mọi field có `reqd=1` phải có `description` không trống (≥ 10 chars)
- Mọi field type "Link" / "Dynamic Link" / "Select" / "Date" / "Currency" / "Float" / "Percent" phải có `description` (kể cả `reqd=0`)
- Mọi DocType có ≥ 1 Section Break phải có Section Break đầu tiên có `description` mô tả phần
- Mọi Custom Button (định nghĩa trong .js) phải có `__('...')` tooltip wrap

Test file: `vn_accounting/tests/test_ui_guidance_coverage.py`. Chạy `python -m unittest` đầu mỗi phase.

Whitelist: standard ERPNext DocType được extend (Landed Cost Voucher, Period Closing Voucher, Company, Project) → chỉ check Custom Field, không check core field.

---

## 9. Phase decomposition (multi-prep-project)

| Phase | Scope | Est. sessions | Depends on |
|---|---|---|---|
| **P0 — Foundation Settings** | 4 Settings DocTypes (LCV / Costing / Period Closing extend / BCTC Mapping) + seed fixtures + Company.on_update hook | 2-3 | — |
| **P1 — LCV Universal** | C7.1-C7.6: LCV defaults wire-up, import VAT split, pending allocation report, sidebar | 2 | P0 |
| **P2 — Tổng hợp Sổ + Kết chuyển** | C9.1-C9.6 + C2.5 + C2.6: 911 wizard, PCV validation, Sổ nhật ký chung, Sổ cái S03b-DN, sidebar | 3 | P0 |
| **P3 — BCTC Reports** | C10.1-C10.10, C10.12: BCTC Mapping management UI, 4 reports (B01/B02/B03 + B09 framework), Excel export, sidebar | 4-5 | P0 |
| **P4 — Giá thành SX** | C8.1-C8.8: WIP Valuation DocType, costing wizard, 2 JE generation, production cost report, sidebar | 3 | P0 |
| **P5 — Polish + i18n + tests** | All translations, no-hardcoded-TK regression test, docs CODEBASE.md, full QA | 1-2 | P1-P4 |

Total: 15-18 sessions. Phase P0-P3 mandatory; P4 chỉ cho DN sản xuất; P5 release-gate.

**Order rationale:**
- P0 trước vì mọi phase phụ thuộc Settings DocTypes
- P1 (LCV) universal, lowest risk, dùng được ngay ERPNext built-in → quick win
- P2 (Tổng hợp) trước P3 vì BCTC dựa trên dữ liệu đã kết chuyển 911
- P3 (BCTC) là goal cuối — kế toán trưởng xem output
- P4 (Giá thành SX) cuối cùng vì chỉ áp dụng DN sản xuất, có thể skip cho DN thương mại
- P5 release polish + regression

---

## 10. Self-review notes

### 10.1 Spec coverage

| 15 items đã chốt | Spec section | FEATURES section |
|---|---|---|
| Giá thành 1: LCV chi phí mua hàng | §3.1 + §4.5 + §5 | C7.2 |
| Giá thành 2: LCV nhập khẩu | §3.1 (import_only) + §4.5 | C7.3 |
| Giá thành 3: Tập hợp chi phí SX | §3.2 + §4.5 | C8.2 |
| Giá thành 4: Bảng tính giá thành | §3.5 + §4.2 | C8.3, C8.4 |
| Giá thành 5: Kết chuyển 621/622/627→154→155 | §4.2 + §3.2 | C8.5 |
| Tổng hợp 1: Sổ nhật ký chung (S03a-DN) | §4.4 | C2.5 |
| Tổng hợp 2: Sổ Cái (S03b-DN) | §4.4 | C2.6 |
| Tổng hợp 3: Sổ chi tiết TK (S38-DN) | (đã có A2.2) | — |
| Tổng hợp 4: Bảng cân đối số phát sinh (S06-DN) | (đã có A2.1) | — |
| Tổng hợp 5: Kết chuyển cuối kỳ → 911 → 421 | §4.1 + §3.3 | C9.2 |
| Tổng hợp 6: Khóa sổ kỳ kế toán | §3.6 + §6.4 | C9.3, C9.4 |
| BCTC 1: B01-DN Báo cáo tình hình tài chính | §4.3 + §3.4 | C10.4 |
| BCTC 2: B02-DN BC KQHĐKD | §4.3 + §3.4 | C10.5 |
| BCTC 3: B03-DN BC LCTT gián tiếp | §4.3 + §3.4 | C10.6 |
| BCTC 4: B09-DN Thuyết minh | §4.3 (D14) | C10.7 |

15/15 covered. ✅

### 10.2 Placeholder scan

Đã check: không có `TODO`, `TBD`, `???`, `XXX` trong spec body. Một số "lookup" placeholders ở §3 (vd: "621 lookup") là cố ý — cụ thể hóa khi implement seed function.

### 10.3 Type consistency

| Type name | Used in |
|---|---|
| `LCV Expense Type Setting` | §3.1 (child of LCV Allocation Settings) |
| `Account List Item` | §3.3 (reusable child) |
| `BCTC Line` | §3.4 (child of BCTC Mapping) |
| `BCTC Mapping Template` | §3.4 (separate template DocType, mentioned in seeding) |
| `Work In Progress Valuation` | §3.5 |
| `Period Closing Voucher` | §3.6 (existing ERPNext) |
| `VN Accounting Settings` | §3.3 (existing, extended) |

Tên DocType nhất quán trong toàn spec. ✅

### 10.4 Open questions — đã chốt 2026-05-11

Toàn bộ 7 câu hỏi đã chốt với KTT (user Long). Quyết định ghi vào §2 decisions D14, D16–D21.

| # | Câu hỏi | Quyết định | Decision ref |
|---|---|---|---|
| 1 | B03-DN có cần phương pháp trực tiếp Phase 1? | Không. Phase 1 chỉ gián tiếp. | D16 |
| 2 | B09-DN sinh Word hay Excel? | Excel đa sheet (option B). 1 sheet văn xuôi + N sheet chi tiết khoản mục. | D14, §4.6 |
| 3 | Wizard kết chuyển Select all hay Select none? | Select all (TK không phát sinh tự skip). TK loại trừ vĩnh viễn cấu hình trong Settings. | D17 |
| 4 | Thuế NK (3333) cộng giá vốn hay treo riêng? | 3333 là TK trung gian phải nộp NSNN, LUÔN cộng giá vốn (luật VAS). Toggle "Có chịu thuế NK?" cho 3 trường hợp đặc thù (khu chế xuất / tạm nhập tái xuất / gia công XK). Đính chính cơ chế bút toán trong §3.1. | D18 |
| 5 | Cost object xây lắp = Project? | Đúng. Bổ sung §4.7 Project setup guide đầy đủ. | §4.7 |
| 6 | BCTC Mapping per-Company vs Single? | Per-Company. Thêm 2 nút trợ giúp: "Copy mapping từ Company khác" + "Khôi phục mặc định TT99/2025". | D19, §3.4 |
| 7 | Khóa sổ — role nào? | Chỉ Accounts Manager (KTT). System Manager xem-only. Bắt buộc nhập lý do khi submit/cancel. Audit log không xóa. | D20, §3.6 |

### 10.5 Cross-cutting UI guidance requirement (chốt 2026-05-11)

Mọi UI surface trong phase này (và mọi phase sau) phải có inline guidance. Đây là **acceptance gate** trước khi merge — xem §15 cho QA checklist. Ref: `~/.claude/projects/.../feedback_ui_inline_guidance.md`.

### 10.6 Filesystem convention (đã verify với existing app)

App `vn_accounting` dùng cấu trúc 3-level package: `apps/vn_accounting/vn_accounting/<sub_package>/`. Tất cả DocType JSON sống trong **một** folder `apps/vn_accounting/vn_accounting/vn_accounting/doctype/<doctype_slug>/` (Frappe convention — DocType registry trong app dùng 1 thư mục).

Sub-package paths trong spec này (`landed_cost`, `costing`, `financial_reporting`, `period_closing`) chứa **helper code + page bundle + report code**, KHÔNG chứa DocType JSON. DocType `BCTC Mapping`, `BCTC Line`, `LCV Allocation Settings`, `Manufacturing Costing Settings`, `Account List Item`, `Work In Progress Valuation` đều land vào `apps/vn_accounting/vn_accounting/vn_accounting/doctype/`.

Mapping:

| Sub-package | Chứa gì |
|---|---|
| `vn_accounting/landed_cost/` | hooks LCV (lcv_apply_default_expense_account, lcv_validate_import_vat_split), seed function, page `landed-cost-allocation-settings` |
| `vn_accounting/costing/` | Wizard page `manufacturing-costing-wizard`, helper aggregate/calculate functions, JE generation |
| `vn_accounting/financial_reporting/` | Report engine (`resolve_bctc_line`), 4 Script Reports b01/b02/b03/b09, Excel export helpers |
| `vn_accounting/period_closing/` | Page `period-closing-911`, helper preview/create JE, PCV validation hooks |
| `vn_accounting/setup/` | Existing — extend với seed functions cho settings mới |

### 10.7 KTT self-review v2 (2026-05-11, sau khi chốt D14-D21 + thêm §4.6/§4.7/§12)

Em tự review với vai KTT chuyên nghiệp, tìm 8 gaps:

| # | Gap | Action |
|---|---|---|
| 1 | Wizard kết chuyển 911 gộp 821 vào danh sách chung → sai workflow tháng/quý (821 chỉ kết chuyển năm) | **Fixed §3.3 + §4.1**: tách `expense_accounts_to_close_periodic` (không 821) + `corporate_income_tax_account` riêng. Wizard auto-detect kỳ năm vs tháng/quý → include/exclude 821 |
| 2 | Wizard tính giá thành luôn qua 155 — không xử lý dịch vụ/xây lắp (kết chuyển 154 → 632 trực tiếp) | **Fixed §3.2 + §4.2**: thêm `transfer_to_finished_goods` + `services_cogs_account` trong Settings. Wizard rẽ nhánh Step 6/7 theo flag |
| 3 | WIP Valuation thiếu field cho phương pháp "Sản lượng tương đương" — cần `physical_units_in_progress` + `equivalent_completion_pct` | **Fixed §3.5**: thêm 3 field + `computed_closing_wip` auto-compute theo 4 valuation_method |
| 4 | Wizard cảnh báo TK ngoại tệ chưa đánh giá lại — không có UI fix Phase 1 | **Documented §4.1**: KTT làm thủ công qua Phiếu kế toán Nợ/Có 413 ↔ TK gốc. Phase 2 sẽ có wizard riêng. Banner cảnh báo có link article |
| 5 | LCV không cover rebate sau (NCC giảm giá sau khi mua → giảm giá vốn) | Phase 2 — added to §10.8 |
| 6 | Sidebar BCTC click vào rỗng vì chưa pick filter | Phase 1 sub-task — default route_options `fiscal_year={current_year}` cho 4 BCTC reports (added to §5 sidebar table guidance) |
| 7 | Test enforce "DocType field reqd=1 phải có description" — thiếu | Added §8.3: thêm `test_doctype_field_descriptions.py` regression test scan toàn app |
| 8 | Excel xuất layout TT99/2025 chưa specify font/column width/merge | Phase 5 polish — added to §10.8 |

3 HIGH/MEDIUM (1, 2, 3) đã fix trong spec. 5 LOW (4-8) đã document hoặc note phase 2.

### 10.8 Phase 1 không làm (cập nhật)

- B01-B09-DNKLT (bộ DN không liên tục) — chờ Company thực tế
- B03-DN trực tiếp — gián tiếp đủ phase 1
- Bảng kê hoá đơn GTGT (C2.7) — thuộc section thuế C3, không phải phase này
- Tờ khai thuế TNDN, TNCN, GTGT — section C3
- Phân tích chỉ số tài chính (ROA, ROE) — đã có Dashboard v2 (A4)
- BCTC giữa niên độ — UI cho phép chọn Quarter là đủ
- BCTC hợp nhất — phase sau khi có Company group
- **Đánh giá lại tỷ giá ngoại tệ** (TK 1112/1122/131/331 cuối kỳ → JE 413 ↔ TK gốc) — wizard riêng, Phase 2. Phase 1: KTT làm thủ công qua Phiếu kế toán.
- **LCV rebate / chiết khấu mua sau** (NCC giảm giá sau khi đã ghi sổ → giảm giá vốn 156/152) — Phase 2
- **Excel layout polish TT99/2025** (font, column width, ô merge chính xác theo Phụ lục IV) — Phase 5 polish trong cùng task, sau khi 4 báo cáo functional xong
- **Wizard tính TNDN tạm tính / quyết toán** (sinh JE Nợ 821 / Có 3334 tự động) — Phase 2 (thuộc section C3 Thuế)

---

## 11. References

- BUSINESS_LOGIC.md §11–§14 (`apps/vn_accounting/docs/BUSINESS_LOGIC.md`)
- FEATURES.md §C7–§C10 (`apps/vn_accounting/FEATURES.md`)
- Thông tư 99/2025/TT-BTC Phụ lục III (Sổ kế toán) + Phụ lục IV (BCTC)
  - https://congbao.chinhphu.vn/van-ban/thong-tu-so-99-2025-tt-btc-46529.htm
  - https://static3.luatvietnam.vn/uploaded/others/2025/10/30/tt99_3010133637.pdf
- Memory: `feedback_vn_accounting_no_hardcoded_accounts.md`, `reference_tt99_2025_form_codes.md`
- Existing patterns: A2 reports, A3 sidebar persistence, A4 dashboard, A7 VN Accounting Settings, A10 Treasury settings

---

---

## 12. UI Guidance Requirements (cross-cutting)

Áp dụng cho **mọi feature trong phase này + mọi feature tương lai của vn_accounting**. Ref: `~/.claude/projects/.../feedback_ui_inline_guidance.md`.

Mục đích: phần mềm mới, kế toán viên + KTT chưa quen → mọi giao diện phải tự giải thích được, không bắt user đoán.

### 12.1 Required guidance surfaces

| UI surface | Required guidance | Pattern |
|---|---|---|
| **DocType field** | `description` attribute đầy đủ, tiếng Việt, 1-2 câu | Vd: "TK 911 — Xác định kết quả kinh doanh. Mặc định TT99/2025. Sửa nếu DN dùng TK chi tiết khác (vd: 9111, 9112)." |
| **Section break** | `description` mô tả phần này dùng để làm gì, khi nào điền | Vd: "Cấu hình tài khoản kết chuyển. Phần này chỉ KTT sửa được." |
| **Custom button** | Tooltip + label rõ ràng (không "OK"/"Submit") | Vd: "Tạo 3 phiếu kế toán nháp cho kết chuyển doanh thu/chi phí/lãi-lỗ. Phiếu ở trạng thái Nháp, cần KTT duyệt riêng." |
| **Wizard page** | Help panel top: 3 phần (Mục đích / Các bước / Kết quả) | Vd: top wizard "Tính giá thành sản xuất": "**Mục đích:** Tính giá thành thực tế của sản phẩm/đơn hàng kỳ này. **Các bước:** 1) Tập hợp chi phí 621/622/627, 2) Đánh giá SPDD, 3) Phân bổ 627, 4) Tính giá thành đơn vị, 5) Sinh JE nháp + Stock Entry nhập kho. **Kết quả:** Bảng giá thành đơn vị + 2 phiếu kế toán nháp + N phiếu nhập kho thành phẩm." |
| **Wizard step** | Mỗi step 1-2 paragraph intro: làm gì, dữ liệu lấy từ đâu, kết quả là gì |  |
| **Script Report** | Tooltip column header (`fieldtype="Currency"` + `description`). Filter có placeholder + hint | Vd: tooltip cột "Số kỳ này": "Phát sinh trong kỳ báo cáo. Click số để xem chi tiết các chứng từ đóng góp." |
| **Settings DocType** | Mỗi field có `description` + example value + reference TT99/2025 article nếu liên quan | Vd: "TK tiền gửi có kỳ hạn — mặc định 1281 (TT99/2025 điều X). Sửa nếu DN tách chi tiết theo NH: 12811 (VCB), 12812 (BIDV)." |
| **Dialog/Modal** | Title rõ + intro line + button label mô tả nghiệp vụ | Vd: dialog xác nhận khóa sổ: title "Khóa sổ kỳ kế toán {period}?", intro: "Sau khi khóa, toàn bộ chứng từ trong kỳ {period} không thể sửa/xóa. Chỉ KTT mở khóa lại được.", buttons: ["Hủy", "Khóa sổ"] |
| **Empty state** | Khi list rỗng, show next action + link vn_help | Vd: list LCV rỗng: "Chưa có phiếu phân bổ chi phí mua hàng. Bấm 'Tạo mới' để bắt đầu, hoặc xem [hướng dẫn LCV trong vn_help]." |
| **Error message** | "X bị Y → sửa bằng cách Z" — không chỉ "Validation failed" | Vd: "Không thể khóa sổ tháng 4/2026 vì còn 3 Phiếu kế toán nháp. Ghi sổ hoặc hủy các nháp trước: [link list]." |

### 12.2 Inline icon pattern

Trên label các field/dòng quan trọng có icon `ℹ` hoặc `?` → hover/click hiện popover giải thích chi tiết:

- Trên báo cáo BCTC: icon trên mã chỉ tiêu hiện công thức tính. Vd: hover "Mã 110": popover "Tiền và các khoản tương đương tiền = Số dư Nợ cuối kỳ của TK 111 + 112 + 113. Click số để xem các chứng từ đóng góp."
- Trên wizard preview JE: tooltip trên dòng bút toán giải thích "Vì sao bút toán này, nguồn dữ liệu từ đâu". Vd: hover "Nợ 911 / Có 632 — 285,000,000": popover "Kết chuyển toàn bộ giá vốn hàng bán (TK 632) trong kỳ về TK 911 để xác định KQKD. Số tiền = phát sinh Nợ TK 632 trong kỳ tháng 4/2026."
- Trên Settings DocType: icon trên field TK hiện ý nghĩa nghiệp vụ + reference TT99/2025.

### 12.3 vn_help integration

Mỗi feature mới phải có 1 article trong `vn_help` (ref: `reference_vn_help_authoring_standard.md` trong memory). Article viết bằng tiếng Việt thuần — không nhắc tên ERPNext/Frappe/DocType (ref: `feedback_help_terminology_vietnamese.md`).

Trên UI:
- Header help panel có nút "Xem hướng dẫn chi tiết" → mở article tương ứng trong vn_help portal.
- Mỗi DocType form có nút "Hướng dẫn" (toolbar) mặc định link tới article của DocType đó.

**Article cần viết cho phase này (~12 articles):**

| ID | Section | Title |
|---|---|---|
| GT-01 | Giá thành | Phân bổ chi phí mua hàng (LCV) — hướng dẫn cơ bản |
| GT-02 | Giá thành | LCV cho hàng nhập khẩu — thuế NK, VAT NK khấu trừ |
| GT-03 | Giá thành | Tính giá thành sản xuất cuối kỳ — quy trình 6 bước |
| GT-04 | Giá thành | Setup Project cho DN xây lắp |
| TH-01 | Tổng hợp | Sổ nhật ký chung & Sổ Cái — đọc và xuất Excel |
| TH-02 | Tổng hợp | Kết chuyển cuối kỳ — quy trình + bút toán 911 |
| TH-03 | Tổng hợp | Khóa sổ kỳ kế toán — khi nào, ai làm, hậu quả |
| TH-04 | Tổng hợp | Mở khóa kỳ đã đóng — quy trình + audit log |
| BCTC-01 | BCTC | Báo cáo tình hình tài chính (B01-DN) — cấu trúc + cách đọc |
| BCTC-02 | BCTC | Cấu hình mapping BCTC — khi nào sửa công thức TK |
| BCTC-03 | BCTC | Thuyết minh BCTC (B09-DN) — quy trình điền |
| BCTC-04 | BCTC | Xuất Excel BCTC để nộp thuế |

### 12.4 QA acceptance gate (trước khi merge từng feature)

Checklist bắt buộc pass:

- [ ] Mọi DocType field (đặc biệt `reqd=1`) có `description` rõ ràng (không trống, không generic kiểu "Enter value")
- [ ] Mọi custom button có tooltip ≥ 1 câu mô tả nghiệp vụ
- [ ] Wizard có help panel top với 3 phần Mục đích / Các bước / Kết quả
- [ ] Báo cáo có tooltip column header + filter hint
- [ ] Settings có example value + TT99/2025 reference (nếu liên quan)
- [ ] Empty state có hướng dẫn next action
- [ ] Error message viết theo style "X bị Y → sửa bằng cách Z" (không chỉ "Mandatory field")
- [ ] Article hướng dẫn trong vn_help đã có + link từ UI

### 12.5 Anti-patterns tuyệt đối tránh

- ❌ DocType field không có description ("dev biết, user đoán")
- ❌ Button label cryptic ("Submit", "Action 1", "Process") không mô tả nghiệp vụ
- ❌ Wizard ném thẳng user vào step 1 không context
- ❌ Error message chỉ "Mandatory field" / "Invalid value" / "Validation failed"
- ❌ Tooltip vô nghĩa "Click here", "More info"
- ❌ Báo cáo có cột "Mã" "Giá trị" không giải thích cách tính
- ❌ Empty state trống trơn không hướng dẫn

---

**Status:** Plan-mode complete. 7 open questions chốt với KTT (§10.4). UI guidance requirement (§12) ghi vào memory cross-cutting. Sẵn sàng decompose qua `multi-prep-project` cho Phase 2 execution. Phase order: P0 Foundation Settings → P1 LCV → P2 Tổng hợp → P3 BCTC → P4 Giá thành SX → P5 Polish (15-18 sessions ước tính).
