# How To: Make Supplier Quotation With Taxes

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test automatic tax addition when supplier quotation is created from RFQ taxes_and_charges are set

## Prerequisites

**Required Modules:**
- `urllib.parse`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.buying.doctype.request_for_quotation.request_for_quotation`
- `erpnext.controllers.accounts_controller`
- `erpnext.crm.doctype.opportunity.opportunity`
- `erpnext.crm.doctype.opportunity.test_opportunity`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.templates.pages.rfq`


## Step-by-Step Guide

### Step 1: 'Test automatic tax addition when supplier quotation is created from RFQ taxes_and_charges are set'

```python
'Test automatic tax addition when supplier quotation is created from RFQ taxes_and_charges are set'
```

### Step 2: Assign tax_template = frappe.new_doc(...)

```python
tax_template = frappe.new_doc('Purchase Taxes and Charges Template')
```

### Step 3: Assign tax_template.doctype = 'Purchase Taxes and Charges Template'

```python
tax_template.doctype = 'Purchase Taxes and Charges Template'
```

### Step 4: Assign tax_template.title = '_Test Purchase Taxes Template for RFQ'

```python
tax_template.title = '_Test Purchase Taxes Template for RFQ'
```

### Step 5: Assign tax_template.company = '_Test Company'

```python
tax_template.company = '_Test Company'
```

### Step 6: Call tax_template.append()

```python
tax_template.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'description': 'VAT', 'rate': 10})
```

### Step 7: Call tax_template.save()

```python
tax_template.save()
```

### Step 8: Assign rfq = make_request_for_quotation(...)

```python
rfq = make_request_for_quotation()
```

### Step 9: Assign supplier = value

```python
supplier = rfq.get('suppliers')[0].supplier
```

### Step 10: Assign tax_rule = frappe.new_doc(...)

```python
tax_rule = frappe.new_doc('Tax Rule')
```

### Step 11: Assign tax_rule.company = '_Test Company'

```python
tax_rule.company = '_Test Company'
```

### Step 12: Assign tax_rule.tax_type = 'Purchase'

```python
tax_rule.tax_type = 'Purchase'
```

### Step 13: Assign tax_rule.supplier = supplier

```python
tax_rule.supplier = supplier
```

### Step 14: Assign tax_rule.purchase_tax_template = value

```python
tax_rule.purchase_tax_template = tax_template.name
```

### Step 15: Call tax_rule.save()

```python
tax_rule.save()
```

### Step 16: Assign sq = make_supplier_quotation_from_rfq(...)

```python
sq = make_supplier_quotation_from_rfq(rfq.name, for_supplier=supplier)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(sq.taxes_and_charges, tax_template.name)
```

### Step 18: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(len(sq.get('taxes')), 1)
```

### Step 19: Call tax_rule.delete()

```python
tax_rule.delete()
```

### Step 20: Call tax_template.delete()

```python
tax_template.delete()
```


## Complete Example

```python
# Workflow
'Test automatic tax addition when supplier quotation is created from RFQ taxes_and_charges are set'
tax_template = frappe.new_doc('Purchase Taxes and Charges Template')
tax_template.doctype = 'Purchase Taxes and Charges Template'
tax_template.title = '_Test Purchase Taxes Template for RFQ'
tax_template.company = '_Test Company'
tax_template.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'description': 'VAT', 'rate': 10})
tax_template.save()
rfq = make_request_for_quotation()
supplier = rfq.get('suppliers')[0].supplier
tax_rule = frappe.new_doc('Tax Rule')
tax_rule.company = '_Test Company'
tax_rule.tax_type = 'Purchase'
tax_rule.supplier = supplier
tax_rule.purchase_tax_template = tax_template.name
tax_rule.save()
sq = make_supplier_quotation_from_rfq(rfq.name, for_supplier=supplier)
self.assertEqual(sq.taxes_and_charges, tax_template.name)
self.assertGreaterEqual(len(sq.get('taxes')), 1)
tax_rule.delete()
tax_template.delete()
```

## Next Steps


---

*Source: test_request_for_quotation.py:79 | Complexity: Advanced | Last updated: 2026-02-04*