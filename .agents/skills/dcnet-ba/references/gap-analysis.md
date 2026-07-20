# Gap Analysis Reference - ERPNext Migration

> Adapted from Gap Analysis methodology for BRAVO -> ERPNext migration context.
> Danh gia khoang cach giua he thong hien tai va ERPNext target.
> Dung khi can phan tich muc do phu hop cua ERPNext voi yeu cau spec khach hang.

---

## 1. Gap Analysis Framework for ERPNext

### Scope

| Aspect | Description |
|--------|-------------|
| **Current State (As-Is)** | BRAVO + quy trinh thu cong + Excel + giay to |
| **Target State (To-Be)** | ERPNext v16 + dcnet_apps custom modules |
| **Focus** | Feature spec -> ERPNext capability mapping |
| **2 cong ty** | Thang Long TM + Nhat Minh Sport (2 site rieng, code chung) |
| **Data migration** | BRAVO -> ERPNext (validate ke toan) |

### Gap Types mapping to SPEC_MAPPING Tags

| Tag | Gap Type | Complexity | Action | Vi du |
|-----|----------|------------|--------|-------|
| `USE` | No gap | None | Test + validate | Listing danh sach, standard CRUD |
| `CFG` | Configuration gap | Low | Setup, settings, permissions | Naming series, Print format, Role |
| `EXT` | Extension gap | Medium | Custom field, client/server script, report | Them truong, custom validation, Script Report |
| `NEW` | Capability gap | High | Custom DocType, new module | Trade-in, Fitting, Coaching |
| `REF` | Cross-module dependency | Varies | Coordinate with other module | Kho tham chieu tu Mua hang |

**Rules:**
- USE/CFG = ERPNext standard, khong can build, chi can config + test
- EXT = ERPNext co DocType, can mo rong (custom field, hook, report)
- NEW = ERPNext khong co, can build tu dau (Custom DocType, full module)
- REF = Thuoc module khac, chi reference, khong phan tich o day

---

## 2. Gap Analysis Workflow (5 Steps)

### Step 1: Document Current State (BRAVO As-Is)

**Muc tieu:** Hieu hien trang he thong cua khach.

| Aspect | BRAVO Capability | Limitation | Pain Points |
|--------|-----------------|------------|-------------|
| Quan ly kho | Nhap/xuat kho co ban | Khong real-time, khong multi-warehouse | Kiem ke lech, du lieu muon |
| Bao cao | Bao cao co dinh | Khong tuy chinh | Export Excel, tinh tay |
| Phe duyet | Email / giay | Khong tracking | Mat thoi gian, khong audit trail |

**Sources:**
- Feature specs (`docs/feature/*.md`)
- Interview notes (neu co)
- Screenshots BRAVO (neu co)

> **Luu y:** Neu khong co thong tin BRAVO -> ghi "Can xac nhan voi khach hang".
> Khong tu doan, khong suy luau ve he thong hien tai neu khong co bang chung.

### Step 2: Define Target State (ERPNext To-Be)

**Muc tieu:** Map moi feature spec sang ERPNext standard capability.

| Aspect | ERPNext DocType | Feature | Standard/Custom |
|--------|-----------------|---------|-----------------|
| Nhap kho | Purchase Receipt | Nhan hang tu PO, cap nhat Stock Ledger | Standard (USE) |
| Duyet PO | Workflow DocType | Approval states: Draft -> Pending -> Approved | Standard (CFG) |
| Trade-in | (Custom) Trade-in Entry | Nhan hang cu, tra hang moi, bu tien | Custom (NEW) |

**Automation points can ghi nhan:**
- Auto GL Entry khi submit Purchase Invoice / Sales Invoice
- Auto Stock Ledger Entry khi submit Purchase Receipt / Delivery Note / Stock Entry
- Auto Payment Reconciliation
- Workflow transition notifications

### Step 3: Identify Gaps

**Gap Inventory Table:**

| Gap ID | Spec # | Feature | Current (BRAVO) | Target (ERPNext) | Gap Description | Tag | Complexity | Risk |
|--------|--------|---------|-----------------|-------------------|-----------------|-----|------------|------|
| G01 | 3.1.1 | Tao PO | Nhap tay BRAVO | Purchase Order form | UX change only | USE | None | Low |
| G02 | 3.1.5 | Ship mode | Khong co | Custom field on PO | Them truong + validation | EXT | Medium | Low |
| G03 | 4.2.1 | Trade-in | Excel theo doi | Custom DocType | Build tu dau | NEW | High | High |

