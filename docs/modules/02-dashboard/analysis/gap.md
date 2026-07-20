# Gap Analysis - Dashboard

> Nguon: FEATURE_SPECIFICATION.md Section 2
> ERPNext base: Number Card, Dashboard Chart, Report Builder, Workspace

## Luu y

Module Dashboard giao T3 (31/03/2026) nhung data thuc den tu cac module T4-T6.
T3 chi giao UI/layout voi placeholder. Data se tu dong hien thi khi module nguon duoc deploy.

## ERPNext da co

| Feature | ERPNext Component | Status |
|---------|------------------|--------|
| Doanh so theo ngay/tuan/thang | Dashboard Chart + date filter | Du |
| Doanh so ban si | Number Card + Customer Group filter | Du |
| Doanh so ban le tong | Number Card + Customer Group filter | Du |
| Doanh so theo nguon KH | Dashboard Chart (group by Lead.utm_source) | Can custom query (join SI→Customer→Lead→UTM Source) |
| Doanh so theo nguon don hang | Dashboard Chart (group by Order Source) | Du |
| Doanh so theo SP (Top 20) | Dashboard Chart / Report Builder | Du |

## Can custom

Khong can custom DocType hoac code. Toan bo 6 features dung ERPNext goc:

- **Number Card**: Cau hinh document_type = Sales Order/Sales Invoice, filter, aggregate
- **Dashboard Chart**: Cau hinh Report hoac Report Builder lam data source
- **Workspace**: Dat cac Number Card + Chart len Workspace "Dashboard"

## Cau hinh can thiet

| # | Config | Chi tiet | Do kho |
|---|--------|----------|--------|
| 1 | Number Card - Doanh so tong | SUM grand_total tu Sales Invoice, filter by date | Easy |
| 2 | Number Card - Ban si | Filter Customer Group = "Wholesale" | Easy |
| 3 | Number Card - Ban le | Filter Customer Group = "Retail" | Easy |
| 4 | Chart - Theo nguon KH | Group by source, Report Builder | Easy |
| 5 | Chart - Theo nguon don | Group by order_source (custom field neu chua co) | Easy |
| 6 | Chart - Top 20 SP | Report Builder, group by item, sort by amount DESC, limit 20 | Easy |

## Tich hop

| Module | Lien ket | Ghi chu |
|--------|---------|---------|
| 03-san-pham | Item master data | Co san T3 |
| 09-don-hang | Sales Order data | T4 moi co |
| 10-ban-buon | Customer Group filter | T4 moi co |
| 11-ban-le | Customer Group filter | T4 moi co |
| 12-ban-hang | Sales Invoice data | T4 moi co |
| 33-lead | Lead.utm_source → UTM Source | T6 moi co |

## Dashboard Widgets tu module khac

Spec con dinh nghia Dashboard Widgets cho cac module chuyen biet (T4-T8).
Cac widget nay KHONG nam trong scope module 02 — moi module tu them widget khi deploy.

| Module | Widgets | Milestone | Approach |
|--------|---------|-----------|----------|
| 34-fitting | 4 widgets (buoi fitting, DT, ti le chuyen doi, top NV) | T6 | Number Card + Chart |
| 35-coaching | 5 widgets (hoc vien, DT, SP phat sinh, top HLV, ti le) | T6 | Number Card + Chart |
| 14-trade-in | 4 widgets (don trade-in, gia tri, SP cu, top SP) | T4 | Number Card + Chart |

> **Ghi chu:** Workspace "Dashboard" can ho tro them widget dong (moi module tu append). Dung Workspace Content JSON array.

## Ket luan

- **Coverage:** 100% bang ERPNext goc (6 features chinh)
- **Custom code:** 3 Script Report (query) — khong can custom DocType
- **Components:** 1 Workspace + 3 Number Card + 3 Dashboard Chart + 3 Script Report + 2 Custom Field
- **Effort:** ~3-4 ngay
- **Risk:** Thap — chi cau hinh, khong anh huong module khac
- **Phu thuoc:** Data thuc chi hien thi sau T4 khi Sales Order/Invoice co data
- **Mo rong:** 13 widget tu module khac se duoc them tu dong khi deploy T4-T8
