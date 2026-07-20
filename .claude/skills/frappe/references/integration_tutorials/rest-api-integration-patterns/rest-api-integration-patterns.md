# How To: REST API Integration Patterns

**Difficulty**: Intermediate
**Estimated Time**: 30 minutes
**Tags**: rest-api, integration, http, patterns, best-practices

## Overview

Learn best practices and patterns for integrating Frappe with external REST APIs, including authentication, error handling, and data mapping.

## Prerequisites

- Python HTTP library knowledge (requests)
- Understanding of REST APIs
- Basic Frappe development

## Step-by-Step Guide

### Step 1: Basic API Client Pattern

```python
import frappe
import requests
from typing import Optional, Dict, Any

class BaseAPIClient:
    """Base class for REST API integrations."""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _get_headers(self) -> Dict[str, str]:
        """Override in subclass to add authentication headers."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        headers: dict = None
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling."""

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {**self._get_headers(), **(headers or {})}

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if method in ["POST", "PUT", "PATCH"] else None,
                params=params,
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.text else None
            }

        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "status_code": e.response.status_code,
                "error": e.response.text
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get(self, endpoint: str, params: dict = None, **kwargs):
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: dict = None, **kwargs):
        return self._request("POST", endpoint, data=data, **kwargs)

    def put(self, endpoint: str, data: dict = None, **kwargs):
        return self._request("PUT", endpoint, data=data, **kwargs)

    def patch(self, endpoint: str, data: dict = None, **kwargs):
        return self._request("PATCH", endpoint, data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)
```

### Step 2: API Key Authentication Pattern

```python
class APIKeyClient(BaseAPIClient):
    """API client with API Key authentication."""

    def __init__(self, base_url: str, api_key: str, header_name: str = "X-API-Key"):
        super().__init__(base_url)
        self.api_key = api_key
        self.header_name = header_name

    def _get_headers(self) -> Dict[str, str]:
        headers = super()._get_headers()
        headers[self.header_name] = self.api_key
        return headers

# Usage
client = APIKeyClient(
    base_url="https://api.service.com/v1",
    api_key="sk_live_xxx",
    header_name="Authorization"  # Some APIs use "Bearer {key}"
)

result = client.get("/customers")
```

### Step 3: Bearer Token Authentication Pattern

```python
class BearerTokenClient(BaseAPIClient):
    """API client with Bearer token authentication."""

    def __init__(self, base_url: str, token: str):
        super().__init__(base_url)
        self.token = token

    def _get_headers(self) -> Dict[str, str]:
        headers = super()._get_headers()
        headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def set_token(self, token: str):
        """Update the bearer token."""
        self.token = token

# Usage with Connected App
def get_authenticated_client(connected_app_name: str, user: str = None):
    """Create API client with OAuth token from Connected App."""
    if not user:
        user = frappe.session.user

    app = frappe.get_doc("Connected App", connected_app_name)
    session = app.get_oauth2_session(user=user)

    # Get token from session
    token = session.token.get("access_token")

    return BearerTokenClient(
        base_url="https://api.service.com/v1",
        token=token
    )
```

### Step 4: Data Mapping Pattern

```python
class DataMapper:
    """Map between Frappe DocTypes and external API formats."""

    @staticmethod
    def customer_to_external(customer: dict) -> dict:
        """Map Frappe Customer to external API format."""
        return {
            "external_id": customer.get("name"),
            "name": customer.get("customer_name"),
            "email": customer.get("email_id"),
            "phone": customer.get("mobile_no"),
            "type": "company" if customer.get("customer_type") == "Company" else "individual",
            "tax_id": customer.get("tax_id"),
            "address": {
                "line1": customer.get("primary_address", {}).get("address_line1"),
                "city": customer.get("primary_address", {}).get("city"),
                "country": customer.get("primary_address", {}).get("country")
            }
        }

    @staticmethod
    def external_to_customer(external: dict) -> dict:
        """Map external API response to Frappe Customer format."""
        return {
            "doctype": "Customer",
            "customer_name": external.get("name"),
            "customer_type": "Company" if external.get("type") == "company" else "Individual",
            "email_id": external.get("email"),
            "mobile_no": external.get("phone"),
            "tax_id": external.get("tax_id")
        }

    @staticmethod
    def order_to_external(sales_order: dict) -> dict:
        """Map Frappe Sales Order to external API format."""
        items = []
        for item in sales_order.get("items", []):
            items.append({
                "sku": item.get("item_code"),
                "quantity": item.get("qty"),
                "price": item.get("rate"),
                "total": item.get("amount")
            })

        return {
            "order_id": sales_order.get("name"),
            "customer_id": sales_order.get("customer"),
            "order_date": sales_order.get("transaction_date"),
            "currency": sales_order.get("currency"),
            "items": items,
            "subtotal": sales_order.get("total"),
            "tax": sales_order.get("total_taxes_and_charges"),
            "total": sales_order.get("grand_total")
        }
```

