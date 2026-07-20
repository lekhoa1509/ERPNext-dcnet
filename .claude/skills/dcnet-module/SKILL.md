---
name: dcnet-module
description: |
  Interactive module documentation builder for DCNET Flow.
  Guides user step-by-step through creating docs for a module (brainstorm-style).

  Use when:
  - User says "/dcnet-module {STT}" (e.g., "/dcnet-module 07")
  - User wants to create or update docs for a specific module
  - User says "tao docs cho module X", "bat dau module X"

  Output: docs/modules/{STT}-{slug}/ with subfolders as needed
---

# /dcnet-module — Interactive Module Documentation Builder

Build module docs step-by-step through guided questions. Each module gets a folder under `docs/modules/{STT}-{slug}/`.

## Quick Start

```bash
/dcnet-module 07              # Start new module docs (auto-resolve slug from source-mapping)
/dcnet-module 33 --update     # Update existing module docs
```

## Core Philosophy: Spec-First, ERPNext-Mapped

```
Khach hang yeu cau gi?  →  ERPNext da co gi?  →  Can lam them gi?
   (SPEC)                    (MAPPING)              (ACTION)
```

- **Dung dung so feature cua spec khach hang** (VD: 4.1.1, 4.1.2...) — KHONG tu dat feature ID rieng
- **Moi feature spec = 1 row** trong SPEC_MAPPING — khong them, khong bot
- **Tags ro rang**: `USE` / `CFG` / `EXT` / `NEW` / `REF`
- **Tach biet**: phan tich (SPEC_MAPPING) vs hanh dong (CUSTOM_REQUIREMENTS)

## Output Structure

```
docs/modules/{STT}-{slug}/
├── README.md                  # Luon co — tong quan + progress tracker
├── SPEC_MAPPING.md            # Luon co — spec → ERPNext mapping (file chinh)
├── CLARIFY.md                 # Neu co cau hoi can hoi khach
├── CUSTOM_REQUIREMENTS.md     # Neu co phan can custom (EXT/NEW)
├── analysis/                  # Neu can phan tich sau (module phuc tap)
├── technical-spec/            # Neu can spec ky thuat chi tiet
├── mockup/                    # Neu can thiet ke UI custom
└── user-guide/                # HDSD tieng Viet (cho end-user)
```

### Scale theo do phuc tap

| Loai module | Files can | Vi du |
|-------------|----------|-------|
| **Don gian** — ERPNext co san ~90% | README + SPEC_MAPPING | 15-chi-nhanh, 16-nhan-vien |
| **Trung binh** — can config + vai custom | + CLARIFY + CUSTOM_REQUIREMENTS | 09-don-hang, 17-khach-hang |
| **Phuc tap** — nhieu custom, nhieu ket noi | + analysis/ + mockup/ | 07-kho-hang, 12-ban-hang, ke toan |
| **Dac thu DCNET** — build moi hoan toan | Full set | 14-trade-in, 34-fitting, 40-giao-van |

---

## Process

### Step 0: Parse & Validate

1. Parse argument to get STT number (e.g., `07`, `33`, `02`)
2. Look up STT in [source-mapping.md](references/source-mapping.md) to get:
   - Slug, module name, milestone, company (TM/NM/both)
   - Source spec file and section
   - Also accept `{STT}-{slug}` format for backward compatibility
3. Module folder path: `docs/modules/{STT}-{slug}/`
4. Check if folder already exists
5. If exists and no `--update` flag: warn and ask to continue or skip
6. If `--update`: read existing files, preserve what's still valid, update to new structure

### Step 1: Read Context (automatic, no user input needed)

Read these files silently to build context:

1. **Source spec**: Read the relevant section from `docs/feature/{SOURCE_FILE}`
2. **ERPNext flows**: Check `docs/erpnext-flows/` for related analysis files
3. **ERPNext skills**: Use relevant erpnext/frappe skills to understand what ERPNext provides out of the box
4. **Existing module folder**: If updating, read current files to extract useful content

> Do NOT dump raw content to user. Summarize what you found internally.

### Step 2: Create README.md (ask user to confirm)

Present a summary and ask user to confirm:

```
Module: 07 - Quan ly Kho hang
Milestone: T4 (30/04/2026)
Cong ty: TM + NM
Nguon spec: ERP_SPECIFICATION.md Section 4
ERPNext base: Stock module (Warehouse, Stock Entry, Item, Batch, Serial No)
Spec features: 20 (Kho) + 5 (BC Kho) + 2 quy trinh dac biet
```

