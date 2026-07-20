# HTKK Module - Technical Documentation

> **Version**: 3.1
> **Last Updated**: 2026-03-20
> **Author**: DCNET Team

---

## 1. Tổng quan

HTKK (Hỗ trợ Kê khai Thuế) là module hỗ trợ kê khai thuế điện tử cho doanh nghiệp Việt Nam, tích hợp với ERPNext. Module cho phép:

- Tự động tính toán các chỉ tiêu từ dữ liệu kế toán ERPNext
- Xuất file XML theo chuẩn Tổng cục Thuế
- Giao diện chỉnh sửa tờ khai trực quan (Vue.js SPA)
- Hỗ trợ nhiều loại tờ khai: 01/GTGT, 03/TNDN, ...
- **Dễ dàng mở rộng** - chỉ cần 3 files để thêm loại tờ khai mới

---

## 2. Kiến trúc hệ thống

### 2.1. Cấu trúc thư mục

```
htkk/
├── api/                        # REST API endpoints
│   ├── __init__.py            # Whitelist wrappers + _get_generator()
│   └── spike.py               # Core API logic
│
├── declarations/               # Declaration Config Registry
│   ├── base.py                # ⭐ DeclarationConfig base class + @register
│   ├── __init__.py            # Re-exports
│   ├── vat_01gtgt.py          # Config: 01/GTGT (VAT)
│   ├── cit_03tndn.py          # Config: 03/TNDN (CIT yearly)
│   ├── pit_05kktncn.py        # Config: 05/KK-TNCN (PIT deduction)
│   └── financial_statements.py # BCTC reports
│
├── utils/                      # Utility modules
│   └── excel_export.py        # Excel export functionality
│
├── doctype/                    # Frappe DocTypes
│   ├── htkk_declaration/      # Tờ khai chính
│   ├── htkk_declaration_ct_value/  # Giá trị chỉ tiêu (child table)
│   ├── htkk_declaration_adjustment/ # Điều chỉnh
│   ├── htkk_account_mapping/  # Ánh xạ tài khoản
│   ├── htkk_mapping_rule/     # Quy tắc mapping
│   └── htkk_settings/         # Cấu hình
│
├── engine/                     # Core processing
│   └── xml_builder.py         # XML generation & XSD validation
│
├── frontend/                   # Vue.js SPA
│   ├── src/
│   │   ├── App.vue            # Main app (dynamic tabs từ API)
│   │   └── components/
│   │       ├── HTKKFormDynamic.vue  # Form chỉ tiêu
│   │       ├── HTKKAppendixGrid.vue # Bảng phụ lục
│   │       ├── ActionToolbar.vue    # Toolbar actions
│   │       └── SheetTabs.vue        # Tab navigation
│   └── vite.config.js         # Build config
│
├── schemas/htkk_template/      # XSD & XML templates
│   ├── TKhaiThue.xsd          # Base schema
│   ├── TKhaiDkyThue.xsd       # Registration schema
│   ├── xmldsig-core-schema.xsd # XML signature
│   ├── xsd/                   # Per-declaration XSD
│   │   ├── 01_GTGT_TT80_283.xsd
│   │   └── 03_TNDN_TT80_292.xsd
│   └── xml/                   # XML templates
│       ├── 01_GTGT_TT80_xml_283.xml
│       └── 03_TNDN_TT80_xml_292.xml
│
├── www/                        # Frappe web pages
│   ├── htkk.html              # Vue SPA host page
│   └── htkk.py                # Context provider
│
├── docs/                       # Documentation
│   ├── new_prd.md             # This file
│   └── architecture_evolution.md # Architecture history
│
├── data_queries.py            # SQL queries for data
├── formula_parser.py          # XSD formula extraction
├── account_resolver.py        # Account mapping resolution
└── install.py                 # Setup/migration hooks
```

### 2.2. DeclarationConfig Pattern (v3.0)