### Step 5: Sync Pattern with Conflict Resolution

```python
import frappe
from datetime import datetime

class ExternalAPISync:
    """Sync data between Frappe and external API."""

    def __init__(self, client: BaseAPIClient, mapper: DataMapper):
        self.client = client
        self.mapper = mapper

    def sync_customers_to_external(self, modified_since: datetime = None) -> dict:
        """Push modified customers to external system."""

        filters = {"disabled": 0}
        if modified_since:
            filters["modified"] = (">=", modified_since)

        customers = frappe.get_all(
            "Customer",
            filters=filters,
            fields=["name", "customer_name", "email_id", "mobile_no",
                    "customer_type", "tax_id", "modified"]
        )

        results = {"created": 0, "updated": 0, "failed": 0, "errors": []}

        for customer in customers:
            # Get full customer data
            full_customer = frappe.get_doc("Customer", customer.name).as_dict()
            external_data = self.mapper.customer_to_external(full_customer)

            # Check if exists in external system
            existing = self.client.get(f"/customers/{customer.name}")

            if existing["success"]:
                # Update existing
                result = self.client.put(f"/customers/{customer.name}", data=external_data)
                if result["success"]:
                    results["updated"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append({"customer": customer.name, "error": result["error"]})
            else:
                # Create new
                result = self.client.post("/customers", data=external_data)
                if result["success"]:
                    results["created"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append({"customer": customer.name, "error": result["error"]})

        return results

    def sync_customers_from_external(self) -> dict:
        """Pull customers from external system."""

        result = self.client.get("/customers", params={"limit": 100})

        if not result["success"]:
            return {"error": result["error"]}

        external_customers = result["data"].get("customers", [])
        results = {"created": 0, "updated": 0, "skipped": 0}

        for ext_customer in external_customers:
            frappe_data = self.mapper.external_to_customer(ext_customer)
            external_id = ext_customer.get("id")

            # Check if exists in Frappe (by external_id custom field)
            existing = frappe.db.exists("Customer", {"external_id": external_id})

            if existing:
                # Compare modified dates for conflict resolution
                local_modified = frappe.db.get_value("Customer", existing, "modified")
                external_modified = ext_customer.get("updated_at")

                if external_modified and external_modified > str(local_modified):
                    # External is newer, update local
                    doc = frappe.get_doc("Customer", existing)
                    doc.update(frappe_data)
                    doc.save(ignore_permissions=True)
                    results["updated"] += 1
                else:
                    results["skipped"] += 1
            else:
                # Create new
                frappe_data["external_id"] = external_id
                doc = frappe.new_doc("Customer")
                doc.update(frappe_data)
                doc.insert(ignore_permissions=True)
                results["created"] += 1

        frappe.db.commit()
        return results
```

## Complete Example: E-commerce API Integration