**Ask:** "Thong tin nay dung khong? Can bo sung gi?"

Then create `README.md`:

```markdown
# {STT} - {Ten module}

| Item | Value |
|------|-------|
| **STT** | {STT} |
| **Milestone** | {Milestone} |
| **Cong ty** | {TM + NM / TM only / NM only} |
| **Nguon spec** | {Source file} Section {X} |
| **ERPNext base** | {Modules/DocTypes ERPNext lien quan} |
| **Status** | Dang lam |

## Tien do

- [x] README
- [ ] SPEC_MAPPING.md
- [ ] CLARIFY.md
- [ ] CUSTOM_REQUIREMENTS.md
- [ ] BA Analysis (/dcnet-ba)
- [ ] Mockup (neu can)
- [ ] User Guide

## Tai lieu trong folder

| File | Mo ta |
|------|-------|
| `SPEC_MAPPING.md` | ⭐ Mapping spec khach hang → ERPNext |
| `CLARIFY.md` | Van de can clarify voi khach |
| `CUSTOM_REQUIREMENTS.md` | Tong hop phan can custom |
| `analysis/` | Phan tich sau (neu co) |
| `mockup/` | UI prototype (neu co) |

## Code Reference

> Code thuc te: `dcnet_apps/dcnet_apps/{module}/`
```

### Step 3: SPEC_MAPPING.md (core — automatic + interactive)

This is the **most important file**. Map EVERY feature in spec to ERPNext.

**Process:**
1. Read spec section carefully — list ALL features (e.g., 4.1.1 → 4.1.20, 4.2.1 → 4.2.5, 4.3.x)
2. For each feature, research what ERPNext provides
3. Assign tag: `USE` / `CFG` / `EXT` / `NEW` / `REF`
4. Ask user to confirm features that are ambiguous

**Tags definition:**

| Tag | Nghia | Action can lam | Effort |
|-----|--------|----------------|--------|
| `USE` | ERPNext co san, dung ngay | Config + test | 0-0.5 ngay |
| `CFG` | ERPNext co, can config/setup | Setup data, settings, permissions | 0.5-2 ngay |
| `EXT` | ERPNext co, can mo rong | Custom field, client/server script | 2-7 ngay |
| `NEW` | ERPNext khong co, can build | Custom DocType, module moi | 5-30 ngay |
| `REF` | Thuoc module khac, tham chieu | Link sang module do | 0 |

**Template SPEC_MAPPING.md:**

```markdown
# {STT} - {Ten module}: Spec → ERPNext Mapping

> **Nguon:** {SOURCE_FILE} Section {X}
> **ERPNext:** v16 — {Module name} (VD: Stock Module)
> **Cap nhat:** {date}

## Quy uoc Tags

| Tag | Nghia | Action |
|-----|--------|--------|
| `USE` | ERPNext co san, dung ngay | Config + test |
| `CFG` | ERPNext co, can config/setup | Setup data, settings, permissions |
| `EXT` | ERPNext co, can mo rong | Custom field, client/server script |
| `NEW` | ERPNext khong co, can build | Custom DocType, module moi |
| `REF` | Thuoc module khac | Tham chieu |

---

## {Spec section}. {Ten nhom} ({N} features)

### {Spec number}. {Ten feature}

- **Tag:** `{USE/CFG/EXT/NEW/REF}`
- **Spec yeu cau:** {Tom tat yeu cau tu spec goc}
- **ERPNext:** {DocType/Feature tuong ung, hoac "Khong co"}
- **ERPNext da co:** {Mo ta cu the ERPNext co gi}
- **Gap:** {Chenh lech giua spec va ERPNext, hoac "Khong co gap"}
- **Action:** {Hanh dong cu the can lam}
- **Effort:** {X ngay}
- **Dependency:** {Feature nao can lam truoc, neu co}
- **⚠️ Clarify:** {Link den CLARIFY.md neu co van de, neu khong thi bo dong nay}

{... lap lai cho moi feature ...}

---

## Tong hop

| Tag | So feature | Effort |
|-----|-----------|--------|
| `USE` | X | X ngay |
| `CFG` | X | X ngay |
| `EXT` | X | X ngay |
| `NEW` | X | X ngay |
| `REF` | X | 0 |
| **Tong** | **{N}** | **X ngay** |
```

**Rules khi tao SPEC_MAPPING:**

