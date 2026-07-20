# App Architecture Design - Single App vs Multi App

> **Brainstorm date:** 11/02/2026
> **Status:** COMPLETE
> **Decision:** Giu 1 app `dcnet_apps` voi nhieu modules ben trong (Phuong an A)
> **Reference:** Xac nhan lai quyet dinh tu `2026-02-10-project-reset-design.md` Section 5.5.2

---

## 1. Context

DCNET Flow su dung `dcnet_apps` la 1 Frappe app chua nhieu modules ben trong (hien tai: Fitting, Order Schedule). Voi ~43-51 modules planned, can xac nhan: nen giu 1 app hay tach thanh nhieu app rieng?

### Hien trang

```
dcnet_apps/
├── dcnet_apps/          # 1 Frappe app
│   ├── hooks.py         # 1 file hooks duy nhat
│   ├── modules.txt      # 2 modules: Fitting, Order Schedule
│   ├── fitting/         # Module Fitting (3 DocTypes, 5 Reports)
│   ├── order_schedule/  # Module Order Schedule (1 DocType)
│   ├── crm/             # CRM extensions (Lead customization)
│   ├── core/            # Shared utilities
│   └── ...
└── dcnet_fixtures/      # App rieng cho test data
```

Apps da cai: frappe + erpnext + dcnet_apps + dcnet_fixtures (4 apps)

Quy mo planned: ~11-15 custom modules (0% ERPNext) + ~10 heavy customization modules

---

## 2. So sanh 3 phuong an

### A. Giu nguyen: 1 App `dcnet_apps` (nhieu modules ben trong) — RECOMMENDED

**Day la pattern chuan cua Frappe/ERPNext.**

| Pro | Con |
|-----|-----|
| ERPNext tu no = 1 app, 21 modules | hooks.py se dai khi co nhieu modules |
| Deploy don gian: 1 app = 1 lan install | Khong the install/uninstall module rieng le |
| Cross-module import truc tiep (fitting → crm) | Git history chung cho tat ca modules |
| 1 version number, 1 release cycle | Test toan app khi chay `bench run-tests` |
| Team 5 nguoi de coordinate | |
| Design doc da chon phuong an nay | |

**Bang chung tu Frappe ecosystem:**
- ERPNext: 21 modules, 1 app, hang tram DocTypes
- Frappe framework: 11 modules, 1 app
- Khong co performance penalty (module map cached, DocTypes lazy-loaded)

### B. Multi App: Moi module 1 app (`dcnet_fitting`, `dcnet_coaching`, ...)

| Pro | Con |
|-----|-----|
| Install/uninstall tung module doc lap | 11-15 apps phai quan ly, deploy, version rieng |
| Moi app co hooks.py rieng, gon | Cross-module dependency phuc tap (required_apps) |
| Test isolated per app | Them overhead: moi app can pyproject.toml, setup, README |
| Independent release cycle | 5 nguoi dev 15 repos = overhead coordination lon |
| | Frappe load hooks tu TAT CA apps → nhieu app = cham hon |
| | Khong can thiet vi 2 site dung chung 100% code |

### C. Hybrid: 2-3 App nhom theo domain

```
dcnet_core_ext/    → CRM extensions, Sales, Purchase, Stock, Accounting customizations
dcnet_services/    → Fitting, Coaching, Membership, Workshop
dcnet_integration/ → Giao van, Web Sync, Barcode
```

| Pro | Con |
|-----|-----|
| Nhom logic theo domain | Ranh gioi domain kho xac dinh ro |
| Hooks.py vua phai per app | Cross-app dependencies van phuc tap |
| Co the disable nhom service cho NM | Them complexity cho team 5 nguoi |
| | Phai refactor lai cau truc hien tai |

---

## 3. Frappe Framework - Su that ky thuat

1. **Hooks chi co o app-level** — Khong co per-module hooks. 1 app = 1 `hooks.py`
2. **Khong the install/uninstall module rieng** — `bench install-app` = cai tat ca modules trong app do
3. **Module names phai unique toan he thong** — Du 1 app hay nhieu app
4. **Fixtures la app-level** — Khong co per-module fixtures mechanism
5. **`restrict_to_domain`** tren Module Def chi an UI, khong disable code/tables

---

## 4. Lich su Frappe ecosystem

| App | Truoc | Sau | Ly do tach |
|-----|-------|-----|-----------|
| HRMS | Module trong ERPNext | App rieng (v14) | Giam bloat, independent identity, rieng issue tracker |
| Healthcare | Module trong ERPNext | App rieng | Community-contributed, niche, khong phai ai cung can |
| Education | Module trong ERPNext | App rieng | Tuong tu Healthcare |

**Diem chung khi tach:** Deu la modules ma NHIEU site KHONG CAN. DCNET Flow thi 2 site deu can gan het modules → khong can tach.

---

