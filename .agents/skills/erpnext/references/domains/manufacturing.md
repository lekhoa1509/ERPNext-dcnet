<!-- Source: erpnext_manufacturing skill -->

# ERPNext Manufacturing Module

## Description

Comprehensive documentation and API reference for the ERPNext Manufacturing module, providing complete production planning, bill of materials management, work order execution, job card tracking, and shop floor management capabilities.

**Source:** ERPNext v16 Manufacturing Module
**Files Analyzed:** 108
**Languages:** Python (95.4%), JavaScript (4.6%)
**Confidence Level:** High (direct codebase analysis)

## When to Use This Skill

Use this skill when you need to:

### Production Planning & Scheduling
- Create and manage **Production Plans** from Sales Orders or Material Requests
- Calculate material requirements and generate Material Requests
- Plan sub-assembly items with multi-level BOM support
- Forecast production needs with exponential smoothing

### Bill of Materials (BOM)
- Create single-level or multi-level BOMs
- Manage BOM versions and replacements
- Calculate BOM costs and update pricing
- Explore BOM trees and exploded items
- Compare BOMs and track changes

### Work Orders & Manufacturing
- Create Work Orders from Production Plans or directly from BOM
- Track material transfer and manufacturing progress
- Manage work order statuses (Draft, Not Started, In Progress, Completed, Stopped, Closed)
- Handle scrap items and process losses

### Job Cards & Operations
- Create and manage Job Cards for each operation
- Track time logs and workstation scheduling
- Validate workstation capacity and overlap
- Handle sub-operations and parallel operations

### Shop Floor Management
- Monitor plant floor activities
- Track downtime and machine efficiency
- Manage workstations and their working hours
- Analyze production analytics and costs

### Reports & Analysis
- BOM Stock Reports (availability analysis)
- Production Analytics
- Downtime Analysis
- Cost of Poor Quality Reports
- Job Card Summary
- Material Requirements Planning (MRP)

---

## Key Concepts

### Core DocTypes

| DocType | Purpose |
|---------|---------|
| **BOM** | Bill of Materials - defines item recipe with raw materials and operations |
| **Production Plan** | Central planning document that generates Work Orders and Material Requests |
| **Work Order** | Manufacturing execution document for a specific item quantity |
| **Job Card** | Tracks individual operations within a Work Order |
| **Workstation** | Physical machine/workspace with capacity and cost settings |
| **Operation** | Manufacturing step/activity that can be assigned to workstations |
| **Routing** | Sequence of operations for manufacturing an item |

### Manufacturing Workflow

```
Sales Order → Production Plan → Work Order → Job Card → Stock Entry
                    ↓
            Material Request → Purchase Order → Purchase Receipt
```

### BOM Structure

```
Finished Good (BOM)
├── Raw Material 1
├── Raw Material 2
├── Sub-Assembly (has its own BOM)
│   ├── Component A
│   └── Component B
└── Operations
    ├── Operation 1 → Workstation A
    └── Operation 2 → Workstation B
```

---

## Quick Reference

### Creating a BOM

```python
# Create a simple BOM
bom = frappe.new_doc("BOM")
bom.item = "Finished Product"
bom.company = "My Company"
bom.quantity = 1
bom.is_default = 1
bom.is_active = 1

# Add raw materials
bom.append("items", {
    "item_code": "Raw Material A",
    "qty": 2,
    "rate": 100,
    "uom": "Nos"
})

bom.append("items", {
    "item_code": "Raw Material B",
    "qty": 1,
    "rate": 50,
    "uom": "Nos"
})

# Add operation (optional)
bom.append("operations", {
    "operation": "Assembly",
    "workstation": "Assembly Station",
    "time_in_mins": 30
})

bom.insert()
bom.submit()
```

### Creating a Production Plan from Sales Orders

```python
# Create Production Plan
pln = frappe.new_doc("Production Plan")
pln.company = "_Test Company"
pln.posting_date = frappe.utils.nowdate()
pln.get_items_from = "Sales Order"

# Add Sales Orders
pln.append("sales_orders", {
    "sales_order": "SO-00001",
    "sales_order_date": "2026-01-01",
    "customer": "Customer A",
    "grand_total": 10000
})

# Get items from Sales Orders
pln.get_items()

# Optionally combine same items
pln.combine_items = 1
pln.get_items()

pln.insert()
pln.submit()

# Generate Work Orders
pln.make_work_order()

# Generate Material Requests
pln.make_material_request()
```

