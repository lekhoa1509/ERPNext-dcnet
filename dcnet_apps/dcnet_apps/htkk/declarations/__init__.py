"""
HTKK Declarations Registry (v3.1)

Quản lý các loại tờ khai được hỗ trợ thông qua DeclarationConfig classes.

Sử dụng @register decorator để tự động đăng ký declaration type.
Chỉ cần tạo 1 file Python với class kế thừa DeclarationConfig là đủ.

Example:
    from dcnet_apps.htkk.declarations.base import DeclarationConfig, register

    @register
    class VAT04GTGT(DeclarationConfig):
        code = "04/GTGT"
        name = "Tờ khai thuế GTGT trực tiếp"
        xsd_file = "04_GTGT_TT80_274.xsd"
        ...

        def compute_chi_tieu(self, doc):
            ...

        def generate(self, doc):
            ...
"""

from typing import List, Dict

# Re-export from base module
from dcnet_apps.htkk.declarations.base import (
    DeclarationConfig,
    DeclarationPeriod,
    register,
    get_declaration_config,
    get_all_declarations,
    get_supported_codes,
)


def get_supported_declarations() -> List[Dict]:
    """
    Trả về danh sách các loại tờ khai được hỗ trợ.

    Returns:
        List of dicts với format:
        [
            {
                "code": "01/GTGT",
                "name": "Tờ khai thuế giá trị gia tăng",
                "short_name": "GTGT khấu trừ",
                "period": "Quý",
                "description": "(Dành cho người nộp thuế...)",
            },
            ...
        ]
    """
    configs = get_all_declarations()

    period_map = {
        "monthly": "Tháng",
        "quarterly": "Quý",
        "yearly": "Năm",
    }

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
