# How To: Make Sales Order Terms Copied

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make sales order terms copied

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

### Step 1: Assign quotation = frappe.copy_doc(...)

```python
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
```

### Step 2: Assign quotation.transaction_date = nowdate(...)

```python
quotation.transaction_date = nowdate()
```

### Step 3: Assign quotation.valid_till = add_months(...)

```python
quotation.valid_till = add_months(quotation.transaction_date, 1)
```

### Step 4: Call quotation.insert()

```python
quotation.insert()
```

### Step 5: Call quotation.submit()

```python
quotation.submit()
```

### Step 6: Assign sales_order = make_sales_order(...)

```python
sales_order = make_sales_order(quotation.name)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(sales_order.get('payment_schedule'))
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.quotation.quotation import make_sales_order
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.insert()
quotation.submit()
sales_order = make_sales_order(quotation.name)
self.assertTrue(sales_order.get('payment_schedule'))
```

## Next Steps


---

*Source: test_quotation.py:145 | Complexity: Intermediate | Last updated: 2026-02-04*