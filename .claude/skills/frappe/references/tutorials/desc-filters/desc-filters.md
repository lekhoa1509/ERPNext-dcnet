# How To: Desc Filters

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test desc filters

## Prerequisites

**Required Modules:**
- `unittest.mock`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.treeview`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.nestedset`


## Step-by-Step Guide

### Step 1: Assign linked_doctype = value

```python
linked_doctype = new_doctype(fields=[{'fieldname': 'link_field', 'fieldtype': 'Link', 'options': TEST_DOCTYPE}]).insert().name
```

### Step 2: Assign record = 'Child 1'

```python
record = 'Child 1'
```

### Step 3: Assign exclusive_filter = value

```python
exclusive_filter = {'name': ('descendants of', record)}
```

### Step 4: Assign inclusive_filter = value

```python
inclusive_filter = {'name': ('descendants of (inclusive)', record)}
```

### Step 5: Assign exclusive_link = value

```python
exclusive_link = {'link_field': ('descendants of', record)}
```

### Step 6: Assign inclusive_link = value

```python
inclusive_link = {'link_field': ('descendants of (inclusive)', record)}
```

### Step 7: Call self.assertNotIn()

```python
self.assertNotIn(record, frappe.get_all(TEST_DOCTYPE, exclusive_filter, run=0).get_sql())
```

### Step 8: Call self.assertIn()

```python
self.assertIn(record, frappe.get_all(TEST_DOCTYPE, inclusive_filter, run=0).get_sql())
```

### Step 9: Call self.assertNotIn()

```python
self.assertNotIn(record, frappe.get_all(linked_doctype, exclusive_link, run=0).get_sql())
```

### Step 10: Call self.assertIn()

```python
self.assertIn(record, frappe.get_all(linked_doctype, inclusive_link, run=0).get_sql())
```

### Step 11: Call self.assertNotIn()

```python
self.assertNotIn(record, str(frappe.qb.get_query(TEST_DOCTYPE, filters=exclusive_filter)))
```

### Step 12: Call self.assertIn()

```python
self.assertIn(record, str(frappe.qb.get_query(TEST_DOCTYPE, filters=inclusive_filter)))
```

### Step 13: Call self.assertNotIn()

```python
self.assertNotIn(record, str(frappe.qb.get_query(table=linked_doctype, filters=exclusive_link)))
```

### Step 14: Call self.assertIn()

```python
self.assertIn(record, str(frappe.qb.get_query(table=linked_doctype, filters=inclusive_link)))
```


## Complete Example

```python
# Workflow
linked_doctype = new_doctype(fields=[{'fieldname': 'link_field', 'fieldtype': 'Link', 'options': TEST_DOCTYPE}]).insert().name
record = 'Child 1'
exclusive_filter = {'name': ('descendants of', record)}
inclusive_filter = {'name': ('descendants of (inclusive)', record)}
exclusive_link = {'link_field': ('descendants of', record)}
inclusive_link = {'link_field': ('descendants of (inclusive)', record)}
self.assertNotIn(record, frappe.get_all(TEST_DOCTYPE, exclusive_filter, run=0).get_sql())
self.assertIn(record, frappe.get_all(TEST_DOCTYPE, inclusive_filter, run=0).get_sql())
self.assertNotIn(record, frappe.get_all(linked_doctype, exclusive_link, run=0).get_sql())
self.assertIn(record, frappe.get_all(linked_doctype, inclusive_link, run=0).get_sql())
self.assertNotIn(record, str(frappe.qb.get_query(TEST_DOCTYPE, filters=exclusive_filter)))
self.assertIn(record, str(frappe.qb.get_query(TEST_DOCTYPE, filters=inclusive_filter)))
self.assertNotIn(record, str(frappe.qb.get_query(table=linked_doctype, filters=exclusive_link)))
self.assertIn(record, str(frappe.qb.get_query(table=linked_doctype, filters=inclusive_link)))
```

## Next Steps


---

*Source: test_nestedset.py:265 | Complexity: Advanced | Last updated: 2026-02-04*