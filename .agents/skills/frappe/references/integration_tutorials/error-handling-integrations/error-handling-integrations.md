# How To: Error Handling in Integrations

**Difficulty**: Intermediate
**Estimated Time**: 25 minutes
**Tags**: error-handling, exceptions, logging, debugging, resilience

## Overview

Learn how to properly handle errors in Frappe integrations, including HTTP errors, validation errors, and integration failures with proper logging and recovery.

## Prerequisites

- Basic Python exception handling
- Understanding of HTTP status codes
- Frappe development knowledge

## Step-by-Step Guide

### Step 1: Define Custom Exceptions

```python
import frappe

class IntegrationError(Exception):
    """Base exception for integration errors."""

    def __init__(self, message: str, code: str = None, details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

class APIConnectionError(IntegrationError):
    """Failed to connect to external API."""
    pass

class APIAuthenticationError(IntegrationError):
    """Authentication failed with external API."""
    pass

class APIRateLimitError(IntegrationError):
    """Rate limit exceeded."""
    def __init__(self, message: str, retry_after: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after

class APIValidationError(IntegrationError):
    """Validation error from external API."""
    pass

class DataMappingError(IntegrationError):
    """Error mapping data between systems."""
    pass
```

### Step 2: HTTP Error Handler

```python
import requests
from typing import Dict, Any, Optional

def handle_http_response(response: requests.Response) -> Dict[str, Any]:
    """Handle HTTP response and raise appropriate exceptions."""

    try:
        response.raise_for_status()
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json() if response.text else None
        }

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_body = {}

        try:
            error_body = e.response.json()
        except:
            error_body = {"raw": e.response.text[:500]}

        # Map HTTP status to appropriate exception
        if status_code == 401:
            raise APIAuthenticationError(
                message="Authentication failed",
                code="AUTH_FAILED",
                details=error_body
            )
        elif status_code == 403:
            raise APIAuthenticationError(
                message="Permission denied",
                code="FORBIDDEN",
                details=error_body
            )
        elif status_code == 429:
            retry_after = int(e.response.headers.get("Retry-After", 60))
            raise APIRateLimitError(
                message="Rate limit exceeded",
                code="RATE_LIMIT",
                retry_after=retry_after,
                details=error_body
            )
        elif status_code == 400:
            raise APIValidationError(
                message="Validation error",
                code="VALIDATION_ERROR",
                details=error_body
            )
        elif status_code == 404:
            raise IntegrationError(
                message="Resource not found",
                code="NOT_FOUND",
                details=error_body
            )
        elif status_code >= 500:
            raise APIConnectionError(
                message=f"Server error: {status_code}",
                code="SERVER_ERROR",
                details=error_body
            )
        else:
            raise IntegrationError(
                message=f"HTTP error: {status_code}",
                code=f"HTTP_{status_code}",
                details=error_body
            )
```

### Step 3: Comprehensive Error Logging

```python
import frappe
import traceback
from datetime import datetime

def log_integration_error(
    service: str,
    error: Exception,
    request_data: dict = None,
    context: dict = None
):
    """Log integration error with full context."""

    error_info = {
        "service": service,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "timestamp": datetime.now().isoformat(),
        "user": frappe.session.user,
        "context": context or {}
    }

    # Add details for custom exceptions
    if isinstance(error, IntegrationError):
        error_info["code"] = error.code
        error_info["details"] = error.details

    # Add request data (sanitized)
    if request_data:
        sanitized_data = sanitize_sensitive_data(request_data)
        error_info["request"] = sanitized_data

    # Add traceback
    error_info["traceback"] = traceback.format_exc()

    # Log to Frappe Error Log
    frappe.log_error(
        title=f"Integration Error: {service}",
        message=frappe.as_json(error_info, indent=2)
    )

    # Also log to Integration Request if available
    try:
        create_failed_integration_request(service, error_info, request_data)
    except:
        pass

    return error_info

def sanitize_sensitive_data(data: dict) -> dict:
    """Remove sensitive data before logging."""
    sensitive_keys = [
        "password", "secret", "token", "api_key", "authorization",
        "client_secret", "access_token", "refresh_token"
    ]

    if not isinstance(data, dict):
        return data

    sanitized = {}
    for key, value in data.items():
        if any(s in key.lower() for s in sensitive_keys):
            sanitized[key] = "***REDACTED***"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_sensitive_data(value)
        else:
            sanitized[key] = value

    return sanitized

def create_failed_integration_request(service: str, error_info: dict, request_data: dict):
    """Create Integration Request for failed request."""
    import json

    ir = frappe.new_doc("Integration Request")
    ir.integration_type = "Remote"
    ir.integration_request_service = service
    ir.status = "Failed"
    ir.data = json.dumps(request_data) if request_data else ""
    ir.error = json.dumps(error_info)
    ir.insert(ignore_permissions=True)
    frappe.db.commit()
```

