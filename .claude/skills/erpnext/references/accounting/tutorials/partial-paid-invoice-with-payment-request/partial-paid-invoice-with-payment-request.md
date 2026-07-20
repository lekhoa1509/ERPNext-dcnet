# How To: Partial Paid Invoice With Payment Request

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test partial paid invoice with payment request

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `re`
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_request.payment_request`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.setup.utils`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`

**Setup Required:**
```python
for payment_gateway in payment_gateways:
    if not frappe.db.get_value('Payment Gateway', payment_gateway['gateway'], 'name'):
        frappe.get_doc(payment_gateway).insert(ignore_permissions=True)
for method in payment_method:
    if not frappe.db.get_value('Payment Gateway Account', {'payment_gateway': method['payment_gateway'], 'currency': method['currency'], 'company': method['company']}, 'name'):
        frappe.get_doc(method).insert(ignore_permissions=True)
send_email = patch('erpnext.accounts.doctype.payment_request.payment_request.PaymentRequest.send_email', return_value=None)
self.send_email = send_email.start()
self.addCleanup(send_email.stop)
get_payment_url = patch('erpnext.accounts.doctype.payment_request.payment_request.PaymentRequest.get_payment_url', return_value=PAYMENT_URL)
self.get_payment_url = get_payment_url.start()
self.addCleanup(get_payment_url.stop)
_get_payment_gateway_controller = patch('erpnext.accounts.doctype.payment_request.payment_request._get_payment_gateway_controller')
self._get_payment_gateway_controller = _get_payment_gateway_controller.start()
self.addCleanup(_get_payment_gateway_controller.stop)
```

## Step-by-Step Guide

### Step 1: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(currency='INR', qty=1, rate=5000)
```

### Step 2: Call si.save()

```python
si.save()
```

### Step 3: Call si.submit()

```python
si.submit()
```

### Step 4: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Bank - _TC')
```

### Step 5: Assign pe.reference_no = 'PAYEE0002'

```python
pe.reference_no = 'PAYEE0002'
```

### Step 6: Assign pe.reference_date = frappe.utils.nowdate(...)

```python
pe.reference_date = frappe.utils.nowdate()
```

### Step 7: Assign pe.paid_amount = 2500

```python
pe.paid_amount = 2500
```

### Step 8: Assign unknown.allocated_amount = 2500

```python
pe.references[0].allocated_amount = 2500
```

### Step 9: Call pe.save()

```python
pe.save()
```

### Step 10: Call pe.submit()

```python
pe.submit()
```

### Step 11: Call si.load_from_db()

```python
si.load_from_db()
```

### Step 12: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Sales Invoice', dn=si.name, mute_email=1)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, si.outstanding_amount)
```


## Complete Example

```python
# Setup
for payment_gateway in payment_gateways:
    if not frappe.db.get_value('Payment Gateway', payment_gateway['gateway'], 'name'):
        frappe.get_doc(payment_gateway).insert(ignore_permissions=True)
for method in payment_method:
    if not frappe.db.get_value('Payment Gateway Account', {'payment_gateway': method['payment_gateway'], 'currency': method['currency'], 'company': method['company']}, 'name'):
        frappe.get_doc(method).insert(ignore_permissions=True)
send_email = patch('erpnext.accounts.doctype.payment_request.payment_request.PaymentRequest.send_email', return_value=None)
self.send_email = send_email.start()
self.addCleanup(send_email.stop)
get_payment_url = patch('erpnext.accounts.doctype.payment_request.payment_request.PaymentRequest.get_payment_url', return_value=PAYMENT_URL)
self.get_payment_url = get_payment_url.start()
self.addCleanup(get_payment_url.stop)
_get_payment_gateway_controller = patch('erpnext.accounts.doctype.payment_request.payment_request._get_payment_gateway_controller')
self._get_payment_gateway_controller = _get_payment_gateway_controller.start()
self.addCleanup(_get_payment_gateway_controller.stop)

# Workflow
si = create_sales_invoice(currency='INR', qty=1, rate=5000)
si.save()
si.submit()
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Bank - _TC')
pe.reference_no = 'PAYEE0002'
pe.reference_date = frappe.utils.nowdate()
pe.paid_amount = 2500
pe.references[0].allocated_amount = 2500
pe.save()
pe.submit()
si.load_from_db()
pr = make_payment_request(dt='Sales Invoice', dn=si.name, mute_email=1)
self.assertEqual(pr.grand_total, si.outstanding_amount)
```

## Next Steps


---

*Source: test_payment_request.py:713 | Complexity: Advanced | Last updated: 2026-02-03*