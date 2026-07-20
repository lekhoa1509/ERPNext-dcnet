# How To: WooCommerce Integration

**Difficulty**: Advanced
**Estimated Time**: 45 minutes
**Tags**: woocommerce, ecommerce, sync, orders, products

## Overview

Learn how to integrate Frappe/ERPNext with WooCommerce for bi-directional synchronization of products, orders, customers, and inventory.

## Prerequisites

- WooCommerce store with REST API enabled
- WooCommerce API credentials (consumer key/secret)
- ERPNext setup with stock module

## Step-by-Step Guide

### Step 1: Create WooCommerce Settings DocType

```python
import frappe

def setup_woocommerce_settings():
    """Create settings DocType for WooCommerce configuration."""

    if frappe.db.exists("DocType", "WooCommerce Settings"):
        return

    doc = frappe.new_doc("DocType")
    doc.name = "WooCommerce Settings"
    doc.module = "Integrations"
    doc.issingle = 1
    doc.fields = [
        {"fieldname": "enabled", "fieldtype": "Check", "label": "Enabled"},
        {"fieldname": "woocommerce_url", "fieldtype": "Data", "label": "WooCommerce URL", "reqd": 1},
        {"fieldname": "consumer_key", "fieldtype": "Data", "label": "Consumer Key", "reqd": 1},
        {"fieldname": "consumer_secret", "fieldtype": "Password", "label": "Consumer Secret", "reqd": 1},
        {"fieldname": "sync_section", "fieldtype": "Section Break", "label": "Sync Settings"},
        {"fieldname": "sync_products", "fieldtype": "Check", "label": "Sync Products"},
        {"fieldname": "sync_orders", "fieldtype": "Check", "label": "Sync Orders"},
        {"fieldname": "sync_customers", "fieldtype": "Check", "label": "Sync Customers"},
        {"fieldname": "sync_inventory", "fieldtype": "Check", "label": "Sync Inventory"},
        {"fieldname": "default_warehouse", "fieldtype": "Link", "label": "Default Warehouse", "options": "Warehouse"},
        {"fieldname": "default_company", "fieldtype": "Link", "label": "Default Company", "options": "Company"},
        {"fieldname": "last_order_sync", "fieldtype": "Datetime", "label": "Last Order Sync", "read_only": 1}
    ]
    doc.insert()

setup_woocommerce_settings()
```

### Step 2: WooCommerce API Client

```python
import frappe
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, List, Optional

class WooCommerceClient:
    """Client for WooCommerce REST API."""

    def __init__(self):
        settings = frappe.get_single("WooCommerce Settings")
        self.base_url = settings.woocommerce_url.rstrip('/')
        self.consumer_key = settings.consumer_key
        self.consumer_secret = settings.get_password("consumer_secret")
        self.api_url = f"{self.base_url}/wp-json/wc/v3"

    def _request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None
    ) -> Dict[str, Any]:
        """Make authenticated request to WooCommerce API."""

        url = f"{self.api_url}/{endpoint.lstrip('/')}"

        try:
            response = requests.request(
                method=method,
                url=url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()

            # Get pagination info from headers
            total = response.headers.get("X-WP-Total")
            total_pages = response.headers.get("X-WP-TotalPages")

            return {
                "success": True,
                "data": response.json(),
                "total": int(total) if total else None,
                "total_pages": int(total_pages) if total_pages else None
            }

        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "error": e.response.text,
                "status_code": e.response.status_code
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # Product endpoints
    def get_products(self, page: int = 1, per_page: int = 100) -> Dict:
        return self._request("GET", "/products", params={"page": page, "per_page": per_page})

    def get_product(self, product_id: int) -> Dict:
        return self._request("GET", f"/products/{product_id}")

    def create_product(self, data: dict) -> Dict:
        return self._request("POST", "/products", data=data)

    def update_product(self, product_id: int, data: dict) -> Dict:
        return self._request("PUT", f"/products/{product_id}", data=data)

    def update_product_stock(self, product_id: int, quantity: int) -> Dict:
        return self._request("PUT", f"/products/{product_id}", data={
            "stock_quantity": quantity,
            "manage_stock": True
        })

    # Order endpoints
    def get_orders(self, status: str = None, after: str = None, page: int = 1, per_page: int = 100) -> Dict:
        params = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        if after:
            params["after"] = after
        return self._request("GET", "/orders", params=params)

    def get_order(self, order_id: int) -> Dict:
        return self._request("GET", f"/orders/{order_id}")

    def update_order_status(self, order_id: int, status: str) -> Dict:
        return self._request("PUT", f"/orders/{order_id}", data={"status": status})

    # Customer endpoints
    def get_customers(self, page: int = 1, per_page: int = 100) -> Dict:
        return self._request("GET", "/customers", params={"page": page, "per_page": per_page})

    def get_customer(self, customer_id: int) -> Dict:
        return self._request("GET", f"/customers/{customer_id}")
```

