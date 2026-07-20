# How To: Lapsed Contract Status

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test lapsed contract status

## Prerequisites

**Required Modules:**
- `unittest`
- `frappe`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign self.contract_doc.contract_term = '_Test Customer Contract with Requirements'

```python
self.contract_doc.contract_term = '_Test Customer Contract with Requirements'
```

### Step 2: Assign self.contract_doc.start_date = add_days(...)

```python
self.contract_doc.start_date = add_days(nowdate(), -2)
```

### Step 3: Assign self.contract_doc.end_date = add_days(...)

```python
self.contract_doc.end_date = add_days(nowdate(), 1)
```

### Step 4: Assign self.contract_doc.requires_fulfilment = 1

```python
self.contract_doc.requires_fulfilment = 1
```

### Step 5: Assign self.contract_doc.fulfilment_deadline = add_days(...)

```python
self.contract_doc.fulfilment_deadline = add_days(nowdate(), -1)
```

### Step 6: Call self.contract_doc.save()

```python
self.contract_doc.save()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(self.contract_doc.fulfilment_status, 'Lapsed')
```


## Complete Example

```python
# Workflow
self.contract_doc.contract_term = '_Test Customer Contract with Requirements'
self.contract_doc.start_date = add_days(nowdate(), -2)
self.contract_doc.end_date = add_days(nowdate(), 1)
self.contract_doc.requires_fulfilment = 1
self.contract_doc.fulfilment_deadline = add_days(nowdate(), -1)
self.contract_doc.save()
self.assertEqual(self.contract_doc.fulfilment_status, 'Lapsed')
```

## Next Steps


---

*Source: test_contract.py:93 | Complexity: Intermediate | Last updated: 2026-02-04*