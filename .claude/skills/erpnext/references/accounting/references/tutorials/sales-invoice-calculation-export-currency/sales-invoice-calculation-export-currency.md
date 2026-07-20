# How To: Sales Invoice Calculation Export Currency

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sales invoice calculation export currency

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

### Step 2: Assign si.currency = 'USD'

```python
si.currency = 'USD'
```

### Step 3: Assign si.conversion_rate = 50

```python
si.conversion_rate = 50
```

### Step 4: Assign unknown.rate = 1

```python
si.get('items')[0].rate = 1
```

### Step 5: Assign unknown.price_list_rate = 1

```python
si.get('items')[0].price_list_rate = 1
```

### Step 6: Assign unknown.rate = 3

```python
si.get('items')[1].rate = 3
```

### Step 7: Assign unknown.price_list_rate = 3

```python
si.get('items')[1].price_list_rate = 3
```

### Step 8: Assign unknown.tax_amount = 2

```python
si.get('taxes')[0].tax_amount = 2
```

### Step 9: Call si.insert()

```python
si.insert()
```

### Step 10: Assign expected_values = value

```python
expected_values = {'keys': ['price_list_rate', 'discount_percentage', 'rate', 'amount', 'base_price_list_rate', 'base_rate', 'base_amount'], '_Test Item Home Desktop 100': [1, 0, 1, 10, 50, 50, 500], '_Test Item Home Desktop 200': [3, 0, 3, 15, 150, 150, 750]}
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(si.get('items')), len(expected_values) - 1)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(si.total, 25)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(si.base_total, 1250)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(si.net_total, 25)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(si.base_net_total, 1250)
```

### Step 16: Assign expected_values = value

```python
expected_values = {'keys': ['base_tax_amount', 'base_total', 'tax_amount', 'total'], '_Test Account Shipping Charges - _TC': [100, 1350, 2, 27], '_Test Account Customs Duty - _TC': [125, 1475, 2.5, 29.5], '_Test Account Excise Duty - _TC': [140, 1615, 2.8, 32.3], '_Test Account Education Cess - _TC': [3, 1618, 0.06, 32.36], '_Test Account S&H Education Cess - _TC': [1.5, 1619.5, 0.03, 32.39], '_Test Account CST - _TC': [32.5, 1652, 0.65, 33.04], '_Test Account VAT - _TC': [156.0, 1808.0, 3.12, 36.16], '_Test Account Discount - _TC': [-181.0, 1627.0, -3.62, 32.54]}
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(si.base_grand_total, 1627.0)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(si.grand_total, 32.54)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(d.get(k), expected_values[d.item_code][i])
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(d.get(k), expected_values[d.account_head][i])
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
si.currency = 'USD'
si.conversion_rate = 50
si.get('items')[0].rate = 1
si.get('items')[0].price_list_rate = 1
si.get('items')[1].rate = 3
si.get('items')[1].price_list_rate = 3
si.get('taxes')[0].tax_amount = 2
si.insert()
expected_values = {'keys': ['price_list_rate', 'discount_percentage', 'rate', 'amount', 'base_price_list_rate', 'base_rate', 'base_amount'], '_Test Item Home Desktop 100': [1, 0, 1, 10, 50, 50, 500], '_Test Item Home Desktop 200': [3, 0, 3, 15, 150, 150, 750]}
self.assertEqual(len(si.get('items')), len(expected_values) - 1)
for d in si.get('items'):
    for i, k in enumerate(expected_values['keys']):
        self.assertEqual(d.get(k), expected_values[d.item_code][i])
self.assertEqual(si.total, 25)
self.assertEqual(si.base_total, 1250)
self.assertEqual(si.net_total, 25)
self.assertEqual(si.base_net_total, 1250)
expected_values = {'keys': ['base_tax_amount', 'base_total', 'tax_amount', 'total'], '_Test Account Shipping Charges - _TC': [100, 1350, 2, 27], '_Test Account Customs Duty - _TC': [125, 1475, 2.5, 29.5], '_Test Account Excise Duty - _TC': [140, 1615, 2.8, 32.3], '_Test Account Education Cess - _TC': [3, 1618, 0.06, 32.36], '_Test Account S&H Education Cess - _TC': [1.5, 1619.5, 0.03, 32.39], '_Test Account CST - _TC': [32.5, 1652, 0.65, 33.04], '_Test Account VAT - _TC': [156.0, 1808.0, 3.12, 36.16], '_Test Account Discount - _TC': [-181.0, 1627.0, -3.62, 32.54]}
for d in si.get('taxes'):
    for i, k in enumerate(expected_values['keys']):
        self.assertEqual(d.get(k), expected_values[d.account_head][i])
self.assertEqual(si.base_grand_total, 1627.0)
self.assertEqual(si.grand_total, 32.54)
```

## Next Steps


---

*Source: test_sales_invoice.py:276 | Complexity: Advanced | Last updated: 2026-02-03*