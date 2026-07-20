# Asset Polishing — TSCĐ & CCDC theo TT99/2025

**Branch:** `feat/asset-polishing`
**Worktree:** `.worktrees/vn_accounting-asset-polishing/`
**Ngày:** 2026-04-29
**Phạm vi:** Cải tiến vn_accounting cho TSCĐ và CCDC, tuân thủ TT99/2025 (hiệu lực 2026-01-01) và các mẫu sổ trong Phụ lục III.

---

## 1. Mục tiêu

Tách biệt rõ TSCĐ ↔ CCDC trong UI và data model theo VAS, tận dụng ERPNext Asset cho TSCĐ và bổ sung custom DocTypes cho CCDC. Đáp ứng đầy đủ vòng đời: ghi tăng → bàn giao → khấu hao/phân bổ → sửa chữa → kiểm kê → thanh lý/ghi giảm. Tuân thủ TT99/2025 về account naming, mẫu sổ S21-DN/S22-DN, định khoản 211/214/153/242. Permission matrix cấu hình được qua VN Accounting Settings, không hardcode.

## 2. Bối cảnh TT99/2025

**Hiệu lực:** 01/01/2026, thay TT200/2014. Phụ lục III có 42 mẫu sổ.

| Khía cạnh | TT99/2025 | Thay đổi vs TT200 |
|-----------|-----------|-------------------|
| Ngưỡng TSCĐ | ≥30tr VND, ≥1 năm (TT45/2013 vẫn governing) | Giữ nguyên |
| Phương pháp khấu hao | Đường thẳng / Số dư giảm dần / Theo sản lượng | Giữ nguyên |
| TK 214 sub-accounts | 2141, 2142, 2143, 2147 | Giữ nguyên |
| TK 153 sub-accounts | TT99 không quy định, DN tự mở | Linh hoạt hơn |
| TK 242 tên | "Chi phí trả trước" | **Đổi từ "Chi phí chờ phân bổ"** |
| Sổ S21-DN | Sổ tài sản cố định | Giữ nguyên |
| Sổ S22-DN | Theo dõi TSCĐ và CCDC tại nơi sử dụng | Giữ nguyên |
| Định khoản | 211/214, 153/242, 627-642 | Giữ nguyên |

**Implication:** TT99 không yêu cầu đại tu khấu hao. Trọng tâm là (a) đổi tên TK 242, (b) tổ chức UI theo VAS-clean (TSCĐ ≠ CCDC), (c) bổ sung mẫu sổ S22-DN cho bàn giao tại nơi sử dụng.

## 3. Architecture

### 3.1 Phân chia trách nhiệm

```
TSCĐ (≥30tr, ≥1 năm)             CCDC (<30tr hoặc <1 năm)
─────────────────────             ────────────────────────
ERPNext Asset (override)          vn_accounting CCDC Item (custom)
Asset Category (label override)   CCDC Category (custom)
Asset Depreciation Schedule       CCDC Allocation Schedule (custom)
Asset Repair (expose + 3-way)     —
Asset Value Adjustment (skip v1)  —
Asset Disposal (đã có)            CCDC Writeoff (custom)

Asset Handover (custom, scope strict)   ←  shared cho cả 2
Asset Stocktake (custom, scope strict)  ←  shared cho cả 2
```

### 3.2 DocType inventory

**Custom mới (9 DocTypes vn_accounting tạo):**

| # | DocType | Loại | Vai trò |
|---|---------|------|---------|
| 1 | CCDC Item | Master | Đơn vị CCDC (parallel với Asset cho TSCĐ) |
| 2 | CCDC Category | Master | Phân loại CCDC + mapping account 153/242/expense |
| 3 | CCDC Allocation Schedule | Submittable | Lịch phân bổ N kỳ qua TK 242 |
| 4 | CCDC Allocation Entry | Child | Từng dòng phân bổ theo kỳ |
| 5 | CCDC Writeoff | Submittable | Ghi giảm CCDC (mất/hỏng/hết hạn) |
| 6 | Asset Handover | Submittable | Bàn giao TSCĐ/CCDC theo S22-DN |
| 7 | Asset Handover Item | Child | Danh mục trong 1 phiếu bàn giao |
| 8 | Asset Stocktake | Workflow | Kiểm kê TSCĐ/CCDC định kỳ theo location |
| 9 | Asset Stocktake Item | Child | Chi tiết đếm cho từng tài sản |

**Asset Permission Rule** (child của VN Accounting Settings — tính riêng, không gộp 9):

| # | DocType | Loại | Vai trò |
|---|---------|------|---------|
| 10 | Asset Permission Rule | Child | Mỗi dòng trong Permission Matrix |

**ERPNext có sẵn — chỉ override (không clone):**

| DocType | Hành động |
|---------|-----------|
| Asset | Override label tiếng Việt qua translations + Property Setter ẩn 3 method khấu hao |
| Asset Category | Re-seed 5 nhóm chuẩn TT99 + label tiếng Việt |
| Asset Repair | Thêm Custom Field `repair_classification` 3-way + JE routing |
| Asset Movement | Ẩn khỏi sidebar (Asset Handover thay thế); giữ DocType native |
| Asset Depreciation Schedule | Không sửa (đã đúng cho TSCĐ) |
| Asset Disposal | Đã có v1 — không sửa |
| Asset Value Adjustment | Skip expose v1 (Settings flag, default off) |

### 3.3 Account routing

