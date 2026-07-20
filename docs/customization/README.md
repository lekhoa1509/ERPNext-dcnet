# UI/UX Customization Log

This directory contains documentation for all UI/UX customizations made to DCNET Flow.

## 📁 Structure

```
customization/
├── README.md           # This file - Index of all customizations
├── ui/                 # UI-specific customizations
│   ├── 2026-01-16-branding-logo.md
│   ├── 2026-01-29-desktop-icons.md
│   └── 2026-01-30-disable-modules.md
└── integration/        # Backend integrations
    └── 2026-01-16-crm-deal-to-customer.md
```

## 📋 Customization Index

| Date | Type | Title | Status | Files Changed |
|------|------|-------|--------|---------------|
| 2026-01-16 | Branding | Logo & Favicon Customization | ✅ Complete | `boot.py`, `hooks.py`, `install.py`, `public/images/` |
| 2026-01-16 | Integration | CRM Deal to Customer | ✅ Complete | `install.py` (Frappe CRM built-in) |
| 2026-01-17 | i18n | Frappe Vietnamese Translations | ✅ Complete | `install.py`, `locale/frappe/vi.po` |
| 2026-01-17 | CRM Config | FCRM Settings Currency VND | ✅ Complete | `install.py` |
| 2026-01-17 | ERPNext Config | Auto Fiscal Year Setup | ✅ Complete | `install.py` |
| 2026-01-29 | UI | Desktop Icons & Folders | ✅ Complete | `install.py`, `public/icons/` |
| 2026-01-30 | System | Disable Unused Modules | ✅ Complete | `install.py` |
| 2026-05-17 | UI | Excel Print Preview | ✅ Complete | `excel_print_template_builder.js`, `form_utils.bundle.js` |
| 2026-05-19 | UI | Import tự động (AI) File Preview & Feedback History | ✅ Complete | `import_auto.js`, `import_auto.py`, `processor.py`, `import_auto_file.json` |
| 2026-05-25 | UI | Import Auto Direct Import | ✅ Complete | `import_auto.js`, `import_auto.py`, `processor.py`, `smart_planner.py`, `smart_runner.py`, `import_auto_file.json` |
| 2026-06-12 | UI | Opening Balance Server Upload | ✅ Complete | `opening_balance_import.js`, `opening_balance_import.py`, `import_auto.py` |
| 2026-06-13 | UI | DCNET CRM Customer Workspace | ✅ Complete | `dcnet_crm/api.py`, `frontend/src/main.js`, `frontend/src/styles.css` |
| 2026-06-29 | UI | DCNET CRM Enterprise UI | ✅ Complete | `frontend/src/styles.css`, `features/dashboard/template.js`, `features/customers/template.js` |
| 2026-07-06 | UI | DCNET CRM Lead Approval Gate | ✅ Complete | `features/leads/template.js`, `features/leads/composable.js` |
| 2026-07-06 | UI | DCNET CRM Lead MISA Detail UI | ✅ Complete | `features/leads/template.js`, `frontend/src/styles.css`, `dcnet_crm/api.py` |
| 2026-07-06 | UI | DCNET CRM Contact MISA Tabs | ✅ Complete | `features/contacts/template-detail.js`, `features/contacts/composable-create.js`, `frontend/src/styles.css`, `dcnet_crm/api.py` |
| 2026-07-06 | UI | DCNET CRM Customer MISA Detail UI | ✅ Complete | `features/customers/template.js`, `features/customers/composable.js`, `frontend/src/styles.css`, `dcnet_crm/api.py` |
| 2026-07-13 | UI | DCNET CRM Dashboard Redesign | ✅ Complete | `features/dashboard/template.js`, `features/dashboard/composable.js`, `frontend/src/styles.css` |
| 2026-07-14 | UI | DCNET CRM Quotation Detail Actions | ✅ Complete | `features/quotations/template.js`, `features/quotations/composable.js`, `features/orders/composable.js`, `dcnet_crm/api.py` |
| 2026-07-14 | UI | DCNET CRM Order Related Documents Compact UI | ✅ Complete | `features/orders/template.js`, `features/orders/composable.js`, `frontend/src/styles.css` |
| 2026-07-15 | UI/Integration | DCNET CRM Sales Order Word Print | ✅ Complete | `dcnet_crm/api.py`, `features/orders/template.js`, `features/orders/composable.js`, `frontend/src/styles.css` |
| 2026-07-14 | UI | DCNET CRM Discussion #9 Feedback Batch | 🧪 QA pending | `dcnet-crm/docs/DISCUSSION_9_FEEDBACK_CHECKLIST.html`, CRM feature templates/composables, `dcnet_crm/api.py` |
| 2026-07-14 | UI | DCNET CRM Lead Detail MISA Reference Refresh | 🧪 QA pending | `features/leads/template.js`, `features/leads/composable.js`, `frontend/src/styles.css` |
| 2026-07-08 | UI | VN Accounting Bank Settings Sidebar | ✅ Complete | `workspace_sidebar/vn_accounting.json`, `help/thiet-lap/index.md` |
| 2026-07-08 | UI | VN Accounting Bank Master Sidebar | ✅ Complete | `workspace_sidebar/vn_accounting.json`, `help/danh-muc/index.md` |
| 2026-07-08 | UI | VN Accounting Tax Settings Sidebar | ✅ Complete | `workspace_sidebar/vn_accounting.json`, `help/thue/index.md` |
| 2026-07-08 | UI | VN Accounting Pro Demo | ✅ Prototype | `docs/vn-accounting/accounting-pro-demo/index.html` |

