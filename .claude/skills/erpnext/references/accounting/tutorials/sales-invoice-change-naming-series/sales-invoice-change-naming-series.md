# How To: Sales Invoice Change Naming Series

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sales invoice change naming series

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

### Step 1: Assign si = frappe.copy_doc(...)

```python
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][2])
```

### Step 2: Call si.insert()

```python
si.insert()
```

### Step 3: Assign si.naming_series = 'TEST-'

```python
si.naming_series = 'TEST-'
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(frappe.CannotChangeConstantError, si.save)
```

### Step 5: Assign si = frappe.copy_doc(...)

```python
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][1])
```

### Step 6: Call si.insert()

```python
si.insert()
```

### Step 7: Assign si.naming_series = 'TEST-'

```python
si.naming_series = 'TEST-'
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(frappe.CannotChangeConstantError, si.save)
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
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][2])
si.insert()
si.naming_series = 'TEST-'
self.assertRaises(frappe.CannotChangeConstantError, si.save)
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][1])
si.insert()
si.naming_series = 'TEST-'
self.assertRaises(frappe.CannotChangeConstantError, si.save)
```

## Next Steps


---

*Source: test_sales_invoice.py:138 | Complexity: Advanced | Last updated: 2026-02-03*