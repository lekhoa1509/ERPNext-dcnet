# API Reference: safe_exec.py

**Language**: Python

**Source**: `utils/safe_exec.py`

---

## Classes

### ServerScriptNotEnabled

**Inherits from**: frappe.PermissionError



### NamespaceDict

Raise AttributeError if function not found in namespace

**Inherits from**: frappe._dict

#### Methods

##### __getattr__(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |




### FrappeTransformer

**Inherits from**: RestrictingNodeTransformer

#### Methods

##### check_name(self, node, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| node | None | - | - |
| name | None | - | - |




### FrappePrintCollector

Collect written text, and return it when called.

**Inherits from**: PrintCollector

#### Methods

##### _call_print(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### is_safe_exec_enabled() → bool

**Returns**: `bool`



### safe_exec(script: str, _globals: dict | None = None, _locals: dict | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| script | str | - | - |
| _globals | dict | None | None | - |
| _locals | dict | None | None | - |

**Returns**: (none)



### _compile_code(script: str, filename: str, mode: str = 'exec')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| script | str | - | - |
| filename | str | - | - |
| mode | str | 'exec' | - |

**Returns**: (none)



### safe_eval(code, eval_globals = None, eval_locals = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | None | - | - |
| eval_globals | None | None | - |
| eval_locals | None | None | - |

**Returns**: (none)



### _validate_safe_eval_syntax(code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | None | - | - |

**Returns**: (none)



### safe_exec_flags()

**Returns**: (none)



### get_safe_globals()

**Returns**: (none)



### get_keys_for_autocomplete(key: str, value: Any, prefix: str = '', offset: int = 0, meta: str = 'ctx', depth: int = 0, max_depth: int | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |
| value | Any | - | - |
| prefix | str | '' | - |
| offset | int | 0 | - |
| meta | str | 'ctx' | - |
| depth | int | 0 | - |
| max_depth | int | None | None | - |

**Returns**: (none)



### is_job_queued(job_name, queue = 'default')

:param job_name: used to identify a queued job, usually dotted path to function
:param queue: should be either long, default or short

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_name | None | - | - |
| queue | None | 'default' | - |

**Returns**: (none)



### safe_enqueue(function)

Enqueue function to be executed using a background worker
Accepts frappe.enqueue params like job_name, queue, timeout, etc.
in addition to params to be passed to function

:param function: whitelisted function or API Method set in Server Script

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| function | None | - | - |

**Returns**: (none)



### call_whitelisted_function(function)

Executes a whitelisted function or Server Script of type API

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| function | None | - | - |

**Returns**: (none)



### run_script(script)

run another server script

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| script | None | - | - |

**Returns**: (none)



### call_with_form_dict(function, kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| function | None | - | - |
| kwargs | None | - | - |

**Returns**: (none)



### patched_qb()

**Returns**: (none)



### _flatten(module)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |

**Returns**: (none)



### get_python_builtins()

**Returns**: (none)



### get_hooks(hook: str | None = None, default = None, app_name: str | None = None) → frappe._dict

Get hooks via `app/hooks.py`

:param hook: Name of the hook. Will gather all hooks for this name and return as a list.
:param default: Default if no hook found.
:param app_name: Filter by app.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| hook | str | None | None | - |
| default | None | None | - |
| app_name | str | None | None | - |

**Returns**: `frappe._dict`



### read_sql(query)

a wrapper for frappe.db.sql to allow reads

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | None | - | - |

**Returns**: (none)



### check_safe_sql_query(query: str, throw: bool = True) → bool

Check if SQL query is safe for running in restricted context.

Safe queries:
        1. Read only 'select' or 'explain' queries
        2. CTE on mariadb where writes are not allowed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | str | - | - |
| throw | bool | True | - |

**Returns**: `bool`



### _getitem(obj, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| key | None | - | - |

**Returns**: (none)



### _getattr_for_safe_exec(object, name, default = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| object | None | - | - |
| name | None | - | - |
| default | None | None | - |

**Returns**: (none)



### _get_attr_for_eval(object, name, default = ARGUMENT_NOT_SET)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| object | None | - | - |
| name | None | - | - |
| default | None | ARGUMENT_NOT_SET | - |

**Returns**: (none)



### _validate_attribute_read(object, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| object | None | - | - |
| name | None | - | - |

**Returns**: (none)



### _write(obj)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |

**Returns**: (none)



### get_module_properties(module, filter_method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| module | None | - | - |
| filter_method | None | - | - |

**Returns**: (none)



### default_function()

**Returns**: (none)