| Nghiệp vụ | TSCĐ → JE | CCDC → JE |
|-----------|-----------|-----------|
| Mua | N 211 / C 331 | N 153 / C 331 |
| Đưa vào sử dụng | (chỉ submit Asset, không JE) | N 242 / C 153 |
| Khấu hao/Phân bổ kỳ | N 627/641/642 / C 214x | N 627/641/642 / C 242 |
| Bàn giao (S22-DN) | KHÔNG JE (chỉ register) | KHÔNG JE (chỉ register) |
| Kiểm kê thiếu | N 1381 / C 211 (giá trị ròng) | N 1381 / C 153 (phần chưa xuất) + N 627/642 / C 242 (phần còn dư) |
| Kiểm kê thừa | N 211 / C 3381 (theo giá ước) | N 153 / C 3381 |
| Sửa chữa thường xuyên | N 627/641/642 / C 331 | n/a |
| Sửa chữa lớn vốn hóa | N 241 / C 331, hoàn thành: N 211 / C 241 | n/a |
| Nâng cấp/cải tạo | N 241 / C 331, hoàn thành: N 211 / C 241 + recreate Depr Schedule | n/a |
| Thanh lý TSCĐ | N 214 + 811 / C 211 + N 111/131 / C 711 | n/a |
| Ghi giảm CCDC | N 627/641/642 / C 242 (phần dư) + N 632/811/1381 / C 153 (chưa xuất) | n/a (CCDC native flow) |
| Đánh giá lại tăng | N 211 / C 412 | n/a |

### 3.4 Shared infrastructure — Dynamic Link cho Handover & Stocktake

`Asset Handover Item` và `Asset Stocktake Item` đều có cột:

```python
{"fieldname": "target_doctype", "fieldtype": "Link", "options": "DocType",
 "default": None,
 "in_list_view": 1, "reqd": 1,
 # validate: chỉ accept Asset hoặc CCDC Item, theo parent.scope}
{"fieldname": "target_name", "fieldtype": "Dynamic Link", "options": "target_doctype",
 "in_list_view": 1, "reqd": 1}
```

Parent có field `scope: Select [TSCĐ | CCDC]` (xem Section 5). Validate: tất cả `target_doctype` của items phải khớp scope.

> **Why Dynamic Link:** tránh duplicate 4 DocTypes (TSCĐ Handover, CCDC Handover, TSCĐ Stocktake, CCDC Stocktake). Frappe Dynamic Link là pattern chuẩn cho 1 child trỏ N parent doctype. Filter sidebar dùng scope thay vì doctype, đơn giản và route_options-friendly.

## 4. Lifecycle & Workflows

### 4.1 TSCĐ Lifecycle

```
Purchase Invoice (item.is_fixed_asset=1)
        │ submit + ERPNext native hook
        ▼
Asset (Draft) ──► [Bàn giao S22-DN] ──► Asset (đang sử dụng)
        │            Asset Handover            │
        │ submit                                │
        ▼                                       ├──► [Khấu hao tự động hàng tháng]
Asset (Submitted)                               │     Asset Depreciation Schedule + Scheduler JE
        │                                       │
        ├──► [Sửa chữa] Asset Repair            │
        │       3 classification:               │
        │       - Chi phí: N 627/641/642        │
        │       - Sửa chữa lớn: N 241 → N 211   │
        │       - Nâng cấp: N 241 → N 211 +     │
        │         lập lại Depr Schedule         │
        │                                       │
        ├──► [Kiểm kê] Asset Stocktake          │
        │       Workflow 4 state                │
        │                                       │
        ├──► [Bàn giao lại]                     │
        │     Asset Handover (di chuyển)        │
        │                                       │
        └──► [Thanh lý] Asset Disposal (đã có)  │
              Trạng thái: Disposed              │
```

### 4.2 CCDC Lifecycle

```
Purchase Invoice (item.is_low_value_asset=1)
        │ submit + custom hook
        ▼
CCDC Item (Draft, status=Mới mua, ở kho)   ────► JE: N 153 / C 331
        │
        │ submit + ngày xuất dùng + số kỳ phân bổ N
        ▼
CCDC Item (Submitted, status=Đang sử dụng)
        │ on_submit:
        ├──► JE: N 242 / C 153
        └──► CCDC Allocation Schedule auto-create, N kỳ
                │
                ▼ scheduler hàng tháng
        [Phân bổ kỳ] JE: N 627/641/642 / C 242
                │
                ├── kỳ cuối → CCDC Item.status = Hết phân bổ
                ├── nhưng vật lý vẫn theo dõi qua S22-DN
                │
                ├──► [Bàn giao] Asset Handover
                │
                ├──► [Kiểm kê] Asset Stocktake
                │
                └──► [Ghi giảm] CCDC Writeoff (mất/hỏng/hết)
                        │ JE phần dư 242 → 627/641/642
                        │ JE phần chưa xuất 153 → 632/1381
                        ▼
                CCDC Item.status = Đã ghi giảm
```

### 4.3 Asset Handover (Bàn giao S22-DN)

**State machine:** Draft → Submitted → (Cancelled). Không có workflow chính thức.

**Field chính:**

| Field | Type | Note |
|-------|------|------|
| scope | Select [TSCĐ, CCDC] | Strict, không Mixed. Pre-fill từ route_options |
| posting_date | Date | Default today |
| from_employee | Link Employee | Có thể null nếu giao từ kho |
| from_department | Link Department | |
| to_employee | Link Employee | Bắt buộc (giao cho ai) |
| to_department | Link Department | |
| to_location | Link Location | |
| co_signer_employee | Link Employee | Bắt buộc khi tổng giá trị ≥ ngưỡng (Settings) |
| handover_items | Table Asset Handover Item | child với Dynamic Link |
| total_asset_value | Currency | Auto sum từ child |
| reason | Small Text | Lý do bàn giao |
| remarks | Text | Ghi chú |

**Submit logic:**
```python
def on_submit(self):
    self.validate_scope_match()  # all items khớp scope
    self.validate_threshold()    # nếu ≥ ngưỡng → co_signer_employee bắt buộc
    self.update_target_records() # set Asset/CCDC.location, custodian
    self.create_movement_shadow() # tạo Asset Movement bóng cho ERPNext audit (chỉ khi scope=TSCĐ)
```

