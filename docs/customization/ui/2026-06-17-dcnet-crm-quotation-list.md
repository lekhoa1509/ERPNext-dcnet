# DCNET CRM Quotation List (Danh sách báo giá)

## Overview

Thêm màn hình danh sách Báo giá riêng trong `dcnet_crm` tại
`/desk/dcnet-crm?view=quotations`, dùng DocType chuẩn `Quotation` và permission
chuẩn của ERPNext. Giao diện mô phỏng màn "Tất cả báo giá" của MISA AMIS CRM
(reference UX), tái sử dụng layout/CSS của màn Đơn hàng (`orders-list-layout`).

Nguồn yêu cầu: `docs/feature/FEATURE_SPECIFICATION.md` (phân hệ Báo giá).
Reference UX: ảnh chụp MISA AMIS CRM `/crm/quote/list`.

## Requirements

- Bảng danh sách báo giá dày, các cột: Thẻ (trạng thái), Số báo giá,
  Ngày báo giá, Hiệu lực đến, Khách hàng, Liên hệ.
- Tìm kiếm thông minh + làm mới + ẩn/hiện giá trị + bật/tắt panel Bộ lọc.
- Panel "Hàng hóa" bên phải hiển thị line items của báo giá đang chọn, mở rộng
  từng dòng để xem đơn giá sau CK, thành tiền và mô tả.
- Panel "Bộ lọc": bộ lọc đã lưu (báo giá tháng/tuần này, còn hiệu lực) và tiêu
  chí lọc chọn được (số báo giá, ngày, khách hàng, liên hệ, tổng tiền, trạng thái).
- Footer tổng hợp: Tổng số, Thành tiền, Tiền thuế, Tiền chiết khấu, Tổng tiền +
  phân trang (20/50/100 dòng/trang).
- Nút "Nhập từ Excel" mở Data Import của `Quotation`.
- Nút "+ Thêm" mở form Quotation chuẩn (chỉ khi có quyền create).
- Click số báo giá / double-click dòng mở form Quotation chuẩn.

## Implementation

- Frontend
  - `frontend/src/features/quotations/composable.js` — `useQuotations(ctx)`:
    state panel Hàng hóa (`get_quotation_items`), state bộ lọc + saved filters.
  - `frontend/src/features/quotations/template.js` — markup màn danh sách,
    chain `v-else-if="route === 'quotations'"` (nối sau accounts template).
  - `frontend/src/app.js` — import composable/template, khởi tạo
    `quotationsState`, nhánh filter trong `loadRows()`, watcher
    `quotationsFilterValues`, spread vào return, nối template.
  - `frontend/src/styles.css` — class riêng cho cột Thẻ/Khách hàng/Liên hệ,
    badge `.ot-qstatus--*`, nút `.crm-btn-ghost`, tái dùng `orders-*`/`odp-*`/`ofp-*`.
- Backend
  - `dcnet_crm/api.py` — mở rộng `RESOURCE_CONFIG["quotations"]` (thêm
    `contact_person`, `contact_display`, `order_type`, `total`, `net_total`,
    `total_taxes_and_charges`, `discount_amount`, `company`), thêm whitelisted
    GET `get_quotation_items(name)` trả line items, đổi default_order theo
    `transaction_date desc`.

## Data Ownership

| UI | Standard data source |
|---|---|
| Báo giá | `Quotation` |
| Line items | `Quotation Item` (qua `get_quotation_items`) |
| Liên hệ | `Quotation.contact_display` / `contact_person` |

Không thêm DocType hay Custom Field mới. Mọi đọc đều qua
`frappe.get_list`/`frappe.get_doc` tôn trọng permission (`_check_permission`).

## Verification

- `bench build --app dcnet_crm` thành công (bundle ~731.9 kb).
- `get_list(resource="quotations")` trả về đúng cấu trúc fields.
- Tạo Quotation thử nghiệm trong transaction → `get_list` + `get_quotation_items`
  trả dữ liệu đúng → `frappe.db.rollback()` (không để lại dữ liệu rác).
- `bench --site flow.local clear-cache` + `clear-website-cache`.

## Known Limitations

- Chưa có form tạo/sửa báo giá nội bộ trong `dcnet_crm`; "+ Thêm" và click mở
  form Quotation chuẩn.
- Cột "Thẻ" hiển thị trạng thái Quotation, chưa hỗ trợ tag tùy chỉnh như MISA.
- Aggregate footer tính trên các dòng của trang hiện tại (không phải toàn bộ
  kết quả lọc).

---

## Cập nhật: Form "Thêm Báo giá" (create-quotation) — 2026-06-17

### Overview

Thêm form tạo báo giá nội bộ tại `/desk/dcnet-crm?view=create-quotation`, mở
trực tiếp tại trang (không popup) khi bấm "+ Thêm" trong danh sách Báo giá.
Mô phỏng mẫu "Thêm Báo giá - Mẫu báo giá DVVT" của MISA AMIS CRM (reference UX),
tái sử dụng layout form Đơn hàng (`opportunity-form-page` + `so-items-table`).

### Requirements (theo mẫu MISA)