### Step 3: Product Sync

```python
import frappe
from typing import Dict, Any

class WooCommerceProductSync:
    """Sync products between ERPNext and WooCommerce."""

    def __init__(self):
        self.client = WooCommerceClient()
        self.settings = frappe.get_single("WooCommerce Settings")

    def sync_products_to_woocommerce(self) -> Dict[str, Any]:
        """Push ERPNext items to WooCommerce."""

        items = frappe.get_all(
            "Item",
            filters={
                "is_sales_item": 1,
                "disabled": 0,
                "sync_to_woocommerce": 1  # Custom field
            },
            fields=[
                "name", "item_name", "description", "standard_rate",
                "stock_uom", "image", "item_group", "woocommerce_id"
            ]
        )

        results = {"created": 0, "updated": 0, "failed": 0, "errors": []}

        for item in items:
            try:
                wc_product = self._map_item_to_wc_product(item)

                if item.woocommerce_id:
                    # Update existing
                    result = self.client.update_product(item.woocommerce_id, wc_product)
                    if result["success"]:
                        results["updated"] += 1
                    else:
                        results["failed"] += 1
                        results["errors"].append({"item": item.name, "error": result["error"]})
                else:
                    # Create new
                    result = self.client.create_product(wc_product)
                    if result["success"]:
                        # Save WooCommerce ID
                        frappe.db.set_value("Item", item.name, "woocommerce_id", result["data"]["id"])
                        results["created"] += 1
                    else:
                        results["failed"] += 1
                        results["errors"].append({"item": item.name, "error": result["error"]})

            except Exception as e:
                results["failed"] += 1
                results["errors"].append({"item": item.name, "error": str(e)})

        frappe.db.commit()
        return results

    def sync_products_from_woocommerce(self) -> Dict[str, Any]:
        """Pull WooCommerce products to ERPNext."""

        results = {"created": 0, "updated": 0, "failed": 0}
        page = 1

        while True:
            response = self.client.get_products(page=page)

            if not response["success"]:
                results["errors"] = response["error"]
                break

            products = response["data"]
            if not products:
                break

            for product in products:
                try:
                    self._import_wc_product(product)
                    if frappe.db.exists("Item", {"woocommerce_id": product["id"]}):
                        results["updated"] += 1
                    else:
                        results["created"] += 1
                except Exception as e:
                    results["failed"] += 1
                    frappe.log_error(f"Failed to import WC product {product['id']}: {e}")

            page += 1
            if page > response.get("total_pages", 1):
                break

        frappe.db.commit()
        return results

    def _map_item_to_wc_product(self, item: dict) -> dict:
        """Map ERPNext Item to WooCommerce product format."""
        return {
            "name": item["item_name"],
            "type": "simple",
            "regular_price": str(item["standard_rate"]),
            "description": item.get("description", ""),
            "short_description": item.get("description", "")[:200] if item.get("description") else "",
            "sku": item["name"],
            "manage_stock": True,
            "stock_quantity": self._get_stock_qty(item["name"])
        }

    def _import_wc_product(self, product: dict):
        """Import WooCommerce product to ERPNext."""
        sku = product.get("sku") or f"WC-{product['id']}"

        if frappe.db.exists("Item", sku):
            # Update existing
            item = frappe.get_doc("Item", sku)
            item.item_name = product["name"]
            item.description = product.get("description", "")
            item.standard_rate = float(product.get("regular_price", 0) or 0)
            item.woocommerce_id = product["id"]
            item.save()
        else:
            # Create new
            item = frappe.new_doc("Item")
            item.item_code = sku
            item.item_name = product["name"]
            item.item_group = "WooCommerce Products"  # Create this group
            item.description = product.get("description", "")
            item.standard_rate = float(product.get("regular_price", 0) or 0)
            item.stock_uom = "Nos"
            item.is_sales_item = 1
            item.woocommerce_id = product["id"]
            item.insert()

    def _get_stock_qty(self, item_code: str) -> int:
        """Get current stock quantity for item."""
        qty = frappe.db.get_value(
            "Bin",
            {"item_code": item_code, "warehouse": self.settings.default_warehouse},
            "actual_qty"
        )
        return int(qty or 0)
```

### Step 4: Order Sync

