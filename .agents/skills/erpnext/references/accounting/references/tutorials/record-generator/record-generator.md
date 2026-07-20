# How To: Record Generator

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test record generator

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign test_records = value

```python
test_records = [{'doctype': 'Fiscal Year', 'year': '_Test Short Fiscal Year 2011', 'is_short_year': 1, 'year_start_date': '2011-04-01', 'year_end_date': '2011-12-31'}]
```

### Step 2: Assign start = 2012

```python
start = 2012
```

### Step 3: Assign this_year = value

```python
this_year = now_datetime().year
```

### Step 4: Assign end = value

```python
end = now_datetime().year + 25
```

### Step 5: Call test_records.append()

```python
test_records.append({'doctype': 'Fiscal Year', 'year': f'_Test Fiscal Year {year}', 'year_start_date': f'{year}-01-01', 'year_end_date': f'{year}-12-31'})
```

### Step 6: Call test_records.append()

```python
test_records.append({'doctype': 'Fiscal Year', 'year': f'_Test Fiscal Year {year}', 'year_start_date': f'{year}-01-01', 'year_end_date': f'{year}-12-31'})
```


## Complete Example

```python
# Workflow
test_records = [{'doctype': 'Fiscal Year', 'year': '_Test Short Fiscal Year 2011', 'is_short_year': 1, 'year_start_date': '2011-04-01', 'year_end_date': '2011-12-31'}]
start = 2012
this_year = now_datetime().year
end = now_datetime().year + 25
for year in range(start, this_year):
    test_records.append({'doctype': 'Fiscal Year', 'year': f'_Test Fiscal Year {year}', 'year_start_date': f'{year}-01-01', 'year_end_date': f'{year}-12-31'})
for year in range(this_year + 1, end):
    test_records.append({'doctype': 'Fiscal Year', 'year': f'_Test Fiscal Year {year}', 'year_start_date': f'{year}-01-01', 'year_end_date': f'{year}-12-31'})
return test_records
```

## Next Steps


---

*Source: test_fiscal_year.py:49 | Complexity: Intermediate | Last updated: 2026-02-03*