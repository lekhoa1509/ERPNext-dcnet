# Disable Unused Modules (Manufacturing, Education, etc.)

**Date:** 30/01/2026
**Category:** System Configuration
**Status:** Active

---

## Overview

Disable các modules không sử dụng trong dự án DCNET Flow (Golf shop) để:
- Ẩn các buttons không cần thiết (vd: "Work Order" trong Sales Order)
- Ẩn dashboard links đến modules không dùng
- Giảm complexity cho end users
- Đồng bộ cấu hình cho cả team dev

## Modules Configuration

### ENABLED (Whitelist)

| Domain | Modules/Features |
|--------|------------------|
| **Distribution** | Selling, Buying, Stock, Warehouse |
| **Services** | CRM, basic services |
| **Retail** | POS |

### DISABLED

| Domain | Hidden Features |
|--------|-----------------|
| **Manufacturing** | Work Order, BOM, Production Planning, Job Card |
| **Education** | Student, Course, Fee, Program |
| **Healthcare** | Patient, Practitioner, Medical Record |
| **Agriculture** | Crop, Land Unit, Weather |
| **Non Profit** | Donor, Volunteer, Chapter |

## Implementation

### Code Location

```
dcnet_apps/dcnet_apps/install.py
└── setup_active_domains()  # Called on after_migrate
```

### How It Works

1. **Domain Settings** - ERPNext built-in mechanism để enable/disable features
2. **after_migrate hook** - Tự động apply khi `bench migrate`
3. **Whitelist approach** - Chỉ enable domains cần thiết

### What Gets Hidden

Khi disable domain "Manufacturing":

**Sales Order form:**
- ❌ Button "Work Order" trong menu "Create"
- ❌ Dashboard link "Manufacturing" (Work Order, BOM)

**Item form:**
- ❌ Section "Manufacturing"
- ❌ Fields: default_bom, is_sub_contracted_item

**Purchase Order form:**
- ❌ Subcontracting features

## Team Sync

```bash
# Sau khi pull code mới
git pull
bench --site flow.local migrate

# Kết quả:
# ✅ Enabled domains: Distribution, Services, Retail
# ✅ Disabled domains: Manufacturing
# ✅ Domain Settings configured - Manufacturing features hidden
```

## Manual Override

Nếu cần enable lại Manufacturing cho testing:

```python
# bench --site flow.local console
import frappe
ds = frappe.get_doc("Domain Settings", "Domain Settings")
ds.append("active_domains", {"domain": "Manufacturing"})
ds.save()
frappe.db.commit()
```

**Note:** Thay đổi thủ công sẽ bị reset khi chạy `bench migrate` tiếp theo.

## Verification

### Check Active Domains

```python
# bench --site flow.local console
import frappe
print(frappe.get_active_domains())
# Expected: ['Distribution', 'Services', 'Retail', '']
```

### Check Sales Order Form

1. Mở Sales Order đã submit
2. Click menu "Create"
3. Confirm **KHÔNG** thấy "Work Order"

### Check Dashboard

1. Mở Sales Order
2. Scroll xuống Dashboard section
3. Confirm **KHÔNG** thấy section "Manufacturing"

## Troubleshooting

### Features vẫn hiện sau migrate

```bash
# Clear cache
bench --site flow.local clear-cache

# Rebuild assets
bench build --app dcnet_apps

# Restart
bench restart
```

### Muốn thêm domain mới

Edit `setup_active_domains()` trong `install.py`:

```python
enabled_domains = [
    "Distribution",
    "Services",
    "Retail",
    "New Domain",  # Thêm vào đây
]
```

## Related Files

- `dcnet_apps/dcnet_apps/install.py` - Main implementation
- `dcnet_apps/dcnet_apps/hooks.py` - Hook registration (after_migrate)
- `docs/customization/ui/2026-01-29-desktop-icons.md` - Desktop icons customization

## References

- [Frappe Domain Settings](https://frappeframework.com/docs/user/en/basics/domains)
- [ERPNext Domain Configuration](https://docs.erpnext.com/docs/user/manual/en/setting-up/domain-settings)
