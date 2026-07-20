# How To: Resolve Independent Formula Row Groups

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test resolve independent formula row groups

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.utils`
- `erpnext.accounts.doctype.financial_report_template.financial_report_engine`
- `erpnext.accounts.doctype.financial_report_template.test_financial_report_template`
- `erpnext.accounts.utils`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`


## Step-by-Step Guide

### Step 1: Assign test_rows = value

```python
test_rows = [{'reference_code': 'A001', 'display_name': 'Chain 1 Base', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Asset"]'}, {'reference_code': 'B001', 'display_name': 'Chain 1 Level 2', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 1.1'}, {'reference_code': 'C001', 'display_name': 'Chain 1 Final', 'data_source': 'Calculated Amount', 'calculation_formula': 'B001 + 100'}, {'reference_code': 'X001', 'display_name': 'Chain 2 Base', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Liability"]'}, {'reference_code': 'Y001', 'display_name': 'Chain 2 Level 2', 'data_source': 'Calculated Amount', 'calculation_formula': 'X001 * 0.9'}, {'reference_code': 'Z001', 'display_name': 'Chain 2 Final', 'data_source': 'Calculated Amount', 'calculation_formula': 'Y001 - 50'}]
```

### Step 2: Assign test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(...)

```python
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
```

### Step 3: Assign resolver = DependencyResolver(...)

```python
resolver = DependencyResolver(test_template)
```

### Step 4: Assign order = resolver.get_processing_order(...)

```python
order = resolver.get_processing_order()
```

### Step 5: Assign positions = value

```python
positions = {row.reference_code: i for i, row in enumerate(order)}
```

### Step 6: Call self.assertLess()

```python
self.assertLess(positions['A001'], positions['B001'])
```

### Step 7: Call self.assertLess()

```python
self.assertLess(positions['B001'], positions['C001'])
```

### Step 8: Call self.assertLess()

```python
self.assertLess(positions['X001'], positions['Y001'])
```

### Step 9: Call self.assertLess()

```python
self.assertLess(positions['Y001'], positions['Z001'])
```

### Step 10: Assign chain1_codes = value

```python
chain1_codes = {'A001', 'B001', 'C001'}
```

### Step 11: Assign chain2_codes = value

```python
chain2_codes = {'X001', 'Y001', 'Z001'}
```

### Step 12: Assign deps = set(...)

```python
deps = set(resolver.dependencies[code])
```

### Step 13: Call self.assertFalse()

```python
self.assertFalse(deps.intersection(chain2_codes), f'{code} should not depend on chain 2')
```

### Step 14: Assign deps = set(...)

```python
deps = set(resolver.dependencies[code])
```

### Step 15: Call self.assertFalse()

```python
self.assertFalse(deps.intersection(chain1_codes), f'{code} should not depend on chain 1')
```


## Complete Example

```python
# Workflow
test_rows = [{'reference_code': 'A001', 'display_name': 'Chain 1 Base', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Asset"]'}, {'reference_code': 'B001', 'display_name': 'Chain 1 Level 2', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 1.1'}, {'reference_code': 'C001', 'display_name': 'Chain 1 Final', 'data_source': 'Calculated Amount', 'calculation_formula': 'B001 + 100'}, {'reference_code': 'X001', 'display_name': 'Chain 2 Base', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Liability"]'}, {'reference_code': 'Y001', 'display_name': 'Chain 2 Level 2', 'data_source': 'Calculated Amount', 'calculation_formula': 'X001 * 0.9'}, {'reference_code': 'Z001', 'display_name': 'Chain 2 Final', 'data_source': 'Calculated Amount', 'calculation_formula': 'Y001 - 50'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order)}
self.assertLess(positions['A001'], positions['B001'])
self.assertLess(positions['B001'], positions['C001'])
self.assertLess(positions['X001'], positions['Y001'])
self.assertLess(positions['Y001'], positions['Z001'])
chain1_codes = {'A001', 'B001', 'C001'}
chain2_codes = {'X001', 'Y001', 'Z001'}
for code in chain1_codes:
    if code in resolver.dependencies:
        deps = set(resolver.dependencies[code])
        self.assertFalse(deps.intersection(chain2_codes), f'{code} should not depend on chain 2')
for code in chain2_codes:
    if code in resolver.dependencies:
        deps = set(resolver.dependencies[code])
        self.assertFalse(deps.intersection(chain1_codes), f'{code} should not depend on chain 1')
```

## Next Steps


---

*Source: test_financial_report_engine.py:206 | Complexity: Advanced | Last updated: 2026-02-03*