# How To: Db Keywords As Fields

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Tests if DB keywords work as docfield names. If they're wrapped with grave accents.

## Prerequisites

**Required Modules:**
- `datetime`
- `math`
- `random`
- `unittest.mock`
- `frappe`
- `frappe.core.utils`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.database`
- `frappe.database.database`
- `frappe.database.utils`
- `frappe.query_builder`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.tests.test_query_builder`
- `frappe.utils`
- `frappe.utils.data`
- `frappe.utils.testutils`
- `frappe.database.database`
- `frappe.database.postgres.database`
- `frappe.database.postgres.database`
- `psycopg2.errors`
- `frappe.core.doctype.doctype.test_doctype`
- `contextlib`
- `os`
- `re`
- `frappe.database.postgres.database`


## Step-by-Step Guide

### Step 1: "Tests if DB keywords work as docfield names. If they're wrapped with grave accents."

```python
"Tests if DB keywords work as docfield names. If they're wrapped with grave accents."
```

### Step 2: Assign all_keywords = value

```python
all_keywords = {'mariadb': ['CHARACTER', 'DELAYED', 'LINES', 'EXISTS', 'YEAR_MONTH', 'LOCALTIME', 'BOTH', 'MEDIUMINT', 'LEFT', 'BINARY', 'DEFAULT', 'KILL', 'WRITE', 'SQL_SMALL_RESULT', 'CURRENT_TIME', 'CROSS', 'INHERITS', 'SELECT', 'TABLE', 'ALTER', 'CURRENT_TIMESTAMP', 'XOR', 'CASE', 'ALL', 'WHERE', 'INT', 'TO', 'SOME', 'DAY_MINUTE', 'ERRORS', 'OPTIMIZE', 'REPLACE', 'HIGH_PRIORITY', 'VARBINARY', 'HELP', 'IS', 'CHAR', 'DESCRIBE', 'KEY'], 'postgres': ['WORK', 'LANCOMPILER', 'REAL', 'HAVING', 'REPEATABLE', 'DATA', 'USING', 'BIT', 'DEALLOCATE', 'SERIALIZABLE', 'CURSOR', 'INHERITS', 'ARRAY', 'TRUE', 'IGNORE', 'PARAMETER_MODE', 'ROW', 'CHECKPOINT', 'SHOW', 'BY', 'SIZE', 'SCALE', 'UNENCRYPTED', 'WITH', 'AND', 'CONVERT', 'FIRST', 'SCOPE', 'WRITE', 'INTERVAL', 'CHARACTER_SET_SCHEMA', 'ADD', 'SCROLL', 'NULL', 'WHEN', 'TRANSACTION_ACTIVE', 'INT', 'FORTRAN', 'STABLE']}
```

### Step 3: Assign created_docs = value

```python
created_docs = []
```

### Step 4: Assign fields = value

```python
fields = all_keywords[frappe.conf.db_type][:1]
```

### Step 5: Assign test_doctype = 'ToDo'

```python
test_doctype = 'ToDo'
```

### Step 6: Assign random_field = choice.lower(...)

```python
random_field = choice(fields).lower()
```

### Step 7: Assign random_doc = choice(...)

```python
random_doc = choice(created_docs)
```

### Step 8: Assign random_value = random_string(...)

```python
random_value = random_string(20)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[random_field], limit=1)[0])), random_field)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[f'`{random_field}` as total'], limit=1)[0])), 'total')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[f'`{random_field}` as total'], distinct=True, limit=1)[0])), 'total')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[f'`{random_field}`'], distinct=True, limit=1)[0])), random_field)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[{'COUNT': random_field}], limit=1, order_by=None)[0])), 'count' if frappe.conf.db_type == 'postgres' else f'COUNT(`{random_field}`)')
```

### Step 14: Call frappe.db.set_value()

```python
frappe.db.set_value(test_doctype, random_doc, random_field, random_value)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(frappe.db.get_value(test_doctype, random_doc, random_field), random_value)
```

### Step 16: Call clear_custom_fields()

```python
clear_custom_fields(test_doctype)
```

### Step 17: Call create_custom_field()

