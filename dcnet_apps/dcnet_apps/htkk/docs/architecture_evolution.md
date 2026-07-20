# HTKK Architecture Evolution

> **Document**: Lịch sử phát triển kiến trúc module HTKK
> **Author**: DCNET Team
> **Last Updated**: 2026-03-20

---

## Tổng quan

Document này ghi lại quá trình tiến hóa kiến trúc của module HTKK qua 4 giai đoạn:

| Version | Thời gian | Đặc điểm chính |
|---------|-----------|----------------|
| v1.0 | Khởi đầu | Monolithic, hardcoded |
| v2.0 | 2026-03-19 | Registry Pattern, Driver Pattern |
| v3.0 | 2026-03-20 | Single Config Class Pattern + Backward Compat |
| v3.1 | 2026-03-20 | Clean Architecture - No Legacy Code |

---

## Version 1.0 - Monolithic Architecture

### Tư duy thiết kế

> "Làm cho nó hoạt động trước" - Tập trung vào một loại tờ khai (01/GTGT)

### Cấu trúc

```
htkk/
├── api.py                    # Tất cả API trong 1 file
├── vat_calculator.py         # Logic tính thuế GTGT
├── xml_generator.py          # Xuất XML
└── frontend/
    └── App.vue               # Frontend cố định cho 01/GTGT
```

### Đặc điểm

1. **Tightly Coupled**: Logic tính toán, metadata, UI config đều nằm rải rác
2. **Single Declaration**: Chỉ hỗ trợ 01/GTGT
3. **Hardcoded Everything**: Tên chỉ tiêu, thuế suất, XSD path đều hardcode

### Code mẫu

```python
# api.py - v1.0
def calculate_vat(company, from_date, to_date):
    # Hardcoded cho 01/GTGT
    ct22 = get_carried_forward(company)
    ct23 = sum_purchase_invoices(company, from_date, to_date)
    ct24 = ct23 * 0.1  # Giả định thuế suất 10%
    ...
    return {"ct22": ct22, "ct23": ct23, ...}

def export_xml(declaration_id):
    # Hardcoded XSD path
    xsd_path = "schemas/01_GTGT.xsd"
    ...
```

### Vấn đề

- Không thể mở rộng cho loại tờ khai khác
- Thay đổi logic = sửa trực tiếp file chính
- Frontend không linh hoạt

---

## Version 2.0 - Registry & Driver Pattern

### Tư duy thiết kế

> "Tách metadata ra khỏi logic" - Separation of Concerns

### Cấu trúc

```
htkk/
├── api/
│   ├── __init__.py           # Whitelist + _DECLARATION_GENERATORS dict
│   └── spike.py              # TITLE_MAP + _get_form_sections()
│
├── declarations/
│   ├── __init__.py           # DECLARATION_REGISTRY dataclass
│   ├── vat_01gtgt.py         # Driver: compute_chi_tieu(), generate()
│   └── cit_03tndn.py         # Driver: compute_chi_tieu(), generate()
│
└── frontend/
    └── App.vue               # APPENDIX_CONFIG hardcoded
```

### Kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                    DECLARATION_REGISTRY                  │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │ DeclarationType │  │ DeclarationType │              │
│  │ code: 01/GTGT   │  │ code: 03/TNDN   │              │
│  │ xsd_file: ...   │  │ xsd_file: ...   │              │
│  └─────────────────┘  └─────────────────┘              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│               _DECLARATION_GENERATORS                    │
│  "01/GTGT" → "dcnet_apps.htkk.declarations.vat_01gtgt"  │
│  "03/TNDN" → "dcnet_apps.htkk.declarations.cit_03tndn"  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Driver Modules                          │
│  vat_01gtgt.py          │  cit_03tndn.py                │
│  ├── compute_chi_tieu() │  ├── compute_chi_tieu()       │
│  └── generate()         │  └── generate()               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    spike.py                              │
│  TITLE_MAP = {                                          │
│    "01/GTGT": ("Tờ khai thuế GTGT", "..."),            │
│    "03/TNDN": ("Tờ khai thuế TNDN", "..."),            │
│  }                                                       │
│  _get_form_sections(declaration_type) → [sections]      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    App.vue                               │
│  APPENDIX_CONFIG = {                                    │
│    "01/GTGT": [{key, label, type}, ...],               │
│    "03/TNDN": [],                                       │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
```

### Code mẫu

```python
# declarations/__init__.py - v2.0
@dataclass
class DeclarationType:
    code: str
    name: str
    xsd_file: str
    period: DeclarationPeriod
    ...

DECLARATION_REGISTRY = {
    "01/GTGT": DeclarationType(code="01/GTGT", ...),
    "03/TNDN": DeclarationType(code="03/TNDN", ...),
}

# api/__init__.py - v2.0
_DECLARATION_GENERATORS = {
    "01/GTGT": "dcnet_apps.htkk.declarations.vat_01gtgt",
    "03/TNDN": "dcnet_apps.htkk.declarations.cit_03tndn",
}

def _get_generator(declaration_type):
    module_path = _DECLARATION_GENERATORS.get(declaration_type)
    return importlib.import_module(module_path)

# api/spike.py - v2.0
TITLE_MAP = {
    "01/GTGT": ("Tờ khai thuế GTGT", "..."),
    "03/TNDN": ("Tờ khai thuế TNDN", "..."),
}

def _get_form_sections(declaration_type):
    if declaration_type == "01/GTGT":
        return [{"id": "header", ...}, ...]
    elif declaration_type == "03/TNDN":
        return [{"id": "profit", ...}, ...]
```

### Cải thiện so với v1.0

- Metadata tách riêng trong `DeclarationType`
- Logic tính toán tách thành driver modules
- Hỗ trợ nhiều loại tờ khai

### Vấn đề còn lại

- **Scattered Configuration**: Config nằm ở 6-8 chỗ khác nhau
- **Manual Registration**: Phải thêm thủ công vào nhiều dict/map
- **Easy to Miss**: Quên update 1 chỗ = bug khó debug

### Thêm loại tờ khai mới (v2.0)

```
Files cần sửa:
1. declarations/__init__.py      → DECLARATION_REGISTRY
2. declarations/xxx.py           → Driver module
3. api/__init__.py               → _DECLARATION_GENERATORS
4. api/spike.py                  → TITLE_MAP
5. api/spike.py                  → _get_form_sections()
6. frontend/App.vue              → APPENDIX_CONFIG
7. schemas/.../xsd/xxx.xsd       → XSD template
8. schemas/.../xml/xxx_xml.xml   → XML template
```

**Total: 8 files** cần thay đổi!

---

## Version 3.0 - Single Config Class Pattern

### Tư duy thiết kế

> "Single Source of Truth" - Mọi thứ về 1 loại tờ khai nằm trong 1 class duy nhất

### Nguyên tắc

1. **Colocated Config**: Metadata, UI config, driver logic cùng 1 file
2. **Auto-Registration**: `@register` decorator thay vì manual dict
3. **Auto-Scan**: Import tự động tất cả modules trong folder
4. **API-Driven Frontend**: Frontend lấy config từ API, không hardcode

### Cấu trúc

```
htkk/
├── api/
│   ├── __init__.py           # _get_generator() → get_declaration_config()
│   └── spike.py              # Lấy title, sections từ config
│
├── declarations/
│   ├── base.py               # ⭐ DeclarationConfig + @register + auto-scan
│   ├── __init__.py           # Re-exports + backward compat
│   ├── vat_01gtgt.py         # ⭐ Class VAT01GTGT(DeclarationConfig)
│   └── cit_03tndn.py         # ⭐ Class CIT03TNDN(DeclarationConfig)
│
└── frontend/
    └── App.vue               # Fetch appendices từ API
```

### Kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                    declarations/base.py                  │
│                                                          │
│  _REGISTRY: Dict[str, DeclarationConfig] = {}           │
│                                                          │
│  @register  ─────────────────┐                          │
│  def register(cls):          │ Auto-register            │
│      instance = cls()        │ khi import               │
│      _REGISTRY[instance.code]│                          │
│      return cls              │                          │
│  ────────────────────────────┘                          │
│                                                          │
│  class DeclarationConfig(ABC):                          │
│      code, name, xsd_file, period     # Metadata        │
│      title, subtitle                  # UI              │
│      appendices, sections             # UI Config       │
│      compute_chi_tieu()               # Driver          │
│      generate()                       # Driver          │
│      _query_gl_sum()                  # Helpers         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  vat_01gtgt.py                           │
│  @register                                               │
│  class VAT01GTGT(DeclarationConfig):                    │
│      code = "01/GTGT"                                   │
│      name = "Tờ khai thuế GTGT"                         │
│      xsd_file = "01_GTGT_TT80_283.xsd"                  │
│      title = "Tờ khai thuế giá trị gia tăng"            │
│      subtitle = "(Dành cho người nộp thuế...)"          │
│      appendices = [                                      │
│          {"key": "PL01_1_GTGT", "label": "PL 01-1"},    │
│      ]                                                   │
│      sections = [                                        │
│          {"id": "header", "indicators": [...]},         │
│      ]                                                   │
│                                                          │
│      def compute_chi_tieu(self, doc): ...               │
│      def generate(self, doc): ...                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    API Layer                             │
│  get_declaration_config("01/GTGT")                      │
│      → VAT01GTGT instance                               │
│      → config.title, config.sections, config.appendices │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Frontend                              │
│  fetchTemplateData(type)                                │
│      → appendices từ API                                │
│      → sections từ API                                  │
│  Không còn hardcode!                                    │
└─────────────────────────────────────────────────────────┘
```

### Code mẫu

```python
# declarations/vat_01gtgt.py - v3.0
from dcnet_apps.htkk.declarations.base import DeclarationConfig, register

@register
class VAT01GTGT(DeclarationConfig):
    # === METADATA ===
    code = "01/GTGT"
    name = "Tờ khai thuế giá trị gia tăng"
    short_name = "GTGT khấu trừ"
    xsd_file = "01_GTGT_TT80_283.xsd"
    period = "quarterly"
    circular = "TT80/2021/TT-BTC"
    has_appendices = True

    # === FRONTEND CONFIG ===
    title = "Tờ khai thuế giá trị gia tăng"
    subtitle = "(Dành cho người nộp thuế tính thuế theo phương pháp khấu trừ)"

    appendices = [
        {"key": "PL01_1_GTGT", "label": "PL 01-1/GTGT", "type": "PL 01-1/GTGT"},
        {"key": "PL01_2_GTGT", "label": "PL 01-2/GTGT", "type": "PL 01-2/GTGT"},
    ]

    sections = [
        {"id": "header", "title": "Thông tin chung", "indicators": [...]},
        {"id": "input_vat", "title": "A. THUẾ GTGT CÒN KHẤU TRỪ", "indicators": [...]},
        ...
    ]

    # === DRIVER LOGIC ===
    def compute_chi_tieu(self, doc):
        r = {}
        # ... tất cả logic tính toán
        return r

    def generate(self, doc):
        chi_tieu, sources = self._get_final_ct_values(doc)
        phu_luc = {...}
        return {"chi_tieu": chi_tieu, "sources": sources, "phu_luc": phu_luc}
```

### Thêm loại tờ khai mới (v3.0)

```
Files cần tạo/sửa:
1. schemas/.../xsd/xxx.xsd       → XSD template (từ Tổng cục Thuế)
2. schemas/.../xml/xxx_xml.xml   → XML template (từ Tổng cục Thuế)
3. declarations/xxx.py           → Class với @register

Total: 3 files!
```

---

## So sánh các phiên bản

### Số files cần sửa khi thêm tờ khai mới

| Version | Số files | Chi tiết |
|---------|----------|----------|
| v1.0 | N/A | Không hỗ trợ mở rộng |
| v2.0 | 8 files | registry, driver, generators, title_map, sections, appendix_config, xsd, xml |
| v3.0 | 3 files | xsd, xml, config class |

### Configuration Locations

| Aspect | v2.0 | v3.0 |
|--------|------|------|
| Metadata | `DECLARATION_REGISTRY` | Class attributes |
| Generator Path | `_DECLARATION_GENERATORS` | `@register` auto |
| Title/Subtitle | `TITLE_MAP` | Class attributes |
| Sections | `_get_form_sections()` | Class attributes |
| Appendices | `APPENDIX_CONFIG` (frontend) | Class attributes → API |

### Code Duplication

```
v2.0:
  - code = "01/GTGT" xuất hiện trong 4 files
  - Tên tờ khai xuất hiện trong 3 files
  - Dễ mismatch khi update

v3.0:
  - Mọi thứ trong 1 class
  - Single source of truth
  - Không thể mismatch
```

---

## Version 3.1 - Clean Architecture

### Tư duy thiết kế

> "Remove all legacy code" - Xóa hoàn toàn backward compatibility layers

### Thay đổi từ v3.0

| Component | v3.0 | v3.1 |
|-----------|------|------|
| `vat_01gtgt.py` | Có legacy wrappers | Chỉ có class |
| `cit_03tndn.py` | Có legacy wrappers | Chỉ có class |
| `__init__.py` | Legacy proxy + compat | Clean re-exports |

### Code đã xóa

```python
# XÓA khỏi vat_01gtgt.py và cit_03tndn.py:
def compute_chi_tieu(declaration):
    """Legacy wrapper for backward compatibility."""
    config = VAT01GTGT()
    return config.compute_chi_tieu(declaration)

def generate(declaration):
    """Legacy wrapper for backward compatibility."""
    config = VAT01GTGT()
    return config.generate(declaration)
```

```python
# XÓA khỏi declarations/__init__.py:
- class DeclarationType (dataclass)
- class _RegistryProxy
- DECLARATION_REGISTRY proxy
- _config_to_legacy_type()
- get_declaration_type()
- get_legacy_registry()
```

### Cấu trúc v3.1

```
declarations/
├── base.py           # DeclarationConfig + @register + auto-scan
├── __init__.py       # Clean re-exports (không có compat layer)
├── vat_01gtgt.py     # class VAT01GTGT (không có legacy wrappers)
└── cit_03tndn.py     # class CIT03TNDN (không có legacy wrappers)
```

### declarations/__init__.py (v3.1)

```python
"""HTKK Declarations Registry (v3.1)"""
from typing import List, Dict
from dcnet_apps.htkk.declarations.base import (
    DeclarationConfig,
    DeclarationPeriod,
    register,
    get_declaration_config,
    get_all_declarations,
    get_supported_codes,
)

def get_supported_declarations() -> List[Dict]:
    configs = get_all_declarations()
    period_map = {"monthly": "Tháng", "quarterly": "Quý", "yearly": "Năm"}
    return [
        {
            "code": config.code,
            "name": config.name,
            "short_name": config.short_name,
            "period": period_map.get(config.period, "Quý"),
            "description": config.subtitle or "",
        }
        for config in configs
    ]
```

---

## Lessons Learned

### 1. Configuration Sprawl là Tech Debt

> Khi config nằm rải rác, mỗi lần thêm feature = thêm nhiều chỗ cần nhớ

### 2. Decorator Pattern cho Registration

> `@register` decorator elegant hơn manual dict:
> - Không quên đăng ký
> - Code và registration cùng chỗ
> - Dễ discover (grep `@register`)

### 3. API-Driven Frontend

> Frontend không nên hardcode business config:
> - Thay đổi backend = tự động update frontend
> - Single deployment
> - Dễ A/B testing

### 4. Backward Compatibility - When to Remove

> v3.0 giữ legacy wrappers "just in case"
> v3.1 xóa hoàn toàn sau khi verify không còn code nào dùng
>
> **Nguyên tắc**: Giữ compat layer trong 1 release cycle, sau đó xóa

---

## Migration Path

### v2.0 → v3.0 → v3.1

```
v2.0 (8 files)
    ↓ Refactor to class-based
v3.0 (3 files + compat layer)
    ↓ Remove compat after verification
v3.1 (3 files, clean)
```

### Checklist v3.1

- [x] Xóa legacy wrappers trong vat_01gtgt.py
- [x] Xóa legacy wrappers trong cit_03tndn.py
- [x] Cleanup declarations/__init__.py
- [x] Verify api/__init__.py dùng get_declaration_config()
- [x] Verify api/spike.py dùng config object
- [x] Test 01/GTGT workflow
- [x] Test 03/TNDN workflow

---

## Kết luận

Evolution từ v1.0 → v3.1 là hành trình từ:

```
v1.0: Monolithic      → Hardcoded     → Scattered
v2.0: Modular         → Registry      → Separated
v3.0: Cohesive        → Self-Register → Colocated + Compat
v3.1: Clean           → Pure Classes  → No Legacy
```

**v3.1 đạt được mục tiêu cuối cùng:**
- Thêm tờ khai mới = **1 file Python** + 2 files từ Tổng cục Thuế
- Không còn code legacy
- Single source of truth cho mỗi loại tờ khai
