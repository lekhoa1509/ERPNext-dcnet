"""
Lazada Marketplace Connector.

Tài liệu API: https://lazada.github.io/lazop-sdk-doc/
Authentication: OAuth 2.0 + HMAC-SHA256 (APP Key + APP Secret)
"""

import frappe
from dcnet_apps.dcnet_ecommerce.connectors.base import BaseConnector


class LazadaConnector(BaseConnector):
    """Connector cho Lazada Marketplace."""

    def get_name(self) -> str:
        return "Lazada"

    def get_base_url(self) -> str:
        """Vietnam endpoint."""
        return "https://api.lazada.vn/rest"

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self) -> None:
        """
        Xác thực với Lazada Open Platform.
        Mỗi request cần sign bằng HMAC-SHA256 với APP Key + APP Secret + access_token.
        """
        cached = self.get_cached_token()
        if cached:
            self._access_token = cached
            return

        token = self.connection_doc.get_password("access_token") if self.connection_doc else None
        if not token:
            frappe.throw(
                "Lazada: Chưa có access_token. Vui lòng hoàn tất OAuth authorization flow."
            )

        self._access_token = token
        # Lazada tokens usually last longer, but we cache for 1 hour by default
        self.cache_token(token, ttl=3600)

    def get_auth_url(self, callback_url: str, state: str) -> str:
        """Tạo URL xác thực của Lazada."""
        app_key = self.connection_doc.get_password("api_key_lazada")
        if not app_key:
            frappe.throw("Vui lòng điền App Key trước khi kết nối.")

        # Lazada Auth URL pattern
        auth_base = "https://auth.lazada.com/oauth/authorize"
        params = {
            "response_type": "code",
            "force_auth": "true",
            "redirect_uri": callback_url,
            "client_id": app_key,
            "state": state
        }
        
        import urllib.parse
        return f"{auth_base}?{urllib.parse.urlencode(params)}"

    def handle_oauth_callback(self, code: str, callback_url: str) -> dict:
        """Đổi code lấy access_token từ Lazada."""
        app_key = self.connection_doc.get_password("api_key_lazada")
        app_secret = self.connection_doc.get_password("api_secret_lazada")

        if not app_key or not app_secret:
            frappe.throw("Không tìm thấy App Key hoặc App Secret để đổi token.")

        # Lazada token endpoint
        token_url = "https://auth.lazada.com/rest/auth/token/create"
        
        import requests
        import time
        import hmac
        import hashlib

        timestamp = str(int(time.time() * 1000))
        payload = {
            "app_key": app_key,
            "timestamp": timestamp,
            "sign_method": "sha256",
            "code": code
        }

        # Sorting params for signature
        sorted_params = sorted(payload.items())
        query_string = "".join(f"{k}{v}" for k, v in sorted_params)
        
        # Sign the string
        # pattern: hmac_sha256(app_secret, "/auth/token/create" + sorted_params)
        sign_base = "/auth/token/create" + query_string
        signature = hmac.new(
            app_secret.encode("utf-8"),
            sign_base.encode("utf-8"),
            hashlib.sha256
        ).hexdigest().upper()
        
        payload["sign"] = signature

        resp = requests.post(token_url, data=payload)
        data = resp.json()

        if "access_token" not in data:
            error_msg = data.get("message", data.get("msg", "Unknown error"))
            frappe.throw(f"Lazada OAuth failed: {error_msg}")

        return {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),
            "expires_in": data.get("expires_in"),
            "shop_id": data.get("country_user_info", [{}])[0].get("seller_id"),
            "shop_name": data.get("account")
        }

    def refresh_access_token(self) -> None:
        """
        Làm mới Lazada access token.
        Lazada endpoint: POST /auth/token/refresh

        TODO: Implement khi cần auto-refresh.
        """
        frappe.logger().info("[Lazada] TODO: refresh_access_token chưa được implement.")

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------

    def get_products(self, filters: dict | None = None) -> list[dict]:
        """
        Lấy danh sách sản phẩm từ Lazada Seller Center.
        Lazada endpoint: GET /products/get

        Args filters: offset, limit, filter ('live'|'inactive'|'deleted'|...)

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Lazada.get_products chưa được implement.")

    def get_product(self, product_id: str) -> dict | None:
        """
        Lấy chi tiết sản phẩm theo item_id.
        Lazada endpoint: GET /product/item/get

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Lazada.get_product chưa được implement.")

    def sync_product(self, product_data: dict) -> bool:
        """
        Đăng sản phẩm mới lên Lazada.
        Lazada endpoint: POST /product/create

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Lazada.sync_product chưa được implement.")

    def update_product(self, product_id: str, product_data: dict) -> bool:
        """
        Cập nhật sản phẩm trên Lazada.
        Lazada endpoint: POST /product/update

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Lazada.update_product chưa được implement.")

    def delete_product(self, product_id: str) -> bool:
        """
        Xoá sản phẩm khỏi Lazada.
        Lazada endpoint: POST /product/remove

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Lazada.delete_product chưa được implement.")

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def get_orders(self, filters: dict | None = None) -> list[dict]:
        """
        Lấy danh sách đơn hàng Lazada.
        Lazada endpoint: GET /orders/get

        Args filters: created_after, created_before, status, offset, limit.

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Lazada.get_orders chưa được implement.")

    def get_order(self, order_id: str) -> dict | None:
        """
        Lấy chi tiết đơn hàng Lazada.
        Lazada endpoint: GET /order/get

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Lazada.get_order chưa được implement.")

    def update_order_status(self, order_id: str, status: str) -> bool:
        """
        Cập nhật trạng thái đơn hàng Lazada.
        Ví dụ: set ready to ship / mark shipped.

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Lazada.update_order_status chưa được implement.")

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------

    def sync_inventory(self, product_id: str, quantity: int) -> bool:
        """
        Cập nhật tồn kho sản phẩm trên Lazada.
        Lazada endpoint: POST /product/stock/sellable/update

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Lazada.sync_inventory chưa được implement.")
