# API Reference: Background Job Handlers

**Language**: Python

**Source**: `frappe/core/doctype/data_import/data_import.py`

---

## Overview

Large imports are processed as background jobs using Frappe's job queue (RQ - Redis Queue). This allows imports to run asynchronously without blocking the UI.

## Background Job Functions

### start_import

Main entry point for background import jobs.

```python
def start_import(data_import: str) -> None:
    """
    This method runs in background job.

    Args:
        data_import: Name of Data Import document

    Called by:
        DataImport.start_import() -> frappe.enqueue()
    """
```

**Implementation:**

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

def start_import(data_import):
    """Background job handler for data import."""
    frappe.publish_realtime(
        "data_import_progress",
        {"data_import": data_import, "status": "started"},
        user=frappe.session.user
    )

    try:
        doc = frappe.get_doc("Data Import", data_import)
        importer = doc.get_importer()
        importer.import_data()

        doc.reload()
        doc.db_set("status", "Success" if all_success else "Partial Success")

    except Exception as e:
        frappe.log_error(title="Data Import Failed")
        doc.db_set("status", "Error")

    finally:
        frappe.publish_realtime(
            "data_import_progress",
            {"data_import": data_import, "status": "completed"},
            user=frappe.session.user
        )
```

### form_start_import

Whitelist function to start import from UI.

```python
@frappe.whitelist()
def form_start_import(data_import: str) -> None:
    """
    Start import via form button.

    Args:
        data_import: Name of Data Import document

    Enqueues background job with proper timeout.
    """
```

**Example:**

```javascript
// From Data Import form
frappe.call({
    method: "frappe.core.doctype.data_import.data_import.form_start_import",
    args: {
        data_import: frm.doc.name
    },
    callback: function(r) {
        frappe.show_alert({
            message: __("Import started in background"),
            indicator: "green"
        });
    }
});
```

### stop_data_import

Stops a running import job.

```python
@frappe.whitelist()
def stop_data_import(doc_name: str) -> None:
    """
    Stop a running Data Import job.

    Args:
        doc_name: Name of Data Import document
    """
```

## Job Queue Configuration

### Enqueue Import

```python
import frappe

def enqueue_import(data_import_name):
    """Enqueue data import as background job."""
    frappe.enqueue(
        "frappe.core.doctype.data_import.data_import.start_import",
        queue="long",  # Use long queue for large imports
        timeout=6000,  # 100 minutes timeout
        data_import=data_import_name,
        now=frappe.flags.in_test  # Run synchronously in tests
    )
```

### Queue Options

| Queue | Timeout | Use Case |
|-------|---------|----------|
| `short` | 300s | Small imports (<100 rows) |
| `default` | 1500s | Medium imports (100-1000 rows) |
| `long` | 6000s | Large imports (1000+ rows) |

### Custom Queue Configuration

```python
# In your app's hooks.py
scheduler_events = {
    "cron": {
        "0 2 * * *": [  # Run at 2 AM
            "your_app.imports.scheduled_import"
        ]
    }
}

# In your_app/imports.py
def scheduled_import():
    """Process queued imports at night."""
    imports = frappe.get_all(
        "Data Import",
        filters={"status": "Pending", "scheduled": 1},
        limit=10
    )

    for imp in imports:
        frappe.enqueue(
            "frappe.core.doctype.data_import.data_import.start_import",
            queue="long",
            data_import=imp.name
        )
```

## Progress Tracking

### Real-time Progress Updates

```python
def update_progress(data_import, current, total):
    """Publish progress updates to UI."""
    frappe.publish_realtime(
        "data_import_progress",
        {
            "data_import": data_import,
            "current": current,
            "total": total,
            "percent": (current / total) * 100
        },
        user=frappe.session.user
    )
```

### JavaScript Progress Handler

```javascript
// Listen for progress updates
frappe.realtime.on("data_import_progress", function(data) {
    if (data.data_import === cur_frm.doc.name) {
        if (data.status === "completed") {
            cur_frm.reload_doc();
        } else {
            frappe.show_progress(
                __("Importing"),
                data.current,
                data.total,
                __("{0} of {1}", [data.current, data.total])
            );
        }
    }
});
```

### Status Updates

```python
def update_import_status(data_import, status, message=None):
    """Update import status with optional message."""
    import frappe

    doc = frappe.get_doc("Data Import", data_import)
    doc.db_set("status", status)

    if message:
        frappe.publish_realtime(
            "data_import_message",
            {
                "data_import": data_import,
                "message": message,
                "status": status
            },
            user=frappe.session.user
        )
```

## Error Handling in Background Jobs

### Job Failure Handler

```python
import frappe

def handle_import_failure(data_import, error):
    """Handle background job failure."""
    # Log the error
    frappe.log_error(
        title=f"Data Import Failed: {data_import}",
        message=str(error)
    )

    # Update status
    frappe.db.set_value("Data Import", data_import, "status", "Error")

    # Notify user
    frappe.publish_realtime(
        "data_import_error",
        {
            "data_import": data_import,
            "error": str(error)
        },
        user=frappe.session.user
    )

    # Send email notification
    doc = frappe.get_doc("Data Import", data_import)
    if doc.owner:
        frappe.sendmail(
            recipients=[doc.owner],
            subject=f"Data Import Failed: {data_import}",
            message=f"Your data import has failed. Error: {error}"
        )
