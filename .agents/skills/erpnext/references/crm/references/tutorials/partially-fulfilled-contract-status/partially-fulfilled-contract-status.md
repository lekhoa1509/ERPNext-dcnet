# How To: Partially Fulfilled Contract Status

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test partially fulfilled contract status

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

### Step 3: Call self.contract_doc.save()

```python
self.contract_doc.save()
```

### Step 4: Assign fulfilment_terms = value

```python
fulfilment_terms = []
```

### Step 5: Call fulfilment_terms.append()

```python
fulfilment_terms.append({'requirement': 'This is a test requirement.', 'fulfilled': 0})
```

### Step 6: Call fulfilment_terms.append()

```python
fulfilment_terms.append({'requirement': 'This is another test requirement.', 'fulfilled': 0})
```

### Step 7: Call self.contract_doc.set()

```python
self.contract_doc.set('fulfilment_terms', fulfilment_terms)
```

### Step 8: Assign unknown.fulfilled = 1

```python
self.contract_doc.fulfilment_terms[0].fulfilled = 1
```

### Step 9: Call self.contract_doc.save()

```python
self.contract_doc.save()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(self.contract_doc.fulfilment_status, 'Partially Fulfilled')
```


## Complete Example

```python
# Workflow
self.contract_doc.contract_terms = '_Test Customer Contract with Requirements'
self.contract_doc.requires_fulfilment = 1
self.contract_doc.save()
fulfilment_terms = []
fulfilment_terms.append({'requirement': 'This is a test requirement.', 'fulfilled': 0})
fulfilment_terms.append({'requirement': 'This is another test requirement.', 'fulfilled': 0})
self.contract_doc.set('fulfilment_terms', fulfilment_terms)
self.contract_doc.fulfilment_terms[0].fulfilled = 1
self.contract_doc.save()
self.assertEqual(self.contract_doc.fulfilment_status, 'Partially Fulfilled')
```

## Next Steps


---

*Source: test_contract.py:77 | Complexity: Advanced | Last updated: 2026-02-04*