# Technical Spec - Dashboard Configuration

> Nguon: FEATURE_SPECIFICATION.md Section 2
> Approach: 100% ERPNext goc — Number Card + Dashboard Chart + Script Report + Workspace

## Overview

| Item | Value |
|------|-------|
| Strategy | 100% ERPNext config + 3 Script Report |
| Effort | ~3-4 ngay |
| Dependencies | Khong block boi module nao (T3 giao UI shell, data tu T4+) |
| Risk | Thap — chi cau hinh, khong anh huong module khac |

## Tong quan

Dashboard duoc xay dung tren **1 Workspace** chua 6 widget (3 Number Card + 3 Dashboard Chart).
3 Script Report cung cap data source cho 3 Dashboard Chart.
1 Workspace Sidebar cung cap navigation sidebar.

**Data source chinh:** Sales Invoice (cho doanh so thuc te).

> Luu y: T3 giao layout truoc. Data thuc chi co tu T4 khi Sales Order/Invoice duoc tao.

## File Structure (trong dcnet_apps)

```
dcnet_apps/dcnet_apps/
├── modules.txt                                    (edit: them "DCNET Dashboard")
├── hooks.py                                       (edit: them before_migrate, fixtures filter)
├── install.py                                     (edit: before_migrate, setup_customer_groups)
├── fixtures/custom_field.json                     (edit: them 2 custom fields)
├── workspace_sidebar/
│   └── dashboard.json                             (NEW: sidebar navigation)
└── dcnet_dashboard/
    ├── __init__.py
    ├── report/
    │   ├── __init__.py
    │   ├── revenue_by_customer_source/
    │   │   ├── __init__.py
    │   │   ├── revenue_by_customer_source.json
    │   │   ├── revenue_by_customer_source.py
    │   │   └── revenue_by_customer_source.js
    │   ├── revenue_by_order_source/
    │   │   ├── __init__.py
    │   │   ├── revenue_by_order_source.json
    │   │   ├── revenue_by_order_source.py
    │   │   └── revenue_by_order_source.js
    │   └── top_products_by_revenue/
    │       ├── __init__.py
    │       ├── top_products_by_revenue.json
    │       ├── top_products_by_revenue.py
    │       └── top_products_by_revenue.js
    ├── number_card/
    │   ├── total_revenue/total_revenue.json
    │   ├── wholesale_revenue/wholesale_revenue.json
    │   └── retail_revenue/retail_revenue.json
    ├── dashboard_chart/
    │   ├── revenue_by_customer_source/revenue_by_customer_source.json
    │   ├── revenue_by_order_source/revenue_by_order_source.json
    │   └── top_products_by_revenue/top_products_by_revenue.json
    └── workspace/
        └── dashboard/dashboard.json
```

---

## Workspace: "Dashboard"

| Field | Value |
|-------|-------|
| Name | Dashboard |
| Module | DCNET Dashboard |
| Icon | chart-line |
| Label | Dashboard |
| Public | Yes |
| Is Standard | Yes |

---

## Workspace Sidebar: "Dashboard"

Navigation sidebar hien thi khi user o trong context Dashboard.

| Item | Type | Link |
|------|------|------|
| Trang chu | Link (Workspace) | Dashboard |
| Bao cao | Section Break (collapsible) | — |
| DS theo nguon KH | Link (Report) | Revenue by Customer Source |
| DS theo nguon don | Link (Report) | Revenue by Order Source |
| Top 20 SP ban chay | Link (Report) | Top Products by Revenue |

> File: `workspace_sidebar/dashboard.json` — Frappe tu sync khi `bench migrate`.

---

## Number Cards (3)

### NC-01: Doanh so tong (ngay/tuan/thang)

| Field | Value |
|-------|-------|
| Name | Total Revenue |
| Label | Doanh so |
| Document Type | Sales Invoice |
| Function | Sum |
| Aggregate Field | grand_total |
| Filters | `docstatus = 1, posting_date = this month` |
| Dynamic Filters | `company = user default` |
| Show Percentage Stats | Yes |
| Stats Timespan | Monthly |

### NC-02: Doanh so ban si

| Field | Value |
|-------|-------|
| Name | Wholesale Revenue |
| Label | Doanh so ban si |
| Document Type | Sales Invoice |
| Function | Sum |
| Aggregate Field | grand_total |
| Filters | `docstatus = 1, this month, customer_group = "Khach si"` |

> **Da fix:** Customer Group "Khach si" duoc tu dong tao boi `setup_customer_groups()` trong `install.py`.

### NC-03: Doanh so ban le tong

| Field | Value |
|-------|-------|
| Name | Retail Revenue |
| Label | Doanh so ban le |
| Document Type | Sales Invoice |
| Function | Sum |
| Aggregate Field | grand_total |
| Filters | `docstatus = 1, this month, customer_group = "Khach le"` |