```

### Retry Failed Jobs

```python
def retry_failed_import(data_import_name, max_retries=3):
    """Retry failed import with exponential backoff."""
    import frappe
    from frappe.utils import now_datetime, add_to_date

    doc = frappe.get_doc("Data Import", data_import_name)
    retry_count = doc.get("retry_count") or 0

    if retry_count >= max_retries:
        doc.db_set("status", "Failed - Max Retries")
        return False

    # Calculate backoff delay
    delay_minutes = 2 ** retry_count  # 1, 2, 4, 8 minutes

    # Schedule retry
    frappe.enqueue(
        "frappe.core.doctype.data_import.data_import.start_import",
        queue="long",
        at_front=False,
        enqueue_after_commit=True,
        data_import=data_import_name
    )

    doc.db_set("retry_count", retry_count + 1)
    doc.db_set("status", f"Retrying ({retry_count + 1}/{max_retries})")

    return True
```

## Monitoring Jobs

### Check Job Status

```python
import frappe
from frappe.utils.background_jobs import get_jobs

def check_import_job_status(data_import_name):
    """Check if import job is still running."""
    jobs = get_jobs()

    for job in jobs:
        if "start_import" in job.get("job_name", ""):
            if data_import_name in str(job.get("kwargs", {})):
                return {
                    "running": True,
                    "job_id": job.get("job_id"),
                    "started": job.get("started")
                }

    return {"running": False}
```

### List Running Imports

```python
def get_running_imports():
    """Get all currently running imports."""
    import frappe

    return frappe.get_all(
        "Data Import",
        filters={"status": "In Progress"},
        fields=["name", "reference_doctype", "owner", "creation"]
    )
```

## Usage Examples

### Complete Background Import Flow

```python
import frappe

def run_import_with_notifications(doctype, file_path, user):
    """
    Run import in background with full notification support.
    """
    # Create Data Import document
    data_import = frappe.new_doc("Data Import")
    data_import.reference_doctype = doctype
    data_import.import_type = "Insert New Records"
    data_import.import_file = file_path
    data_import.owner = user
    data_import.insert()

    # Notify user that import is queued
    frappe.publish_realtime(
        "msgprint",
        f"Import {data_import.name} has been queued",
        user=user
    )

    # Enqueue the job
    frappe.enqueue(
        "frappe.core.doctype.data_import.data_import.start_import",
        queue="long",
        timeout=6000,
        data_import=data_import.name,
        # Custom callback for completion notification
        on_success=notify_import_complete,
        on_failure=notify_import_failed
    )

    return data_import.name

def notify_import_complete(data_import):
    """Callback when import completes successfully."""
    doc = frappe.get_doc("Data Import", data_import)
    success_count = frappe.db.count("Data Import Log", {
        "parent": data_import,
        "success": 1
    })

    frappe.sendmail(
        recipients=[doc.owner],
        subject=f"Import Complete: {data_import}",
        message=f"Successfully imported {success_count} records."
    )

def notify_import_failed(data_import, error):
    """Callback when import fails."""
    doc = frappe.get_doc("Data Import", data_import)

    frappe.sendmail(
        recipients=[doc.owner],
        subject=f"Import Failed: {data_import}",
        message=f"Import failed with error: {error}"
    )
```

### Batch Processing Large Files

```python
def batch_import(doctype, file_path, batch_size=500):
    """
    Split large file into batches for parallel processing.
    """
    import csv
    from frappe.utils.file_manager import get_file

    # Read file
    content = get_file(file_path)
    reader = csv.reader(content.decode("utf-8").splitlines())
    rows = list(reader)

    header = rows[0]
    data_rows = rows[1:]

    # Split into batches
    batches = [
        data_rows[i:i + batch_size]
        for i in range(0, len(data_rows), batch_size)
    ]

    batch_imports = []
    for i, batch in enumerate(batches):
        # Create temp file for batch
        batch_content = [header] + batch
        temp_file = save_batch_file(batch_content, f"batch_{i}.csv")

        # Create Data Import for batch
        data_import = frappe.new_doc("Data Import")
        data_import.reference_doctype = doctype
        data_import.import_file = temp_file
        data_import.flags.batch_number = i
        data_import.insert()

        batch_imports.append(data_import.name)

        # Enqueue
        frappe.enqueue(
            "frappe.core.doctype.data_import.data_import.start_import",
            queue="long",
            data_import=data_import.name
        )

    return batch_imports
```

## Related References

- [Data Import](data_import.md) - DocType reference
- [Importer](importer.md) - Import logic
- [Error Handling](error_handling.md) - Error management

---

*Source: frappe/core/doctype/data_import/data_import.py | Last updated: 2026-02-04*
