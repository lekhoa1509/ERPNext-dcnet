# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

**DCNET Flow** is a comprehensive business management platform combining CRM, Sales, Inventory, Accounting, and specialized business modules built on Frappe + ERPNext.

---

## ⚠️ IMPORTANT - Development Guidelines

> **CRITICAL:** All features MUST be based on official requirements specifications from customer

**Source Documents (in `docs/feature/`):**
- `FEATURE_SPECIFICATION.md` - Phase 1: CRM Requirements (08/12/2025)
- `ERP_SPECIFICATION.md` - Phase 2: ERP Requirements (30/12/2025)
- `IMPORT_PROCESS_SPECIFICATION.md` - Phase 2: Import Process (30/12/2025)

**Rules:**
- ✅ Extract & implement features from specs. Reference: "Nguồn: FEATURE_SPECIFICATION.md Section X"
- ✅ Document all assumptions as questions
- ❌ NEVER add features not in specs
- ❌ NEVER "improve" or "optimize" requirements without approval
- ❌ DO NOT assume or fill in missing details - Note: "⚠️ Cần clarify với khách hàng"

---

## 📋 Project Context

| Item | Value |
|------|-------|
| **Project** | DCNET Flow |
| **Status** | PRE-CONTRACT - Chờ ký HĐ |
| **2 công ty** | Thăng Long TM + Nhật Minh Sport (2 site riêng, code chung, 2 HĐ riêng) |
| **Platform** | Frappe v16 + ERPNext v16 (released 12/01/2026) |
| **Strategy** | Tận dụng ERPNext tối đa, custom app cho modules đặc thù |
| **Start Date** | 10/03/2026 |
| **Bàn giao** | T3→T6 (31/03, 30/04, 30/05, 30/06) + T7 migration + T8 bổ sung |
| **Team** | 5 người (Đức, Phương, Cường, Đạt, Hậu) |
| **Data Migration** | BRAVO → ERPNext (validate kế toán) |
| **SRS** | 2 file riêng (`docs/contract/DCNET_SRS_TM.md` + `DCNET_SRS_NM.md`), brand DCNET |

**Key Documents:** `docs/roadmap/TIMELINE_2026.md` | `docs/plans/2026-02-10-project-reset-design.md` | `docs/infrastructure/CLOUD_INFRASTRUCTURE_PLAN.md`

---

## 📅 Timeline 2026 (Theo tháng bàn giao)

| Tháng | Focus | Bàn giao |
|-------|-------|----------|
| **T3** | Đăng nhập, Dashboard, Sản phẩm, NCC, Mua hàng, BC Phân tích | 31/03 |
| **T4** | Kho, Đơn hàng, Bán buôn/lẻ, Bán hàng, Trade-in, Chi nhánh, NV, KH, 5x BC | 30/04 |
| **T5** | Kế toán (Tiền, Mua, Bán, Công nợ, HTK, Chi phí, Tài sản, Thuế, Tổng hợp), BC | 30/05 |
| **T6** | Lead, Fitting, Coaching★, CSKH, Tích điểm★, Giao vận, Role, Kiểm soát | 30/06 |
| **T7** | Migrate dữ liệu BRAVO, Setup server, Bàn giao, Đào tạo | |
| **T8** | Membership★, Dự báo DT★, Workshop★ (TM only) | |

★ = Chỉ 1 công ty (xem chi tiết `docs/plans/2026-02-10-project-reset-design.md`)

**2 công ty:** Thăng Long TM + Nhật Minh Sport (2 site riêng, code chung)

**Scope:** ~43 modules chung + 4 TM only + 5 NM only

---

## 📦 Project Structure

