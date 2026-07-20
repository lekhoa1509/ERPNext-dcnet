"""
DCNet Ecommerce — Marketplace Connector Registry.

Mỗi connector module implement BaseConnector và được đăng ký tại đây.
Thêm sàn TMĐT mới bằng cách thêm entry vào CONNECTOR_MAP.
"""

CONNECTOR_MAP = {
    "Shopee": "dcnet_apps.dcnet_ecommerce.connectors.shopee.ShopeeConnector",
    "Lazada": "dcnet_apps.dcnet_ecommerce.connectors.lazada.LazadaConnector",
    "TikTok Shop": "dcnet_apps.dcnet_ecommerce.connectors.tiktok.TikTokShopConnector",
    "Woocommerce": "dcnet_apps.dcnet_ecommerce.connectors.woocommerce.WooCommerceConnector",
}


def get_connector_class(platform: str):
    """
    Trả về class connector cho platform chỉ định.

    Args:
        platform: Tên sàn TMĐT (key trong CONNECTOR_MAP), ví dụ "Shopee".

    Returns:
        Connector class (chưa khởi tạo).

    Raises:
        frappe.ValidationError: Nếu platform chưa được hỗ trợ.
    """
    import importlib

    dotted_path = CONNECTOR_MAP.get(platform)
    if not dotted_path:
        import frappe
        frappe.throw(f"Sàn TMĐT '{platform}' chưa được hỗ trợ.")

    module_path, class_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def get_connector(connection_doc):
    """
    Khởi tạo và trả về connector instance từ một Frappe Document.

    Args:
        connection_doc: Document 'DCNet Marketplace Connection' (hoặc tương đương).

    Returns:
        Instance của connector tương ứng với platform.
    """
    platform = connection_doc.platform
    cls = get_connector_class(platform)
    return cls(connection_doc)
