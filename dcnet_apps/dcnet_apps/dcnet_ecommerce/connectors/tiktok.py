"""
TikTok Shop Marketplace Connector.

Tài liệu API: https://partner.tiktokshop.com/docv2/
Authentication: OAuth 2.0
"""

import frappe
from dcnet_apps.dcnet_ecommerce.connectors.base import BaseConnector


class TikTokShopConnector(BaseConnector):
    """Connector cho TikTok Shop Marketplace."""

    def get_name(self) -> str:
        return "TikTok Shop"

    def get_base_url(self) -> str:
        """TikTok Shop Open API endpoint."""
        return "https://open-api.tiktokglobalshop.com"

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self) -> None:
        """
        Xác thực với TikTok Shop.
        """
        cached = self.get_cached_token()
        if cached:
            self._access_token = cached
            return

        token = self.connection_doc.get_password("access_token") if self.connection_doc else None
        if not token:
            frappe.throw(
                "TikTok Shop: Chưa có access_token. Vui lòng hoàn tất OAuth authorization flow."
            )

        self._access_token = token
        self.cache_token(token, ttl=3600)

    def get_auth_url(self, callback_url: str, state: str) -> str:
        """Tạo URL xác thực của TikTok Shop"""

        service_id = self.connection_doc.get_password("service_id")
        if not service_id:
            frappe.throw("Vui lòng điền Service ID trước khi kết nối.")

        # Tiktok Auth URL pattern
        # Docs: https://partner.tiktokshop.com/docv2/230113
        from urllib.parse import urlencode
        
        auth_base = "https://services.tiktokshop.com/open/authorize"
        params = {
            "service_id": service_id,
            "state": state
        }
        
        return f"{auth_base}?{urlencode(params)}"

    def handle_oauth_callback(self, code: str, callback_url: str) -> dict:
        """Xử lý callback của TikTok Shop để lấy access_token."""
        
        api_key_tiktok = self.connection_doc.get_password("api_key_tiktok")
        api_secret_tiktok = self.connection_doc.get_password("api_secret_tiktok")

        if not api_key_tiktok or not api_secret_tiktok:
            frappe.throw("Vui lòng điền API Key và API Secret của TikTok trước khi kết nối.")

        # TikTok Shop API v2 token exchange endpoint
        # Docs: https://partner.tiktokshop.com/docv2/230114
        import requests
        import time

        url = "https://auth.tiktok-shops.com/api/v2/token/get"
        params = {
            "app_key": api_key_tiktok,
            "app_secret": api_secret_tiktok,
            "auth_code": code,
            "grant_type": "authorized_code",
        }

        try:
            resp = requests.get(url, params=params, timeout=30)
            resp_data = resp.json()

            if resp_data.get("code") != 0:
                error_msg = resp_data.get("message", "Unknown error")
                frappe.throw(f"Lỗi TikTok Shop API: {error_msg} (Code: {resp_data.get('code')})")

            data = resp_data.get("data", {})
            
            # Tính toán expires_in (seconds)
            access_token_expire_at = data.get("access_token_expire_at")
            expires_in = 0
            if access_token_expire_at:
                expires_in = int(access_token_expire_at) - int(time.time())

            return {
                "access_token": data.get("access_token"),
                "refresh_token": data.get("refresh_token"),
                "expires_in": expires_in,
                "shop_id": data.get("user_id"), # TikTok V2 dùng user_id / seller_name
                "shop_name": data.get("seller_name"),
            }

        except Exception as e:
            frappe.logger().error(f"[TikTok Shop] OAuth callback failed: {e}")
            frappe.throw(f"Không thể kết nối với TikTok Shop: {e}")

    def refresh_access_token(self) -> None:
        """
        Làm mới TikTok Shop access token bằng refresh token.
        Docs: https://partner.tiktokshop.com/docv2/230114
        """
        if not self._refresh_token:
            frappe.throw("Chưa có refresh_token để làm mới access_token.")

        api_key_tiktok = self.connection_doc.get_password("api_key_tiktok")
        api_secret_tiktok = self.connection_doc.get_password("api_secret_tiktok")

        import requests
        import time

        url = "https://auth.tiktok-shops.com/api/v2/token/refresh"
        params = {
            "app_key": api_key_tiktok,
            "app_secret": api_secret_tiktok,
            "refresh_token": self._refresh_token,
            "grant_type": "refresh_token",
        }

        try:
            resp = requests.get(url, params=params, timeout=30)
            resp_data = resp.json()

            if resp_data.get("code") != 0:
                error_msg = resp_data.get("message", "Unknown error")
                frappe.logger().error(f"[TikTok Shop] Refresh token failed: {error_msg}")
                return

            data = resp_data.get("data", {})
            new_access_token = data.get("access_token")
            new_refresh_token = data.get("refresh_token")
            access_token_expire_at = data.get("access_token_expire_at")

            if new_access_token:
                self._access_token = new_access_token
                self._refresh_token = new_refresh_token
                
                # Cập nhật vào database
                self.connection_doc.access_token = new_access_token
                if new_refresh_token:
                    self.connection_doc.refresh_token = new_refresh_token
                
                if access_token_expire_at:
                    from frappe.utils import add_to_date, now_datetime
                    expires_in = int(access_token_expire_at) - int(time.time())
                    self.connection_doc.token_expires_at = add_to_date(now_datetime(), seconds=expires_in)
                    self.cache_token(new_access_token, ttl=expires_in)
                
                self.connection_doc.save(ignore_permissions=True)
                frappe.db.commit()
                
                frappe.logger().info(f"[TikTok Shop] Access token refreshed for {self.connection_doc.name}")

        except Exception as e:
            frappe.logger().error(f"[TikTok Shop] Refresh token exception: {e}")

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------

    def get_products(self, filters: dict | None = None) -> list[dict]:
        self.ensure_connected()
        raise NotImplementedError("TikTokShop.get_products chưa được implement.")

    def get_product(self, product_id: str) -> dict | None:
        self.ensure_connected()
        raise NotImplementedError("TikTokShop.get_product chưa được implement.")

    def sync_product(self, product_data: dict) -> bool:
        self.ensure_connected()
        raise NotImplementedError("TikTokShop.sync_product chưa được implement.")

    def update_product(self, product_id: str, product_data: dict) -> bool:
        self.ensure_connected()
        raise NotImplementedError("TikTokShop.update_product chưa được implement.")

    def delete_product(self, product_id: str) -> bool:
        self.ensure_connected()
        raise NotImplementedError("TikTokShop.delete_product chưa được implement.")

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def get_orders(self, filters: dict | None = None) -> list[dict]:
        self.ensure_connected()
        raise NotImplementedError("TikTokShop.get_orders chưa được implement.")

    def get_order(self, order_id: str) -> dict | None:
        self.ensure_connected()
        raise NotImplementedError("TikTokShop.get_order chưa được implement.")

    def update_order_status(self, order_id: str, status: str) -> bool:
        self.ensure_connected()
        raise NotImplementedError("TikTokShop.update_order_status chưa được implement.")

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------

    def sync_inventory(self, product_id: str, quantity: int) -> bool:
        self.ensure_connected()
        raise NotImplementedError("TikTokShop.sync_inventory chưa được implement.")
