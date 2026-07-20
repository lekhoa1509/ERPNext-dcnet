# How To: Rate Limiting and Retry Logic

**Difficulty**: Intermediate
**Estimated Time**: 25 minutes
**Tags**: rate-limiting, retry, backoff, throttling, resilience

## Overview

Learn how to implement rate limiting and retry logic for integrations to handle API throttling, transient failures, and ensure reliable data synchronization.

## Prerequisites

- Understanding of HTTP status codes
- Basic Python async/threading
- Frappe background jobs knowledge

## Step-by-Step Guide

### Step 1: Simple Retry with Exponential Backoff

```python
import time
import random
from functools import wraps
from typing import Callable, Any

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: tuple = (Exception,)
):
    """Decorator for retry with exponential backoff."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        raise

                    # Calculate delay
                    delay = min(base_delay * (exponential_base ** attempt), max_delay)

                    # Add jitter to prevent thundering herd
                    if jitter:
                        delay = delay * (0.5 + random.random())

                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s")
                    time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator

# Usage
import requests

@retry_with_backoff(
    max_retries=3,
    base_delay=1.0,
    retryable_exceptions=(requests.exceptions.RequestException,)
)
def call_external_api(url: str, data: dict):
    response = requests.post(url, json=data, timeout=30)
    response.raise_for_status()
    return response.json()
```

### Step 2: Rate Limiter Implementation

```python
import frappe
import time
from datetime import datetime, timedelta
from typing import Optional

class RateLimiter:
    """Token bucket rate limiter using Redis cache."""

    def __init__(
        self,
        key: str,
        rate: int,
        per_seconds: int = 1,
        burst: int = None
    ):
        """
        Args:
            key: Unique identifier for this rate limit
            rate: Number of requests allowed
            per_seconds: Time window in seconds
            burst: Maximum burst size (defaults to rate)
        """
        self.key = f"rate_limit:{key}"
        self.rate = rate
        self.per_seconds = per_seconds
        self.burst = burst or rate

    def _get_tokens(self) -> dict:
        """Get current token state from cache."""
        state = frappe.cache().get(self.key)
        if not state:
            state = {
                "tokens": float(self.burst),
                "last_update": time.time()
            }
        return state

    def _save_tokens(self, state: dict):
        """Save token state to cache."""
        frappe.cache().set(self.key, state, expires_in_sec=self.per_seconds * 2)

    def acquire(self, tokens: int = 1) -> bool:
        """
        Try to acquire tokens.
        Returns True if successful, False if rate limited.
        """
        state = self._get_tokens()
        now = time.time()

        # Refill tokens based on time passed
        time_passed = now - state["last_update"]
        refill_rate = self.rate / self.per_seconds
        state["tokens"] = min(self.burst, state["tokens"] + time_passed * refill_rate)
        state["last_update"] = now

        # Try to consume tokens
        if state["tokens"] >= tokens:
            state["tokens"] -= tokens
            self._save_tokens(state)
            return True

        self._save_tokens(state)
        return False

    def wait_time(self) -> float:
        """Calculate time to wait until tokens available."""
        state = self._get_tokens()
        if state["tokens"] >= 1:
            return 0

        tokens_needed = 1 - state["tokens"]
        refill_rate = self.rate / self.per_seconds
        return tokens_needed / refill_rate

    def wait_and_acquire(self, tokens: int = 1, max_wait: float = 60) -> bool:
        """Wait for tokens to become available, then acquire."""
        wait = self.wait_time()

        if wait > max_wait:
            return False

        if wait > 0:
            time.sleep(wait)

        return self.acquire(tokens)

# Usage
api_limiter = RateLimiter(
    key="external_api",
    rate=100,  # 100 requests
    per_seconds=60  # per minute
)

def make_api_call(url: str, data: dict):
    if not api_limiter.acquire():
        wait_time = api_limiter.wait_time()
        raise Exception(f"Rate limited. Try again in {wait_time:.2f}s")

    # Make the actual call
    response = requests.post(url, json=data)
    return response.json()
```

### Step 3: Sliding Window Rate Limiter

```python
import frappe
import time

class SlidingWindowRateLimiter:
    """Sliding window rate limiter for more precise rate limiting."""

    def __init__(self, key: str, max_requests: int, window_seconds: int):
        self.key = f"sliding_rate:{key}"
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def acquire(self) -> bool:
        """Try to acquire a request slot."""
        now = time.time()
        window_start = now - self.window_seconds

        # Get current request timestamps
        timestamps = frappe.cache().get(self.key) or []

        # Remove old timestamps
        timestamps = [ts for ts in timestamps if ts > window_start]

        # Check if under limit
        if len(timestamps) >= self.max_requests:
            return False

        # Add current timestamp
        timestamps.append(now)
        frappe.cache().set(self.key, timestamps, expires_in_sec=self.window_seconds + 10)

        return True

    def remaining(self) -> int:
        """Get remaining requests in current window."""
        now = time.time()
        window_start = now - self.window_seconds

        timestamps = frappe.cache().get(self.key) or []
        timestamps = [ts for ts in timestamps if ts > window_start]

        return max(0, self.max_requests - len(timestamps))

    def reset_time(self) -> float:
        """Get time until oldest request expires."""
        now = time.time()
        window_start = now - self.window_seconds

        timestamps = frappe.cache().get(self.key) or []
        timestamps = [ts for ts in timestamps if ts > window_start]

        if not timestamps:
            return 0

        oldest = min(timestamps)
        return max(0, oldest - window_start)
```

