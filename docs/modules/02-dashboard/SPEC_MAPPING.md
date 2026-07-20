# 02 - Dashboard: Spec → ERPNext Mapping

> **Nguon:** FEATURE_SPECIFICATION.md Section 2
> **ERPNext:** v16 — Number Card, Dashboard Chart, Script Report, Workspace
> **Cap nhat:** 16/02/2026

## Quy uoc Tags

| Tag | Nghia | Action |
|-----|--------|--------|
| `USE` | ERPNext co san, dung ngay | Config + test |
| `CFG` | ERPNext co, can config/setup | Setup data, settings, permissions |
| `EXT` | ERPNext co, can mo rong | Custom field, client/server script |
| `NEW` | ERPNext khong co, can build | Custom DocType, module moi |
| `REF` | Thuoc module khac | Tham chieu |

---

## 2. Dashboard — Tong quan doanh so (6 features)

### 2.1. Doanh so theo ngay, tuan, thang

- **Tag:** `CFG`
- **Spec yeu cau:** Hien thi doanh so theo cac moc thoi gian. Filter theo khoang thoi gian tuy chon.
- **ERPNext:** Number Card (Document Type: Sales Invoice, Function: Sum, Field: grand_total)
- **ERPNext da co:** Number Card hỗ trợ aggregate function (Sum/Count/Avg) trên document type. Có sẵn `filters_json` cho date range, `show_percentage_stats` + `stats_time_interval` cho trend comparison.
- **Gap:** Khong co gap. ERPNext Number Card hỗ trợ đầy đủ.
- **Action:** Tao Number Card "Total Revenue" voi filter `docstatus=1`, `posting_date=this month`, dynamic filter `company`. Show percentage stats Monthly.
- **Effort:** 0.5 ngay
- **Dependency:** Khong

### 2.2. Doanh so ban si

- **Tag:** `CFG`
- **Spec yeu cau:** Don hang tu khach si. Thong ke theo dai ly.
- **ERPNext:** Number Card + Customer Group filter
- **ERPNext da co:** Number Card filter theo `customer_group`. ERPNext co san Customer Group hierarchy.
- **Gap:** Can tao Customer Group "Khach si" (ERPNext default: "Commercial", "Individual", "Non Profit"). Dung `setup_customer_groups()` trong `install.py` de tu dong tao.
- **Action:** Tao Number Card "Wholesale Revenue" filter `customer_group = "Khach si"`. Them `setup_customer_groups()` tao Customer Group "Khach si" khi migrate.
- **Effort:** 0.5 ngay
- **Dependency:** Khong
- **⚠️ Clarify:** Ten Customer Group "Khach si" hay "Dai ly"? → CLARIFY.md #1.1

### 2.3. Doanh so ban le tong

- **Tag:** `CFG`
- **Spec yeu cau:** Tong doanh so ban le tu tat ca kenh.
- **ERPNext:** Number Card + Customer Group filter
- **ERPNext da co:** Tuong tu 2.2, dung Customer Group filter.
- **Gap:** Can tao Customer Group "Khach le". Dung `setup_customer_groups()`.
- **Action:** Tao Number Card "Retail Revenue" filter `customer_group = "Khach le"`.
- **Effort:** 0.5 ngay (chung voi 2.2)
- **Dependency:** Khong

### 2.4. Doanh so theo tung nguon khach hang

- **Tag:** `EXT`
- **Spec yeu cau:** Breakdown doanh so theo nguon KH (Facebook, Zalo, Website, Cua hang...)
- **ERPNext:** Dashboard Chart (Chart Type: Report) + Script Report
- **ERPNext da co:** Dashboard Chart co the dung Script Report lam data source. ERPNext v16 co `UTM Source` DocType va `Lead.utm_source` field.
- **Gap:** ERPNext v16 **khong co** `Customer.source` field (da bo). Nguon KH chi track qua `Lead.utm_source`. Can Script Report voi custom query join: `Sales Invoice → Customer → Lead → UTM Source`.
- **Action:** Tao Script Report "Revenue by Customer Source" voi SQL join SI→Customer→Lead→UTM Source. Tao Dashboard Chart dung report nay.
- **Effort:** 1.5 ngay
- **Dependency:** 33-lead (T6) cho data UTM Source. T3 giao UI shell, chart se hien "Khong ro" cho den khi Lead data co.

### 2.5. Doanh so theo tung nguon don hang

