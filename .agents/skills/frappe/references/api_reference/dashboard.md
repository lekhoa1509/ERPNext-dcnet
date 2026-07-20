# API Reference: dashboard.py

**Language**: Python

**Source**: `utils/dashboard.py`

---

## Functions

### cache_source(function)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| function | None | - | - |

**Returns**: (none)



### generate_and_cache_results(args, function, cache_key, chart)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| function | None | - | - |
| cache_key | None | - | - |
| chart | None | - | - |

**Returns**: (none)



### get_dashboards_with_link(docname, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### sync_dashboards(app = None)

Import, overwrite dashboards from `[app]/[app]_dashboard`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | None | - |

**Returns**: (none)



### make_records_in_module(app, module)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| module | None | - | - |

**Returns**: (none)



### make_records(path, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### wrapper()

**Returns**: (none)


