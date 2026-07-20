import frappe
from frappe.model import no_value_fields

from dcnet_migrate.import_auto.services.utils import normalize_key


DOCTYPE_ORDER = {
    "UOM": 1,
    "Item Group": 2,
    "Bank": 3,
    "Account": 4,
    "Branch": 5,
    "Department": 6,
    "Warehouse": 7,
    "Bank Account": 8,
    "Customer Group": 9,
    "Supplier Group": 10,
    "Customer": 11,
    "Supplier": 12,
    "Item": 13,
    "Employee": 14,
    "Project": 15,
}

IMPORT_FILE_HINTS = [
    # --- Danh mục bắt buộc (master data, auto-import) ---
    (("danh_sach_don_vi_tinh",), "UOM", True, "Đơn vị tính có DocType UOM tương ứng."),
    (("danh_sach_nhom_vat_tu", "nhom_vat_tu_hang_hoa_dich_vu"), "Item Group", True, "Nhóm VTHH có thể import vào Item Group."),
    (("danh_sach_ngan_hang",), "Bank", True, "Danh sách ngân hàng có thể import vào Bank."),
    (("danh_sach_kho",), "Warehouse", True, "Kho cần Company trước khi import."),
    (("danh_sach_khach_hang",), "Customer", True, "Khách hàng có thể import vào Customer."),
    (("danh_sach_nha_cung_cap",), "Supplier", True, "Nhà cung cấp có thể import vào Supplier."),
    (("danh_sach_nhan_vien",), "Employee", True, "Nhân viên có thể import vào Employee. Cần chọn Company trước."),
    (("danh_sach_hang_hoa_dich_vu",), "Item", True, "Hàng hóa dịch vụ cần UOM và Item Group trước."),
    (("danh_sach_tai_khoan_ngan_hang",), "Bank Account", True, "Tài khoản ngân hàng cần Bank và Company trước."),
    (("danh_sach_co_cau_to_chuc",), "Department", True, "Cơ cấu tổ chức có thể map sang Department nếu đã chọn Company."),
    (("danh_sach_cong_trinh",), "Project", True, "Công trình có thể map sang Project."),
    (("danh_sach_he_thong_tai_khoan", "he_thong_tai_khoan"), "Account", True, "Hệ thống tài khoản — dùng Smart Import (AI) để tự build cây Account: AI sẽ topo-sort, tạo các root VN (Tài sản/Nợ phải trả/Vốn chủ sở hữu/Thu nhập/Chi phí) nếu thiếu, và ghép \" - {abbr}\" vào parent_account theo Company."),

    # --- Danh mục nhóm KH/NCC (không hỗ trợ — DCNET tách riêng Customer Group / Supplier Group) ---
    (("danh_sach_nhom_khach_hang_nha_cung_cap",), None, False, "Phần mềm nguồn có thể dùng chung nhóm KH/NCC, DCNET tách Customer Group và Supplier Group."),

    # --- File chứng từ phát sinh (Trường hợp 1 + 2) — xử lý bởi trang Misa Migration ---
    (("so_nhat_ky_chung",), None, False, "Sổ nhật ký chung — nguồn gốc mọi chứng từ phát sinh. Thả vào trang Misa Migration để xử lý."),
    (("bang_ke_hoa_don",), None, False, "Bảng kê hóa đơn bán ra/mua vào — chi tiết dòng hàng cho hóa đơn. Thả vào trang Misa Migration để xử lý."),
    (("so_chi_tiet_vat_tu_hang_hoa",), None, False, "Sổ chi tiết vật tư hàng hóa — chi tiết nhập/xuất kho. Thả vào trang Misa Migration để xử lý."),

    # --- File đặc thù Trường hợp 2 (migrate theo tháng) — xử lý bởi trang Misa Migration ---
    (("bang_can_doi_tai_khoan_mau_quan_tri",), None, False, "Bảng cân đối tài khoản (mẫu quản trị) — dùng cho migrate theo tháng, cột Đầu kỳ ghi sổ dư đầu. Thả vào trang Misa Migration để xử lý."),
    (("tong_hop_ton_kho",), None, False, "Tổng hợp tồn kho — dùng đối chiếu tồn cuối sau migrate. Thả vào trang Misa Migration để xử lý."),

    # --- File số dư đầu kỳ (Trường hợp 1) — xử lý bởi trang Misa Migration ---
    (("danh_sach_so_du_tai_khoan",), None, False, "Số dư đầu kỳ tổng hợp tất cả tài khoản — nguồn duy nhất ghi sổ đầu kỳ. Thả vào trang Misa Migration để xử lý."),
    (("danh_sach_cong_no_khach_hang",), None, False, "Chi tiết công nợ phải thu (TK 131) theo từng khách hàng. Thả vào trang Misa Migration để xử lý."),
    (("danh_sach_cong_no_nha_cung_cap",), None, False, "Chi tiết công nợ phải trả (TK 331) theo từng NCC. Thả vào trang Misa Migration để xử lý."),
    (("danh_sach_cong_no_nhan_vien",), None, False, "Tạm ứng (TK 141) theo từng nhân viên. Thả vào trang Misa Migration để xử lý."),
    (("danh_sach_ton_kho_vthh",), None, False, "Tồn kho đầu kỳ theo kho - vật tư hàng hóa. Thả vào trang Misa Migration để xử lý."),
    (("danh_sach_nhap_so_du_tai_khoan_ngan_hang",), None, False, "Số dư đầu kỳ từng tài khoản ngân hàng. Thả vào trang Misa Migration để xử lý."),
    (("danh_sach_chi_phi_tra_truoc_dau_ky",), None, False, "Chi phí trả trước (TK 242) đầu kỳ. Thả vào trang Misa Migration để xử lý."),
    (("danh_sach_tai_san_co_dinh_dau_ky",), None, False, "TSCĐ đầu kỳ (nguyên giá, hao mòn lũy kế). Thả vào trang Misa Migration để xử lý."),
    (("danh_sach_cong_cu_dung_cu_dau_ky",), None, False, "CCDC đầu kỳ. Thả vào trang Misa Migration để xử lý."),

    # --- Danh mục bổ trợ tách riêng (nên có, cấu hình thủ công trong ERPNext) ---
    (("danh_sach_loai_tai_san_co_dinh",), None, False, "Loại TSCĐ — tham khảo để cấu hình Asset Category thủ công trong ERPNext."),
    (("danh_sach_loai_cong_cu_dung_cu",), None, False, "Loại CCDC — tham khảo để cấu hình Asset Category thủ công trong ERPNext."),
    (("doi_tuong_tap_hop_chi_phi",), None, False, "Đối tượng tập hợp chi phí (trung tâm chi phí) — cấu hình Cost Center thủ công trong ERPNext."),

    # --- Danh mục Misa nội bộ — không có mapping ERPNext, tự bỏ qua ---
    (("danh_sach_bieu_thue", "bieu_tinh_thue", "tai_khoan_ket_chuyen", "tai_khoan_ngam_dinh", "ky_hieu_cham_cong", "loai_chung_tu", "loai_tien", "ma_thong_ke", "muc_thuchi", "khoan_muc_chi_phi"), None, False, "Danh mục Misa nội bộ — không có mapping ERPNext tương ứng trong scope import tự động."),
]

