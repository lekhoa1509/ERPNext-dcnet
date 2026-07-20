# API Reference: jinja_globals.py

**Language**: Python

**Source**: `utils/jinja_globals.py`

---

## Functions

### resolve_class()

**Returns**: (none)



### inspect(var, render = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| var | None | - | - |
| render | None | True | - |

**Returns**: (none)



### web_block(template, values = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| template | None | - | - |
| values | None | None | - |

**Returns**: (none)



### web_blocks(blocks)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| blocks | None | - | - |

**Returns**: (none)



### get_dom_id(seed = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| seed | None | None | - |

**Returns**: (none)



### include_script(path, preload = True)

Get path of bundled script files.

If preload is specified the path will be added to preload headers so browsers can prefetch
assets.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| preload | None | True | - |

**Returns**: (none)



### include_icons(path, preload = True)

Get path of bundled svg icons files.

If preload is specified the path will be added to preload headers so browsers can prefetch
assets.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| preload | None | True | - |

**Returns**: (none)



### include_style(path, rtl = None, preload = True)

Get path of bundled style files.

If preload is specified the path will be added to preload headers so browsers can prefetch
assets.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| rtl | None | None | - |
| preload | None | True | - |

**Returns**: (none)



### bundled_asset(path, rtl = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| rtl | None | None | - |

**Returns**: (none)



### is_rtl(rtl = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rtl | None | None | - |

**Returns**: (none)


