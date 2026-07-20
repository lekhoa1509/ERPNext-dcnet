# How To: Parse Email

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test parse email

## Prerequisites

**Required Modules:**
- `typing`
- `frappe`
- `frappe.core.doctype.communication.communication`
- `frappe.core.doctype.communication.email`
- `frappe.email.doctype.email_queue.email_queue`
- `frappe.tests`
- `frappe.contacts.doctype.contact.contact`
- `frappe.email.doctype.email_account.email_account`
- `frappe.desk.form.load`


## Step-by-Step Guide

### Step 1: Assign to = 'Jon Doe <jon.doe@example.org>'

```python
to = 'Jon Doe <jon.doe@example.org>'
```

### Step 2: Assign cc = '=?UTF-8?Q?Max_Mu=C3=9F?= <max.muss@examle.org>,\n\terp+Customer=Plus%2BCompany@example.org,\n\terp+Customer+Space%20Company@example.org,\n\terp+Customer+Space+Company+Plus+Encoded@example.org'

```python
cc = '=?UTF-8?Q?Max_Mu=C3=9F?= <max.muss@examle.org>,\n\terp+Customer=Plus%2BCompany@example.org,\n\terp+Customer+Space%20Company@example.org,\n\terp+Customer+Space+Company+Plus+Encoded@example.org'
```

### Step 3: Assign bcc = ''

```python
bcc = ''
```

### Step 4: Assign results = list(...)

```python
results = list(parse_email([to, cc, bcc]))
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual([('Customer', 'Plus+Company'), ('Customer', 'Space Company'), ('Customer', 'Space Company Plus Encoded')], results)
```

### Step 6: Assign results = list(...)

```python
results = list(parse_email([to, bcc]))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(results, [])
```

### Step 8: Assign to = 'jane.doe+A+Test@example.org'

```python
to = 'jane.doe+A+Test@example.org'
```

### Step 9: Assign cc = ''

```python
cc = ''
```

### Step 10: Assign bcc = '=?UTF-8?Q?Max_Mu=C3=9F?= <max.muss+Note=Very%20important@examle.org>'

```python
bcc = '=?UTF-8?Q?Max_Mu=C3=9F?= <max.muss+Note=Very%20important@examle.org>'
```

### Step 11: Assign results = list(...)

```python
results = list(parse_email([to, cc, bcc]))
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual([('A', 'Test'), ('Note', 'Very important')], results)
```


## Complete Example

```python
# Workflow
to = 'Jon Doe <jon.doe@example.org>'
cc = '=?UTF-8?Q?Max_Mu=C3=9F?= <max.muss@examle.org>,\n\terp+Customer=Plus%2BCompany@example.org,\n\terp+Customer+Space%20Company@example.org,\n\terp+Customer+Space+Company+Plus+Encoded@example.org'
bcc = ''
results = list(parse_email([to, cc, bcc]))
self.assertEqual([('Customer', 'Plus+Company'), ('Customer', 'Space Company'), ('Customer', 'Space Company Plus Encoded')], results)
results = list(parse_email([to, bcc]))
self.assertEqual(results, [])
to = 'jane.doe+A+Test@example.org'
cc = ''
bcc = '=?UTF-8?Q?Max_Mu=C3=9F?= <max.muss+Note=Very%20important@examle.org>'
results = list(parse_email([to, cc, bcc]))
self.assertEqual([('A', 'Test'), ('Note', 'Very important')], results)
```

## Next Steps


---

*Source: test_communication.py:219 | Complexity: Advanced | Last updated: 2026-02-04*