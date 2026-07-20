"""HTKK Declaration CT Value — dòng chỉ tiêu trong bảng tổng hợp."""

from frappe.model.document import Document


class HTKKDeclarationCTValue(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        auto_value: DF.Currency
        ct_name: DF.Data
        data_source: DF.SmallText | None
        is_manual: DF.Check
        label: DF.Data | None
        manual_value: DF.Currency
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
    # end: auto-generated types