**Gap ID convention:** `G{sequence}` — dat theo thu tu trong SPEC_MAPPING.

### Step 4: Categorize & Prioritize Gaps

#### By Complexity

```
None (USE)  <  Low (CFG)  <  Medium (EXT)  <  High (NEW)
```

#### By Risk

| Risk Level | Criteria | Vi du |
|------------|----------|-------|
| **Low** | Isolated, khong anh huong module khac | Custom field, CSS change |
| **Medium** | Cross-module, can coordinate | Workflow anh huong nhieu role |
| **High** | Accounting/data integrity, loi = mat tien | GL Entry, Stock valuation, Tax |

#### By Timeline Priority

| Priority | Timeline | Gap types | Dac diem |
|----------|----------|-----------|----------|
| **Must** | T3-T4 | USE + CFG + EXT (core) | Khong co thi khong hoat dong duoc |
| **Should** | T5-T6 | EXT (important) + NEW (simple) | Quan trong nhung co workaround |
| **Could** | T7-T8 | NEW (complex) + nice-to-have | Co the delay, khong block go-live |

### Step 5: Gap Resolution Options

**Voi moi gap loai EXT hoac NEW, phai de xuat resolution options:**

```markdown
## Gap: G{N} - {Feature Name}

**Spec:** {Spec #} | **Tag:** {EXT/NEW} | **Risk:** {Low/Medium/High}

### Current State (BRAVO)
[Mo ta cach lam hien tai — hoac "Khong co thong tin, can xac nhan"]

### Target State (ERPNext)
[Mo ta cach lam mong muon tren ERPNext]

### Resolution Options

#### Option A: {Mo rong DocType co san}
- **Approach:** Custom field + client script tren {DocType}
- **Effort:** X ngay
- **Pros:** Tan dung ERPNext standard, de maintain, upgrade-safe
- **Cons:** Gioi han boi DocType co san
- **ERPNext DocType:** {ten DocType}

#### Option B: {Custom DocType moi}
- **Approach:** Tao DocType moi trong dcnet_apps
- **Effort:** X ngay
- **Pros:** Linh hoat, khong bi rang buoc
- **Cons:** Nhieu effort, can maintain rieng

### Recommendation
[Chon option nao va ly do]
[Tham chieu ERPNext standard de justify]

### Dependencies
[Modules/gaps khac phai resolve truoc]
[VD: Gap G05 can module Kho (07) hoan thanh truoc]
```

**Rules:**
- Luon uu tien Option A (extend) truoc Option B (custom)
- Chi chon NEW khi ERPNext thuc su khong co DocType nao phu hop
- Tham khao `docs/erpnext-flows/MODULE_GAP_ANALYSIS.md` de check ERPNext capability

---

## 3. DCNET-Specific Gap Categories

### 3.1 Data Migration Gaps

> BRAVO -> ERPNext data mapping la rui ro lon nhat cua du an.

| Loai gap | Mo ta | Vi du | Action |
|----------|-------|-------|--------|
| Field mapping | Truong BRAVO khong co trong ERPNext | Ma hang BRAVO vs Item Code ERPNext | Custom field hoac transform |
| Data type | Kieu du lieu khac nhau | BRAVO text vs ERPNext Link field | Data cleansing script |
| Code mapping | Ma/ID he thong khac nhau | Chart of Accounts BRAVO vs ERPNext COA | Mapping table |
| Historical data | Du lieu lich su can migrate | SO/PO/Invoice cu | Import tool + validate |
| Master data | Du lieu chu can dong bo | Customer, Supplier, Item | Priority migrate truoc |

**Luu y:**
- COA mapping: xem `docs/accounting/COA_ANALYSIS.md` (834 dong phan tich chi tiet)
- Item code mapping: can quy uoc moi voi khach
- Customer/Supplier code: BRAVO -> ERPNext naming series

### 3.2 Process Gaps

| Loai gap | Mo ta | Loi ich khi fix |
|----------|-------|-----------------|
| Manual -> Automated | Viec lam tay chuyen sang tu dong | Giam sai sot, tang toc do |
| Paper -> Digital | Giay to -> form dien tu | Tracking, audit trail |
| Approval workflow | Email/giay -> ERPNext Workflow | Theo doi realtime, khong that lac |
| Reporting | Bao cao co dinh -> Report Builder + Script Report | Tuy chinh, realtime |
| Multi-location | 1 kho -> multi-warehouse | Quan ly ton kho chinh xac |