```python
import frappe
from typing import Dict, Any

class WooCommerceOrderSync:
    """Sync orders from WooCommerce to ERPNext."""

    def __init__(self):
        self.client = WooCommerceClient()
        self.settings = frappe.get_single("WooCommerce Settings")

    def import_orders(self, status: str = "processing") -> Dict[str, Any]:
        """Import new orders from WooCommerce."""

        results = {"imported": 0, "skipped": 0, "failed": 0, "errors": []}

        # Get orders since last sync
        last_sync = self.settings.last_order_sync
        after = last_sync.isoformat() if last_sync else None

        page = 1
        while True:
            response = self.client.get_orders(status=status, after=after, page=page)

            if not response["success"]:
                results["errors"].append(response["error"])
                break

            orders = response["data"]
            if not orders:
                break

            for order in orders:
                try:
                    if frappe.db.exists("Sales Order", {"woocommerce_order_id": order["id"]}):
                        results["skipped"] += 1
                        continue

                    self._create_sales_order(order)
                    results["imported"] += 1

                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append({"order_id": order["id"], "error": str(e)})
                    frappe.log_error(f"Failed to import WC order {order['id']}: {e}")

            page += 1
            if page > response.get("total_pages", 1):
                break

        # Update last sync time
        frappe.db.set_single_value("WooCommerce Settings", "last_order_sync", frappe.utils.now())
        frappe.db.commit()

        return results

    def _create_sales_order(self, wc_order: dict) -> str:
        """Create Sales Order from WooCommerce order."""

        # Get or create customer
        customer = self._get_or_create_customer(wc_order)

        # Create Sales Order
        so = frappe.new_doc("Sales Order")
        so.customer = customer
        so.company = self.settings.default_company
        so.woocommerce_order_id = wc_order["id"]
        so.po_no = f"WC-{wc_order['number']}"
        so.delivery_date = frappe.utils.add_days(frappe.utils.today(), 7)

        # Add items
        for line_item in wc_order["line_items"]:
            item_code = self._get_item_code(line_item)
            if not item_code:
                continue

            so.append("items", {
                "item_code": item_code,
                "qty": line_item["quantity"],
                "rate": float(line_item["price"]),
                "warehouse": self.settings.default_warehouse
            })

        # Add shipping as item if exists
        if float(wc_order.get("shipping_total", 0)) > 0:
            shipping_item = self._get_shipping_item()
            so.append("items", {
                "item_code": shipping_item,
                "qty": 1,
                "rate": float(wc_order["shipping_total"])
            })

        so.insert(ignore_permissions=True)

        # Submit if payment is complete
        if wc_order["status"] in ["processing", "completed"]:
            so.submit()

        frappe.db.commit()
        return so.name

    def _get_or_create_customer(self, wc_order: dict) -> str:
        """Get existing customer or create new one."""
        billing = wc_order.get("billing", {})
        email = billing.get("email")

        if email:
            existing = frappe.db.exists("Customer", {"email_id": email})
            if existing:
                return existing

        # Create new customer
        customer = frappe.new_doc("Customer")
        customer.customer_name = f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip()
        customer.customer_type = "Individual"
        customer.email_id = email
        customer.mobile_no = billing.get("phone")
        customer.woocommerce_customer_id = wc_order.get("customer_id")
        customer.insert(ignore_permissions=True)

        # Create address
        if billing.get("address_1"):
            self._create_address(customer.name, billing, "Billing")

        shipping = wc_order.get("shipping", {})
        if shipping.get("address_1"):
            self._create_address(customer.name, shipping, "Shipping")

        frappe.db.commit()
        return customer.name

    def _create_address(self, customer: str, address_data: dict, address_type: str):
        """Create address for customer."""
        address = frappe.new_doc("Address")
        address.address_title = f"{customer} - {address_type}"
        address.address_type = address_type
        address.address_line1 = address_data.get("address_1")
        address.address_line2 = address_data.get("address_2")
        address.city = address_data.get("city")
        address.state = address_data.get("state")
        address.pincode = address_data.get("postcode")
        address.country = address_data.get("country")
        address.append("links", {"link_doctype": "Customer", "link_name": customer})
        address.insert(ignore_permissions=True)

    def _get_item_code(self, line_item: dict) -> str:
        """Get ERPNext item code from WooCommerce line item."""
        sku = line_item.get("sku")
        if sku and frappe.db.exists("Item", sku):
            return sku

        # Try by WooCommerce product ID
        product_id = line_item.get("product_id")
        item = frappe.db.get_value("Item", {"woocommerce_id": product_id}, "name")
        if item:
            return item

        # Create placeholder item
        return self._create_placeholder_item(line_item)

    def _create_placeholder_item(self, line_item: dict) -> str:
        """Create placeholder item for unknown WC product."""
        item_code = f"WC-{line_item['product_id']}"

        if frappe.db.exists("Item", item_code):
            return item_code

        item = frappe.new_doc("Item")
        item.item_code = item_code
        item.item_name = line_item["name"]
        item.item_group = "WooCommerce Products"
        item.stock_uom = "Nos"
        item.is_sales_item = 1
        item.woocommerce_id = line_item["product_id"]
        item.insert(ignore_permissions=True)

        return item_code

    def _get_shipping_item(self) -> str:
        """Get or create shipping charges item."""
        if not frappe.db.exists("Item", "SHIPPING"):
            item = frappe.new_doc("Item")
            item.item_code = "SHIPPING"
            item.item_name = "Shipping Charges"
            item.item_group = "Services"
            item.stock_uom = "Nos"
            item.is_sales_item = 1
            item.is_stock_item = 0
            item.insert(ignore_permissions=True)

        return "SHIPPING"
```