```python
import frappe
import requests
from typing import Optional, Dict, Any, List

class EcommerceAPIClient:
    """Integration with external e-commerce platform."""

    def __init__(self, api_url: str, api_key: str, api_secret: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()

    def _get_auth_headers(self) -> Dict[str, str]:
        """Generate authentication headers."""
        import base64
        credentials = base64.b64encode(
            f"{self.api_key}:{self.api_secret}".encode()
        ).decode()

        return {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request."""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        headers = {**self._get_auth_headers(), **kwargs.pop("headers", {})}

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=30,
                **kwargs
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Product endpoints
    def get_products(self, page: int = 1, per_page: int = 50) -> Dict:
        return self._request("GET", "/products", params={"page": page, "per_page": per_page})

    def get_product(self, product_id: str) -> Dict:
        return self._request("GET", f"/products/{product_id}")

    def create_product(self, product_data: Dict) -> Dict:
        return self._request("POST", "/products", json=product_data)

    def update_product(self, product_id: str, product_data: Dict) -> Dict:
        return self._request("PUT", f"/products/{product_id}", json=product_data)

    def update_stock(self, product_id: str, quantity: int) -> Dict:
        return self._request("POST", f"/products/{product_id}/stock", json={"quantity": quantity})

    # Order endpoints
    def get_orders(self, status: str = None, since: str = None) -> Dict:
        params = {}
        if status:
            params["status"] = status
        if since:
            params["since"] = since
        return self._request("GET", "/orders", params=params)

    def get_order(self, order_id: str) -> Dict:
        return self._request("GET", f"/orders/{order_id}")

    def update_order_status(self, order_id: str, status: str) -> Dict:
        return self._request("PUT", f"/orders/{order_id}/status", json={"status": status})

    def fulfill_order(self, order_id: str, tracking: Dict) -> Dict:
        return self._request("POST", f"/orders/{order_id}/fulfill", json=tracking)


class EcommerceSync:
    """Sync between Frappe and e-commerce platform."""

    def __init__(self, client: EcommerceAPIClient):
        self.client = client

    def sync_products_to_platform(self) -> Dict:
        """Push Frappe items to e-commerce platform."""
        items = frappe.get_all(
            "Item",
            filters={"is_sales_item": 1, "disabled": 0},
            fields=["name", "item_name", "description", "standard_rate",
                    "stock_uom", "image", "item_group"]
        )

        results = {"synced": 0, "failed": 0}

        for item in items:
            product_data = {
                "sku": item.name,
                "name": item.item_name,
                "description": item.description or "",
                "price": item.standard_rate,
                "category": item.item_group
            }

            # Check if exists
            existing = self.client.get_product(item.name)

            if existing["success"]:
                result = self.client.update_product(item.name, product_data)
            else:
                result = self.client.create_product(product_data)

            if result["success"]:
                results["synced"] += 1
            else:
                results["failed"] += 1
                frappe.log_error(f"Failed to sync {item.name}: {result['error']}")

        return results

    def import_orders_from_platform(self) -> Dict:
        """Import new orders from e-commerce platform."""
        # Get orders since last sync
        last_sync = frappe.db.get_single_value("Ecommerce Settings", "last_order_sync")

        orders_result = self.client.get_orders(status="paid", since=last_sync)

        if not orders_result["success"]:
            return {"error": orders_result["error"]}

        orders = orders_result["data"].get("orders", [])
        results = {"imported": 0, "skipped": 0, "failed": 0}

        for order in orders:
            # Check if already imported
            if frappe.db.exists("Sales Order", {"ecommerce_order_id": order["id"]}):
                results["skipped"] += 1
                continue

            try:
                so = self._create_sales_order(order)
                results["imported"] += 1
            except Exception as e:
                results["failed"] += 1
                frappe.log_error(f"Failed to import order {order['id']}: {e}")

        # Update last sync time
        frappe.db.set_single_value("Ecommerce Settings", "last_order_sync",
                                    frappe.utils.now())
        frappe.db.commit()

        return results

    def _create_sales_order(self, order: Dict) -> str:
        """Create Sales Order from e-commerce order."""
        # Find or create customer
        customer = self._get_or_create_customer(order["customer"])

        so = frappe.new_doc("Sales Order")
        so.customer = customer
        so.ecommerce_order_id = order["id"]
        so.delivery_date = frappe.utils.add_days(frappe.utils.today(), 7)

        for item in order["line_items"]:
            so.append("items", {
                "item_code": item["sku"],
                "qty": item["quantity"],
                "rate": item["price"]
            })

        so.insert(ignore_permissions=True)
        so.submit()
        frappe.db.commit()

        return so.name

    def _get_or_create_customer(self, customer_data: Dict) -> str:
        """Get existing or create new customer."""
        email = customer_data.get("email")

        existing = frappe.db.exists("Customer", {"email_id": email})
        if existing:
            return existing

        customer = frappe.new_doc("Customer")
        customer.customer_name = customer_data.get("name")
        customer.customer_type = "Individual"
        customer.email_id = email
        customer.mobile_no = customer_data.get("phone")
        customer.insert(ignore_permissions=True)
        frappe.db.commit()

        return customer.name

# Usage
@frappe.whitelist()
def sync_ecommerce():
    """API endpoint to trigger sync."""
    settings = frappe.get_single("Ecommerce Settings")

    client = EcommerceAPIClient(
        api_url=settings.api_url,
        api_key=settings.api_key,
        api_secret=settings.get_password("api_secret")
    )

    sync = EcommerceSync(client)

    # Run syncs
    product_result = sync.sync_products_to_platform()
    order_result = sync.import_orders_from_platform()

    return {
        "products": product_result,
        "orders": order_result
    }
```

## Best Practices

1. **Use Configuration DocTypes**: Store API credentials in dedicated DocTypes
2. **Implement Retry Logic**: Handle transient failures gracefully
3. **Log All Requests**: Use Integration Request for debugging
4. **Map Data Properly**: Create clear mappings between systems
5. **Handle Pagination**: Process large datasets in chunks
6. **Use Background Jobs**: Run syncs asynchronously for large data

## Next Steps

- [Error Handling in Integrations](../error-handling-integrations/error-handling-integrations.md)
- [Rate Limiting and Retry Logic](../rate-limiting-retry-logic/rate-limiting-retry-logic.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
