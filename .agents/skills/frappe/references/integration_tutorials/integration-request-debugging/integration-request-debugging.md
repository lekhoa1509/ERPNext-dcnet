# How To: Integration Request Logging and Debugging

**Difficulty**: Intermediate
**Estimated Time**: 20 minutes
**Tags**: integration-request, debugging, logging, http, troubleshooting

## Overview

Learn how to use Integration Request DocType to log, monitor, and debug HTTP integrations in Frappe.

## Prerequisites

- Understanding of HTTP requests
- Basic Frappe knowledge
- Access to Integration Request list

## Step-by-Step Guide

### Step 1: Understanding Integration Request

Integration Request is a built-in DocType that logs HTTP requests and responses for integration debugging:

```python
import frappe

# View Integration Request structure
fields = frappe.get_meta("Integration Request").fields
for f in fields:
    print(f"{f.fieldname}: {f.fieldtype}")
```

Key fields:
- `integration_type`: Type of integration (e.g., "Remote", "Webhook")
- `integration_request_service`: Service name
- `status`: Queued, Completed, Failed, etc.
- `data`: Request payload
- `output`: Response data
- `error`: Error message if failed

### Step 2: Create Integration Request Logs

```python
import frappe
import requests
import json

def make_logged_request(service: str, url: str, method: str = "GET", data: dict = None, headers: dict = None):
    """Make HTTP request with Integration Request logging."""

    # Create Integration Request
    integration_request = frappe.new_doc("Integration Request")
    integration_request.integration_type = "Remote"
    integration_request.integration_request_service = service
    integration_request.status = "Queued"
    integration_request.url = url
    integration_request.request_headers = json.dumps(headers or {})
    integration_request.data = json.dumps(data or {})
    integration_request.insert(ignore_permissions=True)
    frappe.db.commit()

    try:
        # Make the request
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=data, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")

        # Update with success
        integration_request.handle_success(response.text)
        integration_request.status = "Completed"
        integration_request.response_code = response.status_code

    except Exception as e:
        # Update with failure
        integration_request.handle_failure(str(e))
        integration_request.status = "Failed"

    integration_request.save(ignore_permissions=True)
    frappe.db.commit()

    return integration_request

# Usage
result = make_logged_request(
    service="External API",
    url="https://api.example.com/data",
    method="POST",
    data={"key": "value"},
    headers={"Authorization": "Bearer token123"}
)
print(f"Request logged: {result.name}, Status: {result.status}")
```

### Step 3: Query Integration Requests

```python
def get_integration_requests(
    service: str = None,
    status: str = None,
    from_date: str = None,
    limit: int = 20
) -> list:
    """Query integration request logs."""

    filters = {}
    if service:
        filters["integration_request_service"] = service
    if status:
        filters["status"] = status
    if from_date:
        filters["creation"] = (">=", from_date)

    return frappe.get_all(
        "Integration Request",
        filters=filters,
        fields=[
            "name", "integration_request_service", "status",
            "creation", "url", "error"
        ],
        order_by="creation desc",
        limit_page_length=limit
    )

# Get failed requests from last 24 hours
from datetime import datetime, timedelta
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

failed_requests = get_integration_requests(
    status="Failed",
    from_date=yesterday
)

for req in failed_requests:
    print(f"{req.creation}: {req.integration_request_service} - {req.error}")
```

### Step 4: Retry Failed Requests

```python
def retry_failed_request(integration_request_name: str) -> dict:
    """Retry a failed integration request."""
    import json
    import requests

    ir = frappe.get_doc("Integration Request", integration_request_name)

    if ir.status != "Failed":
        return {"error": "Only failed requests can be retried"}

    try:
        # Reconstruct request
        headers = json.loads(ir.request_headers or "{}")
        data = json.loads(ir.data or "{}")

        # Make the request again
        response = requests.post(
            ir.url,
            headers=headers,
            json=data,
            timeout=30
        )

        # Update status
        ir.handle_success(response.text)
        ir.status = "Completed"
        ir.error = None

    except Exception as e:
        ir.error = str(e)
        ir.status = "Failed"

    ir.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "name": ir.name,
        "status": ir.status,
        "output": ir.output if ir.status == "Completed" else None,
        "error": ir.error
    }

# Retry a specific request
result = retry_failed_request("INT-REQ-00001")
```

### Step 5: Clean Up Old Logs

```python
def cleanup_old_integration_requests(days: int = 30):
    """Delete integration requests older than specified days."""
    from frappe.integrations.doctype.integration_request.integration_request import IntegrationRequest

    # Use built-in method
    IntegrationRequest.clear_old_logs(days=days)

    # Or manual cleanup
    from datetime import datetime, timedelta
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    old_requests = frappe.get_all(
        "Integration Request",
        filters={"creation": ("<", cutoff_date)},
        pluck="name"
    )

    for name in old_requests:
        frappe.delete_doc("Integration Request", name, force=True)

    frappe.db.commit()
    return len(old_requests)

# Clean up requests older than 7 days
deleted_count = cleanup_old_integration_requests(days=7)
print(f"Deleted {deleted_count} old integration requests")
```

