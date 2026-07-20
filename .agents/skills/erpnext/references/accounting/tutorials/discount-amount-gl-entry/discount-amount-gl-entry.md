# How To: Discount Amount Gl Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test discount amount gl entry

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `copy`
- `json`
- `frappe`
- `frappe`
- `frappe.model.dynamic_links`
- `frappe.tests`
- `frappe.utils`
- `erpnext`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.mode_of_payment.test_mode_of_payment`
- `erpnext.accounts.doctype.pos_profile.test_pos_profile`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.utils`
- `erpnext.assets.doctype.asset.depreciation`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule`
- `erpnext.controllers.accounts_controller`
- `erpnext.controllers.taxes_and_totals`
- `erpnext.exceptions`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.get_item_details`
- `erpnext.stock.utils`
- `erpnext.tests.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry`
- `frappe`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `time`
- `time`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.doctype.cost_center_allocation.test_cost_center_allocation`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.accounts.doctype.accounting_dimension.test_accounting_dimension`
- `erpnext.accounts.doctype.shipping_rule.test_shipping_rule`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.projects.doctype.project.test_project`
- `erpnext.accounts.doctype.repost_accounting_ledger.test_repost_accounting_ledger`
- `erpnext.accounts.doctype.opening_invoice_creation_tool.test_opening_invoice_creation_tool`
- `erpnext.accounts.doctype.party_link.party_link`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.accounts.doctype.opening_invoice_creation_tool.test_opening_invoice_creation_tool`
- `erpnext.accounts.doctype.party_link.party_link`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.accounts.doctype.opening_invoice_creation_tool.test_opening_invoice_creation_tool`
- `erpnext.accounts.doctype.party_link.party_link`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.loyalty_program.test_loyalty_program`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `frappe.model.trace`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `frappe.model.mapper`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.opening_invoice_creation_tool.test_opening_invoice_creation_tool`
- `erpnext.accounts.doctype.party_link.party_link`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.setup.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.opening_invoice_creation_tool.test_opening_invoice_creation_tool`
- `erpnext.accounts.doctype.party_link.party_link`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.setup.utils`
- `copy`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.repost_accounting_ledger.test_repost_accounting_ledger`

**Setup Required:**
```python
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)
```

## Step-by-Step Guide

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company', 'round_off_account', 'Round Off - _TC')
```

### Step 2: Assign si = frappe.copy_doc(...)

```python
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][3])
```

### Step 3: Assign si.discount_amount = 104.94

```python
si.discount_amount = 104.94
```

### Step 4: Call si.append()

```python
si.append('taxes', {'doctype': 'Sales Taxes and Charges', 'charge_type': 'On Previous Row Amount', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 10, 'row_id': 8})
```

### Step 5: Call si.insert()

```python
si.insert()
```

### Step 6: Call si.submit()

```python
si.submit()
```

### Step 7: Assign gl_entries = frappe.db.sql(...)

```python
gl_entries = frappe.db.sql("select account, debit, credit\n\t\t\tfrom `tabGL Entry` where voucher_type='Sales Invoice' and voucher_no=%s\n\t\t\torder by account asc", si.name, as_dict=1)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 9: Assign expected_values = dict(...)

```python
expected_values = dict(((d[0], d) for d in [[si.debit_to, 1500, 0.0], [self.globalTestRecords['Sales Invoice'][3]['items'][0]['income_account'], 0.0, 1163.45], [self.globalTestRecords['Sales Invoice'][3]['taxes'][0]['account_head'], 0.0, 130.31], [self.globalTestRecords['Sales Invoice'][3]['taxes'][1]['account_head'], 0.0, 2.61], [self.globalTestRecords['Sales Invoice'][3]['taxes'][2]['account_head'], 0.0, 1.3], [self.globalTestRecords['Sales Invoice'][3]['taxes'][3]['account_head'], 0.0, 25.95], [self.globalTestRecords['Sales Invoice'][3]['taxes'][4]['account_head'], 0.0, 145.43], [self.globalTestRecords['Sales Invoice'][3]['taxes'][5]['account_head'], 0.0, 116.34], [self.globalTestRecords['Sales Invoice'][3]['taxes'][6]['account_head'], 0.0, 100], [self.globalTestRecords['Sales Invoice'][3]['taxes'][7]['account_head'], 168.54, 0.0], ['_Test Account Service Tax - _TC', 16.85, 0.0], ['Round Off - _TC', 0.01, 0.0]]))
```

### Step 10: Call si.cancel()

```python
si.cancel()
```

### Step 11: Assign gle = frappe.db.sql(...)

```python
gle = frappe.db.sql("select * from `tabGL Entry`\n\t\t\twhere voucher_type='Sales Invoice' and voucher_no=%s", si.name)
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(gle)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(expected_values[gle.account][0], gle.account)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(expected_values[gle.account][1], gle.debit)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(expected_values[gle.account][2], gle.credit)
```


## Complete Example

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

# Workflow
frappe.db.set_value('Company', '_Test Company', 'round_off_account', 'Round Off - _TC')
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][3])
si.discount_amount = 104.94
si.append('taxes', {'doctype': 'Sales Taxes and Charges', 'charge_type': 'On Previous Row Amount', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 10, 'row_id': 8})
si.insert()
si.submit()
gl_entries = frappe.db.sql("select account, debit, credit\n\t\t\tfrom `tabGL Entry` where voucher_type='Sales Invoice' and voucher_no=%s\n\t\t\torder by account asc", si.name, as_dict=1)
self.assertTrue(gl_entries)
expected_values = dict(((d[0], d) for d in [[si.debit_to, 1500, 0.0], [self.globalTestRecords['Sales Invoice'][3]['items'][0]['income_account'], 0.0, 1163.45], [self.globalTestRecords['Sales Invoice'][3]['taxes'][0]['account_head'], 0.0, 130.31], [self.globalTestRecords['Sales Invoice'][3]['taxes'][1]['account_head'], 0.0, 2.61], [self.globalTestRecords['Sales Invoice'][3]['taxes'][2]['account_head'], 0.0, 1.3], [self.globalTestRecords['Sales Invoice'][3]['taxes'][3]['account_head'], 0.0, 25.95], [self.globalTestRecords['Sales Invoice'][3]['taxes'][4]['account_head'], 0.0, 145.43], [self.globalTestRecords['Sales Invoice'][3]['taxes'][5]['account_head'], 0.0, 116.34], [self.globalTestRecords['Sales Invoice'][3]['taxes'][6]['account_head'], 0.0, 100], [self.globalTestRecords['Sales Invoice'][3]['taxes'][7]['account_head'], 168.54, 0.0], ['_Test Account Service Tax - _TC', 16.85, 0.0], ['Round Off - _TC', 0.01, 0.0]]))
for gle in gl_entries:
    self.assertEqual(expected_values[gle.account][0], gle.account)
    self.assertEqual(expected_values[gle.account][1], gle.debit)
    self.assertEqual(expected_values[gle.account][2], gle.credit)
si.cancel()
gle = frappe.db.sql("select * from `tabGL Entry`\n\t\t\twhere voucher_type='Sales Invoice' and voucher_no=%s", si.name)
self.assertTrue(gle)
```

## Next Steps


---

*Source: test_sales_invoice.py:476 | Complexity: Advanced | Last updated: 2026-02-03*