# How To: Payment Cancel Process

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment cancel process

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

### Step 1: Assign so = make_sales_order(...)

```python
so = make_sales_order(currency='INR', qty=1, rate=1000)
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(so.advance_payment_status, 'Not Requested')
```

### Step 3: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Sales Order', dn=so.name, mute_email=1, submit_doc=1, return_doc=1)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Requested')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 1000)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, pr.grand_total)
```

### Step 7: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(so.advance_payment_status, 'Requested')
```

### Step 9: Assign pe = pr.create_payment_entry(...)

```python
pe = pr.create_payment_entry(submit=False)
```

### Step 10: Assign pe.paid_amount = 800

```python
pe.paid_amount = 800
```

### Step 11: Assign unknown.allocated_amount = 800

```python
pe.references[0].allocated_amount = 800
```

### Step 12: Call pe.submit()

```python
pe.submit()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].payment_request, pr.name)
```

### Step 14: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(so.advance_payment_status, 'Partially Paid')
```

### Step 16: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Partially Paid')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, 200)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 1000)
```

### Step 20: Call pe.cancel()

```python
pe.cancel()
```

### Step 21: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Requested')
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, 1000)
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 1000)
```

### Step 25: Call so.load_from_db()

```python
so.load_from_db()
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(so.advance_payment_status, 'Requested')
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
so = make_sales_order(currency='INR', qty=1, rate=1000)
self.assertEqual(so.advance_payment_status, 'Not Requested')
pr = make_payment_request(dt='Sales Order', dn=so.name, mute_email=1, submit_doc=1, return_doc=1)
self.assertEqual(pr.status, 'Requested')
self.assertEqual(pr.grand_total, 1000)
self.assertEqual(pr.outstanding_amount, pr.grand_total)
so.load_from_db()
self.assertEqual(so.advance_payment_status, 'Requested')
pe = pr.create_payment_entry(submit=False)
pe.paid_amount = 800
pe.references[0].allocated_amount = 800
pe.submit()
self.assertEqual(pe.references[0].payment_request, pr.name)
so.load_from_db()
self.assertEqual(so.advance_payment_status, 'Partially Paid')
pr.load_from_db()
self.assertEqual(pr.status, 'Partially Paid')
self.assertEqual(pr.outstanding_amount, 200)
self.assertEqual(pr.grand_total, 1000)
pe.cancel()
pr.load_from_db()
self.assertEqual(pr.status, 'Requested')
self.assertEqual(pr.outstanding_amount, 1000)
self.assertEqual(pr.grand_total, 1000)
so.load_from_db()
self.assertEqual(so.advance_payment_status, 'Requested')
```

## Next Steps


---

*Source: test_payment_request.py:668 | Complexity: Advanced | Last updated: 2026-02-03*