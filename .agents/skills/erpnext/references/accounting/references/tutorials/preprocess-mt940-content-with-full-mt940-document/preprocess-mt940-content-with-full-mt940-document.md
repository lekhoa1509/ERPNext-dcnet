# How To: Preprocess Mt940 Content With Full Mt940 Document

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: Test preprocessing with complete MT940 document

## Prerequisites

**Required Modules:**
- `unittest`
- `erpnext.accounts.doctype.bank_statement_import.bank_statement_import`


## Step-by-Step Guide

### Step 1: 'Test preprocessing with complete MT940 document'

```python
'Test preprocessing with complete MT940 document'
```

### Step 2: Assign mt940_content = ':20:STARTUMSE\n:25:12345678901234567890\n:28C:167619/1\n:60F:C031002EUR0,00\n:61:0310021002DR123,45NMSCNONREF//8327000090031789\n:86:806?20EREF+NONREF?21MREF+M180031?22CRED+DE98ZZZ09999999999\n:62F:C031002EUR-123,45\n-'

```python
mt940_content = ':20:STARTUMSE\n:25:12345678901234567890\n:28C:167619/1\n:60F:C031002EUR0,00\n:61:0310021002DR123,45NMSCNONREF//8327000090031789\n:86:806?20EREF+NONREF?21MREF+M180031?22CRED+DE98ZZZ09999999999\n:62F:C031002EUR-123,45\n-'
```

### Step 3: Assign expected_content = ':20:STARTUMSE\n:25:12345678901234567890\n:28C:67619/1\n:60F:C031002EUR0,00\n:61:0310021002DR123,45NMSCNONREF//8327000090031789\n:86:806?20EREF+NONREF?21MREF+M180031?22CRED+DE98ZZZ09999999999\n:62F:C031002EUR-123,45\n-'

```python
expected_content = ':20:STARTUMSE\n:25:12345678901234567890\n:28C:67619/1\n:60F:C031002EUR0,00\n:61:0310021002DR123,45NMSCNONREF//8327000090031789\n:86:806?20EREF+NONREF?21MREF+M180031?22CRED+DE98ZZZ09999999999\n:62F:C031002EUR-123,45\n-'
```

### Step 4: Assign result = preprocess_mt940_content(...)

```python
result = preprocess_mt940_content(mt940_content)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(result, expected_content)
```


## Complete Example

```python
# Workflow
'Test preprocessing with complete MT940 document'
mt940_content = ':20:STARTUMSE\n:25:12345678901234567890\n:28C:167619/1\n:60F:C031002EUR0,00\n:61:0310021002DR123,45NMSCNONREF//8327000090031789\n:86:806?20EREF+NONREF?21MREF+M180031?22CRED+DE98ZZZ09999999999\n:62F:C031002EUR-123,45\n-'
expected_content = ':20:STARTUMSE\n:25:12345678901234567890\n:28C:67619/1\n:60F:C031002EUR0,00\n:61:0310021002DR123,45NMSCNONREF//8327000090031789\n:86:806?20EREF+NONREF?21MREF+M180031?22CRED+DE98ZZZ09999999999\n:62F:C031002EUR-123,45\n-'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

## Next Steps


---

*Source: test_bank_statement_import.py:64 | Complexity: Intermediate | Last updated: 2026-02-03*