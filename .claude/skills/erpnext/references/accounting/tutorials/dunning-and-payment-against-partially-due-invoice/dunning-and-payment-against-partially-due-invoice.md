# How To: Dunning And Payment Against Partially Due Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Create SI with first installment overdue. Check impact of Dunning and Payment Entry.

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.model`
- `frappe.tests`
- `frappe.utils`
- `erpnext`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`


## Step-by-Step Guide

### Step 1: '\n\t\tCreate SI with first installment overdue. Check impact of Dunning and Payment Entry.\n\t\t'

```python
'\n\t\tCreate SI with first installment overdue. Check impact of Dunning and Payment Entry.\n\t\t'
```

### Step 2: Call create_payment_terms_template_for_dunning()

```python
create_payment_terms_template_for_dunning()
```

### Step 3: Assign sales_invoice = create_sales_invoice_against_cost_center(...)

```python
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=100, do_not_submit=True)
```

### Step 4: Assign sales_invoice.payment_terms_template = '_Test 50-50 for Dunning'

```python
sales_invoice.payment_terms_template = '_Test 50-50 for Dunning'
```

### Step 5: Call sales_invoice.submit()

```python
sales_invoice.submit()
```

### Step 6: Assign dunning = create_dunning_from_sales_invoice(...)

```python
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(dunning.overdue_payments), 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(dunning.overdue_payments[0].payment_term, '_Test Payment Term 1 for Dunning')
```

### Step 9: Call dunning.submit()

```python
dunning.submit()
```

### Step 10: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Dunning', dunning.name)
```

### Step 11: Assign unknown = value

```python
pe.reference_no, pe.reference_date = ('2', nowdate())
```

### Step 12: Call pe.insert()

```python
pe.insert()
```

### Step 13: Call pe.submit()

```python
pe.submit()
```

### Step 14: Call sales_invoice.load_from_db()

```python
sales_invoice.load_from_db()
```

### Step 15: Call dunning.load_from_db()

```python
dunning.load_from_db()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(sales_invoice.status, 'Partly Paid')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(sales_invoice.payment_schedule[0].outstanding, 0)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(dunning.status, 'Resolved')
```

### Step 19: Call pe.cancel()

```python
pe.cancel()
```

### Step 20: Call sales_invoice.reload()

```python
sales_invoice.reload()
```

### Step 21: Call dunning.reload()

```python
dunning.reload()
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(sales_invoice.status, 'Overdue')
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(dunning.status, 'Unresolved')
```


## Complete Example

```python
# Workflow
'\n\t\tCreate SI with first installment overdue. Check impact of Dunning and Payment Entry.\n\t\t'
create_payment_terms_template_for_dunning()
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=100, do_not_submit=True)
sales_invoice.payment_terms_template = '_Test 50-50 for Dunning'
sales_invoice.submit()
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
self.assertEqual(len(dunning.overdue_payments), 1)
self.assertEqual(dunning.overdue_payments[0].payment_term, '_Test Payment Term 1 for Dunning')
dunning.submit()
pe = get_payment_entry('Dunning', dunning.name)
pe.reference_no, pe.reference_date = ('2', nowdate())
pe.insert()
pe.submit()
sales_invoice.load_from_db()
dunning.load_from_db()
self.assertEqual(sales_invoice.status, 'Partly Paid')
self.assertEqual(sales_invoice.payment_schedule[0].outstanding, 0)
self.assertEqual(dunning.status, 'Resolved')
pe.cancel()
sales_invoice.reload()
dunning.reload()
self.assertEqual(sales_invoice.status, 'Overdue')
self.assertEqual(dunning.status, 'Unresolved')
```

## Next Steps


---

*Source: test_dunning.py:104 | Complexity: Advanced | Last updated: 2026-02-03*