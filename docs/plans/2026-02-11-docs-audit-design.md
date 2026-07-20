# Docs Audit & Restructure Design

> **Brainstorm date:** 11/02/2026
> **Status:** COMPLETE
> **Scope:** Restructure docs/modules/, rename docs/analysis/, tao skill /dcnet-module, update references
> **Completed:** Sections 1-7 da thuc hien. Con lai: review noi dung 9 modules + update 4 skills phu (lam dan khi can)

---

## 1. Context

### Van de hien tai

- `docs/modules/` dung **5-file legacy format** (SPEC, WORKFLOW, DIAGRAMS, STATUS, USE_CASE_SPEC) — khong khop voi skill `/dcnet-module` (3-file format)
- Cau truc folder theo ten module (lead, fitting, ...) — khong co thu tu, kho tracking theo milestone
- `docs/analysis/` chua 2 loai tai lieu khac nhau: ERPNext flow reference + module gap analysis
- `docs/implementation/` tach rieng khoi module docs — kho lien ket
- Skill `/generate-module-docs` rigid (batch, 4-file) — can interactive brainstorm-style

### Muc tieu

- Cau truc docs/modules/ theo **STT ban giao** (01-51), de sort va tracking
- Moi module = 1 folder, ben trong chia **subfolder theo loai tai lieu**
- Phan biet ro `docs/erpnext-flows/` (tham khao ERPNext) vs module analysis/ (gap analysis)
- Tao skill `/dcnet-module` interactive (hoi-dap tung buoc, giong brainstorming)
- Linh hoat: module don gian chi can README + gap.md, module phuc tap thi day du

---

## 2. Cau truc moi docs/modules/

### 2.1. Naming convention

```
{STT:02d}-{slug}/
```

- STT: 2 chu so, theo bang ban giao (project-reset-design.md Section 2)
- Slug: ten viet tat, tieng Viet khong dau, dung `-` ngan cach

### 2.2. Danh sach STT day du

#### T3: Ban giao 31/03/2026

| STT | Slug | Module | TM | NM |
|-----|------|--------|:--:|:--:|
| 01 | dang-nhap | Dang nhap/Dang xuat + nen tang | V | V |
| 02 | dashboard | Dashboard | V | V |
| 03 | san-pham | Quan ly San pham | V | V |
| 04 | nha-cung-cap | Danh muc nha cung cap | V | V |
| 05 | mua-hang | Mua hang | V | V |
| 06 | bao-cao-phan-tich | Bao cao Phan tich | V | V |

#### T4: Ban giao 30/04/2026

| STT | Slug | Module | TM | NM |
|-----|------|--------|:--:|:--:|
| 07 | kho-hang | Quan ly Kho hang | V | V |
| 08 | bao-cao-kho | Bao cao Kho | V | V |
| 09 | don-hang | Quan ly Don hang | V | V |
| 10 | ban-buon | Ban buon | V | V |
| 11 | ban-le | Ban le | V | V |
| 12 | ban-hang | Quan ly Ban hang | V | V |
| 13 | danh-muc-ban-hang | Danh muc Ban hang | V | V |
| 14 | trade-in | Don hang Thu cu Doi moi | V | V |
| 15 | chi-nhanh | Quan ly Chi nhanh | V | V |
| 16 | nhan-vien | Quan ly Nhan vien | V | V |
| 17 | khach-hang | Quan ly Khach hang | V | V |
| 18 | bao-cao-don-hang | Bao cao Don hang | V | V |
| 19 | bao-cao-quan-tri | Bao cao Quan tri | V | V |
| 20 | bao-cao-nhan-vien | Bao cao Nhan vien | V | V |
| 21 | bao-cao-khach-hang | Bao cao Khach hang | V | V |
| 22 | bao-cao-doanh-so | Bao cao Doanh so | V | V |

#### T5: Ban giao 30/05/2026

| STT | Slug | Module | TM | NM |
|-----|------|--------|:--:|:--:|
| 23 | ke-toan-tien | Ke toan Tien | V | V |
| 24 | ke-toan-mua-hang | Ke toan Mua hang | V | V |
| 25 | ke-toan-ban-hang | Ke toan Ban hang | V | V |
| 26 | ke-toan-cong-no | Ke toan Cong no | V | V |
| 27 | ke-toan-hang-ton | Ke toan Hang ton kho | V | V |
| 28 | chi-phi-ho-tro | Chi phi & Ho tro | V | V |
| 29 | tai-san-ccdc | Tai san & CCDC | V | V |
| 30 | ke-toan-thue | Ke toan Thue | V | V |
| 31 | ke-toan-tong-hop | Ke toan Tong hop | V | V |
| 32 | bao-cao-tong-hop | Bao cao Tong hop | V | V |

