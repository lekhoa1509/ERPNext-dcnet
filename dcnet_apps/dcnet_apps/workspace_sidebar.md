# DCNET Workspace Sidebar Customization

Custom workspace sidebars cho DCNET Flow. Files JSON trong `workspace_sidebar/` sẽ **override** ERPNext defaults khi chạy `bench migrate`.

## Cách hoạt động

Frappe tự động sync files JSON trong `workspace_sidebar/` của mỗi app theo thứ tự:
1. `frappe` (base)
2. `erpnext` (dcnet_core)
3. `dcnet_apps` (custom - **wins**)

File cùng tên sẽ override hoàn toàn file trước đó.

## Cách thêm/sửa sidebar

### 1. Copy file từ ERPNext
```bash
cp dcnet_core/erpnext/workspace_sidebar/{name}.json dcnet_apps/dcnet_apps/workspace_sidebar/
```

### 2. Sửa `"app"` field
```json
{
  "app": "dcnet_apps",  // Đổi từ "erpnext"
  ...
}
```

### 3. Edit items theo ý muốn

### 4. Commit và migrate
```bash
git add dcnet_apps/dcnet_apps/workspace_sidebar/
git commit -m "feat: customize {name} workspace sidebar"
bench --site flow.local migrate
```

## Cấu trúc item

```json
{
  "label": "Tên hiển thị",
  "type": "Link",              // Link | Section Break
  "link_type": "DocType",      // DocType | Report | Workspace | Dashboard | URL
  "link_to": "Purchase Order", // DocType name (nếu link_type != URL)
  "url": "/app/path/new",      // URL path (nếu link_type == URL)
  "icon": "plus",              // Lucide icon name
  "child": 0,                  // 1 = nested under Section Break
  "indent": 0,                 // 1 = Section Break header
  "collapsible": 0,
  "keep_closed": 0,
  "show_arrow": 0
}
```

## Files hiện có

| File | Mô tả |
|------|-------|
| `buying.json` | Mua hàng - thêm "Tạo PO mới" quick link |

## Lưu ý

- **KHÔNG đặt file không phải JSON** trong folder `workspace_sidebar/` (Frappe sẽ parse error)
- File JSON override **toàn bộ** sidebar, không merge
- Luôn copy từ ERPNext source, không tạo từ đầu
- Sau migrate, reload browser để thấy thay đổi
