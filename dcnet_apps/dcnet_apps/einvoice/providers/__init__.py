"""
EInvoice — Provider Strategy Pattern.

Each provider module implements BaseProvider and is registered here.
"""

PROVIDER_MAP = {
    "Matbao": "dcnet_apps.einvoice.providers.matbao.MatbaoProvider",
    "Viettel": "dcnet_apps.einvoice.providers.viettel.ViettelProvider",
    "MISA": "dcnet_apps.einvoice.providers.misa.MisaProvider",
}


def get_provider_class(provider_type: str):
    """Return the provider class for the given provider_type string."""
    import importlib

    dotted_path = PROVIDER_MAP.get(provider_type)
    if not dotted_path:
        import frappe
        frappe.throw(f"Provider type '{provider_type}' chưa được hỗ trợ.")

    module_path, class_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)