### Step 4: Retry with Rate Limit Awareness

```python
import requests
import time
from typing import Dict, Any

class RateLimitAwareClient:
    """HTTP client that respects rate limits."""

    def __init__(
        self,
        base_url: str,
        rate_limiter: RateLimiter,
        max_retries: int = 3
    ):
        self.base_url = base_url.rstrip('/')
        self.rate_limiter = rate_limiter
        self.max_retries = max_retries
        self.session = requests.Session()

    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make rate-limited request with retry."""

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        last_exception = None

        for attempt in range(self.max_retries + 1):
            # Wait for rate limit
            if not self.rate_limiter.wait_and_acquire(max_wait=60):
                return {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "code": "RATE_LIMIT"
                }

            try:
                response = self.session.request(method, url, **kwargs)

                # Check for rate limit response from server
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    print(f"Server rate limited. Waiting {retry_after}s")
                    time.sleep(retry_after)
                    continue

                response.raise_for_status()

                return {
                    "success": True,
                    "data": response.json() if response.text else None,
                    "headers": dict(response.headers)
                }

            except requests.exceptions.RequestException as e:
                last_exception = e

                if attempt < self.max_retries:
                    delay = 2 ** attempt
                    print(f"Request failed: {e}. Retrying in {delay}s")
                    time.sleep(delay)
                    continue

                return {
                    "success": False,
                    "error": str(e),
                    "code": "REQUEST_FAILED"
                }

        return {
            "success": False,
            "error": str(last_exception),
            "code": "MAX_RETRIES"
        }
```

### Step 5: Batch Processing with Rate Limiting

```python
import frappe
from typing import List, Dict, Any, Callable
import time

class BatchProcessor:
    """Process items in batches with rate limiting."""

    def __init__(
        self,
        rate_limiter: RateLimiter,
        batch_size: int = 10,
        delay_between_batches: float = 1.0
    ):
        self.rate_limiter = rate_limiter
        self.batch_size = batch_size
        self.delay_between_batches = delay_between_batches

    def process(
        self,
        items: List[Any],
        processor: Callable[[Any], Dict],
        on_error: Callable[[Any, Exception], None] = None
    ) -> Dict[str, Any]:
        """Process items in rate-limited batches."""

        results = {
            "total": len(items),
            "processed": 0,
            "succeeded": 0,
            "failed": 0,
            "errors": []
        }

        # Split into batches
        batches = [items[i:i + self.batch_size] for i in range(0, len(items), self.batch_size)]

        for batch_num, batch in enumerate(batches):
            print(f"Processing batch {batch_num + 1}/{len(batches)}")

            for item in batch:
                # Wait for rate limit
                self.rate_limiter.wait_and_acquire()

                try:
                    result = processor(item)
                    results["processed"] += 1

                    if result.get("success"):
                        results["succeeded"] += 1
                    else:
                        results["failed"] += 1
                        results["errors"].append({
                            "item": str(item),
                            "error": result.get("error")
                        })

                except Exception as e:
                    results["processed"] += 1
                    results["failed"] += 1
                    results["errors"].append({
                        "item": str(item),
                        "error": str(e)
                    })

                    if on_error:
                        on_error(item, e)

            # Delay between batches
            if batch_num < len(batches) - 1:
                time.sleep(self.delay_between_batches)

        return results

# Usage
def sync_customers_to_external():
    """Sync customers with rate limiting."""

    rate_limiter = RateLimiter(
        key="customer_sync",
        rate=30,  # 30 requests per minute
        per_seconds=60
    )

    processor = BatchProcessor(
        rate_limiter=rate_limiter,
        batch_size=10,
        delay_between_batches=2.0
    )

    customers = frappe.get_all("Customer", fields=["name", "customer_name", "email_id"])

    def sync_customer(customer):
        # API call to sync customer
        response = requests.post(
            "https://api.external.com/customers",
            json={"name": customer["customer_name"], "email": customer["email_id"]}
        )
        response.raise_for_status()
        return {"success": True}

    results = processor.process(customers, sync_customer)
    print(f"Synced {results['succeeded']}/{results['total']} customers")
    return results
```

## Complete Example: Resilient Integration Service