> **Da fix:** Customer Group "Khach le" duoc tu dong tao boi `setup_customer_groups()` trong `install.py`.

---

## Dashboard Charts (3)

### DC-01: Doanh so theo nguon khach hang

| Field | Value |
|-------|-------|
| Name | Revenue by Customer Source |
| Chart Type | Report |
| Report Name | Revenue by Customer Source |
| Type | Bar |
| Use Report Chart | Yes |

**Query (actual):**

```sql
SELECT
    IFNULL(us.name, 'Khong ro') as source,
    SUM(si.grand_total) as revenue
FROM `tabSales Invoice` si
LEFT JOIN `tabCustomer` c ON si.customer = c.name
LEFT JOIN `tabLead` l ON c.lead_name = l.name
LEFT JOIN `tabUTM Source` us ON l.utm_source = us.name
WHERE si.docstatus = 1
GROUP BY us.name
ORDER BY revenue DESC
```

> **Luu y:** ERPNext v16 KHONG co `Customer.source`. Nguon KH duoc track qua `Lead.utm_source` (Link to UTM Source). Query join: SI → Customer → Lead → UTM Source.

### DC-02: Doanh so theo nguon don hang

| Field | Value |
|-------|-------|
| Name | Revenue by Order Source |
| Chart Type | Report |
| Report Name | Revenue by Order Source |
| Type | Bar |

**Query (actual):**

```sql
SELECT
    IFNULL(si.custom_order_source, 'Khong ro') as order_source,
    SUM(si.grand_total) as revenue
FROM `tabSales Invoice` si
WHERE si.docstatus = 1
GROUP BY si.custom_order_source
ORDER BY revenue DESC
```

### DC-03: Top 20 san pham theo doanh so

| Field | Value |
|-------|-------|
| Name | Top Products by Revenue |
| Chart Type | Report |
| Report Name | Top Products by Revenue |
| Type | Bar |

**Query (actual):**

```sql
SELECT
    sii.item_code, sii.item_name,
    SUM(sii.qty) as qty,
    SUM(sii.amount) as revenue
FROM `tabSales Invoice Item` sii
JOIN `tabSales Invoice` si ON sii.parent = si.name
WHERE si.docstatus = 1
GROUP BY sii.item_code, sii.item_name
ORDER BY revenue DESC
LIMIT %(limit)s
```

---

## Custom Fields

| # | DocType | Fieldname | Label | Fieldtype | Options | Ghi chu |
|---|---------|-----------|-------|-----------|---------|---------|
| 1 | Sales Order | custom_order_source | Nguon don hang | Select | Online\nOffline\nTMDT\nFacebook\nZalo\nWebsite\nKhac | insert_after: source |
| 2 | Sales Invoice | custom_order_source | Nguon don hang | Select | (same) | fetch_from: sales_order.custom_order_source |

> **Luu y:** Fieldname la `custom_order_source` (co prefix `custom_` theo convention Frappe v16 cho custom fields).

---

## Infrastructure (hooks)

| Hook | Function | Muc dich |
|------|----------|----------|
| `before_migrate` | `setup_module_defs()` | Tao Module Def tu modules.txt truoc khi sync |
| `after_migrate` | `setup_customer_groups()` | Tao Customer Group "Khach si" + "Khach le" |
| `after_migrate` | `setup_desk()` | Desktop Icon "Dashboard" idx=1 |
| fixtures | Custom Field filter | `["dt", "in", ["Lead", "Sales Order", "Sales Invoice"]]` |

---

## Tong ket

| Component | So luong | Can code? | Location |
|-----------|---------|-----------|----------|
| Workspace | 1 | Khong (JSON) | `dcnet_dashboard/workspace/dashboard/` |
| Workspace Sidebar | 1 | Khong (JSON) | `workspace_sidebar/dashboard.json` |
| Number Card | 3 | Khong (JSON) | `dcnet_dashboard/number_card/` |
| Dashboard Chart | 3 | Khong (JSON) | `dcnet_dashboard/dashboard_chart/` |
| Script Report | 3 | Co (Python) | `dcnet_dashboard/report/` |
| Custom Field | 2 | Khong (JSON) | `fixtures/custom_field.json` |
| Install hooks | 2 | Co (Python) | `install.py` (setup_module_defs, setup_customer_groups) |
| Custom DocType | 0 | - | - |

**Effort:** ~3-4 ngay
- 0.5 ngay: Setup module dcnet_dashboard + Custom field custom_order_source
- 1 ngay: Tao 3 Script Report (Python + JS + JSON)
- 0.5 ngay: Cau hinh Number Card + Dashboard Chart (JSON fixtures)
- 0.5 ngay: Layout Workspace + Workspace Sidebar + Desktop Icon
- 0.5 ngay: Fix bugs (Customer.source, Customer Group, Module Def)
- 0.5 ngay: Test + review
