<!-- Source: erpnext_assets skill -->

# ERPNext Assets Module

## Overview

The ERPNext Assets module provides comprehensive fixed asset management capabilities including asset lifecycle tracking, multiple depreciation methods, maintenance scheduling, location tracking, and full accounting integration with General Ledger entries.

**Source:** ERPNext v16 codebase analysis
**Path:** `erpnext/assets`
**Files Analyzed:** 48 (47 Python, 1 JavaScript)
**Confidence Level:** High (direct codebase analysis)

## When to Use This Skill

Use this skill when you need to:

### Asset Management
- Create and manage fixed assets (computers, vehicles, machinery, furniture)
- Track asset lifecycle from purchase to disposal/sale
- Handle grouped assets (multiple units as single asset record)
- Split assets into separate records
- Transfer assets between locations or employees (custodians)

### Depreciation & Accounting
- Configure depreciation methods (Straight Line, Written Down Value, Double Declining Balance)
- Set up depreciation schedules with multiple finance books
- Post depreciation entries automatically or manually
- Handle pro-rata depreciation calculations
- Manage Capital Work in Progress (CWIP) accounting
- Process asset value adjustments and revaluations

### Maintenance & Repairs
- Schedule preventive maintenance tasks
- Track asset repairs with cost capitalization
- Manage maintenance teams and assignments
- Log maintenance activities and completion status

### Reporting & Compliance
- Generate Fixed Asset Register reports
- Track asset movements and custody changes
- Audit trail via Asset Activity logs

## Key Concepts

### Asset Status Lifecycle

```
Draft → Submitted → Partially Depreciated → Fully Depreciated
                 ↘ Sold (via Sales Invoice)
                 ↘ Scrapped (via scrap_asset)
                 ↘ Work In Progress (composite assets)
```

### Depreciation Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| **Straight Line** | Equal depreciation each period | Most common, predictable expenses |
| **Double Declining Balance** | Accelerated depreciation | Higher initial deductions |
| **Written Down Value (WDV)** | Percentage of remaining value | Tax purposes in some jurisdictions |

### Finance Books

Assets can have multiple finance books for different depreciation treatments:
- **Company Book** - Internal reporting
- **Tax Book** - Tax authority requirements
- **IFRS Book** - International standards

### CWIP (Capital Work in Progress)

For assets requiring installation or assembly:
1. Asset created via Purchase Receipt → Status: "Work In Progress"
2. Installation costs capitalized via Asset Capitalization
3. Asset submitted → Status: "Submitted" → Depreciation begins

## Quick Reference

### Core DocTypes

| DocType | Purpose | Key Fields |
|---------|---------|------------|
| **Asset** | Fixed asset master | item_code, asset_category, purchase_amount, location |
| **Asset Category** | Classification with accounts | depreciation_method, finance_books |
| **Asset Depreciation Schedule** | Depreciation timeline | depreciation_schedule, status |
| **Asset Movement** | Location/custodian transfers | assets, purpose, from_location, to_location |
| **Asset Maintenance** | Maintenance schedule | asset_name, maintenance_tasks |
| **Asset Repair** | Repair tracking | asset, failure_date, repair_cost |
| **Asset Capitalization** | Capitalize costs to asset | target_asset, stock_items, service_items |
| **Asset Value Adjustment** | Revaluation entries | asset, new_asset_value, difference_amount |
| **Location** | Physical location tree | parent_location, is_group |

### Essential Functions

#### Creating an Asset

```python
import frappe
from frappe.utils import nowdate, add_months

# Create asset manually
asset = frappe.get_doc({
    "doctype": "Asset",
    "asset_name": "Office Laptop",
    "item_code": "MacBook Pro",
    "asset_category": "Computers",
    "company": "_Test Company",
    "purchase_date": nowdate(),
    "available_for_use_date": nowdate(),
    "gross_purchase_amount": 100000,
    "location": "Head Office",
    "is_existing_asset": 1  # For manual entry without PR/PI
})
asset.insert()
```

#### Setting Up Depreciation

```python
# Add finance book with depreciation settings
asset.calculate_depreciation = 1
asset.append("finance_books", {
    "depreciation_method": "Straight Line",
    "total_number_of_depreciations": 36,  # 3 years monthly
    "frequency_of_depreciation": 1,       # Monthly
    "expected_value_after_useful_life": 10000,
    "depreciation_start_date": get_last_day(nowdate())
})
asset.submit()
```

#### Posting Depreciation Entries

