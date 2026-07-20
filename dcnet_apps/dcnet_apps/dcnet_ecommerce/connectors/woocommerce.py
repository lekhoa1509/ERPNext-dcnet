"""
WooCommerce Marketplace Connector.

Documentation: https://woocommerce.github.io/woocommerce-rest-api-docs/
Authentication: REST API Keys (Consumer Key & Consumer Secret)
"""

import frappe
import requests
from dcnet_apps.dcnet_ecommerce.connectors.base import BaseConnector


class WooCommerceConnector(BaseConnector):
    """Connector cho WooCommerce Marketplace."""

    def get_name(self) -> str:
        return "Woocommerce"

    def get_base_url(self) -> str:
        """WooCommerce REST API endpoint."""
        store_url = self.connection_doc.get("store_url")
        if not store_url:
             frappe.throw("WooCommerce: Thiếu Store URL.")
        
        # Đảm bảo store_url kết thúc bằng /wp-json/wc/v3/
        base_url = store_url.rstrip("/")
        if "/wp-json/wc/v3" not in base_url:
            base_url = f"{base_url}/wp-json/wc/v3"
            
        return base_url

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self) -> None:
        """
        Xác thực với WooCommerce.
        """
        consumer_key = self.connection_doc.get_password("consumer_key")
        consumer_secret = self.connection_doc.get_password("consumer_secret")

        if not consumer_key or not consumer_secret:
            frappe.throw(
                "WooCommerce: Chưa có Consumer Key hoặc Consumer Secret."
            )
        self._connected = True

    def get_auth_url(self, callback_url: str, state: str) -> str:
        """
        Tạo URL xác thực của WooCommerce.
        Hỗ trợ WooCommerce API Auth Endpoint để tự động cấp keys.
        """
        store_url = self.connection_doc.get("store_url")
        if not store_url:
            frappe.throw("Vui lòng điền Store URL trước khi kết nối.")

        # Đảm bảo callback_url dùng HTTPS cho WooCommerce
        if callback_url.startswith("http://"):
            callback_url = callback_url.replace("http://", "https://", 1)

        # WooCommerce API Auth Endpoint
        from urllib.parse import urlencode
        
        auth_base = f"{store_url.rstrip('/')}/wc-auth/v1/authorize"
        params = {
            "app_name": "DCNet_Ecommerce",
            "scope": "read_write",
            "user_id": state, # Gửi state qua user_id để nhận diện bản ghi khi WC gọi về
            "return_url": callback_url + f"?state={state}",
            "callback_url": callback_url
        }
        
        return f"{auth_base}?{urlencode(params)}"

    def handle_oauth_callback(self, code: str, callback_url: str) -> dict:
        """
        Xử lý callback của WooCommerce (dành cho return_url redirect).
        """
        return {
            "access_token": "manual",
            "shop_id": self.connection_doc.get("store_url"),
            "shop_name": "WooCommerce Store"
        }

    # ------------------------------------------------------------------
    # Headers & Request Overrides
    # ------------------------------------------------------------------

    def _get_default_headers(self) -> dict:
        """
        Override default headers để dùng Basic Auth cho WooCommerce.
        """
        import base64
        
        consumer_key = self.connection_doc.get_password("consumer_key")
        consumer_secret = self.connection_doc.get_password("consumer_secret")
        
        auth_str = f"{consumer_key}:{consumer_secret}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()
        
        return {
            "Content-Type": "application/json",
            "Accept":       "application/json",
            "Authorization": f"Basic {encoded_auth}"
        }

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------

    def get_products(self, filters: dict | None = None) -> list[dict]:
        self.ensure_connected()
        return self._make_api_request("GET", "products", data=filters)

    def get_product(self, product_id: str) -> dict | None:
        self.ensure_connected()
        return self._make_api_request("GET", f"products/{product_id}")

    def sync_product(self, product_data: dict) -> bool:
        self.ensure_connected()
        resp = self._make_api_request("POST", "products", data=product_data)
        return bool(resp.get("id"))

    def update_product(self, product_id: str, product_data: dict) -> bool:
        self.ensure_connected()
        resp = self._make_api_request("PUT", f"products/{product_id}", data=product_data)
        return bool(resp.get("id"))

    def delete_product(self, product_id: str) -> bool:
        self.ensure_connected()
        resp = self._make_api_request("DELETE", f"products/{product_id}", data={"force": True})
        return bool(resp.get("id"))

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def get_orders(self, filters: dict | None = None) -> list[dict]:
        self.ensure_connected()
        return self._make_api_request("GET", "orders", data=filters)

    def get_order(self, order_id: str) -> dict | None:
        self.ensure_connected()
        return self._make_api_request("GET", f"orders/{order_id}")

    def update_order_status(self, order_id: str, status: str) -> bool:
        self.ensure_connected()
        resp = self._make_api_request("PUT", f"orders/{order_id}", data={"status": status})
        return bool(resp.get("id"))

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------

    def sync_inventory(self, product_id: str, quantity: int) -> bool:
        self.ensure_connected()
        resp = self._make_api_request("PUT", f"products/{product_id}", data={
            "manage_stock": True,
            "stock_quantity": quantity
        })
        return bool(resp.get("id"))
