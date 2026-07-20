# How To: Webhook With Array Body

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: Check if array request body are supported.

## Prerequisites

**Required Modules:**
- `json`
- `contextlib`
- `responses`
- `responses.matchers`
- `frappe`
- `frappe.integrations.doctype.webhook`
- `frappe.integrations.doctype.webhook.webhook`
- `frappe.tests`
- `frappe.tests.classes.context_managers`


## Step-by-Step Guide

### Step 1: 'Check if array request body are supported.'

```python
'Check if array request body are supported.'
```

### Step 2: Assign wh_config = value

```python
wh_config = {'doctype': 'Webhook', 'webhook_doctype': 'Note', 'webhook_docevent': 'on_change', 'enabled': 1, 'request_url': 'https://httpbin.org/post', 'request_method': 'POST', 'request_structure': 'JSON', 'webhook_json': '[\r\n{% for n in range(3) %}\r\n    {\r\n        "title": "{{ doc.title }}"    }\r\n    {%- if not loop.last -%}\r\n        , \r\n    {%endif%}\r\n{%endfor%}\r\n]', 'meets_condition': 'Yes', 'webhook_headers': [{'key': 'Content-Type', 'value': 'application/json'}]}
```

### Step 3: Assign doc = frappe.new_doc(...)

```python
doc = frappe.new_doc('Note')
```

### Step 4: Assign doc.title = 'Test Webhook Note'

```python
doc.title = 'Test Webhook Note'
```

### Step 5: Assign final_title = frappe.generate_hash(...)

```python
final_title = frappe.generate_hash()
```

### Step 6: Assign expected_req = value

```python
expected_req = [{'title': final_title} for _ in range(3)]
```

### Step 7: Call self.responses.add()

```python
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json=expected_req, match=[json_params_matcher(expected_req)])
```

### Step 8: Call doc.insert()

```python
doc.insert()
```

### Step 9: Call doc.reload()

```python
doc.reload()
```

### Step 10: Call doc.save()

```python
doc.save()
```

### Step 11: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc(doc.doctype, doc.name)
```

### Step 12: Assign doc.title = final_title

```python
doc.title = final_title
```

### Step 13: Call doc.save()

```python
doc.save()
```

### Step 14: Call flush_webhook_execution_queue()

```python
flush_webhook_execution_queue()
```

### Step 15: Assign log = frappe.get_last_doc(...)

```python
log = frappe.get_last_doc('Webhook Request Log')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(len(json.loads(log.response)), 3)
```


## Complete Example

```python
# Workflow
'Check if array request body are supported.'
wh_config = {'doctype': 'Webhook', 'webhook_doctype': 'Note', 'webhook_docevent': 'on_change', 'enabled': 1, 'request_url': 'https://httpbin.org/post', 'request_method': 'POST', 'request_structure': 'JSON', 'webhook_json': '[\r\n{% for n in range(3) %}\r\n    {\r\n        "title": "{{ doc.title }}"    }\r\n    {%- if not loop.last -%}\r\n        , \r\n    {%endif%}\r\n{%endfor%}\r\n]', 'meets_condition': 'Yes', 'webhook_headers': [{'key': 'Content-Type', 'value': 'application/json'}]}
doc = frappe.new_doc('Note')
doc.title = 'Test Webhook Note'
final_title = frappe.generate_hash()
expected_req = [{'title': final_title} for _ in range(3)]
self.responses.add(responses.POST, 'https://httpbin.org/post', status=200, json=expected_req, match=[json_params_matcher(expected_req)])
with get_test_webhook(wh_config):
    doc.insert()
    doc.reload()
    doc.save()
    doc = frappe.get_doc(doc.doctype, doc.name)
    doc.title = final_title
    doc.save()
    flush_webhook_execution_queue()
    log = frappe.get_last_doc('Webhook Request Log')
    self.assertEqual(len(json.loads(log.response)), 3)
```

## Next Steps


---

*Source: test_webhook.py:226 | Complexity: Advanced | Last updated: 2026-02-04*