**ERPNext Workflow DocType:**
```
Draft -> Pending Approval -> Approved -> Submitted
                          -> Rejected -> Draft (quay lai chinh sua)
```

### 3.3 Integration Gaps

| He thong | Muc do gap | Ghi chu |
|----------|-----------|---------|
| HDDT (e-invoice) | High | Can tich hop NCC (VNPT/Viettel/MISA/FPT) — chua confirm |
| Bank integration | Medium | API ngan hang hoac import file |
| POS hardware | Medium | Barcode scanner, receipt printer |
| Viettel Post | Low-Medium | API shipment tracking (co ERPNext Shipment) |
| SMS/Zalo | Low | Notification channels |

> **Luu y:** HDDT la gap lon nhat ve integration. Chua co thong tin NCC nao khach chon.
> Ghi vao CLARIFY.md: ":red_circle: Can xac nhan NCC HDDT"

### 3.4 Compliance Gaps

| Yeu cau | ERPNext Standard | Gap | Action |
|---------|-----------------|-----|--------|
| TT200 Chart of Accounts | Co template VN | Thieu mot so TK dac thu | Custom COA (da lam v2) |
| HTKK export (bao cao thue) | Khong co | Can build | NEW — Script Report + export |
| Phieu thu/chi format VN | Print format co ban | Khong dung mau VN | EXT — Custom Print Format |
| Phieu nhap/xuat kho mau VN | Print format co ban | Khong dung mau VN | EXT — Custom Print Format |
| Multi-currency (VND base) | Co | Can config dung | CFG — Currency settings |

> **Conflict can clarify:** ERP spec ghi TT99, SRS ghi TT200. Hien dang lam theo TT200.

---

## 4. Gap Summary Template

Dung template nay o cuoi moi BA_ANALYSIS.md hoac SPEC_MAPPING.md:

```markdown
### Gap Summary

| Category | Count | USE | CFG | EXT | NEW | REF |
|----------|-------|-----|-----|-----|-----|-----|
| Total features | X | X | X | X | X | X |
| No gap (ready) | X | | | | | |
| Config gap | X | | | | | |
| Extension gap | X | | | | | |
| Capability gap | X | | | | | |

### Risk Heat Map

|               | Low (CFG) | Medium (EXT) | High (NEW) |
|---------------|-----------|--------------|------------|
| **Low risk**    | :green_circle: Green   | :yellow_circle: Yellow  | :orange_circle: Orange |
| **Medium risk** | :yellow_circle: Yellow  | :orange_circle: Orange  | :red_circle: Red     |
| **High risk**   | :orange_circle: Orange  | :red_circle: Red       | :red_circle: Red     |

### Resolution Effort Estimate

| Tag | Avg effort/feature | Total features | Total effort |
|-----|-------------------|----------------|--------------|
| USE | 0.5 ngay (test only) | X | X ngay |
| CFG | 1-2 ngay | X | X ngay |
| EXT | 3-5 ngay | X | X ngay |
| NEW | 5-15 ngay | X | X ngay |
| **Total** | | **X** | **X ngay** |
```

**Effort estimate rules:**
- USE: chi test, khong code -> 0.5 ngay
- CFG: setup + test -> 1-2 ngay
- EXT: custom field + script + test -> 3-5 ngay
- NEW: design + code + test -> 5-15 ngay (tuy do phuc tap)
- Buffer: +20% cho moi module (unexpected issues)

---

## 5. Gap-to-Timeline Mapping

### DCNET Timeline 2026

| Timeline | Gap Priority | Modules | Focus |
|----------|-------------|---------|-------|
| **T3** (31/03) | Must - Core | 01-06 | Dashboard, San pham, NCC, Mua hang, BC Phan tich |
| **T4** (30/04) | Must - Operations | 07-17 | Kho, Don hang, Ban buon/le, Ban hang, Trade-in, Chi nhanh, NV, KH |
| **T5** (30/05) | Must - Accounting | 22-30 | 9 sub-modules ke toan (Tien, Mua, Ban, Cong no, HTK, Chi phi, Tai san, Thue, Tong hop) |
| **T6** (30/06) | Should - CRM/Service | 33-41 | Lead, Fitting, Coaching, CSKH, Tich diem, Giao van |
| **T7** | Migration | - | Data migration BRAVO -> ERPNext, setup server |
| **T8** | Could - Advanced | 42-47 | Membership, Du bao DT, Workshop |

