# API Reference: jinja.py

**Language**: Python

**Source**: `utils/jinja.py`

---

## Classes

### FrappeSandboxedEnvironment

**Inherits from**: SandboxedEnvironment

#### Methods

##### is_safe_attribute(self, obj, attr)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| obj | None | - | - |
| attr | None | - | - |




## Functions

### get_jenv()

**Returns**: (none)



### _get_jenv()

**Returns**: (none)



### get_template(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### get_email_from_template(name, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| args | None | - | - |

**Returns**: (none)



### validate_template(html)

Throws exception if there is a syntax error in the Jinja Template

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |

**Returns**: (none)



### render_template(template, context = None, is_path = None, safe_render = True)

Render a template using Jinja

:param template: path or HTML containing the jinja template
:param context: dict of properties to pass to the template
:param is_path: (optional) assert that the `template` parameter is a path
:param safe_render: (optional) prevent server side scripting via jinja templating

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| template | None | - | - |
| context | None | None | - |
| is_path | None | None | - |
| safe_render | None | True | - |

**Returns**: (none)



### guess_is_path(template)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| template | None | - | - |

**Returns**: (none)



### get_jloader()

**Returns**: (none)



### _get_jloader()

**Returns**: (none)



### set_filters(jenv)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| jenv | None | - | - |

**Returns**: (none)



### get_jinja_hooks()

Return a tuple of (methods, filters) each containing a dict of method name and method definition pair.

**Returns**: (none)



### get_obj_dict_from_paths(object_paths)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| object_paths | None | - | - |

**Returns**: (none)


