# How To: Timestamp

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test timestamp

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
self.assertEqual('posting_date+posting_time', CombineDatetime(note.posting_date, note.posting_time).get_sql())
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual("CAST('2021-01-01' AS DATE)+CAST('00:00:21' AS TIME)", CombineDatetime('2021-01-01', '00:00:21').get_sql())
```

### Step 4: Assign todo = frappe.qb.DocType(...)

```python
todo = frappe.qb.DocType('ToDo')
```

### Step 5: Assign select_query = frappe.qb.from_.join.on.select(...)

```python
select_query = frappe.qb.from_(note).join(todo).on(todo.refernce_name == note.name).select(CombineDatetime(note.posting_date, note.posting_time))
```

### Step 6: Call self.assertIn()

```python
self.assertIn('select "tabnote"."posting_date"+"tabnote"."posting_time"', str(select_query).lower())
```

### Step 7: Assign select_query = select_query.orderby(...)

```python
select_query = select_query.orderby(CombineDatetime(note.posting_date, note.posting_time))
```

### Step 8: Call self.assertIn()

```python
self.assertIn('order by "tabnote"."posting_date"+"tabnote"."posting_time"', str(select_query).lower())
```

### Step 9: Assign select_query = select_query.where(...)

```python
select_query = select_query.where(CombineDatetime(note.posting_date, note.posting_time) >= CombineDatetime('2021-01-01', '00:00:01'))
```

### Step 10: Call self.assertIn()

```python
self.assertIn('where "tabnote"."posting_date"+"tabnote"."posting_time">=cast(\'2021-01-01\' as date)+cast(\'00:00:01\' as time)', str(select_query).lower())
```

### Step 11: Assign select_query = select_query.select(...)

```python
select_query = select_query.select(CombineDatetime(note.posting_date, note.posting_time, alias='timestamp'))
```

### Step 12: Call self.assertIn()

```python
self.assertIn('"tabnote"."posting_date"+"tabnote"."posting_time" "timestamp"', str(select_query).lower())
```


## Complete Example

```python
# Workflow
note = frappe.qb.DocType('Note')
self.assertEqual('posting_date+posting_time', CombineDatetime(note.posting_date, note.posting_time).get_sql())
self.assertEqual("CAST('2021-01-01' AS DATE)+CAST('00:00:21' AS TIME)", CombineDatetime('2021-01-01', '00:00:21').get_sql())
todo = frappe.qb.DocType('ToDo')
select_query = frappe.qb.from_(note).join(todo).on(todo.refernce_name == note.name).select(CombineDatetime(note.posting_date, note.posting_time))
self.assertIn('select "tabnote"."posting_date"+"tabnote"."posting_time"', str(select_query).lower())
select_query = select_query.orderby(CombineDatetime(note.posting_date, note.posting_time))
self.assertIn('order by "tabnote"."posting_date"+"tabnote"."posting_time"', str(select_query).lower())
select_query = select_query.where(CombineDatetime(note.posting_date, note.posting_time) >= CombineDatetime('2021-01-01', '00:00:01'))
self.assertIn('where "tabnote"."posting_date"+"tabnote"."posting_time">=cast(\'2021-01-01\' as date)+cast(\'00:00:01\' as time)', str(select_query).lower())
select_query = select_query.select(CombineDatetime(note.posting_date, note.posting_time, alias='timestamp'))
self.assertIn('"tabnote"."posting_date"+"tabnote"."posting_time" "timestamp"', str(select_query).lower())
```

## Next Steps


---

*Source: test_query_builder.py:189 | Complexity: Advanced | Last updated: 2026-02-04*