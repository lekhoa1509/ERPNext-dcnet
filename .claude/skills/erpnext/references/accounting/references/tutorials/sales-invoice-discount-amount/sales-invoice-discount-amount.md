# How To: Sales Invoice Discount Amount

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sales invoice discount amount

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
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][3])
```

### Step 2: Assign si.discount_amount = 104.94

```python
si.discount_amount = 104.94
```

### Step 3: Call si.append()

```python
si.append('taxes', {'charge_type': 'On Previous Row Amount', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 10, 'row_id': 8})
```

### Step 4: Call si.insert()

```python
si.insert()
```

### Step 5: Assign expected_values = value

```python
expected_values = [{'item_code': '_Test Item Home Desktop 100', 'price_list_rate': 62.5, 'discount_percentage': 0, 'rate': 62.5, 'amount': 625, 'base_price_list_rate': 62.5, 'base_rate': 62.5, 'base_amount': 625, 'net_rate': 46.54, 'net_amount': 465.37, 'base_net_rate': 46.54, 'base_net_amount': 465.37}, {'item_code': '_Test Item Home Desktop 200', 'price_list_rate': 190.66, 'discount_percentage': 0, 'rate': 190.66, 'amount': 953.3, 'base_price_list_rate': 190.66, 'base_rate': 190.66, 'base_amount': 953.3, 'net_rate': 139.62, 'net_amount': 698.08, 'base_net_rate': 139.62, 'base_net_amount': 698.08}]
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(si.get('items')), len(expected_values))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(si.base_net_total, 1163.45)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(si.total, 1578.3)
```

### Step 9: Assign expected_values = value

```python
expected_values = {'keys': ['tax_amount', 'tax_amount_after_discount_amount', 'total'], '_Test Account Excise Duty - _TC': [140, 130.31, 1293.76], '_Test Account Education Cess - _TC': [2.8, 2.61, 1296.37], '_Test Account S&H Education Cess - _TC': [1.4, 1.3, 1297.67], '_Test Account CST - _TC': [27.88, 25.95, 1323.62], '_Test Account VAT - _TC': [156.25, 145.43, 1469.05], '_Test Account Customs Duty - _TC': [125, 116.34, 1585.39], '_Test Account Shipping Charges - _TC': [100, 100, 1685.39], '_Test Account Discount - _TC': [-180.33, -168.54, 1516.85], '_Test Account Service Tax - _TC': [-18.03, -16.85, 1500.0]}
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(si.base_grand_total, 1500)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(si.grand_total, 1500)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(si.rounding_adjustment, 0.0)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(d.get(k), v)
```

### Step 14: Call self.assertEqual()

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
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][3])
si.discount_amount = 104.94
si.append('taxes', {'charge_type': 'On Previous Row Amount', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 10, 'row_id': 8})
si.insert()
expected_values = [{'item_code': '_Test Item Home Desktop 100', 'price_list_rate': 62.5, 'discount_percentage': 0, 'rate': 62.5, 'amount': 625, 'base_price_list_rate': 62.5, 'base_rate': 62.5, 'base_amount': 625, 'net_rate': 46.54, 'net_amount': 465.37, 'base_net_rate': 46.54, 'base_net_amount': 465.37}, {'item_code': '_Test Item Home Desktop 200', 'price_list_rate': 190.66, 'discount_percentage': 0, 'rate': 190.66, 'amount': 953.3, 'base_price_list_rate': 190.66, 'base_rate': 190.66, 'base_amount': 953.3, 'net_rate': 139.62, 'net_amount': 698.08, 'base_net_rate': 139.62, 'base_net_amount': 698.08}]
self.assertEqual(len(si.get('items')), len(expected_values))
for i, d in enumerate(si.get('items')):
    for k, v in expected_values[i].items():
        self.assertEqual(d.get(k), v)
self.assertEqual(si.base_net_total, 1163.45)
self.assertEqual(si.total, 1578.3)
expected_values = {'keys': ['tax_amount', 'tax_amount_after_discount_amount', 'total'], '_Test Account Excise Duty - _TC': [140, 130.31, 1293.76], '_Test Account Education Cess - _TC': [2.8, 2.61, 1296.37], '_Test Account S&H Education Cess - _TC': [1.4, 1.3, 1297.67], '_Test Account CST - _TC': [27.88, 25.95, 1323.62], '_Test Account VAT - _TC': [156.25, 145.43, 1469.05], '_Test Account Customs Duty - _TC': [125, 116.34, 1585.39], '_Test Account Shipping Charges - _TC': [100, 100, 1685.39], '_Test Account Discount - _TC': [-180.33, -168.54, 1516.85], '_Test Account Service Tax - _TC': [-18.03, -16.85, 1500.0]}
for d in si.get('taxes'):
    for i, k in enumerate(expected_values['keys']):
        self.assertEqual(d.get(k), expected_values[d.account_head][i])
self.assertEqual(si.base_grand_total, 1500)
self.assertEqual(si.grand_total, 1500)
self.assertEqual(si.rounding_adjustment, 0.0)
```

## Next Steps


---

*Source: test_sales_invoice.py:395 | Complexity: Advanced | Last updated: 2026-02-03*