### Step 4: Error Recovery Patterns

```python
import frappe
from functools import wraps
import time

def with_error_handling(service_name: str):
    """Decorator for consistent error handling."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except APIRateLimitError as e:
                log_integration_error(service_name, e, context={"recoverable": True})
                # Return structured error for retry
                return {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "retry_after": e.retry_after,
                    "recoverable": True
                }
            except APIAuthenticationError as e:
                log_integration_error(service_name, e)
                frappe.throw(f"Authentication failed with {service_name}. Please check credentials.")
            except APIValidationError as e:
                log_integration_error(service_name, e)
                return {
                    "success": False,
                    "error": "Validation error",
                    "details": e.details,
                    "recoverable": False
                }
            except IntegrationError as e:
                log_integration_error(service_name, e)
                return {
                    "success": False,
                    "error": str(e),
                    "code": e.code
                }
            except Exception as e:
                log_integration_error(service_name, e)
                return {
                    "success": False,
                    "error": "Unexpected error",
                    "details": str(e)
                }
        return wrapper
    return decorator

# Usage
class PaymentGateway:
    @with_error_handling("Payment Gateway")
    def charge(self, amount: float, token: str):
        # Implementation
        pass
```

### Step 5: Circuit Breaker Pattern

```python
import frappe
from datetime import datetime, timedelta

class CircuitBreaker:
    """Circuit breaker to prevent repeated failures."""

    def __init__(
        self,
        service_name: str,
        failure_threshold: int = 5,
        reset_timeout: int = 60
    ):
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.cache_key = f"circuit_breaker:{service_name}"

    def _get_state(self) -> dict:
        """Get current circuit state from cache."""
        state = frappe.cache().get(self.cache_key)
        if not state:
            state = {
                "failures": 0,
                "last_failure": None,
                "state": "closed"  # closed, open, half-open
            }
        return state

    def _set_state(self, state: dict):
        """Save circuit state to cache."""
        frappe.cache().set(self.cache_key, state, expires_in_sec=self.reset_timeout * 2)

    def is_open(self) -> bool:
        """Check if circuit is open (failing)."""
        state = self._get_state()

        if state["state"] == "open":
            # Check if timeout has passed
            if state["last_failure"]:
                elapsed = (datetime.now() - datetime.fromisoformat(state["last_failure"])).seconds
                if elapsed >= self.reset_timeout:
                    # Move to half-open
                    state["state"] = "half-open"
                    self._set_state(state)
                    return False
            return True

        return False

    def record_success(self):
        """Record successful call."""
        state = self._get_state()
        state["failures"] = 0
        state["state"] = "closed"
        self._set_state(state)

    def record_failure(self):
        """Record failed call."""
        state = self._get_state()
        state["failures"] += 1
        state["last_failure"] = datetime.now().isoformat()

        if state["failures"] >= self.failure_threshold:
            state["state"] = "open"
            frappe.log_error(
                title=f"Circuit Breaker OPEN: {self.service_name}",
                message=f"Service {self.service_name} has failed {state['failures']} times"
            )

        self._set_state(state)

def with_circuit_breaker(service_name: str, failure_threshold: int = 5, reset_timeout: int = 60):
    """Decorator to add circuit breaker to integration."""
    circuit = CircuitBreaker(service_name, failure_threshold, reset_timeout)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if circuit.is_open():
                raise IntegrationError(
                    message=f"Service {service_name} is temporarily unavailable",
                    code="CIRCUIT_OPEN"
                )

            try:
                result = func(*args, **kwargs)
                circuit.record_success()
                return result
            except Exception as e:
                circuit.record_failure()
                raise

        return wrapper
    return decorator
```

## Complete Example: Resilient API Client

