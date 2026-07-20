<!-- Source: erpnext_stock skill -->

# ERPNext Stock Module

## Description

The **ERPNext Stock Module** is the comprehensive inventory management system within ERPNext. It handles all aspects of stock tracking, warehouse management, inventory valuation, batch/serial number management, and stock transactions. This skill provides deep knowledge synthesized from codebase analysis of 202 files.

**Source Path:** `/Users/vovanduc/Code/dcnet/erpnext/erpnext/stock`
**Files Analyzed:** 202 (194 Python, 8 JavaScript)
**ERPNext Version:** v16
**Analysis Confidence:** High (codebase analysis)

---

## When to Use This Skill

### Primary Use Cases

Use this skill when you need to:

| Use Case | Examples |
|----------|----------|
| **Stock Transactions** | Stock Entry, Material Receipt, Material Issue, Stock Transfer |
| **Delivery & Shipping** | Delivery Note, Delivery Trip, Packing Slip |
| **Inventory Valuation** | FIFO, Moving Average, Standard Costing |
| **Batch & Serial Tracking** | Serial No, Batch, Serial and Batch Bundle |
| **Warehouse Management** | Warehouse setup, Bin management, Stock levels |
| **Stock Reservation** | Reserve stock for Sales Orders, Pick Lists |
| **Stock Reports** | Stock Balance, Stock Ledger, Stock Ageing, Batch reports |
| **Quality Inspection** | Incoming/outgoing quality checks |

### Specific Triggers

- Questions about **stock valuation methods** (FIFO, Moving Average, LIFO)
- How to create/manage **Stock Entry** documents
- Understanding **Stock Ledger Entry (SLE)** mechanics
- Implementing **batch tracking** or **serial number** management
- Setting up **warehouse hierarchies**
- Working with **Stock Reservation Entry** for Sales Orders
- **Delivery Note** creation and fulfillment workflows
- Stock **reordering** and inventory optimization
- **Pick List** generation and management
- **Quality Inspection** workflows

---

## Key Concepts

### Core DocTypes

| DocType | Purpose | Key Fields |
|---------|---------|------------|
| **Item** | Master data for stock items | `item_code`, `item_name`, `stock_uom`, `valuation_method` |
| **Warehouse** | Physical/logical stock locations | `warehouse_name`, `company`, `parent_warehouse` |
| **Bin** | Item-Warehouse quantity snapshot | `item_code`, `warehouse`, `actual_qty`, `projected_qty` |
| **Stock Entry** | All stock movements | `stock_entry_type`, `items`, `from_warehouse`, `to_warehouse` |
| **Stock Ledger Entry** | Immutable transaction log | `item_code`, `warehouse`, `actual_qty`, `valuation_rate` |
| **Delivery Note** | Shipment to customer | `customer`, `items`, `shipping_address` |
| **Batch** | Batch tracking for items | `batch_id`, `item`, `expiry_date` |
| **Serial No** | Individual unit tracking | `serial_no`, `item_code`, `warehouse`, `status` |
| **Serial and Batch Bundle** | Group serial/batch entries | `voucher_type`, `voucher_no`, `entries` |
| **Stock Reservation Entry** | Reserve stock for orders | `item_code`, `warehouse`, `reserved_qty`, `voucher_type` |

### Stock Entry Types

```
Material Receipt     -> Increase stock (no source warehouse)
Material Issue       -> Decrease stock (no target warehouse)
Material Transfer    -> Move between warehouses
Manufacture          -> Create finished goods from raw materials
Repack               -> Break/combine items
Send to Subcontractor -> Send materials for processing
Material Consumption -> Consume for manufacturing
```

### Valuation Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| **FIFO** | First In First Out | Perishable goods, compliance requirements |
| **Moving Average** | Weighted average of all purchases | General merchandise |
| **LIFO** | Last In First Out | Specific accounting needs |

### Stock Ledger Entry Flow

```
Transaction (Stock Entry, DN, PR, etc.)
    │
    ▼
Stock Ledger Entry Created
    │
    ├── actual_qty (change in quantity)
    ├── qty_after_transaction (running balance)
    ├── valuation_rate (cost per unit)
    └── stock_value_difference (monetary impact)
    │
    ▼
Bin Updated (actual_qty, projected_qty)
    │
    ▼
GL Entry Created (if perpetual inventory)
```