#### T6: Ban giao 30/06/2026

| STT | Slug | Module | TM | NM |
|-----|------|--------|:--:|:--:|
| 33 | lead | Quan ly Lead | V | V |
| 34 | fitting | Quan ly Fitting | V | V |
| 35 | coaching | Quan ly Coaching | V | X |
| 36 | cai-dat | Cai dat he thong | V | V |
| 37 | cskh | Cham soc KH tu dong | V | V |
| 38 | tich-diem | Quan ly tich diem | X | V |
| 39 | don-hang-nang-cao | Don hang nang cao | V | V |
| 40 | giao-van | Tich hop Giao van | V | V |
| 41 | role-permission | Role & Permission | V | V |
| 42 | report-website | Report Website | X | V |
| 43 | web-dong-bo | Web & Dong bo | X | V |
| 44 | kiem-soat | Kiem soat | V | V |

#### T7: Thang 7/2026

| STT | Slug | Module | TM | NM |
|-----|------|--------|:--:|:--:|
| 45 | migrate-bravo | Migrate du lieu BRAVO | V | V |
| 46 | server-setup | Cai dat Server Khach | V | V |
| 47 | ban-giao | Ban giao, chuyen server | V | V |
| 48 | dao-tao | Dao tao, huong dan | V | V |

#### T8: Thang 8/2026

| STT | Slug | Module | TM | NM |
|-----|------|--------|:--:|:--:|
| 49 | membership | Membership | V | X |
| 50 | du-bao-doanh-thu | Du bao doanh thu | V | X |
| 51 | workshop | Workshop/Event | V | X |

### 2.3. Cau truc ben trong moi module

```
docs/modules/07-kho-hang/
├── README.md              # Tong quan: mo ta, milestone, trang thai, links
├── technical-spec/        # DocType definitions, field lists, API, ERD
├── analysis/              # Gap analysis + workflow analysis rieng module
├── implementation/        # Ke hoach trien khai, UI plan
├── mockup/                # HTML prototypes
└── user-guide/            # HDSD tieng Viet (cho end-user)
```

**Quy tac:**
- Folder chi tao khi bat dau lam module do (KHONG tao 51 folder rong)
- Subfolder chi tao khi co noi dung
- README.md luon tao dau tien khi bat dau module
- Module don gian co the chi can: README.md + analysis/gap.md
- Module phuc tap: day du tat ca subfolders

### 2.4. README.md template

```markdown
# {STT} - {Ten module}

| Item | Value |
|------|-------|
| STT | {STT} |
| Milestone | {T3/T4/T5/T6/T7/T8} ({ngay}) |
| Cong ty | {TM + NM / TM only / NM only} |
| Nguon spec | {FEATURE_SPECIFICATION.md Section X / ERP_SPECIFICATION.md Section Y} |
| Status | {Chua bat dau / Dang lam / Hoan thanh} |

## Tien do

- [ ] Gap Analysis
- [ ] Technical Spec
- [ ] Implementation Plan
- [ ] UI Mockup
- [ ] Code
- [ ] Test
- [ ] User Guide
```

---

## 3. Rename docs/analysis/ → docs/erpnext-flows/

### Ly do

`docs/analysis/` chua 19 files phan tich **luong ERPNext goc** (reference). Khac voi `analysis/` trong moi module (gap analysis cu the).

### Doi ten

```
docs/analysis/  →  docs/erpnext-flows/
```

Noi dung giu nguyen, chi doi ten folder.

### Danh sach files (19 files)

- ACCOUNTING_SPEC_VS_DCNET_FLOW_ANALYSIS.md
- ACCOUNTING_WORKFLOW.md
- ERPNEXT_CRM_MODULE_ANALYSIS.md
- FITTING_COACHING_TRADEIN_EXTENSION_DESIGN.md
- FITTING_COACHING_WORKFLOW_BUILDER.md
- FRAPPE_HOOKS_SYSTEM_WORKFLOW.md
- LEAD_TO_SALES_ORDER_WORKFLOW.md
- LOYALTY_WORKFLOW_ANALYSIS.md
- MEMBERSHIP_WORKFLOW.md
- MODULE_GAP_ANALYSIS.md
- NOTIFICATION_SYSTEM_WORKFLOW.md
- PRICING_WHOLESALE_RETAIL_WORKFLOW.md
- PRODUCT_VARIANT_WORKFLOW.md
- ROLES_AND_PERMISSIONS_ANALYSIS.md
- SALES_ORDER_ECOSYSTEM_WORKFLOW.md
- SELLING_MODULE_WORKFLOW.md
- SHIPMENT_WORKFLOW.md
- VALUE_ADDED_SERVICES_WORKFLOW.md
- VIETNAM_ACCOUNTING_GAP_ANALYSIS.md