```python
import frappe
import requests
from typing import Dict, Any, Optional
from functools import wraps
import time

class ResilientAPIClient:
    """API client with comprehensive error handling."""

    def __init__(
        self,
        base_url: str,
        service_name: str,
        api_key: str = None,
        max_retries: int = 3,
        timeout: int = 30
    ):
        self.base_url = base_url.rstrip('/')
        self.service_name = service_name
        self.api_key = api_key
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()
        self.circuit = CircuitBreaker(service_name)

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _should_retry(self, exception: Exception) -> bool:
        """Determine if request should be retried."""
        # Retry on connection errors and rate limits
        if isinstance(exception, APIConnectionError):
            return True
        if isinstance(exception, APIRateLimitError):
            return True
        if isinstance(exception, requests.exceptions.ConnectionError):
            return True
        if isinstance(exception, requests.exceptions.Timeout):
            return True
        return False

    def _get_retry_delay(self, attempt: int, exception: Exception) -> float:
        """Calculate retry delay with exponential backoff."""
        if isinstance(exception, APIRateLimitError) and exception.retry_after:
            return exception.retry_after

        # Exponential backoff: 1s, 2s, 4s, etc.
        return min(2 ** attempt, 30)  # Max 30 seconds

    def request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        headers: dict = None
    ) -> Dict[str, Any]:
        """Make HTTP request with retry and circuit breaker."""

        # Check circuit breaker
        if self.circuit.is_open():
            return {
                "success": False,
                "error": "Service temporarily unavailable",
                "code": "CIRCUIT_OPEN"
            }

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {**self._get_headers(), **(headers or {})}
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data if method in ["POST", "PUT", "PATCH"] else None,
                    params=params,
                    headers=request_headers,
                    timeout=self.timeout
                )

                result = handle_http_response(response)
                self.circuit.record_success()
                return result

            except Exception as e:
                last_exception = e

                # Log the error
                log_integration_error(
                    self.service_name,
                    e,
                    request_data={"url": url, "method": method, "data": data},
                    context={"attempt": attempt + 1}
                )

                # Should we retry?
                if attempt < self.max_retries and self._should_retry(e):
                    delay = self._get_retry_delay(attempt, e)
                    frappe.log(f"Retrying {self.service_name} in {delay}s (attempt {attempt + 2})")
                    time.sleep(delay)
                    continue

                # Record failure in circuit breaker
                self.circuit.record_failure()

                # Return error response
                if isinstance(e, IntegrationError):
                    return {
                        "success": False,
                        "error": e.message,
                        "code": e.code,
                        "details": e.details
                    }
                else:
                    return {
                        "success": False,
                        "error": str(e),
                        "code": "UNKNOWN_ERROR"
                    }

        # All retries failed
        return {
            "success": False,
            "error": str(last_exception),
            "code": "MAX_RETRIES_EXCEEDED"
        }

    def get(self, endpoint: str, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, data: dict = None, **kwargs):
        return self.request("POST", endpoint, data=data, **kwargs)

    def put(self, endpoint: str, data: dict = None, **kwargs):
        return self.request("PUT", endpoint, data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)

# Usage
client = ResilientAPIClient(
    base_url="https://api.service.com/v1",
    service_name="Payment Service",
    api_key="sk_live_xxx",
    max_retries=3
)

result = client.post("/payments", data={"amount": 100, "currency": "USD"})

if result["success"]:
    print(f"Payment successful: {result['data']}")
else:
    print(f"Payment failed: {result['error']} ({result.get('code')})")
```

## Error Response Standards

Return consistent error responses:

```python
def create_error_response(
    error: Exception,
    recoverable: bool = False,
    retry_after: int = None
) -> Dict[str, Any]:
    """Create standardized error response."""

    response = {
        "success": False,
        "error": str(error),
        "recoverable": recoverable
    }

    if isinstance(error, IntegrationError):
        response["code"] = error.code
        if error.details:
            response["details"] = error.details

    if retry_after:
        response["retry_after"] = retry_after

    return response
```

## Troubleshooting

### Error Not Logged
- Ensure exception is properly caught
- Check Error Log permissions
- Verify Integration Request is created

### Circuit Breaker Not Resetting
- Check cache is working
- Verify reset_timeout is reasonable
- Manual reset: `frappe.cache().delete("circuit_breaker:service")`

## Next Steps

- [Rate Limiting and Retry Logic](../rate-limiting-retry-logic/rate-limiting-retry-logic.md)
- [Integration Request Debugging](../integration-request-debugging/integration-request-debugging.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
