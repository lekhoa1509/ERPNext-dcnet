# How To: Resolve Api To Formula Dependencies

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test resolve api to formula dependencies

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

**Required Fixtures:**
- `api_client` fixture


## Step-by-Step Guide

### Step 1: Assign test_rows = value

```python
test_rows = [{'reference_code': 'API001', 'display_name': 'Custom API Result', 'data_source': 'Custom API'}, {'reference_code': 'ACC001', 'display_name': 'Account Data', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'CALC001', 'display_name': 'Calculated Result', 'data_source': 'Calculated Amount', 'calculation_formula': 'API001 + ACC001'}]
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
self.assertLess(positions['API001'], positions['CALC001'])
```

### Step 7: Call self.assertLess()

```python
self.assertLess(positions['ACC001'], positions['CALC001'])
```

### Step 8: Call self.assertLess()

```python
self.assertLess(positions['API001'], positions['ACC001'])
```


## Complete Example

```python
# Workflow
test_rows = [{'reference_code': 'API001', 'display_name': 'Custom API Result', 'data_source': 'Custom API'}, {'reference_code': 'ACC001', 'display_name': 'Account Data', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'CALC001', 'display_name': 'Calculated Result', 'data_source': 'Calculated Amount', 'calculation_formula': 'API001 + ACC001'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order)}
self.assertLess(positions['API001'], positions['CALC001'])
self.assertLess(positions['ACC001'], positions['CALC001'])
self.assertLess(positions['API001'], positions['ACC001'])
```

## Next Steps


---

*Source: test_financial_report_engine.py:323 | Complexity: Advanced | Last updated: 2026-02-03*