**Cancel logic:** revert location/custodian về giá trị trước đó (lưu trong field `before_handover_snapshot: JSON`).

### 4.4 Asset Stocktake (Kiểm kê)

**Workflow 4 state:**

```
Draft ───► In Progress ───► Completed ───► Approved ───► Closed
  │           │                │                │            │
  │   đoàn    │   đếm xong     │   KTT          │   không    │
  │   kiểm kê │   chưa duyệt   │   approve →    │   sửa được │
  │   bắt đầu │                │   tạo JE       │            │
  └─Cancel    └─Cancel         └─Reject (về In Progress)
```

**Field chính:**

| Field | Type | Note |
|-------|------|------|
| scope | Select [TSCĐ, CCDC] | Strict, pre-fill từ route_options |
| stocktake_date | Date | Bắt buộc |
| location | Link Location | Bắt buộc — kiểm kê theo nơi sử dụng |
| department | Link Department | Optional, nếu set thì combine với location |
| stocktake_team_lead | Link Employee | Trưởng đoàn |
| storekeeper | Link Employee | Thủ kho/người dùng |
| accountant | Link Employee | Kế toán ghi sổ |
| stocktake_items | Table Asset Stocktake Item | Auto-load từ location/department khi click [Tải danh sách] |
| total_difference_value | Currency | Auto sum |
| difference_resolution | Select [Bồi thường, Ghi chi phí, Treo chờ xử lý] | Cần khi có chênh |

**Stocktake Item child:**

| Field | Type | Note |
|-------|------|------|
| target_doctype | Link DocType | Asset hoặc CCDC Item |
| target_name | Dynamic Link | |
| book_value | Currency | Giá trị ròng hiện tại từ database |
| physical_status | Select [Còn nguyên, Hỏng, Mất] | Người đếm điền |
| remarks | Small Text | Ghi chú từng item |

**On Approve logic — xử lý đủ 3 trạng thái:**
```python
def on_approve(self):
    je_items = []
    for item in self.stocktake_items:
        if item.physical_status == "Còn nguyên":
            pass  # không thay đổi gì, chỉ confirm asset vẫn ở location
        elif item.physical_status == "Mất":
            je_items.append(self._build_loss_je(item))
            self._update_target_status(item, "Lost")
        elif item.physical_status == "Hỏng":
            self._update_target_status(item, "Damaged")
            # KHÔNG auto JE — kế toán quyết sửa (Asset Repair) hay thanh lý sau
    if je_items:
        self._post_je(je_items)
    self._set_target_last_stocktake_date(self.stocktake_date)  # cho mọi item, bất kể status
```

### 4.5 Asset Repair (extend ERPNext)

Custom Field `repair_classification: Select [Chi phí, Sửa chữa lớn vốn hóa, Nâng cấp cải tạo]`. Default = "Chi phí".

**Validate hint:**
```python
def validate(self):
    if self.repair_cost >= 0.10 * frappe.db.get_value("Asset", self.asset, "gross_purchase_amount"):
        if self.repair_classification == "Chi phí":
            frappe.msgprint(
                _("Chi phí sửa chữa ≥ 10% nguyên giá. Cân nhắc vốn hóa."),
                alert=True
            )
```

**JE routing:**

| Classification | Khi nào dùng | JE |
|----------------|-------------|------|
| Chi phí | Sửa chữa thường xuyên (thay phụ tùng nhỏ, vệ sinh máy) | N 627/641/642 / C 331 (default ERPNext) |
| Sửa chữa lớn vốn hóa | Đại tu, phục hồi năng lực ban đầu, không đổi tuổi thọ | N 241 / C 331 → khi `completion_date` set: N 211 / C 241 (cộng vào nguyên giá hiện tại) |
| Nâng cấp cải tạo | Tăng năng lực vượt ban đầu HOẶC kéo dài tuổi thọ | Giống Sửa chữa lớn + **recreate Asset Depreciation Schedule** với nguyên giá mới và useful_life mới (kéo dài) |

> **Khác biệt cốt lõi:** Sửa chữa lớn cộng nguyên giá nhưng giữ nguyên thời gian sử dụng còn lại (kỳ khấu hao theo schedule cũ). Nâng cấp cải tạo cộng nguyên giá VÀ điều chỉnh thời gian sử dụng → schedule cũ cancel, schedule mới tạo từ ngày completion.

## 5. Sidebar Reorganization (γ2)

### 5.1 Layout

2 mother section TSCĐ và CCDC. Bàn giao + Kiểm kê duplicate trong cả 2, dùng `route_options.scope` để filter và pre-fill.

```
═══ TSCĐ ═══
  📋 Danh sách TSCĐ        → Asset           {docstatus:1}
  ➕ Tạo TSCĐ              → Asset           {docstatus:0}
  🧮 Tính khấu hao         → Asset Depreciation Schedule
  🔧 Sửa chữa              → Asset Repair
  🤝 Bàn giao TSCĐ         → Asset Handover  {scope:"TSCĐ"}
  🔍 Kiểm kê TSCĐ          → Asset Stocktake {scope:"TSCĐ"}
  ⚖️ Thanh lý              → Asset Disposal
  📖 Sổ TSCĐ (S21-DN)      → Custom Report (S21-DN)
  📜 Lịch sử khấu hao      → Asset Depreciation Ledger

═══ CCDC ═══
  📋 Danh sách CCDC        → CCDC Item       {docstatus:1}
  ➕ Tạo CCDC              → CCDC Item       {docstatus:0}
  📊 Phân bổ CCDC          → CCDC Allocation Schedule
  📉 Ghi giảm CCDC         → CCDC Writeoff
  🤝 Bàn giao CCDC         → Asset Handover  {scope:"CCDC"}
  🔍 Kiểm kê CCDC          → Asset Stocktake {scope:"CCDC"}
  📖 Sổ S22-DN tại nơi dùng → Custom Report (S22-DN)
```