- **Tag:** `EXT`
- **Spec yeu cau:** Breakdown doanh so theo nguon don (Online, Offline, TMDT...)
- **ERPNext:** Dashboard Chart + Script Report + Custom Field
- **ERPNext da co:** Dashboard Chart + Script Report infrastructure. ERPNext co `Sales Order.source` (Link to Lead Source) nhung day la nguon Lead, khong phai nguon don hang.
- **Gap:** ERPNext **khong co** field "nguon don hang" tren Sales Order/Invoice. Can them custom field `custom_order_source` (Select) tren Sales Order + Sales Invoice.
- **Action:** Them Custom Field `custom_order_source` (Select: Online/Offline/TMDT/Facebook/Zalo/Website/Khac) tren SO + SI. SI auto-fetch tu SO. Tao Script Report "Revenue by Order Source" group by `custom_order_source`. Tao Dashboard Chart.
- **Effort:** 1.5 ngay
- **Dependency:** Khong
- **⚠️ Clarify:** Danh sach nguon don hang (Online/Offline/TMDT/...) da chinh xac chua? → CLARIFY.md #2.1

### 2.6. Doanh so theo san pham (Top 20)

- **Tag:** `EXT`
- **Spec yeu cau:** Top 20 san pham ban chay nhat. Bieu do doanh so theo san pham.
- **ERPNext:** Dashboard Chart + Script Report
- **ERPNext da co:** ERPNext co "Item-wise Sales History" report nhung khong co dang Top N va khong tich hop Dashboard Chart.
- **Gap:** Can Script Report custom voi GROUP BY item, ORDER BY revenue DESC, LIMIT 20. Report tra ve chart data cho Dashboard Chart.
- **Action:** Tao Script Report "Top Products by Revenue" voi filter (company, from_date, to_date, limit). Tao Dashboard Chart dung report nay.
- **Effort:** 1 ngay
- **Dependency:** 03-san-pham (T3) cho Item master data

---

## Dashboard Widgets tu module khac (REF)

### 16.2.4. Fitting Dashboard Widgets

- **Tag:** `REF`
- **Spec yeu cau:** 4 widgets: So buoi fitting, Doanh thu fitting, Ti le chuyen doi, Top NV Fitting
- **Module:** 34-fitting (T6)
- **Action:** Module 34 tu them widgets vao Workspace "Dashboard" khi deploy. Module 02 khong can lam gi.

### 17.2.4. Coaching Dashboard Widgets

- **Tag:** `REF`
- **Spec yeu cau:** 5 widgets: So hoc vien, DT coaching, DT SP phat sinh, Top HLV, Ti le hoan thanh
- **Module:** 35-coaching (T6, TM only)
- **Action:** Module 35 tu them widgets. Chi hien tren site Thang Long TM.

### 18.2.4. Trade-in Dashboard Widgets

- **Tag:** `REF`
- **Spec yeu cau:** 4 widgets: Don trade-in, Gia tri chenh lech, SP cu da thu, Top SP trade-in
- **Module:** 14-trade-in (T4)
- **Action:** Module 14 tu them widgets vao Workspace "Dashboard" khi deploy.

---

## Fake Data (Demo)

Dashboard giao T3 nhung data den tu module T4+ (Sales Invoice, Sales Order).
De demo cho khach, can tao **fake data** thong qua `dcnet_fixtures`:

| Data can tao | So luong | Module |
|-------------|---------|--------|
| Item (san pham golf) | 20+ | dcnet_fixtures/master |
| Customer (Khach si + Khach le) | 10+ | dcnet_fixtures/customers |
| UTM Source (Cua hang, Facebook, Zalo, Website, Gioi thieu) | 5 | dcnet_fixtures/master |
| Sales Invoice (submitted, nhieu thang) | 50+ | **can tao moi** |
| Sales Invoice Item (link Items) | 100+ | **can tao moi** |

> **Fake data theo mockup:** Doanh so ~2.8 ty/thang, ty le si/le 67/33, nguon KH va nguon don phan bo thuc te nganh golf.

---

## Tong hop

| Tag | So feature | Effort |
|-----|-----------|--------|
| `CFG` | 3 (2.1, 2.2, 2.3) | 1 ngay |
| `EXT` | 3 (2.4, 2.5, 2.6) | 4 ngay |
| `REF` | 3 (fitting, coaching, trade-in) | 0 |
| **Tong** | **9** (6 core + 3 REF) | **5 ngay** |

> **Ghi chu:** Effort bao gom ca fake data generation (~1 ngay). Thuc te da code xong (PR #6), effort tren la uoc luong ban dau.