IMPORT_COLUMN_MAPPINGS = {
    "UOM": {
        "đơn vị tính": "uom_name",
        "mô tả": "description",
    },
    "Item Group": {
        "tên nhóm vật tư hàng hóa dịch vụ": "item_group_name",
        "tên nhóm vật tư": "item_group_name",
    },
    "Bank": {
        "tên đầy đủ": "bank_name",
        "tên viết tắt": "bank_name",
    },
    "Warehouse": {
        "tên kho": "warehouse_name",
        "địa chỉ": "address_line_1",
    },
    "Customer Group": {
        # Source file lists ONE shared group list for both Customer and
        # Supplier ("Danh_sach_nhom_khach_hang_nha_cung_cap.xlsx" — no column
        # distinguishes which rows are customer-only vs supplier-only), so
        # the same header feeds both Customer Group and Supplier Group.
        # Keys here must already be normalize_key()'d (no punctuation) since
        # get_direct_mappings() looks up normalize_key(header) directly.
        "tên nhóm khách hàng nhà cung cấp": "customer_group_name",
        "tên nhóm khách hàng": "customer_group_name",
    },
    "Supplier Group": {
        "tên nhóm khách hàng nhà cung cấp": "supplier_group_name",
        "tên nhóm nhà cung cấp": "supplier_group_name",
    },
    "Customer": {
        "tên khách hàng": "customer_name",
        "mã số thuế cccd chủ hộ": "tax_id",
        "địa chỉ": "customer_details",
    },
    "Supplier": {
        "tên nhà cung cấp": "supplier_name",
        "mã số thuế cccd chủ hộ": "tax_id",
        "địa chỉ": "supplier_details",
    },
    "Item": {
        "mã": "item_code",
        "tên": "item_name",
        "nhóm vthh": "item_group",
        "đơn vị tính chính": "stock_uom",
        "số lượng tồn": "opening_stock",
        "số lượng tồn tối thiểu": "safety_stock",
        "mô tả": "description",
    },
    "Bank Account": {
        "số tài khoản": "bank_account_no",
        "tên ngân hàng": "bank",
        "chủ tài khoản": "account_name",
        "tên chi nhánh ngân hàng": "branch_code",
    },
    "Employee": {
        "tên nhân viên": "employee_name",
        "bộ phận": "department",
        "phòng ban": "department",
        "tên đơn vị": "department",
        "chức danh": "designation",
        "chức vụ": "designation",
        "ngày sinh": "date_of_birth",
        "giới tính": "gender",
        "email": "personal_email",
        "số điện thoại": "cell_number",
        "địa chỉ": "current_address",
    },
    "Department": {
        # v1 flat file header. v2 (theo chi nhánh) multi-sheet workbook uses
        # "Tên phòng ban" on every per-branch department sheet — the branch
        # itself is no longer represented as a Department (see "Branch"
        # mapping below), it's linked via the `branch` field instead
        # (dcnet_organization's Department.branch custom field).
        "tên đơn vị": "department_name",
        "tên phòng ban": "department_name",
        "mã đơn vị": "department_name",
    },
    "Branch": {
        # Branch-master sheet ("Chi nhánh") — each row is a real Branch
        # record (dcnet_organization model: Company -> Branch -> Department),
        # not a fake parent Department.
        "tên chi nhánh": "branch",
        "mã đơn vị": "branch",
    },
    "Project": {
        "tên công trình": "project_name",
        "ngày bắt đầu": "expected_start_date",
        "ngày kết thúc": "expected_end_date",
        "dự toán": "estimated_costing",
    },
}