```python
from erpnext.assets.doctype.asset.depreciation import post_depreciation_entries

# Post all pending depreciation entries up to date
post_depreciation_entries(date=nowdate())

# Or for a specific schedule
from erpnext.assets.doctype.asset.depreciation import make_depreciation_entry
make_depreciation_entry(depr_schedule_name="ACC-ADS-2024-00001")
```

#### Asset Movement (Transfer)

```python
from erpnext.assets.doctype.asset.asset import make_asset_movement

# Transfer asset to new location
movement = make_asset_movement(
    assets=[{
        "asset": "ACC-ASS-2024-00001",
        "source_location": "Head Office",
        "target_location": "Branch Office"
    }],
    purpose="Transfer"
)
movement.insert()
movement.submit()
```

#### Scrapping an Asset

```python
from erpnext.assets.doctype.asset.depreciation import scrap_asset

# Scrap asset (creates Journal Entry for disposal)
scrap_asset(asset_name="ACC-ASS-2024-00001", scrap_date=nowdate())
```

#### Restoring a Scrapped Asset

```python
from erpnext.assets.doctype.asset.depreciation import restore_asset

# Restore previously scrapped asset
restore_asset(asset_name="ACC-ASS-2024-00001")
```

#### Selling an Asset

```python
from erpnext.assets.doctype.asset.asset import make_sales_invoice

# Create Sales Invoice for asset sale
si = make_sales_invoice(
    asset="ACC-ASS-2024-00001",
    item_code="MacBook Pro",
    company="_Test Company",
    sell_qty=1
)
si.customer = "_Test Customer"
si.items[0].rate = 25000  # Selling price
si.insert()
si.submit()
# Asset status changes to "Sold"
```

#### Asset Capitalization

```python
# Capitalize stock items and services to a composite asset
capitalization = frappe.get_doc({
    "doctype": "Asset Capitalization",
    "company": "_Test Company",
    "capitalization_method": "Create a new composite asset",
    "target_asset": "ACC-ASS-2024-00001",
    "target_asset_location": "Head Office",
    "posting_date": nowdate()
})

# Add stock items consumed
capitalization.append("stock_items", {
    "item_code": "Installation Materials",
    "warehouse": "Stores - TC",
    "stock_qty": 5,
    "valuation_rate": 1000
})

# Add service costs
capitalization.append("service_items", {
    "item_code": "Installation Service",
    "qty": 1,
    "rate": 5000,
    "expense_account": "Installation Expenses - TC"
})

capitalization.insert()
capitalization.submit()
```

#### Asset Repair with Cost Capitalization

```python
# Create repair record
repair = frappe.get_doc({
    "doctype": "Asset Repair",
    "asset": "ACC-ASS-2024-00001",
    "failure_date": nowdate(),
    "repair_status": "Pending",
    "company": "_Test Company"
})

# Add consumed items (from stock)
repair.append("stock_items", {
    "item_code": "Replacement Part",
    "warehouse": "Stores - TC",
    "consumed_quantity": 1,
    "serial_no": "SN001"
})

# Link to Purchase Invoice for repair cost
repair.append("purchase_invoices", {
    "purchase_invoice": "ACC-PINV-2024-00001",
    "expense_account": "Repair Expense - TC",
    "repair_cost": 5000
})

repair.capitalize_repair_cost = 1  # Add to asset value
repair.insert()
repair.submit()
```

#### Setting Up Maintenance Schedule

```python
# Create maintenance schedule
maintenance = frappe.get_doc({
    "doctype": "Asset Maintenance",
    "asset_name": "ACC-ASS-2024-00001",
    "company": "_Test Company",
    "asset_maintenance_team": "IT Team"
})

maintenance.append("asset_maintenance_tasks", {
    "maintenance_task": "Annual Inspection",
    "maintenance_type": "Preventive Maintenance",
    "periodicity": "Yearly",
    "start_date": nowdate(),
    "assign_to": "john@example.com"
})

maintenance.insert()
```

#### Get Asset Value After Depreciation

```python
from erpnext.assets.doctype.asset.asset import get_asset_value_after_depreciation

# Get current value
current_value = get_asset_value_after_depreciation(
    asset_name="ACC-ASS-2024-00001",
    finance_book=None  # Default finance book
)
```

#### Split a Grouped Asset

```python
from erpnext.assets.doctype.asset.asset import split_asset

# Split 2 units from a grouped asset
new_asset = split_asset(
    asset_name="ACC-ASS-2024-00001",
    split_qty=2
)
# Returns new Asset document with split quantity
```

## Module Architecture

### Class Hierarchy

