"""
Abstract base class cho tất cả Marketplace Connectors.

Port từ PHP AbstractMarketplaceConnector sang Python/Frappe,
theo pattern của dcnet_einvoice.providers.base.BaseProvider.
"""

import time
import math
import frappe
from abc import ABC, abstractmethod
from frappe.utils import now_datetime


class BaseConnector(ABC):
    """
    Abstract base class định nghĩa giao diện chung cho các marketplace connector.

    Mỗi sàn TMĐT (Shopee, Lazada, Tiki, ...) phải kế thừa class này
    và implement tất cả abstract methods.

    Attributes:
        connection_doc: Frappe Document chứa thông tin kết nối (platform, shop_id, tokens,...).
        _access_token:  Access token hiện tại (sau khi authenticate).
        _refresh_token: Refresh token để lấy access token mới.
        _token_expires_at: Thời điểm access token hết hạn (datetime hoặc None).
        _connected:     Trạng thái kết nối.
    """

    def __init__(self, connection_doc):
        """
        Args:
            connection_doc: Frappe Document chứa config kết nối.
                            Phải có các trường: platform, shop_id,
                            access_token, refresh_token, token_expires_at.
        """
        self.connection_doc = connection_doc
        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._token_expires_at = None
        self._connected: bool = False

    # ------------------------------------------------------------------
    # Abstract: Subclass phải implement
    # ------------------------------------------------------------------

    @abstractmethod
    def get_name(self) -> str:
        """Trả về tên định danh của platform, ví dụ: 'Shopee', 'Lazada'."""
        ...

    @abstractmethod
    def get_base_url(self) -> str:
        """Trả về base API URL của marketplace."""
        ...

    @abstractmethod
    def authenticate(self) -> None:
        """
        Xác thực với marketplace API.
        Phải set self._access_token sau khi thành công.
        """
        ...

    @abstractmethod
    def get_auth_url(self, callback_url: str, state: str) -> str:
        """
        Tạo URL để người dùng đăng nhập và cấp quyền (OAuth Authorization URL).
        """
        ...

    @abstractmethod
    def handle_oauth_callback(self, code: str, callback_url: str) -> dict:
        """
        Xử lý code từ callback để lấy access_token và refresh_token.
        Returns:
            Dict chứa token data (access_token, refresh_token, expires_in).
        """
        ...

    # ------------------------------------------------------------------
    # Abstract: Products
    # ------------------------------------------------------------------

    @abstractmethod
    def get_products(self, filters: dict | None = None) -> list[dict]:
        """
        Lấy danh sách sản phẩm từ marketplace.

        Args:
            filters: Dict bộ lọc tuỳ sàn (page, limit, status, ...).

        Returns:
            List raw product dicts từ API.
        """
        ...

    @abstractmethod
    def get_product(self, product_id: str) -> dict | None:
        """
        Lấy chi tiết một sản phẩm theo ID.

        Returns:
            Raw product dict, hoặc None nếu không tìm thấy.
        """
        ...

    @abstractmethod
    def sync_product(self, product_data: dict) -> bool:
        """
        Tạo (đăng) một sản phẩm mới lên marketplace.

        Args:
            product_data: Dict chuẩn hoá với các trường sản phẩm.

        Returns:
            True nếu thành công.
        """
        ...

    @abstractmethod
    def update_product(self, product_id: str, product_data: dict) -> bool:
        """
        Cập nhật thông tin sản phẩm đã có trên marketplace.

        Returns:
            True nếu thành công.
        """
        ...

    @abstractmethod
    def delete_product(self, product_id: str) -> bool:
        """
        Xoá sản phẩm khỏi marketplace.

        Returns:
            True nếu thành công.
        """
        ...

    # ------------------------------------------------------------------
    # Abstract: Orders
    # ------------------------------------------------------------------

    @abstractmethod
    def get_orders(self, filters: dict | None = None) -> list[dict]:
        """
        Lấy danh sách đơn hàng từ marketplace.

        Args:
            filters: Dict bộ lọc tuỳ sàn (from_date, to_date, status, ...).

        Returns:
            List raw order dicts từ API.
        """
        ...

    @abstractmethod
    def get_order(self, order_id: str) -> dict | None:
        """
        Lấy chi tiết một đơn hàng theo ID.

        Returns:
            Raw order dict, hoặc None nếu không tìm thấy.
        """
        ...

    @abstractmethod
    def update_order_status(self, order_id: str, status: str) -> bool:
        """
        Cập nhật trạng thái đơn hàng trên marketplace.

        Args:
            order_id: ID đơn hàng trên sàn.
            status:   Trạng thái mới (ví dụ: 'SHIPPED', 'CANCELLED').

        Returns:
            True nếu thành công.
        """
        ...

    # ------------------------------------------------------------------
    # Abstract: Inventory
    # ------------------------------------------------------------------

    @abstractmethod
    def sync_inventory(self, product_id: str, quantity: int) -> bool:
        """
        Cập nhật số lượng tồn kho của sản phẩm trên marketplace.

        Args:
            product_id: ID sản phẩm trên sàn.
            quantity:   Số lượng tồn kho mới.

        Returns:
            True nếu thành công.
        """
        ...

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> bool:
        """
        Khởi tạo connector: load token từ Document, gọi authenticate().

        Tương đương PHP initialize(ConnectionConfig $config).

        Returns:
            True nếu kết nối thành công.

        Raises:
            frappe.ValidationError: Nếu connection_doc không hợp lệ hoặc authenticate thất bại.
        """
        if not self.connection_doc:
            frappe.throw(f"Không tìm thấy bản ghi kết nối cho sàn {self.get_name()}.")

        # Nạp token từ document một cách an toàn
        self._access_token = self.connection_doc.get_password("access_token") or None
        self._refresh_token = self.connection_doc.get_password("refresh_token") or None
        self._token_expires_at = self.connection_doc.get("token_expires_at") or None

        try:
            self.authenticate()
            self._connected = True

            frappe.logger().info(
                f"[Ecommerce] Connected to {self.get_name()}",
                {"shop_id": self.connection_doc.get("shop_id")},
            )
            return True

        except Exception as e:
            frappe.logger().error(
                f"[Ecommerce] Failed to connect to {self.get_name()}: {e}",
                {"shop_id": self.connection_doc.get("shop_id")},
            )
            frappe.throw(
                f"Kết nối tới {self.get_name()} thất bại: {e}"
            )

    def connect(self, token_data: dict) -> None:
        """
        Kết nối trực tiếp bằng token data (không qua Document).

        Args:
            token_data: Dict với keys: access_token, refresh_token (optional).

        Tương đương PHP connect(TokenDTO $token).
        """
        self._access_token = token_data.get("access_token")
        self._refresh_token = token_data.get("refresh_token")
        self._connected = True

        frappe.logger().info(
            f"[Ecommerce] Connected to {self.get_name()} via token",
            {"shop_id": self.connection_doc.get("shop_id") if self.connection_doc else None},
        )

    def disconnect(self) -> None:
        """
        Ngắt kết nối, xóa token khỏi memory và cache.
        Tương đương PHP disconnect().
        """
        self._connected = False
        self._access_token = None
        self.clear_token_cache()

        frappe.logger().info(f"[Ecommerce] Disconnected from {self.get_name()}")

    def is_connected(self) -> bool:
        """Kiểm tra trạng thái kết nối."""
        return self._connected

    def ensure_connected(self) -> None:
        """Raise exception nếu chưa kết nối."""
        if not self.is_connected():
            frappe.throw(f"Connector {self.get_name()} chưa được kết nối.")

    def get_rate_limit_info(self) -> dict:
        """
        Trả về thông tin rate limit từ lần request gần nhất.
        Subclass có thể override để trả về giá trị thực từ response headers.

        Returns:
            Dict với keys: limit, remaining, reset.
        """
        return {
            "limit":     None,
            "remaining": None,
            "reset":     None,
        }

    # ------------------------------------------------------------------
    # Token refresh (override trong subclass nếu cần)
    # ------------------------------------------------------------------

    def refresh_access_token(self) -> None:
        """
        Làm mới access token bằng refresh token.
        Subclass cần override nếu marketplace hỗ trợ refresh token flow.
        Tương đương PHP refreshAccessToken().
        """
        frappe.logger().info(
            f"[Ecommerce] Token refresh không được implement cho {self.get_name()}"
        )

    # ------------------------------------------------------------------
    # Token cache (dùng frappe.cache thay cho Laravel Cache)
    # ------------------------------------------------------------------

    def cache_token(self, token: str, ttl: int = 3600) -> None:
        """
        Lưu access token vào cache.

        Args:
            token: Access token cần cache.
            ttl:   Thời gian sống (giây), mặc định 3600s.

        Tương đương PHP cacheToken().
        """
        key = self._get_token_cache_key()
        frappe.cache().set_value(key, token, expires_in_sec=ttl)

    def get_cached_token(self) -> str | None:
        """
        Lấy access token từ cache.
        Tương đương PHP getCachedToken().
        """
        key = self._get_token_cache_key()
        return frappe.cache().get_value(key)

    def clear_token_cache(self) -> None:
        """
        Xóa cached token.
        Tương đương PHP clearTokenCache().
        """
        key = self._get_token_cache_key()
        frappe.cache().delete_value(key)

    def _get_token_cache_key(self) -> str:
        """
        Tạo cache key theo pattern: ecommerce.{platform}.{shop_id}.token
        Tương đương PHP getTokenCacheKey().
        """
        shop_id = self.connection_doc.get("shop_id", "unknown") if self.connection_doc else "unknown"
        return f"ecommerce.{self.get_name().lower()}.{shop_id}.token"

    # ------------------------------------------------------------------
    # API request helper (retry + rate limit + token refresh)
    # ------------------------------------------------------------------

    def _make_api_request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
        headers: dict | None = None,
        max_retries: int = 3,
    ) -> dict:
        """
        Gọi API với retry logic, xử lý rate limiting (429) và token expired (401).

        Args:
            method:      HTTP method: 'get', 'post', 'put', 'delete'.
            endpoint:    API endpoint path (relative, e.g. '/orders/list').
            data:        Request body / params.
            headers:     Extra headers.
            max_retries: Số lần retry tối đa.

        Returns:
            Response JSON dưới dạng dict.

        Raises:
            frappe.ValidationError: Sau max_retries thất bại.

        Tương đương PHP makeApiRequest().
        """
        import requests as _requests

        if data is None:
            data = {}
        if headers is None:
            headers = {}

        url = self._build_api_url(endpoint)
        merged_headers = {**self._get_default_headers(), **headers}

        attempt = 0
        last_exception = None

        while attempt < max_retries:
            try:
                resp = _requests.request(
                    method=method.upper(),
                    url=url,
                    json=data if method.lower() in ("post", "put", "patch") else None,
                    params=data if method.lower() == "get" else None,
                    headers=merged_headers,
                    timeout=30,
                )

                if resp.ok:
                    return resp.json()

                # 429 — Rate limited
                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", 60))
                    frappe.logger().warning(
                        f"[Ecommerce] {self.get_name()} rate limited, "
                        f"waiting {retry_after}s",
                        {"endpoint": endpoint},
                    )
                    time.sleep(retry_after)
                    attempt += 1
                    continue

                # 401 — Token expired, thử refresh
                if resp.status_code == 401:
                    self.refresh_access_token()
                    merged_headers = {**self._get_default_headers(), **headers}
                    attempt += 1
                    continue

                # Lỗi khác
                raise Exception(
                    f"API request failed [{resp.status_code}]: {resp.text}"
                )

            except Exception as exc:
                last_exception = exc
                attempt += 1

                if attempt < max_retries:
                    wait = math.pow(2, attempt)  # Exponential backoff: 2s, 4s, 8s
                    frappe.logger().warning(
                        f"[Ecommerce] API request failed, retrying "
                        f"({attempt}/{max_retries}) in {wait:.0f}s",
                        {"endpoint": endpoint, "error": str(exc)},
                    )
                    time.sleep(wait)

        frappe.throw(
            f"API request tới {self.get_name()} thất bại sau {max_retries} lần thử: "
            f"{last_exception}"
        )

    def _build_api_url(self, endpoint: str) -> str:
        """
        Ghép base URL với endpoint.
        Tương đương PHP buildApiUrl().
        """
        return f"{self.get_base_url().rstrip('/')}/{endpoint.lstrip('/')}"

    def _get_default_headers(self) -> dict:
        """
        Trả về default headers cho mỗi request.
        Tương đương PHP getDefaultHeaders().
        """
        headers = {
            "Content-Type": "application/json",
            "Accept":       "application/json",
        }
        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        return headers
