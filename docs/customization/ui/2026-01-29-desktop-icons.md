# Desktop Icons Customization

> **Date:** 29/01/2026
> **Category:** UI/UX - Desk Home Page
> **Status:** Implemented

## Overview

Customize Frappe Desk home page icons for DCNET Flow using **Whitelist Approach**:

**Strategy:** Hide ALL icons first, then show only what we need.

This ensures any new ERPNext icons/workspaces added in future updates are hidden by default.

**Features:**
- Show only whitelisted icons (CRM, Selling, Buying, Stock, Assets, Fitting)
- Group icons into folders (Kế toán, Dịch vụ Golf)
- Use custom SVG icons from dcnet_apps

## Team Sync

```bash
# Pull code and run migrate - all devs get same desk layout
git pull origin main
bench --site flow.local migrate
```

## Implementation

### Files

| File | Purpose |
|------|---------|
| `dcnet_apps/install.py` | Main setup logic via `setup_desk()` hook |
| `dcnet_apps/public/icons/desktop_icons/solid/*.svg` | Custom SVG icons |

### Key Functions

```python
# dcnet_apps/install.py

setup_desk()                        # Main entry (called on migrate)
├── hide_all_desktop_icons()        # 1. Hide ALL icons first
├── hide_all_workspaces()           # 2. Hide ALL workspaces
├── ensure_erpnext_desktop_icons()  # 3. Show only whitelisted icons
├── update icons app                # 4. Use dcnet_apps custom SVG
└── setup_desktop_icon_folders()    # 5. Create folder groups (also unhides)

# Utility functions (for manual use in bench console)
hide_desktop_icons(labels)      # Hide icons by label
show_desktop_icons(labels)      # Show icons by label
reorder_desktop_icons(order)    # Change icon order
```

## Configuration

### Whitelist Icons (Standalone)

Only these icons are visible on desk (everything else is hidden):

```python
icons_whitelist = [
    "CRM",
    "Selling",
    "Buying",
    "Stock",
    "Assets",
    "Fitting",  # Added 29/01/2026 - standalone icon
]
```

> **Note:** ERPNext Settings removed from whitelist - not compatible with Desktop Icon system. Access via search bar (Ctrl+K → "ERPNext Settings").

### Folder Groups

Icons inside folders are automatically unhidden when the folder is created.

```python
folder_config = {
    "Dịch vụ Golf": {
        "idx": 7,  # After Fitting (idx=5) and Assets (idx=6)
        "icon": "file",
        "children": [
            # NOTE: Fitting moved to standalone icon (29/01/2026)
            {"label": "Coaching", "link_to": "Coaching", "icon": "education"},
            {"label": "Trade-in", "link_to": "Trade-in", "icon": "refresh"},
        ]
    },
    "Kế toán": {
        "idx": 20,
        "icon": "accounting",
        "children": [
            {"label": "Accounting", "link_to": "Accounting"},
            {"label": "Financial Reports", "link_to": "Financial Reports"},
            {"label": "Taxes", "link_to": "Taxes"},
            {"label": "Budget", "link_to": "Budget"},
            {"label": "Banking", "link_to": "Banking"},
        ]
    },
}
```

## How It Works

### Desktop Icon DocType

| Field | Description |
|-------|-------------|
| `label` | Display name |
| `icon_type` | `Link` \| `Folder` \| `App` |
| `link_type` | `Workspace Sidebar` \| `External` |
| `link_to` | Target workspace name |
| `parent_icon` | Folder label to nest inside |
| `hidden` | 1 = hidden from view |
| `idx` | Sort order |
| `app` | App name for custom icons |

### Icon Type: Folder

When `icon_type = "Folder"`:
- Displays as a folder tile on home
- Click opens modal showing child icons
- Children have `parent_icon = folder label`

### Custom SVG Icons

Location:
```
dcnet_apps/public/icons/desktop_icons/solid/{name}.svg
```

Frappe loads from:
```
/assets/dcnet_apps/icons/desktop_icons/solid/{name}.svg
```

## Usage

### Apply Changes (Team Sync)

```bash
bench --site flow.local migrate
```

Expected output:
```
✅ Hidden all: X icons, Y workspaces
✅ ERPNext icons: 0 created, 5 shown
✅ Updated 5 desktop icons to use custom SVG
✅ Desktop folders: 2 folders, 8 child icons
```

### Manual Operations (bench console)

```python
import frappe
from dcnet_apps.install import (
    hide_desktop_icons,
    show_desktop_icons,
    reorder_desktop_icons
)

# Hide icons
hide_desktop_icons(["Home", "Website"])

# Show icons
show_desktop_icons(["HR", "Payroll"])

# Reorder icons
reorder_desktop_icons(["CRM", "Selling", "Stock", "Buying"])

frappe.db.commit()
```

## Troubleshooting

### Icons not updating

```bash
bench --site flow.local clear-cache
# Then Ctrl+Shift+R in browser
```

### Folder not showing children

Check:
1. Child icons have `parent_icon` matching folder `label`
2. Child icons are not `hidden = 1`
3. Target workspace exists

```python
# Debug in bench console
frappe.get_all("Desktop Icon",
    filters={"parent_icon": "Kế toán"},
    fields=["label", "hidden", "link_to"]
)
```

## Related Files

- `dcnet_apps/install.py:168-370` - Desk setup functions
- `dcnet_apps/public/icons/desktop_icons/solid/*.svg` - Custom icons
- `frappe/desk/doctype/desktop_icon/` - Desktop Icon DocType

## References

- [Frappe Workspace](https://docs.frappe.io/framework/user/en/desk/workspace)
