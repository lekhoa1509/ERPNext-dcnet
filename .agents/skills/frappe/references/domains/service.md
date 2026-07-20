# Frappe Service Layer

Patterns for organizing business logic, background processing, scheduled tasks, and service architecture in Frappe applications.

---

## Service Class Pattern

### Why a Service Layer?

Frappe DocType controllers (`*.py`) handle document lifecycle events (validate, before_save, on_submit). For complex business logic that spans multiple DocTypes or involves external systems, extract logic into service classes.

```
Controller (fitting_session.py)
    validates fields, triggers events
        calls Service (fitting_completion.py)
            orchestrates business logic across DocTypes
                calls Repository (data access) if needed
```

### Basic Service Class

```python
# dcnet_apps/fitting/services/fitting_completion.py

import frappe
from frappe import _


class FittingCompletionService:
    """Handles business logic when a fitting session is completed."""

    def __init__(self, session_name):
        self.session_name = session_name
        self.session = None

    def execute(self):
        """Main entry point. Completes a fitting session end-to-end."""
        self.session = frappe.get_doc("Fitting Session", self.session_name)
        self._validate_can_complete()
        self._generate_report()
        self._create_follow_up_task()
        self._notify_customer()
        return self.session

    def _validate_can_complete(self):
        if not self.session.measurements:
            frappe.throw(_("Cannot complete session without measurements"))
        if self.session.workflow_state != "In Progress":
            frappe.throw(_("Session must be In Progress to complete"))

    def _generate_report(self):
        """Create a Fitting Report document from measurements."""
        report = frappe.get_doc({
            "doctype": "Fitting Report",
            "fitting_session": self.session.name,
            "customer": self.session.customer,
            "measurements": self.session.measurements
        })
        report.insert()
        self.session.fitting_report = report.name
        self.session.save()

    def _create_follow_up_task(self):
        """Create a ToDo for follow-up after fitting."""
        frappe.get_doc({
            "doctype": "ToDo",
            "description": f"Follow up on fitting {self.session.name}",
            "reference_type": "Fitting Session",
            "reference_name": self.session.name,
            "allocated_to": self.session.fitter,
            "date": frappe.utils.add_days(frappe.utils.today(), 7)
        }).insert()

    def _notify_customer(self):
        """Send completion notification email."""
        if frappe.flags.in_test:
            return

        frappe.sendmail(
            recipients=[self.session.customer_email],
            subject=_("Fitting Session Complete - {0}").format(self.session.name),
            template="fitting_complete",
            args={"session": self.session}
        )
```

### Calling the Service from Controller

```python
# dcnet_apps/fitting/doctype/fitting_session/fitting_session.py

class FittingSession(Document):
    def on_update(self):
        if self.workflow_state == "Completed":
            from dcnet_apps.fitting.services.fitting_completion import FittingCompletionService
            FittingCompletionService(self.name).execute()
```

### Calling from API Endpoint

```python
# dcnet_apps/fitting/api.py

@frappe.whitelist()
def complete_fitting(session_name):
    from dcnet_apps.fitting.services.fitting_completion import FittingCompletionService
    result = FittingCompletionService(session_name).execute()
    return {"status": "success", "name": result.name}
```

---

## Repository Pattern for Data Access

For complex queries, encapsulate data access in repository classes:

