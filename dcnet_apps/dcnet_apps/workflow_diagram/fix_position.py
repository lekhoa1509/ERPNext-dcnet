"""
Move workflow diagram to top of workspace.
Run: bench --site flow.local execute dcnet_apps.workflow_diagram.fix_position.fix
"""

import frappe
import json


def fix():
    """Move workflow diagram block to the top of Buying workspace."""

    workspace = frappe.get_doc("Workspace", "Buying")
    content = json.loads(workspace.content or "[]")

    # Find and remove the workflow diagram block
    workflow_block = None
    new_content = []
    for block in content:
        if block.get("type") == "custom_block" and block.get("data", {}).get("custom_block_name") == "Buying Workflow Diagram":
            workflow_block = block
        else:
            new_content.append(block)

    if not workflow_block:
        print("❌ Workflow diagram block not found in content")
        return

    # Insert at the beginning
    new_content.insert(0, workflow_block)

    # Save
    workspace.content = json.dumps(new_content)
    workspace.save()
    frappe.db.commit()

    print("✅ Moved workflow diagram to top of workspace")
    print("ℹ️ Reload the page to see changes")


if __name__ == "__main__":
    fix()