```python
import frappe
import requests
import time
from typing import Dict, Any, Optional, List
from functools import wraps

class IntegrationService:
    """Complete integration service with rate limiting and retry."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        service_name: str,
        requests_per_minute: int = 60,
        max_retries: int = 3
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.service_name = service_name
        self.max_retries = max_retries
        self.session = requests.Session()

        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            key=service_name,
            rate=requests_per_minute,
            per_seconds=60,
            burst=min(requests_per_minute, 10)  # Allow small burst
        )

        # Track consecutive failures for circuit breaker
        self.consecutive_failures = 0
        self.circuit_open_until = None

    def _is_circuit_open(self) -> bool:
        """Check if circuit breaker is open."""
        if self.circuit_open_until:
            if time.time() < self.circuit_open_until:
                return True
            # Reset circuit
            self.circuit_open_until = None
            self.consecutive_failures = 0
        return False

    def _record_success(self):
        """Record successful request."""
        self.consecutive_failures = 0

    def _record_failure(self):
        """Record failed request and possibly open circuit."""
        self.consecutive_failures += 1
        if self.consecutive_failures >= 5:
            # Open circuit for 60 seconds
            self.circuit_open_until = time.time() + 60
            frappe.log_error(
                title=f"Circuit Breaker Open: {self.service_name}",
                message=f"Service failed {self.consecutive_failures} times consecutively"
            )

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Make rate-limited, retriable request."""

        # Check circuit breaker
        if self._is_circuit_open():
            return {
                "success": False,
                "error": "Service temporarily unavailable",
                "code": "CIRCUIT_OPEN",
                "retry_after": self.circuit_open_until - time.time()
            }

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        last_error = None

        for attempt in range(self.max_retries + 1):
            # Wait for rate limit
            wait_time = self.rate_limiter.wait_time()
            if wait_time > 0:
                time.sleep(wait_time)

            if not self.rate_limiter.acquire():
                return {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "code": "RATE_LIMITED"
                }

            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data if method in ["POST", "PUT", "PATCH"] else None,
                    params=params,
                    headers=self._get_headers(),
                    timeout=timeout
                )

                # Handle rate limit from server
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    if attempt < self.max_retries:
                        time.sleep(retry_after)
                        continue
                    return {
                        "success": False,
                        "error": "Rate limited by server",
                        "code": "SERVER_RATE_LIMIT",
                        "retry_after": retry_after
                    }

                response.raise_for_status()
                self._record_success()

                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json() if response.text else None
                }

            except requests.exceptions.Timeout:
                last_error = "Request timeout"
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue

            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection error: {e}"
                self._record_failure()
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue

            except requests.exceptions.HTTPError as e:
                status = e.response.status_code
                # Don't retry client errors (4xx except 429)
                if 400 <= status < 500 and status != 429:
                    return {
                        "success": False,
                        "error": e.response.text,
                        "code": f"HTTP_{status}"
                    }
                last_error = str(e)
                self._record_failure()
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                    continue

        return {
            "success": False,
            "error": last_error,
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

    def bulk_operation(
        self,
        items: List[Any],
        operation: str,
        endpoint_template: str,
        batch_size: int = 10
    ) -> Dict[str, Any]:
        """Perform bulk operations with rate limiting."""

        results = {"total": len(items), "succeeded": 0, "failed": 0, "errors": []}

        for i, item in enumerate(items):
            endpoint = endpoint_template.format(**item) if isinstance(item, dict) else endpoint_template

            if operation == "POST":
                result = self.post(endpoint, data=item)
            elif operation == "PUT":
                result = self.put(endpoint, data=item)
            elif operation == "DELETE":
                result = self.delete(endpoint)
            else:
                result = self.get(endpoint)

            if result["success"]:
                results["succeeded"] += 1
            else:
                results["failed"] += 1
                results["errors"].append({"item": str(item), "error": result["error"]})

            # Progress logging
            if (i + 1) % batch_size == 0:
                print(f"Progress: {i + 1}/{len(items)}")

        return results

# Usage
service = IntegrationService(
    base_url="https://api.service.com/v1",
    api_key="sk_live_xxx",
    service_name="payment_service",
    requests_per_minute=60,
    max_retries=3
)

# Single request
result = service.post("/payments", data={"amount": 100})

# Bulk operation
customers = [{"id": 1}, {"id": 2}, {"id": 3}]
bulk_result = service.bulk_operation(
    items=customers,
    operation="GET",
    endpoint_template="/customers/{id}"
)
```

## Troubleshooting

### Rate Limiting Not Working
- Verify Redis cache is running
- Check rate limiter key uniqueness
- Confirm rate values are correct

### Requests Still Failing
- Increase retry count or delay
- Check circuit breaker state
- Review server-side limits

## Next Steps

- [Error Handling in Integrations](../error-handling-integrations/error-handling-integrations.md)
- [REST API Integration Patterns](../rest-api-integration-patterns/rest-api-integration-patterns.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