1. **Dung dung so spec** — Neu spec ghi 4.1.1 thi dung 4.1.1, KHONG tu dat WH-001
2. **Khong them feature** — Chi map features co trong spec. KHONG tu them
3. **Khong bot feature** — Moi feature trong spec PHAI co 1 entry. Neu overlap voi module khac, dung tag `REF`
4. **Khong gop feature** — Spec co 4.1.9, 4.1.10, 4.1.11 thi phai co 3 entries rieng, KHONG gop lai
5. **Spec la source of truth** — Ten feature theo spec, khong doi ten

### Step 3.5: CLARIFY.md (automatic)

After writing SPEC_MAPPING, scan for items that need customer clarification:
- Features where ERPNext approach differs significantly from spec requirement
- Conflicts between spec documents
- Missing details needed for implementation
- Phrases: "can clarify", "chua ro", "can xac nhan", "chon 1 trong 2"

If found (>= 1 item), create `CLARIFY.md`:

```markdown
# {STT} - {Ten module}: Van de can Clarify

> **Ngay tao:** {date}
> **Trang thai:** Cho khach hang xac nhan

---

## Quy uoc

| Icon | Y nghia |
|------|---------|
| :red_circle: | **Critical** — Block trien khai, can tra loi truoc khi code |
| :orange_circle: | **High** — Anh huong thiet ke, can tra loi truoc Sprint |
| :yellow_circle: | **Medium** — Co the dung gia tri mac dinh, confirm sau |
| :green_circle: | **Resolved** — Da co cau tra loi |

---

## {Chu de 1}

| # | Cau hoi | Priority | Anh huong | Tra loi | Nguon |
|---|---------|----------|-----------|---------|-------|
| 1.1 | {question} | :red_circle: Critical | {impact} | Recommend: {default} | {spec ref} |

---

## Thong ke

| Priority | So luong |
|----------|----------|
| :red_circle: Critical | X |
| :orange_circle: High | X |
| :yellow_circle: Medium | X |
| **Tong** | **X** |
```

**Rules:**
- Group questions by topic/domain
- Include "Recommend:" if you have a suggested default
- Reference spec feature number (e.g., "4.1.20 Tinh gia von")
- If 0 clarify items → skip creating file, note in README

### Step 3.7: BA Analysis (ask user — calls /dcnet-ba)

After SPEC_MAPPING and CLARIFY are written, offer BA analysis:

**Ask:** "Chay BA analysis (BPMN process + ERPNext workflow + Traceability)?"

Options: "Co, chay /dcnet-ba" / "Skip, lam sau"

If user chooses yes:
- Call `/dcnet-ba {STT}` skill (it reads SPEC_MAPPING from context)
- Output: `analysis/BA_ANALYSIS.md`
- After completion, continue to Step 4

If user chooses skip:
- Note in README: `- [ ] BA Analysis (chay /dcnet-ba {STT})`
- Continue to Step 4

> **Luu y:** User co the chay `/dcnet-ba {STT}` bat ky luc nao sau khi co SPEC_MAPPING.

### Step 4: CUSTOM_REQUIREMENTS.md (automatic — extract from SPEC_MAPPING)

Extract all features tagged `EXT` and `NEW` from SPEC_MAPPING into actionable format.

Only create if there are `EXT` or `NEW` features. If module is 100% `USE`/`CFG` → skip.

```markdown
# {STT} - {Ten module}: Custom Requirements

> Extract tu SPEC_MAPPING.md — chi phan can custom.
> Dung de plan execution va track tien do.

## Custom Fields (them vao DocType co san)

| DocType | Field | Type | Muc dich | Spec ref |
|---------|-------|------|----------|----------|
| {DocType} | custom_{name} | {Type} | {Purpose} | {4.x.x} |

## Custom DocTypes (tao moi)

| DocType | Module | Parent | Spec ref | Effort |
|---------|--------|--------|----------|--------|
| {Name} | DCNET {Module} | {Parent nếu child} | {4.x.x} | X ngay |

## Server Scripts / Hooks

| Hook | Trigger | Muc dich | Spec ref |
|------|---------|----------|----------|
| validate | {DocType} submit | {Purpose} | {4.x.x} |
| scheduled | Daily | {Purpose} | {4.x.x} |

## Client Scripts

| DocType | Event | Muc dich | Spec ref |
|---------|-------|----------|----------|
| {DocType} | {event} | {Purpose} | {4.x.x} |

## Custom Reports (Script Report)

| Report | Spec ref | Format | Effort |
|--------|----------|--------|--------|
| {Name} | {4.x.x} | {Description} | X ngay |

## Workflows

| DocType | States | Muc dich | Spec ref |
|---------|--------|----------|----------|
| {DocType} | {State list} | {Purpose} | {4.x.x} |

## Tong effort

| Hang muc | So luong | Effort |
|----------|---------|--------|
| Custom Fields | X | X ngay |
| Custom DocTypes | X | X ngay |
| Scripts | X | X ngay |
| Reports | X | X ngay |
| Workflows | X | X ngay |
| Testing | - | X ngay |
| **Tong** | | **X ngay** |
```

