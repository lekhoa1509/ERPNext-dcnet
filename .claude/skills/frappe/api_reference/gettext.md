# API Reference: gettext.py

**Language**: Python

**Source**: `commands/gettext.py`

---

## Functions

### generate_pot_file(context: CliCtxObj, app: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| app | str | None | None | - |

**Returns**: (none)



### compile_translations(context: CliCtxObj, app: str | None = None, locale: str | None = None, force = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| app | str | None | None | - |
| locale | str | None | None | - |
| force | None | False | - |

**Returns**: (none)



### csv_to_po(context: CliCtxObj, app: str | None = None, locale: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| app | str | None | None | - |
| locale | str | None | None | - |

**Returns**: (none)



### update_po_files(context: CliCtxObj, app: str | None = None, locale: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| app | str | None | None | - |
| locale | str | None | None | - |

**Returns**: (none)



### create_po_file(context: CliCtxObj, locale: str, app: str | None = None)

Create PO file for lang code

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| locale | str | - | - |
| app | str | None | None | - |

**Returns**: (none)



### connect_to_site(site)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | - | - |

**Returns**: (none)


