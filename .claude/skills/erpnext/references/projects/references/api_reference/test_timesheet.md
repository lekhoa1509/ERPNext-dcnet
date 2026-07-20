# API Reference: test_timesheet.py

**Language**: Python

**Source**: `doctype/timesheet/test_timesheet.py`

---

## Classes

### TestTimesheet

**Inherits from**: ERPNextTestSuite

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timesheet_post_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timesheet_base_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timesheet_billing_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timesheet_billing_amount_not_billable(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_from_timesheet(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timesheet_billing_based_on_project(self)

**Decorators**: `@IntegrationTestCase.change_settings('Projects Settings', {'fetch_timesheet_in_sales_invoice': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timesheet_time_overlap(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timesheet_not_overlapping_with_continuous_timelogs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_to_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_per_billed_hours(self)

If amounts are 0, per_billed should be calculated based on hours.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_per_billed_amount(self)

If amounts are > 0, per_billed should be calculated based on amounts, regardless of hours.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_partial_billing_and_return(self)

Test Timesheet status transitions during partial billing, full billing,
sales return, and return cancellation.

Scenario:
1. Create a Timesheet with two billable time logs.
2. Create a Sales Invoice billing only one time log → Timesheet becomes Partially Billed.
3. Create another Sales Invoice billing the remaining time log → Timesheet becomes Billed.
4. Create a Sales Return against the second invoice → Timesheet reverts to Partially Billed.
5. Cancel the Sales Return → Timesheet returns to Billed status.

This test ensures Timesheet status is recalculated correctly
across billing and return lifecycle events.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_timesheet(employee, simulate = False, is_billable = 0, activity_type = '_Test Activity Type', project = None, task = None, company = None, currency = None, exchange_rate = None, do_not_submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| employee | None | - | - |
| simulate | None | False | - |
| is_billable | None | 0 | - |
| activity_type | None | '_Test Activity Type' | - |
| project | None | None | - |
| task | None | None | - |
| company | None | None | - |
| currency | None | None | - |
| exchange_rate | None | None | - |
| do_not_submit | None | False | - |

**Returns**: (none)



### update_activity_type(activity_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| activity_type | None | - | - |

**Returns**: (none)


