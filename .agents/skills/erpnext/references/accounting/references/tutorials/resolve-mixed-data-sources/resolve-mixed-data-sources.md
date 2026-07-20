# How To: Resolve Mixed Data Sources

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test resolve mixed data sources

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
test_rows = [{'reference_code': 'CALC001', 'display_name': 'Calculated', 'data_source': 'Calculated Amount', 'calculation_formula': 'ACC001 + 100'}, {'reference_code': None, 'display_name': 'Spacing', 'data_source': 'Blank Line'}, {'reference_code': 'ACC001', 'display_name': 'Account', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': None, 'display_name': 'Custom', 'data_source': 'Custom API'}]
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
positions = {}
```

### Step 6: Call self.assertLess()

```python
self.assertLess(positions['ACC001'], positions['CALC001'])
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(order), 4)
```

### Step 8: Assign unknown = i

```python
positions[row.reference_code] = i
```

### Step 9: Assign unknown = i

```python
positions[f'{row.data_source}_{i}'] = i
```


## Complete Example

```python
# Workflow
test_rows = [{'reference_code': 'CALC001', 'display_name': 'Calculated', 'data_source': 'Calculated Amount', 'calculation_formula': 'ACC001 + 100'}, {'reference_code': None, 'display_name': 'Spacing', 'data_source': 'Blank Line'}, {'reference_code': 'ACC001', 'display_name': 'Account', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': None, 'display_name': 'Custom', 'data_source': 'Custom API'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {}
for i, row in enumerate(order):
    if row.reference_code:
        positions[row.reference_code] = i
    else:
        positions[f'{row.data_source}_{i}'] = i
self.assertLess(positions['ACC001'], positions['CALC001'])
self.assertEqual(len(order), 4)
```

## Next Steps


---

*Source: test_financial_report_engine.py:278 | Complexity: Advanced | Last updated: 2026-02-03*