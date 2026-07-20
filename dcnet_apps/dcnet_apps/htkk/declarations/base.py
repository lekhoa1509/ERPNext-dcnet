"""
Base classes for HTKK Declaration Types.

Sử dụng @register decorator để tự động đăng ký declaration type.
Chỉ cần tạo 1 file Python với class kế thừa DeclarationConfig là đủ.

Example:
    from dcnet_apps.htkk.declarations.base import DeclarationConfig, register

    @register
    class VAT01GTGT(DeclarationConfig):
        code = "01/GTGT"
        name = "Tờ khai thuế giá trị gia tăng"
        ...

        def compute_chi_tieu(self, doc):
            ...

        def generate(self, doc):
            ...
"""

import os
import importlib
import frappe
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class DeclarationPeriod(Enum):
    """Kỳ kê khai."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


# Global registry - auto-populated by @register decorator
_REGISTRY: Dict[str, "DeclarationConfig"] = {}
_SCANNED = False


def register(cls):
    """
    Decorator để tự động đăng ký declaration config.

    Usage:
        @register
        class VAT01GTGT(DeclarationConfig):
            code = "01/GTGT"
            ...
    """
    # Instantiate and register
    instance = cls()
    _REGISTRY[instance.code] = instance
    return cls


def _scan_declaration_modules():
    """Auto-import tất cả modules trong declarations/ folder."""
    global _SCANNED
    if _SCANNED:
        return

    declarations_dir = os.path.dirname(__file__)
    for filename in os.listdir(declarations_dir):
        if filename.endswith(".py") and not filename.startswith("_") and filename != "base.py":
            module_name = filename[:-3]  # Remove .py
            try:
                importlib.import_module(f"dcnet_apps.htkk.declarations.{module_name}")
            except Exception as e:
                frappe.log_error(f"Error importing declaration module {module_name}: {e}")

    _SCANNED = True


def get_declaration_config(code: str) -> Optional["DeclarationConfig"]:
    """
    Get declaration config by code.

    Args:
        code: Declaration type code (e.g., "01/GTGT", "03/TNDN")

    Returns:
        DeclarationConfig instance or None
    """
    _scan_declaration_modules()
    return _REGISTRY.get(code)


def get_all_declarations() -> List["DeclarationConfig"]:
    """Get all registered declaration configs."""
    _scan_declaration_modules()
    return list(_REGISTRY.values())


def get_supported_codes() -> List[str]:
    """Get list of supported declaration type codes."""
    _scan_declaration_modules()
    return list(_REGISTRY.keys())


class DeclarationConfig(ABC):
    """
    Base class cho declaration type configuration.

    Kế thừa class này và implement compute_chi_tieu() và generate() để
    tạo một loại tờ khai mới.

    Attributes:
        code: Mã tờ khai (e.g., "01/GTGT")
        name: Tên đầy đủ
        short_name: Tên ngắn
        xsd_file: Tên file XSD (e.g., "01_GTGT_TT80_283.xsd")
        period: Kỳ kê khai (monthly, quarterly, yearly)
        circular: Số thông tư
        has_appendices: Có phụ lục không
        title: Tiêu đề hiển thị trên form
        subtitle: Phụ đề
        appendices: Danh sách phụ lục [{key, label, type}]
        sections: Cấu trúc form [{id, title, indicators, subsections}]
    """

    # === METADATA (bắt buộc) ===
    code: str = ""
    name: str = ""
    short_name: str = ""
    xsd_file: str = ""
    period: str = "quarterly"  # monthly, quarterly, yearly
    circular: str = ""
    has_appendices: bool = False

    # === FRONTEND CONFIG ===
    title: str = ""
    subtitle: str = ""
    appendices: List[Dict] = []
    sections: List[Dict] = []

    # === ABSTRACT METHODS ===

    @abstractmethod
    def compute_chi_tieu(self, doc) -> Dict:
        """
        Tính toán các chỉ tiêu từ dữ liệu kế toán.

        Args:
            doc: HTKK Declaration document

        Returns:
            Dict với format:
            {
                "ct21": {"auto_value": 0, "label": "Không phát sinh", "source": "Check logic"},
                "ct22": {"auto_value": 1000000, "label": "Thuế còn khấu trừ", "source": "Kỳ trước"},
                ...
            }
        """
        pass

    @abstractmethod
    def generate(self, doc) -> Dict:
        """
        Generate full declaration data cho preview/export.

        Args:
            doc: HTKK Declaration document

        Returns:
            Dict với format:
            {
                "chi_tieu": {"ct21": 0, "ct22": 1000000, ...},
                "phu_luc": {"PL01_1_GTGT": [...], ...},
                "sources": {"ct21": "Check logic", ...}
            }
        """
        pass

    # === HELPER METHODS ===

    def _get_indicator_values(self, doc) -> Dict:
        """
        Lấy giá trị chỉ tiêu từ ct_values table.
        Ưu tiên manual_value nếu is_manual=True.
        """
        return {
            row.ct_name: (row.manual_value if row.is_manual else row.auto_value)
            for row in doc.ct_values
        }

    def _query_gl_sum(self, doc, account_patterns: List[str], credit_minus_debit: bool = True) -> float:
        """
        Helper query GL Entry sum.

        Args:
            doc: Declaration document
            account_patterns: List of account patterns (e.g., ["511%", "512%"])
            credit_minus_debit: True = credit - debit, False = debit - credit

        Returns:
            Total sum
        """
        if not account_patterns:
            return 0.0

        # Build parameterized conditions for account patterns
        pattern_params = {f"pattern_{i}": p for i, p in enumerate(account_patterns)}
        conditions = " OR ".join([f"account LIKE %(pattern_{i})s" for i in range(len(account_patterns))])
        # sum_expr is safe - only two fixed values, no user input
        sum_expr = "SUM(credit - debit)" if credit_minus_debit else "SUM(debit - credit)"

        result = frappe.db.sql("""
            SELECT {sum_expr} as total
            FROM `tabGL Entry`
            WHERE company = %(company)s
            AND posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND is_cancelled = 0
            AND ({conditions})
        """.format(sum_expr=sum_expr, conditions=conditions), {
            "company": doc.company,
            "from_date": doc.from_date,
            "to_date": doc.to_date,
            **pattern_params
        })

        return result[0][0] or 0.0 if result else 0.0

    def _get_previous_period_value(self, doc, ct_name: str, default: float = 0.0) -> float:
        """
        Lấy giá trị chỉ tiêu từ kỳ trước.

        Args:
            doc: Declaration document
            ct_name: Indicator name (e.g., "ct43")
            default: Default value if not found
        """
        # Tính kỳ trước
        prev_period = doc.period - 1 if doc.period > 1 else (12 if doc.period_type == "Tháng" else 4)
        prev_year = doc.year if doc.period > 1 else doc.year - 1

        prev_name = frappe.db.get_value(
            "HTKK Declaration",
            {
                "company": doc.company,
                "declaration_type": doc.declaration_type,
                "period_type": doc.period_type,
                "period": prev_period,
                "year": prev_year,
                "docstatus": ["!=", 2]  # Not cancelled
            },
            "name"
        )

        if not prev_name:
            return default

        ct_value = frappe.db.get_value(
            "HTKK Declaration CT Value",
            {"parent": prev_name, "ct_name": ct_name},
            ["auto_value", "manual_value", "is_manual"],
            as_dict=True
        )

        if not ct_value:
            return default

        return ct_value.manual_value if ct_value.is_manual else ct_value.auto_value

    # === SERIALIZATION ===

    def to_dict(self) -> Dict:
        """Convert config to dict for API response."""
        return {
            "code": self.code,
            "name": self.name,
            "short_name": self.short_name,
            "xsd_file": self.xsd_file,
            "period": self.period,
            "circular": self.circular,
            "has_appendices": self.has_appendices,
            "title": self.title or self.name,
            "subtitle": self.subtitle,
            "appendices": self.appendices,
            "sections": self.sections,
        }

    def get_period_enum(self) -> DeclarationPeriod:
        """Get period as enum."""
        return DeclarationPeriod(self.period)
