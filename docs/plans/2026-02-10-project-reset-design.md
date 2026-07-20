# Project Reset Design - DCNET Flow

> **Brainstorm date:** 10/02/2026
> **Status:** COMPLETE
> **Completed:** All sections (1-7)
> **Thuc hien tiep:** Da hoan tat tat ca. Commit + push.

---

## 1. Context - Ly do Reset

- **Scope thay doi:** Thu tu uu tien module thay doi hoan toan (Operations-first thay vi CRM-first)
- **2 cong ty:** TM va Nhat Minh, 2 site rieng, code chung, 2 HĐ rieng
- **Timeline moi:** Ban giao theo thang T3 (31/03) → T4 (30/04) → T5 (30/05) → T6 (30/06) + T7 + T8
- **Team:** 5 nguoi (Duc, Phuong, Cuong, Dat, Hau)
- **Tech:** Frappe + ERPNext moi nhat, tan dung ERPNext toi da, custom app cho modules dac thu
- **SRS:** 2 file rieng (TM + NM), brand "DCNET" (KHONG mention ERPNext/Frappe)
- **Specs goc:** Van valid (FEATURE_SPECIFICATION.md, ERP_SPECIFICATION.md), chi thay doi thu tu uu tien

---

## 2. Timeline Moi (Tu Excel khach hang)

### Truoc 30/06: TAT CA modules → Ca 2 cong ty (TM + NM)

### T3: BAN GIAO 31/03/2026

| STT | Module | TM | NM | Ghi chu |
|-----|--------|:--:|:--:|---------|
| 1 | Dang nhap/Dang xuat + nen tang | V | V | |
| 2 | Dashboard | V | V | |
| 3 | Quan ly San pham | V | V | Can data BRAVO |
| 4 | Danh muc nha cung cap | V | V | Can data BRAVO |
| 5 | Mua hang | V | V | |
| 6 | Bao cao Phan tich | V | V | |

### T4: BAN GIAO 30/04/2026

| STT | Module | TM | NM | Ghi chu |
|-----|--------|:--:|:--:|---------|
| 7 | Quan ly Kho hang | V | V | Can data BRAVO |
| 8 | Bao cao Kho | V | V | |
| 9 | Quan ly Don hang | V | V | Can data BRAVO |
| 10 | Ban buon | V | V | Can data BRAVO |
| 11 | Ban le | V | V | Can data BRAVO |
| 12 | Quan ly Ban hang | V | V | KH ban hang, chiet khau, tra lai, thuong DS, voucher, bang gia |
| 13 | Danh muc Ban hang | V | V | Can data BRAVO |
| 14 | Don hang Thu cu Doi moi | V | V | Bao gom Trade-in tich hop |
| 15 | Quan ly Chi nhanh | V | V | Can data BRAVO |
| 16 | Quan ly Nhan vien | V | V | Can data BRAVO |
| 17 | Quan ly Khach hang | V | V | Can data BRAVO |
| 18 | Bao cao Don hang | V | V | |
| 19 | Bao cao Quan tri | V | V | |
| 20 | Bao cao Nhan vien | V | V | |
| 21 | Bao cao Khach hang | V | V | |
| 22 | Bao cao Doanh so | V | V | |

### T5: BAN GIAO 30/05/2026

| STT | Module | TM | NM | Ghi chu |
|-----|--------|:--:|:--:|---------|
| 22 | Ke toan Tien | V | V | Can data BRAVO |
| 23 | Ke toan Mua hang | V | V | Can data BRAVO |
| 24 | Ke toan Ban hang | V | V | Can data BRAVO |
| 25 | Ke toan Cong no | V | V | Can data BRAVO |
| 26 | Ke toan Hang ton | V | V | Can data BRAVO |
| 27 | Chi phi & Ho tro | V | V | Can data BRAVO |
| 28 | Tai san & CCDC | V | V | Can data BRAVO |
| 29 | Ke toan Thue | V | V | Can data BRAVO |
| 30 | Ke toan Tong hop | V | V | Can data BRAVO |
| 31 | Bao cao Tong hop | V | V | |

### T6: BAN GIAO 30/06/2026 — Co phan tach

