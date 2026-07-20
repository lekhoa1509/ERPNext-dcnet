# DCNET Fixtures - Sample Data for Golf Business

Sample data fixtures for DCNET Golf Business running on ERPNext v16.

## Overview

This app provides realistic sample data for a Golf equipment & services business, including:
- **CRM Data**: Leads, Opportunities
- **Selling**: Customers, Sales Orders
- **Buying**: Suppliers, Purchase Orders
- **Stock**: Items (Golf equipment), Warehouses
- **Accounts**: Invoices, Payments, Journal Entries
- **HR**: Employees
- **Services**: Fitting Sessions

## Quick Start

### Installation

```bash
# Inside devcontainer/frappe-bench directory:
cd /workspace/development/frappe-bench

# 1. Install the Python package (symlink mode for development)
pip install -e /workspace/dcnet_apps/dcnet_fixtures

# 2. Register app with Frappe (add to apps.txt)
echo "dcnet_fixtures" >> sites/apps.txt

# 3. Install app to site
bench --site flow.local install-app dcnet_fixtures

# 4. Generate sample data (master + Vietnamese dynamic data)
bench --site flow.local dcnet-fixtures generate
```

---

## CLI Commands

### Generate Sample Data

The `generate` command is the main command that:
1. **Installs master data** (Item Groups, Items, Warehouses) from JSON fixtures
2. **Generates Vietnamese data** (Leads, Customers, Orders, Fitting Sessions) dynamically

```bash
# Generate all data (master + dynamic Vietnamese data)
# Default: 150 Leads, 100 Opportunities, 100 Customers, 50 Suppliers,
#          150 SOs, 100 POs, 50 Fitting Sessions
bench --site flow.local dcnet-fixtures generate

# Custom counts
bench --site flow.local dcnet-fixtures generate \
    --leads 200 \
    --opportunities 150 \
    --customers 150 \
    --suppliers 80 \
    --sales-orders 200 \
    --purchase-orders 100 \
    --fitting-sessions 100

# Skip master data (if already installed)
bench --site flow.local dcnet-fixtures generate --skip-master

# Submit orders (creates GL entries for accounting)
bench --site flow.local dcnet-fixtures generate --submit
```

### Unified 3-Year Data Generation (Realistic Model)

The `generate-3y` command is a high-level orchestrator that simulates a company's growth over **3 years (2023-2026 Q1)** with a **50% Year-over-Year (YoY) growth** in sales and profit.

```bash
# Generate full 3-year history with automatic clearing
bench --site flow.local dcnet-fixtures generate-3y --clear

# Generate only specific phases (if you want to build incrementally)
bench --site flow.local dcnet-fixtures generate-3y --phase foundation
bench --site flow.local dcnet-fixtures generate-3y --phase stock
bench --site flow.local dcnet-fixtures generate-3y --phase sales
```

#### The 7-Phase Pipeline:
- **Phase 1: Foundation Setup**: Fiscal Years, Cost Centers, Warehouses, Taxes.
- **Phase 1.5: Vietnamese Accounting (TT200)**: Normalizes COA to TT200, injects initial capital, and sets up asset lifecycles.
- **Phase 2: Master Data**: Generates Vietnamese Customers/Suppliers.
- **Phase 3: CRM Data**: Generates Leads/Opportunities.
- **Phase 4: Stock Setup**: Opening stock and quarterly transfers.
- **Phase 5: Procurement Cycle**: Full PO → PR → PI → Payment.
- **Phase 6: Sales Cycle**: Full SO → DN → SI → Payment.
- **Phase 7: Business Expenses**: Monthly expenses (Rent, Internet, etc.) + Detailed Payroll (Salary/Insurance/Bank Payment).

### Key Features (Enhanced)
1. **TT200 Standard**: Accounts like `1111` (Cash), `1121` (Bank), `334` (Payroll), `4111` (Capital) are properly named and used.
2. **50% Annual Growth**: Realistic increase in order volume and value across 2023-2026.
3. **Cash vs Bank Logic**: 
   - Payments > 10M VND (Sales) or > 20M VND (Purchase) are forced through Bank (1121).
   - Smaller payments use a realistic mix of Cash/Bank.