---

## Quick Reference

### 1. Get Stock Balance

```python
from erpnext.stock.utils import get_stock_balance

# Get current stock quantity
qty = get_stock_balance(
    item_code="ITEM-001",
    warehouse="Stores - Company"
)

# Get stock with valuation rate
qty, rate = get_stock_balance(
    item_code="ITEM-001",
    warehouse="Stores - Company",
    with_valuation_rate=True
)
```

### 2. Create Stock Entry (Material Receipt)

```python
import frappe
from erpnext.stock.doctype.stock_entry.stock_entry import make_stock_entry

# Simple material receipt
se = make_stock_entry(
    item_code="ITEM-001",
    qty=100,
    to_warehouse="Stores - Company",
    rate=50,
    purpose="Material Receipt"
)
se.submit()

# Or create manually
se = frappe.new_doc("Stock Entry")
se.stock_entry_type = "Material Receipt"
se.append("items", {
    "item_code": "ITEM-001",
    "qty": 100,
    "t_warehouse": "Stores - Company",
    "basic_rate": 50
})
se.save()
se.submit()
```

### 3. Stock Transfer Between Warehouses

```python
se = make_stock_entry(
    item_code="ITEM-001",
    qty=50,
    from_warehouse="Stores - Company",
    to_warehouse="Finished Goods - Company",
    purpose="Material Transfer"
)
se.submit()
```

### 4. Create Delivery Note from Sales Order

```python
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note

# Create DN from SO
dn = make_delivery_note(sales_order_name)
dn.save()
dn.submit()
```

### 5. Get Actual Qty in Bin

```python
from erpnext.stock.doctype.bin.bin import get_actual_qty

actual_qty = get_actual_qty(
    item_code="ITEM-001",
    warehouse="Stores - Company"
)
```

### 6. Get Item Details for Transaction

```python
from erpnext.stock.get_item_details import get_item_details

details = get_item_details({
    "item_code": "ITEM-001",
    "warehouse": "Stores - Company",
    "doctype": "Stock Entry",
    "company": "My Company"
})
# Returns: item_name, stock_uom, valuation_rate, etc.
```

### 7. Working with Batches

```python
from erpnext.stock.doctype.batch.batch import get_batch_qty

# Get batch quantity
qty = get_batch_qty(
    batch_no="BATCH-001",
    warehouse="Stores - Company",
    item_code="ITEM-001"
)

# Create batch
batch = frappe.new_doc("Batch")
batch.item = "ITEM-001"
batch.batch_id = "BATCH-2024-001"  # Optional, auto-generated if blank
batch.expiry_date = "2025-12-31"
batch.save()
```

### 8. Stock Reservation for Sales Order

```python
from erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry import (
    make_stock_reservation_entry,
    cancel_stock_reservation_entries
)

# Reserve stock for SO
sre = make_stock_reservation_entry(
    item_code="ITEM-001",
    warehouse="Stores - Company",
    voucher_type="Sales Order",
    voucher_no="SO-00001",
    voucher_detail_no="SO-00001-item-1",
    reserved_qty=30
)

# Cancel all reservations for an SO
cancel_stock_reservation_entries("Sales Order", "SO-00001")
```

### 9. Pick List Operations

```python
from erpnext.stock.doctype.pick_list.pick_list import create_pick_list

# Create pick list from Sales Order
pl = create_pick_list(sales_order_name)
pl.save()
pl.submit()

# Create stock reservations from pick list
pl.create_stock_reservation_entries()
```

### 10. Get Warehouse Account Mapping

```python
from erpnext.stock import get_warehouse_account_map

# Get all warehouse-account mappings for a company
account_map = get_warehouse_account_map(company="My Company")
# Returns: {warehouse_name: account_name, ...}
```

---

## Stock Reservation Workflow

The Stock Reservation Entry (SRE) tracks reserved stock for Sales Orders:

### Status Flow

```
Draft → Partially Reserved → Reserved → Partially Delivered → Delivered → Cancelled
```

### Example: Complete Reservation Workflow

