# How To: Multiple Payment Entries Against Sales Order

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multiple payment entries against sales order

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
so = make_sales_order()
```

### Step 2: Assign pr1 = make_payment_request(...)

```python
pr1 = make_payment_request(dt='Sales Order', dn=so.name, recipient_id='nabin@erpnext.com', return_doc=1)
```

### Step 3: Assign pr1.grand_total = 200

```python
pr1.grand_total = 200
```

### Step 4: Call pr1.submit()

```python
pr1.submit()
```

### Step 5: Assign pr2 = make_payment_request(...)

```python
pr2 = make_payment_request(dt='Sales Order', dn=so.name, recipient_id='nabin@erpnext.com', return_doc=1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(pr2.grand_total, 800)
```

### Step 7: Assign pr2.grand_total = 900

```python
pr2.grand_total = 900
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, pr2.save)
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
so = make_sales_order()
pr1 = make_payment_request(dt='Sales Order', dn=so.name, recipient_id='nabin@erpnext.com', return_doc=1)
pr1.grand_total = 200
pr1.submit()
pr2 = make_payment_request(dt='Sales Order', dn=so.name, recipient_id='nabin@erpnext.com', return_doc=1)
self.assertEqual(pr2.grand_total, 800)
pr2.grand_total = 900
self.assertRaises(frappe.ValidationError, pr2.save)
```

## Next Steps


---

*Source: test_payment_request.py:391 | Complexity: Advanced | Last updated: 2026-02-03*