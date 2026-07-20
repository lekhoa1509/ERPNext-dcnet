# Hướng dẫn Custom Menu Dropdown (Context Menu)

Tài liệu này hướng dẫn cách can thiệp vào các menu dropdown có class `.frappe-menu.context-menu` trong Frappe thông qua app `dcnet_apps`.

## 1. Cơ chế hoạt động
Chúng ta sử dụng kỹ thuật **Monkey-patching** để ghi đè hàm `add_menu_item` của class `frappe.ui.menu`. 
- File can thiệp: `dcnet_apps/public/js/menu_override.js`
- Cơ chế: Kiểm tra nhãn (label) của từng item trước khi nó được thêm vào giao diện. Nếu nhãn nằm trong danh sách cần ẩn, item đó sẽ bị chặn.

## 2. Các bước cài đặt & Cập nhật

### Bước 1: Khai báo trong Hooks
Đảm bảo file JS đã được khai báo trong `dcnet_apps/dcnet_apps/hooks.py`:

```python
app_include_js = [
    f"/assets/dcnet_apps/js/menu_override.js?v={develop_version}",
]
```

### Bước 2: Tùy chỉnh danh sách item cần ẩn
Mở file `dcnet_apps/dcnet_apps/public/js/menu_override.js` và chỉnh sửa mảng `labels_to_hide`:

```javascript
const labels_to_hide = [
    "Documentation",
    "User Manual",
    "Frappe Support",
    // Thêm các nhãn khác tại đây
];
```

### Bước 3: Chạy lệnh cập nhật hệ thống
Sau khi thay đổi code, bạn cần chạy các lệnh sau trong terminal của `frappe-bench`:

1. **Build lại assets (JS/CSS):**
   ```bash
   bench build --app dcnet_apps
   ```
   *Lưu ý: Nếu gặp lỗi TypeError liên quan đến esbuild, hãy đảm bảo cấu trúc thư mục public đúng chuẩn hoặc thử chạy `bench build` cho toàn bộ apps.*

2. **Đồng bộ hóa cấu hình (Migrate):**
   Mặc dù thay đổi chủ yếu ở JS, chạy migrate giúp đồng bộ các thiết lập app:
   ```bash
   bench --site <site_name> migrate
   ```

3. **Xóa cache:**
   ```bash
   bench clear-cache
   ```

### Bước 4: Kiểm tra trên trình duyệt
- Nhấn `Ctrl + F5` (hoặc `Cmd + Shift + R` trên Mac) để xóa cache trình duyệt và tải lại file JS mới nhất.
- Kiểm tra các menu dropdown (ví dụ menu ở Sidebar hoặc menu chuột phải) để xác nhận các item đã bị ẩn.

## 3. Lưu ý quan trọng
- **Dịch thuật:** Nếu hệ thống sử dụng đa ngôn ngữ, hãy đảm bảo nhãn trong `labels_to_hide` khớp với nhãn đã được dịch hiển thị trên giao diện (hoặc kiểm tra logic so sánh trong script).
