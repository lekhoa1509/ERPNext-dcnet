"""HTKK Account Mapping — child table cho HTKK Settings."""

from frappe.model.document import Document


class HTKKAccountMapping(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        account: DF.Link | None
        account_code: DF.Data
        company: DF.Link
        description: DF.Data | None
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
        role: DF.Literal[
            "",
            "OUTPUT_VAT",
            "OUTPUT_VAT_IMPORT",
            "INPUT_VAT",
            "INPUT_VAT_FIXED_ASSET",
            "CIT_PAYABLE",
            "CIT_EXPENSE_CURRENT",
            "CIT_EXPENSE_DEFERRED",
            "PIT_PAYABLE",
            "REVENUE",
            "REVENUE_FINANCIAL",
            "REVENUE_DEDUCTION",
            "COGS",
            "EXPENSE_FINANCIAL",
            "EXPENSE_SELLING",
            "EXPENSE_ADMIN",
            "INCOME_OTHER",
            "EXPENSE_OTHER",
            "CASH",
            "BANK",
            "CASH_IN_TRANSIT",
            "RECEIVABLE",
            "PAYABLE",
            "EQUITY",
            "RETAINED_EARNINGS",
            "FIXED_ASSET_TANGIBLE",
            "FIXED_ASSET_INTANGIBLE",
            "DEPRECIATION",
            "INVENTORY_RAW_MATERIAL",
            "INVENTORY_TOOLS",
            "INVENTORY_WIP",
            "INVENTORY_FINISHED_GOODS",
            "INVENTORY_MERCHANDISE",
        ]
    # end: auto-generated types

    pass