## 5. Quyet dinh: Phuong an A — Giu 1 app `dcnet_apps`

### Ly do chinh

1. **Chuan Frappe pattern** — ERPNext 21 modules, 1 app, chay production worldwide
2. **Team 5 nguoi** — Multi-repo overhead khong dang
3. **2 site dung chung code** — Khong co nhu cau install module khac nhau (dung `restrict_to_domain` de an UI)
4. **Modules lien ket chat** — Fitting → CRM, Sales → Stock, CRM → Accounting
5. **Design doc da quyet dinh** — `2026-02-10-project-reset-design.md` Section 5.5.2

### Cach quan ly hooks.py khi nhieu modules

Pattern hien tai (hooks.py ngan, doc events truc tiep):

```python
# hooks.py
doc_events = {
    "Lead": {"validate": "dcnet_apps.crm.lead.lead_validation.validate_lead_duplicate"},
    "Data Import": {"validate": "dcnet_apps.core.data_import_validation.validate_import_row_limit"},
}
```

Khi hooks.py dai hon (~20+ modules), co the delegate:

```python
# hooks.py - pattern nang cao
from dcnet_apps.fitting.setup import fitting_doc_events
from dcnet_apps.coaching.setup import coaching_doc_events

doc_events = {}
for events in [fitting_doc_events, coaching_doc_events]:
    for doctype, handlers in events.items():
        doc_events.setdefault(doctype, {}).update(handlers)
```

> **Luu y:** Pattern nay chi can thiet khi hooks.py vuot 200+ dong. Hien tai van giu truc tiep.

### Modules TM-only / NM-only

- Dung `restrict_to_domain` tren Module Def (an khoi Desk)
- Hoac check company trong code logic
- KHONG can tach app

---

## 6. Dieu kien xem xet tach app (tuong lai)

Chi xem xet tach app khi:
- Team scale len 15+ nguoi, can parallel release cycles
- Co nhu cau sell/distribute module rieng le (SaaS marketplace)
- Module thuc su 100% doc lap, khong share data voi modules khac

---

## 7. Ket luan

**Giu `dcnet_apps` la 1 app, nhieu modules ben trong.** Day la:
- Chuan Frappe ecosystem
- Phu hop quy mo team (5 nguoi)
- Phu hop deployment (2 site, chung code)
- Da duoc quyet dinh trong design doc
- Khong co technical limitation nao buoc phai tach

---

## 8. Thuc hien: Reset dcnet_apps (11/02/2026)

Sau khi xac nhan architecture, da reset dcnet_apps de chuan bi tao lai modules tu dau.

### Da xoa (57 files)

| Component | Files | Chi tiet |
|-----------|-------|----------|
| `fitting/` | 38 | 3 DocTypes, 5 Reports, setup.py (workflow), workspace |
| `order_schedule/` | 16 | 1 DocType, 3 Workspaces, 2 Number Cards, fixtures |
| `crm/deal_handler.py` | 1 | Dead code — Frappe CRM da remove, ERPNext CRM khong co Deal DocType |
| `public/css/workflow_viewer.css` | 1 | Fitting workflow viewer styles |
| `public/icons/.../fitting.svg` | 1 | Fitting desktop icon |

### Da sua (5 files)

| File | Thay doi |
|------|----------|
| `modules.txt` | Xoa Fitting + Order Schedule (file trong, chua co module nao) |
| `hooks.py` | Xoa Order Schedule fixture entries |
| `install.py` | Xoa Fitting/OS tu icon whitelist & config, comment out Dich vu folder |
| `dcnet_apps/README.md` | Cap nhat structure, xoa stale Fitting references |
| `README.md` (top-level) | Cap nhat toan bo, xoa stale content |

### Cau truc sau reset

```
dcnet_apps/dcnet_apps/
├── hooks.py          # Boot, branding, Lead/DataImport doc_events
├── install.py        # Branding, desk icons (CRM/Selling/Buying/Stock/Assets), translations, domains
├── boot.py           # App title/logo override
├── modules.txt       # (trong — chua co module nao)
├── crm/
│   └── lead/
│       └── lead_validation.py    # Lead duplicate email/phone validation
├── core/
│   └── data_import_validation.py # Max 1000 row import limit
├── public/
│   ├── css/dcnet_theme.css       # DCNET branding
│   ├── images/                   # Logo + favicon
│   └── desktop_icons/            # SVG icons cho ERPNext modules
├── locale/                       # Vietnamese translations (frappe + erpnext)
└── fixtures/                     # Lead custom fields + property setters
```

### Luu y

- `dcnet_fixtures` app van con references den fitting/order_schedule (generators, sample data). Can clean up khi tao lai 2 module nay.
- Fitting workflow (8 states, 11 transitions) da luu trong `install.py` comment out block cua `setup_desktop_icon_folders()` de tham khao.
- Se tao lai Fitting + Order Schedule modules tu dau theo quy trinh chuan.