## 🎯 Types of Customizations

### 1. Branding
- Logo, favicon, splash screens
- App name, colors, themes
- Email templates branding

### 2. UI Components
- Custom widgets, forms
- Dashboard layouts
- Navigation modifications

### 3. Themes & Styling
- CSS customizations
- Color schemes
- Typography

### 4. User Experience
- Workflow customizations
- Keyboard shortcuts
- Quick actions

### 5. Integration
- CRM to ERPNext integrations
- External API connections
- Data sync handlers

### 6. Localization (i18n)
- Vietnamese translations for Frappe/ERPNext
- Custom terminology glossary
- Auto-sync translations on migrate

## 📝 Documentation Template

When adding new customization, create file: `YYYY-MM-DD-category-name.md`

**Required sections:**
1. Overview
2. Requirements
3. Implementation
4. Technical Notes
5. Deployment
6. Future Updates
7. Troubleshooting
8. Verification Checklist

**See:** `ui/2026-01-16-branding-logo.md` for reference.

## 🔍 Quick Reference

### Current Customizations

#### Branding Logo (2026-01-16)
- **What:** DCNET TELECOM logo + Paper plane favicon
- **Files:** `boot.py`, `hooks.py`, `dcnet-logo.png`, `favicon.png`
- **How to update:** Replace PNG files, clear cache, reload browser
- **Docs:** [ui/2026-01-16-branding-logo.md](ui/2026-01-16-branding-logo.md)

#### CRM Deal to Customer (2026-01-16)
- **What:** Auto-create ERPNext Customer when CRM Deal status = "Won"
- **Files:** `install.py` (uses Frappe CRM built-in)
- **Config:** Auto-configured via `bench migrate` (ERPNext CRM Settings)
- **Settings:** `enabled=1`, `create_customer_on_status_change=1`, `deal_status="Won"`
- **Docs:** [integration/2026-01-16-crm-deal-to-customer.md](integration/2026-01-16-crm-deal-to-customer.md)

#### Frappe Vietnamese Translations (2026-01-17)
- **What:** Vietnamese translations for Frappe Framework (~3,411 strings)
- **Source:** `dcnet_apps/locale/frappe/vi.po` (tracked in git)
- **Target:** `frappe/frappe/locale/vi.po` (inside container)
- **Sync:** Auto-sync via `bench migrate` → `sync_frappe_translations()`
- **Coverage:** ~63% (3,739/5,903 strings) - UI buttons, common labels, messages
- **Last Updated:** 2026-01-18 (added ~394 strings total - Please enter*, Please find*, Please login*, Please make/refresh/remove*, Please save*, Please select*, Please set*)

#### FCRM Settings Currency VND (2026-01-17)
- **What:** Auto-set FCRM Settings currency to VND (single-currency mode)
- **Why:** Bypass exchange rate API calls when creating CRM Organization
- **Problem:** Default provider (Frankfurter API) doesn't support VND → error when creating Organization
- **Solution:** Set FCRM Settings currency = VND, so `VND == VND` → no API call needed
- **Files:** `install.py` → `setup_fcrm_settings()`
- **Runs on:** `after_install`, `after_migrate`

#### Auto Fiscal Year Setup (2026-01-17)
- **What:** Auto-create Fiscal Year for current year if not exists
- **Why:** ERPNext requires Fiscal Year for all accounting operations
- **Problem:** Without Fiscal Year → `FiscalYearError` when opening Customer form (after CRM Deal → Won)
- **Solution:** Auto-create Fiscal Year on migrate (e.g., 2026: 01-01-2026 to 31-12-2026)
- **Files:** `install.py` → `setup_fiscal_year()`
- **Runs on:** `after_install`, `after_migrate`

