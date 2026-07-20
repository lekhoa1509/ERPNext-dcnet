# How To: Get Data

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get data

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.defaults`
- `frappe.contacts.report.addresses_and_contacts.addresses_and_contacts`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign linked_docs = value

```python
linked_docs = [get_custom_doc_for_address_and_contacts()]
```

### Step 2: Assign links_list = value

```python
links_list = [item.name for item in linked_docs]
```

### Step 3: Assign d = create_linked_address(...)

```python
d = create_linked_address(links_list)
```

### Step 4: Call create_linked_contact()

```python
create_linked_contact(links_list, d)
```

### Step 5: Assign report_data = get_data(...)

```python
report_data = get_data({'reference_doctype': 'Test Custom Doctype'})
```

### Step 6: Assign test_item = value

```python
test_item = [link, 'test address line 1', 'test address line 2', 'Milan', None, None, 'Italy', 0, '_Test First Name', '_Test Last Name', '_Test Address-Billing', '+91 0000000020', '', 'test_contact@example.com', 1]
```

### Step 7: Call self.assertListEqual()

```python
self.assertListEqual(test_item, report_data[idx])
```


## Complete Example

```python
# Workflow
linked_docs = [get_custom_doc_for_address_and_contacts()]
links_list = [item.name for item in linked_docs]
d = create_linked_address(links_list)
create_linked_contact(links_list, d)
report_data = get_data({'reference_doctype': 'Test Custom Doctype'})
for idx, link in enumerate(links_list):
    test_item = [link, 'test address line 1', 'test address line 2', 'Milan', None, None, 'Italy', 0, '_Test First Name', '_Test Last Name', '_Test Address-Billing', '+91 0000000020', '', 'test_contact@example.com', 1]
    self.assertListEqual(test_item, report_data[idx])
```

## Next Steps


---

*Source: test_addresses_and_contacts.py:89 | Complexity: Intermediate | Last updated: 2026-02-04*