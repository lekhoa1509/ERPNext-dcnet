# How To: Unix Ts Mariadb

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test unix ts mariadb

## Prerequisites

**Required Modules:**
- `unittest`
- `collections.abc`
- `datetime`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.query_builder`
- `frappe.query_builder.builder`
- `frappe.query_builder.custom`
- `frappe.query_builder.functions`
- `frappe.query_builder.utils`
- `frappe.tests`
- `frappe.query_builder.terms`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder`
- `frappe.query_builder.utils`


## Step-by-Step Guide

### Step 1: Assign note = frappe.qb.DocType(...)

```python
note = frappe.qb.DocType('Note')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual('unix_timestamp(posting_date)', UnixTimestamp(note.posting_date).get_sql())
```

### Step 3: Assign todo = frappe.qb.DocType(...)

```python
todo = frappe.qb.DocType('ToDo')
```

### Step 4: Assign select_query = frappe.qb.from_.join.on.select(...)

```python
select_query = frappe.qb.from_(note).join(todo).on(todo.refernce_name == note.name).select(UnixTimestamp(note.posting_date))
```

### Step 5: Call self.assertIn()

```python
self.assertIn('select unix_timestamp(`tabnote`.`posting_date`)', str(select_query).lower())
```

### Step 6: Assign select_query = select_query.orderby(...)

```python
select_query = select_query.orderby(UnixTimestamp(note.posting_date))
```

### Step 7: Call self.assertIn()

```python
self.assertIn('order by unix_timestamp(`tabnote`.`posting_date`)', str(select_query).lower())
```

### Step 8: Assign select_query = select_query.where(...)

```python
select_query = select_query.where(UnixTimestamp(note.posting_date) >= UnixTimestamp('2021-01-01'))
```

### Step 9: Call self.assertIn()

```python
self.assertIn("unix_timestamp(`tabnote`.`posting_date`)>=unix_timestamp('2021-01-01')", str(select_query).lower())
```

### Step 10: Assign select_query = select_query.select(...)

```python
select_query = select_query.select(UnixTimestamp(note.posting_date, alias='unix_ts'))
```

### Step 11: Call self.assertIn()

```python
self.assertIn('unix_timestamp(`tabnote`.`posting_date`) `unix_ts`', str(select_query).lower())
```


## Complete Example

```python
# Workflow
note = frappe.qb.DocType('Note')
self.assertEqual('unix_timestamp(posting_date)', UnixTimestamp(note.posting_date).get_sql())
todo = frappe.qb.DocType('ToDo')
select_query = frappe.qb.from_(note).join(todo).on(todo.refernce_name == note.name).select(UnixTimestamp(note.posting_date))
self.assertIn('select unix_timestamp(`tabnote`.`posting_date`)', str(select_query).lower())
select_query = select_query.orderby(UnixTimestamp(note.posting_date))
self.assertIn('order by unix_timestamp(`tabnote`.`posting_date`)', str(select_query).lower())
select_query = select_query.where(UnixTimestamp(note.posting_date) >= UnixTimestamp('2021-01-01'))
self.assertIn("unix_timestamp(`tabnote`.`posting_date`)>=unix_timestamp('2021-01-01')", str(select_query).lower())
select_query = select_query.select(UnixTimestamp(note.posting_date, alias='unix_ts'))
self.assertIn('unix_timestamp(`tabnote`.`posting_date`) `unix_ts`', str(select_query).lower())
```

## Next Steps


---

*Source: test_query_builder.py:93 | Complexity: Advanced | Last updated: 2026-02-04*