DOCTYPE_DEFAULTS = {
    "Customer Group": {"is_group": 0},
    "Supplier Group": {"is_group": 0},
    "Customer": {"customer_type": "Company", "customer_group": "All Customer Groups", "territory": "All Territories"},
    "Supplier": {"supplier_type": "Company", "supplier_group": "All Supplier Groups"},
    "Item": {"is_stock_item": 1},
    "Warehouse": {"is_group": 0},
    "Department": {"is_group": 0},
    "Bank Account": {"is_company_account": 1},
    "Employee": {"status": "Active"},
    "Project": {"status": "Open"},
}

# Danh_sach_co_cau_to_chuc_theo_chi_nhanh.xlsx (v2) sheet name → chi nhánh
# label (matching the "Tên chi nhánh" value on the DEPARTMENT_BRANCH_MASTER_SHEET
# row — that's the Branch record's name, since Mã đơn vị is never used as the
# record's name in practice). Each sheet becomes its own "Import Auto File"
# row (see processor.scan_files multi-sheet support) so get_default_values
# can look up the right Branch to link a per-branch sheet's Departments to.
#
# Org model (matches dcnet_organization, see organization_customization.py):
#   Company ──< Branch ──< Department ──< Designation
# A Company has many Branches; a Branch has many Departments (Department.branch,
# optional — company-level departments with no specific branch just leave it
# unset). The branch-master sheet therefore imports into the real "Branch"
# doctype, never into Department.
#
# The workbook's "Công ty" sheet is company info, not a department — the
# Company doctype record already exists, so that sheet must never resolve to
# any doctype at all (see infer_import_file()).
DEPARTMENT_COMPANY_SHEET = "Công ty"
DEPARTMENT_BRANCH_MASTER_SHEET = "Chi nhánh"
DEPARTMENT_BRANCH_SHEETS = {
    "PB - Trụ Sở HCM": "Trụ Sở Hồ Chí Minh",
    "PB - CN Hà Nội": "Chi Nhánh Hà Nội",
    "PB - CN Đà Nẵng": "Chi Nhánh Đà Nẵng",
    "PB - TT Công Nghệ": "Trung Tâm Công Nghệ",
}


