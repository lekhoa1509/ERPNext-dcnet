"""Cash Flow Forecast Aggregator.

Discovers all providers via frappe.get_hooks("cash_flow_forecast_providers"),
calls each, validates entries, and returns consolidated forecast data.
"""
import frappe
from datetime import datetime

VALID_DIRECTIONS = ("inflow", "outflow")
VALID_CONFIDENCE = ("overdue", "committed", "probable", "possible")
REQUIRED_FIELDS = ("expected_date", "amount", "direction", "category",
                   "confidence", "source_doctype", "source_name")


def validate_entry(entry, provider_path):
    """Validate a single ForecastEntry dict. Returns entry if valid, None if invalid."""
    if not isinstance(entry, dict):
        return None

    for field in REQUIRED_FIELDS:
        if field not in entry or entry[field] is None:
            _log_invalid(provider_path, entry, f"Missing required field: {field}")
            return None

    if not isinstance(entry["amount"], (int, float)):
        _log_invalid(provider_path, entry, f"amount must be numeric, got {type(entry['amount'])}")
        return None
    if entry["amount"] <= 0:
        _log_invalid(provider_path, entry, f"amount must be > 0, got {entry['amount']}")
        return None

    if entry["direction"] not in VALID_DIRECTIONS:
        _log_invalid(provider_path, entry, f"direction must be one of {VALID_DIRECTIONS}")
        return None
    if entry["confidence"] not in VALID_CONFIDENCE:
        _log_invalid(provider_path, entry, f"confidence must be one of {VALID_CONFIDENCE}")
        return None

    try:
        datetime.strptime(str(entry["expected_date"]), "%Y-%m-%d")
    except ValueError:
        _log_invalid(provider_path, entry, f"expected_date must be YYYY-MM-DD, got {entry['expected_date']}")
        return None

    return entry


def _log_invalid(provider_path, entry, reason):
    """Log validation failure. Uses frappe.log_error if available, else pass."""
    try:
        frappe.log_error(
            title="Cash Flow Forecast: invalid entry",
            message=f"Provider: {provider_path}\nReason: {reason}\nEntry: {entry}",
        )
    except Exception:
        pass  # Unit tests run without frappe context


def get_all_forecast_entries(filters):
    """Collect and validate forecast entries from all registered providers.

    Args:
        filters: dict with keys: company (str), from_date (str), to_date (str),
                 confidence (list[str], optional)

    Returns:
        tuple: (entries: list[dict], errors: list[dict])
    """
    entries = []
    errors = []

    for method_path in frappe.get_hooks("cash_flow_forecast_providers"):
        try:
            fn = frappe.get_attr(method_path)
            raw = fn(filters)
            if not isinstance(raw, (list, tuple)):
                errors.append({"provider": method_path, "error": "Provider did not return a list"})
                continue
            for entry in raw:
                validated = validate_entry(entry, method_path)
                if validated:
                    validated["_provider"] = method_path
                    entries.append(validated)
        except Exception as e:
            errors.append({"provider": method_path, "error": str(e)})
            frappe.log_error(
                title=f"Cash flow provider failed: {method_path}",
                message=str(e),
            )

    return entries, errors