```
flow_next/ (repository)
├── .devcontainer/               # 🐳 VS Code Devcontainer config
│   ├── docker-compose.yml
│   └── devcontainer.json
├── development/                 # 🛠️ Development workspace
│   ├── installer.py             # Auto-setup script (run inside devcontainer)
│   └── frappe-bench/            # Generated (gitignored)
├── dcnet_core/                  # 🎯 ERPNext v16 (symlinked as apps/erpnext)
│   └── erpnext/
├── dcnet_apps/                  # ⭐ Custom modules (symlinked as apps/dcnet_apps)
│   ├── dcnet_apps/
│   └── dcnet_fixtures/          # 🎲 Sample data (see README.md inside)
└── docs/                        # 📚 Business documentation (NOT code)
    ├── feature/                 # ⭐ Requirements Specs (SOURCE OF TRUTH)
    ├── modules/                 # Module docs by STT (07-kho-hang/, 33-lead/, ...)
    │   └── {STT}-{slug}/       # technical-spec/, analysis/, implementation/, mockup/, user-guide/
    ├── accounting/              # ⭐ Hệ thống tài khoản kế toán (COA) - xem mục riêng bên dưới
    ├── erpnext-flows/           # ERPNext flow reference (19 analysis files)
    ├── customization/           # UI/UX customization log
    ├── roadmap/                 # Project timeline
    ├── plans/                   # Design docs + TODO tracking
    └── infrastructure/          # Cloud deployment planning
```

**3 Apps:** frappe (framework) + erpnext (dcnet_core symlink) + dcnet_apps (custom modules)

### 🐳 Docker Commands

**Container:** `devcontainer-frappe-1`

```bash
# Bench commands
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local [command]"

# Common: migrate, clear-cache, run-tests
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local run-tests --app dcnet_apps --module [module] -v"

# Generate fixtures
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local dcnet-fixtures generate --module [module]"
```

### ⚠️ Common Issues

| Issue | Fix |
|-------|-----|
| Desktop Icon không hiển thị | Thiếu Workspace Sidebar → tự động fix bởi `install.py` sau migrate |
| Workspace bị ẩn sau migrate | Thêm workspace vào whitelist trong `install.py` |
| Module cũ còn trong DB | `bench execute 'frappe.delete_doc("Module Def", "Old Name", force=True)'` |

### 📐 Shared File Rules (avoid merge conflicts)

