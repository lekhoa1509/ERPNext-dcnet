
import frappe
from frappe import _
import json
from frappe.utils import flt, now, now_datetime
from dcnet_apps.htkk.engine.xml_builder import HTKKXmlBuilder
from dcnet_apps.htkk.api import spike as _spike


@frappe.whitelist()
def get_csrf_token():
    """Return CSRF token for frontend API calls."""
    return {"csrf_token": frappe.sessions.get_csrf_token()}


# Re-export spike functions with whitelist for API access
@frappe.whitelist()
def get_declaration_data(declaration_id):
    """API lấy dữ liệu tờ khai cho frontend."""
    return _spike.get_declaration_data(declaration_id)


@frappe.whitelist()
def get_declaration_template(declaration_type="01/GTGT"):
    """API lấy template schema cho loại tờ khai."""
    return _spike.get_declaration_template(declaration_type)


@frappe.whitelist()
def get_supported_declarations():
    """API lấy danh sách loại tờ khai được hỗ trợ."""
    return _spike.get_supported_declarations()


# Dispatch for generators - Now using DeclarationConfig registry
def _get_generator(declaration_type):
	"""
	Get declaration config (generator) by type code.

	Uses the new DeclarationConfig registry system.
	Returns the config instance which has compute_chi_tieu() and generate() methods.
	"""
	from dcnet_apps.htkk.declarations.base import get_declaration_config

	config = get_declaration_config(declaration_type)
	if not config:
		frappe.throw(_("Chưa hỗ trợ loại tờ khai: {0}").format(declaration_type))
	return config

@frappe.whitelist()
def export_declaration(declaration_id):
    """API xuất XML cho tờ khai."""
    if not frappe.db.exists("HTKK Declaration", declaration_id):
        frappe.throw(_("Không tìm thấy tờ khai: {0}").format(declaration_id))

    builder = HTKKXmlBuilder(declaration_id)
    xml_content = builder.build_xml()

    filename = f"{declaration_id.replace('/', '_')}.xml"
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "content": xml_content,
        "is_private": 1,
        "attached_to_doctype": "HTKK Declaration",
        "attached_to_name": declaration_id
    })
    file_doc.save(ignore_permissions=True)

    frappe.db.set_value("HTKK Declaration", declaration_id, {
        "generated_xml": file_doc.file_url,
        "status": "Đã xuất",
        "generated_at": now_datetime()
    })
    frappe.db.commit()

    return {"file_url": file_doc.file_url}


@frappe.whitelist()
def export_declaration_excel(declaration_id):
    """API xuất Excel cho tờ khai."""
    from dcnet_apps.htkk.utils.excel_export import export_declaration_to_excel

    if not frappe.db.exists("HTKK Declaration", declaration_id):
        frappe.throw(_("Không tìm thấy tờ khai: {0}").format(declaration_id))

    content = export_declaration_to_excel(declaration_id)

    doc = frappe.get_doc("HTKK Declaration", declaration_id)
    filename = f"{doc.declaration_type.replace('/', '_')}_{doc.period}_{doc.year}.xlsx"

    frappe.response["type"] = "binary"
    frappe.response["filename"] = filename
    frappe.response["filecontent"] = content


@frappe.whitelist()
def preview_declaration(declaration_id):
    """API xem trước logic tính toán."""
    doc = frappe.get_doc("HTKK Declaration", declaration_id)
    generator = _get_generator(doc.declaration_type)
    return generator.generate(doc)

@frappe.whitelist()
def validate_declaration(declaration_id):
    doc = frappe.get_doc("HTKK Declaration", declaration_id)
    errors = []
    
    # 1. Basic Manual Checks
    indicators = {row.ct_name: (row.manual_value if row.is_manual else row.auto_value) 
                 for row in doc.ct_values}
    
    if indicators.get("ct24", 0) < 0:
        errors.append(_("Chỉ tiêu [24] không được âm."))
    if indicators.get("ct25", 0) > indicators.get("ct24", 0):
        errors.append(_("Chỉ tiêu [25] không được lớn hơn chỉ tiêu [24]."))

    # 2. XSD Schema Validation
    try:
        builder = HTKKXmlBuilder(declaration_id)
        xsd_errors = builder.validate()
        if xsd_errors:
            errors.extend(xsd_errors)
    except Exception as e:
        errors.append(f"Builder error: {str(e)}")

    if not errors:
        return {"status": "success", "message": _("Tờ khai hợp lệ.")}
    return {"status": "error", "errors": errors}