#### Desktop Icons & Folders (2026-01-29)
- **What:** Customize Desk home page icons - hide, add, group into folders
- **Why:** Organize icons by business function (e.g., "Dịch vụ Golf", "Kế toán")
- **Features:**
  - Ensure ERPNext icons visible (CRM, Selling, Buying, Stock, Assets)
  - Hide workspaces (Manufacturing, Quality, Projects, Subcontracting, HR, Payroll)
  - Create icon folders (Kế toán, Dịch vụ Golf)
  - Use custom SVG icons from dcnet_apps
- **Files:** `install.py` → `setup_desk()`, `setup_desktop_icon_folders()`
- **Runs on:** `after_install`, `after_migrate`
- **Docs:** [ui/2026-01-29-desktop-icons.md](ui/2026-01-29-desktop-icons.md)

**Visible icons:** CRM, Selling, Buying, Stock, Assets, ERPNext Settings

**Folder groups:**
| Folder | Children |
|--------|----------|
| Dịch vụ Golf | Fitting, Coaching, Trade-in |
| Kế toán | Accounting, Financial Reports, Taxes, Budget, Banking |

#### Disable Unused Modules (2026-01-30)
- **What:** Disable modules không dùng qua Domain Settings
- **Why:** Ẩn buttons/features không cần (vd: "Work Order" trong Sales Order)
- **Enabled:** Distribution, Services, Retail
- **Disabled:** Manufacturing, Education, Healthcare, Agriculture, Non Profit
- **Files:** `install.py` → `setup_active_domains()`
- **Runs on:** `after_migrate`
- **Docs:** [ui/2026-01-30-disable-modules.md](ui/2026-01-30-disable-modules.md)

**What gets hidden when Manufacturing disabled:**
| DocType | Hidden Features |
|---------|-----------------|
| Sales Order | Button "Work Order", Dashboard link "Manufacturing" |
| Item | Section "Manufacturing", BOM fields |
| Purchase Order | Subcontracting features |

**Fiscal Year is required for:**
| Feature | Needs Fiscal Year |
|---------|-------------------|
| Customer Dashboard | ✅ Yes (shows revenue by year) |
| Sales Invoice | ✅ Yes |
| Purchase Invoice | ✅ Yes |
| Payment Entry | ✅ Yes |
| Financial Reports | ✅ Yes |

**Translation locations:**
| App | Location | Tracked |
|-----|----------|---------|
| Frappe Framework | `dcnet_apps/locale/frappe/vi.po` | ✅ Yes |
| Frappe CRM | `dcnet_crm/crm/locale/vi.po` | ✅ Yes |
| ERPNext | `dcnet_core/erpnext/locale/vi.po` | ✅ Yes |

## 🚀 Quick Commands

### Apply All Customizations (New Setup / After Pull)

```bash
# 1. Pull code
git pull origin main

# 2. Run migrate - ALL configurations auto-apply
bench --site flow.local migrate

# 3. Restart (recommended)
bench restart

# 4. Hard reload browser
# Cmd+Shift+R (Mac) / Ctrl+Shift+R (Windows)
```

**Expected output:**
```
✅ Navbar Settings updated with DCNET logo
✅ Website Settings updated with DCNET branding
✅ Cache cleared - branding applied
✅ ERPNext CRM Settings: Auto-create Customer on Deal Won
✅ FCRM Settings: Currency set to VND (single-currency mode)
✅ Fiscal Year 2026 created (01-01 to 31-12)
✅ Frappe translations synced: vi.po (1,102,830 bytes)
✅ Vietnamese language set for X users
```

### Verify Customizations

```bash
# Check logo URLs
curl -I http://localhost:8000/assets/dcnet_apps/images/dcnet-logo.png
curl -I http://localhost:8000/assets/dcnet_apps/images/favicon.png

# Check boot session
bench --site flow.local console
>>> from frappe.boot import get_bootinfo
>>> boot = get_bootinfo()
>>> boot['app_data'][0]['app_logo_url']
```

## 📚 Best Practices

1. **Documentation First:** Document before coding
2. **Git Everything:** All customizations must be in git
3. **Test Thoroughly:** Test on clean setup before commit
4. **Clear Instructions:** Write deployment steps for team
5. **Rollback Plan:** Document how to revert if needed

## 🤝 Contributing

When adding new customization:

1. Create documentation file in appropriate folder
2. Update this README.md index table
3. Test on clean environment
4. Commit with clear message
5. Share with team

---

**Maintained by:** DCNET Cloud Team
**Last Updated:** 2026-01-30