```
Asset (AccountsController)
├── validate() - Item, dates, finance books validation
├── before_save() - Create/update depreciation schedules
├── on_submit() - Activate depreciation schedules, create movement
├── make_gl_entries() - Post GL entries for CWIP
├── get_depreciation_rate() - Calculate depreciation rate
└── set_status() - Update status based on depreciation state

AssetDepreciationSchedule (DepreciationScheduleController)
├── validate() - Check asset and finance book
├── on_submit() - Activate schedule
├── cancel_depreciation_entries() - Reverse JE on cancel
└── fetch_asset_details() - Load asset info

AssetCapitalization (StockController)
├── validate_target_asset() - Verify target asset
├── validate_consumed_stock_item() - Check stock availability
├── on_submit() - Create GL/SLE entries
└── set_warehouse_details() - Fetch valuation rates

AssetRepair (AccountsController)
├── validate_asset() - Check asset status
├── calculate_total_repair_cost() - Sum all costs
├── update_asset_value() - Capitalize if enabled
├── decrease_stock_quantity() - Create Stock Entry
└── make_gl_entries() - Post accounting entries

AssetMovement (Document)
├── validate_asset() - Check asset status
├── validate_location() - Verify locations
├── on_submit() - Update asset location
└── log_asset_activity() - Create activity log
```

### Depreciation Methods Implementation

```
StraightLineMethod
├── get_straight_line_depr_amount() - Fixed amount per period
├── get_daily_prorata_based_depr_amount() - Daily calculation
└── get_shift_depr_amount() - Shift-based depreciation

WDVMethod
├── get_wdv_or_dd_depr_amount() - Declining balance calculation
├── get_daily_prorata_based_wdv_depr_amount() - Daily WDV
└── calculate_wdv_or_dd_based_depreciation_amount() - Core calculation
```

## Integration Points

### Accounting Integration

| Transaction | Debit Account | Credit Account |
|-------------|---------------|----------------|
| Asset Purchase (CWIP) | CWIP Account | Stock/Creditors |
| Asset Submission | Fixed Asset Account | CWIP Account |
| Depreciation Entry | Depreciation Expense | Accumulated Depreciation |
| Asset Sale | Accumulated Depr + Debtors | Fixed Asset + Gain/Loss |
| Asset Scrap | Accumulated Depr + Loss | Fixed Asset |
| Asset Repair (Capitalized) | Fixed Asset | Expense Account |

### Stock Integration

- **Asset Capitalization**: Consumes stock items, creates Stock Ledger Entries
- **Asset Repair**: Consumes spare parts from warehouse

### Purchase Integration

- **Purchase Receipt**: Auto-creates Asset if item.auto_create_assets = 1
- **Purchase Invoice**: Links to Asset for payment tracking

### HR Integration

- **Asset Movement**: Can assign custodian (Employee) to asset

## Working with This Skill

### For Beginners

1. Start with **Asset Category** setup - define accounts and depreciation defaults
2. Create **Location** hierarchy for physical tracking
3. Learn the basic Asset creation flow (PR → Asset → Submit → Depreciation)
4. Use `post_depreciation_entries()` for automatic depreciation posting

### For Intermediate Users

1. Implement multiple **Finance Books** for tax vs. book depreciation
2. Set up **Asset Maintenance** schedules for preventive maintenance
3. Use **Asset Capitalization** for composite assets
4. Handle **Asset Repair** with cost capitalization options

### For Advanced Users

1. Customize depreciation methods using `@erpnext.allow_regional` decorator
2. Implement shift-based depreciation for manufacturing equipment
3. Build custom reports using Asset Depreciation Schedule data
4. Integrate with external asset tracking systems via API

## Reference Files

### API Documentation

| File | Description | Confidence |
|------|-------------|------------|
| `api_reference/asset.md` | Core Asset DocType with 45+ methods | High |
| `api_reference/depreciation.md` | Depreciation posting functions | High |
| `api_reference/asset_depreciation_schedule.md` | Schedule management | High |
| `api_reference/asset_capitalization.md` | Capitalization logic | High |
| `api_reference/asset_repair.md` | Repair with GL entries | High |
| `api_reference/asset_maintenance.md` | Maintenance scheduling | High |
| `api_reference/asset_movement.md` | Transfer/custody tracking | High |
| `api_reference/asset_value_adjustment.md` | Revaluation entries | High |
| `api_reference/asset_category.md` | Category accounts setup | High |
| `api_reference/depreciation_methods.md` | SL/WDV/DD calculations | High |

### Test Examples

