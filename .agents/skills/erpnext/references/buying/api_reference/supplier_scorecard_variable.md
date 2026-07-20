# API Reference: supplier_scorecard_variable.py

**Language**: Python

**Source**: `doctype/supplier_scorecard_variable/supplier_scorecard_variable.py`

---

## Classes

### VariablePathNotFound

**Inherits from**: frappe.ValidationError



### SupplierScorecardVariable

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_path_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_total_workdays(scorecard)

Gets the number of days in this period

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_item_workdays(scorecard)

Gets the number of days in this period

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_cost_of_shipments(scorecard)

Gets the total cost of all shipments in the period (based on Purchase Orders)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_cost_of_delayed_shipments(scorecard)

Gets the total cost of all delayed shipments in the period (based on Purchase Receipts - POs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_cost_of_on_time_shipments(scorecard)

Gets the total cost of all on_time shipments in the period (based on Purchase Receipts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_days_late(scorecard)

Gets the number of item days late in the period (based on Purchase Receipts vs POs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_on_time_shipments(scorecard)

Gets the number of late shipments (counting each item) in the period (based on Purchase Receipts vs POs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_late_shipments(scorecard)

Gets the number of late shipments (counting each item) in the period (based on Purchase Receipts vs POs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_received(scorecard)

Gets the total number of received shipments in the period (based on Purchase Receipts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_received_amount(scorecard)

Gets the total amount (in company currency) received in the period (based on Purchase Receipts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_received_items(scorecard)

Gets the total number of received shipments in the period (based on Purchase Receipts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_rejected_amount(scorecard)

Gets the total amount (in company currency) rejected in the period (based on Purchase Receipts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_rejected_items(scorecard)

Gets the total number of rejected items in the period (based on Purchase Receipts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_accepted_amount(scorecard)

Gets the total amount (in company currency) accepted in the period (based on Purchase Receipts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_accepted_items(scorecard)

Gets the total number of rejected items in the period (based on Purchase Receipts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_total_shipments(scorecard)

Gets the total number of ordered shipments to arrive in the period (based on Purchase Receipts)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_ordered_qty(scorecard)

Returns the total number of ordered quantity (based on Purchase Orders)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_invoiced_qty(scorecard)

Returns the total number of invoiced quantity (based on Purchase Invoice)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_rfq_total_number(scorecard)

Gets the total number of RFQs sent to supplier

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_rfq_total_items(scorecard)

Gets the total number of RFQ items sent to supplier

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_sq_total_number(scorecard)

Gets the total number of RFQ items sent to supplier

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_sq_total_items(scorecard)

Gets the total number of RFQ items sent to supplier

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)



### get_rfq_response_days(scorecard)

Gets the total number of days it has taken a supplier to respond to rfqs in the period

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scorecard | None | - | - |

**Returns**: (none)


