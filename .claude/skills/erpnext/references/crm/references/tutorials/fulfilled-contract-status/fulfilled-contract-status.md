# How To: Fulfilled Contract Status

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test fulfilled contract status

## Prerequisites

**Required Modules:**
- `unittest`
- `frappe`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign self.contract_doc.contract_terms = '_Test Customer Contract with Requirements'

```python
self.contract_doc.contract_terms = '_Test Customer Contract with Requirements'
```

### Step 2: Assign self.contract_doc.requires_fulfilment = 1

```python
self.contract_doc.requires_fulfilment = 1
```

### Step 3: Assign fulfilment_terms = value

```python
fulfilment_terms = []
```

### Step 4: Call fulfilment_terms.append()

```python
fulfilment_terms.append({'requirement': 'This is a test requirement.', 'fulfilled': 0})
```

### Step 5: Call self.contract_doc.set()

```python
self.contract_doc.set('fulfilment_terms', fulfilment_terms)
```

### Step 6: Call self.contract_doc.save()

```python
self.contract_doc.save()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(self.contract_doc.fulfilment_status, 'Fulfilled')
```

### Step 8: Assign term.fulfilled = 1

```python
term.fulfilled = 1
```


## Complete Example

```python
# Workflow
self.contract_doc.contract_terms = '_Test Customer Contract with Requirements'
self.contract_doc.requires_fulfilment = 1
fulfilment_terms = []
fulfilment_terms.append({'requirement': 'This is a test requirement.', 'fulfilled': 0})
self.contract_doc.set('fulfilment_terms', fulfilment_terms)
for term in self.contract_doc.fulfilment_terms:
    term.fulfilled = 1
self.contract_doc.save()
self.assertEqual(self.contract_doc.fulfilment_status, 'Fulfilled')
```

## Next Steps


---

*Source: test_contract.py:61 | Complexity: Advanced | Last updated: 2026-02-04*