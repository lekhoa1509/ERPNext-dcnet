---
name: dcnet-guide
description: |
  Generate professional Vietnamese user guides for DCNET Flow modules.
  Output: docs/modules/{STT}-{slug}/user-guide/

  Use when:
  - User asks "/dcnet-guide {STT}" (e.g., "/dcnet-guide 07")
  - User asks to create user guide/manual for a module
  - User says "tao tai lieu huong dan", "viet user guide", "tao manual"
  - User wants documentation for customer training

  Triggers: "user guide", "huong dan su dung", "tai lieu", "manual", "HDSD"
---

# /dcnet-guide — User Guide Generator for DCNET Flow

Generate professional Vietnamese user guides for modules. Output to module docs folder.

## Usage

```bash
/dcnet-guide 02                # Auto-resolve: STT 02 → 02-dashboard
/dcnet-guide 07                # Auto-resolve: STT 07 → 07-kho-hang
```

## Output

```
docs/modules/{STT}-{slug}/user-guide/
└── USER_GUIDE.md
```

## Process

### Step 1: Resolve Module

1. Parse argument → get STT number
2. Look up STT in source mapping at `../dcnet-module/references/source-mapping.md` → get slug, module name
3. Also accept `{STT}-{slug}` format for backward compatibility
4. Module folder path: `docs/modules/{STT}-{slug}/`
5. Read module docs: `README.md`, `analysis/gap.md`, `technical-spec/`, `mockup/`
6. Read source spec if available (`docs/feature/`)
7. If no module docs: warn, suggest `/dcnet-module {STT}` first

### Step 2: Gather Module Information

Before writing, collect:

```
1. Module schema: dcnet_core/ or dcnet_apps/ (find relevant doctype)
2. Business logic: {doctype}.py
3. UI logic: {doctype}.js
4. Spec requirements: docs/feature/* (check relevant files)
5. Module docs: docs/modules/{STT}-{slug}/* (gap analysis, technical spec, mockup)
```

### Step 3: Generate User Guide

Write `docs/modules/{STT}-{slug}/user-guide/USER_GUIDE.md` following the structure below.

### Step 4: Update Module README

Check User Guide in the module's `README.md` checklist.

## Document Structure

```markdown
# Huong Dan Su Dung Module {MODULE_NAME}

> **He thong:** DCNET Flow
> **Phien ban:** 1.0 | **Ngay:** {DATE}
> **Doi tuong:** {TARGET_AUDIENCE}

## Muc Luc
1. Gioi Thieu
2. Truy Cap Module
3. Danh Sach {Entity}
4. Tao {Entity} Moi
5. Xem Chi Tiet
6. Cap Nhat
7. Tuong Tac
8. Chuyen Doi/Workflow
9. Import/Export
10. Bao Cao
11. Cau Hoi Thuong Gap
+ Phu Luc (Phim tat, Glossary)
```

## Section Guidelines

| Section | Must Include |
|---------|--------------|
| **Gioi Thieu** | Definition, lifecycle diagram (ASCII), status table |
| **Truy Cap** | Menu path, search method, shortcuts |
| **Danh Sach** | List view mockup, search/filter/sort instructions |
| **Tao Moi** | Form mockup, required/optional fields tables |
| **Xem Chi Tiet** | Detail view mockup, tabs description |
| **Cap Nhat** | Edit workflow, status change, owner change |
| **Tuong Tac** | Comments, attachments, email, tasks |
| **Workflow** | Conversion paths diagram, step-by-step |
| **Import/Export** | Template, format table, error handling |
| **Bao Cao** | Available reports, filters, export |
| **FAQ** | 10+ common Q&A |
| **Phu Luc** | Shortcuts table, glossary |

## Writing Style

- Vietnamese, formal but friendly
- Address user as "ban"
- Imperative form: "Click vao...", "Nhap..."
- Explain technical terms in glossary

## ASCII Diagram Templates

### List View
```
┌─────────────────────────────────────────────────────────────────────────┐
│ {Entity}                                       [+ Add {Entity}] [Menu ▼]│
├─────────────────────────────────────────────────────────────────────────┤
│ [🔍 Search...]  [Edit Filters]  [Save Filter]                           │
├─────────────────────────────────────────────────────────────────────────┤
│ □ │ ID           │ Name        │ Status     │ Owner      │ Created     │
├───┼──────────────┼─────────────┼────────────┼────────────┼─────────────┤
│ □ │ XXX-0001     │ Example 1   │ Open       │ user@...   │ 29/01/2026  │
└───┴──────────────┴─────────────┴────────────┴────────────┴─────────────┘
```

### Form View
```
┌─────────────────────────────────────────────────────────────────────────┐
│ New {Entity}                                                    [Save]  │
├─────────────────────────────────────────────────────────────────────────┤
│ ═══ SECTION NAME ═══════════════════════════════════════════════════   │
│ Field 1*:       [_______________]     Field 2:     [_______________]    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Workflow
```
┌─────────────────────────────────────────────────────────────────────────┐
│                         WORKFLOW TITLE                                   │
├─────────────────────────────────────────────────────────────────────────┤
│   ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌──────────┐ │
│   │ Step 1 │───▶│ Step 2 │───▶│ Step 3 │───▶│ Step 4 │───▶│  Final   │ │
│   └────────┘    └────────┘    └────────┘    └────────┘    └──────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Table Formats

### Fields Table
```markdown
| Truong | Loai | Bat buoc | Mo ta | Vi du |
|--------|------|----------|-------|-------|
| **field_name** | Data | Co | Description | Example |
```

### Status Table
```markdown
| Trang thai | Y nghia | Khi nao su dung |
|------------|---------|-----------------|
| **Open** | Dang xu ly | Khi bat dau lam viec |
```

### Shortcuts Table
```markdown
| Phim tat | Chuc nang |
|----------|-----------|
| `Ctrl + B` | Tao moi (New) |
| `Ctrl + S` | Luu (Save) |
| `Ctrl + E` | Chinh sua (Edit) |
| `Ctrl + G` | Di den (Go to) |
| `/` | Mo Search |
| `Esc` | Dong/Huy |
```

## Footer Template

```markdown
---

**Document Version:** 1.0
**Created:** {DATE}
**Last Updated:** {DATE}
**Author:** DCNET Team

---

*© 2026 DCNET Telecom. All rights reserved.*
```

## Quality Checklist

Before finalizing:
- [ ] All 11 sections present
- [ ] Vietnamese throughout
- [ ] Technical terms explained
- [ ] ASCII diagrams render correctly
- [ ] Tables formatted properly
- [ ] 10+ FAQ items
- [ ] Shortcuts included
- [ ] Glossary complete

## Module-Specific Notes

| Module Type | Focus Areas |
|-------------|-------------|
| **CRM** (Lead, Customer) | Conversion workflows, pipeline, status auto-updates |
| **Sales** (Quotation, SO) | Pricing, items table, payment terms |
| **Inventory** (Stock) | Movement types, warehouse, batch/serial |
| **Services** (Fitting, Coaching) | Appointment flow, service terminology |

## Principles

- **Bam sat module docs** — Doc gap analysis + technical spec truoc khi viet
- **Thuc te** — Dung data mau tieng Viet, kich ban kinh doanh thuc
- **Day du** — 11 sections + FAQ + Phu luc
- **Doc lap** — User doc duoc ma khong can ho tro ky thuat
