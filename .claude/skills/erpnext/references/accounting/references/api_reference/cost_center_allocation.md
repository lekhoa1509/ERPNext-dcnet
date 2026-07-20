# API Reference: cost_center_allocation.py

**Language**: Python

**Source**: `doctype/cost_center_allocation/cost_center_allocation.py`

---

## Classes

### MainCostCenterCantBeChild

**Inherits from**: frappe.ValidationError



### InvalidMainCostCenter

**Inherits from**: frappe.ValidationError



### InvalidChildCostCenter

**Inherits from**: frappe.ValidationError



### WrongPercentageAllocation

**Inherits from**: frappe.ValidationError



### InvalidDateError

**Inherits from**: frappe.ValidationError



### CostCenterAllocation

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_total_allocation_percentage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_from_date_based_on_existing_gle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_backdated_allocation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_main_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_child_cost_centers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



