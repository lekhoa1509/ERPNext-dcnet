# API Reference: attribution.py

**Language**: Python

**Source**: `www/attribution.py`

---

## Functions

### get_context(context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | - | - |

**Returns**: (none)



### get_app_info(app: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |

**Returns**: (none)



### get_python_package_metadata(package_name: str) → dict

Get metadata for a Python package using importlib.metadata

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| package_name | str | - | - |

**Returns**: `dict`



### parse_classifiers(classifiers: list[str]) → str | None

Parse classifiers to get the license

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| classifiers | list[str] | - | - |

**Returns**: `str | None`



### get_js_deps(app: str) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |

**Returns**: `list[dict]`



### get_pyproject_info(app: str) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |

**Returns**: `dict`



### parse_pip_requirement(requirement: str) → str

Parse pip requirement string to package name and version

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| requirement | str | - | - |

**Returns**: `str`


