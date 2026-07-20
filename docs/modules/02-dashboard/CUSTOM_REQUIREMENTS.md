# 02 - Dashboard: Custom Requirements

> Extract tu SPEC_MAPPING.md — chi phan can custom (EXT).
> Dung de plan execution va track tien do.

## Custom Fields (them vao DocType co san)

| DocType | Field | Type | Options | Muc dich | Spec ref |
|---------|-------|------|---------|----------|----------|
| Sales Order | custom_order_source | Select | Online\nOffline\nTMDT\nFacebook\nZalo\nWebsite\nKhac | Nguon don hang cho chart 2.5 | 2.5 |
| Sales Invoice | custom_order_source | Select | (same) | Auto-fetch tu SO, dung cho report | 2.5 |

## Server Scripts / Hooks

| Hook | Trigger | Muc dich | Spec ref |
|------|---------|----------|----------|
| before_migrate | App migrate | `setup_module_defs()` — tao Module Def "DCNET Dashboard" | Infra |
| after_migrate | App migrate | `setup_customer_groups()` — tao "Khach si" + "Khach le" | 2.2, 2.3 |
| after_migrate | App migrate | `setup_desk()` — Desktop Icon "Dashboard" idx=1 | Infra |

## Custom Reports (Script Report)

| Report | Spec ref | Data source | Query | Effort |
|--------|----------|-------------|-------|--------|
| Revenue by Customer Source | 2.4 | Sales Invoice + Customer + Lead + UTM Source | JOIN SI→Customer→Lead→UTM Source, GROUP BY utm_source | 0.5 ngay |
| Revenue by Order Source | 2.5 | Sales Invoice | GROUP BY custom_order_source | 0.5 ngay |
| Top Products by Revenue | 2.6 | Sales Invoice Item + Sales Invoice | GROUP BY item_code, ORDER BY revenue DESC, LIMIT N | 0.5 ngay |

## ERPNext Config (Number Card + Dashboard Chart + Workspace)

| Component | So luong | Spec ref | Muc dich |
|-----------|---------|----------|----------|
| Number Card | 3 | 2.1, 2.2, 2.3 | Doanh so tong / Ban si / Ban le |
| Dashboard Chart | 3 | 2.4, 2.5, 2.6 | Chart tu 3 Script Report |
| Workspace | 1 | All | Layout chua tat ca widgets |
| Workspace Sidebar | 1 | All | Navigation sidebar (Trang chu + 3 report links) |

## Fake Data Generation (dcnet_fixtures)

| Data | So luong | Muc dich | Spec ref |
|------|---------|----------|----------|
| Sales Invoice (submitted) | 50+ | Data source cho Number Card + Chart | All |
| Sales Invoice Item | 100+ | Data cho Top 20 SP | 2.6 |
| UTM Source | 5 | Nguon KH (Cua hang, Facebook, Zalo, Website, Gioi thieu) | 2.4 |
| Customer + Customer Group | 10+ | Khach si + Khach le | 2.2, 2.3 |

> **Quan trong:** Fake data phai theo mockup — san pham golf, doanh so ty dong, phan bo nguon thuc te.

## Tong effort

| Hang muc | So luong | Effort |
|----------|---------|--------|
| Custom Fields | 2 | 0.5 ngay |
| Script Reports | 3 | 1.5 ngay |
| Number Card + Chart + Workspace | 7 JSON | 1 ngay |
| Hooks (install.py) | 3 | 0.5 ngay |
| Fake Data | 1 module | 1 ngay |
| Testing | - | 0.5 ngay |
| **Tong** | | **5 ngay** |

> **Trang thai:** Da code xong (PR #6). Fake data can tao them.
