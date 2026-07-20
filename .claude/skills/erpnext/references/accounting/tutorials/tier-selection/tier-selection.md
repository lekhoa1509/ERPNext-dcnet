# How To: Tier Selection

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: mock, unittest, workflow, integration

## Overview

Workflow: test tier selection

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `unittest`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.loyalty_program.loyalty_program`
- `erpnext.accounts.party`

**Setup Required:**
```python
# Fixtures: mock_get_loyalty_details
```

## Step-by-Step Guide

### Step 1: Assign loyalty_program = frappe.get_doc(...)

```python
loyalty_program = frappe.get_doc({'doctype': 'Loyalty Program', 'loyalty_program_name': 'Test Tier Selection', 'auto_opt_in': 1, 'from_date': today(), 'loyalty_program_type': 'Multiple Tier Program', 'conversion_factor': 1, 'expiry_duration': 10, 'company': '_Test Company', 'cost_center': 'Main - _TC', 'expense_account': 'Loyalty - _TC', 'collection_rules': [{'tier_name': 'Gold', 'collection_factor': 1000, 'min_spent': 20000}, {'tier_name': 'Silver', 'collection_factor': 1000, 'min_spent': 10000}, {'tier_name': 'Bronze', 'collection_factor': 1000, 'min_spent': 0}]})
```

### Step 2: Call loyalty_program.insert()

```python
loyalty_program.insert()
```

### Step 3: Assign test_cases = value

```python
test_cases = [(0, 6000, 'Bronze'), (0, 15000, 'Silver'), (0, 25000, 'Gold'), (4000, 500, 'Bronze'), (8000, 3000, 'Silver'), (18000, 3000, 'Gold'), (22000, 5000, 'Gold')]
```

### Step 4: Call loyalty_program.delete()

```python
loyalty_program.delete()
```

### Step 5: Assign mock_get_loyalty_details.side_effect = side_effect

```python
mock_get_loyalty_details.side_effect = side_effect
```

### Step 6: Assign lp_details = get_loyalty_program_details_with_points(...)

```python
lp_details = get_loyalty_program_details_with_points('Test Loyalty Customer', loyalty_program=loyalty_program.name, company='_Test Company', current_transaction_amount=current_transaction_amount)
```

### Step 7: Assign selected_tier = value

```python
selected_tier = lp_details.tier_name
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(selected_tier, expected_tier, f'Expected tier {expected_tier} for total_spent {total_spent} and current_transaction_amount {current_transaction_amount}, but got {selected_tier}')
```

### Step 9: Assign result = get_loyalty_details(...)

```python
result = get_loyalty_details(*args, **kwargs)
```

### Step 10: Call result.update()

```python
result.update({'total_spent': total_spent})
```


## Complete Example

```python
# Setup
# Fixtures: mock_get_loyalty_details

# Workflow
loyalty_program = frappe.get_doc({'doctype': 'Loyalty Program', 'loyalty_program_name': 'Test Tier Selection', 'auto_opt_in': 1, 'from_date': today(), 'loyalty_program_type': 'Multiple Tier Program', 'conversion_factor': 1, 'expiry_duration': 10, 'company': '_Test Company', 'cost_center': 'Main - _TC', 'expense_account': 'Loyalty - _TC', 'collection_rules': [{'tier_name': 'Gold', 'collection_factor': 1000, 'min_spent': 20000}, {'tier_name': 'Silver', 'collection_factor': 1000, 'min_spent': 10000}, {'tier_name': 'Bronze', 'collection_factor': 1000, 'min_spent': 0}]})
loyalty_program.insert()
test_cases = [(0, 6000, 'Bronze'), (0, 15000, 'Silver'), (0, 25000, 'Gold'), (4000, 500, 'Bronze'), (8000, 3000, 'Silver'), (18000, 3000, 'Gold'), (22000, 5000, 'Gold')]
for total_spent, current_transaction_amount, expected_tier in test_cases:
    with self.subTest(total_spent=total_spent, current_transaction_amount=current_transaction_amount):

        def side_effect(*args, **kwargs):
            result = get_loyalty_details(*args, **kwargs)
            result.update({'total_spent': total_spent})
            return result
        mock_get_loyalty_details.side_effect = side_effect
        lp_details = get_loyalty_program_details_with_points('Test Loyalty Customer', loyalty_program=loyalty_program.name, company='_Test Company', current_transaction_amount=current_transaction_amount)
        selected_tier = lp_details.tier_name
        self.assertEqual(selected_tier, expected_tier, f'Expected tier {expected_tier} for total_spent {total_spent} and current_transaction_amount {current_transaction_amount}, but got {selected_tier}')
loyalty_program.delete()
```

## Next Steps


---

*Source: test_loyalty_program.py:205 | Complexity: Advanced | Last updated: 2026-02-03*