### Step 5: Analysis / Mockup (ask if needed)

**Ask:** "Module nay co can phan tich sau hon khong? (workflow phuc tap, ket noi nhieu module, etc.)"

Options: "Co, tao analysis/" / "Co, can mockup UI" / "Du roi, skip"

If analysis needed:
- Write focused analysis files in `analysis/` (e.g., workflow diagrams, integration mapping)
- Keep analysis files **specific** — 1 file per topic, not mega-files
- Reference SPEC_MAPPING feature numbers

If mockup needed:
- Note in README, user can run `/dcnet-mockup {STT}` separately

### Step 6: Summary

Present what was created:

```
Da tao cho module {STT}-{slug}:
  docs/modules/{STT}-{slug}/
  ├── README.md                    ← Tong quan + progress
  ├── SPEC_MAPPING.md              ← ⭐ {N} features mapped
  │   └── USE: X | CFG: X | EXT: X | NEW: X | REF: X
  ├── CLARIFY.md                   ← {N} van de can hoi khach
  └── CUSTOM_REQUIREMENTS.md       ← {N} items can custom

Con thieu:
  - BA Analysis → /dcnet-ba {STT}
  - Mockup → /dcnet-mockup {STT}
  - User Guide → /dcnet-guide {STT}

Buoc tiep theo:
  1. Review SPEC_MAPPING → dam bao khong thieu feature nao
  2. Gui CLARIFY.md cho khach hang
  3. Sau khi co confirm → tao execution plan (superpowers:writing-plans)
```

Update README.md checklist accordingly.

---

## Handling --update flag (existing modules)

When updating existing module docs to new structure:

1. Read ALL existing files in module folder
2. Extract useful content:
   - Feature lists → map to SPEC_MAPPING format
   - Gap analysis → merge into SPEC_MAPPING Gap/Action columns
   - Clarify items → keep in CLARIFY.md
   - Technical details → keep in analysis/ or CUSTOM_REQUIREMENTS
3. Create new files (SPEC_MAPPING.md, CUSTOM_REQUIREMENTS.md)
4. **DO NOT delete old files** — user will clean up manually after review
5. Mark old files as deprecated in README:
   ```
   ## Files cu (tham khao, se remove sau)
   - analysis/ERPNEXT_COVERAGE_GAP.md → replaced by SPEC_MAPPING.md
   ```

---

## Key Principles

- **Spec la source of truth** — Moi feature trong SPEC_MAPPING phai trace ve spec
- **1 cau hoi moi lan** — Khong hoi nhieu cau cung luc
- **Prefer multiple choice** — Dung AskUserQuestion voi options
- **Tu doc truoc khi hoi** — Doc spec + ERPNext truoc, chi hoi nhung gi can user input
- **Skip duoc** — Module don gian co the skip analysis/mockup
- **Khong bat buoc day du** — Chi tao files can thiet
- **Tags nhat quan** — USE/CFG/EXT/NEW/REF dung cho moi module

## Mermaid Diagram Rules

When generating diagrams, follow [mermaid-validation.md](references/mermaid-validation.md):

1. **State diagrams:** ASCII IDs only (no Vietnamese in IDs)
2. **Flowcharts:** Quote special characters (`:`, `=`, `{`, `}`, `<`, `>`)
3. **ERD:** No Unicode in field descriptions
4. **Line endings:** Unix (LF)
5. **Code fences:** Must be balanced

## Source Mapping

See [source-mapping.md](references/source-mapping.md) for complete STT → spec mapping.

## Error Handling

| Error | Solution |
|-------|----------|
| STT not found | Check source-mapping.md, suggest closest match |
| Spec section missing | Warn user, ask if they want to continue without spec |
| Module folder exists | If no --update flag: ask update or skip |
| ERPNext skill not available | Continue without ERPNext context, note in SPEC_MAPPING |
| Feature count mismatch | Count features in spec vs SPEC_MAPPING — must match exactly |
