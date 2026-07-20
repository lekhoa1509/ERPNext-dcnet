import frappe
import os
import json
from dcnet_apps.htkk.engine.auto_detect import auto_detect_indicators
from dcnet_apps.htkk.formula_parser import HTKKFormulaParser
from frappe.utils import flt

@frappe.whitelist()
def run_auto_detect(file_url=None):
    if not file_url:
        file_path = frappe.get_app_path("dcnet_apps", "htkk", "engine", "test_sample.xls")
    else:
        from frappe.utils.file_manager import get_file_path
        file_path = get_file_path(file_url.split("/")[-1])
        if not os.path.exists(file_path):
            file_path = frappe.get_site_path(file_url.lstrip("/"))

    if not os.path.exists(file_path):
        frappe.throw(f"File không tồn tại: {file_path}")

    results = auto_detect_indicators(file_path)
    return results

@frappe.whitelist()
def get_declaration_data(declaration_id):
    """
    Trả về dữ liệu thô (JSON phẳng) cho tờ khai và thông tin công ty.
    Phục vụ cho giao diện HTML/Tailwind mới.
    """
    if not frappe.db.exists("HTKK Declaration", declaration_id):
        frappe.throw(f"Không tìm thấy tờ khai: {declaration_id}")

    doc = frappe.get_doc("HTKK Declaration", declaration_id)
    company = frappe.get_doc("Company", doc.company)

    # Sử dụng registry để lấy generator phù hợp với loại tờ khai
    from dcnet_apps.htkk.api import _get_generator
    generator = _get_generator(doc.declaration_type)

    # generate() trả về dict với chi_tieu, sources, phu_luc
    data = generator.generate(doc)

    return {
        "doc": {
            "name": doc.name,
            "status": doc.status,
            "type": doc.declaration_type,
            "period": f"{doc.period_type} {doc.period}/{doc.year}"
        },
        "company": {
            "name": company.company_name,
            "tax_id": company.tax_id,
            "address": getattr(company, 'address', 'N/A'),
            "email": getattr(company, 'email', 'N/A'),
            "phone": getattr(company, 'phone_no', 'N/A')
        },
        "indicators": data.get("chi_tieu", {}),
        "indicators_auto": {row.ct_name: row.auto_value for row in doc.ct_values},
        "sources": data.get("sources", {}),
        "appendices": data.get("phu_luc", {})
    }

import gzip
import base64
from dcnet_apps.htkk.engine.data_fetcher import get_source_documents

@frappe.whitelist()
def save_declaration_state(declaration_id, state_json):
    """
    Saves the UI state as a compressed Gzip file and cleans up old versions.
    """
    if not frappe.db.exists("HTKK Declaration", declaration_id):
        frappe.throw("Declaration not found")
        
    doc = frappe.get_doc("HTKK Declaration", declaration_id)
    
    # 1. Compress state
    compressed_data = gzip.compress(state_json.encode('utf-8'))
    
    # 2. Create file and attach
    filename = f"state_{doc.name}_{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}.gz"
    _file = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "attached_to_doctype": "HTKK Declaration",
        "attached_to_name": doc.name,
        "content": compressed_data,
        "is_private": 1
    })
    _file.save()
    
    # 3. Cleanup logic: Keep only the last 5 state cycles to save storage
    old_files = frappe.get_all("File", filters={
        "attached_to_doctype": "HTKK Declaration",
        "attached_to_name": doc.name,
        "file_name": ["like", "state_%.gz"]
    }, order_by="creation desc")
    
    if len(old_files) > 5:
        to_delete = old_files[5:]
        for f in to_delete:
            frappe.delete_doc("File", f.name)
    
    # 4. Update doc
    doc.state_file = _file.file_url
    doc.state_version += 1
    doc.save()
    
    return {"message": "State saved successfully", "version": doc.state_version}

@frappe.whitelist()
def get_latest_declaration_state(declaration_id):
    """
    Retrieves and decompresses the most recent UI state for a declaration.
    """
    latest_file = frappe.db.get_value("File", {
        "attached_to_doctype": "HTKK Declaration",
        "attached_to_name": declaration_id,
        "file_name": ["like", "state_%.gz"]
    }, ["name", "file_name", "creation"], order_by="creation desc", as_dict=True)
    
    if not latest_file:
        return None
        
    file_doc = frappe.get_doc("File", latest_file.name)
    content = file_doc.get_content()
    
    try:
        decompressed = gzip.decompress(content).decode('utf-8')
        return {
            "state": json.loads(decompressed),
            "timestamp": latest_file.creation
        }
    except Exception as e:
        frappe.log_error(f"HTKK State Restore Error: {str(e)}")
        return None

