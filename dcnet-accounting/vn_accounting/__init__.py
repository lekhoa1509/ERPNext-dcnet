__version__ = "1.3.2"


def _patch_get_chart():
    """Monkey-patch get_chart để ERPNext tìm được tree data của VN COA templates.

    get_chart không phải whitelisted method nên không thể override qua hooks.
    Patch ở đây đảm bảo chạy khi vn_accounting module được import.

    Hoạt động vì các module ERPNext dùng lazy import (from ... import get_chart
    bên trong function body) → tại thời điểm gọi, Python lấy attribute từ module
    đã cached trong sys.modules → nhận được patched version.
    """
    try:
        import erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts as _coa_module
        from vn_accounting.chart_of_accounts.coa_registry import get_chart as _vn_get_chart

        _coa_module.get_chart = _vn_get_chart
    except ImportError:
        pass


_patch_get_chart()


def _patch_budget_variance_locale():
    """Fix ERPNext Budget Variance Report locale mismatch.

    build_budget_map stores month keys via strftime("%B") (always English),
    but build_report_data looks them up via formatdate(d, "MMMM") which uses
    Babel + user locale → "tháng 1" for VN user → KeyError → every cell = 0.

    Patch get_months_between to always return English month names.
    """
    try:
        import erpnext.accounts.report.budget_variance_report.budget_variance_report as _bvr
        from frappe.utils import add_months

        def _get_months_between_en(from_date, to_date):
            months = []
            current = from_date
            while current <= to_date:
                months.append(current.strftime("%B"))
                current = add_months(current, 1)
            return months

        _bvr.get_months_between = _get_months_between_en
    except ImportError:
        pass


_patch_budget_variance_locale()
