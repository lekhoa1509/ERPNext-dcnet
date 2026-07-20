# How To: Maintain Rate In Sales Cycle Is Enforced

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test maintain rate in sales cycle is enforced

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.accounts_controller`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.quotation.quotation`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign maintain_rate = frappe.db.get_single_value(...)

```python
maintain_rate = frappe.db.get_single_value('Selling Settings', 'maintain_same_sales_rate')
```

### Step 2: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Selling Settings', 'maintain_same_sales_rate', 1)
```

### Step 3: Assign quotation = frappe.copy_doc(...)

```python
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
```

### Step 4: Assign quotation.transaction_date = nowdate(...)

```python
quotation.transaction_date = nowdate()
```

### Step 5: Assign quotation.valid_till = add_months(...)

```python
quotation.valid_till = add_months(quotation.transaction_date, 1)
```

### Step 6: Call quotation.insert()

```python
quotation.insert()
```

### Step 7: Call quotation.submit()

```python
quotation.submit()
```

### Step 8: Assign sales_order = make_sales_order(...)

```python
sales_order = make_sales_order(quotation.name)
```

### Step 9: Assign unknown.rate = 1

```python
sales_order.items[0].rate = 1
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, sales_order.save)
```

### Step 11: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Selling Settings', 'maintain_same_sales_rate', maintain_rate)
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.quotation.quotation import make_sales_order
maintain_rate = frappe.db.get_single_value('Selling Settings', 'maintain_same_sales_rate')
frappe.db.set_single_value('Selling Settings', 'maintain_same_sales_rate', 1)
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.insert()
quotation.submit()
sales_order = make_sales_order(quotation.name)
sales_order.items[0].rate = 1
self.assertRaises(frappe.ValidationError, sales_order.save)
frappe.db.set_single_value('Selling Settings', 'maintain_same_sales_rate', maintain_rate)
```

## Next Steps


---

*Source: test_quotation.py:223 | Complexity: Advanced | Last updated: 2026-02-04*