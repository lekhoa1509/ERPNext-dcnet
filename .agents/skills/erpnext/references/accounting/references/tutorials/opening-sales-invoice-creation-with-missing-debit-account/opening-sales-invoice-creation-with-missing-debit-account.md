# How To: Opening Sales Invoice Creation With Missing Debit Account

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test opening sales invoice creation with missing debit account

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.accounting_dimension.test_accounting_dimension`
- `erpnext.accounts.doctype.opening_invoice_creation_tool.opening_invoice_creation_tool`


## Step-by-Step Guide

### Step 1: Assign company = '_Test Opening Invoice Company'

```python
company = '_Test Opening Invoice Company'
```

### Step 2: Assign unknown = value

```python
party_1, party_2 = (make_customer('Customer A'), make_customer('Customer B'))
```

### Step 3: Assign old_default_receivable_account = frappe.db.get_value(...)

```python
old_default_receivable_account = frappe.db.get_value('Company', company, 'default_receivable_account')
```

### Step 4: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', company, 'default_receivable_account', '')
```

### Step 5: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', company, 'cost_center', 'Main - _TOIC')
```

### Step 6: Call self.make_invoices()

```python
self.make_invoices(company='_Test Opening Invoice Company', party_1=party_1, party_2=party_2)
```

### Step 7: Assign error_log = frappe.db.exists(...)

```python
error_log = frappe.db.exists('Error Log', {'error': ['like', '%erpnext.controllers.accounts_controller.AccountMissingError%']})
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(error_log)
```

### Step 9: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', company, 'default_receivable_account', old_default_receivable_account)
```

### Step 10: Assign cc = frappe.get_doc(...)

```python
cc = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Opening Invoice Company', 'is_group': 1, 'company': '_Test Opening Invoice Company'})
```

### Step 11: Call cc.insert()

```python
cc.insert(ignore_mandatory=True)
```

### Step 12: Assign cc2 = frappe.get_doc(...)

```python
cc2 = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': 'Main', 'is_group': 0, 'company': '_Test Opening Invoice Company', 'parent_cost_center': cc.name})
```

### Step 13: Call cc2.insert()

```python
cc2.insert()
```


## Complete Example

```python
# Workflow
company = '_Test Opening Invoice Company'
party_1, party_2 = (make_customer('Customer A'), make_customer('Customer B'))
old_default_receivable_account = frappe.db.get_value('Company', company, 'default_receivable_account')
frappe.db.set_value('Company', company, 'default_receivable_account', '')
if not frappe.db.exists('Cost Center', '_Test Opening Invoice Company - _TOIC'):
    cc = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Opening Invoice Company', 'is_group': 1, 'company': '_Test Opening Invoice Company'})
    cc.insert(ignore_mandatory=True)
    cc2 = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': 'Main', 'is_group': 0, 'company': '_Test Opening Invoice Company', 'parent_cost_center': cc.name})
    cc2.insert()
frappe.db.set_value('Company', company, 'cost_center', 'Main - _TOIC')
self.make_invoices(company='_Test Opening Invoice Company', party_1=party_1, party_2=party_2)
error_log = frappe.db.exists('Error Log', {'error': ['like', '%erpnext.controllers.accounts_controller.AccountMissingError%']})
self.assertTrue(error_log)
frappe.db.set_value('Company', company, 'default_receivable_account', old_default_receivable_account)
```

## Next Steps


---

*Source: test_opening_invoice_creation_tool.py:82 | Complexity: Advanced | Last updated: 2026-02-03*