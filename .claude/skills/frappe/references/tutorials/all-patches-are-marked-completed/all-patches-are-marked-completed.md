# How To: All Patches Are Marked Completed

**Difficulty**: Intermediate
**Estimated Time**: 5 minutes
**Tags**: mock, workflow, integration

## Overview

Workflow: test all patches are marked completed

## Prerequisites

**Required Modules:**
- `pathlib`
- `unittest.mock`
- `frappe`
- `frappe.modules`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign all_patches = patch_handler.get_patches_from_app(...)

```python
all_patches = patch_handler.get_patches_from_app('frappe')
```

### Step 2: Assign finished_patches = frappe.db.count(...)

```python
finished_patches = frappe.db.count('Patch Log')
```

### Step 3: Call self.assertGreaterEqual()

```python
self.assertGreaterEqual(finished_patches, len(all_patches))
```


## Complete Example

```python
# Workflow
all_patches = patch_handler.get_patches_from_app('frappe')
finished_patches = frappe.db.count('Patch Log')
self.assertGreaterEqual(finished_patches, len(all_patches))
```

## Next Steps


---

*Source: test_patches.py:74 | Complexity: Intermediate | Last updated: 2026-02-04*