@frappe.whitelist()
def get_drilldown_data(declaration_id, indicator_code):
    """
    Returns detailed source documents contributing to a specific indicator.
    """
    return get_source_documents(declaration_id, indicator_code)

@frappe.whitelist()
def update_indicator_value(declaration_id, indicator_code, value, is_manual=True):
    """
    Updates a specific indicator value in the child table.
    """
    doc = frappe.get_doc("HTKK Declaration", declaration_id)
    found = False
    for row in doc.ct_values:
        if row.ct_name == indicator_code:
            row.manual_value = flt(value)
            row.is_manual = is_manual
            found = True
            break

    if not found:
        doc.append("ct_values", {
            "ct_name": indicator_code,
            "manual_value": flt(value),
            "is_manual": is_manual
        })

    doc.save()
    return {"status": "success"}


@frappe.whitelist()
def get_supported_declarations():
    """
    Trả về danh sách các loại tờ khai được hỗ trợ.
    """
    from dcnet_apps.htkk.declarations import get_supported_declarations as get_list
    return get_list()


@frappe.whitelist()
def get_declaration_template(declaration_type="01/GTGT"):
    """
    Trả về schema template đầy đủ cho tờ khai, bao gồm:
    - fields: Danh sách các chỉ tiêu với metadata
    - formulas: Công thức tính toán tự động
    - sections: Cấu trúc phân nhóm chỉ tiêu
    - appendices: Danh sách phụ lục
    - calculation_order: Thứ tự tính toán (topological sort)

    Lấy title, subtitle, sections, appendices từ DeclarationConfig.
    Auto-generated từ XSD của Tổng cục thuế.
    """
    from dcnet_apps.htkk.declarations.base import get_declaration_config

    # Get config từ registry mới
    config = get_declaration_config(declaration_type)
    if not config:
        frappe.throw(f"Không hỗ trợ loại tờ khai: {declaration_type}")

    xsd_filename = config.xsd_file

    # frappe.get_app_path converts filenames to lowercase, so we build path manually
    xsd_dir = frappe.get_app_path(
        "dcnet_apps", "htkk", "schemas", "htkk_template", "xsd"
    )
    xsd_path = os.path.join(xsd_dir, xsd_filename)

    if not os.path.exists(xsd_path):
        frappe.throw(f"Không tìm thấy schema: {xsd_filename}")

    with open(xsd_path, "r", encoding="utf-8") as f:
        xsd_content = f.read()

    parser = HTKKFormulaParser()
    result = parser.parse_xsd(xsd_content)

    # Convert dataclass fields to dict for JSON serialization
    fields_dict = []
    for field in result["fields"]:
        fields_dict.append({
            "element": field.element,
            "indicator": field.indicator,
            "label": field.label,
            "formula": field.formula,
            "condition": field.condition,
            "dependencies": field.dependencies,
            "data_type": field.data_type,
        })

    # Get calculation order
    calc_order = parser.get_calculation_order(result["formulas"])

    # Generate JS calculator code
    js_calculator = parser.generate_js_calculator(result["formulas"])

    # Period mapping
    period_map = {
        "monthly": "Tháng",
        "quarterly": "Quý",
        "yearly": "Năm",
    }

    return {
        "declaration_type": declaration_type,
        "name": config.name,
        "title": config.title or config.name,
        "subtitle": config.subtitle or "",
        "short_name": config.short_name,
        "period": period_map.get(config.period, "Quý"),
        "circular": config.circular,
        "has_appendices": config.has_appendices,
        "appendices": config.appendices,  # NEW: Danh sách phụ lục từ config
        "fields": fields_dict,
        "formulas": result["formulas"],
        "calculation_order": calc_order,
        "js_calculator": js_calculator,
        "sections": config.sections,  # Lấy từ config thay vì hardcoded
    }



# NOTE: _get_form_sections() has been removed.
# Sections are now defined in each DeclarationConfig class (e.g., VAT01GTGT.sections)
# and accessed via config.sections in get_declaration_template().