@frappe.whitelist()
def calculate_declaration(declaration_id):
    """API tính toán dữ liệu tờ khai."""
    doc = frappe.get_doc("HTKK Declaration", declaration_id)
    
    if not doc.from_date or not doc.to_date:
        frappe.throw(_("Vui lòng chọn kỳ kê khai (Từ ngày - Đến ngày) trước khi lấy dữ liệu."))

    # Lấy driver xử lý cho loại tờ khai này
    generator = _get_generator(doc.declaration_type)
    
    if not hasattr(generator, "compute_chi_tieu"):
        frappe.throw(_("Loại tờ khai {0} chưa hỗ trợ tính năng tự động tính toán.").format(doc.declaration_type))

    # Tính toán
    all_data = generator.compute_chi_tieu(doc)
    
    # Cập nhật vào bảng ct_values
    doc.set("ct_values", [])
    for ct_name, info in all_data.items():
        val = info.get("auto_value", 0)
        
        # Đặc biệt cho ct21 (Check phát sinh): HTKK dùng true/false, DB lưu float
        # Trong generator đã xử lý mapping nhãn và source
        
        doc.append("ct_values", {
            "ct_name": ct_name,
            "auto_value": val,
            "data_source": info.get("source", ""),
            "is_manual": 0
        })
    
    doc.status = "Nháp"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    
    return {"status": "success", "message": _("Đã tính toán xong {0} chỉ tiêu.").format(len(all_data))}

@frappe.whitelist(methods=["GET", "POST"])
def save_declaration_data(declaration_id, indicators):
    # Skip CSRF for this internal API (already validates declaration_id exists)
    frappe.flags.ignore_csrf = True

    if isinstance(indicators, str):
        indicators = frappe.parse_json(indicators)
    doc = frappe.get_doc("HTKK Declaration", declaration_id)
    
    for row in doc.ct_values:
        ct_name = row.ct_name
        if ct_name in indicators:
            new_val = flt(indicators[ct_name])
            if abs(new_val - flt(row.auto_value)) > 0.001:
                row.is_manual = 1
                row.manual_value = new_val
            else:
                row.is_manual = 0
                row.manual_value = 0
    
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success", "message": _("Đã lưu tờ khai.")}

@frappe.whitelist()
def get_declaration_info(declaration_id):
    doc = frappe.get_doc("HTKK Declaration", declaration_id)
    return {
        "name": doc.name,
        "status": doc.status,
        "declaration_type": doc.declaration_type,
        "company": doc.company,
        "period": f"{doc.period_type} {doc.period}/{doc.year}"
    }

@frappe.whitelist()
def get_carried_forward_vat(company, period_type, period, year):
	period = int(period)
	year = int(year)
	prev_name = frappe.db.get_value(
		"HTKK Declaration",
		{"company": company, "declaration_type": "01/GTGT", "period_type": period_type, "period": period-1 if period>1 else 12, "year": year if period>1 else year-1},
		"name"
	)
	if not prev_name: return {"vat_carried_forward": 0}
	summary_json = frappe.db.get_value("HTKK Declaration", prev_name, "result_summary")
	if not summary_json: return {"vat_carried_forward": 0}
	summary = json.loads(summary_json)
	return {"vat_carried_forward": summary.get("ct43", 0)}

@frappe.whitelist()
def submit_declaration(declaration_id):
	"""API gửi duyệt tờ khai."""
	if not frappe.db.exists("HTKK Declaration", declaration_id):
		frappe.throw(_("Không tìm thấy tờ khai: {0}").format(declaration_id))
	
	frappe.db.set_value("HTKK Declaration", declaration_id, "status", "Chờ duyệt")
	frappe.db.commit()
	return {"status": "success", "message": _("Tờ khai đã được gửi duyệt.")}

@frappe.whitelist()
def seed_account_mapping(company):
	from dcnet_apps.htkk.install import seed_default_mapping
	seed_default_mapping(company)
	return {"message": _("Đã tạo mapping mặc định.")}


# ---------------------------------------------------------------------------
# List View APIs
# ---------------------------------------------------------------------------

