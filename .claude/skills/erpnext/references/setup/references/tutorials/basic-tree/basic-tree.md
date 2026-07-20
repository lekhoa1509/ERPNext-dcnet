# How To: Basic Tree

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test basic tree

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts`
- `erpnext.setup.doctype.company.company`
- `erpnext.setup.demo`

**Setup Required:**
```python
# Fixtures: records
```

## Step-by-Step Guide

### Step 1: Assign min_lft = 1

```python
min_lft = 1
```

### Step 2: Assign max_rgt = value

```python
max_rgt = frappe.db.sql('select max(rgt) from `tabCompany`')[0][0]
```

### Step 3: Assign records = value

```python
records = self.globalTestRecords['Company'][2:]
```

### Step 4: Assign unknown = frappe.db.get_value(...)

```python
lft, rgt, parent_company = frappe.db.get_value('Company', company['company_name'], ['lft', 'rgt', 'parent_company'])
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(lft)
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(rgt)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(lft < rgt)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(parent_lft < parent_rgt)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(lft > parent_lft)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(rgt < parent_rgt)
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(lft >= min_lft)
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(rgt <= max_rgt)
```

### Step 13: Assign unknown = frappe.db.get_value(...)

```python
parent_lft, parent_rgt = frappe.db.get_value('Company', parent_company, ['lft', 'rgt'])
```

### Step 14: Assign parent_lft = value

```python
parent_lft = min_lft - 1
```

### Step 15: Assign parent_rgt = value

```python
parent_rgt = max_rgt + 1
```


## Complete Example

```python
# Setup
# Fixtures: records

# Workflow
min_lft = 1
max_rgt = frappe.db.sql('select max(rgt) from `tabCompany`')[0][0]
if not records:
    records = self.globalTestRecords['Company'][2:]
for company in records:
    lft, rgt, parent_company = frappe.db.get_value('Company', company['company_name'], ['lft', 'rgt', 'parent_company'])
    if parent_company:
        parent_lft, parent_rgt = frappe.db.get_value('Company', parent_company, ['lft', 'rgt'])
    else:
        parent_lft = min_lft - 1
        parent_rgt = max_rgt + 1
    self.assertTrue(lft)
    self.assertTrue(rgt)
    self.assertTrue(lft < rgt)
    self.assertTrue(parent_lft < parent_rgt)
    self.assertTrue(lft > parent_lft)
    self.assertTrue(rgt < parent_rgt)
    self.assertTrue(lft >= min_lft)
    self.assertTrue(rgt <= max_rgt)
```

## Next Steps


---

*Source: test_company.py:112 | Complexity: Advanced | Last updated: 2026-02-04*