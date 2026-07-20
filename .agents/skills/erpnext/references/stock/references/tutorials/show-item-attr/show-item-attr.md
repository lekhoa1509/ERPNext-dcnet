# How To: Show Item Attr

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test show item attr

## Prerequisites

**Required Modules:**
- `typing`
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.report.stock_balance.stock_balance`
- `erpnext.controllers.item_variant`


## Step-by-Step Guide

### Step 1: Assign self.item.has_variants = True

```python
self.item.has_variants = True
```

### Step 2: Call self.item.append()

```python
self.item.append('attributes', {'attribute': 'Test Size'})
```

### Step 3: Call self.item.save()

```python
self.item.save()
```

### Step 4: Assign attributes = value

```python
attributes = {'Test Size': 'Large'}
```

### Step 5: Assign variant = create_variant(...)

```python
variant = create_variant(self.item.name, attributes)
```

### Step 6: Call variant.save()

```python
variant.save()
```

### Step 7: Call self.generate_stock_ledger()

```python
self.generate_stock_ledger(variant.name, [_dict(qty=5, rate=10)])
```

### Step 8: Assign rows = stock_balance(...)

```python
rows = stock_balance(self.filters.update({'show_variant_attributes': 1, 'item_code': [variant.name]}))
```

### Step 9: Call self.assertPartialDictEq()

```python
self.assertPartialDictEq(attributes, rows[0])
```

### Step 10: Call self.assertInvariants()

```python
self.assertInvariants(rows)
```


## Complete Example

```python
# Workflow
from erpnext.controllers.item_variant import create_variant
self.item.has_variants = True
self.item.append('attributes', {'attribute': 'Test Size'})
self.item.save()
attributes = {'Test Size': 'Large'}
variant = create_variant(self.item.name, attributes)
variant.save()
self.generate_stock_ledger(variant.name, [_dict(qty=5, rate=10)])
rows = stock_balance(self.filters.update({'show_variant_attributes': 1, 'item_code': [variant.name]}))
self.assertPartialDictEq(attributes, rows[0])
self.assertInvariants(rows)
```

## Next Steps


---

*Source: test_stock_balance.py:156 | Complexity: Advanced | Last updated: 2026-02-04*