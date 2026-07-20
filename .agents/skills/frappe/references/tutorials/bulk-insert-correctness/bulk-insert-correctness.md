# How To: Bulk Insert Correctness

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bulk insert correctness

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.geo.doctype.country.country`
- `frappe.geo.doctype.currency.currency`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Call clear_tables()

```python
clear_tables()
```

### Step 2: Call import_country_and_currency()

```python
import_country_and_currency()
```

### Step 3: Assign countries_before = get_table_snapshot(...)

```python
countries_before = get_table_snapshot('Country')
```

### Step 4: Assign currencies_before = get_table_snapshot(...)

```python
currencies_before = get_table_snapshot('Currency')
```

### Step 5: Call clear_tables()

```python
clear_tables()
```

### Step 6: Assign unknown = get_countries_and_currencies(...)

```python
countries, currencies = get_countries_and_currencies()
```

### Step 7: Call enable_default_currencies()

```python
enable_default_currencies()
```

### Step 8: Assign countries_after = get_table_snapshot(...)

```python
countries_after = get_table_snapshot('Country')
```

### Step 9: Assign currencies_after = get_table_snapshot(...)

```python
currencies_after = get_table_snapshot('Currency')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(countries_before, countries_after)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(currencies_before, currencies_after)
```

### Step 12: Call frappe.db.delete()

```python
frappe.db.delete('Currency')
```

### Step 13: Call frappe.db.delete()

```python
frappe.db.delete('Country')
```

### Step 14: Call country.db_insert()

```python
country.db_insert(ignore_if_duplicate=True)
```

### Step 15: Call currency.db_insert()

```python
currency.db_insert(ignore_if_duplicate=True)
```


## Complete Example

```python
# Workflow
def clear_tables():
    frappe.db.delete('Currency')
    frappe.db.delete('Country')
clear_tables()
import_country_and_currency()
countries_before = get_table_snapshot('Country')
currencies_before = get_table_snapshot('Currency')
clear_tables()
countries, currencies = get_countries_and_currencies()
for country in countries:
    country.db_insert(ignore_if_duplicate=True)
for currency in currencies:
    currency.db_insert(ignore_if_duplicate=True)
enable_default_currencies()
countries_after = get_table_snapshot('Country')
currencies_after = get_table_snapshot('Currency')
self.assertEqual(countries_before, countries_after)
self.assertEqual(currencies_before, currencies_after)
```

## Next Steps


---

*Source: test_country.py:24 | Complexity: Advanced | Last updated: 2026-02-04*