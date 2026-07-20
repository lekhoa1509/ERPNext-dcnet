# Branding Logo Customization

**Date:** 2026-01-16
**Type:** UI Customization - Branding
**Status:** ✅ Completed
**Author:** DCNET Cloud Team

---

## 📋 Overview

Custom branding cho DCNET Flow application với logo DCNET TELECOM và favicon paper plane.

## 🎯 Requirements

- **Navbar Logo:** DCNET TELECOM logo (tam giác vàng gradient + text)
- **Favicon:** Paper plane vàng (32×32px)
- **Splash Screen:** DCNET TELECOM logo khi loading/chuyển trang
- **Maintainability:** Chỉ cần thay file PNG, không cần rebuild hoặc update DB

## 🛠️ Implementation

### Files Changed

```
dcnet_apps/dcnet_apps/
├── boot.py                      # 🆕 Boot session hook
├── hooks.py                     # ✏️ Modified (boot_session, after_migrate hook)
├── install.py                   # 🆕 Install/Migrate hooks for Navbar Settings
└── public/images/
    ├── dcnet-logo.png           # 🆕 Main logo (160×52px, 4.6KB)
    └── favicon.png              # 🆕 Favicon (32×32px, 2.5KB)
```

### 1. Boot Session Hook

**File:** `dcnet_apps/boot.py`

```python
def boot_session(bootinfo):
    """Override Frappe boot session to customize branding."""

    # Override navbar logo (app_data[0] = Frappe app)
    if bootinfo.get("app_data"):
        for app in bootinfo["app_data"]:
            if app.get("app_name") == "frappe":
                app["app_logo_url"] = "/assets/dcnet_apps/images/dcnet-logo.png"
                break

    # Override app name
    if not bootinfo.get("app_name"):
        bootinfo["app_name"] = "DCNET Flow"
```

**Purpose:** Override navbar logo từ Python (không cần JS, không cache)

### 2. Hooks Configuration

**File:** `dcnet_apps/hooks.py`

```python
# Boot session hook
boot_session = "dcnet_apps.boot.boot_session"

# App logo (fallback)
app_logo_url = "/assets/dcnet_apps/images/dcnet-logo.png"

# Website branding
website_context = {
    "favicon": "/assets/dcnet_apps/images/favicon.png",
    "splash_image": "/assets/dcnet_apps/images/dcnet-logo.png"
}
```

### 3. Install/Migrate Hooks

**File:** `dcnet_apps/install.py`

```python
def after_migrate():
    """Auto-apply branding after bench --site flow.local migrate."""
    setup_branding()

def setup_branding():
    """Update Navbar Settings and Website Settings."""
    # Update Navbar Settings
    navbar = frappe.get_doc("Navbar Settings")
    navbar.app_logo = "/assets/dcnet_apps/images/dcnet-logo.png"
    navbar.save(ignore_permissions=True)

    # Update Website Settings
    frappe.db.set_value("Website Settings", "Website Settings", {
        "app_logo": "/assets/dcnet_apps/images/dcnet-logo.png",
        "favicon": "/assets/dcnet_apps/images/favicon.png"
    })

    # Clear cache
    frappe.cache().delete_keys("bootinfo*")
    frappe.clear_cache()
```

**Registered in hooks.py:**
```python
after_install = "dcnet_apps.install.after_install"
after_migrate = "dcnet_apps.install.after_migrate"
```

**Purpose:** Auto-update branding khi team chạy `bench --site flow.local migrate` → No manual steps needed!

## 📍 Logo Locations

| Location | File | Size | Description |
|----------|------|------|-------------|
| Navbar (top-left) | `dcnet-logo.png` | 160×52px | DCNET TELECOM logo |
| Splash Screen | `dcnet-logo.png` | 160×52px | Loading screen |
| Browser Favicon | `favicon.png` | 32×32px | Paper plane icon |

## 🎨 Assets

**Source Files:**
- Navbar Logo: `photo_2026-01-16_15-22-57.jpg` → converted to PNG, cropped & resized
- Favicon: `photo_2026-01-16_15-28-35.jpg` → converted to PNG

**Output:**
- `dcnet-logo.png`: 4.6KB, 160×52px (JPEG → PNG, cropped, resized)
- `favicon.png`: 2.5KB, 32×32px (JPEG → PNG)

## 🔧 Technical Notes

### Why Boot Session Hook?

**Problem:** Frappe sidebar logo lấy từ `frappe.boot.app_data[0].app_logo_url` (app đầu tiên = Frappe)

**Solution:** Override bootinfo từ Python hook, không cần:
- ❌ Custom JS (browser cache issues)
- ❌ Build assets (chỉ có static images)
- ❌ Update DB thủ công mỗi lần đổi logo

