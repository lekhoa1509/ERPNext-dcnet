# How To: 02 Various Filters And Output

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test 02 various filters and output

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.accounts_receivable_summary.accounts_receivable_summary`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Assign filters = value

```python
filters = {'company': self.company, 'customer': self.customer, 'posting_date': today(), 'range': '30, 60, 90, 120'}
```

### Step 2: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=200, price_list_rate=200)
```

### Step 3: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry(si.doctype, si.name)
```

### Step 4: Assign pe.paid_amount = 150

```python
pe.paid_amount = 150
```

### Step 5: Assign unknown.allocated_amount = 150

```python
pe.references[0].allocated_amount = 150
```

### Step 6: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 7: Assign unknown = value

```python
customer_group, customer_territory = frappe.db.get_all('Customer', filters={'name': self.customer}, fields=['customer_group', 'territory'], as_list=True)[0]
```

### Step 8: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 9: Assign rpt_output = value

```python
rpt_output = report[1]
```

### Step 10: Assign expected_data = value

```python
expected_data = {'party_type': 'Customer', 'advance': 0, 'party': self.customer, 'party_name': self.customer, 'invoiced': 200.0, 'paid': 150.0, 'credit_note': 0.0, 'outstanding': 50.0, 'range1': 50.0, 'range2': 0.0, 'range3': 0.0, 'range4': 0.0, 'range5': 0.0, 'total_due': 50.0, 'future_amount': 0.0, 'sales_person': [], 'currency': si.currency, 'territory': customer_territory, 'customer_group': customer_group}
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(rpt_output), 1)
```

### Step 12: Call self.assertDictEqual()

```python
self.assertDictEqual(rpt_output[0], expected_data)
```

### Step 13: Call filters.update()

```python
filters.update({'show_gl_balance': True})
```

### Step 14: Call expected_data.update()

```python
expected_data.update({'gl_balance': 50.0, 'diff': 0.0})
```

### Step 15: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 16: Assign rpt_output = value

```python
rpt_output = report[1]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(len(rpt_output), 1)
```

### Step 18: Call self.assertDictEqual()

```python
self.assertDictEqual(rpt_output[0], expected_data)
```

### Step 19: Call filters.update()

```python
filters.update({'show_future_payments': True})
```

### Step 20: Call expected_data.update()

```python
expected_data.update({'remaining_balance': 50.0})
```

### Step 21: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 22: Assign rpt_output = value

```python
rpt_output = report[1]
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(len(rpt_output), 1)
```

### Step 24: Call self.assertDictEqual()

```python
self.assertDictEqual(rpt_output[0], expected_data)
```

### Step 25: Assign pe = get_payment_entry.save.submit(...)

```python
pe = get_payment_entry(si.doctype, si.name).save().submit()
```

### Step 26: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 27: Assign rpt_output = value

```python
rpt_output = report[1]
```

### Step 28: Call self.assertEqual()

```python
self.assertEqual(len(rpt_output), 0)
```


## Complete Example

```python
# Workflow
filters = {'company': self.company, 'customer': self.customer, 'posting_date': today(), 'range': '30, 60, 90, 120'}
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=200, price_list_rate=200)
pe = get_payment_entry(si.doctype, si.name)
pe.paid_amount = 150
pe.references[0].allocated_amount = 150
pe.save().submit()
customer_group, customer_territory = frappe.db.get_all('Customer', filters={'name': self.customer}, fields=['customer_group', 'territory'], as_list=True)[0]
report = execute(filters)
rpt_output = report[1]
expected_data = {'party_type': 'Customer', 'advance': 0, 'party': self.customer, 'party_name': self.customer, 'invoiced': 200.0, 'paid': 150.0, 'credit_note': 0.0, 'outstanding': 50.0, 'range1': 50.0, 'range2': 0.0, 'range3': 0.0, 'range4': 0.0, 'range5': 0.0, 'total_due': 50.0, 'future_amount': 0.0, 'sales_person': [], 'currency': si.currency, 'territory': customer_territory, 'customer_group': customer_group}
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
filters.update({'show_gl_balance': True})
expected_data.update({'gl_balance': 50.0, 'diff': 0.0})
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
filters.update({'show_future_payments': True})
expected_data.update({'remaining_balance': 50.0})
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
pe = get_payment_entry(si.doctype, si.name).save().submit()
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 0)
```

## Next Steps


---

*Source: test_accounts_receivable_summary.py:116 | Complexity: Advanced | Last updated: 2026-02-03*