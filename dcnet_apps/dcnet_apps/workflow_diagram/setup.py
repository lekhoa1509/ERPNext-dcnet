"""
Setup Workflow Diagram Custom Block

Creates the Custom HTML Block and adds it to Buying workspace.
Run with: bench --site flow.local execute dcnet_apps.workflow_diagram.setup.setup_workflow_diagram_block
"""

import frappe
import json


def setup_workflow_diagram_block():
    """Create Custom HTML Block for Workflow Diagram and add to Buying workspace."""

    block_name = "Buying Workflow Diagram"

    # HTML template
    html = """
<div class="workflow-diagram-wrapper" data-workspace="Buying">
    <div class="workflow-loading">Đang tải sơ đồ quy trình...</div>
</div>
"""

    # JavaScript to render the diagram
    script = """
(function() {
    const wrapper = cur_block.querySelector('.workflow-diagram-wrapper');
    if (!wrapper) return;

    const workspace = wrapper.dataset.workspace;

    frappe.call({
        method: 'dcnet_apps.workflow_diagram.api.get_workflow_config',
        args: { workspace_name: workspace },
        callback: function(r) {
            if (!r.message) {
                wrapper.innerHTML = '<div class="workflow-error">Không có dữ liệu workflow</div>';
                return;
            }

            const config = r.message;
            if (!config.nodes || config.nodes.length === 0) {
                wrapper.innerHTML = '<div class="workflow-empty">Chưa có workflow nodes</div>';
                return;
            }

            // Render using WorkflowDiagramBlock if available
            if (window.WorkflowDiagramRenderer) {
                wrapper.innerHTML = window.WorkflowDiagramRenderer.render(config);
            } else {
                // Fallback: simple render
                wrapper.innerHTML = renderSimpleDiagram(config);
            }
        },
        error: function(err) {
            wrapper.innerHTML = '<div class="workflow-error">Lỗi tải workflow: ' + (err.message || 'Unknown') + '</div>';
        }
    });

    function renderSimpleDiagram(config) {
        // Simple SVG rendering
        const nodes = config.nodes || [];
        const connections = config.connections || [];
        const groups = config.groups || [];

        // Color mapping
        const colors = {
            blue: { bg: '#dbeafe', border: '#3b82f6', text: '#1e40af' },
            green: { bg: '#dcfce7', border: '#22c55e', text: '#166534' },
            orange: { bg: '#ffedd5', border: '#f97316', text: '#9a3412' },
            purple: { bg: '#f3e8ff', border: '#a855f7', text: '#7c3aed' },
            red: { bg: '#fee2e2', border: '#ef4444', text: '#991b1b' },
            auto: { bg: '#f1f5f9', border: '#64748b', text: '#334155' }
        };

        // Layout calculation
        const nodeWidth = 180;
        const nodeHeight = 60;
        const gapX = 80;
        const gapY = 40;
        const padding = 40;

        // Position nodes by group
        const groupMap = {};
        groups.forEach((g, gi) => {
            groupMap[g.name] = gi;
        });

        const positions = {};
        let currentX = padding;
        let maxY = padding;

        // Group nodes by workflow_group
        const nodesByGroup = {};
        nodes.forEach(node => {
            const group = node.group || 'default';
            if (!nodesByGroup[group]) nodesByGroup[group] = [];
            nodesByGroup[group].push(node);
        });

        // Calculate positions
        Object.keys(nodesByGroup).forEach((groupName, groupIdx) => {
            const groupNodes = nodesByGroup[groupName];
            groupNodes.forEach((node, nodeIdx) => {
                positions[node.id] = {
                    x: currentX + nodeIdx * (nodeWidth + gapX),
                    y: padding + groupIdx * (nodeHeight + gapY * 2)
                };
            });
            currentX = padding; // Reset for next group
            maxY = Math.max(maxY, padding + (groupIdx + 1) * (nodeHeight + gapY * 2));
        });

        // Calculate SVG size
        const maxX = Math.max(...Object.values(positions).map(p => p.x)) + nodeWidth + padding;
        const svgWidth = Math.max(maxX, 400);
        const svgHeight = Math.max(maxY, 200);

        // Build SVG
        let svg = '<svg class="workflow-svg" width="' + svgWidth + '" height="' + svgHeight + '" viewBox="0 0 ' + svgWidth + ' ' + svgHeight + '">';

        // Draw connections
        connections.forEach(conn => {
            const from = positions[conn.from];
            const to = positions[conn.to];
            if (from && to) {
                const startX = from.x + nodeWidth;
                const startY = from.y + nodeHeight / 2;
                const endX = to.x;
                const endY = to.y + nodeHeight / 2;
                const midX = (startX + endX) / 2;

                svg += '<path class="workflow-edge" d="M' + startX + ',' + startY +
                       ' C' + midX + ',' + startY + ' ' + midX + ',' + endY + ' ' + endX + ',' + endY +
                       '" fill="none" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrowhead)"/>';
            }
        });

        // Arrow marker
        svg += '<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">';
        svg += '<polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8"/></marker></defs>';

        // Draw nodes
        nodes.forEach(node => {
            const pos = positions[node.id];
            if (!pos) return;

            const color = colors[node.color] || colors.auto;

            svg += '<g class="workflow-node" data-node="' + node.id + '">';
            svg += '<rect class="workflow-node-rect" x="' + pos.x + '" y="' + pos.y +
                   '" width="' + nodeWidth + '" height="' + nodeHeight +
                   '" rx="8" fill="' + color.bg + '" stroke="' + color.border + '" stroke-width="2"/>';
            svg += '<text x="' + (pos.x + nodeWidth/2) + '" y="' + (pos.y + nodeHeight/2 + 5) +
                   '" text-anchor="middle" fill="' + color.text + '" font-size="13" font-weight="500">' +
                   node.label + '</text>';
            svg += '</g>';
        });

        svg += '</svg>';

        return '<div class="workflow-diagram-block"><h4 class="workflow-title">Quy trình Mua hàng</h4><div class="workflow-container">' + svg + '</div></div>';
    }
})();
"""

    # CSS styles
    style = """
.workflow-diagram-wrapper {
    min-height: 200px;
}
.workflow-loading, .workflow-error, .workflow-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 200px;
    color: var(--text-muted);
}
.workflow-error {
    color: var(--red-500);
}
.workflow-diagram-block {
    padding: 15px;
    background: var(--card-bg);
    border-radius: 8px;
    border: 1px solid var(--border-color);
}
.workflow-title {
    margin: 0 0 15px 0;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-color);
}
.workflow-container {
    overflow-x: auto;
}
.workflow-node {
    cursor: pointer;
    transition: transform 0.15s ease;
}
.workflow-node:hover {
    transform: scale(1.02);
}
"""

    # Check if block exists
    if frappe.db.exists("Custom HTML Block", block_name):
        # Update existing
        block = frappe.get_doc("Custom HTML Block", block_name)
        block.html = html
        block.script = script
        block.style = style
        block.save()
        print(f"✅ Updated Custom HTML Block: {block_name}")
    else:
        # Create new
        block = frappe.get_doc({
            "doctype": "Custom HTML Block",
            "name": block_name,
            "html": html,
            "script": script,
            "style": style,
            "private": 0
        })
        block.insert()
        print(f"✅ Created Custom HTML Block: {block_name}")

    frappe.db.commit()

    # Add to Buying workspace
    add_block_to_workspace("Buying", block_name)

    return block_name


def add_block_to_workspace(workspace_name: str, block_name: str):
    """Add the custom block to workspace content."""

    workspace = frappe.get_doc("Workspace", workspace_name)

    # Parse existing content
    content = json.loads(workspace.content or "[]")

    # Check if block already exists
    for block in content:
        if block.get("type") == "custom_block" and block.get("data", {}).get("custom_block_name") == block_name:
            print(f"ℹ️ Block already in workspace: {workspace_name}")
            return

    # Add workflow diagram block at the beginning (after any header)
    new_block = {
        "id": frappe.generate_hash(length=10),
        "type": "custom_block",
        "data": {
            "custom_block_name": block_name,
            "col": 12
        }
    }

    # Insert after first header if exists, otherwise at beginning
    insert_idx = 0
    for i, block in enumerate(content):
        if block.get("type") == "header":
            insert_idx = i + 1
            break

    content.insert(insert_idx, new_block)

    # Save
    workspace.content = json.dumps(content)
    workspace.save()
    frappe.db.commit()

    print(f"✅ Added workflow diagram to workspace: {workspace_name}")


if __name__ == "__main__":
    setup_workflow_diagram_block()
