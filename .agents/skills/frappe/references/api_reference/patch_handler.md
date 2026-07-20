# API Reference: patch_handler.py

**Language**: Python

**Source**: `modules/patch_handler.py`

---

## Classes

### PatchError

**Inherits from**: Exception



### PatchType

**Inherits from**: Enum



## Functions

### run_all(skip_failing: bool = False, patch_type: PatchType | None = None) → None

run all pending patches

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| skip_failing | bool | False | - |
| patch_type | PatchType | None | None | - |

**Returns**: `None`



### get_all_patches(patch_type: PatchType | None = None) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| patch_type | PatchType | None | None | - |

**Returns**: `list[str]`



### get_patches_from_app(app: str, patch_type: PatchType | None = None) → list[str]

Get patches from an app's patches.txt

patches.txt can be:
        1. ini like file with section for different patch_type
        2. plain text file with each line representing a patch.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |
| patch_type | PatchType | None | None | - |

**Returns**: `list[str]`



### parse_as_configfile(patches_file: str, patch_type: PatchType | None = None) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| patches_file | str | - | - |
| patch_type | PatchType | None | None | - |

**Returns**: `list[str]`



### reload_doc(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### run_single(patchmodule = None, method = None, methodargs = None, force = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| patchmodule | None | None | - |
| method | None | None | - |
| methodargs | None | None | - |
| force | None | False | - |

**Returns**: (none)



### execute_patch(patchmodule: str, method = None, methodargs = None)

execute the patch

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| patchmodule | str | - | - |
| method | None | None | - |
| methodargs | None | None | - |

**Returns**: (none)



### update_patch_log(patchmodule, skipped = False)

update patch_file in patch log

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| patchmodule | None | - | - |
| skipped | None | False | - |

**Returns**: (none)



### executed(patchmodule)

return True if is executed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| patchmodule | None | - | - |

**Returns**: (none)



### _patch_mode(enable)

stop/start execution till patch is run

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| enable | None | - | - |

**Returns**: (none)



### run_patch(patch)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| patch | None | - | - |

**Returns**: (none)


