# API Reference: test_bom_update_log.py

**Language**: Python

**Source**: `doctype/bom_update_log/test_bom_update_log.py`

---

## Classes

### TestBOMUpdateLog

Test BOM Update Tool Operations via BOM Update Log.

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_update_log_validate(self)

1) Test if BOM presence is validated.
2) Test if same BOMs are validated.
3) Test of non-existent BOM is validated.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_update_log_completion(self)

Test if BOM Update Log handles job completion correctly.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_replace_for_root_bom(self)

- B-Item A (Root Item)
        - B-Item B
                - B-Item C
        - B-Item D
                - B-Item E
                        - B-Item F

Create New BOM for B-Item E with B-Item G and replace it in the above BOM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### remove_bom(item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |

**Returns**: (none)



### update_cost_in_all_boms_in_test()

Utility to run 'Update Cost' job in tests without Cron job until fully complete.

**Returns**: (none)


