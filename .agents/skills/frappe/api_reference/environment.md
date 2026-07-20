# API Reference: environment.py

**Language**: Python

**Source**: `testing/environment.py`

---

## Classes

### IntegrationTestPreparation

**Inherits from**: (none)

#### Methods

##### __init__(self, cfg)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cfg | None | - | - |


##### __call__(self, suite: unittest.TestSuite, app: str, category: str) → None

Prepare the environment for integration tests.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| suite | unittest.TestSuite | - | - |
| app | str | - | - |
| category | str | - | - |

**Returns**: `None`


##### _run_before_test_hooks(app: str, category: str)

Run 'before_tests' hooks

**Decorators**: `@staticmethod`, `@debug_timer`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |
| category | str | - | - |


##### _create_global_test_record_dependencies(app: str, category: str)

Create global test record dependencies

**Decorators**: `@staticmethod`, `@debug_timer`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |
| category | str | - | - |




## Functions

### _initialize_test_environment(site, config)

Initialize the test environment

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |
| config | None | - | - |

**Returns**: (none)



### _cleanup_after_tests()

Perform cleanup operations after running tests

**Returns**: (none)



### _disable_scheduler_if_needed()

Disable scheduler if it's not already disabled

**Returns**: (none)



### _decorate_all_methods_and_functions_with_type_checker()

**Returns**: (none)



### _get_config_from_pyproject(app_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_path | None | - | - |

**Returns**: (none)



### _decorate_callable(obj, parent_module)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| parent_module | None | - | - |

**Returns**: (none)



### _decorate_module(app, module, apps, current_depth, max_depth)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| module | None | - | - |
| apps | None | - | - |
| current_depth | None | - | - |
| max_depth | None | - | - |

**Returns**: (none)



### wrapper()

**Returns**: (none)


