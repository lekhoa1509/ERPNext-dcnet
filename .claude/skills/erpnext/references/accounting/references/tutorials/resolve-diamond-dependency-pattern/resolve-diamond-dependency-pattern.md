# How To: Resolve Diamond Dependency Pattern

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test Diamond Dependency Pattern - A → B, A → C, and both B,C → D

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

### Step 1: 'Test Diamond Dependency Pattern - A → B, A → C, and both B,C → D'

```python
'Test Diamond Dependency Pattern - A → B, A → C, and both B,C → D'
```

### Step 2: Assign test_rows = value

```python
test_rows = [{'reference_code': 'A001', 'display_name': 'Base Data', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'B001', 'display_name': 'Branch B', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 0.6'}, {'reference_code': 'C001', 'display_name': 'Branch C', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 0.4'}, {'reference_code': 'D001', 'display_name': 'Final Result', 'data_source': 'Calculated Amount', 'calculation_formula': 'B001 + C001'}]
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
positions = {row.reference_code: i for i, row in enumerate(order)}
```

### Step 7: Call self.assertLess()

```python
self.assertLess(positions['A001'], positions['B001'])
```

### Step 8: Call self.assertLess()

```python
self.assertLess(positions['A001'], positions['C001'])
```

### Step 9: Call self.assertLess()

```python
self.assertLess(positions['A001'], positions['D001'])
```

### Step 10: Call self.assertLess()

```python
self.assertLess(positions['B001'], positions['D001'])
```

### Step 11: Call self.assertLess()

```python
self.assertLess(positions['C001'], positions['D001'])
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(set(resolver.dependencies['D001']), {'B001', 'C001'})
```


## Complete Example

```python
# Workflow
'Test Diamond Dependency Pattern - A → B, A → C, and both B,C → D'
test_rows = [{'reference_code': 'A001', 'display_name': 'Base Data', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'B001', 'display_name': 'Branch B', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 0.6'}, {'reference_code': 'C001', 'display_name': 'Branch C', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 0.4'}, {'reference_code': 'D001', 'display_name': 'Final Result', 'data_source': 'Calculated Amount', 'calculation_formula': 'B001 + C001'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order)}
self.assertLess(positions['A001'], positions['B001'])
self.assertLess(positions['A001'], positions['C001'])
self.assertLess(positions['A001'], positions['D001'])
self.assertLess(positions['B001'], positions['D001'])
self.assertLess(positions['C001'], positions['D001'])
self.assertEqual(set(resolver.dependencies['D001']), {'B001', 'C001'})
```

## Next Steps


---

*Source: test_financial_report_engine.py:159 | Complexity: Advanced | Last updated: 2026-02-03*