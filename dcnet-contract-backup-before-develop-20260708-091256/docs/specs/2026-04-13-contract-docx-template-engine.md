---
project: frappe-bench-dcnet
base_branch: master
---

# DCNet Contract — Docx Template Engine & Template Management

## Mục tiêu

1. **Xuất hợp đồng dạng .docx/pdf** với thông tin đã điền sẵn, giữ nguyên format gốc
2. **Quản lý mẫu hợp đồng** — thêm, chỉnh sửa .docx templates từ Frappe UI

## Phân tích mẫu hợp đồng thực tế

6 mẫu gốc đã convert sang markdown tại `docs/contract_templates/converted/`:

| Mẫu | Loại | Đặc điểm |
|-----|------|----------|
| HĐ Dịch vụ Viễn thông | HĐ khung | 13 điều, dùng cho P2P/ILL/MPLS, chi tiết ở phụ lục |
| HĐ FTTH Doanh nghiệp | Standalone | Gói: hàng tháng / 7 tháng (6+1) / 14 tháng (12+2) |
| HĐ FTTH Hộ gia đình | Standalone | Giống DN, khác customer type (cá nhân), proration fixed/30 |
| PL Kênh thuê riêng P2P | Phụ lục | Điểm đầu-cuối, FO, cước lắp đặt + hàng tháng |
| PL Internet Leased Line | Phụ lục | Băng thông Mbps, cam kết RTT latency |
| PL Truyền số liệu MPLS | Phụ lục | Băng thông, điểm đầu-cuối |

### Biến (placeholders) chung trong các mẫu

| Placeholder | Nguồn dữ liệu | Ghi chú |
|------------|---------------|---------|
| `{{contract_number}}` | `doc.name` hoặc `doc.contract_no_external` | Số HĐ |
| `{{contract_date}}` | `doc.contract_date` | Ngày ký |
| `{{customer_name}}` | `doc.customer_name` | Tên Bên A |
| `{{customer_address}}` | Customer → address | Trụ sở |
| `{{customer_phone}}` | Customer → phone | Điện thoại |
| `{{customer_tax_id}}` | Customer → tax_id | MST |
| `{{customer_representative}}` | Contact → full_name | Người đại diện |
| `{{customer_representative_title}}` | Contact → designation | Chức vụ |
| `{{customer_id_number}}` | Contact → custom field | CMND/CCCD (HGĐ) |
| `{{service_type}}` | `doc.service_type` | Loại dịch vụ |
| `{{package_name}}` | `doc.package_name` | Gói cước/tốc độ |
| `{{installation_address}}` | `doc.installation_address` | Địa chỉ lắp đặt |
| `{{setup_fee}}` | `doc.setup_fee` | Phí lắp đặt |
| `{{monthly_fee}}` | `doc.unit_price_total` | Cước hàng tháng |
| `{{package_term}}` | `doc.package_term_months` | Thời hạn (tháng) |
| `{{acceptance_date}}` | `doc.acceptance_date` | Ngày nghiệm thu |
| `{{end_date}}` | `doc.end_date` | Ngày kết thúc |
| `{{ITEMS_TABLE}}` | `doc.items` | Bảng items — xử lý đặc biệt |

> **Why placeholders, không dùng Jinja2:** Mẫu HĐ là file .docx do phòng pháp chế soạn. Họ không biết Jinja. Placeholder `{{tên_biến}}` đơn giản, ai cũng edit được trong Word.

## Kiến trúc

### 1. Docx Generator Engine (`utils/docx_generator.py`)

```
Input:  contract_name + template_name (optional)
        ↓
Step 1: Load .docx template file from DCNet Contract Template attachment
Step 2: Build placeholder → value mapping from contract data
Step 3: Replace placeholders in paragraphs, tables, headers/footers
Step 4: Handle ITEMS_TABLE — clone template row, fill for each item
Step 5: Save to temp file → attach to contract or return for download
Step 6: (Optional) Convert to PDF via LibreOffice headless
        ↓
Output: File URL (.docx or .pdf)
```

**python-docx approach:** Iterate all paragraphs + table cells + header/footer paragraphs. For each `run`, check if text contains `{{...}}` and replace. Handles Word's tendency to split `{{placeholder}}` across multiple runs by joining adjacent runs first.

**ITEMS_TABLE handling:** Template .docx has a table with a single data row containing `{{item_label}}`, `{{item_qty}}`, `{{item_price}}`, `{{item_amount}}`. Engine clones this row N times (one per item), fills values, removes the template row.

> **Why python-docx, không dùng Jinja2-docx:** python-docx-template (docxtpl) adds Jinja inside Word XML — phức tạp cho end-user. Raw python-docx find-replace giữ format gốc 100% và placeholder đơn giản.

### 2. Template Management (DCNet Contract Template enhancement)

**Thêm fields:**
- `template_file` (Attach) — file .docx mẫu
- `placeholders` (Table → DCNet Contract Template Placeholder) — read-only, auto-discovered
- `template_category` (Select: "Hợp đồng" / "Phụ lục") — phân biệt HĐ chính vs phụ lục

**DCNet Contract Template Placeholder** (new child DocType):
- `placeholder_key` (Data, read-only) — e.g., `customer_name`
- `mapped_field` (Data, read-only) — e.g., `doc.customer_name`
- `sample_value` (Data, read-only) — preview value

**Workflow:** Admin upload .docx → system scan tất cả `{{...}}` → hiển thị trong bảng placeholders → admin verify mapping → save.

### 3. Contract Form Integration

**Button "Xuất Hợp đồng"** trên DCNet Contract form (chỉ khi status != Draft):
- Dialog chọn: format (DOCX / PDF), template (nếu có nhiều)
- Call API → download file

**API:**
```python
@frappe.whitelist()
def generate_contract_document(contract_name, template_name=None, output_format="docx"):
    """Generate filled contract document.
    Returns: file URL for download.
    """
```

### 4. PDF Conversion

LibreOffice 24.2 có sẵn trên server:
```bash
libreoffice --headless --convert-to pdf --outdir /tmp /tmp/contract.docx
```

> **Why LibreOffice, không wkhtmltopdf:** wkhtmltopdf không có sẵn. LibreOffice convert docx→pdf giữ nguyên format Word 100%.

## Prepare .docx Templates

Chuẩn bị 6 file .docx từ originals, thay dots/blanks bằng `{{placeholder}}`:

1. `HĐ Dịch vụ Viễn thông.docx` — HĐ khung
2. `HĐ FTTH Doanh nghiệp.docx` — standalone
3. `HĐ FTTH Hộ gia đình.docx` — standalone (cá nhân)
4. `PL Kênh thuê riêng P2P.docx` — phụ lục
5. `PL Internet Leased Line ILL.docx` — phụ lục
6. `PL Truyền số liệu MPLS.docx` — phụ lục

Mỗi file: copy từ original → thay `…………` bằng `{{placeholder}}` tương ứng → giữ nguyên format, font, layout.

## Không làm trong scope này

- HĐ khung + phụ lục relationship (parent-child contract) — scope riêng
- SLA fields, nghiệm thu workflow, phạt vi phạm — scope riêng
- FTTH package pricing (7 tháng = 6+1, 14 tháng = 12+2) — scope riêng
- Proration formula per service type — scope riêng
- Customer type (cá nhân/doanh nghiệp) field — scope riêng
