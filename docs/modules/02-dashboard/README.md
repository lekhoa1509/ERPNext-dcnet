# 02 - Dashboard

| Item | Value |
|------|-------|
| **STT** | 02 |
| **Milestone** | T3 (31/03/2026) |
| **Cong ty** | TM + NM |
| **Nguon spec** | FEATURE_SPECIFICATION.md Section 2 |
| **ERPNext base** | Number Card, Dashboard Chart, Script Report, Workspace |
| **Status** | Code done — PR [#6](https://github.com/dcnet-cloud/flow_next/pull/6) |

## Luu y quan trong

**Dashboard giao T3 nhung data den tu cac module giao sau:**

| Data | Module nguon | Milestone |
|------|-------------|-----------|
| Doanh so ban si/le | 10-ban-buon, 11-ban-le, 12-ban-hang | T4 |
| Don hang | 09-don-hang | T4 |
| Khach hang, nguon KH | 17-khach-hang, 33-lead | T4, T6 |
| San pham | 03-san-pham | T3 |

**=> Can fake data de demo cho khach hang T3.** Fake data theo mockup (san pham golf, doanh so ty dong).

## 6 Features (tu spec)

| # | Feature | Tag | Approach |
|---|---------|-----|----------|
| 2.1 | Doanh so theo ngay/tuan/thang | `CFG` | Number Card + date filter |
| 2.2 | Doanh so ban si | `CFG` | Number Card + Customer Group "Khach si" |
| 2.3 | Doanh so ban le tong | `CFG` | Number Card + Customer Group "Khach le" |
| 2.4 | Doanh so theo nguon KH | `EXT` | Script Report (SI→Customer→Lead→UTM Source) |
| 2.5 | Doanh so theo nguon don hang | `EXT` | Custom field `custom_order_source` + Script Report |
| 2.6 | Doanh so theo SP Top 20 | `EXT` | Script Report (GROUP BY item, LIMIT 20) |

**Tong:** CFG: 3 | EXT: 3 | REF: 3 (widgets tu module khac)

## Approach

Su dung ERPNext built-in: Number Card + Dashboard Chart + Script Report + Workspace. Khong can custom DocType.

- 3 **Number Card** — aggregate tu Sales Invoice (tong, ban si, ban le)
- 3 **Script Report** — query cho 3 chart (nguon KH, nguon don, top SP)
- 3 **Dashboard Chart** — render tu 3 Script Report
- 1 **Workspace** — layout chua tat ca widgets
- 1 **Workspace Sidebar** — navigation sidebar (Trang chu + 3 report links)
- 2 **Custom Field** — `custom_order_source` tren Sales Order + Sales Invoice
- **Fake data** — dcnet_fixtures tao Sales Invoice mau de demo

## Tien do

- [x] README
- [x] SPEC_MAPPING.md
- [x] CLARIFY.md
- [x] CUSTOM_REQUIREMENTS.md
- [x] Gap Analysis — `analysis/gap.md`
- [x] Technical Spec — `technical-spec/dashboard-config.md`
- [x] Execution Plan — `implementation/plan.md`
- [x] UI Mockup — `mockup/`
- [x] Code — PR [#6](https://github.com/dcnet-cloud/flow_next/pull/6) (`feature/02-dashboard`)
- [ ] Fake Data — dcnet_fixtures tao Sales Invoice mau
- [x] User Guide — `user-guide/USER_GUIDE.md`

## Tai lieu trong folder

| File | Mo ta |
|------|-------|
| `SPEC_MAPPING.md` | ⭐ Mapping spec khach hang → ERPNext (6 core + 3 REF) |
| `CLARIFY.md` | 4 van de can clarify (0 Critical, 1 High, 3 Medium) |
| `CUSTOM_REQUIREMENTS.md` | Custom fields, Script Reports, Hooks, Fake data |
| `analysis/gap.md` | Gap analysis chi tiet |
| `technical-spec/dashboard-config.md` | Cau hinh Number Card, Chart, Workspace, SQL queries |
| `implementation/plan.md` | Execution plan (writing-plans format, 6 steps) |
| `mockup/` | HTML mockup voi fake data golf |
| `user-guide/USER_GUIDE.md` | HDSD tieng Viet (12 sections, 12 FAQ) |

## Dashboard Widgets tu module khac (T4-T8)

Ngoai 6 features chinh (T3), spec con dinh nghia Dashboard Widgets cho cac module chuyen biet.
Cac widget nay se duoc them vao dashboard khi module tuong ung duoc deploy:

| Module | Milestone | Widgets |
|--------|-----------|---------|
| 14-trade-in | T4 | So don trade-in, Gia tri chenh lech, SP cu da thu, Top SP trade-in |
| 34-fitting | T6 | So buoi fitting, Doanh thu fitting, Ti le chuyen doi, Top NV Fitting |
| 35-coaching (TM only) | T6 | So hoc vien, DT coaching, DT SP phat sinh, Top HLV, Ti le hoan thanh |

> **Approach:** Moi module tu them widget cua minh vao Workspace "Dashboard" khi deploy. Module 02 chi tao khung + 6 widget chinh.

## Dependencies

| Module | Quan he | Anh huong |
|--------|---------|-----------|
| 03-san-pham (T3) | Item master | Can co truoc de test Top 20 SP |
| 09-don-hang (T4) | Sales Order | Data source — dashboard khong block |
| 12-ban-hang (T4) | Sales Invoice | Data source chinh — dashboard khong block |
| 33-lead (T6) | Lead.utm_source | Data cho chart nguon KH |

> Dashboard khong bi block boi module nao. T3 giao UI shell + fake data, data thuc tu dong hien thi khi module nguon san sang.

## Lessons Learned (tu implementation)

| Van de | Nguyen nhan | Fix |
|--------|-------------|-----|
| Module Def khong tu tao khi migrate | Frappe chi tao Module Def khi `install-app` | Them `before_migrate` hook goi `setup_module_defs()` |
| `Customer.source` khong ton tai | ERPNext v16 bo field `source` tren Customer | Join qua Lead.utm_source (SI → Customer → Lead → UTM Source) |
| Customer Group "Wholesale"/"Retail" | Ten phu thuoc vao setup, chua chac co | Them `setup_customer_groups()` tao "Khach si" + "Khach le" khi migrate |
| Workspace Sidebar chi hien "Trang chu" | Chua co `workspace_sidebar/*.json` | Tao `workspace_sidebar/dashboard.json` |

## Risk

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| Customer Group ten khac du kien | Number Card sai filter | `setup_customer_groups()` tu tao "Khach si" + "Khach le" | Done |
| Danh sach order_source chua chinh xac | Chart thieu/thua category | Can clarify voi khach hang (CLARIFY.md #2.1) | Open |
| Performance voi data lon | Chart load cham | Report co date filter, limit 20 — du nhanh | OK |

## Code Reference

> Code trien khai thuc te nam trong `dcnet_apps/`, khong nam trong docs.

| Component | Location |
|-----------|----------|
| Script Reports | `dcnet_apps/dcnet_apps/dcnet_dashboard/report/` |
| Number Card fixtures | `dcnet_apps/dcnet_apps/dcnet_dashboard/number_card/` |
| Dashboard Chart fixtures | `dcnet_apps/dcnet_apps/dcnet_dashboard/dashboard_chart/` |
| Workspace config | `dcnet_apps/dcnet_apps/dcnet_dashboard/workspace/` |
| Workspace Sidebar | `dcnet_apps/dcnet_apps/workspace_sidebar/dashboard.json` |
| Custom fields | `dcnet_apps/dcnet_apps/fixtures/custom_field.json` |
| Module setup (hooks) | `dcnet_apps/dcnet_apps/install.py` (before_migrate, setup_customer_groups) |

## Files cu (tham khao, se remove sau)

> Cac file duoi day la docs cu, da duoc thay the boi SPEC_MAPPING.md + CUSTOM_REQUIREMENTS.md.
> Giu lai de tham khao, co the xoa sau khi review xong.

- `analysis/gap.md` → noi dung da merge vao SPEC_MAPPING.md
