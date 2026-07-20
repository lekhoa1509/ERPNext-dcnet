# How To: Get Mode Of Payments

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get mode of payments

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.report.sales_payment_summary.sales_payment_summary`


## Step-by-Step Guide

### Step 1: Assign filters = get_filters(...)

```python
filters = get_filters()
```

### Step 2: Assign mop = get_mode_of_payments(...)

```python
mop = get_mode_of_payments(filters)
```

### Step 3: Call self.assertTrue()

```python
self.assertTrue('Credit Card' in next(iter(mop.values())))
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue('Cash' in next(iter(mop.values())))
```

### Step 5: Assign payment_entries = frappe.get_all(...)

```python
payment_entries = frappe.get_all('Payment Entry', filters={'mode_of_payment': 'Cash', 'docstatus': 1}, fields=['name', 'docstatus'])
```

### Step 6: Assign mop = get_mode_of_payments(...)

```python
mop = get_mode_of_payments(filters)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue('Credit Card' in next(iter(mop.values())))
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue('Cash' not in next(iter(mop.values())))
```

### Step 9: Assign si = create_sales_invoice_record(...)

```python
si = create_sales_invoice_record()
```

### Step 10: Call si.insert()

```python
si.insert()
```

### Step 11: Call si.submit()

```python
si.submit()
```

### Step 12: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Sales Invoice', si.name, bank_account=bank_account)
```

### Step 13: Assign pe.reference_no = '_Test'

```python
pe.reference_no = '_Test'
```

### Step 14: Assign pe.reference_date = today(...)

```python
pe.reference_date = today()
```

### Step 15: Assign pe.mode_of_payment = mode_of_payment

```python
pe.mode_of_payment = mode_of_payment
```

### Step 16: Call pe.insert()

```python
pe.insert()
```

### Step 17: Call pe.submit()

```python
pe.submit()
```

### Step 18: Assign pe = frappe.get_doc(...)

```python
pe = frappe.get_doc('Payment Entry', payment_entry.name)
```

### Step 19: Call pe.cancel()

```python
pe.cancel()
```

### Step 20: Assign bank_account = '_Test Cash - _TC'

```python
bank_account = '_Test Cash - _TC'
```

### Step 21: Assign mode_of_payment = 'Cash'

```python
mode_of_payment = 'Cash'
```

### Step 22: Assign bank_account = '_Test Bank - _TC'

```python
bank_account = '_Test Bank - _TC'
```

### Step 23: Assign mode_of_payment = 'Credit Card'

```python
mode_of_payment = 'Credit Card'
```


## Complete Example

```python
# Workflow
filters = get_filters()
for _dummy in range(2):
    si = create_sales_invoice_record()
    si.insert()
    si.submit()
    if int(si.name[-3:]) % 2 == 0:
        bank_account = '_Test Cash - _TC'
        mode_of_payment = 'Cash'
    else:
        bank_account = '_Test Bank - _TC'
        mode_of_payment = 'Credit Card'
    pe = get_payment_entry('Sales Invoice', si.name, bank_account=bank_account)
    pe.reference_no = '_Test'
    pe.reference_date = today()
    pe.mode_of_payment = mode_of_payment
    pe.insert()
    pe.submit()
mop = get_mode_of_payments(filters)
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' in next(iter(mop.values())))
payment_entries = frappe.get_all('Payment Entry', filters={'mode_of_payment': 'Cash', 'docstatus': 1}, fields=['name', 'docstatus'])
for payment_entry in payment_entries:
    pe = frappe.get_doc('Payment Entry', payment_entry.name)
    pe.cancel()
mop = get_mode_of_payments(filters)
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' not in next(iter(mop.values())))
```

## Next Steps


---

*Source: test_sales_payment_summary.py:32 | Complexity: Advanced | Last updated: 2026-02-03*