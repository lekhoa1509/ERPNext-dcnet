"""
Add Custom HTML Block to Workspace Custom Blocks tab.
Run: bench --site flow.local execute dcnet_apps.workflow_diagram.add_to_workspace.add_block
"""

import frappe


def add_block():
    """Add Buying Workflow Diagram to Buying workspace custom blocks."""

    workspace_name = "Buying"
    block_name = "Buying Workflow Diagram"

    # Get workspace
    workspace = frappe.get_doc("Workspace", workspace_name)

    # Check if already exists
    for cb in workspace.custom_blocks or []:
        if cb.custom_block_name == block_name:
            print(f"ℹ️ Block already exists in workspace: {block_name}")
            return

    # Add custom block
    workspace.append("custom_blocks", {
        "custom_block_name": block_name,
        "label": "Quy trình Mua hàng"
    })

    workspace.save()
    frappe.db.commit()

    print(f"✅ Added '{block_name}' to workspace '{workspace_name}'")
    print(f"ℹ️ Reload the workspace page to see the block")


if __name__ == "__main__":
    add_block()
