"""
Shopee Marketplace Connector.

Tài liệu API: https://open.shopee.com/documents
Authentication: OAuth 2.0 / HMAC-SHA256 signature
"""

import frappe
from dcnet_apps.dcnet_ecommerce.connectors.base import BaseConnector


class ShopeeConnector(BaseConnector):
    """Connector cho Shopee Marketplace."""

    def get_name(self) -> str:
        return "Shopee"

    def get_base_url(self) -> str:
        is_sandbox = self.connection_doc.get("is_sandbox") if self.connection_doc else False
        if is_sandbox:
            return "https://partner.test-stable.shopeemobile.com"
        return "https://partner.shopeemobile.com"

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self) -> None:
        """
        Xác thực với Shopee Open Platform API.
        Shopee dùng HMAC-SHA256 signature — mỗi request cần sign riêng.
        """
        cached = self.get_cached_token()
        if cached:
            self._access_token = cached
            return

        token = self.connection_doc.get_password("access_token") if self.connection_doc else None
        if not token:
            frappe.throw(
                "Shopee: Chưa có access_token. Vui lòng hoàn tất OAuth authorization flow."
            )

        self._access_token = token
        self.cache_token(token, ttl=3600)

    def get_auth_url(self, callback_url: str, state: str) -> str:
        """Tạo URL xác thực của Shopee (Trống)."""
        raise NotImplementedError("Shopee.get_auth_url chưa được implement.")

    def handle_oauth_callback(self, code: str, callback_url: str) -> dict:
        """Xử lý callback của Shopee (Trống)."""
        raise NotImplementedError("Shopee.handle_oauth_callback chưa được implement.")

    def refresh_access_token(self) -> None:
        """
        Làm mới Shopee access token bằng refresh token.
        Shopee endpoint: POST /api/v2/auth/access_token/get

        TODO: Implement khi cần auto-refresh.
        """
        frappe.logger().info("[Shopee] TODO: refresh_access_token chưa được implement.")

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------

    def get_products(self, filters: dict | None = None) -> list[dict]:
        """
        Lấy danh sách sản phẩm từ Shopee shop.
        Shopee endpoint: GET /api/v2/product/get_item_list

        TODO: Implement thực tế.
        Docs: https://open.shopee.com/documents/v2/v2.product.get_item_list
        """
        self.ensure_connected()
        raise NotImplementedError("Shopee.get_products chưa được implement.")

    def get_product(self, product_id: str) -> dict | None:
        """
        Lấy chi tiết sản phẩm theo item_id.
        Shopee endpoint: GET /api/v2/product/get_item_base_info

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Shopee.get_product chưa được implement.")

    def sync_product(self, product_data: dict) -> bool:
        """
        Đăng sản phẩm mới lên Shopee.
        Shopee endpoint: POST /api/v2/product/add_item

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Shopee.sync_product chưa được implement.")

    def update_product(self, product_id: str, product_data: dict) -> bool:
        """
        Cập nhật sản phẩm trên Shopee.
        Shopee endpoint: POST /api/v2/product/update_item

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Shopee.update_product chưa được implement.")

    def delete_product(self, product_id: str) -> bool:
        """
        Xoá sản phẩm khỏi Shopee.
        Shopee endpoint: POST /api/v2/product/delete_item

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Shopee.delete_product chưa được implement.")

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    def get_orders(self, filters: dict | None = None) -> list[dict]:
        """
        Lấy danh sách đơn hàng từ Shopee.
        Shopee endpoint: GET /api/v2/order/get_order_list

        Args filters:
            time_range_field: 'create_time' | 'update_time'
            time_from:  Unix timestamp
            time_to:    Unix timestamp
            order_status: 'UNPAID' | 'READY_TO_SHIP' | 'SHIPPED' | ...

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Shopee.get_orders chưa được implement.")

    def get_order(self, order_id: str) -> dict | None:
        """
        Lấy chi tiết đơn hàng theo order_sn.
        Shopee endpoint: GET /api/v2/order/get_order_detail

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Shopee.get_order chưa được implement.")

    def update_order_status(self, order_id: str, status: str) -> bool:
        """
        Cập nhật trạng thái đơn hàng Shopee.
        Ví dụ: ship đơn hàng qua /api/v2/logistics/init_logistic

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Shopee.update_order_status chưa được implement.")

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------

    def sync_inventory(self, product_id: str, quantity: int) -> bool:
        """
        Cập nhật tồn kho sản phẩm trên Shopee.
        Shopee endpoint: POST /api/v2/product/update_stock

        TODO: Implement thực tế.
        """
        self.ensure_connected()
        raise NotImplementedError("Shopee.sync_inventory chưa được implement.")