| STT | Module | TM | NM | Ghi chu |
|-----|--------|:--:|:--:|---------|
| 32 | Quan ly Lead | V | V | |
| 33 | Quan ly Fitting | V | V | Bao gom Fitting tich hop |
| 34 | Quan ly Coaching | V | X | Bao gom Coaching tich hop |
| 35 | Cai dat he thong | V | V | |
| 36 | Cham soc KH tu dong | V | V | |
| 37 | Quan ly tich diem | X | V | Quy tac tinh diem/len hang |
| 38 | Don hang nang cao | V | V | Bao hanh, bao tri |
| 39 | Tich hop Giao van | V | V | Viettel Post, GHTK |
| 40 | Role & Permission | V | V | |
| 41 | Report Website | X | V | |
| 42 | Web & Dong bo | X | V | |
| 43 | Kiem soat | V | V | |

### T7: THANG 7/2026

| STT | Module | TM | NM | Ghi chu |
|-----|--------|:--:|:--:|---------|
| 44 | Migrate du lieu BRAVO | V | V | Lay trong khoang time muon kiem tra |
| 45 | Cai dat Server Khach | V | V | |
| 46 | Ban giao, chuyen server | V | V | Co the lui T8 neu day #49-51 vao dau T7 |
| 47 | Dao tao, huong dan | V | V | |

### T8: THANG 8/2026 — Phat sinh sau hop C.Linh 3/2/2026

| STT | Module | TM | NM | Ghi chu |
|-----|--------|:--:|:--:|---------|
| 49 | Membership | V | X | Quan ly goi/the, QR check-in, nang/ha hang |
| 50 | Du bao doanh thu | V | X | Canh bao hut doanh so |
| 51 | Workshop/Event | V | X | Don hang dich vu, tag workshop/event |

### Tong ket phan tach

