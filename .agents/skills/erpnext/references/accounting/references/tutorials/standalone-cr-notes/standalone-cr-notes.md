# How To: Standalone Cr Notes

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Standalone cr notes will be reported as usual

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.gross_profit.gross_profit`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`

**Setup Required:**
```python
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()
```

## Step-by-Step Guide

### Step 1: '\n\t\tStandalone cr notes will be reported as usual\n\t\t'

```python
'\n\t\tStandalone cr notes will be reported as usual\n\t\t'
```

### Step 2: Assign sinv = self.create_sales_invoice(...)

```python
sinv = self.create_sales_invoice(qty=-1, rate=100, posting_date=nowdate(), do_not_save=True, do_not_submit=True)
```

### Step 3: Assign sinv.is_return = 1

```python
sinv.is_return = 1
```

### Step 4: Assign sinv = sinv.save.submit(...)

```python
sinv = sinv.save().submit()
```

### Step 5: Assign filters = frappe._dict(...)

```python
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice', include_returned_invoices=1)
```

### Step 6: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 7: Assign expected_entry = value

```python
expected_entry = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': -1.0, 'avg._selling_rate': 100.0, 'valuation_rate': 0.0, 'selling_amount': -100.0, 'buying_amount': 0.0, 'gross_profit': -100.0, 'gross_profit_%': 100.0}
```

### Step 8: Assign gp_entry = value

```python
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
```

### Step 9: Assign report_output = value

```python
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry}
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(report_output, expected_entry)
```


## Complete Example

```python
# Setup
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()

# Workflow
'\n\t\tStandalone cr notes will be reported as usual\n\t\t'
sinv = self.create_sales_invoice(qty=-1, rate=100, posting_date=nowdate(), do_not_save=True, do_not_submit=True)
sinv.is_return = 1
sinv = sinv.save().submit()
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice', include_returned_invoices=1)
columns, data = execute(filters=filters)
expected_entry = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': -1.0, 'avg._selling_rate': 100.0, 'valuation_rate': 0.0, 'selling_amount': -100.0, 'buying_amount': 0.0, 'gross_profit': -100.0, 'gross_profit_%': 100.0}
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry}
self.assertEqual(report_output, expected_entry)
```

## Next Steps


---

*Source: test_gross_profit.py:438 | Complexity: Advanced | Last updated: 2026-02-03*