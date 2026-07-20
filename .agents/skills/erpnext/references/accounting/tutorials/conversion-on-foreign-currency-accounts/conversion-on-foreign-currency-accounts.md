# How To: Conversion On Foreign Currency Accounts

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test conversion on foreign currency accounts

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

### Step 1: Assign po_doc = create_purchase_order(...)

```python
po_doc = create_purchase_order(supplier='_Test Supplier USD', currency='USD', do_not_submit=1)
```

### Step 2: Assign po_doc.conversion_rate = 80

```python
po_doc.conversion_rate = 80
```

### Step 3: Assign unknown.qty = 1

```python
po_doc.items[0].qty = 1
```

### Step 4: Assign unknown.rate = 10

```python
po_doc.items[0].rate = 10
```

### Step 5: Call po_doc.save.submit()

```python
po_doc.save().submit()
```

### Step 6: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt=po_doc.doctype, dn=po_doc.name, recipient_id='nabin@erpnext.com')
```

### Step 7: Assign pr = frappe.get_doc.save.submit(...)

```python
pr = frappe.get_doc(pr).save().submit()
```

### Step 8: Assign pe = pr.create_payment_entry(...)

```python
pe = pr.create_payment_entry()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(pe.base_paid_amount, 800)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pe.paid_amount, 800)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pe.base_received_amount, 800)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pe.received_amount, 10)
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
po_doc = create_purchase_order(supplier='_Test Supplier USD', currency='USD', do_not_submit=1)
po_doc.conversion_rate = 80
po_doc.items[0].qty = 1
po_doc.items[0].rate = 10
po_doc.save().submit()
pr = make_payment_request(dt=po_doc.doctype, dn=po_doc.name, recipient_id='nabin@erpnext.com')
pr = frappe.get_doc(pr).save().submit()
pe = pr.create_payment_entry()
self.assertEqual(pe.base_paid_amount, 800)
self.assertEqual(pe.paid_amount, 800)
self.assertEqual(pe.base_received_amount, 800)
self.assertEqual(pe.received_amount, 10)
```

## Next Steps


---

*Source: test_payment_request.py:413 | Complexity: Advanced | Last updated: 2026-02-03*