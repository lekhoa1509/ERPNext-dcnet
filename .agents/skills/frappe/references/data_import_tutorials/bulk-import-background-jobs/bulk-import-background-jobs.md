# How To: Bulk Import with Background Jobs

**Difficulty**: Advanced
**Estimated Time**: 40 minutes
**Tags**: bulk-import, background-jobs, performance

## Overview

Learn how to handle large data imports using Frappe's background job system. This ensures the UI remains responsive and provides progress tracking for long-running imports.

## Prerequisites

- Frappe/ERPNext with Redis configured
- Understanding of Frappe background jobs
- Basic Data Import experience

## Step-by-Step Guide

### Step 1: Understanding Background Jobs

Frappe uses Redis Queue (RQ) for background processing:

```python
# Jobs are queued to Redis and processed by workers
# Three queue types: short (5min), default (25min), long (100min)

import frappe

# Enqueue a job
frappe.enqueue(
    method="my_app.tasks.import_task",
    queue="long",
    timeout=6000,
    **kwargs
)
```

### Step 2: Create Basic Background Import

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

def start_background_import(data_import_name):
    """Start import in background."""
    frappe.enqueue(
        method="frappe.core.doctype.data_import.data_import.start_import",
        queue="long",
        timeout=6000,
        data_import=data_import_name
    )

    return {"message": "Import started in background", "import": data_import_name}

# Usage via Data Import document
data_import = frappe.get_doc("Data Import", "DATA-IMPORT-001")
data_import.start_import()  # This enqueues automatically
```

### Step 3: Add Progress Tracking

Track and report progress during import.

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

def import_with_progress(data_import_name):
    """Import with real-time progress updates."""
    data_import = frappe.get_doc("Data Import", data_import_name)
    importer = data_import.get_importer()

    # Get total rows
    importer.import_file.parse_data_from_template()
    total = len(importer.import_file.data)

    # Notify start
    frappe.publish_realtime(
        "data_import_progress",
        {
            "data_import": data_import_name,
            "status": "started",
            "current": 0,
            "total": total
        },
        user=frappe.session.user
    )

    processed = 0
    for doc, rows, indexes in importer.import_file.get_payloads_for_import():
        try:
            importer.process_doc(doc)
        except Exception as e:
            frappe.log_error(f"Row {indexes}: {e}")

        processed += 1

        # Update progress every 10 records
        if processed % 10 == 0:
            frappe.publish_realtime(
                "data_import_progress",
                {
                    "data_import": data_import_name,
                    "status": "in_progress",
                    "current": processed,
                    "total": total,
                    "percent": (processed / total) * 100
                },
                user=frappe.session.user
            )

    # Notify completion
    frappe.publish_realtime(
        "data_import_progress",
        {
            "data_import": data_import_name,
            "status": "completed",
            "current": total,
            "total": total
        },
        user=frappe.session.user
    )
```

### Step 4: JavaScript Progress Handler

Listen for progress updates in the UI.

```javascript
// In Data Import form or custom page
frappe.realtime.on("data_import_progress", function(data) {
    if (data.data_import === cur_frm.doc.name) {
        if (data.status === "started") {
            frappe.show_progress(
                __("Importing"),
                0,
                data.total,
                __("Starting import...")
            );
        } else if (data.status === "in_progress") {
            frappe.show_progress(
                __("Importing"),
                data.current,
                data.total,
                __("{0} of {1} records", [data.current, data.total])
            );
        } else if (data.status === "completed") {
            frappe.hide_progress();
            frappe.show_alert({
                message: __("Import completed!"),
                indicator: "green"
            });
            cur_frm.reload_doc();
        }
    }
});
```

### Step 5: Batch Processing for Large Files

Split large imports into batches.

