# Workspace Sidebar Persistence

> Giữ sidebar workspace khi user F5 hoặc mở link trực tiếp. Hỗ trợ nhiều custom workspace cùng share DocType/Report/Page.

## Bối cảnh

Frappe v16 cho phép nhiều workspace sidebar cùng chứa link đến 1 entity (vd: "Sales Invoice" có trong cả "Invoicing" lẫn "Ke Toan VN"). Khi user navigate trong sidebar thì sidebar giữ nguyên, nhưng khi F5 thì Frappe chọn lại sidebar từ đầu.

### Root Causes

1. **App filter loại custom sidebar:** `filter_sidebars_from_app()` (sidebar.js:679) chỉ giữ sidebar có `sidebar.app === entity's module app`. Sales Invoice thuộc module Accounts (app=erpnext), nên "Ke Toan VN" (app=vn_accounting) bị loại.

2. **Không nhớ context:** Khi F5, `this.sidebar_title` là null (fresh page load), không có cơ chế nhớ sidebar nào user đang dùng.

## Giải pháp: 3-Tier Selection

Monkey-patch `set_workspace_sidebar()` trên `frappe.ui.Sidebar.prototype`, chèn 2 tầng kiểm tra TRƯỚC logic gốc của Frappe:

```
┌─────────────────────────────────────────────────┐
│  Route Change / Page Load                       │
│  entity_name = parse(route)                     │
│  candidates = get_workspace_sidebars(entity)    │
├─────────────────────────────────────────────────┤
│  Current sidebar in candidates? → keep it       │  (same as Frappe)
├─────────────────────────────────────────────────┤
│  TIER 1: localStorage                           │  ← NEW
│  Key: workspace_sidebar_preferences             │
│  Lưu sidebar cuối cùng user chọn cho mỗi entity│
│  Match? → dùng, return                          │
├─────────────────────────────────────────────────┤
│  TIER 2: frappe.boot.workspace_defaults         │  ← NEW
│  Auto-generated từ Workspace Sidebar JSON       │
│  Sort by priority desc, first match → dùng      │
├─────────────────────────────────────────────────┤
│  TIER 3: Original Frappe logic                  │  (fallback)
│  filter_sidebars_from_app → module fallback     │
└─────────────────────────────────────────────────┘
```

### Tier 1: localStorage (user preference)

- **Key:** `workspace_sidebar_preferences`
- **Format:** `{ "Sales Invoice": "Ke Toan VN", "General Ledger": "Ke Toan VN", ... }`
- **Lưu khi:** sidebar được chọn (bất kể tier nào chọn)
- **Ưu tiên:** Cao nhất — user's explicit choice always wins

### Tier 2: Boot Defaults (configurable)

- **Source:** `frappe.boot.workspace_defaults` — inject qua `boot_session` hook
- **Format:**
  ```json
  {
    "Sales Invoice": [{"sidebar": "Ke Toan VN", "priority": 10}],
    "Quotation": [
      {"sidebar": "Ke Toan VN", "priority": 10},
      {"sidebar": "Trung Tam Phe Duyet", "priority": 20}
    ]
  }
  ```
- **Priority convention:**
  - `10` = general workspace (Ke Toan VN — bao quát)
  - `20` = specialized workspace (Trung Tam Phe Duyet — chuyên biệt)
  - Số cao hơn thắng khi conflict
- **Auto-generated:** Đọc từ Workspace Sidebar items trong DB, không hardcode per-DocType

### Tier 3: Frappe Default

Logic gốc: `filter_sidebars_from_app()` → `get_workspace_for_module()` → `show_sidebar_for_module()`. Custom sidebar thường bị loại ở đây vì khác app.

## Files

| File | Vai trò |
|------|---------|
| `vn_accounting/boot.py` | `boot_session()` — đọc sidebar items → build defaults map |
| `vn_accounting/hooks.py` | `boot_session` hook registration |
| `vn_accounting/public/js/sidebar_route_options.bundle.js` | 3rd IIFE — monkey-patch `set_workspace_sidebar()` |

## Thêm workspace mới

Khi tạo workspace mới (vd: "Trung Tâm Phê Duyệt"), chỉ cần thêm 1 entry vào `WORKSPACE_SIDEBARS` trong `boot.py`:

```python
WORKSPACE_SIDEBARS = [
    {"sidebar": "Ke Toan VN", "priority": 10},
    {"sidebar": "Trung Tam Phe Duyet", "priority": 20},  # thêm dòng này
]
```

Sau đó: `bench --site <site> clear-cache`. Không cần sửa JS.

## Porting sang app/project khác

Nếu muốn áp dụng pattern này trong một custom app khác (không phải vn_accounting), cần 3 thứ:

### 1. `<your_app>/boot.py`

```python
import frappe

WORKSPACE_SIDEBARS = [
    {"sidebar": "My Custom Sidebar", "priority": 10},
]

def boot_session(bootinfo):
    defaults = {}
    for ws in WORKSPACE_SIDEBARS:
        sidebar_name = ws["sidebar"]
        priority = ws["priority"]
        try:
            sidebar_doc = frappe.get_doc("Workspace Sidebar", sidebar_name)
        except frappe.DoesNotExistError:
            continue
        for item in sidebar_doc.items:
            if item.type == "Link" and item.link_to:
                defaults.setdefault(item.link_to, [])
                defaults[item.link_to].append({
                    "sidebar": sidebar_name,
                    "priority": priority,
                })
    bootinfo["workspace_defaults"] = defaults
```

### 2. `hooks.py`

```python
# Nếu chưa có boot_session hook:
boot_session = "<your_app>.boot.boot_session"

# Nếu đã có boot_session hook khác → dùng list:
boot_session = [
    "<your_app>.boot.existing_boot",
    "<your_app>.boot.boot_session",
]
```

### 3. JS bundle

Copy IIFE thứ 3 từ `vn_accounting/public/js/sidebar_route_options.bundle.js` vào bundle JS của app bạn. Đổi tên app trong log:

```js
console.warn("[your_app] frappe.ui.Sidebar not found, sidebar persistence skipped");
```

Đăng ký bundle trong `hooks.py`:
```python
app_include_js = ["your_app.bundle.js"]
```

Sau đó: `bench build --app <your_app> && bench --site <site> clear-cache`.

> **Lưu ý:** Workspace Sidebar phải tồn tại trong DB (không chỉ JSON file). `boot.py` đọc từ DB — nếu chưa install workspace thì `DoesNotExistError` được catch, Tier 2 sẽ rỗng, hệ thống vẫn hoạt động qua Tier 1 + Tier 3.

## Timing & Performance

- **Không dùng setInterval/polling.** Patch prototype ngay lập tức khi bundle JS chạy.
- **Thứ tự load:** `desk.bundle.js` (define Sidebar) → `app_include_js` (our patch) → router "change" event (async, sau boot data). Patch luôn sẵn sàng trước lần gọi đầu tiên.
- **Không jank/flash:** Sidebar đúng hiển thị ngay từ đầu, không có hiện tượng chuyển sidebar.

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| F5 sau khi dùng Ke Toan VN | localStorage → Ke Toan VN |
| F5 sau khi dùng Invoicing | localStorage → Invoicing |
| Lần đầu mở link (chưa có history) | Boot defaults → Ke Toan VN |
| DocType không trong workspace nào custom | Tier 3 → Frappe default |
| Workspace bị xóa/đổi tên | localStorage trả tên cũ → không match candidates → skip → Tier 2/3 |
| 2 tab cùng DocType, khác workspace | localStorage shared → last-write wins (acceptable) |
| localStorage bị disable/full | try/catch → skip → Tier 2/3 |