---

## 4. Skill /dcnet-module

### 4.1. Thiet ke

**Ten:** `/dcnet-module`
**Style:** Interactive brainstorm (hoi-dap tung buoc, 1 cau moi lan)
**Muc dich:** Huong dan user tao docs cho 1 module, tu doc context roi hoi confirm/bo sung

### 4.2. Flow

```
/dcnet-module 07-kho-hang
    |
    +-- Buoc 1: Doc context
    |   +-- Doc spec goc (docs/feature/) -> trich phan lien quan
    |   +-- Doc ERPNext flows (docs/erpnext-flows/) neu co
    |   +-- Check folder da ton tai chua
    |
    +-- Buoc 2: Tao README.md (hoi confirm)
    |   +-- "Module nay thuoc milestone T4, TM+NM, dung khong?"
    |
    +-- Buoc 3: Gap Analysis (hoi tung muc)
    |   +-- "ERPNext Stock module da co X, Y, Z -- du chua?"
    |   +-- "Can custom them gi?"
    |   +-- "Co van de gi can luu y?"
    |
    +-- Buoc 4: Technical Spec (hoi neu can)
    |   +-- "Can custom DocType moi khong?"
    |   +-- "API endpoints nao?"
    |   +-- Skip neu user noi "dung ERPNext goc"
    |
    +-- Buoc 5: Implementation Plan (hoi)
    |   +-- "Uu tien phan nao truoc?"
    |   +-- "Co dependency voi module nao?"
    |
    +-- Buoc 6: Summary
        +-- Hien checklist da tao nhung gi, con thieu gi
```

### 4.3. Dac diem

- Hoi 1 cau moi lan (giong superpowers:brainstorming)
- Prefer multiple choice khi co the
- Tu doc ERPNext (dung erpnext skills) truoc khi hoi
- Skip buoc neu module don gian — user noi "skip" hoac "dung goc"
- Khong bat buoc tao du tat ca files
- Tu dong dung AskUserQuestion cho cau hoi

### 4.4. Tan dung tu skill cu /generate-module-docs

**Giu lai:**
- `references/source-mapping.md` — update theo STT moi (1-51)
- `references/mermaid-validation.md` — van valid, giu nguyen
- `assets/technical-spec.template.html` — template HTML cho customer
- Source detection logic

**Bo:**
- 4-file output format → subfolder-based
- Batch mode → interactive
- Rigid checklist → flexible

### 4.5. Cau truc skill

```
.claude/skills/dcnet-module/
├── SKILL.md                              # Main skill definition
├── references/
│   ├── source-mapping.md                 # Module -> spec mapping (updated STT)
│   └── mermaid-validation.md             # Mermaid diagram rules
└── assets/
    └── technical-spec.template.html      # HTML template
```

---

## 5. Migration plan — Docs hien tai

### 5.1. Module docs legacy (12 folders, 6-file format)

| Folder hien tai | STT moi | Hanh dong |
|----------------|---------|-----------|
| docs/modules/lead/ | 33-lead | Move + restructure |
| docs/modules/fitting/ | 34-fitting | Move + restructure |
| docs/modules/coaching/ | 35-coaching | Move + restructure |
| docs/modules/tradein/ | 14-trade-in | Move + restructure |
| docs/modules/loyalty/ | 38-tich-diem | Move + restructure |
| docs/modules/shipping/ | 40-giao-van | Move + restructure |
| docs/modules/warehouse/ | 07-kho-hang | Move + restructure |
| docs/modules/pricing/ | 12-ban-hang (subset) | Move + restructure |
| docs/modules/order/ | 09-don-hang | Move + restructure |
| docs/modules/credit-management/ | 26-ke-toan-cong-no (subset) | Move + restructure |
| docs/modules/import-management/ | (cross-module) | Move + restructure |
| docs/modules/nhatminh-connect/ | 43-web-dong-bo | Move + restructure |

**Luu y:** accounting/ (empty) — xoa

### 5.2. Implementation docs

| Folder hien tai | Di chuyen vao |
|----------------|---------------|
| docs/implementation/lead/ | docs/modules/33-lead/implementation/ |
| docs/implementation/fitting/ | docs/modules/34-fitting/implementation/ |
| docs/implementation/aggregate/ | Xoa (empty) |
| docs/implementation/reports/ | Xoa (empty) |