**Single Source of Truth** - Mỗi loại tờ khai được định nghĩa hoàn toàn trong 1 class:

```python
# declarations/base.py
class DeclarationConfig(ABC):
    """Base class cho tất cả loại tờ khai."""

    # === METADATA ===
    code: str = ""           # "01/GTGT"
    name: str = ""           # "Tờ khai thuế giá trị gia tăng"
    short_name: str = ""     # "GTGT khấu trừ"
    xsd_file: str = ""       # "01_GTGT_TT80_283.xsd"
    period: str = ""         # "monthly", "quarterly", "yearly"
    circular: str = ""       # "TT80/2021/TT-BTC"
    has_appendices: bool = False

    # === FRONTEND CONFIG ===
    title: str = ""          # Tiêu đề hiển thị
    subtitle: str = ""       # Phụ đề
    appendices: List[Dict] = []   # [{key, label, type}]
    sections: List[Dict] = []     # Cấu trúc form

    # === DRIVER METHODS ===
    @abstractmethod
    def compute_chi_tieu(self, doc) -> Dict: pass

    @abstractmethod
    def generate(self, doc) -> Dict: pass
```

### 2.3. Auto-Registration với @register Decorator

```python
# declarations/vat_01gtgt.py
from dcnet_apps.htkk.declarations.base import DeclarationConfig, register

@register
class VAT01GTGT(DeclarationConfig):
    code = "01/GTGT"
    name = "Tờ khai thuế giá trị gia tăng"
    xsd_file = "01_GTGT_TT80_283.xsd"
    ...

    def compute_chi_tieu(self, doc):
        # Logic tính toán
        ...
```

Khi module được import, `@register` decorator tự động:
1. Instantiate class
2. Đăng ký vào `_REGISTRY` global dict
3. Cho phép truy xuất qua `get_declaration_config(code)`

### 2.4. Auto-Scan Modules

```python
# declarations/base.py
def _scan_declaration_modules():
    """Auto-import tất cả modules trong declarations/ folder."""
    declarations_dir = os.path.dirname(__file__)
    for filename in os.listdir(declarations_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            if filename != "base.py":
                module_name = filename[:-3]
                importlib.import_module(f"dcnet_apps.htkk.declarations.{module_name}")
```

---

## 3. Thêm loại tờ khai mới (v3.0)

### Chỉ cần 3 files:

| # | File | Nguồn |
|---|------|-------|
| 1 | `schemas/.../xsd/{code}.xsd` | Tổng cục Thuế |
| 2 | `schemas/.../xml/{code}_xml_{ver}.xml` | Tổng cục Thuế |
| 3 | `declarations/{code}.py` | Viết code |

### Ví dụ: Thêm tờ khai 04/GTGT

```python
# declarations/vat_04gtgt.py
from dcnet_apps.htkk.declarations.base import DeclarationConfig, register

@register
class VAT04GTGT(DeclarationConfig):
    """Tờ khai thuế GTGT trực tiếp trên doanh thu."""

    # === METADATA ===
    code = "04/GTGT"
    name = "Tờ khai thuế GTGT trực tiếp"
    short_name = "GTGT trực tiếp"
    xsd_file = "04_GTGT_TT80_274.xsd"
    period = "quarterly"
    circular = "TT80/2021/TT-BTC"
    has_appendices = False

    # === FRONTEND CONFIG ===
    title = "Tờ khai thuế giá trị gia tăng"
    subtitle = "(Dành cho cơ sở kinh doanh tính thuế GTGT trực tiếp trên doanh thu)"
    appendices = []

    sections = [
        {
            "id": "header",
            "title": "Thông tin chung",
            "indicators": ["ct04", "ct05"]
        },
        {
            "id": "revenue",
            "title": "Doanh thu phát sinh trong kỳ",
            "indicators": ["ct21", "ct22", "ct23"],
        },
        # ...
    ]

    # === DRIVER LOGIC ===
    def compute_chi_tieu(self, doc):
        result = {}
        # Query dữ liệu và tính toán
        revenue = self._query_gl_sum(doc, ["511%", "512%"])
        result["ct21"] = {"auto_value": revenue, "source": "GL Entry 511*, 512*"}
        return result

    def generate(self, doc):
        chi_tieu = self._get_indicator_values(doc)
        return {"chi_tieu": chi_tieu, "phu_luc": {}, "sources": {}}
```

