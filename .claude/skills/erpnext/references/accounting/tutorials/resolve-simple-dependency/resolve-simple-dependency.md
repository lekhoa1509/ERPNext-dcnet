# How To: Resolve Simple Dependency

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test resolve simple dependency

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
test_rows = [{'reference_code': 'A001', 'display_name': 'Base Account', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'B001', 'display_name': 'Calculated Row', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 2'}]
```

### Step 2: Assign test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(...)

```python
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
```

### Step 3: Assign resolver = DependencyResolver(...)

```python
resolver = DependencyResolver(test_template)
```

### Step 4: Call self.assertIn()

```python
self.assertIn('B001', resolver.dependencies)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(resolver.dependencies['B001'], ['A001'])
```

### Step 6: Assign order = resolver.get_processing_order(...)

```python
order = resolver.get_processing_order()
```

### Step 7: Assign a001_index = next(...)

```python
a001_index = next((i for i, row in enumerate(order) if row.reference_code == 'A001'))
```

### Step 8: Assign b001_index = next(...)

```python
b001_index = next((i for i, row in enumerate(order) if row.reference_code == 'B001'))
```

### Step 9: Call self.assertLess()

```python
self.assertLess(a001_index, b001_index, 'A001 should be processed before B001')
```


## Complete Example

```python
# Workflow
test_rows = [{'reference_code': 'A001', 'display_name': 'Base Account', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'B001', 'display_name': 'Calculated Row', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 2'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
self.assertIn('B001', resolver.dependencies)
self.assertEqual(resolver.dependencies['B001'], ['A001'])
order = resolver.get_processing_order()
a001_index = next((i for i, row in enumerate(order) if row.reference_code == 'A001'))
b001_index = next((i for i, row in enumerate(order) if row.reference_code == 'B001'))
self.assertLess(a001_index, b001_index, 'A001 should be processed before B001')
```

## Next Steps


---

*Source: test_financial_report_engine.py:38 | Complexity: Advanced | Last updated: 2026-02-03*