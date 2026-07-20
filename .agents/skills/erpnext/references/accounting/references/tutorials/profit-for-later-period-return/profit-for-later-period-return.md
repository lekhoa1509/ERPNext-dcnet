# How To: Profit For Later Period Return

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test profit for later period return

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

### Step 1: Assign unknown = value

```python
month_start_date, month_end_date = (get_first_day(nowdate()), get_last_day(nowdate()))
```

### Step 2: Assign sinv = self.create_sales_invoice(...)

```python
sinv = self.create_sales_invoice(qty=1, rate=100, do_not_save=True, do_not_submit=True)
```

### Step 3: Assign sinv.set_posting_time = 1

```python
sinv.set_posting_time = 1
```

### Step 4: Assign sinv.posting_date = month_start_date

```python
sinv.posting_date = month_start_date
```

### Step 5: Call sinv.save.submit()

```python
sinv.save().submit()
```

### Step 6: Assign cr_note = make_sales_return(...)

```python
cr_note = make_sales_return(sinv.name)
```

### Step 7: Assign cr_note.set_posting_time = 1

```python
cr_note.set_posting_time = 1
```

### Step 8: Assign cr_note.posting_date = add_days(...)

```python
cr_note.posting_date = add_days(month_end_date, 1)
```

### Step 9: Call cr_note.save.submit()

```python
cr_note.save().submit()
```

### Step 10: Assign filters = frappe._dict(...)

```python
filters = frappe._dict(company=self.company, from_date=month_start_date, to_date=month_end_date, group_by='Invoice')
```

### Step 11: Assign unknown = execute(...)

```python
_, data = execute(filters=filters)
```

### Step 12: Assign total = value

```python
total = data[-1]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(total.selling_amount, 100.0)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(total.buying_amount, 0.0)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(total.gross_profit, 100.0)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(total.get('gross_profit_%'), 100.0)
```

### Step 17: Call filters.update()

```python
filters.update(to_date=add_days(month_end_date, 1))
```

### Step 18: Assign unknown = execute(...)

```python
_, data = execute(filters=filters)
```

### Step 19: Assign total = value

```python
total = data[-1]
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(total.selling_amount, 0.0)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(total.buying_amount, 0.0)
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(total.gross_profit, 0.0)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(total.get('gross_profit_%'), 0.0)
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
month_start_date, month_end_date = (get_first_day(nowdate()), get_last_day(nowdate()))
sinv = self.create_sales_invoice(qty=1, rate=100, do_not_save=True, do_not_submit=True)
sinv.set_posting_time = 1
sinv.posting_date = month_start_date
sinv.save().submit()
cr_note = make_sales_return(sinv.name)
cr_note.set_posting_time = 1
cr_note.posting_date = add_days(month_end_date, 1)
cr_note.save().submit()
filters = frappe._dict(company=self.company, from_date=month_start_date, to_date=month_end_date, group_by='Invoice')
_, data = execute(filters=filters)
total = data[-1]
self.assertEqual(total.selling_amount, 100.0)
self.assertEqual(total.buying_amount, 0.0)
self.assertEqual(total.gross_profit, 100.0)
self.assertEqual(total.get('gross_profit_%'), 100.0)
filters.update(to_date=add_days(month_end_date, 1))
_, data = execute(filters=filters)
total = data[-1]
self.assertEqual(total.selling_amount, 0.0)
self.assertEqual(total.buying_amount, 0.0)
self.assertEqual(total.gross_profit, 0.0)
self.assertEqual(total.get('gross_profit_%'), 0.0)
```

## Next Steps


---

*Source: test_gross_profit.py:649 | Complexity: Advanced | Last updated: 2026-02-03*