# API Reference: setup_db.py

**Language**: Python

**Source**: `database/sqlite/setup_db.py`

---

## Functions

### get_sqlite_version() → str

**Returns**: `str`



### setup_database(force, verbose)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| force | None | - | - |
| verbose | None | - | - |

**Returns**: (none)



### bootstrap_database(verbose, source_db = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| verbose | None | - | - |
| source_db | None | None | - |

**Returns**: (none)



### copy_db(db_file = None, verbose = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| db_file | None | None | - |
| verbose | None | False | - |

**Returns**: (none)



### drop_database(db_name: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| db_name | str | - | - |

**Returns**: (none)



### get_root_connection()

**Returns**: (none)


