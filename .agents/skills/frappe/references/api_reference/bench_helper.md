# API Reference: bench_helper.py

**Language**: Python

**Source**: `utils/bench_helper.py`

---

## Classes

### CliCtxObj

**Inherits from**: (none)



### Cls

**Inherits from**: cls

#### Methods

##### get_command(self, ctx, cmd_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ctx | None | - | - |
| cmd_name | None | - | - |


##### make_context(self, info_name, args, parent = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| info_name | None | - | - |
| args | None | - | - |
| parent | None | None | - |


##### invoke(self, ctx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ctx | None | - | - |




## Functions

### FrappeClickWrapper(cls, handler)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| handler | None | - | - |

**Returns**: (none)



### handle_exception(cmd, info_name, exc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cmd | None | - | - |
| info_name | None | - | - |
| exc | None | - | - |

**Returns**: (none)



### main()

**Returns**: (none)



### get_app_groups() → dict[str, click.Group | click.Command]

Get all app groups, put them in main group "frappe" since bench is
designed to only handle that

**Returns**: `dict[str, click.Group | click.Command]`



### get_app_group(app: str) → click.Group

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |

**Returns**: `click.Group`



### app_group(ctx, site = False, force = False, verbose = False, profile = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |
| site | None | False | - |
| force | None | False | - |
| verbose | None | False | - |
| profile | None | False | - |

**Returns**: (none)



### get_sites(site_arg: str) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site_arg | str | - | - |

**Returns**: `list[str]`



### get_app_commands(app: str) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |

**Returns**: `dict`



### get_frappe_commands()

**Returns**: (none)



### get_frappe_help()

**Returns**: (none)



### get_apps()

**Returns**: (none)