4. **Asset Lifecycle**: Includes purchase of Vehicles (TSCĐ) and Laptops (CCDC) with monthly depreciation entries and a disposal example in 2025.
5. **Detailed Payroll**: Instead of a simple expense, it creates a 2-step process (Accrual JV for Salary/Insurance + Payment JV from Bank).
- **Historical Accuracy**: Uses `set_posting_time = 1` to ensure all historical transactions are recorded with their correct past dates, bypassing modern validation.
- **Accounting Completeness**: Generates submitted documents to populate General Ledger and Stock Ledger.

---
### Generate Specific Module Only

```bash
# Master data only (Item Groups, Items, Warehouses from JSON)
bench --site flow.local dcnet-fixtures generate --module master

# CRM data
bench --site flow.local dcnet-fixtures generate --module leads --leads 100
bench --site flow.local dcnet-fixtures generate --module opportunities --opportunities 80

# Trading data
bench --site flow.local dcnet-fixtures generate --module customers --customers 50
bench --site flow.local dcnet-fixtures generate --module suppliers --suppliers 30
bench --site flow.local dcnet-fixtures generate --module sales-orders --sales-orders 100
bench --site flow.local dcnet-fixtures generate --module purchase-orders --purchase-orders 50

# Services data
bench --site flow.local dcnet-fixtures generate --module fitting --fitting-sessions 100
```

### Other Commands

```bash
# Check fixtures status
bench --site flow.local dcnet-fixtures status

# Clear all fixtures (requires --force)
bench --site flow.local dcnet-fixtures clear --force
```

---

## Command Options Reference

| Option | Default | Description |
|--------|---------|-------------|
| `--leads` | 150 | Number of Leads to generate |
| `--opportunities` | 100 | Number of Opportunities to generate |
| `--customers` | 100 | Number of Customers to generate |
| `--suppliers` | 50 | Number of Suppliers to generate |
| `--sales-orders` | 150 | Number of Sales Orders to generate |
| `--purchase-orders` | 100 | Number of Purchase Orders to generate |
| `--fitting-sessions` | 50 | Number of Fitting Sessions to generate |
| `--submit` | false | Submit orders (creates GL entries) |
| `--skip-master` | false | Skip installing master data |
| `--module` | (all) | Generate specific module only |

**Available modules:** `master`, `leads`, `customers`, `suppliers`, `opportunities`, `sales-orders`, `purchase-orders`, `fitting`

---

## Vietnamese Data Generator

Generator tao data voi ten tieng Viet co dau day du, bao gom:

### Sample Names Generated

| Type | Examples |
|------|----------|
| **Lead/Customer (B2C)** | Nguyen Van Hung, Tran Thi Mai, Pham Duc Anh, Le Hoang Nam |
| **Customer (B2B)** | Cong ty TNHH Nguyen Sports, Pro Shop San Golf Long Thanh |
| **Supplier** | Cong ty TNHH TaylorMade Viet Nam, Dai ly Callaway TP. Ho Chi Minh |

### Data Distribution

| Field | Values |
|-------|--------|
| **Lead Source** | Website, Facebook, Zalo, Phone, Walk In, Referral, Google Ads, TikTok, Instagram |
| **Lead Status** | Lead (15%), Open (30%), Replied (20%), Interested (20%), Converted (8%), Do Not Contact (4%) |
| **Opportunity Stage** | Prospecting, Qualification, Needs Analysis, Value Proposition, Proposal/Price Quote, Negotiation/Review |
| **Customer Type** | 70% B2C (Individual), 30% B2B (Company) |
| **Fitting Status** | New, Confirmed, In Progress, Completed, Has Order, Follow Up, No Show, Cancelled |
| **Cities** | Ha Noi, TP. Ho Chi Minh, Da Nang, Hai Phong, Can Tho, Nha Trang, Hue... |

### Python API