**Benefits:**
- ✅ Clean architecture (theo Frappe pattern)
- ✅ Auto apply cho tất cả users
- ✅ Sync qua git
- ✅ Easy maintenance

### Frappe Branding Layers

Frappe có 4 tầng config cho branding:

| Layer | Priority | Source | Use Case |
|-------|----------|--------|----------|
| **Navbar Settings** | Highest | Database | Navbar logo (overrides bootinfo) |
| **Boot Session** | High | Python hook | Override app_data logo |
| **Website Settings** | Medium | Database | Favicon, fallback logo |
| **hooks.py** | Lowest | Code | Default values |

**Why all 4 layers?**
- **Navbar Settings:** Frappe checks this first for navbar logo
- **Boot Session:** Ensures bootinfo has correct logo for sidebar
- **Website Settings:** Favicon and splash screen
- **after_migrate hook:** Auto-sync team members after git pull

**Implementation:** Dùng cả 4 layers + auto-migration để ensure consistency.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRAPPE BRANDING SYSTEM                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: CODE (Git-tracked)                                     │
├─────────────────────────────────────────────────────────────────┤
│ hooks.py                                                         │
│   ├── app_logo_url = "/assets/dcnet_apps/images/dcnet-logo.png"│
│   ├── boot_session = "dcnet_apps.boot.boot_session"            │
│   ├── after_install = "dcnet_apps.install.after_install"       │
│   └── after_migrate = "dcnet_apps.install.after_migrate"       │
│                                                                  │
│ boot.py                                                          │
│   └── boot_session(bootinfo)                                    │
│       └── Override app_data[0].app_logo_url                     │
│                                                                  │
│ install.py                                                       │
│   ├── after_install() → setup_branding()                       │
│   └── after_migrate() → setup_branding()                       │
│       ├── Update Navbar Settings                                │
│       ├── Update Website Settings                               │
│       └── Clear cache                                            │
│                                                                  │
│ public/images/                                                   │
│   ├── dcnet-logo.png                                            │
│   └── favicon.png                                               │
└─────────────────────────────────────────────────────────────────┘
                            ↓ (bench --site flow.local migrate)
┌─────────────────────────────────────────────────────────────────┐
│ Layer 2: DATABASE (Per-site, NOT git-tracked)                  │
├─────────────────────────────────────────────────────────────────┤
│ DocType: Navbar Settings                                        │
│   └── app_logo = "/assets/dcnet_apps/images/dcnet-logo.png"    │
│                                                                  │
│ DocType: Website Settings                                       │
│   ├── app_logo = "/assets/dcnet_apps/images/dcnet-logo.png"    │
│   └── favicon = "/assets/dcnet_apps/images/favicon.png"        │
└─────────────────────────────────────────────────────────────────┘
                            ↓ (on page load)
┌─────────────────────────────────────────────────────────────────┐
│ Layer 3: RUNTIME (Session cache)                               │
├─────────────────────────────────────────────────────────────────┤
│ frappe.boot.get_bootinfo()                                      │
│   ├── app_data[0].app_logo_url (from boot_session hook)        │
│   └── Cached in Redis (key: "bootinfo:user")                   │
└─────────────────────────────────────────────────────────────────┘
                            ↓ (rendered to browser)
┌─────────────────────────────────────────────────────────────────┐
│ Layer 4: FRONTEND (Browser DOM)                                │
├─────────────────────────────────────────────────────────────────┤
│ Navbar Component                                                │
│   └── <img src="/assets/dcnet_apps/images/dcnet-logo.png">     │
│                                                                  │
│ Favicon                                                          │
│   └── <link rel="icon" href="/assets/.../favicon.png">         │
└─────────────────────────────────────────────────────────────────┘
```

### Hooks Execution Flow

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Event: bench --site flow.local migrate (sau khi git pull)                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    ↓
    1. Run pending patches
    ↓
    2. Update schema (DocType changes)
    ↓
    3. ✅ RUN: after_migrate hook (for EACH installed app)
       └── dcnet_apps.install.after_migrate()
           └── setup_branding()
               ├── Update Navbar Settings (DB)
               ├── Update Website Settings (DB)
               └── Clear cache (Redis)
    ↓
    4. Done ✅

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Event: User login / Page load                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    ↓
    1. frappe.boot.get_bootinfo()
    ↓
    2. ✅ RUN: boot_session hook
       └── dcnet_apps.boot.boot_session(bootinfo)
           └── Override app_data[0].app_logo_url
    ↓
    3. Cache bootinfo in Redis
    ↓
    4. Send to browser → Render logo
```

### Team Sync Process

**Khi có thay đổi branding (logo/favicon):**

