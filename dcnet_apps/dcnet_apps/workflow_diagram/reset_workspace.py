"""
Reset Buying workspace to clean state.
Run: bench --site flow.local execute dcnet_apps.workflow_diagram.reset_workspace.reset
"""

import frappe
import json


def reset():
    """Reset Buying workspace content to original ERPNext state."""

    # Original ERPNext Buying workspace content
    original_content = [
        {"id": "j3dJGo8Ok6", "type": "chart", "data": {"chart_name": "Purchase Order Trends", "col": 12}},
        {"id": "k75jSq2D6Z", "type": "number_card", "data": {"number_card_name": "Purchase Orders Count", "col": 4}},
        {"id": "UPXys0lQLj", "type": "number_card", "data": {"number_card_name": "Total Purchase Amount", "col": 4}},
        {"id": "yQGK3eb2hg", "type": "number_card", "data": {"number_card_name": "Average Order Values", "col": 4}},
        {"id": "oN7lXSwQji", "type": "spacer", "data": {"col": 12}},
        {"id": "Xe2GVLOq8J", "type": "header", "data": {"text": "<span class=\"h4\"><b>Báo cáo & Danh mục</b></span>", "col": 12}},
        {"id": "QwqyG6XuUt", "type": "card", "data": {"card_name": "Buying", "col": 4}},
        {"id": "bTPjOxC_N_", "type": "card", "data": {"card_name": "Items & Pricing", "col": 4}},
        {"id": "87ht0HIneb", "type": "card", "data": {"card_name": "Settings", "col": 4}},
        {"id": "EDOsBOmwgw", "type": "card", "data": {"card_name": "Supplier", "col": 4}},
        {"id": "oWNNIiNb2i", "type": "card", "data": {"card_name": "Supplier Scorecard", "col": 4}},
        {"id": "7F_13-ihHB", "type": "card", "data": {"card_name": "Key Reports", "col": 4}},
        {"id": "pfwiLvionl", "type": "card", "data": {"card_name": "Other Reports", "col": 4}},
        {"id": "8ySDy6s4qn", "type": "card", "data": {"card_name": "Regional", "col": 4}}
    ]

    workspace = frappe.get_doc("Workspace", "Buying")
    workspace.content = json.dumps(original_content)
    workspace.save()
    frappe.db.commit()

    print("✅ Reset Buying workspace to clean state")


if __name__ == "__main__":
    reset()