### Mapping rules

- **T3-T4 gaps:** Phai resolve truoc, khong co workaround
- **T5 (ke toan):** Phuc tap nhat, 9 modules la 1 khoi thong nhat, test end-to-end
- **T6 gaps:** Co the co workaround tam (VD: tracking bang Excel cho den khi module xong)
- **T8 gaps:** Nice-to-have, chi lam neu con thoi gian

### 2 cong ty — Gap differences

| Gap | Thang Long TM | Nhat Minh Sport | Ghi chu |
|-----|---------------|-----------------|---------|
| Coaching | Co | Khong | TM only |
| Tich diem | Khong | Co | NM only |
| Workshop | Co | Khong | TM only |
| Membership | Co | Khong | TM only |
| Du bao DT | Khong | Co | NM only |

> Chi tiet: `docs/plans/2026-02-10-project-reset-design.md`

---

## 6. Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| **Over-customizing** | Build custom khi ERPNext co standard | Check ERPNext standard TRUOC, chi custom khi that su can |
| **Ignoring data migration** | Chi focus features, quen data | Plan data mapping song song voi feature dev |
| **Single-module thinking** | Gap chi anh huong 1 module | Check cross-module impact (VD: Kho anh huong Ke toan) |
| **Gold plating gaps** | Them feature khi fix gap | Chi fix dung nhung gi spec yeu cau, khong them |
| **Underestimating accounting** | Coi ke toan nhu module binh thuong | Ke toan = 9 sub-modules lien ket, phai test end-to-end |
| **Skipping BRAVO analysis** | Khong hieu he thong cu | Du lieu migrate se sai neu khong hieu BRAVO structure |
| **Assuming gap = custom** | Thay gap la phai build moi | Nhieu gap chi can config (CFG) hoac extend nhe (EXT) |

---

## 7. Gap Analysis Checklist

Dung checklist nay de dam bao gap analysis day du:

```markdown
### Pre-Analysis
- [ ] Doc SPEC_MAPPING.md cua module
- [ ] Doc MODULE_GAP_ANALYSIS.md (docs/erpnext-flows/)
- [ ] Check ERPNext standard features cho DocTypes lien quan
- [ ] Xac dinh BRAVO As-Is (neu co thong tin)

### Analysis
- [ ] List tat ca features tu spec
- [ ] Map moi feature -> ERPNext capability
- [ ] Gan tag (USE/CFG/EXT/NEW/REF) cho moi feature
- [ ] Xac dinh gap cho EXT va NEW
- [ ] De xuat resolution options cho moi gap
- [ ] Danh gia risk va complexity

### Post-Analysis
- [ ] Gap Summary table hoan chinh
- [ ] Risk Heat Map
- [ ] Effort estimate
- [ ] Timeline mapping
- [ ] Cross-module dependencies identified
- [ ] Items can clarify voi khach -> CLARIFY.md
- [ ] Review voi team
```

---

## 8. Cross-Reference

| Document | Muc dich | Location |
|----------|---------|----------|
| SPEC_MAPPING.md | Feature -> ERPNext mapping (input chinh) | `docs/modules/{STT}-{slug}/SPEC_MAPPING.md` |
| MODULE_GAP_ANALYSIS.md | ERPNext gap analysis tong hop 21 modules | `docs/erpnext-flows/MODULE_GAP_ANALYSIS.md` |
| COA_ANALYSIS.md | Gap analysis he thong tai khoan ke toan | `docs/accounting/COA_ANALYSIS.md` |
| BA_ANALYSIS.md | Output cua /dcnet-ba (chua gap summary) | `docs/modules/{STT}-{slug}/analysis/BA_ANALYSIS.md` |
| CUSTOM_REQUIREMENTS.md | Chi tiet cho EXT/NEW features | `docs/modules/{STT}-{slug}/CUSTOM_REQUIREMENTS.md` |
| CLARIFY.md | Cac van de can hoi khach hang | `docs/modules/{STT}-{slug}/CLARIFY.md` |
| ba-methodology.md | Phuong phap BA tong quat | `.claude/skills/dcnet-ba/references/ba-methodology.md` |
