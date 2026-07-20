# How To: Extract From Complex Formulas

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test extract from complex formulas

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
test_rows = [{'reference_code': 'INCOME', 'display_name': 'Total Income', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Income"]'}, {'reference_code': 'EXPENSE', 'display_name': 'Total Expense', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Expense"]'}, {'reference_code': 'TAX_RATE', 'display_name': 'Tax Rate', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_name", "like", "Tax"]'}, {'reference_code': 'NET_RESULT', 'display_name': 'Net Result', 'data_source': 'Calculated Amount', 'calculation_formula': '(INCOME - EXPENSE) * (1 - TAX_RATE / 100)'}]
```

### Step 2: Assign test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(...)

```python
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
```

### Step 3: Assign resolver = DependencyResolver(...)

```python
resolver = DependencyResolver(test_template)
```

### Step 4: Assign net_deps = resolver.dependencies.get(...)

```python
net_deps = resolver.dependencies.get('NET_RESULT', [])
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(set(net_deps), {'INCOME', 'EXPENSE', 'TAX_RATE'})
```


## Complete Example

```python
# Workflow
test_rows = [{'reference_code': 'INCOME', 'display_name': 'Total Income', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Income"]'}, {'reference_code': 'EXPENSE', 'display_name': 'Total Expense', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Expense"]'}, {'reference_code': 'TAX_RATE', 'display_name': 'Tax Rate', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_name", "like", "Tax"]'}, {'reference_code': 'NET_RESULT', 'display_name': 'Net Result', 'data_source': 'Calculated Amount', 'calculation_formula': '(INCOME - EXPENSE) * (1 - TAX_RATE / 100)'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
net_deps = resolver.dependencies.get('NET_RESULT', [])
self.assertEqual(set(net_deps), {'INCOME', 'EXPENSE', 'TAX_RATE'})
```

## Next Steps


---

*Source: test_financial_report_engine.py:405 | Complexity: Intermediate | Last updated: 2026-02-03*