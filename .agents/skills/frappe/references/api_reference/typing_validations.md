# API Reference: typing_validations.py

**Language**: Python

**Source**: `utils/typing_validations.py`

---

## Functions

### validate_argument_types(func: Callable, apply_condition: Callable | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | Callable | - | - |
| apply_condition | Callable | None | None | - |

**Returns**: (none)



### qualified_name(obj) → str

Return the qualified name (e.g. package.module.Type) for the given object.

Builtins and types from the :mod:typing package get special treatment by having the module
name stripped from the generated name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |

**Returns**: `str`



### raise_type_error(func: callable, arg_name: str, arg_type: type, arg_value: object, current_exception: Exception | None = None)

Raise a TypeError with a message that includes the name of the argument, the expected type
and the actual type of the value passed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | callable | - | - |
| arg_name | str | - | - |
| arg_type | type | - | - |
| arg_value | object | - | - |
| current_exception | Exception | None | None | - |

**Returns**: (none)



### TypeAdapter(type_)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| type_ | None | - | - |

**Returns**: (none)



### transform_parameter_types(func: Callable, args: tuple, kwargs: dict)

Validate the types of the arguments passed to a function with the type annotations
defined on the function.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | Callable | - | - |
| args | tuple | - | - |
| kwargs | dict | - | - |

**Returns**: (none)



### wrapper()

Validate argument types of whitelisted functions.

:param args: Function arguments.
:param kwargs: Function keyword arguments.

**Returns**: (none)


