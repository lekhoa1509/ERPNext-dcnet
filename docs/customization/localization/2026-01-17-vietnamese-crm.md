# Vietnamese CRM Translation

> **Date:** 2026-01-17
> **Type:** Localization
> **Status:** Active (355/1340 strings translated)

---

## 1. Overview

Dịch giao diện Frappe CRM sang tiếng Việt để người dùng DCNET Flow sử dụng dễ dàng hơn.

**Phạm vi:**
- Frappe CRM UI (Lead, Deal, Contact, Organization, etc.)
- Labels, buttons, messages, notifications
- Status & stage names

**Không bao gồm:**
- ERPNext modules (sẽ dịch riêng)
- Frappe Framework core (đã có sẵn)

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Translation Flow                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  dcnet_crm/crm/locale/vi.po                                │
│         ↓                                                   │
│  bench build --app crm                                      │
│         ↓                                                   │
│  sites/assets/locale/vi/LC_MESSAGES/crm.mo                 │
│         ↓                                                   │
│  CRM Frontend calls get_translations() API                  │
│         ↓                                                   │
│  UI displays Vietnamese                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Files Structure

```
flow_next/
├── dcnet_crm/
│   └── crm/
│       └── locale/
│           ├── vi.po           # Vietnamese translations (MODIFIED)
│           └── vi.po.backup    # Original backup
│
├── dcnet_apps/
│   └── dcnet_apps/
│       └── install.py          # setup_vietnamese_language() hook
│
├── scripts/
│   └── translate_crm.py        # Translation script with glossary
│
└── docs/
    └── translations/
        ├── CRM_GLOSSARY.md     # Standard terminology
        └── vi_untranslated.txt # Strings needing translation
```

---

## 4. Translation Statistics

| Metric | Value |
|--------|-------|
| Total strings | 1,340 |
| Translated | 355 (26%) |
| Untranslated | 985 (74%) |
| Source file | `dcnet_crm/crm/locale/vi.po` |
| Glossary | `docs/translations/CRM_GLOSSARY.md` |

### Key Terms Translated

| English | Vietnamese |
|---------|------------|
| Lead | Khách hàng tiềm năng |
| Deal | Cơ hội kinh doanh |
| Contact | Liên hệ |
| Organization | Tổ chức |
| Task | Công việc |
| Note | Ghi chú |
| Activity | Hoạt động |
| Status | Trạng thái |
| Stage | Giai đoạn |
| Pipeline | Quy trình |
| Won | Thành công |
| Lost | Thất bại |
| Owner | Người phụ trách |
| Assignee | Người được giao |

---

## 5. How It Works

### 5.1 Translation Hook (install.py)

```python
def setup_vietnamese_language():
    """
    Set Vietnamese as default language for all users.
    Called after bench migrate.
    """
    # Set system default
    frappe.db.set_single_value("System Settings", "language", "vi")

    # Set for all users
    users = frappe.get_all("User", filters={"name": ["not in", ["Guest"]]})
    for user in users:
        frappe.db.set_value("User", user, "language", "vi")
```

### 5.2 CRM Translation Loading

CRM frontend calls API `crm.api.get_translations()`:

```python
@frappe.whitelist(allow_guest=True)
def get_translations():
    language = frappe.db.get_value("User", frappe.session.user, "language")
    return get_all_translations(language)
```

### 5.3 Translation Script

```bash
# Add new translations to glossary in scripts/translate_crm.py
# Then run:
python3 scripts/translate_crm.py

# Output:
# ✅ Backup created: dcnet_crm/crm/locale/vi.po.backup
# 📊 Translation Statistics:
#    - New translations: 339
#    - Already translated: 16
#    - Untranslated: 985
```

---

## 6. Deployment

### New Setup

```bash
# 1. Pull code (includes vi.po with translations)
git pull origin main

# 2. Build CRM (compiles .mo file)
bench build --app crm

# 3. Migrate (runs setup_vietnamese_language hook)
bench --site [site] migrate

# 4. Clear browser cache / unregister PWA service worker
```

### Adding New Translations

```bash
# 1. Edit glossary in scripts/translate_crm.py (GLOSSARY dict)

# 2. Run translation script
python3 scripts/translate_crm.py

# 3. Rebuild CRM
bench build --app crm

# 4. Clear cache
bench --site [site] clear-cache
```

---

## 7. Troubleshooting

### UI Still Shows English

1. **Check User language:**
   ```python
   bench --site [site] console
   >>> frappe.db.get_value("User", "Administrator", "language")
   # Must return 'vi'
   ```

2. **Clear PWA cache (CRM is a PWA):**
   - F12 → Application → Service Workers → Unregister
   - F12 → Application → Storage → Clear site data
   - Hard refresh: Ctrl+Shift+R

3. **Verify .mo file exists:**
   ```bash
   ls -la sites/assets/locale/vi/LC_MESSAGES/crm.mo
   ```

4. **Check translations loaded:**
   ```python
   >>> from frappe.translate import get_all_translations
   >>> t = get_all_translations("vi")
   >>> t.get("Lead")
   'Khách hàng tiềm năng'
   ```

### Restore Original vi.po

```bash
cp dcnet_crm/crm/locale/vi.po.backup dcnet_crm/crm/locale/vi.po
bench build --app crm
```

---

## 8. Glossary Management

### Location
- `docs/translations/CRM_GLOSSARY.md` - Human-readable reference
- `scripts/translate_crm.py` - GLOSSARY dict (source of truth)

### Adding New Terms

1. Add to `GLOSSARY` dict in `scripts/translate_crm.py`:
   ```python
   GLOSSARY = {
       # ...existing...
       "New Term": "Thuật ngữ mới",
   }
   ```

2. Run script:
   ```bash
   python3 scripts/translate_crm.py
   ```

3. Update `CRM_GLOSSARY.md` for documentation

### Translation Guidelines

| Rule | Example |
|------|---------|
| Keep technical terms | API, Webhook, Kanban |
| Keep brand names | WhatsApp, Twilio |
| Keep DocType names in technical context | CRM Lead, CRM Deal |
| Translate user-facing labels | Lead → Khách hàng tiềm năng |
| Be consistent | One English term = One Vietnamese term |

---

## 9. Future Work

### Phase 1 (Current)
- [x] Core CRM terms (Lead, Deal, Contact, etc.)
- [x] Status & stages
- [x] Common actions (Add, Edit, Delete, etc.)
- [x] Auto-set Vietnamese language hook

### Phase 2 (Planned)
- [ ] Translate remaining 985 strings
- [ ] ERPNext modules translation
- [ ] Email templates in Vietnamese
- [ ] Print formats in Vietnamese

### Phase 3 (Future)
- [ ] Contribute translations to Frappe CRM upstream (Crowdin)
- [ ] Multi-language support (EN/VI toggle)

---

## 10. References

- **Frappe CRM Crowdin:** https://crowdin.com/project/frappe
- **Frappe Translation Docs:** https://frappeframework.com/docs/user/en/translations
- **DCNET Glossary:** `docs/translations/CRM_GLOSSARY.md`

---

**Created by:** Claude Code
**Maintained by:** DCNET Cloud Team