### 5.2 Bỏ khỏi sidebar

- ❌ "Điều chuyển → Asset Movement" — Asset Handover thay thế (vai trò Movement đồng bộ trong on_submit)
- ❌ "Phân bổ CCDC → JE filter" — CCDC Allocation Schedule thay
- ❌ "Sổ TSCĐ → Fixed Asset Register" — Script Report S21-DN thay
- ⏸️ Asset Value Adjustment — không expose, Settings flag default off

### 5.3 Mitigate UX cho phiếu thuần TSCĐ vs CCDC

`scope` strict 2-value (không Mixed) → khi giao 1 lúc cả TSCĐ + CCDC phải lập 2 phiếu. Mitigate:

- Button toolbar trên Asset Handover: "📋 Sao chép sang phiếu CCDC" — duplicate phiếu hiện tại với scope đảo, user thay items.
- Tương tự cho Stocktake.

> **Why scope strict không Mixed:** Frappe `route_options={"scope":"TSCĐ"}` chỉ exact match. Nếu cho phép Mixed, phiếu Mixed không show ở cả 2 link sidebar → defeats γ2. Strict scope cũng khớp pháp lý: S22-DN của TT99 quy định mỗi đơn vị mở 2 sổ riêng (1 cho TSCĐ + 1 cho CCDC), nên 2 phiếu là chuẩn.

## 6. Print Formats

| # | DocType nguồn | Tên biên bản | Mã/Mẫu | Số ký |
|---|---------------|-------------|--------|-------|
| 1 | Asset Handover (TSCĐ) | Sổ S22-DN — Theo dõi TSCĐ tại nơi sử dụng | S22-DN (TT99 PL3) | 3 (Bên giao / Bên nhận / Kế toán) |
| 2 | Asset Handover (CCDC) | Sổ S22-DN — Theo dõi CCDC tại nơi sử dụng | S22-DN (TT99 PL3) | 3 |
| 3 | Asset Stocktake (TSCĐ) | Biên bản kiểm kê TSCĐ | (mẫu thị trường) | 3 (Trưởng đoàn / Thủ kho / Kế toán) |
| 4 | Asset Stocktake (CCDC) | Biên bản kiểm kê CCDC | (mẫu thị trường) | 3 |
| 5 | Asset Repair | Biên bản sửa chữa TSCĐ | (mẫu thị trường) | 3 (Người dùng / Kỹ thuật / Kế toán) |
| 6 | CCDC Writeoff | Biên bản ghi giảm CCDC | (mẫu thị trường) | 2 (Bên giữ / Kế toán) |
| 7 | Sổ S21-DN (Report) | S21-DN — Sổ tài sản cố định | S21-DN (TT99 PL3) | — báo cáo |
| 8 | Sổ S22-DN (Report) | S22-DN — Theo dõi TSCĐ/CCDC theo nơi sử dụng | S22-DN (TT99 PL3) | — báo cáo |
| 9 | Asset (Ghi tăng) | Biên bản giao nhận TSCĐ | 01-TSCĐ (TT99 PL2) | 3 (Bên giao / Bên nhận / Kế toán) |

→ 9 print format cần build (Asset Disposal đã có v1). Pattern Jinja A4 dọc, font Times New Roman 12pt, 3 ô chữ ký giống Cash Count + Asset Disposal đã làm.

## 7. i18n & Label Strategy

### 7.1 ERPNext built-in translations (vi.csv)

Map cụ thể vào `apps/vn_accounting/vn_accounting/translations/vi.csv`:

| ERPNext label | VN label |
|---------------|---------|
| Asset | Tài sản cố định |
| Asset Category | Nhóm tài sản cố định |
| Asset Movement | Điều chuyển tài sản |
| Asset Repair | Sửa chữa tài sản |
| Gross Purchase Amount | Nguyên giá |
| Asset Owner | Người sở hữu |
| Custodian | Người giữ tài sản |
| Available-for-use Date | Ngày đưa vào sử dụng |
| Depreciation Method | Phương pháp khấu hao |
| Straight Line | Đường thẳng |
| Double Declining Balance | Số dư giảm dần |
| Manual | Thủ công |
| Total Number of Depreciations | Tổng số kỳ khấu hao |
| Frequency of Depreciation | Tần suất khấu hao |
| Repair Status | Trạng thái sửa chữa |
| Disposal Date | Ngày thanh lý |

### 7.2 Property Setter — Hide depreciation methods

Ẩn 3 method ít dùng / không khớp VAS:

```python
# fixtures: property_setter
{"doc_type": "Asset", "field_name": "depreciation_method",
 "property": "options", "value": "\nĐường thẳng\nSố dư giảm dần"}
```

→ Chỉ còn 2 option phù hợp: "Đường thẳng" (Straight Line) và "Số dư giảm dần" (Double Declining Balance hệ số 2). Hide "Manual", "Written Down Value", "Single Declining Balance".

> **Why ẩn Manual:** Manual cho phép kế toán nhập tay từng kỳ, dễ sai chuẩn VAS. Ẩn để force chọn 2 method công thức.
> **TODO:** "Theo sản lượng" (Units of Production) chưa support trong ERPNext native. Đánh dấu future work, không trong sprint này.

### 7.3 Custom Fields

| DocType | Field | Type | Why |
|---------|-------|------|-----|
| Item | is_low_value_asset | Check | Phân biệt CCDC khi mua qua PI |
| Asset Repair | repair_classification | Select [Chi phí, Sửa chữa lớn vốn hóa, Nâng cấp cải tạo] | VAS phân loại 3 cách |
| Asset Repair | capitalization_je | Link Journal Entry | JE vốn hóa khi classification != Chi phí |

### 7.4 Asset Category re-seed (theo TT99/2025)

