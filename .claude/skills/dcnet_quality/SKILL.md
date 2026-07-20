---
name: dcnet-quality
description: "ERPNext/Frappe code quality orchestrator with 28 deterministic skills across 5 layers. Auto-triggers on ERPNext code patterns. Use for: code review, PR validation, writing client scripts, server scripts, controllers, hooks.py, whitelisted methods, jinja templates, scheduler jobs, custom apps. Triggers: review code, validate code, check my script, PR review, code quality, client script, server script, controller, hooks.py, frappe.whitelist, jinja, print format, scheduler, custom app, frappe.db, permissions, API endpoint, before_save, on_update, frappe.call, frappe.ui.form.on, frm.set_value."
---

# DCNET Quality - ERPNext Code Quality Orchestrator

> 28 deterministic skills for generating and validating flawless ERPNext/Frappe v16 code.
> Source: [OpenAEC Foundation ERPNext Skills Package v1.2](https://github.com/OpenAEC-Foundation/ERPNext_Anthropic_Claude_Development_Skill_Package)

## Skill Selection Router

Based on the task, load the appropriate SKILL.md from subdirectories:

```
What are you doing?
│
├─► WRITING code
│   │
│   ├─► Client Script (JS) ──────► Read: syntax/erpnext-syntax-clientscripts/SKILL.md
│   │                                     impl/erpnext-impl-clientscripts/SKILL.md
│   │
│   ├─► Server Script (Python) ──► Read: syntax/erpnext-syntax-serverscripts/SKILL.md
│   │                                     impl/erpnext-impl-serverscripts/SKILL.md
│   │
│   ├─► Controller (.py) ────────► Read: syntax/erpnext-syntax-controllers/SKILL.md
│   │                                     impl/erpnext-impl-controllers/SKILL.md
│   │
│   ├─► hooks.py ────────────────► Read: syntax/erpnext-syntax-hooks/SKILL.md
│   │                                     impl/erpnext-impl-hooks/SKILL.md
│   │
│   ├─► @frappe.whitelist() ─────► Read: syntax/erpnext-syntax-whitelisted/SKILL.md
│   │                                     impl/erpnext-impl-whitelisted/SKILL.md
│   │
│   ├─► Jinja / Print Format ───► Read: syntax/erpnext-syntax-jinja/SKILL.md
│   │                                     impl/erpnext-impl-jinja/SKILL.md
│   │
│   ├─► Scheduler / Background ─► Read: syntax/erpnext-syntax-scheduler/SKILL.md
│   │                                     impl/erpnext-impl-scheduler/SKILL.md
│   │
│   └─► Custom App structure ───► Read: syntax/erpnext-syntax-customapp/SKILL.md
│                                        impl/erpnext-impl-customapp/SKILL.md
│
├─► REVIEWING / VALIDATING code
│   └─► Read: agents/erpnext-code-validator/SKILL.md
│        Then apply relevant error skills:
│        - errors/erpnext-errors-clientscripts/SKILL.md
│        - errors/erpnext-errors-serverscripts/SKILL.md
│        - errors/erpnext-errors-controllers/SKILL.md
│        - errors/erpnext-errors-hooks/SKILL.md
│        - errors/erpnext-errors-database/SKILL.md
│        - errors/erpnext-errors-permissions/SKILL.md
│        - errors/erpnext-errors-api/SKILL.md
│
├─► DATABASE operations ────────► Read: core/erpnext-database/SKILL.md
│
├─► PERMISSIONS / Roles ────────► Read: core/erpnext-permissions/SKILL.md
│
├─► API design ─────────────────► Read: core/erpnext-api-patterns/SKILL.md
│
└─► Vague requirement ──────────► Read: agents/erpnext-code-interpreter/SKILL.md
```

## How This Skill Works

### Auto-trigger (when writing code)

When Claude detects ERPNext/Frappe code patterns in the task, it MUST:

1. **Identify code type** from trigger keywords
2. **Read the matching SKILL.md** files (syntax + impl for the domain)
3. **Also read core skills** if database/permissions/API are involved
4. **Apply patterns deterministically** - follow ALWAYS/NEVER rules exactly

### PR Review / Code Validation

When reviewing code (PR review, code check, validate):

1. **Read `agents/erpnext-code-validator/SKILL.md`** for validation workflow
2. **Identify all code types** in the PR/changeset
3. **Read relevant error skills** for each code type
4. **Generate validation report** with CRITICAL/WARNING/SUGGESTION levels

### Quick Reference: Critical Rules

These are the #1 causes of ERPNext code failures:

| Rule | Severity | Details |
|------|----------|---------|
| **NO imports in Server Scripts** | FATAL | `from frappe.utils import X` FAILS. Use `frappe.utils.X()` |
| **NO `self.` in Server Scripts** | FATAL | Use `doc.field`, not `self.field` |
| **NO `frappe.db.*` in Client Scripts** | FATAL | Server-side only. Use `frappe.call()` |
| **NO field modify in `on_update`** | FATAL | Changes won't save. Use `frappe.db.set_value()` |
| **ALWAYS `super().validate()`** | ERROR | Missing breaks parent validation chain |
| **ALWAYS callback in `frappe.call()`** | ERROR | Without callback = undefined result |
| **ALWAYS `frm.refresh_field()` after set_value** | ERROR | UI won't update |

## Layer Architecture

```
Layer 5: AGENTS        → Orchestrate (code-interpreter, code-validator)
Layer 4: ERRORS (7)    → How to handle failures
Layer 3: IMPL (8)      → How to build (step-by-step workflows)
Layer 2: CORE (3)      → Cross-cutting (database, permissions, API)
Layer 1: SYNTAX (8)    → How to write (foundation patterns)
```

## File Locations

All skills are in `.claude/skills/dcnet_quality/`:

| Domain | Syntax | Implementation | Errors |
|--------|--------|----------------|--------|
| Client Scripts | `syntax/erpnext-syntax-clientscripts/` | `impl/erpnext-impl-clientscripts/` | `errors/erpnext-errors-clientscripts/` |
| Server Scripts | `syntax/erpnext-syntax-serverscripts/` | `impl/erpnext-impl-serverscripts/` | `errors/erpnext-errors-serverscripts/` |
| Controllers | `syntax/erpnext-syntax-controllers/` | `impl/erpnext-impl-controllers/` | `errors/erpnext-errors-controllers/` |
| hooks.py | `syntax/erpnext-syntax-hooks/` | `impl/erpnext-impl-hooks/` | `errors/erpnext-errors-hooks/` |
| Whitelisted | `syntax/erpnext-syntax-whitelisted/` | `impl/erpnext-impl-whitelisted/` | - |
| Jinja | `syntax/erpnext-syntax-jinja/` | `impl/erpnext-impl-jinja/` | - |
| Scheduler | `syntax/erpnext-syntax-scheduler/` | `impl/erpnext-impl-scheduler/` | - |
| Custom App | `syntax/erpnext-syntax-customapp/` | `impl/erpnext-impl-customapp/` | - |
| Database | `core/erpnext-database/` | - | `errors/erpnext-errors-database/` |
| Permissions | `core/erpnext-permissions/` | - | `errors/erpnext-errors-permissions/` |
| API | `core/erpnext-api-patterns/` | - | `errors/erpnext-errors-api/` |

Each skill folder contains `SKILL.md` + `references/` with examples, anti-patterns, workflows.

## DCNET Coding Standards (Extracted from frappe-claude best practices)

### Import Order Convention (STRICTLY ENFORCED)

```python
# 1. Standard library (alphabetically)
import json
import os
from datetime import datetime

# 2. Frappe framework
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint, cstr, nowdate, getdate, add_days

# 3. Third-party libraries
import requests
from redis import Redis

# 4. Local/custom modules (app-specific)
from dcnet_apps.utils import get_company_settings
from dcnet_apps.overrides.selling import calculate_discount
```

### API Response Envelope (Standard for @frappe.whitelist)

```python
@frappe.whitelist()
def get_dashboard_data(customer, from_date=None):
    """Get customer dashboard data.

    Args:
        customer (str): Customer ID
        from_date (str, optional): Start date filter

    Returns:
        dict: Response with success/data/message keys

    Raises:
        frappe.ValidationError: When customer not found
    """
    try:
        if not frappe.db.exists("Customer", customer):
            return {"success": False, "message": _("Customer not found")}

        data = compute_dashboard(customer, from_date)
        return {
            "success": True,
            "data": data,
            "message": _("Dashboard loaded")
        }
    except Exception as e:
        frappe.log_error(
            title="Dashboard API Error",
            message=f"Customer: {customer}\n{frappe.get_traceback()}"
        )
        return {"success": False, "message": str(e)}
```

### Docstring Format (Required for all public functions)

```python
def calculate_outstanding(customer: str, company: str = None) -> dict:
    """Calculate customer outstanding balance with aging analysis.

    Args:
        customer (str): Customer name/ID
        company (str, optional): Company filter. Defaults to user's default company.

    Returns:
        dict: Outstanding data with keys:
            - total (float): Total outstanding
            - overdue (float): Overdue amount
            - aging (list): Aging buckets [0-30, 31-60, 61-90, 90+]

    Raises:
        frappe.ValidationError: When customer doesn't exist
        frappe.PermissionError: When user lacks read access
    """
```

## Frappe-Specific Debug Checklist

When debugging Frappe/ERPNext issues, follow this order:

```
1. CHECK LOGS FIRST
   → tail -100 logs/frappe.log (or docker exec ... tail ...)
   → Check Error Log DocType in Desk

2. IDENTIFY ERROR TYPE
   → ValidationError: Check controller validate() + doc_events
   → PermissionError: Check roles, DocPerm, User Permission
   → LinkValidationError: Check if linked doc exists
   → MandatoryError: Check reqd fields + mandatory_depends_on
   → DuplicateEntryError: Check unique constraints

3. REPRODUCE IN CONSOLE
   → bench --site <site> console
   → frappe.get_doc("DocType", "name") → inspect state
   → frappe.has_permission("DocType", "write", "name") → check perms

4. CHECK PERMISSIONS (if access issue)
   → frappe.get_roles("user@email.com")
   → frappe.get_all("DocPerm", filters={"parent": "DocType"})
   → frappe.get_all("User Permission", filters={"user": "..."})

5. CHECK DATA INTEGRITY
   → Orphaned child records: LEFT JOIN parent IS NULL
   → Invalid links: field NOT IN (SELECT name FROM linked_table)
   → Duplicate entries: GROUP BY HAVING count > 1

6. CLEAR CACHE (if stale data)
   → bench --site <site> clear-cache
   → frappe.clear_document_cache("DocType", "name")
   → frappe.clear_cache(doctype="DocType")

7. CHECK BACKGROUND JOBS (if async issue)
   → bench --site <site> show-pending-jobs
   → Check logs/worker.error.log
   → from frappe.utils.background_jobs import get_jobs

8. CHECK CONFIGURATION
   → site_config.json (database, redis, email)
   → common_site_config.json (shared settings)
   → hooks.py (doc_events, override_doctype_class)

9. CHECK RECENT CHANGES
   → git log --oneline -20
   → git diff HEAD~5 -- hooks.py
   → bench --site <site> migrate (if schema out of sync)

10. PROFILE IF SLOW
    → site_config.json: "log_slow_queries": 1
    → cProfile for Python profiling
    → tracemalloc for memory debugging
```

## Performance Profiling Patterns

### Python Profiling (cProfile)

```python
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    """Profile a function and log results."""
    profiler = cProfile.Profile()
    profiler.enable()

    result = func(*args, **kwargs)

    profiler.disable()
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(20)

    frappe.log_error(
        title=f"Profile: {func.__name__}",
        message=stream.getvalue()
    )
    return result

# Usage in debugging
profile_function(frappe.get_doc, "Sales Invoice", "SINV-00001")
```

### Memory Profiling (tracemalloc)

```python
import tracemalloc

def debug_memory_usage(label=""):
    """Snapshot memory and log top allocations."""
    if not tracemalloc.is_tracing():
        tracemalloc.start()

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    output = [f"Memory snapshot: {label}"]
    for stat in top_stats[:15]:
        output.append(str(stat))

    frappe.log_error(
        title=f"Memory Debug: {label}",
        message="\n".join(output)
    )

# Usage
debug_memory_usage("before_heavy_query")
heavy_result = frappe.db.sql("SELECT * FROM `tabGL Entry`", as_dict=True)
debug_memory_usage("after_heavy_query")
```

### Query Performance (N+1 Detection)

```python
# BAD: N+1 query pattern (1 query per item)
for item in items:
    supplier = frappe.db.get_value("Supplier", item.supplier, "supplier_name")

# GOOD: Batch fetch (1 query total)
supplier_names = {s.name: s.supplier_name for s in frappe.db.get_all(
    "Supplier",
    filters={"name": ["in", [i.supplier for i in items]]},
    fields=["name", "supplier_name"]
)}
for item in items:
    supplier = supplier_names.get(item.supplier)

# GOOD: Use frappe.qb for complex batch queries
from frappe.query_builder import DocType
Item = DocType("Item")
Supplier = DocType("Supplier")
result = (
    frappe.qb.from_(Item)
    .join(Supplier).on(Item.default_supplier == Supplier.name)
    .select(Item.name, Item.item_name, Supplier.supplier_name)
    .where(Item.name.isin([i.item_code for i in items]))
    .run(as_dict=True)
)
```

## Compatibility

All patterns validated for **Frappe/ERPNext v16** (DCNET Flow target platform).