```python
# dcnet_apps/fitting/services/fitting_repository.py

import frappe


class FittingRepository:
    """Data access layer for Fitting-related queries."""

    @staticmethod
    def get_active_sessions(customer=None, fitter=None, limit=20):
        """Get active fitting sessions with optional filters."""
        filters = {"workflow_state": ["not in", ["Completed", "Cancelled"]]}
        if customer:
            filters["customer"] = customer
        if fitter:
            filters["fitter"] = fitter

        return frappe.get_all(
            "Fitting Session",
            filters=filters,
            fields=["name", "customer", "fitting_date", "workflow_state", "fitter"],
            order_by="fitting_date asc",
            limit_page_length=limit
        )

    @staticmethod
    def get_session_with_details(session_name):
        """Get full session with child tables loaded."""
        session = frappe.get_doc("Fitting Session", session_name)
        session.check_permission("read")
        return session

    @staticmethod
    def get_customer_fitting_history(customer, limit=10):
        """Get completed fittings for a customer."""
        return frappe.get_all(
            "Fitting Session",
            filters={
                "customer": customer,
                "workflow_state": "Completed"
            },
            fields=["name", "fitting_date", "fitter", "fitting_report"],
            order_by="fitting_date desc",
            limit_page_length=limit
        )

    @staticmethod
    def count_pending_by_fitter():
        """Get count of pending sessions grouped by fitter."""
        return frappe.db.sql("""
            SELECT fitter, COUNT(*) as count
            FROM `tabFitting Session`
            WHERE workflow_state IN ('Scheduled', 'In Progress')
            GROUP BY fitter
            ORDER BY count DESC
        """, as_dict=True)
```

---

## Background Jobs with frappe.enqueue()

### Basic Usage

```python
import frappe

# Simple enqueue
frappe.enqueue(
    "dcnet_apps.fitting.tasks.generate_monthly_report",
    month="2026-01",
    queue="long"
)

# With all options
frappe.enqueue(
    method="dcnet_apps.fitting.tasks.process_bulk_fittings",
    queue="long",
    timeout=600,                    # seconds (default: 300)
    is_async=True,                  # True by default
    now=False,                      # if True, runs synchronously (useful in tests)
    job_name="bulk_fitting_2026_01",  # unique name (prevents duplicates)
    at_front=False,                 # push to front of queue
    enqueue_after_commit=True,      # wait for current transaction to commit
    # Function arguments:
    session_names=["FS-001", "FS-002", "FS-003"],
    notify=True
)
```

### Queue Types

| Queue | Use Case | Default Timeout | Workers |
|-------|----------|----------------|---------|
| `short` | Quick tasks (< 30s): emails, cache updates | 300s | 1 |
| `default` | Standard tasks (< 5min): doc processing, API calls | 300s | 1 |
| `long` | Heavy tasks (> 5min): reports, bulk operations, data migration | 1500s | 1 |

### Background Job Function

```python
# dcnet_apps/fitting/tasks.py

import frappe
from frappe import _


def generate_monthly_report(month):
    """Generate monthly fitting report. Runs as background job."""
    frappe.publish_realtime(
        "fitting_report_progress",
        {"status": "started", "month": month}
    )

    try:
        sessions = frappe.get_all(
            "Fitting Session",
            filters={
                "fitting_date": ["between", [f"{month}-01", f"{month}-31"]],
                "workflow_state": "Completed"
            },
            fields=["name", "customer", "fitter", "fitting_date"]
        )

        # Process...
        report = create_report_doc(month, sessions)

        frappe.publish_realtime(
            "fitting_report_progress",
            {"status": "completed", "report": report.name}
        )
    except Exception:
        frappe.log_error(title=f"Monthly Report Failed: {month}")
        frappe.publish_realtime(
            "fitting_report_progress",
            {"status": "failed", "month": month}
        )
        raise


def process_bulk_fittings(session_names, notify=False):
    """Process multiple fitting sessions in bulk."""
    total = len(session_names)

    for i, name in enumerate(session_names):
        try:
            session = frappe.get_doc("Fitting Session", name)
            # Process each session...
            session.save()

            # Progress update
            frappe.publish_progress(
                percent=(i + 1) / total * 100,
                title=_("Processing Fittings"),
                description=f"Processing {name}"
            )
        except Exception:
            frappe.log_error(title=f"Bulk Fitting Error: {name}")

    if notify:
        frappe.sendmail(
            recipients=[frappe.session.user],
            subject=_("Bulk Fitting Processing Complete"),
            message=f"Processed {total} fitting sessions."
        )
```

### doc.queue_action()

For document-specific background actions:

```python
# In DocType controller or API
doc = frappe.get_doc("Fitting Session", "FS-00001")

# Submit in background
doc.queue_action("submit")

# Cancel in background
doc.queue_action("cancel")

# Custom method in background
doc.queue_action("run_custom_processing", timeout=600)
```