```python
# 1. Create Sales Order with stock reservation
so = make_sales_order(
    item_code="ITEM-001",
    warehouse="Stores - Company",
    qty=50,
    rate=100,
    do_not_submit=True
)
so.reserve_stock = 1
so.items[0].reserve_stock = 1
so.save()
so.submit()

# 2. Create partial reservation
sre = make_stock_reservation_entry(
    item_code="ITEM-001",
    warehouse="Stores - Company",
    voucher_type="Sales Order",
    voucher_no=so.name,
    voucher_detail_no=so.items[0].name,
    reserved_qty=30
)
# Status: "Partially Reserved"

# 3. Reserve remaining quantity
sre.reserved_qty = sre.voucher_qty
sre.save()
sre.update_status()
# Status: "Reserved"

# 4. Delivery updates reservation
sre.delivered_qty = 30
sre.db_update()
sre.update_status()
# Status: "Partially Delivered"

# 5. Full delivery
sre.delivered_qty = sre.voucher_qty
sre.db_update()
sre.update_status()
# Status: "Delivered"
```

### Reserved Stock Protection

Reserved stock cannot be consumed by other transactions:

```python
from erpnext.stock.stock_ledger import NegativeStockError

# This will raise NegativeStockError if stock is reserved
se = make_stock_entry(
    item_code="ITEM-001",
    qty=actual_qty,  # Includes reserved qty
    from_warehouse="Stores - Company",
    purpose="Material Issue"
)
se.submit()  # Raises NegativeStockError!
```

---

## Delivery Note Workflow

### Creating Delivery Note

```python
class DeliveryNote(SellingController):
    def validate(self):
        # Validates against Sales Order/Invoice
        self.validate_with_previous_doc()
        self.validate_references()
        self.validate_warehouse()
        self.validate_packed_qty()

    def on_submit(self):
        # Updates stock, status, reservations
        self.update_pick_list_status()
        self.check_credit_limit()
```

### Key Validations

| Validation | Description |
|------------|-------------|
| `so_required()` | Check if SO is mandatory (from Stock Settings) |
| `validate_proj_cust()` | Ensure customer matches project |
| `validate_packed_qty()` | Packed qty must equal item qty |
| `validate_against_stock_reservation_entries()` | Verify SRE exists for SO items |

---

## FIFO Queue Logic

The stock module uses FIFO (First In First Out) queues for valuation:

### FIFO Slot Generation

```python
from erpnext.stock.report.stock_ageing.stock_ageing import FIFOSlots

# Stock Ledger Entries
sle = [
    frappe._dict(
        name="Item-001",
        actual_qty=30,
        qty_after_transaction=30,
        warehouse="WH 1",
        posting_date="2024-01-01",
        voucher_type="Stock Entry",
        voucher_no="SE-001"
    ),
    frappe._dict(
        name="Item-001",
        actual_qty=20,
        qty_after_transaction=50,
        warehouse="WH 1",
        posting_date="2024-01-02",
        voucher_type="Stock Entry",
        voucher_no="SE-002"
    ),
    frappe._dict(
        name="Item-001",
        actual_qty=-10,
        qty_after_transaction=40,
        warehouse="WH 1",
        posting_date="2024-01-03",
        voucher_type="Stock Entry",
        voucher_no="SE-003"
    )
]

# Generate FIFO queue
slots = FIFOSlots(filters, sle).generate()
queue = slots["Item-001"]["fifo_queue"]
# queue[0][0] = 20.0 (remaining from first batch)
# Total qty = 40.0
```

### Multi-Warehouse FIFO

```python
from erpnext.stock.report.stock_ageing.stock_ageing import (
    generate_item_and_item_wh_wise_slots
)

# Returns both item-wise and item-warehouse-wise slots
item_wise, item_wh_wise = generate_item_and_item_wh_wise_slots(
    filters=filters,
    sle=sle
)

# item_wise aggregates across warehouses
# item_wh_wise maintains per-warehouse detail
```

---

## Batch Management

### Batch Naming Series

```python
from erpnext.stock.doctype.batch.batch import (
    batch_uses_naming_series,
    get_batch_naming_series
)

# Check if naming series is enabled
if batch_uses_naming_series():
    series = get_batch_naming_series()
    # Returns: "BATCH-.#####" or custom prefix
```