5 nhóm hữu hình + 1 nhóm vô hình = **6 categories**:
- 211 Tài sản cố định hữu hình (group)
  - 2111 Nhà cửa, vật kiến trúc
  - 2112 Máy móc thiết bị
  - 2113 Phương tiện vận tải
  - 2114 Thiết bị dụng cụ quản lý
  - 2115 Cây trồng vật nuôi
- 213 Tài sản cố định vô hình (leaf)

### 7.5 CCDC Category seed

5 nhóm mặc định:
- Bàn ghế văn phòng
- Máy tính, thiết bị IT
- Dụng cụ sản xuất
- Đồ bảo hộ
- Khác

## 8. TT99/2025 Compliance Items

| # | Item | Action |
|---|------|--------|
| 1 | TK 242 rename | Update `vn_small_enterprise.json` + `vn_large_enterprise.json` + vi.csv: "Chi phí chờ phân bổ" → **"Chi phí trả trước"** |
| 2 | Sổ S21-DN | Tạo Script Report đúng cột mẫu (mã TS, tên, ngày sử dụng, nguyên giá, kỳ KH, % KH năm, GTKH năm, GTKH luỹ kế, GTCL, ghi chú) |
| 3 | Sổ S22-DN | Tạo Script Report group by location/department, hiển thị TSCĐ + CCDC tại nơi đó |
| 4 | Asset Category re-seed | Như mục 7.4 |
| 5 | CCDC Category seed | Như mục 7.5 |
| 6 | Khấu hao methods hide | Property Setter ẩn 3 method (mục 7.2) |
| 7 | Khấu hao "Theo sản lượng" | TODO note trong README, future work |

## 9. VN Accounting Settings — Tab "Phân quyền TSCĐ & CCDC"

### 9.1 UI Layout

Tab dedicated trong VN Accounting Settings (Single DocType) với 4 sections:

```
[Section] Mức ngưỡng kiểm soát
  ☐ Bật ngưỡng kiểm soát theo giá trị
    Ngưỡng thanh lý cần KTT duyệt           50,000,000 đ
    Ngưỡng bàn giao cần KTT đồng ký        100,000,000 đ
    Ngưỡng ghi tăng TSCĐ tối thiểu           30,000,000 đ

[Section] Phạm vi xem theo phòng ban
  ☐ User chỉ xem TSCĐ/CCDC trong phòng ban của mình
  ☐ Trưởng phòng xem được phòng cấp con   (v2 — disabled v1)

[Section] Bật / Tắt module
  ☐ Cho phép đánh giá lại tài sản (Asset Value Adjustment)  — default OFF

[Section] Ma trận phân quyền (child table)
  ┌──────┬─────────────────┬─────────────────┬───┬───┬───┬─────┬────────┐
  │ Bật  │ DocType         │ Role            │ R │ W │ C │ Sub │ Cancel │
  ├──────┼─────────────────┼─────────────────┼───┼───┼───┼─────┼────────┤
  │ ☑    │ Asset           │ Accounts User   │ ✓ │ ✓ │ ✓ │  ✓  │        │
  │ ☑    │ Asset           │ Accounts Mgr    │ ✓ │ ✓ │ ✓ │  ✓  │   ✓    │
  │ ☑    │ Asset           │ Dept Head       │ ✓ │   │   │     │        │
  │ ...  │ ...             │ ...             │   │   │   │     │        │
  └──────┴─────────────────┴─────────────────┴───┴───┴───┴─────┴────────┘
  [+ Thêm dòng]   [↺ Khôi phục mặc định]   [💾 Áp dụng]

[Section] Hoạt động gần đây (audit log)
  • 2026-04-29 09:15 — admin sửa quyền Asset Stocktake / Stocktake Mbr (tắt)
  • 2026-04-28 14:30 — admin đổi ngưỡng thanh lý 30tr → 50tr
```

### 9.2 4 Capabilities

| Capability | Cơ chế |
|------------|--------|
| Xem mặc định | Mỗi dòng có icon 📍 nếu đã sửa khác mặc định; tooltip hiện giá trị gốc đọc từ fixture file |
| Thiết lập | Sửa trực tiếp child table (R/W/C/Sub/Cancel checkboxes, role/doctype Link); validate khi click "Áp dụng" |
| Thay đổi mặc định | Edit row tự đánh dấu `is_modified=1` → 📍 hiện. "Khôi phục mặc định" reload fixture, reset table |
| Bật / Tắt | Cột `enabled` Check. Tắt → row bị xóa khỏi Custom DocPerm khi Áp dụng. Bật → tạo lại |

### 9.3 Default permissions fixture

`vn_accounting/fixtures/asset_permission_defaults.json` — file-based, version-controlled:

```json
[
  {"doctype_name": "Asset", "role": "Accounts User",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 0, "if_owner": 0},
  {"doctype_name": "Asset", "role": "Accounts Manager",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "if_owner": 0},
  {"doctype_name": "Asset", "role": "Department Head",
   "read": 1, "write": 0, "create": 0, "submit": 0, "cancel": 0, "if_owner": 0},
  {"doctype_name": "CCDC Item", "role": "Accounts User",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 0, "if_owner": 0},
  {"doctype_name": "CCDC Item", "role": "Accounts Manager",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "if_owner": 0},
  {"doctype_name": "Asset Handover", "role": "Accounts User",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 0, "if_owner": 0},
  {"doctype_name": "Asset Handover", "role": "Accounts Manager",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "if_owner": 0},
  {"doctype_name": "Asset Handover", "role": "Department Head",
   "read": 1, "write": 0, "create": 0, "submit": 0, "cancel": 0, "if_owner": 0},
  {"doctype_name": "Asset Stocktake", "role": "Accounts User",
   "read": 1, "write": 1, "create": 1, "submit": 0, "cancel": 0, "if_owner": 0},
  {"doctype_name": "Asset Stocktake", "role": "Stocktake Member",
   "read": 1, "write": 1, "create": 0, "submit": 0, "cancel": 0, "if_owner": 0},
  {"doctype_name": "Asset Stocktake", "role": "Accounts Manager",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "if_owner": 0},
  {"doctype_name": "Asset Repair", "role": "Accounts User",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 0, "if_owner": 0},
  {"doctype_name": "Asset Repair", "role": "Accounts Manager",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "if_owner": 0},
  {"doctype_name": "CCDC Writeoff", "role": "Accounts User",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 0, "if_owner": 0},
  {"doctype_name": "CCDC Writeoff", "role": "Accounts Manager",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "if_owner": 0},
  {"doctype_name": "CCDC Allocation Schedule", "role": "System Manager",
   "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "if_owner": 0}
]
```

