"""
Simple embed workflow diagram using header block.
Run: bench --site flow.local execute dcnet_apps.workflow_diagram.simple_embed.embed
"""

import frappe
import json


def embed():
    """Embed workflow diagram as header with custom HTML."""

    workspace = frappe.get_doc("Workspace", "Buying")
    content = json.loads(workspace.content or "[]")

    # Remove any existing workflow blocks
    content = [b for b in content if not (
        b.get("type") == "custom_block" and
        b.get("data", {}).get("custom_block_name") == "Buying Workflow Diagram"
    )]
    content = [b for b in content if not (
        b.get("type") == "header" and
        "workflow-diagram" in b.get("data", {}).get("text", "")
    )]

    # Create workflow diagram HTML
    diagram_html = '''<div class="workflow-diagram-inline" id="buying-workflow-diagram">
<style>
.workflow-diagram-inline {
    padding: 20px;
    background: var(--card-bg);
    border-radius: 8px;
    border: 1px solid var(--border-color);
    margin-bottom: 20px;
}
.workflow-diagram-inline h4 {
    margin: 0 0 15px;
    font-weight: 600;
    color: var(--text-color);
}
.workflow-diagram-inline .workflow-nodes {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    align-items: center;
}
.workflow-diagram-inline .workflow-node {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
}
.workflow-diagram-inline .workflow-node:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.workflow-diagram-inline .workflow-arrow {
    font-size: 20px;
    color: var(--text-muted);
    margin: 0 5px;
}
.workflow-diagram-inline .node-blue { background: #dbeafe; color: #1e40af; border: 2px solid #3b82f6; }
.workflow-diagram-inline .node-green { background: #dcfce7; color: #166534; border: 2px solid #22c55e; }
.workflow-diagram-inline .node-orange { background: #ffedd5; color: #9a3412; border: 2px solid #f97316; }
.workflow-diagram-inline .node-purple { background: #f3e8ff; color: #7c3aed; border: 2px solid #a855f7; }
.workflow-diagram-inline .workflow-group {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px dashed var(--border-color);
}
.workflow-diagram-inline .group-label {
    font-size: 11px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
}
</style>
<h4>📊 Quy trình Mua hàng</h4>
<div class="workflow-nodes">
    <div class="workflow-node node-blue" onclick="frappe.set_route('List', 'Material Request')">
        📋 Yêu cầu & Đặt hàng
    </div>
    <span class="workflow-arrow">→</span>
    <div class="workflow-node node-green" onclick="frappe.set_route('List', 'Purchase Receipt')">
        📦 Nhận hàng
    </div>
    <span class="workflow-arrow">→</span>
    <div class="workflow-node node-orange" onclick="frappe.set_route('List', 'Purchase Invoice')">
        💳 Hóa đơn & Thanh toán
    </div>
</div>
<div class="workflow-group">
    <div class="group-label">Danh mục</div>
    <div class="workflow-nodes">
        <div class="workflow-node node-purple" onclick="frappe.set_route('List', 'Supplier')">
            👥 Nhà cung cấp
        </div>
    </div>
</div>
</div>'''

    # Add as header block at the beginning
    workflow_block = {
        "id": frappe.generate_hash(length=10),
        "type": "header",
        "data": {
            "text": diagram_html,
            "col": 12
        }
    }

    content.insert(0, workflow_block)

    workspace.content = json.dumps(content)
    workspace.save()
    frappe.db.commit()

    print("✅ Embedded workflow diagram as header block")
    print("ℹ️ Hard refresh (Ctrl+Shift+R) to see changes")


if __name__ == "__main__":
    embed()
