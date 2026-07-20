# API Reference: app.py

**Language**: Python

**Source**: `app.py`

---

## Functions

### after_response_wrapper(app)

Wrap a WSGI application to call after_response hooks after we have responded.

This is done to reduce response time by deferring expensive tasks.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)



### application(request: Request)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| request | Request | - | - |

**Returns**: (none)



### run_after_request_hooks(request, response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| request | None | - | - |
| response | None | - | - |

**Returns**: (none)



### init_request(request)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| request | None | - | - |

**Returns**: (none)



### setup_read_only_mode()

During maintenance_mode reads to DB can still be performed to reduce downtime. This
function sets up read only mode

- Setting global flag so other pages, desk and database can know that we are in read only mode.
- Setup read only database access either by:
    - Connecting to read replica if one exists
    - Or setting up read only SQL transactions.

**Returns**: (none)



### log_request(request, response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| request | None | - | - |
| response | None | - | - |

**Returns**: (none)



### process_response(response: Response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response | Response | - | - |

**Returns**: (none)



### set_cors_headers(response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response | None | - | - |

**Returns**: (none)



### set_authenticate_headers(response: Response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response | Response | - | - |

**Returns**: (none)



### make_form_dict(request: Request)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| request | Request | - | - |

**Returns**: (none)



### handle_exception(e)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | None | - | - |

**Returns**: (none)



### sync_database()

**Returns**: (none)



### serve(port = 8000, profile = False, no_reload = False, no_threading = False, site = None, sites_path = '.', proxy = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| port | None | 8000 | - |
| profile | None | False | - |
| no_reload | None | False | - |
| no_threading | None | False | - |
| site | None | None | - |
| sites_path | None | '.' | - |
| proxy | None | False | - |

**Returns**: (none)



### application_with_statics()

**Returns**: (none)



### application(environ, start_response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| environ | None | - | - |
| start_response | None | - | - |

**Returns**: (none)


