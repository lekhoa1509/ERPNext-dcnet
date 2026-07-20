# How To: Resolve Multiple Dependencies

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test resolve multiple dependencies

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
test_rows = [{'reference_code': 'INC001', 'display_name': 'Income', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Income"]'}, {'reference_code': 'EXP001', 'display_name': 'Expenses', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Expense"]'}, {'reference_code': 'GROSS001', 'display_name': 'Gross Profit', 'data_source': 'Calculated Amount', 'calculation_formula': 'INC001 - EXP001'}, {'reference_code': 'MARGIN001', 'display_name': 'Profit Margin', 'data_source': 'Calculated Amount', 'calculation_formula': 'GROSS001 / INC001 * 100'}]
```

### Step 2: Assign test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(...)

```python
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
```

### Step 3: Assign resolver = DependencyResolver(...)

```python
resolver = DependencyResolver(test_template)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(set(resolver.dependencies['GROSS001']), {'INC001', 'EXP001'})
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(set(resolver.dependencies['MARGIN001']), {'GROSS001', 'INC001'})
```

### Step 6: Assign order = resolver.get_processing_order(...)

```python
order = resolver.get_processing_order()
```

### Step 7: Assign positions = value

```python
positions = {row.reference_code: i for i, row in enumerate(order) if row.reference_code}
```

### Step 8: Call self.assertLess()

```python
self.assertLess(positions['INC001'], positions['GROSS001'])
```

### Step 9: Call self.assertLess()

```python
self.assertLess(positions['EXP001'], positions['GROSS001'])
```

### Step 10: Call self.assertLess()

```python
self.assertLess(positions['GROSS001'], positions['MARGIN001'])
```


## Complete Example

```python
# Workflow
test_rows = [{'reference_code': 'INC001', 'display_name': 'Income', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Income"]'}, {'reference_code': 'EXP001', 'display_name': 'Expenses', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Expense"]'}, {'reference_code': 'GROSS001', 'display_name': 'Gross Profit', 'data_source': 'Calculated Amount', 'calculation_formula': 'INC001 - EXP001'}, {'reference_code': 'MARGIN001', 'display_name': 'Profit Margin', 'data_source': 'Calculated Amount', 'calculation_formula': 'GROSS001 / INC001 * 100'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
self.assertEqual(set(resolver.dependencies['GROSS001']), {'INC001', 'EXP001'})
self.assertEqual(set(resolver.dependencies['MARGIN001']), {'GROSS001', 'INC001'})
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order) if row.reference_code}
self.assertLess(positions['INC001'], positions['GROSS001'])
self.assertLess(positions['EXP001'], positions['GROSS001'])
self.assertLess(positions['GROSS001'], positions['MARGIN001'])
```

## Next Steps


---

*Source: test_financial_report_engine.py:71 | Complexity: Advanced | Last updated: 2026-02-03*