## Complete Example: Integration Request Wrapper

```python
import frappe
import requests
import json
from typing import Optional, Dict, Any
from functools import wraps

class IntegrationLogger:
    """Wrapper class for logging HTTP integrations."""

    def __init__(self, service_name: str):
        self.service_name = service_name

    def _create_request(self, url: str, method: str, data: dict, headers: dict) -> 'frappe._dict':
        """Create Integration Request document."""
        ir = frappe.new_doc("Integration Request")
        ir.integration_type = "Remote"
        ir.integration_request_service = self.service_name
        ir.status = "Queued"
        ir.url = url
        ir.request_headers = json.dumps(headers or {})
        ir.data = json.dumps(data or {})
        ir.insert(ignore_permissions=True)
        frappe.db.commit()
        return ir

    def request(
        self,
        method: str,
        url: str,
        data: dict = None,
        headers: dict = None,
        timeout: int = 30,
        raise_on_error: bool = True
    ) -> Dict[str, Any]:
        """Make HTTP request with automatic logging."""

        ir = self._create_request(url, method, data, headers)

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data if method.upper() in ["POST", "PUT", "PATCH"] else None,
                params=data if method.upper() == "GET" else None,
                timeout=timeout
            )

            # Check for HTTP errors
            response.raise_for_status()

            # Success
            ir.status = "Completed"
            ir.output = response.text[:65000]  # Truncate if too long
            ir.error = None

            result = {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.text else None,
                "integration_request": ir.name
            }

        except requests.exceptions.HTTPError as e:
            ir.status = "Failed"
            ir.error = f"HTTP {e.response.status_code}: {e.response.text[:1000]}"
            ir.output = e.response.text[:65000]

            result = {
                "success": False,
                "status_code": e.response.status_code,
                "error": str(e),
                "integration_request": ir.name
            }

            if raise_on_error:
                ir.save(ignore_permissions=True)
                frappe.db.commit()
                raise

        except Exception as e:
            ir.status = "Failed"
            ir.error = str(e)

            result = {
                "success": False,
                "error": str(e),
                "integration_request": ir.name
            }

            if raise_on_error:
                ir.save(ignore_permissions=True)
                frappe.db.commit()
                raise

        ir.save(ignore_permissions=True)
        frappe.db.commit()

        return result

    def get(self, url: str, params: dict = None, **kwargs):
        return self.request("GET", url, data=params, **kwargs)

    def post(self, url: str, data: dict = None, **kwargs):
        return self.request("POST", url, data=data, **kwargs)

    def put(self, url: str, data: dict = None, **kwargs):
        return self.request("PUT", url, data=data, **kwargs)

    def delete(self, url: str, **kwargs):
        return self.request("DELETE", url, **kwargs)

# Usage
api = IntegrationLogger("Payment Gateway")

# Make logged requests
result = api.post(
    url="https://api.payment.com/charge",
    data={"amount": 1000, "currency": "USD"},
    headers={"Authorization": "Bearer sk_test_123"},
    raise_on_error=False  # Don't raise, check result instead
)

if result["success"]:
    print(f"Payment successful: {result['data']}")
else:
    print(f"Payment failed: {result['error']}")
    print(f"See Integration Request: {result['integration_request']}")
```

## Monitoring Dashboard

```python
def get_integration_dashboard(days: int = 7) -> dict:
    """Get integration request statistics for dashboard."""
    from datetime import datetime, timedelta

    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Total by status
    status_counts = frappe.db.sql("""
        SELECT status, COUNT(*) as count
        FROM `tabIntegration Request`
        WHERE creation >= %s
        GROUP BY status
    """, [start_date], as_dict=True)

    # By service
    service_counts = frappe.db.sql("""
        SELECT
            integration_request_service as service,
            COUNT(*) as total,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) as failed
        FROM `tabIntegration Request`
        WHERE creation >= %s
        GROUP BY integration_request_service
    """, [start_date], as_dict=True)

    # Failure rate
    total = sum(s.count for s in status_counts)
    failed = sum(s.count for s in status_counts if s.status == "Failed")
    failure_rate = (failed / total * 100) if total > 0 else 0

    return {
        "period_days": days,
        "total_requests": total,
        "by_status": {s.status: s.count for s in status_counts},
        "by_service": service_counts,
        "failure_rate": round(failure_rate, 2)
    }

# Get dashboard data
dashboard = get_integration_dashboard(days=7)
print(f"Total requests: {dashboard['total_requests']}")
print(f"Failure rate: {dashboard['failure_rate']}%")
```

## Troubleshooting

### Missing Requests
- Ensure Integration Request is inserted before API call
- Check if old logs were cleaned up

### Large Payloads Truncated
- Output field has character limit
- Consider storing in File or separate table

### Performance Issues
- Set up scheduled cleanup job
- Index frequently queried fields

## Next Steps

- [Error Handling in Integrations](../error-handling-integrations/error-handling-integrations.md)
- [Rate Limiting and Retry Logic](../rate-limiting-retry-logic/rate-limiting-retry-logic.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