```python
# In bench console
import frappe
from dcnet_fixtures.dcnet_fixtures.generators.vietnamese_data import (
    generate_all_data,
    generate_leads,
    generate_customers,
    generate_suppliers,
    generate_opportunities,
    generate_sales_orders,
    generate_purchase_orders,
    generate_fitting_sessions
)

# Generate all data
generate_all_data(
    leads=150,
    opportunities=100,
    customers=100,
    suppliers=50,
    sales_orders=150,
    purchase_orders=100,
    fitting_sessions=50,
    submit_orders=False
)
frappe.db.commit()

# Or generate individually
generate_leads(count=100)
generate_customers(count=50, b2b_ratio=0.3)  # 30% B2B
generate_suppliers(count=30)
generate_opportunities(count=80)
generate_sales_orders(count=100, start_date="2025-01-01", end_date="2025-03-31")
generate_purchase_orders(count=50, submit=False)
generate_fitting_sessions(count=50)
frappe.db.commit()
```

---

## Data Volume Summary

### After Generate (Full Dataset)

| DocType | Default Count |
|---------|---------------|
| Item Groups | 24 |
| Items | 80 |
| Customers | ~140 (40 base + 100 generated) |
| Suppliers | ~60 (10 base + 50 generated) |
| Leads | ~170 (20 base + 150 generated) |
| Opportunities | ~115 (15 base + 100 generated) |
| Sales Orders | ~180 (30 base + 150 generated) |
| Purchase Orders | ~120 (20 base + 100 generated) |
| Fitting Sessions | ~100 (50 base + 50 generated) |
| Employees | 15 |

---

## Data Relationships

Understanding the data flow is crucial for testing and development:

```
                         +-------------+
                         |   Lead      |
                         +------+------+
                                | convert (status=Converted)
                         +------v------+
                         | Opportunity |
                         +------+------+
                                | create quotation
+-----------+            +------v------+            +-----------+
| Supplier  |----------->|  Customer   |<-----------| Customer  |
+-----+-----+            +------+------+            |  Group    |
      |                         |                   +-----------+
      |                         |
+-----v-----+            +------v------+
| Purchase  |            |   Sales     |
|  Order    |            |   Order     |<--- Fitting Session (optional link)
+-----+-----+            +------+------+
      | receive                 | deliver
+-----v-----+            +------v------+
| Purchase  |            |  Delivery   |
| Receipt   |            |   Note      |
| (Stock    |            +------+------+
|  Entry)   |                   |
+-----+-----+                   |
      |                         |
+-----v-----+            +------v------+
| Purchase  |            |   Sales     |
| Invoice   |            |  Invoice    |
+-----+-----+            +------+------+
      |                         |
      +-----------+-------------+
                  | payment
           +------v------+
           |  Payment    |
           |   Entry     |
           +------+------+
                  | auto-generate
           +------v------+
           |  GL Entry   |
           +-------------+
```

### Key Relationships

| Parent | Child | Link Field | Notes |
|--------|-------|------------|-------|
| Lead | Opportunity | `party_name` | Lead converts to Opportunity |
| Customer | Sales Order | `customer` | Customer places orders |
| Customer/Lead | Fitting Session | `party` | Customer/Lead has fitting |
| Fitting Session | Sales Order | `fitting_session` | Fitting converts to order |
| Sales Order | Delivery Note | `against_sales_order` | SO items delivered |
| Sales Order | Sales Invoice | `sales_order` | SO items billed |
| Supplier | Purchase Order | `supplier` | Supplier receives orders |
| Purchase Order | Purchase Receipt | `purchase_order` | PO items received |

---

## Product Categories (Golf Equipment)

### Item Groups Hierarchy

```
All Item Groups/
+-- Golf Equipment/
|   +-- Gay Golf (Clubs)/
|   |   +-- Driver
|   |   +-- Fairway Wood
|   |   +-- Hybrid
|   |   +-- Iron Set
|   |   +-- Wedge
|   |   +-- Putter
|   +-- Bong Golf (Balls)
|   +-- Phu kien Golf (Accessories)/
|   |   +-- Grip
|   |   +-- Shaft
|   |   +-- Golf Bag
|   |   +-- Gang tay (Gloves)
|   |   +-- Thiet bi do (Rangefinders)
|   +-- Quan ao Golf (Apparel)/
|       +-- Ao Polo
|       +-- Quan Golf
|       +-- Giay Golf
|       +-- Mu Golf
+-- Dich vu Golf (Services)/
    +-- Fitting Service
    +-- Coaching Service
    +-- Trade-in Service
```