### Batch Auto-Creation

```python
class Batch(Document):
    def autoname(self):
        """Generate random ID for batch if not specified"""
        if not self.batch_id:
            self.batch_id = get_name_from_hash()

    def set_expiry_date(self):
        """Auto-calculate expiry from item shelf life"""
        if not self.expiry_date and self.item:
            shelf_life = frappe.db.get_value("Item", self.item, "shelf_life_in_days")
            if shelf_life:
                self.expiry_date = add_days(self.manufacturing_date, shelf_life)
```

---

## Delivery Trip Management

### Route Optimization

```python
class DeliveryTrip(Document):
    def process_route(self, optimize=False):
        """
        Estimate arrival times for each stop.
        If optimize=True, re-arrange stops for optimal routing.
        """
        route_list = self.form_route_list(optimize)
        directions = self.get_directions(route_list, optimize)

    def get_directions(self, route, optimize):
        """
        Retrieve map directions using Google Maps API.
        Returns optimized route if requested.
        """
        # Uses Google Directions API
        pass
```

### Trip Status Flow

```
Draft → Scheduled → In Transit → Completed → Cancelled
```

---

## API Reference Summary

### Core Functions (`erpnext.stock`)

| Function | Description |
|----------|-------------|
| `get_warehouse_account_map(company)` | Get warehouse-to-account mapping |
| `get_warehouse_account(warehouse)` | Get GL account for specific warehouse |
| `get_company_default_inventory_account(company)` | Get default inventory account |

### Stock Utils (`erpnext.stock.utils`)

| Function | Description |
|----------|-------------|
| `get_stock_balance(item, warehouse)` | Current stock quantity |
| `get_latest_stock_qty(item, warehouse)` | Latest quantity from Bin |
| `get_incoming_rate(args)` | Calculate incoming valuation rate |

### Get Item Details (`erpnext.stock.get_item_details`)

| Function | Description |
|----------|-------------|
| `get_item_details(ctx, doc)` | Complete item details for transactions |
| `get_basic_details(ctx, item)` | Basic item information |
| `get_item_tax_template(ctx, item)` | Applicable tax template |
| `get_item_warehouse_(ctx, item)` | Default warehouse resolution |
| `set_valuation_rate(out, ctx)` | Set valuation rate on output |
| `update_stock(ctx, out, doc)` | Update stock-related fields |

### Bin Operations (`erpnext.stock.doctype.bin`)

| Function | Description |
|----------|-------------|
| `get_bin_details(bin_name)` | Full bin document details |
| `update_qty(bin_name, args)` | Update bin quantities |
| `get_actual_qty(item, warehouse)` | Get actual quantity |

### Batch Operations (`erpnext.stock.doctype.batch`)

| Function | Description |
|----------|-------------|
| `get_batch_qty(batch, warehouse, item)` | Quantity in specific batch |
| `batch_uses_naming_series()` | Check naming series setting |
| `get_batch_naming_series()` | Get batch naming series |

---

## Design Patterns Detected

*From codebase analysis (confidence > 0.7)*

| Pattern | Count | Usage |
|---------|-------|-------|
| **Factory** | 37 | Document creation, entry generation |
| **Observer** | 17 | Event hooks, status updates |
| **Command** | 2 | Stock operations encapsulation |
| **Builder** | 1 | Complex document construction |

---

## Reports Reference

| Report | Purpose | Key Filters |
|--------|---------|-------------|
| **Stock Balance** | Current stock across warehouses | Item, Warehouse, Date |
| **Stock Ledger** | Transaction history | Item, Warehouse, Date Range |
| **Stock Ageing** | Inventory age analysis | Item Group, Warehouse |
| **Batch-Wise Balance** | Stock by batch | Item, Batch, Warehouse |
| **Available Batch** | Batches with available qty | Item, Warehouse |
| **Batch Item Expiry** | Expiring batches | Days to Expiry |
| **Delivery Note Trends** | Delivery analytics | Period, Company |
| **Delayed Item Report** | Late deliveries | Date Range |
| **COGS by Item Group** | Cost analysis | Item Group, Period |
| **FIFO Queue vs QAT** | Queue validation | Item, Warehouse |