### Creating a Work Order

```python
from erpnext.manufacturing.doctype.work_order.work_order import make_work_order

# Create Work Order from BOM
wo = make_work_order(
    bom_no="BOM-FP-001",
    item="Finished Product",
    qty=10,
    project=None
)

# Set warehouses
wo.wip_warehouse = "Work In Progress - TC"
wo.fg_warehouse = "Finished Goods - TC"

wo.insert()
wo.submit()

# Get operations from BOM
wo.set_work_order_operations()
```

### Creating Stock Entry for Material Transfer

```python
from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry

# Transfer materials to WIP warehouse
se = make_stock_entry(
    work_order_id="WO-00001",
    purpose="Material Transfer for Manufacture",
    qty=10
)
se.insert()
se.submit()
```

### Creating Stock Entry for Manufacture

```python
# Complete manufacturing
se = make_stock_entry(
    work_order_id="WO-00001",
    purpose="Manufacture",
    qty=10
)
se.insert()
se.submit()
```

### Working with Job Cards

```python
# Get Job Card for a Work Order
jc = frappe.get_last_doc("Job Card", {"work_order": "WO-00001"})

# Add time log
jc.append("time_logs", {
    "from_time": "2026-01-15 08:00:00",
    "to_time": "2026-01-15 12:00:00",
    "completed_qty": 5
})

jc.save()

# Check for workstation overlap
# Job Card validates capacity constraints automatically
```

### BOM Tree Traversal

```python
from erpnext.manufacturing.doctype.bom.bom import BOMTree

# Get full BOM tree
tree = BOMTree("BOM-FP-001")

# Level order traversal
items = tree.level_order_traversal()
for item in items:
    print(f"{item.name}: qty={item.qty}, exploded_qty={item.exploded_qty}")
```

### Getting Material Requirements

```python
from erpnext.manufacturing.doctype.production_plan.production_plan import (
    get_items_for_material_requests
)

# Get material requirements for a Production Plan
doc = frappe.get_doc("Production Plan", "PP-00001")
mr_items = get_items_for_material_requests(doc.as_dict())

for item in mr_items:
    print(f"{item['item_code']}: need {item['quantity']} {item['uom']}")
```

### BOM Cost Update

```python
from erpnext.manufacturing.doctype.bom_update_tool.bom_update_tool import (
    enqueue_update_cost
)

# Queue BOM cost update (runs in background)
log = enqueue_update_cost()
print(f"BOM Update Log: {log.name}")
```

---

## Work Order Status Flow

```
Draft → Not Started → In Progress → Completed
           ↓              ↓
        Stopped       Stopped
           ↓              ↓
        Closed        Closed
```

**Status Conditions:**
- **Not Started**: Submitted but no material transferred
- **In Progress**: Material transferred or manufacturing started
- **Completed**: All quantity manufactured
- **Stopped**: Temporarily halted (can resume)
- **Closed**: Permanently closed (cannot resume)

---

## API Reference Summary

### Production Plan

| Method | Description |
|--------|-------------|
| `get_open_sales_orders()` | Pull pending Sales Orders |
| `get_pending_material_requests()` | Pull pending Material Requests |
| `get_items()` | Get items from SO/MR |
| `make_work_order()` | Generate Work Orders |
| `make_material_request()` | Generate Material Requests |
| `get_sub_assembly_items()` | Get sub-assembly items from BOM |
| `set_status()` | Update plan status |

### Work Order

| Method | Description |
|--------|-------------|
| `get_items_and_operations_from_bom()` | Load BOM data |
| `update_status()` | Update WO status based on progress |
| `create_job_card()` | Create Job Cards for operations |
| `update_work_order_qty()` | Update manufactured/transferred qty |
| `make_bom()` | Create BOM from Work Order |

### BOM

| Method | Description |
|--------|-------------|
| `get_routing()` | Load routing operations |
| `update_cost()` | Recalculate BOM cost |
| `get_bom_material_detail()` | Get material details with rate |

### Job Card

| Method | Description |
|--------|-------------|
| `validate_time_logs()` | Validate time entries |
| `get_overlap_for()` | Check workstation scheduling conflicts |
| `add_time_log()` | Add time log entry |
| `add_start_time_log()` | Start time tracking |

---

## Exception Classes

