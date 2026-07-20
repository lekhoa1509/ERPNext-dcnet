# API Reference: backups.py

**Language**: Python

**Source**: `page/backups/backups.py`

---

## Functions

### get_time(path: Path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | Path | - | - |

**Returns**: (none)



### get_encrytion_status(path: Path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | Path | - | - |

**Returns**: (none)



### get_size(path: Path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | Path | - | - |

**Returns**: (none)



### get_context(context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | - | - |

**Returns**: (none)



### cleanup_old_backups(backups: dict[str, list[Path]], limit: int)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| backups | dict[str, list[Path]] | - | - |
| limit | int | - | - |

**Returns**: (none)



### delete_downloadable_backups()

**Returns**: (none)



### schedule_files_backup(user_email: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_email | str | - | - |

**Returns**: (none)



### backup_files_and_notify_user(user_email = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_email | None | None | - |

**Returns**: (none)



### get_downloadable_links(backup_files)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| backup_files | None | - | - |

**Returns**: (none)