The `queue_action` method wraps the document method call in `frappe.enqueue()` with proper locking.

---

## Scheduled Tasks (hooks.py)

### Configuration in hooks.py

```python
# hooks.py

scheduler_events = {
    # Run every minute (use sparingly!)
    "all": [
        "dcnet_apps.fitting.tasks.check_overdue_sessions"
    ],

    # Run once daily (midnight)
    "daily": [
        "dcnet_apps.fitting.tasks.send_daily_fitting_summary",
        "dcnet_apps.fitting.tasks.archive_old_sessions"
    ],

    # Hourly
    "hourly": [
        "dcnet_apps.fitting.tasks.sync_external_bookings"
    ],

    # Weekly (Sunday midnight)
    "weekly": [
        "dcnet_apps.fitting.tasks.generate_weekly_report"
    ],

    # Monthly (1st of month, midnight)
    "monthly": [
        "dcnet_apps.fitting.tasks.generate_monthly_report"
    ],

    # Cron expressions for precise scheduling
    "cron": {
        # Every day at 8 AM
        "0 8 * * *": [
            "dcnet_apps.fitting.tasks.send_fitting_reminders"
        ],
        # Every weekday at 6 PM
        "0 18 * * 1-5": [
            "dcnet_apps.fitting.tasks.send_daily_summary"
        ],
        # Every 15 minutes
        "*/15 * * * *": [
            "dcnet_apps.fitting.tasks.check_pending_approvals"
        ]
    }
}
```

### Scheduler Event Reference

| Event | When | Use Case |
|-------|------|----------|
| `all` | Every minute | Real-time monitoring (use sparingly) |
| `hourly` | Every hour | Syncing external data, cleanup |
| `daily` | Midnight | Daily summaries, archiving |
| `weekly` | Sunday midnight | Weekly reports |
| `monthly` | 1st of month | Monthly reports, billing |
| `daily_long` | Midnight (long queue) | Heavy daily processing |
| `hourly_long` | Every hour (long queue) | Heavy hourly processing |
| `weekly_long` | Sunday (long queue) | Heavy weekly processing |
| `monthly_long` | 1st (long queue) | Heavy monthly processing |
| `cron` | Custom schedule | Any specific schedule |

### Scheduled Task Implementation

```python
# dcnet_apps/fitting/tasks.py

def send_fitting_reminders():
    """Send reminders for tomorrow's fitting sessions.
    Scheduled: daily at 8 AM via cron.
    """
    tomorrow = frappe.utils.add_days(frappe.utils.today(), 1)

    sessions = frappe.get_all(
        "Fitting Session",
        filters={
            "fitting_date": tomorrow,
            "workflow_state": "Scheduled"
        },
        fields=["name", "customer", "customer_email", "fitting_date", "fitter"]
    )

    for session in sessions:
        if not session.customer_email:
            continue

        frappe.sendmail(
            recipients=[session.customer_email],
            subject=f"Reminder: Fitting Session Tomorrow - {session.name}",
            template="fitting_reminder",
            args=session
        )

    frappe.logger().info(f"Sent {len(sessions)} fitting reminders for {tomorrow}")
```

---

## Error Handling in Background Jobs

### Logging Errors

```python
def risky_background_task():
    try:
        # ... processing ...
        pass
    except frappe.ValidationError:
        # Expected validation errors -- log and continue
        frappe.log_error(title="Fitting Validation Error")
    except Exception:
        # Unexpected errors -- log full traceback
        frappe.log_error(title="Fitting Background Task Failed")
        raise  # Re-raise so the job is marked as failed
```

### frappe.log_error()

```python
# Logs to Error Log doctype with full traceback
frappe.log_error(
    title="Fitting Sync Failed",       # Short title
    message="Additional context here"  # Optional extra info
)
# Traceback is auto-captured from sys.exc_info()

# Or log without an active exception
frappe.log_error(
    title="Unexpected State",
    message=f"Session {name} in state {state}, expected Scheduled"
)
```

