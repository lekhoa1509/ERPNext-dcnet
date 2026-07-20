# Phân công khách hàng (Customer Assignment) — Design Plan

> Ngày: 2026-06-25
> Nguồn: `dcnet-crm/HANDOFF.md` §12 "Phân công khách hàng (Customer Assignment) — design note (2026-06-20)", Option 2
> Trạng thái: DRAFT — chờ confirm placement + business rules

## 1. Mục tiêu

Cho phép **Sales Manager** tự gán/bỏ gán khách hàng cho từng nhân viên sales **mà không cần IT**.
Hiện tại chỉ System Manager / IT mới cấu hình được `User Permission` qua Setup → User Permissions.

Kết quả: danh sách Customer của sales user bị giới hạn theo dòng (row-level) về đúng các KH được giao.

## 2. Cơ chế nền (đã xác nhận trong codebase)

- Cơ chế giới hạn dùng **`User Permission`** với `allow="Customer"`, `for_value={Customer.name}`, `user={sales email}`.
- ERPNext tự động lọc list/report theo User Permission khi user không có quyền bỏ qua.
- `dcnet-permission` đã quản lý `User Permission` (hiện cho `allow="Department"`) — ta thêm nhánh `allow="Customer"`.
- Đây là **dữ liệu hạn chế bổ sung**, không phải role permission (Custom DocPerm) — độc lập với tab phân quyền hiện có.

## 3. Placement — KHUYẾN NGHỊ

**Đặt trong app `dcnet-permission`** (không build CRM Vue view mới).

Lý do:
- App này đã sở hữu toàn bộ logic CRUD `User Permission` + helper `normalize_email`, audit comment, `frappe.clear_cache(user=...)`.
- Đã có design system teal (`dcnet_permission_manager.css`) + framework Frappe Page + JS.
- Tránh duplicate logic ghi `User Permission` sang CRM và tránh rebuild bundle Vue.

**Hình thức:** Trang Frappe Page **mới riêng** `dcnet-customer-assignment` (KHÔNG nhồi vào page permission manager hiện tại), để access control tách bạch:
- Page permission manager hiện tại: roles `DCNET Permission Admin/Manager`, `System Manager` (IT).
- Page customer assignment: roles `System Manager`, `Sales Master Manager`, `Sales Manager` (nghiệp vụ bán hàng).

> ⚠️ Cần confirm khách: đặt ở đâu — `dcnet-permission` (khuyến nghị) hay CRM `?view=customer-assignment`?
> Nếu khách muốn sales mở ngay trong CRM, có thể thêm sidebar link CRM trỏ sang Page này (cùng tab).

## 4. Backend (`dcnet_permission`)

File mới: `dcnet_permission/customer_assignment.py` (logic) + thêm endpoint vào `api.py`.

### Access guard
```python
CUSTOMER_ASSIGNMENT_ROLES = {"System Manager", "Sales Master Manager", "Sales Manager"}

def assert_customer_assignment_access(user=None):
    roles = set(frappe.get_roles(user or frappe.session.user))
    if not (roles & CUSTOMER_ASSIGNMENT_ROLES):
        frappe.throw(_("Bạn không có quyền phân công khách hàng."), frappe.PermissionError)
```

### Endpoints (`api.py`, whitelisted)
| Method | Mô tả |
|--------|-------|
| `list_sales_users()` | GET. DS user có role `Sales User`/`Sales Manager` (enabled) để chọn từ dropdown. |
| `get_user_customer_assignments(user)` | GET. Trả `{ assigned: [Customer.name...], customers: [{name, customer_name, customer_group, territory}] }` — full list + đánh dấu đã gán. |
| `set_user_customer_assignments(user, customers)` | POST. Diff old/new → xóa `User Permission` bị bỏ, insert cái mới. Trả counts. |

### Logic `set_user_customer_assignments`
1. `assert_customer_assignment_access()`; chặn user tự sửa chính mình; `normalize_email(user)`.
2. Load hiện tại: `frappe.get_all("User Permission", filters={"user": user, "allow": "Customer"}, fields=["name","for_value"])`.
3. `to_add = new - existing`, `to_remove = existing - new`.
4. Xóa: `frappe.delete_doc("User Permission", name, force=True, ignore_permissions=True)` cho `to_remove`.
5. Thêm: `new_doc("User Permission")` với `user`, `allow="Customer"`, `for_value=cust`, `apply_to_all_doctypes=1` (giới hạn mọi doctype tham chiếu Customer) → `insert(ignore_permissions=True)`.
6. `frappe.clear_cache(user=user)`; ghi audit comment (tái dùng pattern `add_audit_comment` nếu phù hợp).
7. Validate mỗi `cust` tồn tại trong Customer trước khi insert (chặn injection).

> Quyết định cần confirm: `apply_to_all_doctypes=1` (giới hạn cả SO/SI/Quotation theo KH) HAY chỉ `allow_doctype="Customer"`? → Khuyến nghị `apply_to_all_doctypes=1` để sales chỉ thấy giao dịch của KH mình.

## 5. Frontend

- Page mới `dcnet-customer-assignment` (json + `__init__.py` + js + tái dùng css teal).
- UI:
  1. Dropdown chọn **nhân viên sales** (từ `list_sales_users`).
  2. Sau khi chọn → load `get_user_customer_assignments` → bảng checklist tất cả Customer; KH đã gán có ✓ sẵn.
  3. Search box lọc theo tên/mã KH; (tùy chọn) lọc theo Customer Group / Territory.
  4. Chọn/bỏ chọn → nút **Lưu** gọi `set_user_customer_assignments`.
  5. Nút "Chọn tất cả" / "Bỏ chọn tất cả" theo kết quả lọc hiện tại.
- Tái dùng class CSS card/teal hiện có; thêm prefix riêng `dca-*` cho phần mới.

## 6. Install / hooks

- Đăng ký page (Frappe tự nhận qua thư mục `page/`).
- Nếu cần role `Sales Manager` thấy được desktop icon → cập nhật `desktop.py` / workspace sidebar (theo pattern hiện có), chỉ trong `dcnet-permission`.
- Không tạo DocType mới — chỉ dùng `User Permission` chuẩn.

## 7. Verify

- Tạo 1 sales user test, gán 2 KH → đăng nhập user đó → list Customer chỉ thấy 2 KH (chạy trong container, rollback hoặc cleanup User Permission sau test).
- Bỏ gán 1 KH → list còn 1.
- Kiểm tra Sales Manager truy cập được page; Sales User thường KHÔNG mở được page.
- Test trong `devcontainer-frappe-1`, `bench --site flow.local clear-cache`.

## 8. Open questions (confirm khách / nội bộ)

1. :orange_circle: Placement: `dcnet-permission` (khuyến nghị) hay CRM view?
2. :orange_circle: `apply_to_all_doctypes=1` (giới hạn cả giao dịch) hay chỉ Customer doctype?
3. :yellow_circle: Có cần phân công theo **nhóm** (Customer Group / Territory) hàng loạt, hay chỉ từng KH?
4. :yellow_circle: Khi sales nghỉ việc / reassign — có cần "chuyển toàn bộ KH từ user A sang user B" không?
5. :yellow_circle: Quan hệ với ERPNext "Sales Team" (Sales Person + commission) — có đồng bộ hay độc lập?

## 9. Scope / Non-goals

- KHÔNG động vào `dcnet_apps` hay ERPNext core.
- KHÔNG tạo DocType mới.
- Bước 1 chỉ làm gán theo từng Customer; gán hàng loạt theo group là phase sau (nếu khách cần).