```python
import frappe

def batch_import(doctype, file_path, batch_size=500):
    """
    Split large file into batches and process in background.
    """
    import csv

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    total = len(data)
    num_batches = (total + batch_size - 1) // batch_size

    # Create master job tracker
    master_job = frappe.get_doc({
        "doctype": "Custom DocType",  # Create a job tracker DocType
        "total_rows": total,
        "total_batches": num_batches,
        "status": "Queued"
    }).insert()

    # Queue each batch
    for i in range(num_batches):
        start = i * batch_size
        end = min(start + batch_size, total)
        batch = data[start:end]

        frappe.enqueue(
            method="your_app.imports.process_batch",
            queue="long",
            timeout=3600,
            batch_data=batch,
            batch_number=i + 1,
            master_job=master_job.name,
            doctype=doctype
        )

    return master_job.name

def process_batch(batch_data, batch_number, master_job, doctype):
    """Process a single batch."""
    success = 0
    failed = 0

    for row in batch_data:
        try:
            row["doctype"] = doctype
            doc = frappe.get_doc(row)
            doc.insert()
            success += 1
        except Exception as e:
            failed += 1
            frappe.log_error(f"Batch {batch_number} error: {e}")

    frappe.db.commit()

    # Update master job
    frappe.db.set_value("Custom DocType", master_job, {
        "completed_batches": frappe.db.get_value(
            "Custom DocType", master_job, "completed_batches"
        ) + 1,
        "success_count": frappe.db.get_value(
            "Custom DocType", master_job, "success_count"
        ) + success,
        "failed_count": frappe.db.get_value(
            "Custom DocType", master_job, "failed_count"
        ) + failed
    })

    # Publish progress
    frappe.publish_realtime(
        "batch_import_progress",
        {"master_job": master_job, "batch": batch_number}
    )
```

### Step 6: Parallel Processing

Process multiple batches in parallel.

```python
import frappe
from concurrent.futures import ThreadPoolExecutor

def parallel_import(doctype, file_path, num_workers=4):
    """
    Import using parallel workers.

    Note: Each worker needs own DB connection.
    """
    import csv

    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    chunk_size = len(data) // num_workers
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    results = []

    def process_chunk(chunk, chunk_id):
        """Process a chunk in separate thread."""
        frappe.connect()  # Each thread needs connection
        success = 0
        failed = 0

        try:
            for row in chunk:
                try:
                    row["doctype"] = doctype
                    doc = frappe.get_doc(row)
                    doc.insert()
                    success += 1
                except Exception:
                    failed += 1

            frappe.db.commit()
        finally:
            frappe.db.close()

        return {"chunk": chunk_id, "success": success, "failed": failed}

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(process_chunk, chunk, i)
            for i, chunk in enumerate(chunks)
        ]
        results = [f.result() for f in futures]

    return results
```

### Step 7: Handle Job Failures and Retry

Implement retry logic for failed jobs.

```python
import frappe

def import_with_retry(data_import_name, max_retries=3):
    """Import with automatic retry on failure."""
    retry_count = 0

    while retry_count < max_retries:
        try:
            data_import = frappe.get_doc("Data Import", data_import_name)
            importer = data_import.get_importer()
            importer.import_data()

            data_import.db_set("status", "Success")
            return {"success": True}

        except Exception as e:
            retry_count += 1
            frappe.log_error(
                f"Import attempt {retry_count} failed: {e}",
                "Data Import Retry"
            )

            if retry_count < max_retries:
                # Wait before retry (exponential backoff)
                import time
                time.sleep(2 ** retry_count)

    data_import.db_set("status", "Error")
    return {"success": False, "retries": max_retries}

def retry_failed_imports():
    """Scheduled job to retry failed imports."""
    failed_imports = frappe.get_all(
        "Data Import",
        filters={
            "status": "Error",
            "retry_count": ["<", 3],
            "modified": [">=", frappe.utils.add_days(frappe.utils.now(), -1)]
        },
        pluck="name"
    )

    for name in failed_imports:
        frappe.enqueue(
            method="your_app.imports.import_with_retry",
            queue="long",
            data_import_name=name
        )
```

## Complete Example

