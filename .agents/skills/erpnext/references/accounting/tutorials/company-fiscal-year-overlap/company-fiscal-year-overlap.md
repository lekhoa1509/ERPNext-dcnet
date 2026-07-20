# How To: Company Fiscal Year Overlap

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test company fiscal year overlap

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign global_fy = frappe.new_doc(...)

```python
global_fy = frappe.new_doc('Fiscal Year')
```

### Step 2: Assign global_fy.year = '_Test Global FY 2001'

```python
global_fy.year = '_Test Global FY 2001'
```

### Step 3: Assign global_fy.year_start_date = '2001-04-01'

```python
global_fy.year_start_date = '2001-04-01'
```

### Step 4: Assign global_fy.year_end_date = '2002-03-31'

```python
global_fy.year_end_date = '2002-03-31'
```

### Step 5: Call global_fy.insert()

```python
global_fy.insert()
```

### Step 6: Assign company_fy = frappe.new_doc(...)

```python
company_fy = frappe.new_doc('Fiscal Year')
```

### Step 7: Assign company_fy.year = '_Test Company FY 2001'

```python
company_fy.year = '_Test Company FY 2001'
```

### Step 8: Assign company_fy.year_start_date = '2001-01-01'

```python
company_fy.year_start_date = '2001-01-01'
```

### Step 9: Assign company_fy.year_end_date = '2001-12-31'

```python
company_fy.year_end_date = '2001-12-31'
```

### Step 10: Call company_fy.append()

```python
company_fy.append('companies', {'company': '_Test Company'})
```

### Step 11: Call company_fy.insert()

```python
company_fy.insert()
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))
```

### Step 14: Call frappe.delete_doc()

```python
frappe.delete_doc('Fiscal Year', name)
```


## Complete Example

```python
# Workflow
for name in ['_Test Global FY 2001', '_Test Company FY 2001']:
    if frappe.db.exists('Fiscal Year', name):
        frappe.delete_doc('Fiscal Year', name)
global_fy = frappe.new_doc('Fiscal Year')
global_fy.year = '_Test Global FY 2001'
global_fy.year_start_date = '2001-04-01'
global_fy.year_end_date = '2002-03-31'
global_fy.insert()
company_fy = frappe.new_doc('Fiscal Year')
company_fy.year = '_Test Company FY 2001'
company_fy.year_start_date = '2001-01-01'
company_fy.year_end_date = '2001-12-31'
company_fy.append('companies', {'company': '_Test Company'})
company_fy.insert()
self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))
self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))
```

## Next Steps


---

*Source: test_fiscal_year.py:27 | Complexity: Advanced | Last updated: 2026-02-03*