Sau khi migrate xong: xoa `docs/implementation/` (chi giu README neu can)

### 5.3. User guide

| File hien tai | Di chuyen vao |
|---------------|---------------|
| docs/user-guide/CRM_LEAD_USER_GUIDE.md | docs/modules/33-lead/user-guide/ |

### 5.4. Mockups

| Folder hien tai | Di chuyen vao |
|----------------|---------------|
| docs/mockups/coaching/ | docs/modules/35-coaching/mockup/ |

---

## 6. Cleanup

### 6.1. Xoa folders/files

- `docs/modules/accounting/` (empty)
- `docs/implementation/aggregate/` (empty)
- `docs/implementation/reports/` (empty)
- `docs/examples/` (empty)
- `docs/customization/integration/` (empty)

### 6.2. Giu nguyen (khong thay doi)

- `docs/feature/` — source of truth, giu nguyen
- `docs/contract/` — SRS da tach xong
- `docs/infrastructure/` — cloud plan
- `docs/kickoff/` — onboarding materials
- `docs/architecture/` — system architecture
- `docs/customization/` — UI changes log (tru integration/ empty)
- `docs/roadmap/` — TIMELINE_2026.md
- `docs/plans/` — design documents

---

## 7. Update references

### 7.1. CLAUDE.md

- Doi `docs/analysis/` → `docs/erpnext-flows/`
- Doi docs/modules/ structure description
- Doi skill `/generate-module-docs` → `/dcnet-module`
- Doi `docs/implementation/` → note da migrate vao modules

### 7.2. Cac skills can review

| Skill | Can update | Ly do |
|-------|-----------|-------|
| `/guide` | Co | Output path thay doi |
| `/plan-implementation` | Co | Output path → docs/modules/XX/implementation/ |
| `/user-guide-generator` | Co | Output path → docs/modules/XX/user-guide/ |
| `/analyze-workflow` | Co | Output path → docs/erpnext-flows/ hoac docs/modules/XX/analysis/ |
| `/mermaid-doctor` | Khong | Path-agnostic, van dung |
| `/generate-module-docs` | Xoa | Thay the boi /dcnet-module |

### 7.3. docs/modules/README.md

Viet lai hoan toan — index theo STT, link den tung folder, hien thi status

---

## 8. Thu tu thuc hien

### Nhom A: Restructure docs/modules/ (Core) — DA XONG

- [x] A1. Tao cau truc folder moi (9 modules da co docs)
- [x] A2. Migrate 9/12 module docs legacy → cau truc moi (3 modules giu lai vi tri cu)
- [x] A3. Migrate implementation docs (lead, fitting) → module folders
- [x] A4. Migrate user-guide, mockups → module folders
- [x] A5. Tao README.md cho docs/modules/ (index tong)
- [x] A6. Xoa folders cu sau migrate

### Nhom B: Rename & Cleanup — DA XONG

- [x] B1. Rename docs/analysis/ → docs/erpnext-flows/
- [x] B2. Xoa empty dirs (examples, accounting, aggregate, reports, integration)

### Nhom C: Tao skill /dcnet-module — DA XONG

- [x] C1. Tao SKILL.md (interactive brainstorm-style)
- [x] C2. Migrate references tu /generate-module-docs
- [x] C3. Update source-mapping.md theo STT moi (51 modules)
- [x] C4. Xoa skill cu /generate-module-docs

### Nhom D: Update references — DA XONG

- [x] D1. Update CLAUDE.md
- [x] D2. Update skill /guide — updated 10/03/2026 (docs/analysis → docs/erpnext-flows, /analyze-workflow → /dcnet-ba)
- [x] D3. Xoa skill /plan-implementation (overlap voi /dcnet-module)
- [x] D4. Update skill /user-guide-generator — replaced by /dcnet-guide, updated /guide ref 10/03/2026
- [x] D5. Xoa skill /analyze-workflow (output da rename, overlap voi /dcnet-module)
- [x] D6. Viet lai docs/modules/README.md

---

## 9. Ghi chu

- Module docs hien tai dung **5-file legacy** (SPEC, WORKFLOW, DIAGRAMS, STATUS, USE_CASE_SPEC)
- Khi migrate: gop WORKFLOW + DIAGRAMS + STATUS → analysis/ hoac technical-spec/ tuy noi dung
- SPEC → giu lam reference trong technical-spec/
- USE_CASE_SPEC → giu trong technical-spec/
- Khong can migrate hoan hao — chi sap xep lai folder, noi dung giu nguyen