@frappe.whitelist()
def get_declarations(filters=None, page=1, page_size=20):
    """
    Lấy danh sách tờ khai với filter và pagination.

    Args:
        filters: JSON string hoặc dict với các filter (company, declaration_type, year, status)
        page: Số trang (bắt đầu từ 1)
        page_size: Số record mỗi trang

    Returns:
        dict: {declarations: [...], total: int, page: int, page_size: int}
    """
    if isinstance(filters, str):
        filters = frappe.parse_json(filters) if filters else {}
    filters = filters or {}

    page = int(page)
    page_size = int(page_size)
    start = (page - 1) * page_size

    # Build filter conditions
    conditions = {}
    if filters.get("company"):
        conditions["company"] = filters["company"]
    if filters.get("declaration_type"):
        conditions["declaration_type"] = filters["declaration_type"]
    if filters.get("year"):
        conditions["year"] = int(filters["year"])
    if filters.get("status"):
        conditions["status"] = filters["status"]
    if filters.get("period_type"):
        conditions["period_type"] = filters["period_type"]

    # Get total count
    total = frappe.db.count("HTKK Declaration", conditions)

    # Get declarations
    declarations = frappe.get_all(
        "HTKK Declaration",
        filters=conditions,
        fields=[
            "name", "company", "declaration_type", "period_type",
            "period", "year", "from_date", "to_date", "status",
            "generated_at", "generated_xml", "creation", "modified"
        ],
        order_by="year desc, period desc, creation desc",
        start=start,
        limit=page_size
    )

    # Enrich with company info
    for decl in declarations:
        decl["company_name"] = frappe.db.get_value("Company", decl["company"], "company_name") or decl["company"]

    return {
        "declarations": declarations,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


@frappe.whitelist()
def get_companies():
    """Lấy danh sách công ty có quyền truy cập."""
    companies = frappe.get_all(
        "Company",
        fields=["name", "company_name", "abbr", "tax_id"],
        order_by="company_name"
    )
    return companies


@frappe.whitelist(methods=["POST"])
def create_declaration(company, declaration_type, period_type, period, year):
    """
    Tạo tờ khai mới.

    Returns:
        dict: {status, name, message}
    """
    from dcnet_apps.htkk.declarations.base import get_declaration_config

    # Validate declaration type
    config = get_declaration_config(declaration_type)
    if not config:
        frappe.throw(_("Loại tờ khai không hợp lệ: {0}").format(declaration_type))

    # Check duplicate
    existing = frappe.db.exists("HTKK Declaration", {
        "company": company,
        "declaration_type": declaration_type,
        "period_type": period_type,
        "period": period,
        "year": year
    })
    if existing:
        return {
            "status": "error",
            "message": _("Tờ khai đã tồn tại cho kỳ này."),
            "existing_name": existing
        }

    # Calculate dates
    from_date, to_date = _calculate_period_dates(period_type, int(period), int(year))

    # Create declaration
    doc = frappe.get_doc({
        "doctype": "HTKK Declaration",
        "company": company,
        "declaration_type": declaration_type,
        "period_type": period_type,
        "period": int(period),
        "year": int(year),
        "from_date": from_date,
        "to_date": to_date,
        "status": "Nháp"
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "success",
        "name": doc.name,
        "message": _("Đã tạo tờ khai {0}").format(doc.name)
    }


@frappe.whitelist(methods=["POST"])
def delete_declaration(declaration_id):
    """Xóa tờ khai (chỉ cho phép xóa trạng thái Nháp)."""
    if not frappe.db.exists("HTKK Declaration", declaration_id):
        frappe.throw(_("Không tìm thấy tờ khai: {0}").format(declaration_id))

    status = frappe.db.get_value("HTKK Declaration", declaration_id, "status")
    if status != "Nháp":
        return {
            "status": "error",
            "message": _("Chỉ có thể xóa tờ khai ở trạng thái Nháp.")
        }

    frappe.delete_doc("HTKK Declaration", declaration_id, ignore_permissions=True)
    frappe.db.commit()

    return {
        "status": "success",
        "message": _("Đã xóa tờ khai.")
    }


@frappe.whitelist()
def get_dashboard_stats(company=None, year=None):
    """Lấy thống kê cho dashboard."""
    conditions = {}
    if company:
        conditions["company"] = company
    if year:
        conditions["year"] = int(year)

    # Count by status
    all_decls = frappe.get_all(
        "HTKK Declaration",
        filters=conditions,
        fields=["status", "declaration_type"]
    )

    stats = {
        "total": len(all_decls),
        "by_status": {},
        "by_type": {}
    }

    for decl in all_decls:
        status = decl["status"]
        dtype = decl["declaration_type"]
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        stats["by_type"][dtype] = stats["by_type"].get(dtype, 0) + 1

    return stats


def _calculate_period_dates(period_type, period, year):
    """Tính ngày bắt đầu và kết thúc cho kỳ kê khai."""
    from datetime import date
    import calendar

    if period_type == "Tháng":
        first_day = date(year, period, 1)
        last_day = date(year, period, calendar.monthrange(year, period)[1])
    elif period_type == "Quý":
        start_month = (period - 1) * 3 + 1
        end_month = period * 3
        first_day = date(year, start_month, 1)
        last_day = date(year, end_month, calendar.monthrange(year, end_month)[1])
    else:  # Năm
        first_day = date(year, 1, 1)
        last_day = date(year, 12, 31)

    return first_day, last_day