### 9.4 Sync mechanism

```python
# vn_accounting_settings.py
def on_update(self):
    self._validate_thresholds()
    self._sync_permissions_to_docperm()
    self._apply_dept_user_permissions()  # if scope_by_department flag on
    self._add_audit_log_entry()

def _sync_permissions_to_docperm(self):
    affected_doctypes = {"Asset", "CCDC Item", "Asset Handover",
                         "Asset Stocktake", "Asset Repair", "CCDC Writeoff",
                         "CCDC Allocation Schedule", "Asset Disposal"}
    frappe.db.delete("Custom DocPerm",
                     filters={"parent": ["in", list(affected_doctypes)]})
    for rule in self.permission_matrix:
        if rule.enabled:
            frappe.get_doc({
                "doctype": "Custom DocPerm",
                "parent": rule.doctype_name,
                "role": rule.role,
                "read": rule.read, "write": rule.write,
                "create": rule.create, "submit": rule.submit,
                "cancel": rule.cancel, "if_owner": rule.if_owner,
            }).insert(ignore_permissions=True)
    frappe.clear_cache()

@frappe.whitelist()
def reset_permission_matrix():
    """Server method called from button 'Khôi phục mặc định'."""
    settings = frappe.get_single("VN Accounting Settings")
    settings.permission_matrix = []
    defaults = frappe.get_file_json(
        frappe.get_app_path("vn_accounting", "fixtures",
                            "asset_permission_defaults.json")
    )
    for rule in defaults:
        rule["enabled"] = 1
        settings.append("permission_matrix", rule)
    settings.save()
    return _("Đã khôi phục mặc định")
```

### 9.5 Threshold-based validation

3 ngưỡng độc lập. 2 ngưỡng đầu (thanh lý, bàn giao) phụ thuộc flag "Bật ngưỡng kiểm soát theo giá trị". Ngưỡng thứ 3 (ghi tăng TSCĐ) là chuẩn pháp lý TT45/2013, **luôn check** không phụ thuộc flag.

| Ngưỡng | Implement ở đâu | Hành vi | Flag-gated? |
|--------|----------------|--------|------------|
| Thanh lý ≥ 50tr | Asset Disposal `validate()` | Throw nếu non-Manager submit | Có (tắt flag → bỏ qua) |
| Bàn giao ≥ 100tr | Asset Handover `validate()` | Field `co_signer_employee` reqd | Có (tắt flag → bỏ qua) |
| Ghi tăng TSCĐ < 30tr | Asset `validate()` | Warning (không block): "cân nhắc tạo CCDC" | Không (luôn check theo TT45/2013) |

### 9.6 Department scope

Khi flag `scope_by_department` bật:

```python
def apply_dept_user_permissions(self):
    if not self.scope_by_department:
        return
    for user in frappe.get_all("User", filters={"enabled": 1}, fields=["name"]):
        u = frappe.get_doc("User", user.name)
        if not u.department:
            continue
        for dt in ["Asset", "CCDC Item", "Asset Handover", "Asset Stocktake"]:
            up_name = f"{u.name}-{dt}-{u.department}"
            if not frappe.db.exists("User Permission", up_name):
                frappe.get_doc({
                    "doctype": "User Permission",
                    "user": u.name,
                    "allow": "Department",
                    "for_value": u.department,
                    "applicable_for": dt,
                    "apply_to_all_doctypes": 0,
                }).insert(ignore_permissions=True)
```

> **Trade-off v1:** "Trưởng phòng xem cấp con" disabled. Department Head chỉ xem chính phòng họ. Nâng cấp v2 cần custom permission query xử lý hierarchy.

### 9.7 Audit log

Field `permission_audit_log: Long Text` (JSON array). Mỗi `on_update` ghi:

```json
[
  {"ts": "2026-04-29 09:15:00", "user": "admin@dcnet.vn",
   "action": "modify", "field": "permission_matrix[3].enabled",
   "before": 1, "after": 0,
   "details": "Asset Stocktake / Stocktake Member tắt"}
]
```

Hiển thị 5 dòng mới nhất trong UI. Cũ hơn truy lục từ field text.

## 10. Edge Cases

