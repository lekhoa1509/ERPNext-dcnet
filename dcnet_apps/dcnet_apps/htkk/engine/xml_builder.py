"""
HTKK XML Builder - Xuất XML tờ khai thuế.

Sử dụng Declaration Registry để tìm XSD/XML template files,
không còn phụ thuộc vào HTKK XML Template DocType.
"""

import os
import re
import frappe
from lxml import etree

from dcnet_apps.htkk.declarations.base import get_declaration_config


class HTKKXmlBuilder:
    """Builder xuất XML tờ khai theo chuẩn HTKK."""

    def __init__(self, declaration_id):
        self.doc = frappe.get_doc("HTKK Declaration", declaration_id)
        self.declaration_type = get_declaration_config(self.doc.declaration_type)
        if not self.declaration_type:
            frappe.throw(f"Loại tờ khai không được hỗ trợ: {self.doc.declaration_type}")

        self.xml_root = None
        self.nsmap = None

    def build_xml(self):
        """Build XML content từ declaration data."""
        # 1. Load XML mẫu
        xml_template_path = self._find_xml_template()

        if not xml_template_path or not os.path.exists(xml_template_path):
            frappe.throw(f"Không tìm thấy file XML mẫu cho {self.declaration_type.code}")

        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_template_path, parser)
        self.xml_root = tree.getroot()

        # Kiểm tra root hợp lệ
        root_tag = etree.QName(self.xml_root).localname
        if root_tag == 'Sections':
            frappe.throw(
                f"File XML mẫu ({os.path.basename(xml_template_path)}) không phải tờ khai hợp lệ. "
                "Root là 'Sections' thay vì 'HSoThueDTu'."
            )

        # HTKK XML yêu cầu namespace chuẩn
        ns = "http://kekhaithue.gdt.gov.vn/TKhaiThue"
        if not self.xml_root.tag.startswith("{"):
            self._apply_namespace(self.xml_root, ns)

        # 2. Lấy dữ liệu từ Driver
        data = self._get_driver_data()

        # 3. Điền thông tin chung (Header)
        self._fill_header()

        # 4. Điền các chỉ tiêu (Body)
        self._fill_indicators(data.get("chi_tieu", {}))

        # 5. Điền phụ lục (Appendices)
        self._fill_appendices(data.get("phu_luc", {}))

        # 6. Kiểm tra dữ liệu thiết yếu
        self._verify_essential_data()

        # 7. Trả về XML string
        return etree.tostring(
            self.xml_root,
            encoding='UTF-8',
            xml_declaration=True,
            pretty_print=True
        ).decode('utf-8')

    def _find_xml_template(self):
        """Tìm file XML mẫu dựa trên declaration type."""
        base_path = frappe.get_app_path("dcnet_apps")

        # Thử tìm trong thư mục schemas/htkk_template/xml
        xml_dir = os.path.join(base_path, "htkk", "schemas", "htkk_template", "xml")

        # Derive base name from XSD file name
        xsd_name = self.declaration_type.xsd_file
        base_name = xsd_name.replace(".xsd", "")

        # Paths to try (ưu tiên file có _xml_ trong tên)
        # Chuyển "03_TNDN_TT80_292" -> "03_TNDN_TT80_xml_292"
        xml_name = re.sub(r'_(\d+)$', r'_xml_\1', base_name)
        paths_to_try = [
            os.path.join(xml_dir, f"{xml_name}.xml"),
            os.path.join(xml_dir, f"{base_name}.xml"),
        ]

        for path in paths_to_try:
            if os.path.exists(path):
                # Kiểm tra không phải file Sections
                try:
                    with open(path, 'rb') as f:
                        head = f.read(500).decode('utf-8', errors='ignore')
                        if '<Sections' in head:
                            continue
                except Exception:
                    pass
                return path

        # Fallback: tìm trong thư mục docs cũ
        docs_dir = os.path.join(base_path, "htkk", "docs", "htkk_InterfaceTemplates", "xml")
        if os.path.isdir(docs_dir):
            import glob
            matches = glob.glob(os.path.join(docs_dir, f"*{base_name}*.xml"))

            # Lọc bỏ các file layout
            valid = [
                m for m in matches
                if not any(x in m.upper() for x in ['_VIEW_', '_PL_', '_S_'])
            ]

            # Ưu tiên file có _xml_
            xml_matches = [m for m in valid if '_xml_' in m.lower()]
            if xml_matches:
                return xml_matches[0]
            if valid:
                return valid[0]

        return None

    def _find_xsd_file(self):
        """Tìm file XSD dựa trên declaration type."""
        base_path = frappe.get_app_path("dcnet_apps")
        xsd_dir = os.path.join(base_path, "htkk", "schemas", "htkk_template", "xsd")
        xsd_path = os.path.join(xsd_dir, self.declaration_type.xsd_file)

        if os.path.exists(xsd_path):
            return xsd_path

        # Fallback: thư mục docs cũ
        docs_dir = os.path.join(base_path, "htkk", "docs", "htkk_InterfaceTemplates", "Validate")
        xsd_path = os.path.join(docs_dir, self.declaration_type.xsd_file)

        return xsd_path if os.path.exists(xsd_path) else None

    def _apply_namespace(self, element, ns):
        """Đệ quy gán namespace cho element và con của nó."""
        element.tag = f"{{{ns}}}{element.tag}"
        for child in element:
            self._apply_namespace(child, ns)

    def _fill_header(self):
        """Điền thông tin header (TTinChung)."""
        company = frappe.get_doc("Company", self.doc.company)

        def set_node_text(path, text):
            nodes = self.xml_root.xpath(path)
            if nodes:
                nodes[0].text = str(text) if text is not None else ""
            return nodes

        header_path = "//*[local-name()='TTinChung']"
        tk_path = f"{header_path}//*[local-name()='TKhaiThue']"

        # Thông tin cơ bản
        set_node_text(f"{tk_path}/*[local-name()='loaiTKhai']", "C")
        set_node_text(f"{tk_path}/*[local-name()='soLan']", "0")

        # Kỳ kê khai
        ky_path = f"{tk_path}/*[local-name()='KyKKhaiThue']"
        if self.doc.period_type == "Tháng":
            set_node_text(f"{ky_path}/*[local-name()='kieuKy']", "M")
            set_node_text(f"{ky_path}/*[local-name()='kyKKhaiTuThang']", f"{self.doc.period:02d}/{self.doc.year}")
            set_node_text(f"{ky_path}/*[local-name()='kyKKhaiDenThang']", f"{self.doc.period:02d}/{self.doc.year}")
        elif self.doc.period_type == "Quý":
            set_node_text(f"{ky_path}/*[local-name()='kieuKy']", "Q")
            set_node_text(f"{ky_path}/*[local-name()='kyKKhaiTuQuy']", f"{self.doc.period:01d}/{self.doc.year}")
            set_node_text(f"{ky_path}/*[local-name()='kyKKhaiDenQuy']", f"{self.doc.period:01d}/{self.doc.year}")
        else:  # Năm
            set_node_text(f"{ky_path}/*[local-name()='kieuKy']", "Y")
            set_node_text(f"{ky_path}/*[local-name()='kyKKhaiTuNam']", str(self.doc.year))
            set_node_text(f"{ky_path}/*[local-name()='kyKKhaiDenNam']", str(self.doc.year))

        # Ngày ký & MST
        from frappe.utils import nowdate
        set_node_text(f"{tk_path}/*[local-name()='ngayKy']", nowdate())

        mst = (company.tax_id or "").strip()
        if not mst:
            frappe.throw(f"Công ty {company.name} chưa có Mã số thuế.")

        if len(mst) == 13 and "-" not in mst:
            mst = f"{mst[:10]}-{mst[10:]}"

        set_node_text(f"{header_path}//*[local-name()='mst']", mst)
        set_node_text(f"{header_path}//*[local-name()='tenNNT']", company.company_name)

        # Đại lý thuế (xóa nếu không có)
        dly_thue_node = self.xml_root.xpath(f"{header_path}//*[local-name()='DLyThue']")
        if dly_thue_node:
            mst_dly = (getattr(self.doc, 'tax_agent_mst', '') or '').strip()
            if not mst_dly:
                dly_thue_node[0].getparent().remove(dly_thue_node[0])
            else:
                set_node_text(f"//*[local-name()='mstDLyThue']", mst_dly)
                set_node_text(f"//*[local-name()='tenDLyThue']", getattr(self.doc, 'tax_agent_name', ''))

        # Tiểu mục hạch toán
        tieu_muc_map = {
            "01/GTGT": "1701",
            "03/TNDN": "1052",
            "05/TNCN": "1001",
        }
        set_node_text(f"//*[local-name()='tieuMucHachToan']", tieu_muc_map.get(self.doc.declaration_type, "0000"))

    def _fill_indicators(self, indicator_data):
        """Điền các chỉ tiêu vào CTieuTKhaiChinh."""
        body_node = self.xml_root.xpath("//*[local-name()='CTieuTKhaiChinh']")
        if not body_node:
            return

        # Normalize keys to lowercase
        indicator_data = {k.lower(): v for k, v in indicator_data.items()}

        for child in body_node[0].iterdescendants():
            if len(child) == 0:  # Leaf nodes
                tag_name = etree.QName(child).localname.lower()

                if tag_name in ['tieumuchachtoan', 'ma_nganhnghe', 'ten_nganhnghe']:
                    if child.text:
                        continue

                if tag_name in indicator_data:
                    val = indicator_data[tag_name]
                    if isinstance(val, bool) or str(val).lower() in ["true", "false"]:
                        child.text = "true" if str(val).lower() == "true" else "false"
                    elif isinstance(val, (int, float)):
                        child.text = str(int(val))
                    else:
                        child.text = str(val or "")
                else:
                    if tag_name == 'ct21':
                        child.text = "false"
                    elif tag_name.startswith('ct'):
                        child.text = "0"

    def _fill_appendices(self, appendices_data):
        """Điền dữ liệu vào thẻ <PLuc>."""
        pluc_node = self.xml_root.xpath("//*[local-name()='PLuc']")
        if not pluc_node or not appendices_data:
            return

        pluc_node = pluc_node[0]
        ns = "http://kekhaithue.gdt.gov.vn/TKhaiThue"

        def _build_nodes(parent, data):
            if isinstance(data, list):
                for i, item in enumerate(data):
                    tag = "HoaDon"
                    if "NQ142" in parent.tag:
                        tag = "BangKeTenHHDV"

                    item_node = etree.SubElement(parent, f"{{{ns}}}{tag}")
                    if isinstance(item, dict):
                        item_node.set("ID" if "ID" in parent.tag or "NQ142" in parent.tag else "id", f"ID_{i+1}")
                        _build_nodes(item_node, item)
            elif isinstance(data, dict):
                for key, val in data.items():
                    if key in ["doctype", "doc_name"]:
                        continue

                    child = etree.SubElement(parent, f"{{{ns}}}{key}")
                    if isinstance(val, (dict, list)):
                        _build_nodes(child, val)
                    else:
                        child.text = str(val) if val is not None else ""

        for pl_tag, content in appendices_data.items():
            if not content:
                continue

            # TT80: Skip legacy PL01-1 and PL01-2 in XML output
            if pl_tag in ["PL01_1_GTGT", "PL01_2_GTGT"]:
                continue

            pl_elements = pluc_node.xpath(f"*[local-name()='{pl_tag}']")
            if pl_elements:
                pl_element = pl_elements[0]
            else:
                pl_element = etree.SubElement(pluc_node, f"{{{ns}}}{pl_tag}")

            _build_nodes(pl_element, content)

    def _get_driver_data(self):
        """Gọi Driver tương ứng để lấy data."""
        from dcnet_apps.htkk.declarations.base import get_declaration_config

        config = get_declaration_config(self.doc.declaration_type)

        if not config:
            # Fallback: dùng ct_values nếu không có driver
            return {
                "chi_tieu": {
                    row.ct_name: (row.manual_value if row.is_manual else row.auto_value)
                    for row in self.doc.ct_values
                },
                "phu_luc": {}
            }

        # Use the config's generate method
        return config.generate(self.doc)

    def _verify_essential_data(self):
        """Kiểm tra các trường bắt buộc."""
        essentials = {
            "mst": "Mã số thuế",
            "tenNNT": "Tên người nộp thuế",
            "loaiTKhai": "Loại tờ khai"
        }

        for tag, label in essentials.items():
            nodes = self.xml_root.xpath(f"//*[local-name()='{tag}']")
            if not nodes or not nodes[0].text or nodes[0].text.strip() == "":
                frappe.msgprint(f"Cảnh báo: Trường '{label}' đang trống trong XML.")

    def validate(self):
        """Validate XML against XSD."""
        if self.xml_root is None:
            self.build_xml()

        xsd_path = self._find_xsd_file()
        if not xsd_path or not os.path.exists(xsd_path):
            return [f"Không tìm thấy file XSD cho {self.declaration_type.code}"]

        try:
            xsd_doc = etree.parse(xsd_path)
            schema = etree.XMLSchema(xsd_doc)
            is_valid = schema.validate(self.xml_root)
            if is_valid:
                return []
            return [self._translate_error(e) for e in schema.error_log]
        except Exception as e:
            return [f"Lỗi kiểm tra XSD: {str(e)}"]

    def _translate_error(self, error):
        """Dịch lỗi XSD sang tiếng Việt."""
        msg = error.message

        # Trích xuất tên thẻ
        element_name = ""
        match = re.search(r"Element\s+'(?:\{.*?\})?([^']+)'", msg)
        if match:
            element_name = match.group(1)

        # Map tên kỹ thuật
        field_map = {
            "mst": "Mã số thuế",
            "tenNNT": "Tên người nộp thuế",
            "ngayKy": "Ngày ký tờ khai",
            "loaiTKhai": "Loại tờ khai",
            "soLan": "Số lần bổ sung",
            "kieuKy": "Kiểu kỳ kê khai",
        }

        if element_name.lower().startswith("ct"):
            label = f"Chỉ tiêu [{element_name[2:].upper()}]"
        elif element_name in field_map:
            label = field_map[element_name]
        else:
            label = f"Trường '{element_name}'" if element_name else "Dữ liệu"

        # Dịch thông điệp
        if "is not accepted by the pattern" in msg:
            if "The value ''" in msg:
                return f"{label}: Không được để trống."
            return f"{label}: Sai định dạng."
        elif "is not a valid value of the atomic type" in msg:
            if "xs:date" in msg:
                return f"{label}: Ngày tháng sai định dạng (YYYY-MM-DD)."
            elif any(t in msg for t in ["xs:decimal", "xs:integer", "xs:long"]):
                return f"{label}: Phải là giá trị số."
            return f"{label}: Giá trị không hợp lệ."
        elif "This element is not expected" in msg:
            return f"Lỗi cấu trúc: Thẻ {label} xuất hiện sai vị trí."

        return f"{label}: {msg.split(':')[-1].strip()}"
