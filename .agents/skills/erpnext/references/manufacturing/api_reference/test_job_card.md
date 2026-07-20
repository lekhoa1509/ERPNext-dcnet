# API Reference: test_job_card.py

**Language**: Python

**Source**: `doctype/job_card/test_job_card.py`

---

## Classes

### TestJobCard

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


##### make_bom_for_jc_tests(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### work_order(self) → WorkOrder

Work Order lazily created for tests.

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `WorkOrder`


##### generate_required_stock(self, work_order: WorkOrder) → None

Create twice the stock for all required items in work order.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| work_order | WorkOrder | - | - |

**Returns**: `None`


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_operations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_with_different_work_station(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_overlap(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_overlap_with_capacity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_multiple_materials_transfer(self)

Test transferring RMs separately against Job Card with multiple RMs.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_excess_material_transfer(self)

Test transferring more than required RM against Job Card.

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'job_card_excess_transfer': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_excess_material_transfer_block(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'job_card_excess_transfer': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_excess_material_transfer_with_no_reference(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'job_card_excess_transfer': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_partial_material_transfer(self)

Test partial material transfer against Job Card

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_material_transfer_correctness(self)

1. Test if only current Job Card Items are pulled in a Stock Entry against a Job Card
2. Test impact of changing 'For Qty' in such a Stock Entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_corrective_costing(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'add_corrective_operation_cost_in_finished_good_valuation': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_if_corrective_jc_ops_cost_is_added_to_manufacture_stock_entry(self)

**Decorators**: `@IntegrationTestCase.change_settings('Manufacturing Settings', {'add_corrective_operation_cost_in_finished_good_valuation': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_statuses(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_material_request_and_bom_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_card_proccess_qty_and_completed_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_op_cost_calculation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_bom_with_multiple_operations()

Create a BOM with multiple operations and Material Transfer against Job Card

**Returns**: (none)



### make_wo_with_transfer_against_jc()

Create a WO with multiple operations and Material Transfer against Job Card

**Returns**: (none)



### assertStatus(status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| status | None | - | - |

**Returns**: (none)


