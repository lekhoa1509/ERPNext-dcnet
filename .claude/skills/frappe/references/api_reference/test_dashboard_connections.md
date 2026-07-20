# API Reference: test_dashboard_connections.py

**Language**: Python

**Source**: `tests/test_dashboard_connections.py`

---

## Classes

### TestDashboardConnections

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Decorators**: `@patch.dict(frappe.conf, {'developer_mode': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Decorators**: `@patch.dict(frappe.conf, {'developer_mode': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_internal_link_count(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_external_link_count(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_external_doctype_link_with_dashboard_override(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_test_data()

**Returns**: (none)



### delete_test_data()

**Returns**: (none)



### create_test_child_table_with_link_to_doctype_a()

**Returns**: (none)



### create_test_child_table_with_link_to_doctype_b()

**Returns**: (none)



### add_links_in_child_tables()

**Returns**: (none)



### create_test_doctype_a_with_test_child_table_with_link_to_doctype_b()

**Returns**: (none)



### create_test_doctype_b_with_test_child_table_with_link_to_doctype_a()

**Returns**: (none)



### get_dashboard_for_test_doctype_a_with_test_child_table_with_link_to_doctype_b()

**Returns**: (none)



### create_linked_doctypes()

Test Doctype D and Test Doctype E linked to "ToDo"

**Returns**: (none)



### get_dashboard_for_todo(data: dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | dict | - | - |

**Returns**: (none)