- Mở tại trang, header có: tên mẫu báo giá (dropdown), Hủy, Lưu và thêm, Lưu.
- Section "Thông tin chi tiết": Số báo giá (mã tự sinh, disabled), Ngày báo giá,
  Cơ hội, Tình trạng, Chu kỳ thanh toán, Khu vực lắp đặt dịch vụ, Khách hàng,
  Hiệu lực đến ngày, Liên hệ, Mã số thuế, Email KH.
- Section "Thông tin mô tả": Mô tả, Thời gian triển khai, Cam kết chất lượng (SLA).
- Section "Thông tin hàng hóa": bảng 17 cột + dòng Tổng cộng, nút Thêm dòng,
  checkbox "Tự động tăng SL khi chọn trùng".
- Section "Thông tin hệ thống": Người thực hiện, Công ty, Dùng chung.

### Implementation

- Frontend
  - `frontend/src/features/quotations/composable.js` — bổ sung state form
    (`createQTForm`, `createQTItems`, `qtFormOptions`), `openCreateQuotation`,
    `backToQuotations`, các hàm tính tiền (`qtItemPreTotal`, `qtItemDiscount`,
    `qtItemTax`, `qtSubtotal`, `qtGrandTotal`...), `saveCreateQuotation`.
  - `frontend/src/features/quotations/template.js` — markup form
    `v-else-if="route === 'create-quotation'"` (đứng trước list view).
  - `frontend/src/app.js` — `createDocument` cho `quotations` mở form nội bộ;
    `syncRouteUrl`/`syncNativeSidebarActive`/`readRoute` xử lý route mới.
  - `frontend/src/styles.css` — `.col-amt-total`, `.qt-goods-head-actions`,
    `.qt-auto-qty`.
- Backend (`dcnet_crm/api.py`)
  - `get_quotation_form_options(customer=None)` — GET, trả dropdown options.
  - `create_quotation(data)` — POST, insert Quotation chuẩn (không
    `ignore_validate` để `set_missing_values` tự điền `conversion_rate`,
    `price_list_currency`...). Custom field chỉ set khi meta đã có field.

### Data Ownership

| UI | Standard data source |
|---|---|
| Báo giá | `Quotation` |
| Line items | `Quotation Item` |
| Liên hệ / Cơ hội | `Contact` / `Opportunity` |

Không tạo DocType/Custom Field mới. Các cột A-End/Z-End/Account hiển thị theo
mẫu MISA nhưng chỉ lưu khi custom field tương ứng đã tồn tại trên DocType
(hiện chưa có → bỏ qua, ghi nhận chờ duyệt).

### Verification

- `bench build --app dcnet_crm` OK (bundle ~748.6 kb).
- `get_quotation_form_options()` trả đủ 8 nhóm options (items: 2000).
- `create_quotation(...)` tạo Quotation thật trong transaction → grand_total
  đúng (qty 3 × 180.000 = 540.000) → `frappe.db.rollback()`.

### Known Limitations

- Chưa có chế độ sửa (edit) báo giá nội bộ; mở báo giá cũ vẫn dùng form chuẩn.
- A-End/Z-End/Account chưa lưu (chờ duyệt Custom Field cho Quotation Item).
- "Tự động tăng SL khi chọn trùng" mới là cờ UI, chưa nối logic chọn hàng hóa
  hàng loạt (form hiện thêm dòng thủ công + autocomplete mã hàng).


---

## Cập nhật: Empty state + popup Chọn hàng hóa (form Thêm Báo giá) — 2026-06-17

### Thay đổi

- Khi tạo báo giá mới, bảng "Thông tin hàng hóa" KHÔNG còn hiển thị 1 dòng
  trống mặc định. Thay vào đó hiện empty state với 2 nút: "+ Chọn hàng hóa"
  (mở popup) và "Thêm dòng trống".
- Popup "Chọn hàng hóa": tìm theo mã/tên, lọc theo nhóm, chọn nhiều dòng,
  phân trang (20/50/100). Nút xác nhận thêm các hàng hóa đã chọn vào bảng.
- Khi đã có ít nhất 1 dòng: bảng + dòng Tổng cộng hiển thị như cũ, kèm nút
  "Thêm dòng" và "+ Chọn hàng hóa" ở thanh hành động dưới bảng; checkbox
  "Tự động tăng SL khi chọn trùng" chỉ hiện khi đã có dòng.

### Implementation

- `frontend/src/features/quotations/composable.js` — `openCreateQuotation`
  khởi tạo `createQTItems = []`; thêm state + computed cho popup
  (`qtItemPickerOpen`, `qtItemPickerFiltered`, `qtItemPickerRows`...),
  `openQTItemPicker`/`closeQTItemPicker`/`toggleQTItemPickerRow`/
  `confirmQTItemPicker` (tôn trọng cờ "Tự động tăng SL khi chọn trùng").
- `frontend/src/features/quotations/template.js` — empty state +
  popup `item-picker-modal` (tái dùng CSS picker của form Đơn hàng:
  `<header>`/`<footer>`, `item-picker-*`).