**Không cần sửa thêm file nào khác!** Frontend và API tự động nhận diện loại tờ khai mới.

---

## 4. Luồng công việc

### 4.1. Tạo tờ khai mới

```
User tạo HTKK Declaration
    ↓
Chọn: declaration_type, company, period_type, period, year
    ↓
Hệ thống tự động set: from_date, to_date
    ↓
Trạng thái: "Nháp"
```

### 4.2. Tính toán chỉ tiêu

```
User click "Lấy dữ liệu" (frontend) hoặc "Tính toán" (DocType)
    ↓
API: calculate_declaration(declaration_id)
    ↓
_get_generator(declaration_type)  →  get_declaration_config()
    ↓
config.compute_chi_tieu(doc)
    ├── Query GL Entry trong kỳ
    ├── Ánh xạ tài khoản → chỉ tiêu
    ├── Tính toán công thức
    └── Lấy phụ lục từ Sales/Purchase Invoice
    ↓
Lưu vào ct_values (child table)
    ↓
Hiển thị trên frontend
```

### 4.3. Frontend Data Flow

```
onMounted()
    ├── fetchDocInfo(id)           →  docInfo (type, period, company)
    ├── fetchTemplateData(type)    →  templateData (appendices, sections)
    └── fetchRawData(id)           →  rawData (indicators, sources)

appendixTabs = computed(() => templateData.appendices)
computedTabs = computed(() => [mainTab, ...appendixTabs])
```

### 4.4. Validate & Export

```
User click "Validate"
    ↓
validate_declaration(declaration_id)
    ├── Basic checks
    ├── HTKKXmlBuilder.build_xml()
    └── Validate against XSD
    ↓
Return: {status, errors?}

User click "Xuất XML"
    ↓
export_declaration(declaration_id)
    ├── HTKKXmlBuilder.build_xml()
    ├── Save as File
    └── Update status = "Đã xuất"
```

---

## 5. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `get_declaration_data` | GET | Lấy dữ liệu tờ khai cho frontend |
| `get_declaration_info` | GET | Lấy metadata tờ khai |
| `get_declaration_template` | GET | Lấy schema + **appendices** + **sections** |
| `calculate_declaration` | GET | Tính toán chỉ tiêu từ GL |
| `save_declaration_data` | POST | Lưu chỉ tiêu đã chỉnh sửa |
| `validate_declaration` | GET | Kiểm tra hợp lệ (XSD) |
| `export_declaration` | GET | Xuất file XML |
| `export_declaration_excel` | GET | Xuất file Excel (v3.1) |
| `submit_declaration` | GET | Gửi duyệt |

### get_declaration_template Response (v3.0)

```json
{
  "declaration_type": "01/GTGT",
  "name": "Tờ khai thuế giá trị gia tăng",
  "title": "Tờ khai thuế giá trị gia tăng",
  "subtitle": "(Dành cho người nộp thuế...)",
  "has_appendices": true,
  "appendices": [
    {"key": "PL01_1_GTGT", "label": "PL 01-1/GTGT", "type": "PL 01-1/GTGT"},
    {"key": "PL01_2_GTGT", "label": "PL 01-2/GTGT", "type": "PL 01-2/GTGT"}
  ],
  "sections": [...],
  "fields": [...],
  "formulas": {...}
}
```

---

## 6. Frontend Architecture

### 6.1. Dynamic Configuration từ API

Frontend **không còn hardcode** config cho từng loại tờ khai:

