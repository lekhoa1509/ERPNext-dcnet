# API Reference: synchronization.py

**Language**: Python

**Source**: `utils/synchronization.py`

---

## Functions

### filelock(lock_name: str)

Create a lockfile to prevent concurrent operations acrosss processes.

args:
        lock_name: Unique name to identify a specific lock. Lockfile called `{name}.lock` will be
        created.
        timeout: time to wait before failing.
        is_global: if set lock is global to bench

Lock file location:
        global - {bench_dir}/config/{name}.lock
        site - {bench_dir}/sites/sitename/{name}.lock

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lock_name | str | - | - |

**Returns**: (none)