```python
create_custom_field(test_doctype, {'fieldname': field.lower(), 'label': field.title(), 'fieldtype': 'Data'})
```

### Step 18: Call add_custom_field()

```python
add_custom_field(field)
```

### Step 19: Assign docfields = value

```python
docfields = {key.lower(): random_string(10) for key in fields}
```

### Step 20: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc({'doctype': test_doctype, 'description': random_string(20), **docfields})
```

### Step 21: Call doc.insert()

```python
doc.insert()
```

### Step 22: Call created_docs.append()

```python
created_docs.append(doc.name)
```

### Step 23: Call frappe.delete_doc()

```python
frappe.delete_doc(test_doctype, doc)
```


## Complete Example

```python
# Workflow
"Tests if DB keywords work as docfield names. If they're wrapped with grave accents."
all_keywords = {'mariadb': ['CHARACTER', 'DELAYED', 'LINES', 'EXISTS', 'YEAR_MONTH', 'LOCALTIME', 'BOTH', 'MEDIUMINT', 'LEFT', 'BINARY', 'DEFAULT', 'KILL', 'WRITE', 'SQL_SMALL_RESULT', 'CURRENT_TIME', 'CROSS', 'INHERITS', 'SELECT', 'TABLE', 'ALTER', 'CURRENT_TIMESTAMP', 'XOR', 'CASE', 'ALL', 'WHERE', 'INT', 'TO', 'SOME', 'DAY_MINUTE', 'ERRORS', 'OPTIMIZE', 'REPLACE', 'HIGH_PRIORITY', 'VARBINARY', 'HELP', 'IS', 'CHAR', 'DESCRIBE', 'KEY'], 'postgres': ['WORK', 'LANCOMPILER', 'REAL', 'HAVING', 'REPEATABLE', 'DATA', 'USING', 'BIT', 'DEALLOCATE', 'SERIALIZABLE', 'CURSOR', 'INHERITS', 'ARRAY', 'TRUE', 'IGNORE', 'PARAMETER_MODE', 'ROW', 'CHECKPOINT', 'SHOW', 'BY', 'SIZE', 'SCALE', 'UNENCRYPTED', 'WITH', 'AND', 'CONVERT', 'FIRST', 'SCOPE', 'WRITE', 'INTERVAL', 'CHARACTER_SET_SCHEMA', 'ADD', 'SCROLL', 'NULL', 'WHEN', 'TRANSACTION_ACTIVE', 'INT', 'FORTRAN', 'STABLE']}
created_docs = []
fields = all_keywords[frappe.conf.db_type][:1]
test_doctype = 'ToDo'

def add_custom_field(field):
    create_custom_field(test_doctype, {'fieldname': field.lower(), 'label': field.title(), 'fieldtype': 'Data'})
for field in fields:
    add_custom_field(field)
for _ in range(10):
    docfields = {key.lower(): random_string(10) for key in fields}
    doc = frappe.get_doc({'doctype': test_doctype, 'description': random_string(20), **docfields})
    doc.insert()
    created_docs.append(doc.name)
random_field = choice(fields).lower()
random_doc = choice(created_docs)
random_value = random_string(20)
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[random_field], limit=1)[0])), random_field)
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[f'`{random_field}` as total'], limit=1)[0])), 'total')
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[f'`{random_field}` as total'], distinct=True, limit=1)[0])), 'total')
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[f'`{random_field}`'], distinct=True, limit=1)[0])), random_field)
self.assertEqual(next(iter(frappe.get_all('ToDo', fields=[{'COUNT': random_field}], limit=1, order_by=None)[0])), 'count' if frappe.conf.db_type == 'postgres' else f'COUNT(`{random_field}`)')
frappe.db.set_value(test_doctype, random_doc, random_field, random_value)
self.assertEqual(frappe.db.get_value(test_doctype, random_doc, random_field), random_value)
for doc in created_docs:
    frappe.delete_doc(test_doctype, doc)
clear_custom_fields(test_doctype)
```

## Next Steps


---

*Source: test_db.py:253 | Complexity: Advanced | Last updated: 2026-02-04*