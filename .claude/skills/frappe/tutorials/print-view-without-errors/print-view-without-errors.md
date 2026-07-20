# How To: Print View Without Errors

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test print view without errors

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.tests`
- `frappe.www.printview`


## Step-by-Step Guide

### Step 1: Assign user = frappe.get_last_doc(...)

```python
user = frappe.get_last_doc('User')
```

### Step 2: Assign messages_before = frappe.get_message_log(...)

```python
messages_before = frappe.get_message_log()
```

### Step 3: Assign ret = get_html_and_style(...)

```python
ret = get_html_and_style(doc=user.as_json(), print_format='Standard', no_letterhead=1)
```

### Step 4: Assign messages_after = frappe.get_message_log(...)

```python
messages_after = frappe.get_message_log()
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(bool(ret['html']))
```

### Step 6: Assign new_messages = value

```python
new_messages = messages_after[len(messages_before):]
```

### Step 7: Call self.fail()

```python
self.fail('Print view showing error/warnings: \n' + '\n'.join((str(msg) for msg in new_messages)))
```


## Complete Example

```python
# Workflow
user = frappe.get_last_doc('User')
messages_before = frappe.get_message_log()
ret = get_html_and_style(doc=user.as_json(), print_format='Standard', no_letterhead=1)
messages_after = frappe.get_message_log()
if len(messages_after) > len(messages_before):
    new_messages = messages_after[len(messages_before):]
    self.fail('Print view showing error/warnings: \n' + '\n'.join((str(msg) for msg in new_messages)))
self.assertTrue(bool(ret['html']))
```

## Next Steps


---

*Source: test_printview.py:8 | Complexity: Intermediate | Last updated: 2026-02-04*