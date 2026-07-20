# How To: File With Percent In Filename

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test file with percent in filename

## Prerequisites

**Required Modules:**
- `typing`
- `urllib.parse`
- `requests`
- `frappe`
- `frappe.email.receive`
- `frappe.tests`
- `frappe.utils`
- `frappe.core.doctype.file.file`


## Step-by-Step Guide

### Step 1: Call make_and_check_file()

```python
make_and_check_file(1, '1test%2542.txt', '1test_2542.txt')
```

**Verification:**
```python
assert file.file_url
```

### Step 2: Call make_and_check_file()

```python
make_and_check_file(2, '2test%42.txt', '2test_42.txt')
```

### Step 3: Call make_and_check_file()

```python
make_and_check_file(3, '3test*.txt', '3test*.txt')
```

### Step 4: Assign content = 'abcdefghijklmnop_attachment'

```python
content = 'abcdefghijklmnop_attachment'
```

### Step 5: Call file.update()

```python
file.update({'file_name': literal_file_name, 'is_private': 0, 'content': f'{content}{index}'})
```

### Step 6: Call file.save()

```python
file.save()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(file.file_name, literal_file_name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(file.file_url, '/files/' + disk_file_name)
```

**Verification:**
```python
assert file.file_url
```

### Step 9: Assign res = requests.get(...)

```python
res = requests.get(get_url(quote(file.file_url)))
```

### Step 10: Call res.raise_for_status()

```python
res.raise_for_status()
```

### Step 11: Assign res = requests.get(...)

```python
res = requests.get(get_url('/files/' + disk_file_name))
```

### Step 12: Call res.raise_for_status()

```python
res.raise_for_status()
```

### Step 13: Assign values = file.as_dict(...)

```python
values = file.as_dict()
```

### Step 14: Call file.save()

```python
file.save()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(file.file_name, literal_file_name)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(file.file_url, values['file_url'])
```


## Complete Example

```python
# Workflow
def make_and_check_file(index: int, literal_file_name: str, disk_file_name: str):
    content = 'abcdefghijklmnop_attachment'
    file: File = frappe.new_doc('File')
    file.update({'file_name': literal_file_name, 'is_private': 0, 'content': f'{content}{index}'})
    file.save()
    self.assertEqual(file.file_name, literal_file_name)
    self.assertEqual(file.file_url, '/files/' + disk_file_name)
    assert file.file_url
    res = requests.get(get_url(quote(file.file_url)))
    res.raise_for_status()
    res = requests.get(get_url('/files/' + disk_file_name))
    res.raise_for_status()
    values = file.as_dict()
    file.save()
    self.assertEqual(file.file_name, literal_file_name)
    self.assertEqual(file.file_url, values['file_url'])
make_and_check_file(1, '1test%2542.txt', '1test_2542.txt')
make_and_check_file(2, '2test%42.txt', '2test_42.txt')
make_and_check_file(3, '3test*.txt', '3test*.txt')
```

## Next Steps


---

*Source: test_email_attachments.py:51 | Complexity: Advanced | Last updated: 2026-02-04*