```javascript
// App.vue - TRƯỚC (v2.0)
const APPENDIX_CONFIG = {
  '01/GTGT': [...],
  '03/TNDN': [],
};

// App.vue - SAU (v3.0)
const templateData = ref(null);

const appendixTabs = computed(() => {
  return templateData.value?.appendices || [];
});

onMounted(async () => {
  await fetchDocInfo(currentId.value);
  await fetchTemplateData(docInfo.value.declaration_type);
  await fetchRawData(currentId.value);
});
```

### 6.2. Deployment

```bash
# Build frontend
cd htkk/frontend && npm run build

# Sync assets
bench build --app dcnet_apps

# Clear cache
bench --site <site> clear-cache
```

---

## 7. Schema Management

### 7.1. File Naming Convention

```
XSD: {code}_{circular}_{version}.xsd
     01_GTGT_TT80_283.xsd

XML: {code}_{circular}_xml_{version}.xml
     01_GTGT_TT80_xml_283.xml
```

### 7.2. XSD Structure

```
schemas/htkk_template/
├── TKhaiThue.xsd              # Base schema
├── TKhaiDkyThue.xsd           # Registration schema
├── xmldsig-core-schema.xsd    # XML signature
├── xsd/                       # Per-declaration XSD
│   └── 01_GTGT_TT80_283.xsd   # xs:redefine "../TKhaiThue.xsd"
└── xml/                       # XML templates
    └── 01_GTGT_TT80_xml_283.xml
```

---

## 8. Các loại tờ khai được hỗ trợ

| Code | Tên | Period | Phụ lục |
|------|-----|--------|---------|
| 01/GTGT | Thuế GTGT khấu trừ | Tháng/Quý | PL01-1, PL01-2 |
| 03/TNDN | Thuế TNDN quyết toán năm | Năm | Không |
| 05/KK-TNCN | Thuế TNCN khấu trừ | Tháng | PL05-1 |

---

## 9. Helper Methods trong DeclarationConfig

Base class cung cấp các helper methods:

```python
class DeclarationConfig(ABC):

    def _get_indicator_values(self, doc) -> Dict:
        """Lấy giá trị từ ct_values, ưu tiên manual_value."""
        return {
            row.ct_name: (row.manual_value if row.is_manual else row.auto_value)
            for row in doc.ct_values
        }

    def _query_gl_sum(self, doc, account_patterns, credit_minus_debit=True) -> float:
        """Query tổng GL Entry theo patterns."""
        # SELECT SUM(credit - debit) FROM GL Entry WHERE account LIKE ...

    def _get_previous_period_value(self, doc, ct_name, default=0.0) -> float:
        """Lấy giá trị chỉ tiêu từ kỳ trước."""
        # Tính prev_period, prev_year và query
```

---

## 10. Troubleshooting

### Lỗi "File XML mẫu không phải tờ khai hợp lệ"

- **Nguyên nhân**: File XML có root `<Sections>` (layout file)
- **Fix**: Copy file có `_xml_` trong tên từ docs/htkk_InterfaceTemplates/

### Lỗi "Failed to load TKhaiThue.xsd for redefinition"

- **Nguyên nhân**: File `TKhaiThue.xsd` nằm sai vị trí
- **Fix**: Di chuyển ra `schemas/htkk_template/` (cha của `xsd/`)

### Loại tờ khai mới không xuất hiện

- **Kiểm tra**: Import module trong declarations/__init__.py
- **Debug**: `get_all_declarations()` để xem registry

---

## 11. Roadmap

- [x] ~~Thêm loại tờ khai: 05/KK-TNCN~~ (v3.1)
- [x] ~~Export Excel báo cáo~~ (v3.1)
- [ ] Auto-save draft (mỗi 30s)
- [ ] Integration với iHOADON (nộp tờ khai điện tử)
- [ ] Workflow approval (multi-level)
- [ ] Thêm loại tờ khai: 05/QTT-TNCN (quyết toán năm)
