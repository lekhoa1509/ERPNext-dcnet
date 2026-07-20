# API Reference: _optimizations.py

**Language**: Python

**Source**: `_optimizations.py`

---

## Functions

### optimize_all()

Single entry point to enable all optimizations at right time automatically.

**Returns**: (none)



### optimize_gc_parameters()

**Returns**: (none)



### optimize_regex_cache()

**Returns**: (none)



### register_fault_handler()

**Returns**: (none)



### optimize_gc_for_copy_on_write()

**Returns**: (none)



### freeze_gc()

**Returns**: (none)



### optimize_for_gil_contention()

**Returns**: (none)



### increment_worker_count()

**Returns**: (none)



### assign_core(pid: int, physical_cpu_count: int, logical_cpu_count: int, current_affinity: list[int], thread_siblings: list[tuple[int, ...]]) → int | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pid | int | - | - |
| physical_cpu_count | int | - | - |
| logical_cpu_count | int | - | - |
| current_affinity | list[int] | - | - |
| thread_siblings | list[tuple[int, ...]] | - | - |

**Returns**: `int | None`



### pin_web_worker_to_one_core()

Try to assign current process to one core.

**Returns**: (none)



### parse_thread_siblings() → list[tuple[int, int]] | None

**Returns**: `list[tuple[int, int]] | None`