```python
import frappe
from frappe.core.doctype.data_import.importer import Importer

class BackgroundImportManager:
    """
    Manage large imports with background processing.
    """

    def __init__(self, doctype, file_path):
        self.doctype = doctype
        self.file_path = file_path
        self.batch_size = 500
        self.job_id = None

    def start_import(self, async_mode=True):
        """Start the import process."""
        # Create Data Import document
        data_import = self.create_data_import()

        if async_mode:
            # Queue background job
            self.job_id = frappe.enqueue(
                method=self.run_import,
                queue="long",
                timeout=7200,  # 2 hours
                data_import_name=data_import.name
            )

            return {
                "message": "Import queued",
                "data_import": data_import.name,
                "job_id": self.job_id
            }
        else:
            # Run synchronously
            return self.run_import(data_import.name)

    def create_data_import(self):
        """Create Data Import document."""
        data_import = frappe.new_doc("Data Import")
        data_import.reference_doctype = self.doctype
        data_import.import_type = "Insert New Records"
        data_import.import_file = self.file_path
        data_import.insert()
        return data_import

    def run_import(self, data_import_name):
        """Run the actual import."""
        data_import = frappe.get_doc("Data Import", data_import_name)
        data_import.db_set("status", "In Progress")

        try:
            importer = Importer(
                self.doctype,
                data_import=data_import,
                console=False
            )

            # Get total for progress
            importer.import_file.parse_data_from_template()
            total = len(importer.import_file.data)

            self.notify_progress(data_import_name, "started", 0, total)

            # Import with progress updates
            success = 0
            failed = 0

            for i, (doc, rows, indexes) in enumerate(
                importer.import_file.get_payloads_for_import()
            ):
                try:
                    importer.process_doc(doc)
                    success += 1
                except Exception as e:
                    failed += 1
                    self.log_error(data_import_name, indexes, str(e))

                # Update progress every batch
                if (i + 1) % self.batch_size == 0:
                    frappe.db.commit()
                    self.notify_progress(data_import_name, "in_progress", i + 1, total)

            frappe.db.commit()

            # Final status
            status = "Success" if failed == 0 else "Partial Success"
            data_import.db_set("status", status)

            self.notify_progress(data_import_name, "completed", total, total)

            return {
                "status": status,
                "success": success,
                "failed": failed,
                "total": total
            }

        except Exception as e:
            data_import.db_set("status", "Error")
            frappe.log_error(f"Import failed: {e}", "Background Import")
            self.notify_progress(data_import_name, "error", 0, 0)
            raise

    def notify_progress(self, data_import_name, status, current, total):
        """Send progress notification."""
        frappe.publish_realtime(
            "data_import_progress",
            {
                "data_import": data_import_name,
                "status": status,
                "current": current,
                "total": total,
                "percent": (current / total * 100) if total > 0 else 0
            },
            user=frappe.session.user
        )

    def log_error(self, data_import_name, row_indexes, error_message):
        """Log import error."""
        frappe.get_doc({
            "doctype": "Data Import Log",
            "parent": data_import_name,
            "parenttype": "Data Import",
            "parentfield": "import_log",
            "success": 0,
            "messages": frappe.as_json([error_message]),
            "row_indexes": ",".join(str(i) for i in row_indexes)
        }).insert()


# Usage
manager = BackgroundImportManager("Customer", "/files/customers.csv")
result = manager.start_import(async_mode=True)
print(f"Import started: {result['data_import']}")
```

## Monitoring Jobs

```python
# Check job status
from frappe.utils.background_jobs import get_jobs

def check_import_jobs():
    """List all running import jobs."""
    jobs = get_jobs()
    import_jobs = [
        j for j in jobs
        if "data_import" in j.get("job_name", "").lower()
    ]
    return import_jobs

# Cancel a job
def cancel_import_job(job_id):
    """Cancel a running import job."""
    from rq import cancel_job
    cancel_job(job_id)
```

## Next Steps

- [Import Validation and Error Handling](../import-validation-error-handling/import-validation-error-handling.md)
- [Performance Optimization](../performance-optimization/performance-optimization.md)

---

*Last updated: 2026-02-04*