---

## Retry Patterns

### Manual Retry with enqueue

```python
def process_with_retry(session_name, attempt=1, max_attempts=3):
    """Process a fitting session with retry logic."""
    try:
        session = frappe.get_doc("Fitting Session", session_name)
        # ... processing ...
        session.save()
        frappe.db.commit()
    except Exception:
        frappe.db.rollback()
        frappe.log_error(title=f"Fitting Process Attempt {attempt}/{max_attempts}")

        if attempt < max_attempts:
            # Retry with exponential backoff via delayed enqueue
            frappe.enqueue(
                "dcnet_apps.fitting.tasks.process_with_retry",
                session_name=session_name,
                attempt=attempt + 1,
                max_attempts=max_attempts,
                queue="default",
                enqueue_after_commit=True
            )
        else:
            # Max retries exhausted -- alert admin
            frappe.sendmail(
                recipients=["admin@dcnet.vn"],
                subject=f"Fitting Processing Failed After {max_attempts} Attempts",
                message=f"Session: {session_name}"
            )
```

### Preventing Duplicate Jobs

```python
# Use job_name to prevent duplicate enqueues
frappe.enqueue(
    "dcnet_apps.fitting.tasks.sync_all_fittings",
    job_name="sync_all_fittings",  # Only one job with this name at a time
    queue="long"
)

# Check if job is already running
from frappe.utils.background_jobs import is_job_enqueued
if not is_job_enqueued("sync_all_fittings"):
    frappe.enqueue(
        "dcnet_apps.fitting.tasks.sync_all_fittings",
        job_name="sync_all_fittings",
        queue="long"
    )
```

---

## Idempotency

Background jobs may execute more than once (worker crash, retry). Design for idempotency:

```python
def create_fitting_report(session_name):
    """Create report for session. Idempotent -- safe to call multiple times."""

    # Check if already processed
    existing = frappe.db.exists("Fitting Report", {"fitting_session": session_name})
    if existing:
        frappe.logger().info(f"Report already exists for {session_name}, skipping")
        return frappe.get_doc("Fitting Report", existing)

    # Create new report
    session = frappe.get_doc("Fitting Session", session_name)
    report = frappe.get_doc({
        "doctype": "Fitting Report",
        "fitting_session": session_name,
        "customer": session.customer,
    })
    report.insert()
    frappe.db.commit()
    return report


def update_fitting_status_bulk(session_names, target_status):
    """Bulk status update. Idempotent -- skips already-updated sessions."""
    updated = 0

    for name in session_names:
        current_status = frappe.db.get_value("Fitting Session", name, "custom_sync_status")
        if current_status == target_status:
            continue  # Already in target status, skip

        frappe.db.set_value("Fitting Session", name, "custom_sync_status", target_status)
        updated += 1

    frappe.db.commit()
    return {"total": len(session_names), "updated": updated, "skipped": len(session_names) - updated}
```

---

## Service Directory Structure

```
dcnet_apps/
  dcnet_apps/
    fitting/
      doctype/                    # DocType controllers (thin)
        fitting_session/
          fitting_session.py      # Delegates to services
      services/                   # Business logic layer
        __init__.py
        fitting_completion.py     # Completion workflow logic
        fitting_repository.py     # Data access queries
        fitting_sync.py           # External system sync
      tasks.py                    # Background jobs & scheduled tasks
      api.py                      # Whitelisted API endpoints
```

### Service Layer Guidelines

| Guideline | Description |
|-----------|-------------|
| **Thin controllers** | DocType `*.py` should validate and delegate, not contain business logic |
| **One responsibility** | Each service class handles one business operation |
| **Testable** | Services should accept parameters, not read from `frappe.form_dict` |
| **Transaction aware** | Services should not call `frappe.db.commit()` -- let the caller decide |
| **Error handling** | Use `frappe.throw()` for user-facing errors, `raise` for system errors |
| **No side effects** | Constructor should not trigger actions; use an explicit `execute()` method |
