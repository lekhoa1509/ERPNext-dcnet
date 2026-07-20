# API Reference: subscription_plan.py

**Language**: Python

**Source**: `doctype/subscription_plan/subscription_plan.py`

---

## Classes

### SubscriptionPlan

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_interval_count(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_plan_rate(plan, quantity = 1, customer = None, start_date = None, end_date = None, prorate_factor = 1, party = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| plan | None | - | - |
| quantity | None | 1 | - |
| customer | None | None | - |
| start_date | None | None | - |
| end_date | None | None | - |
| prorate_factor | None | 1 | - |
| party | None | None | - |

**Returns**: (none)



### get_prorate_factor(start_date, end_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start_date | None | - | - |
| end_date | None | - | - |

**Returns**: (none)