def resolve_branch_by_label(label: str, company: str | None) -> str | None:
    """Look up an already-imported Branch's actual (possibly autoname-
    suffixed) name by its chi nhánh label — ``label`` here is "whatever
    value DEPARTMENT_BRANCH_SHEETS was keyed with". Returns None if not
    created yet — caller either blocks the per-branch sheet import (see
    importer._apply_department_branch_link) or, during Analyze, leaves
    Department.branch unset (optional field).

    ``company`` is accepted for API symmetry with other resolvers but is
    unused: ERPNext's standard "Branch" doctype has no ``company`` field
    (it's just a name), so filtering by it raises
    ``Unknown column 'company' in 'WHERE'``.
    """
    if not label:
        return None
    if frappe.db.exists("Branch", label):
        return label
    match = frappe.db.get_value("Branch", {"branch": label}, "name")
    if match:
        return match
    return frappe.db.get_value("Branch", {"name": ("like", f"{label} - %")}, "name")


def infer_import_file(file_name: str, sheet_name: str | None = None) -> dict:
    if sheet_name == DEPARTMENT_COMPANY_SHEET:
        # Filename hints below match the whole "co cau to chuc" workbook, but
        # this one sheet lists the company itself (already exists as a
        # Company doctype record) — never route it to Department.
        return {
            "target_doctype": None,
            "is_supported": False,
            "known_file_type": True,
            "matched_pattern": None,
            "note": "Sheet danh sách công ty — công ty đã tồn tại trong hệ thống, bỏ qua khi import.",
            "import_order": 999,
        }
    if sheet_name == DEPARTMENT_BRANCH_MASTER_SHEET:
        # Branch-master sheet — real "Branch" records, not Department.
        return {
            "target_doctype": "Branch",
            "is_supported": True,
            "known_file_type": True,
            "matched_pattern": None,
            "note": "Sheet danh sách chi nhánh — import vào DocType Branch.",
            "import_order": DOCTYPE_ORDER.get("Branch", 999),
        }
    key = normalize_key(file_name).replace(" ", "_")
    for patterns, doctype, is_supported, note in IMPORT_FILE_HINTS:
        matched_pattern = next(
            (pattern for pattern in patterns if _matches_file_pattern(key, pattern)),
            None,
        )
        if matched_pattern:
            return {
                "target_doctype": doctype,
                "is_supported": is_supported,
                "known_file_type": True,
                "matched_pattern": matched_pattern,
                "note": note,
                "import_order": DOCTYPE_ORDER.get(doctype, 999) if is_supported else 999,
            }
    return {
        "target_doctype": None,
        "is_supported": False,
        "known_file_type": False,
        "matched_pattern": None,
        "note": "AI chưa xác định được danh mục DCNET tương ứng.",
        "import_order": 999,
    }


