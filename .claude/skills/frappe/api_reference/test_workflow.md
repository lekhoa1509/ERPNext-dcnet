# API Reference: test_workflow.py

**Language**: Python

**Source**: `workflow/doctype/workflow/test_workflow.py`

---

## Classes

### TestWorkflow

**Inherits from**: IntegrationTestCase

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


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_default_condition(self)

test default condition is set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_approve(self, doc = None)

test simple workflow

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | None | - |


##### test_wrong_action(self)

Check illegal action (approve after reject)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_workflow_condition(self)

Test condition in transition

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_common_transition_actions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_if_workflow_actions_were_processed_using_role(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_if_workflow_set_on_action(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_syntax_error_in_transition_rule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dynamic_update_value_expression(self)

Test dynamic expression evaluation in workflow update_value field

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dynamic_update_value_with_doc_field(self)

Test dynamic expression using doc field value

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_static_value_when_expression_disabled(self)

Test that value is not evaluated when evaluate_as_expression is disabled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invalid_expression_raises_error(self)

Test that invalid expression raises proper error

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sync_tasks(self, doc = None)

test workflow with workflow tasks (server scripts, webhooks and app-defined methods)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | None | - |




## Functions

### create_todo_workflow()

**Returns**: (none)



### create_domain_workflow()

**Returns**: (none)



### create_new_todo()

**Returns**: (none)



### create_new_note(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### create_new_server_script()

**Returns**: (none)



### create_new_webhook()

**Returns**: (none)