> **CRITICAL:** These rules prevent merge conflicts when multiple developers work in parallel.
> Every developer and AI agent MUST follow these rules.
>
> **Tham khảo chính thức:**
> - [Frappe Hooks API](https://docs.frappe.io/framework/user/en/python-api/hooks) — hooks.py là file duy nhất Frappe đọc per app
> - [Frappe App Structure](https://docs.frappe.io/framework/user/en/basics/apps) — cấu trúc app chuẩn (hooks.py, modules.txt)
> - [ERPNext hooks.py (reference)](https://github.com/frappe/erpnext/blob/develop/erpnext/hooks.py) — ví dụ thực tế từ ERPNext

#### Root-level shared files

| File | Rule | How to edit |
|------|------|-------------|
| `dcnet_apps/hooks.py` | ⚠️ **Single source of truth** — Frappe only reads this file | Add to correct `# === [MODULE] ===` section, coordinate with team |
| `dcnet_apps/install.py` | ⚠️ Root delegates to module functions | Add your module's install function call, don't add inline logic |
| `dcnet_apps/modules.txt` | ⚠️ Add new lines in **alphabetical order** | Easier conflict resolution |
| `dcnet_apps/patches.txt` | ⚠️ Each module owns its own `patches/` folder | Root file just lists paths |

> **Why root hooks.py?** Frappe framework reads hooks as Python variables (`fixtures`, `doc_events`, `scheduler_events`) from **one root file per app** ([docs](https://docs.frappe.io/framework/user/en/python-api/hooks)). Module-level hooks.py files are NOT loaded by Frappe. Using `import *` would cause variables to override each other. See [ERPNext hooks.py](https://github.com/frappe/erpnext/blob/develop/erpnext/hooks.py) as reference — even with 40+ modules, ERPNext uses a single monolithic hooks.py.

#### hooks.py — section-based organization

```python
# dcnet_apps/hooks.py — SINGLE SOURCE OF TRUTH
# Frappe only reads this file. Do NOT create module-level hooks.py expecting Frappe to load them.
#
# Rules:
# 1. Each section is labeled with # === [MODULE NAME] === comments
# 2. When adding hooks for your module, add to the correct section
# 3. Coordinate with team before editing (this file is a merge conflict hotspot)
# 4. Keep entries sorted alphabetically within each section

# === FIXTURES ===
fixtures = [
    # [Core] Custom Fields & Property Setters
    {"doctype": "Custom Field", "filters": [["dt", "in", [...]]]},
    {"doctype": "Property Setter", "filters": [["doc_type", "in", [...]]]},
    # [EInvoice] — owner: @developer_a
    # [HTKK] — owner: @developer_b
]

# === DOC EVENTS ===
doc_events = {
    # [EInvoice]
    "Sales Invoice": {
        "on_submit": "dcnet_apps.einvoice.events.on_si_submit",
    },
}

# === SCHEDULER EVENTS ===
scheduler_events = {
    # [Module] — add cron/daily/hourly tasks here
}
```

#### install.py — modular delegation

```python
# dcnet_apps/install.py — root delegates to module install functions
from dcnet_apps.einvoice.install import after_install as einvoice_install
from dcnet_apps.htkk.install import after_install as htkk_install

def after_install():
    setup_core()        # Core setup (currency, desk icons, etc.)
    einvoice_install()  # EInvoice module setup
    htkk_install()      # HTKK module setup
```

#### Workspace sidebar JSON files — ownership rules

| Rule | Detail |
|------|--------|
| ✅ Only the module owner edits their workspace JSON | E.g., only stock module dev touches `stock.json` |
| ❌ NEVER edit another module's workspace JSON | Coordinate with the owner if changes are needed |

#### Module isolation principle

| Rule | Detail |
|------|--------|
| ✅ Each developer owns only files inside their module folder | `dcnet_apps/dcnet_apps/{your_module}/` |
| ✅ Module code (controllers, API, services) lives in module folder | `{your_module}/api.py`, `{your_module}/events.py` |
| ✅ Root `install.py` calls module install functions | Explicit imports, no inline logic |
| ⚠️ Root `hooks.py` is shared — edit your section only | Use `# === [MODULE] ===` comments to mark ownership |
| ❌ NEVER use `from module.hooks import *` in root hooks.py | Frappe variables would override each other |

---

## 🌿 Git Flow

> **Chi tiết:** `docs/git-flow.md`

**Simplified Git Flow:** `main` (production) ← PR ← `develop` (tích hợp) ← PR ← `feature/*` (dev)

| Nhánh | Quy tắc |
|-------|---------|
| `main` | Chỉ nhận PR từ `develop` (bàn giao) hoặc `hotfix/*` |
| `develop` | Chỉ nhận PR từ `feature/*` hoặc `fix/*` |
| `feature/{STT}-{tên}` | Tạo từ `develop`, merge về `develop` qua PR |
| `fix/{STT}-{tên}` | Bug fix nhỏ, tạo từ `develop` |
| `hotfix/{tên}` | Lỗi production, tạo từ `main`, merge cả `main` + `develop` |

**Commit message:** Conventional Commits — `{type}({STT}): {mô tả}` (VD: `feat(02): add dashboard reports`)

**Hàng ngày:** `git pull develop` → `git rebase develop` trên feature branch → làm việc → push cuối ngày

**QUAN TRỌNG khi tạo branch mới cho feature:**
```bash
git checkout develop && git pull origin develop
git checkout -b feature/{STT}-{tên}
```

---

## 🎲 Sample Data Fixtures

> **Full docs:** `dcnet_apps/dcnet_fixtures/README.md`

```bash
bench --site [site] dcnet-fixtures generate                    # All data
bench --site [site] dcnet-fixtures generate --module [module]  # Specific module
bench --site [site] dcnet-fixtures status                      # Check status
bench --site [site] dcnet-fixtures clear --force               # Clear all
```

**Modules:** `master`, `leads`, `customers`, `suppliers`, `opportunities`, `sales-orders`, `purchase-orders`, `fitting`

---

## 📁 Documentation & Workflow

### Development Workflow — `/dcnet-start {STT}`

> **Master orchestrator** điều phối toàn bộ workflow từ task start → done.
> Dùng `/dcnet-start {STT}` để bắt đầu, `--resume` để tiếp tục, `--status` để xem tiến độ.

| Phase | Tên | Skills sử dụng | Output |
|:-----:|-----|----------------|--------|
| 0 | Assessment | — | Dashboard + Feature List + Related Modules |
| 1 | Clarify | `/dcnet-interview` | Requirements rõ ràng |
| 2 | Documentation | `/dcnet-module`, `/dcnet-ba`, `/dcnet-mockup` | SPEC_MAPPING, BA, Mockup |
| 3 | Planning | `superpowers:writing-plans` | `docs/plans/` or `docs/modules/{STT}-{slug}/` |
| 4 | Implementation | `superpowers:TDD`, `superpowers:executing-plans`, `dcnet_quality` | Code trong `dcnet_apps/` |
| 5 | Review & Verify | `superpowers:requesting-code-review`, `superpowers:verification-before-completion` | Code review passed |
| 6 | Ship & Document | `superpowers:finishing-branch`, `/dcnet-guide` | PR/merge + User Guide |

**Tracker file:** `docs/modules/{STT}-{slug}/WORKFLOW_TRACKER.md` — persist progress across sessions.

**Quick ref:**
1. `/dcnet-start 07` — bắt đầu module mới (auto-detect phase phù hợp)
2. `/dcnet-start 07 --resume` — tiếp tục từ checkpoint cuối
3. `/dcnet-start 07 --status` — xem tiến độ (feature list + related modules + phase progress)

### Module Documentation Standard (Spec-First, ERPNext-Mapped)

```
docs/modules/{STT}-{slug}/
├── README.md                  # Luôn có — tổng quan, milestone, tiến độ
├── SPEC_MAPPING.md            # ⭐ Luôn có — spec → ERPNext mapping (file chính)
├── CLARIFY.md                 # Nếu có vấn đề cần hỏi khách
├── CUSTOM_REQUIREMENTS.md     # Nếu có phần cần custom (EXT/NEW)
├── analysis/                  # Phân tích sâu (module phức tạp)
├── workflow/                  # ⭐ So sánh luồng ERPNext vs khách hàng
│   ├── erpnext.md             # Reference kỹ thuật thuần ERPNext
│   └── nhatminh.md            # Luồng theo specs (bảng ✅/❌/🔧 + chi tiết)
├── technical-spec/            # Spec kỹ thuật chi tiết (nếu cần)
├── mockup/                    # HTML prototypes (nếu cần)
└── user-guide/                # HDSD tiếng Việt
```

> **SPEC_MAPPING.md là file chính** — map TỪNG feature spec → ERPNext, dùng đúng số spec khách hàng.
> Chi tiết cấu trúc: xem `docs/modules/README.md`

#### Tags trong SPEC_MAPPING

| Tag | Nghĩa | Action |
|-----|--------|--------|
| `USE` | ERPNext có sẵn, dùng ngay | Config + test |
| `CFG` | ERPNext có, cần config/setup | Setup data, settings, permissions |
| `EXT` | ERPNext có, cần mở rộng | Custom field, client/server script |
| `NEW` | ERPNext không có, cần build | Custom DocType, module mới |
| `REF` | Thuộc module khác | Tham chiếu |

#### Quy tắc quan trọng

- **Dùng đúng số feature spec** (VD: 4.1.1, 4.1.2) — KHÔNG tự đặt feature ID riêng
- **Không thêm, không bớt, không gộp** features so với spec gốc
- **CLARIFY.md**: Priority icons :red_circle: Critical | :orange_circle: High | :yellow_circle: Medium | :green_circle: Resolved
- **CUSTOM_REQUIREMENTS.md**: Chỉ tạo khi có features tag `EXT` hoặc `NEW`

### UI/UX Customization

All UI changes MUST be documented in `docs/customization/`. See `docs/customization/README.md` for template and process.

---

## 📚 Reference Documents

### Gap Analysis

- ⭐ **ERPNext Coverage Analysis:** `docs/feature/ERPNEXT_COVERAGE_ANALYSIS.md` — ~120 có sẵn (51%) / ~117 cần build mới (49%)
- Module Gap Analysis (21 modules): `docs/erpnext-flows/MODULE_GAP_ANALYSIS.md`

### Competitor Analysis (in `docs/competitor-analysis/`)

- ⭐ **MISA AMIS Quy Trình:** `docs/competitor-analysis/misa-amis/quy-trinh/ANALYSIS.md` — Process/Workflow Management, 26 tính năng so sánh vs ERPNext
- ⭐ **MISA AMIS HRM:** `docs/competitor-analysis/misa-amis/hrm/ANALYSIS.md` — Nhân sự (9 sub-systems), 42 tính năng so sánh vs ERPNext

### ERPNext Flow Reference (in `docs/erpnext-flows/`)

Lead→SO | Product Variants | Shipment (Viettel Post) | Loyalty Program | SO Ecosystem | Pricing Wholesale/Retail

---

## 🏦 Kế toán - Phần khó nhất của dự án

> **CRITICAL:** Kế toán là module phức tạp nhất, bàn giao T5 (30/05/2026), gồm 9 sub-modules (STT 22-30), 20 features (ERP-ACC-001→020). Đọc kỹ `docs/accounting/COA_ANALYSIS.md` trước khi làm bất kỳ gì liên quan kế toán.

### Tài liệu kế toán (`docs/accounting/`)

| File | Mô tả |
|------|-------|
| `COA_ANALYSIS.md` | ⭐ **Phân tích chi tiết COA vs specs khách hàng** (834 dòng) |
| `ChartOfAccountsImporter_v1_original.csv` | File COA gốc (244 TK) - KHÔNG SỬA file này |
| `ChartOfAccountsImporter_v2.csv` | File COA đã sửa (254 TK) - dùng để import |

### Hệ thống tài khoản (Chart of Accounts)

- **Chuẩn:** Thông tư 200/2014/TT-BTC (⚠️ conflict với ERP spec ghi TT99 — cần clarify)
- **Đồng tiền:** VND (base), multi-currency ở cấp giao dịch
- **Giá vốn:** ERPNext hỗ trợ FIFO / Moving Average (⚠️ khách yêu cầu "trung bình tháng" — cần clarify)
- **Khấu hao:** Đường thẳng (straight-line)

### Thay đổi chính v1 → v2

| Loại | Số lượng | Chi tiết |
|------|:--------:|---------|
| Sửa Account Type | 14 TK | Stock, Fixed Asset, Depreciation, CWIP, Round Off... |
| Sửa Currency | 3 TK | 1112, 1122, 1132: USD → VND |
| Sửa Parent | 2 TK | 2118 (→211), 3339 (→333) |
| **TK mới thêm** | 10 TK | 4119 (Round Off), 6329 (Stock Adjustment), 1565 (Trade-in), 51111/51112 (DT buôn/lẻ), 6351-6353 (CP tài chính), 8111-8112 (CP khác) |

### Luồng GL Entry quan trọng

```
Bán hàng:  SI submit → Nợ 131 (Debtors), Có 5111 (DT), Có 33311 (VAT) + Nợ 632, Có 1561 (COGS)
Mua hàng:  PI submit → Nợ 1561 (Kho), Nợ 1331 (VAT), Có 331 (NCC)
Thu tiền:  PE submit → Nợ 1111/1121 (Cash/Bank), Có 131 (Debtors)
Chi tiền:  PE submit → Nợ 331 (NCC), Có 1111/1121 (Cash/Bank)
Kho:       SE submit → Stock Ledger → GL Entry (perpetual inventory)
```

### Vấn đề cần clarify với khách (⚠️)

1. **TT99 vs TT200** — ERP spec nói TT99, SRS nói TT200
2. **Giá vốn** — "Trung bình tháng" vs Moving Average (ERPNext không có trung bình tháng)
3. **Trade-in** — Giá cũ > giá mới → hoàn tiền chênh lệch?
4. **HĐĐT** — Tích hợp nhà cung cấp nào? (VNPT/Viettel/MISA/FPT)
5. **Phiếu thu/chi** — Theo mẫu TT200 hay format ERPNext?

### Lưu ý khi triển khai kế toán

- Trong ERPNext, các module 22-26 + 29 (Tiền, Mua, Bán, Công nợ, HTK, Thuế) là **1 khối thống nhất** — submit 1 invoice = tạo GL cho tất cả
- **KHÔNG tách rời** bàn giao từng module kế toán, phải test end-to-end
- Module 27 (Chi phí) + 28 (Tài sản) tương đối độc lập
- Module 30 (Tổng hợp + BC) phải làm cuối cùng
- Custom development cần thiết: Xuất HTKK, Print format phiếu thu/chi VN, tích hợp HĐĐT

---

## 🤖 Available Skills

### Knowledge Skills (auto-triggered)

| Skill | Domains | Trigger |
|-------|---------|---------|
| `frappe` | Framework Core, Desk UI, Integration, frappe-ui, Data Import, DocType, Testing, Service, App Structure, API, Bench Commands | frappe.*, DocType, bench, client script... |
| `erpnext` | Accounting, Assets, Buying, Selling, Stock, Manufacturing, Projects, Setup, CRM, Code Interpreter, Jinja, Whitelisted Methods, Errors & Permissions, Custom App, Controllers | Sales Order, Purchase Order, Stock Entry... |
| `dcnet_quality` | **Code Quality Orchestrator** — 28 skills, 5 layers (Syntax→Core→Impl→Errors→Agents). Client/Server Scripts, Controllers, hooks.py, Whitelisted, Jinja, Scheduler, Custom App, Database, Permissions, API. PR review & code validation. | review code, validate code, client script, server script, controller, hooks.py, frappe.whitelist, jinja, print format, scheduler, frappe.db, permissions, PR review |

### Code Quality Skills (`dcnet_quality`) — Chi tiết

> Source: [OpenAEC Foundation ERPNext Skills Package v1.2](https://github.com/OpenAEC-Foundation/ERPNext_Anthropic_Claude_Development_Skill_Package)
> Location: `.claude/skills/dcnet_quality/`

**Cách hoạt động:**
- **Auto-trigger khi viết code**: Claude detect keyword (VD: `frappe.call`, `hooks.py`, `@frappe.whitelist`) → tự load SKILL.md tương ứng → áp dụng patterns
- **PR Review / Code Validation**: Dùng `agents/erpnext-code-validator/` + error skills → sinh validation report (CRITICAL/WARNING/SUGGESTION)
- **Vague requirements**: Dùng `agents/erpnext-code-interpreter/` → chuyển yêu cầu mơ hồ → technical spec

**5 Layers:**

| Layer | Skills | Mô tả |
|-------|:------:|-------|
| Syntax | 8 | Foundation — cú pháp đúng cho từng loại code |
| Core | 3 | Cross-cutting — database, permissions, API |
| Implementation | 8 | Step-by-step workflows cho từng domain |
| Errors | 7 | Error handling patterns cho production |
| Agents | 2 | Code interpreter + code validator |

**Critical Rules (lỗi #1 khi AI sinh code ERPNext):**
- Server Script: **KHÔNG import** (`from frappe.utils import X` → dùng `frappe.utils.X()`)
- Server Script: **KHÔNG `self.`** → dùng `doc.field`
- Client Script: **KHÔNG `frappe.db.*`** → dùng `frappe.call()`
- Controller: **KHÔNG modify field trong `on_update`** → dùng `frappe.db.set_value()`

### User-Invocable Skills

| Skill | Purpose | Output |
|-------|---------|--------|
| `/dcnet-start {STT}` | ⭐ **Master orchestrator** — full workflow start→done (7 phases, coordinates all skills below + superpowers) | `WORKFLOW_TRACKER.md` + Dashboard |
| `/dcnet-module {STT}-{slug}` | Interactive module docs builder (brainstorm-style) | `docs/modules/{STT}-{slug}/` |
| `/dcnet-ba {STT}` | Business Analysis: BPMN, gap analysis, value stream, workflow comparison | `docs/modules/{STT}-{slug}/analysis/` + `workflow/` |
| `/dcnet-mockup {STT}` | Create UI mockup HTML prototypes | `docs/modules/{STT}-{slug}/mockup/` |
| `/dcnet-guide {STT}` | Generate Vietnamese user guides | `docs/modules/{STT}-{slug}/user-guide/` |
| `/dcnet-interview` | Socratic interview (clarify) + Lateral thinking (unstuck) | Requirements clarity |
| `/dcnet-merge [PR#...]` | Review, merge PRs vào develop, tổng hợp chức năng | Feature summary table |
| `/dcnet-release [version]` | Tạo PR develop→main, tag SemVer, GitHub Release với notes tiếng Việt | PR + Tag + Release |
| `/dcnet-competitor-analysis {platform} {module}` | Phân tích module đối thủ + ERPNext gap mapping | `docs/competitor-analysis/{platform}/{module}/ANALYSIS.md` |
| `/guide {module}` | Show implementation checklist with progress | Formatted checklist |
| `/frappe-academy [learn\|exercise\|quiz\|check]` | ⭐ **Interactive Frappe tutor** — 8 modules, 42 lessons, song ngữ Việt-Anh, thực hành trên devcontainer | `docs/learning/PROGRESS.md` |
| `/mermaid-doctor {file}` | Validate & fix Mermaid diagrams | In-place |

---

## 🧠 Knowledge Graph & Onboarding

### Knowledge Graph (`.understand-anything/`)

Codebase đã được phân tích và tạo knowledge graph tự động:

- **File:** `.understand-anything/knowledge-graph.json` (12.7 MB)
- **Phạm vi:** 4.267 files → 19.531 nodes (4.267 file, 14.420 function, 844 class) + 15.349 edges
- **7 layers:** ERPNext Core Business (1.938) | HRMS (933) | Patches (460) | Manufacturing (438) | Setup (381) | Custom DCNET (104) | Dev Tooling (13)
- **10-step guided tour:** Từ hooks.py → DocType → Kế toán → Invoice → Payment → Pricing → Custom modules
- **Dashboard:** Chạy `/understand-dashboard` để xem interactive visualization

**Cập nhật graph:** Chạy `/understand` — tự động detect incremental changes theo git commit.

### Tài Liệu Onboarding (`docs/ONBOARDING.md`)

Tài liệu hướng dẫn onboarding tiếng Việt cho thành viên mới:
- Tổng quan dự án & cấu trúc repo
- 7 tầng kiến trúc với mô tả chi tiết
- Các khái niệm quan trọng (DocType, hooks.py, GL Entry, TT200)
- Lộ trình 10 bước khám phá codebase
- Vùng code phức tạp (646 files "complex") + top "rồng"
- Hướng dẫn bắt đầu nhanh (Docker, bench, fixtures)

---

## 🎯 Current Status

> **⭐ Module Progress:** [`docs/modules/PROGRESS.md`](docs/modules/PROGRESS.md) — checklist tất cả 47 modules, cập nhật sau mỗi thay đổi.
> **Khi bắt đầu module mới, ĐỌC PROGRESS.md trước** để biết tình hình tổng thể.

**Completed:** SRS tách 2 file (TM + NM) | Docs restructure (STT-based modules) | Skill `/dcnet-module` | Project Reset Design | Cloud Infrastructure Plan | dcnet_fixtures | Desktop Icons customization | **COA Analysis + CSV v2** (kế toán) | **Knowledge Graph + Onboarding Guide**

**Module progress (T3):** 01 :white_check_mark: config | 02 :white_check_mark: full (docs + code) | 03-06 :x: chưa làm

**Module docs (format cũ, cần update):** 07, 09, 12, 14, 33, 34, 35, 38, 40

**Design docs:** `docs/plans/`

**Next Steps (Trước khi ký HĐ):**
1. [ ] Khách confirm timeline T3-T8
2. [ ] Khách confirm cung cấp server trước 01/07
3. [ ] Khách cung cấp access BRAVO trước **01/05**

**Next Steps (Trước 10/03):**
1. [ ] Finalize team 5 người
2. [ ] Setup development environment
3. [ ] Review ERPNext base modules
4. [ ] Hoàn thành docs T3: modules 03, 04, 05, 06

---

**Last Updated:** 21/03/2026