1. **TSCĐ ghi tăng từ PI nhưng PI cancel** → Asset draft auto-cancel qua hook `on_cancel` của PI
2. **CCDC mua nhưng chưa xuất dùng** → sit on TK 153 indefinitely. Status `Mới mua`. Cảnh báo nếu >12 tháng
3. **Backdated Asset Handover** → cần `set_posting_time=1` trước khi set `posting_date`
4. **Asset đã thanh lý trong Stocktake** → validate Stocktake Item không include asset có `status=Disposed`
5. **CCDC phân bổ chưa hết bị Writeoff** → CCDC Allocation Schedule cancel + JE phần dư về 627/641/642
6. **Nâng cấp giữa kỳ khấu hao** → recreate Asset Depreciation Schedule với `(nguyên giá mới - GTCL)` chia thời gian sử dụng còn lại
7. **Bàn giao về kho (de-handover)** → Asset Handover với `to_employee=NULL`, `location=Kho`
8. **Period Closing đã đóng** → ERPNext native check, không cho tạo bản ghi mới trong kỳ đã đóng
9. **CCDC giá trị 0 hoặc âm** → validate min nguyên giá > 0
10. **Asset cùng tên trong cùng company** → validate unique
11. **Stocktake với 0 item missing/damaged** → vẫn cho approve (kiểm kê confirm sạch)
12. **Asset Handover scope mismatch** → validation error "Item phải khớp scope của phiếu"
13. **Ngưỡng vô hiệu** (Settings flag tắt) → bỏ qua tất cả threshold check
14. **Custom DocPerm conflict với Standard DocPerm** → Custom thắng (Frappe behavior); cảnh báo trong UI nếu có conflict
15. **Reset Permission Matrix khi đang có pending changes** → confirm dialog
16. **Migration trên site cũ đã có Custom DocPerm thủ công** → trên `after_install`, KHÔNG xóa Custom DocPerm hiện có. Chỉ load fixture vào Settings.permission_matrix nếu `permission_matrix` rỗng. User có thể sync sau khi review.
17. **Asset Movement bóng tạo bởi Asset Handover bị user xóa thủ công** → handover.cancel() vẫn revert được vì đọc `before_handover_snapshot` chứ không đọc Asset Movement

## 11. Phasing — 4 Sprints Sequential

### Sprint 1 (3-4 ngày) — Foundation + TSCĐ polish

- TK 242 rename trong 2 file COA + vi.csv
- Property Setter hide 3 depreciation methods
- Translations vi.csv polish ~30 label TSCĐ
- Asset Category re-seed 5 nhóm chuẩn
- Sidebar reorg: tách 2 section TSCĐ + CCDC, thêm 4 link γ2 (placeholder cho CCDC links chưa có DocType)
- Custom Field `Item.is_low_value_asset`
- Asset Repair: thêm `repair_classification` + JE routing + biên bản sửa chữa
- Sổ S21-DN Script Report
- VN Accounting Settings tab "Phân quyền TSCĐ & CCDC" (UI + sync logic, defaults file, audit log)

**Acceptance:**
- [ ] TK 242 hiển thị "Chi phí trả trước" trên Desk + báo cáo
- [ ] Asset depreciation_method dropdown chỉ còn 2 option
- [ ] Sidebar có 2 section TSCĐ + CCDC, click vào "Bàn giao TSCĐ" route đúng (link dẫn đến trang lỗi nếu DocType chưa có — sẽ fix Sprint 3)
- [ ] Sổ S21-DN report render đúng cột TT99
- [ ] VN Accounting Settings tab phân quyền lưu được rule, sync sang Custom DocPerm verify qua `bench --site clear-cache && SQL`

### Sprint 2 (4-5 ngày) — CCDC Backbone

- DocType `CCDC Category` (seed 5 nhóm)
- DocType `CCDC Item` (Asset-equivalent đơn giản)
- DocType `CCDC Allocation Schedule` + child `CCDC Allocation Entry`
- Scheduler hook hàng tháng (tham khảo `process_asset_depreciation`)
- Hook PI submit: nếu item.is_low_value_asset=1 → auto-create CCDC Item draft
- DocType `CCDC Writeoff` + biên bản ghi giảm

**Acceptance:**
- [ ] Tạo CCDC Item từ PI, submit → JE 153 / 331 đúng
- [ ] CCDC Item submit + ngày xuất + N kỳ → JE 242/153 + Allocation Schedule auto-create
- [ ] Scheduler chạy đầu tháng 5 → JE 627/642 / C 242 đúng amount
- [ ] CCDC Writeoff giữa kỳ → JE phần dư 242 + phần 153 đúng
- [ ] Sidebar links CCDC route đúng

### Sprint 3 (3-4 ngày) — Bàn giao + Kiểm kê

- DocType `Asset Handover` + child `Asset Handover Item` + Dynamic Link
- Asset Handover on_submit: update Asset/CCDC.location + custodian + tạo Asset Movement bóng
- Validation scope match
- Threshold validation co_signer_employee
- Print biên bản S22-DN (1 template, render 2 mẫu cho TSCĐ vs CCDC)
- DocType `Asset Stocktake` + child + workflow 4 state
- Auto-load items theo location/department
- Approve action → JE chênh lệch + update target status
- Print biên bản kiểm kê
- Sổ S22-DN Script Report

**Acceptance:**
- [ ] Tạo Bàn giao TSCĐ phòng IT → submit → Asset.custodian update + Asset Movement bóng tạo + biên bản S22-DN render
- [ ] Tạo Bàn giao CCDC tương tự
- [ ] Validation: thêm CCDC vào phiếu scope=TSCĐ → error
- [ ] Threshold: bàn giao 150tr (> 100tr) không co_signer → error
- [ ] Kiểm kê phòng IT, đánh dấu 1 missing → approve → JE 1381 đúng + asset.status=Lost
- [ ] Sổ S22-DN report group by location đúng
- [ ] "Sao chép sang phiếu CCDC" button hoạt động

### Sprint 4 (1-2 ngày) — Polish + Demo data + QA

- Demo data: 10 TSCĐ (5 ghi tăng từ PI + 5 backdate) + 20 CCDC (10 đang phân bổ + 5 hết phân bổ + 5 đã ghi giảm) + 5 bàn giao + 1 kiểm kê
- Auto qua dcnet_sample patch
- 3 Persona QA round (Section 12)
- Design QA exploratory (Playwright MCP)
- Fix bugs phát sinh
- Update docs/CODEBASE.md + FEATURES.md

**Acceptance:**
- [ ] Demo data hiển thị đầy đủ trong UI
- [ ] 3 Persona QA pass 0 console error
- [ ] Design QA proposals logged hoặc fixed
- [ ] CODEBASE.md liệt kê 9 DocType mới + relationship

