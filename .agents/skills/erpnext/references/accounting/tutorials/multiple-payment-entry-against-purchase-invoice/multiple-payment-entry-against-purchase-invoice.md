# How To: Multiple Payment Entry Against Purchase Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multiple payment entry against purchase invoice

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

### Step 1: Assign purchase_invoice = make_purchase_invoice(...)

```python
purchase_invoice = make_purchase_invoice(supplier='_Test Supplier USD', debit_to='_Test Payable USD - _TC', currency='USD', conversion_rate=50)
```

### Step 2: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Purchase Invoice', party_type='Supplier', party='_Test Supplier USD', dn=purchase_invoice.name, recipient_id='user@example.com', mute_email=1, payment_gateway_account='_Test Gateway - USD - _TC', return_doc=1)
```

### Step 3: Assign pr.grand_total = value

```python
pr.grand_total = pr.grand_total / 2
```

### Step 4: Call pr.submit()

```python
pr.submit()
```

### Step 5: Call pr.create_payment_entry()

```python
pr.create_payment_entry()
```

### Step 6: Call purchase_invoice.load_from_db()

```python
purchase_invoice.load_from_db()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(purchase_invoice.status, 'Partly Paid')
```

### Step 8: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Purchase Invoice', party_type='Supplier', party='_Test Supplier USD', dn=purchase_invoice.name, recipient_id='user@example.com', mute_email=1, payment_gateway_account='_Test Gateway - USD - _TC', return_doc=1)
```

### Step 9: Call pr.save()

```python
pr.save()
```

### Step 10: Call pr.submit()

```python
pr.submit()
```

### Step 11: Call pr.create_payment_entry()

```python
pr.create_payment_entry()
```

### Step 12: Call purchase_invoice.load_from_db()

```python
purchase_invoice.load_from_db()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(purchase_invoice.status, 'Paid')
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
purchase_invoice = make_purchase_invoice(supplier='_Test Supplier USD', debit_to='_Test Payable USD - _TC', currency='USD', conversion_rate=50)
pr = make_payment_request(dt='Purchase Invoice', party_type='Supplier', party='_Test Supplier USD', dn=purchase_invoice.name, recipient_id='user@example.com', mute_email=1, payment_gateway_account='_Test Gateway - USD - _TC', return_doc=1)
pr.grand_total = pr.grand_total / 2
pr.submit()
pr.create_payment_entry()
purchase_invoice.load_from_db()
self.assertEqual(purchase_invoice.status, 'Partly Paid')
pr = make_payment_request(dt='Purchase Invoice', party_type='Supplier', party='_Test Supplier USD', dn=purchase_invoice.name, recipient_id='user@example.com', mute_email=1, payment_gateway_account='_Test Gateway - USD - _TC', return_doc=1)
pr.save()
pr.submit()
pr.create_payment_entry()
purchase_invoice.load_from_db()
self.assertEqual(purchase_invoice.status, 'Paid')
```

## Next Steps


---

*Source: test_payment_request.py:252 | Complexity: Advanced | Last updated: 2026-02-03*