```
Developer A (làm thay đổi):
  1. Update logo files (dcnet-logo.png, favicon.png)
  2. Commit + push code
     └── git push origin main

Developer B, C, D (pull code):
  1. git pull origin main
  2. bench --site flow.local migrate
     └── ✅ after_migrate hook tự động chạy
         ├── Navbar Settings updated
         ├── Website Settings updated
         └── Cache cleared
  3. bench restart
  4. Logout → Login lại browser
  5. ✅ Logo mới hiển thị (đồng bộ với team)
```

**Key Point:** Database settings (Navbar/Website Settings) không nằm trong Git → Dùng `after_migrate` hook để sync từ code → DB.

## 🚀 Deployment

### 1. Commit Changes

```bash
git add dcnet_apps/dcnet_apps/boot.py
git add dcnet_apps/dcnet_apps/hooks.py
git add dcnet_apps/dcnet_apps/public/images/
git commit -m "feat(branding): add DCNET TELECOM logo customization"
```

### 2. Team Sync

**Khi team members pull code:**

```bash
# Pull code
git pull origin main

# Migrate (auto run after_migrate hook)
bench --site flow.local migrate

# Restart
bench restart

# Logout → Login lại browser
```

**Auto-applied by hook:**
- ✅ Navbar Settings updated
- ✅ Website Settings updated
- ✅ Cache cleared

**Không cần:**
- ❌ Run bench build (không có JS/CSS bundle)
- ❌ Update DB manually (đã auto qua after_migrate hook)
- ❌ Install dependencies

### 3. Production Deployment

```bash
# Pull code
git pull origin main

# Clear cache
bench --site production.site clear-cache
bench --site production.site clear-website-cache

# Restart
bench restart

# Verify
curl -I https://production.site/assets/dcnet_apps/images/dcnet-logo.png
curl -I https://production.site/assets/dcnet_apps/images/favicon.png
```

## 🔄 Future Updates

**To update logo:**

1. Replace PNG files:
   ```bash
   dcnet_apps/dcnet_apps/public/images/dcnet-logo.png
   dcnet_apps/dcnet_apps/public/images/favicon.png
   ```

2. Clear cache:
   ```bash
   bench clear-cache && bench restart
   ```

3. Hard reload browser (Cmd+Shift+R)

**No need to:**
- ❌ Update code (hooks.py, boot.py)
- ❌ Update database
- ❌ Rebuild assets

## 📚 References

- [Frappe Hooks - boot_session](https://docs.frappe.io/framework/user/en/python-api/hooks#boot_session)
- [Frappe Boot Process](https://github.com/frappe/frappe/blob/develop/frappe/boot.py)
- [Website Settings](https://docs.frappe.io/erpnext/user/manual/en/website-settings)

## 🐛 Troubleshooting

### Logo không hiển thị ở navbar?

```bash
# 1. Check Navbar Settings (highest priority)
bench --site flow.local console
>>> import frappe
>>> navbar = frappe.get_doc('Navbar Settings')
>>> navbar.app_logo
# Should return: '/assets/dcnet_apps/images/dcnet-logo.png'

# 2. If empty, run setup_branding
>>> from dcnet_apps.install import setup_branding
>>> setup_branding()

# 3. Verify bootinfo
>>> from frappe.boot import get_bootinfo
>>> boot = get_bootinfo()
>>> [a for a in boot['app_data'] if a['app_name']=='frappe'][0]['app_logo_url']
# Should return: '/assets/dcnet_apps/images/dcnet-logo.png'

# 4. Restart bench
bench restart

# 5. Logout → Login lại browser
```

### Favicon không đổi?

```bash
# 1. Clear browser cache completely
# Chrome: Settings → Privacy → Clear browsing data

# 2. Check Website Settings
bench --site flow.local console
>>> frappe.db.get_value('Website Settings', None, 'favicon')
# Should return: '/assets/dcnet_apps/images/favicon.png'

# 3. Hard reload (Cmd+Shift+R)
```

### Asset URL 404?

```bash
# Check file exists
ls -lh dcnet_apps/dcnet_apps/public/images/

# Check symlink
ls -lh development/frappe-bench/sites/assets/dcnet_apps/images/

# Re-link assets
bench build --app dcnet_apps
```

## ✅ Verification Checklist

- [x] Navbar logo hiển thị DCNET TELECOM (160×52px)
- [x] Favicon hiển thị paper plane vàng (32×32px)
- [x] Splash screen hiển thị DCNET TELECOM khi loading
- [x] Logo scale tốt trên các độ phân giải
- [x] Assets accessible qua HTTP (200 OK)
- [x] Git tracked đầy đủ files
- [x] Documentation complete

---

**Last Updated:** 2026-01-16
**Status:** Production Ready ✅
