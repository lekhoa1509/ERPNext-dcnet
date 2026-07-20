# How To: Resolve Chain Dependencies

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test dependency resolution with chain of dependencies (A -> B -> C -> D)

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

### Step 1: 'Test dependency resolution with chain of dependencies (A -> B -> C -> D)'

```python
'Test dependency resolution with chain of dependencies (A -> B -> C -> D)'
```

### Step 2: Assign test_rows = value

```python
test_rows = [{'reference_code': 'A001', 'display_name': 'Base', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'B001', 'display_name': 'Level 1', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 + 100'}, {'reference_code': 'C001', 'display_name': 'Level 2', 'data_source': 'Calculated Amount', 'calculation_formula': 'B001 * 1.2'}, {'reference_code': 'D001', 'display_name': 'Level 3', 'data_source': 'Calculated Amount', 'calculation_formula': 'C001 - 50'}]
```

### Step 3: Assign test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(...)

```python
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
```

### Step 4: Assign resolver = DependencyResolver(...)

```python
resolver = DependencyResolver(test_template)
```

### Step 5: Assign order = resolver.get_processing_order(...)

```python
order = resolver.get_processing_order()
```

### Step 6: Assign positions = value

```python
positions = {row.reference_code: i for i, row in enumerate(order) if row.reference_code}
```

### Step 7: Call self.assertLess()

```python
self.assertLess(positions['A001'], positions['B001'])
```

### Step 8: Call self.assertLess()

```python
self.assertLess(positions['B001'], positions['C001'])
```

### Step 9: Call self.assertLess()

```python
self.assertLess(positions['C001'], positions['D001'])
```


## Complete Example

```python
# Workflow
'Test dependency resolution with chain of dependencies (A -> B -> C -> D)'
test_rows = [{'reference_code': 'A001', 'display_name': 'Base', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'B001', 'display_name': 'Level 1', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 + 100'}, {'reference_code': 'C001', 'display_name': 'Level 2', 'data_source': 'Calculated Amount', 'calculation_formula': 'B001 * 1.2'}, {'reference_code': 'D001', 'display_name': 'Level 3', 'data_source': 'Calculated Amount', 'calculation_formula': 'C001 - 50'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order) if row.reference_code}
self.assertLess(positions['A001'], positions['B001'])
self.assertLess(positions['B001'], positions['C001'])
self.assertLess(positions['C001'], positions['D001'])
```

## Next Steps


---

*Source: test_financial_report_engine.py:119 | Complexity: Advanced | Last updated: 2026-02-03*