| File | Coverage |
|------|----------|
| `api_reference/test_asset.md` | Asset creation, purchase, sale, split, depreciation |
| `api_reference/test_asset_capitalization.md` | Stock/service capitalization, GL/SLE verification |
| `api_reference/test_asset_depreciation_schedule.md` | Schedule generation, cancellation |
| `api_reference/test_asset_maintenance.md` | Maintenance task scheduling |
| `api_reference/test_asset_movement.md` | Location transfers |
| `api_reference/test_asset_repair.md` | Repair cost capitalization |
| `api_reference/test_asset_value_adjustment.md` | Revaluation entries |

### Dependencies

See `references/dependencies/dependency_graph.mmd` for complete module dependency visualization.

## Design Patterns Detected

| Pattern | Count | Usage |
|---------|-------|-------|
| **Factory** | 9 | Asset creation from Purchase Receipt |
| **Observer** | 5 | Status updates, activity logging |
| **Strategy** | 1 | Depreciation method selection |
| **Template Method** | 1 | Depreciation schedule generation |
| **Builder** | 1 | GL entry construction |

## Common Patterns from Codebase

### Creating Test Assets (from test files)

```python
def create_asset(**args):
    """Helper function to create test assets"""
    args = frappe._dict(args)

    asset = frappe.get_doc({
        "doctype": "Asset",
        "asset_name": args.asset_name or "Test Asset",
        "item_code": args.item_code or "Macbook Pro",
        "company": args.company or "_Test Company",
        "asset_category": args.asset_category or "Computers",
        "location": args.location or "Test Location",
        "purchase_date": args.purchase_date or nowdate(),
        "available_for_use_date": args.available_for_use_date or nowdate(),
        "gross_purchase_amount": args.asset_value or 100000,
        "is_existing_asset": args.is_existing_asset or 1,
        "calculate_depreciation": args.calculate_depreciation or 0
    })

    if asset.calculate_depreciation:
        asset.append("finance_books", {
            "depreciation_method": args.depreciation_method or "Straight Line",
            "total_number_of_depreciations": args.total_number_of_depreciations or 5,
            "frequency_of_depreciation": args.frequency_of_depreciation or 12,
            "expected_value_after_useful_life": args.expected_value_after_useful_life or 0,
            "depreciation_start_date": args.depreciation_start_date or get_last_day(nowdate())
        })

    if not args.do_not_save:
        asset.insert()
        if args.submit:
            asset.submit()

    return asset
```

### Verifying GL Entries (from test files)

```python
def get_gl_entries(doctype, docname):
    """Get GL entries for a document"""
    return frappe.db.sql("""
        SELECT account, debit, credit
        FROM `tabGL Entry`
        WHERE voucher_type = %s AND voucher_no = %s
        ORDER BY account
    """, (doctype, docname), as_dict=1)
```

### Asset Validation Patterns

```python
# Validate item is fixed asset
def validate_item(self):
    item = frappe.get_doc("Item", self.item_code)
    if item.disabled:
        frappe.throw(_("Item {0} is disabled").format(self.item_code))
    if not item.is_fixed_asset:
        frappe.throw(_("Item {0} must be a Fixed Asset").format(self.item_code))
    if item.is_stock_item:
        frappe.throw(_("Fixed Asset cannot be a Stock Item"))
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Asset cannot be submitted without finance books" | `calculate_depreciation=1` but no finance_books | Add finance book row or set calculate_depreciation=0 |
| "Depreciation start date before purchase date" | Invalid date configuration | Set depreciation_start_date >= purchase_date |
| "Expected value cannot exceed gross purchase amount" | Salvage value too high | Reduce expected_value_after_useful_life |
| "Asset Received But Not Billed account not set" | Missing account in Asset Category | Configure asset_category.accounts for company |
| "Cannot modify depreciated asset" | Trying to edit submitted asset with posted depreciation | Cancel depreciation entries first |

### Debugging Tips

```python
# Check asset status
asset = frappe.get_doc("Asset", asset_name)
print(f"Status: {asset.status}")
print(f"Docstatus: {asset.docstatus}")
print(f"Value after depreciation: {asset.finance_books[0].value_after_depreciation}")

# Check depreciation schedule
from erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule import (
    get_asset_depr_schedule_doc
)
schedule = get_asset_depr_schedule_doc(asset_name, "Active")
for row in schedule.depreciation_schedule:
    print(f"{row.schedule_date}: {row.depreciation_amount} (JE: {row.journal_entry})")

# Check GL entries
entries = frappe.get_all("GL Entry",
    filters={"voucher_type": "Journal Entry", "against_voucher": asset_name},
    fields=["account", "debit", "credit", "posting_date"]
)
```

---

**Generated by Skill Seeker** | ERPNext Assets Module Analysis
**Analysis Source:** Codebase (High Confidence)
**Last Updated:** Based on ERPNext v16 codebase