### Step 5: Inventory Sync

```python
import frappe

class WooCommerceInventorySync:
    """Sync inventory levels to WooCommerce."""

    def __init__(self):
        self.client = WooCommerceClient()
        self.settings = frappe.get_single("WooCommerce Settings")

    def sync_inventory(self) -> Dict[str, Any]:
        """Push inventory levels to WooCommerce."""

        items = frappe.db.sql("""
            SELECT
                i.name as item_code,
                i.woocommerce_id,
                COALESCE(b.actual_qty, 0) as qty
            FROM `tabItem` i
            LEFT JOIN `tabBin` b ON i.name = b.item_code
                AND b.warehouse = %(warehouse)s
            WHERE i.woocommerce_id IS NOT NULL
                AND i.disabled = 0
        """, {"warehouse": self.settings.default_warehouse}, as_dict=True)

        results = {"updated": 0, "failed": 0}

        for item in items:
            result = self.client.update_product_stock(
                item.woocommerce_id,
                int(item.qty)
            )

            if result["success"]:
                results["updated"] += 1
            else:
                results["failed"] += 1
                frappe.log_error(f"Failed to sync stock for {item.item_code}: {result['error']}")

        return results
```

## Complete Example: WooCommerce Integration Manager

```python
import frappe
from frappe import _

class WooCommerceIntegration:
    """Complete WooCommerce integration manager."""

    def __init__(self):
        self.settings = frappe.get_single("WooCommerce Settings")
        if not self.settings.enabled:
            frappe.throw(_("WooCommerce integration is not enabled"))

        self.product_sync = WooCommerceProductSync()
        self.order_sync = WooCommerceOrderSync()
        self.inventory_sync = WooCommerceInventorySync()

    def full_sync(self) -> Dict[str, Any]:
        """Run full synchronization."""
        results = {}

        if self.settings.sync_products:
            results["products_to_wc"] = self.product_sync.sync_products_to_woocommerce()
            results["products_from_wc"] = self.product_sync.sync_products_from_woocommerce()

        if self.settings.sync_orders:
            results["orders"] = self.order_sync.import_orders()

        if self.settings.sync_inventory:
            results["inventory"] = self.inventory_sync.sync_inventory()

        return results

    def sync_orders_only(self) -> Dict[str, Any]:
        """Sync orders only."""
        return self.order_sync.import_orders()

    def sync_inventory_only(self) -> Dict[str, Any]:
        """Sync inventory only."""
        return self.inventory_sync.sync_inventory()

# API Endpoints
@frappe.whitelist()
def run_woocommerce_sync():
    """Run full WooCommerce sync."""
    integration = WooCommerceIntegration()
    return integration.full_sync()

@frappe.whitelist()
def import_woocommerce_orders():
    """Import new orders from WooCommerce."""
    integration = WooCommerceIntegration()
    return integration.sync_orders_only()

@frappe.whitelist()
def sync_inventory_to_woocommerce():
    """Push inventory to WooCommerce."""
    integration = WooCommerceIntegration()
    return integration.sync_inventory_only()
```

## Scheduler Configuration

```python
# In hooks.py
scheduler_events = {
    "hourly": [
        "your_app.woocommerce.import_woocommerce_orders"
    ],
    "daily": [
        "your_app.woocommerce.sync_inventory_to_woocommerce"
    ]
}
```

## Troubleshooting

### API Connection Failed
- Verify WooCommerce URL includes https://
- Check consumer key/secret
- Ensure REST API is enabled in WooCommerce

### Orders Not Importing
- Verify order status filter matches WC orders
- Check for duplicate woocommerce_order_id
- Review error logs

## Next Steps

- [REST API Integration Patterns](../rest-api-integration-patterns/rest-api-integration-patterns.md)
- [Webhook Event Handling](../webhook-event-handling/webhook-event-handling.md)

---

*Source: Frappe Integration Documentation | Difficulty: Advanced | Last updated: 2026-02-04*