---

## Configuration Patterns

### Stock Settings

| Setting | Purpose |
|---------|---------|
| `allow_negative_stock` | Permit negative stock balance |
| `valuation_method` | Default: FIFO/Moving Average |
| `stock_frozen_upto` | Freeze stock before date |
| `auto_create_serial_no` | Auto-generate serial numbers |
| `set_qty_in_transactions` | Auto-set qty based on reserved |

### Item Defaults

| Field | Purpose |
|-------|---------|
| `default_warehouse` | Default transaction warehouse |
| `valuation_method` | Item-specific valuation |
| `has_batch_no` | Enable batch tracking |
| `has_serial_no` | Enable serial tracking |
| `is_stock_item` | Maintain stock for item |

---

## Working with This Skill

### For Beginners

1. Start with **Stock Entry** basics - Material Receipt/Issue/Transfer
2. Understand the **Bin** concept (Item-Warehouse snapshot)
3. Learn **Stock Ledger Entry** as the audit trail
4. Practice with simple transactions before batch/serial items

### For Intermediate Users

1. Implement **Stock Reservation** for Sales Orders
2. Set up **Pick List** workflows
3. Configure **Batch/Serial** tracking
4. Customize **Delivery Note** workflows

### For Advanced Users

1. Understand **FIFO Queue** valuation internals
2. Implement custom **stock validation** hooks
3. Extend **Delivery Trip** with custom routing
4. Build custom **stock reports** using SLE data

### Navigation Tips

| Need | Reference |
|------|-----------|
| API details | `references/api_reference/` |
| Code patterns | `references/patterns/` |
| Test examples | `references/test_examples/` |
| Dependencies | `references/dependencies/` |
| Config options | `references/config_patterns/` |

---

## Available Reference Files

| Directory | Contents | Confidence |
|-----------|----------|------------|
| `api_reference/` | Complete function/class documentation | Medium-High |
| `dependencies/` | Module dependency graph | High |
| `patterns/` | Design pattern implementations | High |
| `test_examples/` | Real test code examples | High |
| `config_patterns/` | DocType configurations (100 files) | Medium |
| `documentation/` | README files (36 documents) | High |

### Key API Reference Files

| File | Contents |
|------|----------|
| `delivery_note.md` | DeliveryNote class, make_delivery_note, validations |
| `stock_entry.md` | Stock Entry creation, purposes, workflows |
| `bin.md` | Bin operations, qty calculations |
| `batch.md` | Batch management, naming, expiry |
| `get_item_details.md` | Item detail retrieval, pricing, taxes |
| `stock_ledger.md` | SLE operations, reposting |
| `delivery_trip.md` | Route optimization, trip management |

---

## Common Integration Patterns

### Sales Flow

```
Sales Order → (Stock Reservation) → Pick List → Delivery Note → Sales Invoice
                    ↓
              Serial/Batch Bundle
```

### Purchase Flow

```
Purchase Order → Purchase Receipt → (Quality Inspection) → Stock Ledger Entry
                        ↓
                  Batch/Serial Creation
```

### Manufacturing Flow

```
Work Order → Stock Entry (Material Transfer) → Stock Entry (Manufacture)
                    ↓                                  ↓
              Raw Material Issued              Finished Goods Created
```

---

## Troubleshooting

### Negative Stock Error

```python
from erpnext.stock.stock_ledger import NegativeStockError

# This exception is raised when:
# 1. Insufficient stock in warehouse
# 2. Reserved stock prevents consumption
# 3. allow_negative_stock is False

# Solution: Check actual_qty vs reserved_qty in Bin
```

### Batch Not Found

```python
from erpnext.stock.doctype.batch.batch import UnableToSelectBatchError

# Raised when batch auto-selection fails
# Check: batch has_qty, not expired, matches item
```

### Serial No Mismatch

```python
# Ensure serial numbers:
# 1. Exist in database
# 2. Have correct status (Active/Available)
# 3. Match item_code
# 4. Are in source warehouse
```

---

**Generated by Skill Seeker** | ERPNext Stock Module Analysis | 202 files analyzed