### Sample Products with Pricing (VND)

| Category | Product | Price (VND) |
|----------|---------|-------------|
| **Drivers** | TaylorMade Stealth 2 | 18,500,000 |
| | Callaway Paradym | 22,000,000 |
| | Titleist TSR3 | 16,500,000 |
| **Iron Sets** | Callaway Paradym (5-PW) | 32,000,000 |
| | TaylorMade P790 (5-PW) | 28,500,000 |
| **Balls (12-pack)** | Titleist Pro V1 | 1,850,000 |
| | Callaway Chrome Soft | 1,450,000 |
| **Fitting Services** | Fitting Basic (1hr) | 500,000 |
| | Fitting Premium (2hr) | 1,200,000 |

---

## File Structure

```
dcnet_apps/dcnet_fixtures/
+-- dcnet_fixtures/
|   +-- __init__.py
|   +-- hooks.py                    # Frappe app hooks (internal)
|   +-- setup_fixtures.py           # Import/clear logic
|   |
|   +-- fixtures/                   # JSON data files
|   |   +-- master/
|   |   |   +-- 00_uom.json
|   |   |   +-- 01_item_group.json
|   |   |   +-- 02_customer_group.json
|   |   |   +-- 03_supplier_group.json
|   |   |   +-- 04_item.json
|   |   |   +-- 05_customer.json
|   |   |   +-- 06_supplier.json
|   |   +-- crm/
|   |   |   +-- 01_lead.json
|   |   |   +-- 02_opportunity.json
|   |   +-- transactions/
|   |   |   +-- 01_purchase_order.json
|   |   |   +-- 02_sales_order.json
|   |   +-- accounting/
|   |       +-- 01_employee.json
|   |
|   +-- generators/                 # Python data generators
|       +-- __init__.py
|       +-- vietnamese_data.py      # Vietnamese name generator (main)
|       +-- transactions.py         # Transaction generators
|       +-- fitting.py              # Fitting session generator
|
+-- commands.py                     # CLI commands (registered with bench)
+-- hooks.py                        # Frappe app hooks
+-- setup.py
+-- pyproject.toml
+-- README.md
```

---

## Troubleshooting

### "App dcnet_fixtures not in apps.txt" error

The app needs to be registered with Frappe before installation:
```bash
cd /workspace/development/frappe-bench
echo "dcnet_fixtures" >> sites/apps.txt
bench --site flow.local install-app dcnet_fixtures
```

### "Item not found" error when generating orders

Make sure master data is installed first:
```bash
bench --site flow.local dcnet-fixtures generate --module master
```

### "Customer not found" error

Check that Customers exist before generating transactions:
```bash
bench --site flow.local dcnet-fixtures generate --module customers --customers 50
```

### "Fitting Session DocType not found" error

The Fitting Session DocType must be installed from dcnet_apps:
```bash
bench --site flow.local install-app dcnet_apps
```

### Clearing and regenerating data

```bash
bench --site flow.local dcnet-fixtures clear --force
bench --site flow.local dcnet-fixtures generate
```

### Email validation errors

The generator automatically converts Vietnamese names to ASCII for emails:
- "Dang Van Phuong" -> "dangvanphuong@gmail.com"

---

## Technical Notes

1. **Currency**: All prices in VND (Vietnamese Dong)
2. **Territory**: Default "Vietnam" for all customers/suppliers
3. **Date Range**: Generated transactions span 3 months back from today
4. **Stock UOM**: "Nos" for units, "Hop" for ball boxes, "Set" for iron sets
5. **Vietnamese Diacritics**: Full support for Vietnamese names (Nguyen, Tran, Pham...)
6. **Fitting Integration**: Fitting Sessions can link to Sales Orders via `fitting_session` field

---

## License

MIT License

---

## Contributing

To add more fixtures:
1. Edit JSON files in `fixtures/` directory
2. Follow existing naming conventions
3. Ensure data relationships are valid
4. Test with `bench --site flow.local dcnet-fixtures generate`

To extend generators:
1. Add functions to `generators/vietnamese_data.py`
2. Follow existing patterns for error handling
3. Use `frappe.db.commit()` after bulk operations

---

**Last Updated**: January 2026
**Version**: 0.0.3