def _matches_file_pattern(file_key: str, pattern: str) -> bool:
    bounded_key = f"_{file_key}_"
    bounded_pattern = f"_{pattern}_"
    return file_key == pattern or file_key.startswith(f"{pattern}_") or bounded_pattern in bounded_key


def get_doctype_schema(doctype: str) -> dict:
    meta = frappe.get_meta(doctype)
    fields = []
    for df in meta.fields:
        if df.fieldtype in no_value_fields or df.fieldtype == "Table":
            continue
        if df.read_only and not df.reqd:
            continue
        fields.append(
            {
                "fieldname": df.fieldname,
                "label": df.label,
                "fieldtype": df.fieldtype,
                "options": df.options,
                "required": bool(df.reqd),
            }
        )

    return {
        "doctype": doctype,
        "module": meta.module,
        "fields": fields,
        "required_fields": [field["fieldname"] for field in fields if field["required"]],
        "defaults": DOCTYPE_DEFAULTS.get(doctype, {}),
    }


def field_exists(doctype: str, fieldname: str) -> bool:
    if fieldname == "name":
        return True
    return bool(frappe.get_meta(doctype).get_field(fieldname))


def get_default_values(doctype: str, company: str | None = None, sheet_name: str | None = None) -> dict:
    defaults = dict(DOCTYPE_DEFAULTS.get(doctype, {}))
    if doctype == "Department" and sheet_name in DEPARTMENT_BRANCH_SHEETS:
        branch = resolve_branch_by_label(DEPARTMENT_BRANCH_SHEETS[sheet_name], company)
        if branch:
            defaults["branch"] = branch
        # Chi nhánh chưa được import thì để trống branch — phòng ban vẫn
        # thuộc company bình thường (branch là optional trên Department).
    if company and field_exists(doctype, "company"):
        defaults["company"] = company
    return {key: value for key, value in defaults.items() if field_exists(doctype, key)}


def get_direct_mappings(doctype: str, headers: list[str]) -> list[dict]:
    configured = IMPORT_COLUMN_MAPPINGS.get(doctype, {})
    mappings = []
    for header in headers:
        fieldname = configured.get(normalize_key(header))
        if fieldname and field_exists(doctype, fieldname):
            mappings.append(
                {
                    "source_column": header,
                    "target_field": fieldname,
                    "default": None,
                    "transform": "direct",
                }
            )
    if doctype == "Department":
        mappings = _prefer_code_column(mappings, "department_name")
    elif doctype == "Branch":
        mappings = _prefer_code_column(mappings, "branch")
    return mappings


def _prefer_code_column(mappings: list[dict], target_field: str) -> list[dict]:
    """Mã đơn vị is a stable code but not human-readable; the Vietnamese
    label header ("Tên chi nhánh"/"Tên phòng ban"/"Tên đơn vị") is what
    people actually recognize. When a header maps both a code column and a
    label column to the same target field, keep ONLY the label mapping —
    otherwise the imported record's name reads as a cryptic code like
    "KD_HDG" instead of "Kinh Doanh Hải Dương". Falls back to the code only
    when there's no label column in the sheet at all.

    Note: an earlier version tried to keep the code as primary with the
    label as a `fallback_column` for blank-code rows, but the AI-plan
    executor (smart_planner.py's field_map rendering) never reads
    `fallback_column` — only the legacy importer.py pipeline did — so that
    fallback silently never applied on the path actually used for imports.
    """
    name_entries = [m for m in mappings if m["target_field"] == target_field]
    if len(name_entries) < 2:
        return mappings
    label_entry = next(
        (m for m in name_entries if normalize_key(m["source_column"]) != "mã đơn vị"), None
    )
    if not label_entry:
        return mappings
    return [m for m in mappings if m["target_field"] != target_field or m is label_entry]


def missing_required_context(doctype: str, company: str | None) -> str | None:
    if field_exists(doctype, "company") and not company:
        return "Cần chọn Company trước khi import danh mục này."
    return None