- **TM only (NM khong co):** Coaching (#34), Membership (#49), Du bao (#50), Workshop (#51)
- **NM only (TM khong co):** Tich diem (#37), Report Website (#41), Web & Dong bo (#42)

---

## 3. Docs Cleanup - DA THUC HIEN

### Da xoa (commit cbf1653):

- `docs/examples/remotion-sales-report/` - node_modules committed vao git
- `docs/processes/` - SDLC generic docs
- `docs/recruitment/` - Interview materials
- `docs/modules/ai/` - AI strategy (post go-live)
- `docs/tramy/` - Personal workspace
- `docs/translations/` - CRM glossary
- `docs/PROJECT_ORGANIZATION.md`, `docs/TODO_ERPNEXT_TRANSLATION.md`

### CLAUDE.md da slim: 707 → 203 dong

---

## 4. Docs Audit - CON LAI

| Folder | Danh gia | Hanh dong |
|--------|----------|-----------|
| `docs/feature/` (3 specs + 3 gaps) | GIU | Source of truth, van valid |
| `docs/modules/` (12 folders x 6 files) | GIU | Business docs van dung |
| `docs/analysis/` (18 files) | GIU | Reference ky thuat |
| `docs/implementation/` (lead + fitting) | GIU | Implementation plans |
| `docs/mockups/coaching/` | GIU | UI prototypes |
| `docs/infrastructure/` | GIU | Cloud plan |
| `docs/customization/` | GIU | UI changes log |
| `docs/kickoff/` | GIU | Onboarding materials |
| `docs/user-guide/` | GIU | Dung khi toi T6 |
| `docs/contract/` | **LAM LAI** | Tach 2 SRS (TM + NM) |
| `docs/roadmap/` | **THAY THE** | Tao TIMELINE_2026.md moi |
| `CLAUDE.md` | **CAP NHAT** | Them info tu brainstorm |

---

## 5. Action Items - CHUA THUC HIEN

### 5.1. Tao TIMELINE_2026.md moi — DA XONG
- [x] Tao `docs/roadmap/TIMELINE_2026.md` thay the file cu
- [x] Theo dung format Excel (chia theo cty, T3-T8)
- [x] Mapping module → spec goc (FEATURE_SPECIFICATION / ERP_SPECIFICATION section)

### 5.2. Tach SRS thanh 2 file — THIET KE CHI TIET

**Approach:** 2 file hoan chinh rieng biet (khong dung base + overlay)

**Ly do:** Day la tai lieu hop dong — moi khach can ban rieng, chuyen nghiep, khong thay thong tin cua ben kia.

#### 5.2.1. Cau truc thu muc

```
docs/contract/
├── DCNET_SRS_TM.md              (moi - ban day du cho Thang Long TM)
├── DCNET_SRS_NM.md              (moi - ban day du cho Nhat Minh Sport)
├── DCNET_FLOW_SRS.md            (XOA sau khi tach xong)
├── DIEU_6_NGHIEM_THU_BAN_GIAO.md  (giu nguyen, dung chung)
├── appendix/
│   ├── tm/
│   │   ├── A_FEATURE_MATRIX.md
│   │   ├── B_ERD_DIAGRAMS.md
│   │   ├── C_WORKFLOW_DIAGRAMS.md
│   │   └── D_PERMISSION_MATRIX.md
│   └── nm/
│       ├── A_FEATURE_MATRIX.md
│       ├── B_ERD_DIAGRAMS.md
│       ├── C_WORKFLOW_DIAGRAMS.md
│       └── D_PERMISSION_MATRIX.md
```

#### 5.2.2. Header thay doi

| Field | TM | NM |
|-------|----|----|
| Khach hang | Cong ty TNHH Thang Long TM | Cong ty TNHH Nhat Minh Sport |
| Tai lieu so | PHU LUC SO 02 - Hop dong DCNET-TLTM | PHU LUC SO 02 - Hop dong DCNET-NMS |
| Brand | DCNET Flow (KHONG mention ERPNext/Frappe/Python/MariaDB) | DCNET Flow |

Section 2.2 Kien truc: Mo ta generic (Web Application, Database) thay vi specific tech stack.

#### 5.2.3. Section 3 — Sap xep theo MILESTONE (khong theo chuc nang)

**DCNET_SRS_TM.md:**

```
3. YEU CAU CHUC NANG

--- T3: BAN GIAO 31/03/2026 ---
3.1  Dang nhap & Nen tang
3.2  Dashboard
3.3  Quan ly San pham
3.4  Danh muc Nha cung cap
3.5  Mua hang
3.6  Bao cao Phan tich

--- T4: BAN GIAO 30/04/2026 ---
3.7  Quan ly Kho hang
3.8  Bao cao Kho
3.9  Quan ly Don hang
3.10 Ban buon
3.11 Ban le
3.12 Quan ly Ban hang (KH ban hang, chiet khau, tra lai, thuong DS, voucher, bang gia)
3.13 Danh muc Ban hang
3.14 Don hang Thu cu Doi moi (Trade-in)
3.15 Quan ly Chi nhanh
3.16 Quan ly Nhan vien
3.17 Quan ly Khach hang
3.18 Bao cao Don hang
3.19 Bao cao Quan tri
3.20 Bao cao Nhan vien
3.21 Bao cao Khach hang
3.22 Bao cao Doanh so

--- T5: BAN GIAO 30/05/2026 ---
3.23 Ke toan Tien
3.24 Ke toan Mua hang
3.25 Ke toan Ban hang
3.26 Ke toan Cong no
3.27 Ke toan Hang ton kho
3.28 Chi phi & Ho tro
3.29 Tai san & CCDC
3.30 Ke toan Thue
3.31 Ke toan Tong hop
3.32 Bao cao Tong hop

--- T6: BAN GIAO 30/06/2026 ---
3.33 Quan ly Lead
3.34 Quan ly Fitting
3.35 Quan ly Coaching                    ★ TM only
3.36 Cai dat he thong
3.37 Cham soc KH tu dong
3.38 Don hang nang cao (bao hanh, bao tri)
3.39 Tich hop Giao van (Viettel Post, GHTK)
3.40 Role & Permission
3.41 Kiem soat

--- T8: THANG 8/2026 ---
3.42 Membership                          ★ TM only
3.43 Du bao Doanh thu                    ★ TM only
3.44 Workshop/Event                      ★ TM only
```

**DCNET_SRS_NM.md:** (Giong TM nhung T6 thay doi)

```
--- T6: BAN GIAO 30/06/2026 ---
3.33 Quan ly Lead
3.34 Quan ly Fitting
3.35 Cai dat he thong
3.36 Cham soc KH tu dong
3.37 Quan ly tich diem (Loyalty)         ★ NM only
3.38 Don hang nang cao (bao hanh, bao tri)
3.39 Tich hop Giao van (Viettel Post, GHTK)
3.40 Role & Permission
3.41 Report Website                      ★ NM only
3.42 Web & Dong bo                       ★ NM only
3.43 E-commerce (Shopee/TikTok/Lazada)   ★ NM only
3.44 Messaging (Zalo/Messenger)          ★ NM only
3.45 Kiem soat
```

(NM KHONG co: Coaching, Membership, Du bao DT, Workshop/Event)

#### 5.2.4. Phan bo modules

**CHUNG (T3-T5 + phan lon T6):**
- T3: 6 modules (Dang nhap, Dashboard, San pham, NCC, Mua hang, BC Phan tich)
- T4: 16 modules (Kho, Don hang, Ban buon/le, Ban hang, Trade-in, Chi nhanh, NV, KH, Bao cao x5)
- T5: 10 modules (Ke toan x9, BC Tong hop)
- T6 chung: Lead, Fitting, Cai dat, CSKH, Don hang NC, Giao van, Role, Kiem soat

**TM only (4 modules):**
| Module | Milestone | Ghi chu |
|--------|-----------|---------|
| Coaching | T6 | Quan ly HLV, goi hoc, san tap, lich hoc, diem danh |
| Membership | T8 | Quan ly goi/the, QR check-in, nang/ha hang |
| Du bao Doanh thu | T8 | Canh bao hut doanh so |
| Workshop/Event | T8 | Don hang dich vu, tag workshop/event |

**NM only (5 modules):**
| Module | Milestone | Ghi chu |
|--------|-----------|---------|
| Tich diem/Loyalty | T6 | Quy tac tinh diem, len hang |
| Report Website | T6 | Heatmap, phan tich web |
| Web & Dong bo | T6 | API dong bo KH, SP, Don hang, Ton kho |
| E-commerce | T6 | Shopee, TikTok, Lazada |
| Messaging | T6 | Zalo OA, Facebook Messenger |

#### 5.2.5. Muc do chi tiet

- **Modules da co trong SRS hien tai:** Copy + chinh sua theo milestone moi
- **Modules moi (Membership, Du bao, Workshop, Report Web, Kiem soat):** Viet HIGH-LEVEL (mo ta ngan + danh sach features chinh). Chi tiet bo sung sau khi co them thong tin tu khach
- **Dieu 6 Nghiem thu:** Giu nguyen, dung chung (noi dung generic, khong mention timeline cu the)

#### 5.2.6. Checklist thuc hien — DA XONG

- [x] Tao `docs/contract/appendix/tm/` va `docs/contract/appendix/nm/`
- [x] Tao `DCNET_SRS_TM.md` tu SRS hien tai (thay header, brand, sap xep theo milestone)
- [x] Tao `DCNET_SRS_NM.md` tu SRS hien tai (thay header, brand, sap xep theo milestone)
- [x] Loai bo modules rieng cua ben kia trong moi file
- [x] Them modules moi (high-level) vao dung milestone
- [x] Loai bo tat ca mention ERPNext/Frappe/Python/MariaDB → generic terms
- [x] Tach appendices vao tm/ va nm/
- [x] Review cross-reference giua SRS va appendices
- [x] Xoa `DCNET_FLOW_SRS.md` sau khi tach xong
- [x] Xoa `docs/contract/appendix/` (4 files goc) sau khi tach xong

### 5.3. Cap nhat CLAUDE.md — DA XONG
- [x] Team: 5 nguoi (Duc, Phuong, Cuong, Dat, Hau)
- [x] 2 cong ty: TM + Nhat Minh, 2 site rieng
- [x] Timeline: T3-T8 theo thang ban giao
- [x] Tech: Frappe + ERPNext moi nhat (khong ghi version cu the)
- [x] Strategy: Tan dung ERPNext max, custom app cho dac thu
- [x] SRS: 2 file, brand DCNET
- [x] Xoa reference den files khong ton tai

### 5.4. Cleanup roadmap cu — DA XONG
- [x] Review `docs/roadmap/PHASE_1_CRM_DETAILED.md` - da xoa
- [x] Review `docs/roadmap/PHASE_2_ERP_DETAILED.md` - da xoa
- [x] Review `docs/roadmap/QA_METHODOLOGY.md` - da xoa
- [x] Xoa cac files khong con phu hop (5 files)

### 5.5. Yeu to ky thuat — DA THIET KE

#### 5.5.1. Version

| Component | Version | Ghi chu |
|-----------|---------|---------|
| Frappe Framework | v16 | Released 12/01/2026 |
| ERPNext | v16 | Released 12/01/2026 |

Lay version moi nhat hien tai, bat dau trien khai luon.

#### 5.5.2. Custom app structure

**1 app: `dcnet_apps`** — tat ca custom modules trong 1 app. Dung module structure ben trong de to chuc code.

```
dcnet_apps/
├── dcnet_apps/
│   ├── fitting/          # Module Fitting
│   ├── coaching/         # Module Coaching
│   ├── trade_in/         # Module Thu cu Doi moi
│   ├── barcode/          # Module Barcode/Tem
│   ├── consignment/      # Module Ky gui
│   ├── shipping/         # Module Giao van
│   └── ...               # Cac module khac
├── dcnet_fixtures/       # Sample data (da co)
└── setup.py
```

#### 5.5.3. Dev environment

**Devcontainer** (VS Code) — da co san `.devcontainer/`. Moi dev clone repo + "Open in Container".

#### 5.5.4. Git branching strategy

**Simplified Git Flow:**

```
main ──────────────────────────────────── (production)
  │
  └── develop ─────────────────────────── (integration)
        │
        ├── feature/fitting ──── (merge vao develop khi xong)
        ├── feature/trade-in ─── (1-3 ngay, short-lived)
        └── feature/barcode ────

Release: PR develop → main (moi dot ban giao T3/T4/T5/T6)
Hotfix:  hotfix/* tu main → merge nguoc develop
```

- Feature branches: short-lived (1-3 ngay), merge vao develop
- Release: **PR develop → main** (thay vi release branch rieng)
- Moi dot ban giao (T3-T6): tao PR develop → main, team review
- Hotfix: hotfix/* tu main, merge nguoc lai develop

#### 5.5.5. Phan chia cong viec

**Team structure:**

| Vai tro | Nguoi | Cong viec chinh |
|---------|-------|-----------------|
| **Leader** | Duc | Review code, tracking tien do, ho tro modules kho |
| **QA/Tester** | Phuong | Check chuc nang, test, task don gian |
| **Dev** | Dat | Tap trung dev |
| **Dev** | Cuong | Tap trung dev |
| **Dev** | Hau | Tap trung dev |

**Phan chia theo domain (3 devs):**

```
Dev 1 — BAN HANG + MUA HANG
  T3: Mua hang, NCC
  T4: Ban buon, Ban le, QL Ban hang, Danh muc BH
  T5: KT Mua hang, KT Ban hang, KT Cong no
  T6: Lead, CSKH

Dev 2 — KHO + KE TOAN
  T3: San pham
  T4: Kho hang, Barcode, Consignment, Don hang
  T5: KT Tien, KT HTK, Chi phi, Tai san, Thue, Tong hop, BC
  T6: Role & Permission, Kiem soat

Dev 3 — SERVICES + INTEGRATIONS
  T3: Dang nhap, Dashboard
  T4: Trade-in, Chi nhanh, NV, KH, 5x BC
  T5: (Ho tro KT)
  T6: Fitting, Coaching, Giao van, Tich diem, Web, Report Website
```

> Phan cong cu the se dieu chinh khi bat dau sprint.

---

## 6. Thong tin ky thuat

| Item | Gia tri |
|------|---------|
| Platform | Frappe v16 + ERPNext v16 (released 12/01/2026) |
| Strategy | Tan dung ERPNext toi da, custom app cho modules dac thu |
| Custom app | 1 app: `dcnet_apps` (module structure ben trong) |
| Dev env | Devcontainer (VS Code) |
| Branching | Simplified Git Flow (develop + feature + PR thay release) |
| Deploy | 2 site rieng (TM + NM), code chung |
| Team | Duc (leader), Phuong (QA), Dat+Cuong+Hau (3 devs) |
| Brand (doi ngoai) | DCNET (khong mention ERPNext/Frappe trong SRS) |
| Data migration | BRAVO → ERPNext (nhieu modules can data mau tu BRAVO) |

---

## 7. Source file

- File Excel goc: `Timeline du an - TM & Nhat Minh Sports.xlsx` (tu khach hang)
- SRS hien tai: `docs/contract/DCNET_FLOW_SRS.md` (can tach + update)
- Specs goc: `docs/feature/FEATURE_SPECIFICATION.md`, `docs/feature/ERP_SPECIFICATION.md`