**Tổng:** 11-15 ngày làm việc / ~2 tuần thực tế.

## 12. Testing Strategy

### 12.1 Tier 1 — Unit tests (TDD, pure functions)

| Module | File | Coverage target |
|--------|------|-----------------|
| ccdc_allocation | `tests/test_ccdc_allocation.py` | tính lịch N kỳ, amount mỗi kỳ, edge case |
| permission_sync | `tests/test_permission_sync.py` | sync rules → Custom DocPerm idempotent + reset_permission_matrix loading từ fixture |
| asset_repair_classification | `tests/test_asset_repair.py` | route JE 211/241 vs 627/641/642 |
| stocktake_diff_calc | `tests/test_stocktake.py` | tính chênh lệch → JE 1381/3381 |
| s21_dn_report_logic | `tests/test_s21_dn.py` | aggregation queries cho Sổ S21-DN |

→ ≥80% coverage cho 5 module trên. Pure function ưu tiên.

### 12.2 Tier 2 — Integration tests (workflow + JE)

| Scenario | Assert |
|---------|--------|
| Mua TSCĐ qua PI auto | Asset draft tạo, gross_purchase_amount khớp |
| Mua CCDC qua PI auto | CCDC Item draft tạo, cost khớp |
| CCDC Allocation full cycle 12 kỳ | TK 242 = 0, 627/641/642 += cost; status=Hết phân bổ |
| Bàn giao TSCĐ S22-DN | Asset.custodian/location update + Asset Movement bóng tạo |
| Kiểm kê thiếu tài sản | JE N 1381 / C 211; asset.status=Lost |
| Sửa chữa lớn vốn hóa | JE N 211 / C 241 + Depr Schedule recreate |
| CCDC Writeoff giữa kỳ | TK 242 cleared phần dư |
| Threshold check thanh lý | Validation error nếu non-Manager submit |
| Permission Matrix sync | Custom DocPerm rows khớp Settings.permission_matrix |
| Reset to defaults | Settings.permission_matrix khớp fixture file |

→ Chạy qua `bench console` (`bench run-tests` xung đột với sample data).

### 12.3 Tier 3 — Persona-based QA

**Persona 1: Kế toán tài sản** (daily user)
- Tạo TSCĐ từ PI → bàn giao phòng IT → in S22-DN → tháng sau khấu hao auto chạy
- Tạo CCDC từ PI → xuất dùng phân bổ 12 tháng → kiểm tra JE phân bổ tháng đầu
- Sửa chữa máy tính (chi phí) → xem GL có 627
- Kiểm kê phòng IT cuối quý → 1 máy thiếu → submit Stocktake → KTT approve

**Persona 2: Kế toán trưởng** (approval flow)
- Approve Stocktake với chênh lệch → kiểm tra GL chính xác
- Approve Asset Disposal nguyên giá 80tr (> ngưỡng) → check workflow chữ ký
- Đổi ngưỡng bàn giao trong Settings → test lại flow

**Persona 3: Trưởng phòng** (read-only own dept)
- Login với Department Head + User Permission Phòng IT → xem được TSCĐ phòng IT
- KHÔNG xem được TSCĐ phòng Kế toán
- KHÔNG có button Tạo/Submit

→ Mỗi round: **0 console error**, golden path < 5 phút, biên bản print PDF đúng layout.

### 12.4 Tier 4 — Design QA exploratory

Playwright MCP chạy sau persona QA pass. Screenshot toàn bộ 9 form Asset chính + 9 print format. Edge case: tạo CCDC 0đ, nguyên giá âm, Handover không item. 2-tier auto-fix per `feature-development-process.md`:
- Spacing/alignment/labels → fix ngay, commit atomic
- Flow change → log `docs/design-qa-proposals/asset-polishing.md`

### 12.5 Coverage gates

| Sprint | Gate |
|--------|------|
| Sprint 1 | Tier 1 cho asset_repair + permission_sync ≥80% |
| Sprint 2 | Tier 1 cho ccdc_allocation; Tier 2 mua + phân bổ pass |
| Sprint 3 | Tier 2 bàn giao + kiểm kê + sửa chữa pass |
| Sprint 4 | Persona 3 round 0 error + Design QA done |

## 13. Out of Scope (v1)

- Khấu hao "Theo sản lượng" (Units of Production) — ERPNext native chưa support
- Asset Value Adjustment (đánh giá lại) — Settings flag default off, expose v2 khi cần
- Trưởng phòng xem cấp con (department hierarchy) — v2
- BĐS đầu tư (TK 217 + 2147) — TT99 có quy định nhưng SME hiếm dùng, v2
- Asset Capitalization workflow (mua nhiều hạng mục → 1 TSCĐ) — v2
- Mobile bàn giao (chữ ký số trên điện thoại) — v3

## 14. References

**Pháp lý:**
- TT99/2025/TT-BTC — Hướng dẫn Chế độ Kế toán Doanh nghiệp (hiệu lực 01/01/2026)
- TT45/2013/TT-BTC — Quản lý, sử dụng và trích khấu hao TSCĐ (vẫn governing ngưỡng 30tr)

**Mẫu sổ Phụ lục III TT99:**
- S21-DN — Sổ tài sản cố định
- S22-DN — Sổ theo dõi TSCĐ và CCDC tại nơi sử dụng

**Codebase pattern reference:**
- `vn_accounting/doctype/asset_disposal/` — pattern custom DocType + 4-sign biên bản
- `vn_accounting/doctype/cash_count/` — pattern workflow 4 state + biên bản 3 ký
- `vn_accounting/workspace_sidebar/vn_accounting.json` — sidebar mother-section + items
- `apps/erpnext/erpnext/assets/doctype/` — ERPNext Asset, Asset Repair, Asset Movement, Asset Depreciation Schedule
