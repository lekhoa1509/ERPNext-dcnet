# DCNET CRM — Form Thêm Liên hệ (MISA-style)

## Tổng quan

Tạo form "Thêm Liên hệ" mở trực tiếp tại trang trong `dcnet-crm` (route
`?view=create-contact`), bám layout MISA AMIS 100%: Thông tin chung, Thông tin
địa chỉ, Thông tin địa chỉ giao hàng, Thông tin mô tả, Thông tin hệ thống.

Bấm "＋ Thêm" ở danh sách Liên hệ sẽ mở thẳng form này (không còn dùng
`frappe.new_doc`).

## Yêu cầu

- Form mở tại trang (không popup), header có: chọn mẫu, "Sửa bố cục", Hủy,
  "Lưu và thêm", "Lưu".
- Các nhóm trường khớp ảnh MISA: Mã liên hệ (tự sinh), Xưng hô, Họ và đệm, Tên
  (bắt buộc), Họ và tên (readonly ghép), Chức danh, Phòng ban, Tổ chức, Phân
  loại khách hàng, Không gọi điện, Không gửi Email, Điện thoại khác, ĐT di động,
  Email cá nhân, ĐT cơ quan, Nguồn gốc, Email cơ quan, Zalo.
- Địa chỉ + Địa chỉ giao hàng dùng cascade VN (tỉnh → phường/xã theo cải cách
  2025) như form Khách hàng; có nút "Sao chép địa chỉ".

## Implementation

- `frontend/src/features/contacts/composable-create.js` — `useCreateContact`:
  state form, options, cascade địa chỉ VN (`fetchVnProvinces`/`fetchVnWards`),
  `openCreateContact`/`cancelCreateContact`/`saveCreateContact`,
  `copyContactAddress`.
- `frontend/src/features/contacts/template-create.js` — markup MISA, tái dùng
  class `ccf-*` của form Khách hàng.
- `frontend/src/app.js` — import + instantiate `createContState`, xử lý route
  `create-contact` (sidebar label, danh sách route hợp lệ), nút "＋ Thêm" ở
  danh sách Liên hệ mở form nội bộ, spread state, nối template.
- `dcnet_crm/api.py`:
  - `get_contact_create_options()` — GET. Trả salutations, genders (query đúng
    doctype Link), designations, departments, customers, territories, countries.
  - `create_contact_standalone(data)` — POST. Tạo Contact chuẩn ERPNext, set
    email/phone primary, link Customer (nếu có), tạo Address liên kết.

## Data model

- Contact/Address dùng field CHUẨN ERPNext (không thêm Custom Field mới).
- Các trường MISA chưa có chỗ lưu (Zalo, Email cá nhân, Nguồn gốc, Phân loại
  KH, Không gọi điện/Email, Điện thoại khác) hiển thị đúng UI nhưng chưa
  persist — chờ duyệt Custom Field nếu cần lưu.

## Verification

- `bench build --app dcnet_crm` OK (bundle ~771.6 kb).
- `get_contact_create_options()` trả đủ options (salutations 9, genders 7,
  designations 58, departments 30, customers 343, territories 5, countries 250).
- `create_contact_standalone(...)` tạo Contact thật trong transaction → link
  Customer + Address đúng → `frappe.db.rollback()`.

## Known Limitations

- Chưa có chế độ sửa liên hệ nội bộ; mở liên hệ cũ vẫn dùng panel hiện có.
- Các trường MISA ngoài chuẩn ERPNext chưa được lưu (xem mục Data model).

---

## Cập nhật: Trang chi tiết Liên hệ (contact-detail) — 2026-06-17

### Tổng quan

Click một liên hệ trong danh sách mở trang chi tiết `?view=contact-detail&contact={name}`
ngay trong `dcnet-crm` (không dùng Frappe form). Layout giống y form Thêm Liên hệ
nhưng ở chế độ xem; nút "Sửa" bật chế độ chỉnh sửa trực tiếp.

### Implementation

- `frontend/src/features/contacts/template-detail.js` — markup detail/edit
  (readonly khi xem, input/select khi sửa; cascade VN 2025 cho địa chỉ).
- `frontend/src/features/contacts/composable-create.js` — bổ sung state
  (`contactDetail`, `contactDetailEditing`, `cdForm`, `cdBillingForm`...),
  `loadContactDetail`, `openContactDetail`, `startContactEdit`,
  `cancelContactEdit`, `saveContactDetail`, `backToContacts`, cascade watchers
  + `_matchProvince`/`_matchWard` để tự restore dropdown từ text.
- `frontend/src/app.js` — import `contactDetailTemplate`, thêm route
  `contact-detail` vào valid keys/syncRouteUrl/syncNativeSidebarActive/watch,
  `openDocument` cho `contacts` gọi `openContactDetail`.
- `dcnet_crm/api.py` — `get_contact_detail(name)` GET + `update_contact_standalone(name, data)` POST.

### Verification

- Build OK (~787.7 kb), đã clear cache.
- `get_contact_detail` trả đúng trường + customer link + billing address + `can_write`.
- `update_contact_standalone` lưu Contact, đồng bộ Customer link + Address.
- Cả hai đã rollback trong test — không để lại dữ liệu rác.

### Known Limitations

- Các trường UI-only (Zalo, email cá nhân, nguồn gốc...) hiển thị "—" khi xem,
  chưa persist (chờ duyệt Custom Field).
- Chưa có tab Hoạt động / Mua hàng trong trang chi tiết (chỉ là thông tin hồ sơ).