| Exception | When Raised |
|-----------|-------------|
| `OverProductionError` | Manufactured qty exceeds WO qty |
| `StockOverProductionError` | Stock entry qty exceeds allowed |
| `CapacityError` | Workstation capacity exceeded |
| `OperationTooLongError` | Operation time exceeds limits |
| `BOMRecursionError` | Circular BOM reference detected |
| `OverlapError` | Job Card time overlap detected |
| `OperationMismatchError` | Operation doesn't match WO |
| `OperationSequenceError` | Operations out of sequence |
| `JobCardCancelError` | Cannot cancel Job Card |

---

## Common Patterns

### Multi-Level BOM with Sub-Assembly

```python
from erpnext.manufacturing.doctype.bom.test_bom import create_nested_bom

# Define BOM tree structure
bom_tree = {
    "Laptop": {
        "Motherboard": {
            "CPU": {},
            "RAM": {}
        },
        "Screen": {},
        "Battery": {}
    }
}

# Create all BOMs automatically
parent_bom = create_nested_bom(bom_tree, prefix="")
```

### Production Plan with Subcontracting

```python
# Create Production Plan with sub-assembly items
plan = frappe.new_doc("Production Plan")
plan.company = "_Test Company"
# ... add sales orders ...
plan.insert()

# Get sub-assembly items
plan.get_sub_assembly_items()

# Set default suppliers for subcontracting
plan.set_default_supplier_for_subcontracting_order()

# Items marked as sub-contracted will generate Purchase Orders
plan.submit()
plan.make_work_order()
```

### Capacity Planning

```python
# Set workstation capacity
frappe.db.set_value("Workstation", "Assembly Station", "production_capacity", 2)

# Job Cards will validate against capacity
# Two simultaneous operations allowed on this workstation
```

---

## Reports Reference

| Report | Purpose |
|--------|---------|
| `bom_stock_report` | Check raw material availability for BOM |
| `bom_stock_calculated` | Calculate manufacturable qty based on stock |
| `bom_explorer` | Explore exploded BOM items |
| `bom_operations_time` | Analyze operation times |
| `bom_variance_report` | Compare actual vs planned usage |
| `production_analytics` | Production trends and analysis |
| `production_plan_summary` | Summary of production plans |
| `downtime_analysis` | Machine downtime analysis |
| `cost_of_poor_quality_report` | Quality cost tracking |
| `job_card_summary` | Job Card performance summary |
| `exponential_smoothing_forecasting` | Demand forecasting |

---

## Working with This Skill

### Beginner Level
1. Start with **BOM** creation - understand item structure
2. Create simple **Work Orders** directly from BOM
3. Track progress with **Stock Entries**

### Intermediate Level
1. Use **Production Plans** for batch planning
2. Implement **Routing** and **Operations**
3. Track **Job Cards** for shop floor execution

### Advanced Level
1. Multi-level BOM with **sub-assembly** planning
2. **Subcontracting** workflows
3. **Capacity planning** and workstation scheduling
4. Custom reports and analytics

---

## Reference Files

| Directory | Contents | Confidence |
|-----------|----------|------------|
| `references/api_reference/` | Complete Python/JS API docs | High |
| `references/documentation/` | Project README files | Medium |
| `references/patterns/` | Design patterns (Factory: 16, Observer: 7) | High |
| `references/test_examples/` | Real test cases from codebase | High |
| `references/config_patterns/` | Configuration patterns (93 files) | Medium |

### Key API Reference Files

- `work_order.md` - Complete Work Order API (90+ methods)
- `production_plan.md` - Production Planning API (50+ methods)
- `bom.md` - Bill of Materials API
- `job_card.md` - Job Card and time tracking API
- `workstation.md` - Workstation management API
- `routing.md` - Operation routing API
- `manufacturing_settings.md` - Module settings

---

## Integration Points

### With Stock Module
- Stock Entry for material transfer and manufacture
- Bin updates for reserved quantities
- Warehouse-based material tracking

### With Buying Module
- Material Request generation from Production Plan
- Subcontracting Purchase Orders
- Blanket Orders for long-term manufacturing contracts

### With Selling Module
- Sales Order linkage to Production Plan
- Work Order qty updates to Sales Order items
- Delivery planning based on manufacturing completion

### With Accounting Module
- Manufacturing cost tracking
- Work-in-Progress accounting
- Scrap and process loss accounting

---

**Generated from:** ERPNext Manufacturing Module Codebase Analysis
**Analysis Depth:** Full (108 files)
**Last Updated:** 2026-02-04
