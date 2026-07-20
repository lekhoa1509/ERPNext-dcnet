# API Reference: lazy_loader.py

**Language**: Python

**Source**: `utils/lazy_loader.py`

---

## Functions

### lazy_import(name, package = None)

Import a module lazily.

The module is loaded when modules's attribute is accessed for the first time.
This works with both absolute and relative imports.
$ cat mod.py
print("Loading mod.py")
$ python -i lazy_loader.py
>>> mod = lazy_import("mod")  # Module is not loaded
>>> mod.__str__()  # module is loaded on accessing attribute
Loading mod.py
"<module 'mod' from '.../frappe/utils/mod.py'>"
>>>

Code based on https://github.com/python/cpython/blob/master/Doc/library/importlib.rst#implementing-lazy-imports.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| package | None | None | - |

**Returns**: (none)


