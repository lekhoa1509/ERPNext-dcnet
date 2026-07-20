# Workflow Diagram Block - Proposal

> **Ngày tạo:** 18/03/2026
> **Tác giả:** Nguyễn Hoàng Long
> **Tham chiếu:** MISA Next workflow visualization (project_docs/Pasted image*.png)

---

## 1. Tổng quan

### 1.1 Mục tiêu

Tạo một **Workflow Diagram Block** tự động hiển thị trên trang chính của Workspace, cho phép:
- Visualize quy trình nghiệp vụ dưới dạng biểu đồ tương tác
- Tự động sinh từ cấu hình **Workspace Sidebar JSON**
- Hover vào node hiển thị dropdown menu các hành động
- Click để điều hướng đến DocType/Report/Page tương ứng

### 1.2 Ý tưởng chính

```
┌──────────────────────────────────────────────────────────────────┐
│  Workspace Sidebar JSON                                          │
│  ┌─────────────────┐                                             │
│  │ Section Break   │◄── is_workflow_node: true                   │
│  │ (Yêu cầu & Đặt  │    workflow_sequence: 1                     │
│  │  hàng)          │    workflow_row: 1                          │
│  │                 │    workflow_icon_style: "circle"            │
│  │  ├─ Link 1      │    workflow_color: "red"                    │
│  │  ├─ Link 2      │    workflow_connects_to: ["Nhận hàng"]      │
│  │  └─ Link 3      │                                             │
│  └─────────────────┘                                             │
└──────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│  Workflow Diagram Block (auto-rendered on Workspace)             │
│                                                                  │
│   ┌───────┐         ┌───────┐         ┌───────┐                  │
│   │   📋  │────────▶│   📦  │────────▶│   💳  │                  │
│   │Yêu cầu│         │Nhận   │         │Thanh  │                  │
│   │& Đặt  │         │hàng   │         │toán   │                  │
│   └───┬───┘         └───────┘         └───────┘                  │
│       │                                                          │
│       ▼ (hover dropdown)                                         │
│   ┌─────────────────┐                                            │
│   │ • Material Req  │                                            │
│   │ • RFQ           │                                            │
│   │ • Supplier Quot │                                            │
│   │ • Purchase Order│                                            │
│   └─────────────────┘                                            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Kiến trúc giải pháp

### 2.1 Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Browser)                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  WorkflowDiagram Block (JS Class)                            │  │
│  │  ├── render() → SVG Canvas                                   │  │
│  │  ├── renderNodes() → Icon + Label + Dropdown                 │  │
│  │  ├── renderConnections() → Arrows/Lines                      │  │
│  │  └── bindEvents() → Hover, Click handlers                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                               ▲                                     │
│                               │ JSON Config                         │
└───────────────────────────────│─────────────────────────────────────┘
                                │
┌───────────────────────────────│─────────────────────────────────────┐
│                        BACKEND (Frappe)                             │
│                               │                                     │
│  ┌────────────────────────────┴─────────────────────────────────┐  │
│  │  API: frappe.call("dcnet_apps.api.get_workflow_config")      │  │
│  │  ├── Read Workspace Sidebar                                  │  │
│  │  ├── Filter items where is_workflow_node = 1                 │  │
│  │  ├── Build node graph with connections                       │  │
│  │  └── Return JSON config for rendering                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                               ▲                                     │
│                               │                                     │
│  ┌────────────────────────────┴─────────────────────────────────┐  │
│  │  Extended Workspace Sidebar Item (DocType)                   │  │
│  │  + is_workflow_node (Check)                                  │  │
│  │  + workflow_sequence (Int)                                   │  │
│  │  + workflow_row (Int)                                        │  │
│  │  + workflow_icon_style (Select)                              │  │
│  │  + workflow_color (Select)                                   │  │
│  │  + workflow_connects_to (JSON)                               │  │
│  │  + workflow_group (Data)                                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Components

| Component | Location | Mô tả |
|-----------|----------|-------|
| **Workspace Sidebar Item Extension** | `frappe/desk/doctype/workspace_sidebar_item/` | Custom Fields cho workflow config |
| **Workflow Config API** | `dcnet_apps/api/workflow.py` | API endpoint lấy config |
| **WorkflowDiagram Block** | `dcnet_apps/public/js/workflow_diagram.js` | Frontend rendering |
| **CSS Styles** | `dcnet_apps/public/css/workflow_diagram.css` | Styles cho nodes, arrows |
| **Workspace Integration** | `hooks.py` + `install.py` | Auto-inject block vào workspace |

---

## 3. Backend Implementation

### 3.1 Extend Workspace Sidebar Item

**File:** `dcnet_apps/dcnet_apps/custom_fields/workspace_sidebar_item.json`

```json
{
  "doctype": "Custom Field",
  "custom_fields": [
    {
      "fieldname": "workflow_section",
      "fieldtype": "Section Break",
      "label": "Workflow Configuration",
      "collapsible": 1,
      "insert_after": "navigate_to_tab"
    },
    {
      "fieldname": "is_workflow_node",
      "fieldtype": "Check",
      "label": "Is Workflow Node",
      "description": "Mark this item as a workflow node to show in diagram",
      "default": "0",
      "insert_after": "workflow_section"
    },
    {
      "fieldname": "workflow_sequence",
      "fieldtype": "Int",
      "label": "Workflow Sequence",
      "description": "Order in workflow (left to right)",
      "depends_on": "is_workflow_node",
      "insert_after": "is_workflow_node"
    },
    {
      "fieldname": "workflow_row",
      "fieldtype": "Int",
      "label": "Workflow Row",
      "description": "Row position (for multi-row layouts)",
      "default": "1",
      "depends_on": "is_workflow_node",
      "insert_after": "workflow_sequence"
    },
    {
      "fieldname": "workflow_icon_style",
      "fieldtype": "Select",
      "label": "Workflow Icon Style",
      "options": "\ncircle\nsquare\ndiamond\nhexagon\nrounded-square",
      "default": "circle",
      "depends_on": "is_workflow_node",
      "insert_after": "workflow_row"
    },
    {
      "fieldname": "workflow_color",
      "fieldtype": "Select",
      "label": "Workflow Color",
      "options": "\nred\norange\nyellow\ngreen\nblue\npurple\ngray",
      "default": "blue",
      "depends_on": "is_workflow_node",
      "insert_after": "workflow_icon_style"
    },
    {
      "fieldname": "workflow_connects_to",
      "fieldtype": "Small Text",
      "label": "Connects To",
      "description": "JSON array of target node labels, e.g., [\"Nhận hàng\", \"Thanh toán\"]",
      "depends_on": "is_workflow_node",
      "insert_after": "workflow_color"
    },
    {
      "fieldname": "workflow_group",
      "fieldtype": "Data",
      "label": "Workflow Group",
      "description": "Group name for visually grouping nodes",
      "depends_on": "is_workflow_node",
      "insert_after": "workflow_connects_to"
    }
  ]
}
```

### 3.2 API Endpoint

**File:** `dcnet_apps/dcnet_apps/api/workflow.py`

```python
import frappe
import json

@frappe.whitelist()
def get_workflow_config(workspace_sidebar_name):
    """
    Get workflow configuration from Workspace Sidebar for rendering diagram.

    Returns:
    {
        "nodes": [
            {
                "id": "node_1",
                "label": "Yêu cầu & Đặt hàng",
                "icon": "file-text",
                "sequence": 1,
                "row": 1,
                "style": "circle",
                "color": "red",
                "group": "ordering",
                "children": [
                    {"label": "Material Request", "url": "/app/material-request"},
                    {"label": "Purchase Order", "url": "/app/purchase-order"}
                ]
            }
        ],
        "connections": [
            {"from": "node_1", "to": "node_2", "style": "solid"}
        ],
        "groups": [
            {"name": "ordering", "label": "Đặt hàng", "color": "red"}
        ]
    }
    """
    sidebar = frappe.get_doc("Workspace Sidebar", workspace_sidebar_name)

    nodes = []
    connections = []
    node_map = {}  # label -> node_id mapping

    current_parent = None

    for idx, item in enumerate(sidebar.items):
        if item.is_workflow_node:
            node_id = f"node_{idx}"
            node_map[item.label] = node_id

            # Collect children (items until next workflow node or section break)
            children = []
            for child_item in sidebar.items[idx+1:]:
                if child_item.is_workflow_node or child_item.type == "Section Break":
                    break
                if child_item.child and child_item.type == "Link":
                    children.append({
                        "label": child_item.label,
                        "url": get_item_url(child_item),
                        "icon": child_item.icon or ""
                    })

            nodes.append({
                "id": node_id,
                "label": item.label,
                "icon": item.icon or "circle",
                "sequence": item.workflow_sequence or idx,
                "row": item.workflow_row or 1,
                "style": item.workflow_icon_style or "circle",
                "color": item.workflow_color or "blue",
                "group": item.workflow_group or "",
                "children": children
            })

            # Parse connections
            if item.workflow_connects_to:
                try:
                    targets = json.loads(item.workflow_connects_to)
                    for target in targets:
                        connections.append({
                            "from_label": item.label,
                            "to_label": target,
                            "style": "solid"
                        })
                except json.JSONDecodeError:
                    pass

    # Resolve connection labels to IDs
    resolved_connections = []
    for conn in connections:
        from_id = node_map.get(conn["from_label"])
        to_id = node_map.get(conn["to_label"])
        if from_id and to_id:
            resolved_connections.append({
                "from": from_id,
                "to": to_id,
                "style": conn["style"]
            })

    # Extract groups
    groups = {}
    for node in nodes:
        if node["group"] and node["group"] not in groups:
            groups[node["group"]] = {
                "name": node["group"],
                "label": node["group"].replace("_", " ").title(),
                "color": node["color"]
            }

    return {
        "nodes": sorted(nodes, key=lambda x: (x["row"], x["sequence"])),
        "connections": resolved_connections,
        "groups": list(groups.values())
    }


def get_item_url(item):
    """Generate URL for sidebar item"""
    if item.url:
        return item.url

    link_type = item.link_type
    link_to = item.link_to

    if link_type == "DocType":
        return f"/app/{frappe.scrub(link_to)}"
    elif link_type == "Report":
        return f"/app/query-report/{link_to}"
    elif link_type == "Page":
        return f"/app/{link_to}"
    elif link_type == "Dashboard":
        return f"/app/dashboard-view/{link_to}"
    elif link_type == "Workspace":
        return f"/app/{frappe.scrub(link_to)}"

    return "#"
```

### 3.3 hooks.py Integration

**File:** `dcnet_apps/hooks.py` (add)

```python
# Workflow Diagram
doctype_js = {
    "Workspace Sidebar": "public/js/workspace_sidebar_workflow.js"
}

# Auto-inject workflow block to workspaces
app_include_js = [
    "/assets/dcnet_apps/js/workflow_diagram.bundle.js"
]

app_include_css = [
    "/assets/dcnet_apps/css/workflow_diagram.css"
]
```

---

## 4. Frontend Implementation

### 4.1 Workflow Diagram Block Class

**File:** `dcnet_apps/dcnet_apps/public/js/workflow_diagram.js`

```javascript
/**
 * Workflow Diagram Block for Frappe Workspace
 * Renders interactive workflow visualization from Workspace Sidebar config
 */

class WorkflowDiagram {
    constructor(options) {
        this.wrapper = options.wrapper;
        this.workspace = options.workspace;
        this.config = null;
        this.svg = null;

        // Dimensions
        this.nodeWidth = 100;
        this.nodeHeight = 80;
        this.nodeSpacingX = 60;
        this.nodeSpacingY = 40;
        this.padding = 40;

        // Colors
        this.colors = {
            red: { bg: '#fee2e2', border: '#ef4444', text: '#dc2626' },
            orange: { bg: '#ffedd5', border: '#f97316', text: '#ea580c' },
            yellow: { bg: '#fef3c7', border: '#f59e0b', text: '#d97706' },
            green: { bg: '#dcfce7', border: '#22c55e', text: '#16a34a' },
            blue: { bg: '#dbeafe', border: '#3b82f6', text: '#2563eb' },
            purple: { bg: '#f3e8ff', border: '#a855f7', text: '#9333ea' },
            gray: { bg: '#f3f4f6', border: '#6b7280', text: '#4b5563' }
        };

        this.init();
    }

    async init() {
        try {
            this.config = await this.fetchConfig();
            if (this.config && this.config.nodes.length > 0) {
                this.render();
            }
        } catch (error) {
            console.error('WorkflowDiagram init error:', error);
        }
    }

    async fetchConfig() {
        const response = await frappe.call({
            method: 'dcnet_apps.api.workflow.get_workflow_config',
            args: { workspace_sidebar_name: this.workspace }
        });
        return response.message;
    }

    render() {
        // Calculate dimensions
        const maxRow = Math.max(...this.config.nodes.map(n => n.row));
        const maxSeq = Math.max(...this.config.nodes.map(n => n.sequence));

        const width = (maxSeq + 1) * (this.nodeWidth + this.nodeSpacingX) + this.padding * 2;
        const height = (maxRow) * (this.nodeHeight + this.nodeSpacingY) + this.padding * 2;

        // Create container
        this.wrapper.innerHTML = `
            <div class="workflow-diagram-container">
                <svg class="workflow-diagram-svg" width="${width}" height="${height}">
                    <defs>
                        <marker id="arrowhead" markerWidth="10" markerHeight="7"
                                refX="9" refY="3.5" orient="auto">
                            <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
                        </marker>
                    </defs>
                    <g class="connections"></g>
                    <g class="nodes"></g>
                </svg>
                <div class="workflow-dropdown" style="display: none;"></div>
            </div>
        `;

        this.svg = this.wrapper.querySelector('.workflow-diagram-svg');
        this.dropdown = this.wrapper.querySelector('.workflow-dropdown');

        // Calculate node positions
        this.nodePositions = {};
        this.config.nodes.forEach(node => {
            const x = this.padding + (node.sequence - 1) * (this.nodeWidth + this.nodeSpacingX);
            const y = this.padding + (node.row - 1) * (this.nodeHeight + this.nodeSpacingY);
            this.nodePositions[node.id] = { x, y, node };
        });

        // Render connections first (under nodes)
        this.renderConnections();

        // Render nodes
        this.renderNodes();

        // Bind events
        this.bindEvents();
    }

    renderConnections() {
        const connectionsGroup = this.svg.querySelector('.connections');

        this.config.connections.forEach(conn => {
            const from = this.nodePositions[conn.from];
            const to = this.nodePositions[conn.to];

            if (!from || !to) return;

            const startX = from.x + this.nodeWidth;
            const startY = from.y + this.nodeHeight / 2;
            const endX = to.x;
            const endY = to.y + this.nodeHeight / 2;

            // Create path with curve
            let path;
            if (from.node.row === to.node.row) {
                // Same row - straight line
                path = `M ${startX} ${startY} L ${endX - 10} ${endY}`;
            } else {
                // Different rows - curved line
                const midX = (startX + endX) / 2;
                path = `M ${startX} ${startY}
                        C ${midX} ${startY}, ${midX} ${endY}, ${endX - 10} ${endY}`;
            }

            const line = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            line.setAttribute('d', path);
            line.setAttribute('class', 'workflow-connection');
            line.setAttribute('stroke', '#94a3b8');
            line.setAttribute('stroke-width', '2');
            line.setAttribute('fill', 'none');
            line.setAttribute('stroke-dasharray', conn.style === 'dashed' ? '5,5' : 'none');
            line.setAttribute('marker-end', 'url(#arrowhead)');

            connectionsGroup.appendChild(line);
        });
    }

    renderNodes() {
        const nodesGroup = this.svg.querySelector('.nodes');

        Object.values(this.nodePositions).forEach(({ x, y, node }) => {
            const colors = this.colors[node.color] || this.colors.blue;

            // Create node group
            const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            g.setAttribute('class', 'workflow-node');
            g.setAttribute('data-node-id', node.id);
            g.setAttribute('transform', `translate(${x}, ${y})`);

            // Node shape
            let shape;
            switch (node.style) {
                case 'diamond':
                    shape = this.createDiamond(colors);
                    break;
                case 'hexagon':
                    shape = this.createHexagon(colors);
                    break;
                case 'square':
                    shape = this.createSquare(colors);
                    break;
                case 'rounded-square':
                    shape = this.createRoundedSquare(colors);
                    break;
                default:
                    shape = this.createCircle(colors);
            }
            g.appendChild(shape);

            // Icon
            const iconText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            iconText.setAttribute('x', this.nodeWidth / 2);
            iconText.setAttribute('y', 35);
            iconText.setAttribute('text-anchor', 'middle');
            iconText.setAttribute('class', 'workflow-node-icon');
            iconText.setAttribute('fill', colors.text);
            iconText.textContent = this.getIconChar(node.icon);
            g.appendChild(iconText);

            // Label
            const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            label.setAttribute('x', this.nodeWidth / 2);
            label.setAttribute('y', this.nodeHeight + 15);
            label.setAttribute('text-anchor', 'middle');
            label.setAttribute('class', 'workflow-node-label');
            label.setAttribute('fill', '#374151');
            label.textContent = this.truncateLabel(node.label, 15);
            g.appendChild(label);

            // Badge for children count
            if (node.children && node.children.length > 0) {
                const badge = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                badge.setAttribute('cx', this.nodeWidth - 5);
                badge.setAttribute('cy', 10);
                badge.setAttribute('r', 10);
                badge.setAttribute('fill', colors.border);
                g.appendChild(badge);

                const badgeText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                badgeText.setAttribute('x', this.nodeWidth - 5);
                badgeText.setAttribute('y', 14);
                badgeText.setAttribute('text-anchor', 'middle');
                badgeText.setAttribute('fill', 'white');
                badgeText.setAttribute('font-size', '11');
                badgeText.textContent = node.children.length;
                g.appendChild(badgeText);
            }

            nodesGroup.appendChild(g);
        });
    }

    createCircle(colors) {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        circle.setAttribute('x', 10);
        circle.setAttribute('y', 0);
        circle.setAttribute('width', this.nodeWidth - 20);
        circle.setAttribute('height', this.nodeHeight - 20);
        circle.setAttribute('rx', (this.nodeWidth - 20) / 2);
        circle.setAttribute('ry', (this.nodeHeight - 20) / 2);
        circle.setAttribute('fill', colors.bg);
        circle.setAttribute('stroke', colors.border);
        circle.setAttribute('stroke-width', '2');
        return circle;
    }

    createSquare(colors) {
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', 10);
        rect.setAttribute('y', 0);
        rect.setAttribute('width', this.nodeWidth - 20);
        rect.setAttribute('height', this.nodeHeight - 20);
        rect.setAttribute('fill', colors.bg);
        rect.setAttribute('stroke', colors.border);
        rect.setAttribute('stroke-width', '2');
        return rect;
    }

    createRoundedSquare(colors) {
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', 10);
        rect.setAttribute('y', 0);
        rect.setAttribute('width', this.nodeWidth - 20);
        rect.setAttribute('height', this.nodeHeight - 20);
        rect.setAttribute('rx', 8);
        rect.setAttribute('ry', 8);
        rect.setAttribute('fill', colors.bg);
        rect.setAttribute('stroke', colors.border);
        rect.setAttribute('stroke-width', '2');
        return rect;
    }

    createDiamond(colors) {
        const size = Math.min(this.nodeWidth, this.nodeHeight) - 20;
        const cx = this.nodeWidth / 2;
        const cy = (this.nodeHeight - 20) / 2;
        const points = `${cx},0 ${cx + size/2},${cy} ${cx},${size} ${cx - size/2},${cy}`;

        const diamond = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        diamond.setAttribute('points', points);
        diamond.setAttribute('fill', colors.bg);
        diamond.setAttribute('stroke', colors.border);
        diamond.setAttribute('stroke-width', '2');
        return diamond;
    }

    createHexagon(colors) {
        const w = this.nodeWidth - 20;
        const h = this.nodeHeight - 20;
        const points = `${w*0.25},0 ${w*0.75},0 ${w},${h/2} ${w*0.75},${h} ${w*0.25},${h} 0,${h/2}`;

        const hex = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        hex.setAttribute('points', points);
        hex.setAttribute('transform', 'translate(10, 0)');
        hex.setAttribute('fill', colors.bg);
        hex.setAttribute('stroke', colors.border);
        hex.setAttribute('stroke-width', '2');
        return hex;
    }

    getIconChar(icon) {
        // Map Lucide icon names to Unicode or use emoji fallback
        const iconMap = {
            'file-text': '📄',
            'package': '📦',
            'credit-card': '💳',
            'users': '👥',
            'shopping-cart': '🛒',
            'truck': '🚚',
            'receipt': '🧾',
            'wallet': '💰',
            'building': '🏢',
            'settings': '⚙️',
            'bar-chart': '📊',
            'plus-circle': '➕',
            'check-circle': '✅',
            'arrow-right': '➡️'
        };
        return iconMap[icon] || '📋';
    }

    truncateLabel(label, maxLength) {
        if (label.length <= maxLength) return label;
        return label.substring(0, maxLength - 3) + '...';
    }

    bindEvents() {
        const nodes = this.svg.querySelectorAll('.workflow-node');

        nodes.forEach(node => {
            node.addEventListener('mouseenter', (e) => this.showDropdown(e, node));
            node.addEventListener('mouseleave', (e) => this.scheduleHideDropdown());
        });

        this.dropdown.addEventListener('mouseenter', () => {
            clearTimeout(this.hideTimeout);
        });

        this.dropdown.addEventListener('mouseleave', () => {
            this.hideDropdown();
        });
    }

    showDropdown(e, nodeElement) {
        clearTimeout(this.hideTimeout);

        const nodeId = nodeElement.getAttribute('data-node-id');
        const nodeData = this.config.nodes.find(n => n.id === nodeId);

        if (!nodeData || !nodeData.children || nodeData.children.length === 0) {
            return;
        }

        // Build dropdown content
        const items = nodeData.children.map(child => `
            <a href="${child.url}" class="workflow-dropdown-item">
                <span class="workflow-dropdown-icon">${this.getIconChar(child.icon)}</span>
                <span class="workflow-dropdown-label">${child.label}</span>
            </a>
        `).join('');

        this.dropdown.innerHTML = `
            <div class="workflow-dropdown-header">${nodeData.label}</div>
            <div class="workflow-dropdown-items">${items}</div>
        `;

        // Position dropdown
        const rect = nodeElement.getBoundingClientRect();
        const containerRect = this.wrapper.getBoundingClientRect();

        this.dropdown.style.left = (rect.left - containerRect.left + rect.width / 2 - 100) + 'px';
        this.dropdown.style.top = (rect.bottom - containerRect.top + 10) + 'px';
        this.dropdown.style.display = 'block';
    }

    scheduleHideDropdown() {
        this.hideTimeout = setTimeout(() => this.hideDropdown(), 200);
    }

    hideDropdown() {
        this.dropdown.style.display = 'none';
    }
}

// Auto-initialize on workspace load
$(document).on('page-change', function() {
    const workspaceMatch = frappe.get_route_str().match(/^Workspaces\/(.+)$/);
    if (workspaceMatch) {
        const workspaceName = workspaceMatch[1];
        initWorkflowDiagram(workspaceName);
    }
});

function initWorkflowDiagram(workspaceName) {
    // Check if workspace has workflow sidebar configured
    frappe.call({
        method: 'frappe.client.get_value',
        args: {
            doctype: 'Workspace Sidebar',
            filters: { name: workspaceName },
            fieldname: 'name'
        },
        callback: function(r) {
            if (r.message && r.message.name) {
                // Find or create workflow container
                let container = document.querySelector('.workspace-workflow-diagram');
                if (!container) {
                    container = document.createElement('div');
                    container.className = 'workspace-workflow-diagram';

                    // Insert after workspace header
                    const header = document.querySelector('.workspace-header');
                    if (header && header.parentNode) {
                        header.parentNode.insertBefore(container, header.nextSibling);
                    }
                }

                // Initialize diagram
                new WorkflowDiagram({
                    wrapper: container,
                    workspace: workspaceName
                });
            }
        }
    });
}

// Export for external use
frappe.WorkflowDiagram = WorkflowDiagram;
```

### 4.2 CSS Styles

**File:** `dcnet_apps/dcnet_apps/public/css/workflow_diagram.css`

```css
/* Workflow Diagram Container */
.workflow-diagram-container {
    position: relative;
    margin: 20px 0 30px 0;
    padding: 20px;
    background: #f8fafc;
    border-radius: 12px;
    overflow-x: auto;
}

.workflow-diagram-svg {
    display: block;
    margin: 0 auto;
}

/* Node Styles */
.workflow-node {
    cursor: pointer;
    transition: transform 0.2s, filter 0.2s;
}

.workflow-node:hover {
    transform: scale(1.05);
    filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

.workflow-node-icon {
    font-size: 24px;
    font-family: 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif;
}

.workflow-node-label {
    font-size: 12px;
    font-weight: 500;
}

/* Connection Styles */
.workflow-connection {
    transition: stroke-width 0.2s;
}

.workflow-node:hover ~ .connections .workflow-connection {
    stroke-width: 3;
}

/* Dropdown Styles */
.workflow-dropdown {
    position: absolute;
    min-width: 200px;
    max-width: 280px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    z-index: 100;
    animation: dropdownFadeIn 0.2s ease;
}

@keyframes dropdownFadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.workflow-dropdown-header {
    padding: 12px 16px;
    font-weight: 600;
    font-size: 13px;
    color: #374151;
    border-bottom: 1px solid #e5e7eb;
    background: #f9fafb;
    border-radius: 8px 8px 0 0;
}

.workflow-dropdown-items {
    padding: 8px 0;
    max-height: 300px;
    overflow-y: auto;
}

.workflow-dropdown-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    color: #4b5563;
    text-decoration: none;
    transition: background 0.15s;
}

.workflow-dropdown-item:hover {
    background: #f3f4f6;
    color: #111827;
}

.workflow-dropdown-icon {
    font-size: 16px;
    width: 20px;
    text-align: center;
}

.workflow-dropdown-label {
    font-size: 13px;
    flex: 1;
}

/* Responsive */
@media (max-width: 768px) {
    .workflow-diagram-container {
        padding: 10px;
    }

    .workflow-diagram-svg {
        transform: scale(0.8);
        transform-origin: top left;
    }
}

/* Dark mode support */
[data-theme="dark"] .workflow-diagram-container {
    background: #1f2937;
}

[data-theme="dark"] .workflow-dropdown {
    background: #374151;
}

[data-theme="dark"] .workflow-dropdown-header {
    background: #4b5563;
    color: #f9fafb;
    border-color: #6b7280;
}

[data-theme="dark"] .workflow-dropdown-item {
    color: #d1d5db;
}

[data-theme="dark"] .workflow-dropdown-item:hover {
    background: #4b5563;
    color: #f9fafb;
}

[data-theme="dark"] .workflow-node-label {
    fill: #e5e7eb;
}
```

---

## 5. Integration với Workspace

### 5.1 Option A: Auto-inject (Recommended)

**File:** `dcnet_apps/dcnet_apps/install.py` (add)

```python
def after_install():
    """Setup workflow diagram integration"""
    # Create workflow-enabled workspaces
    setup_workspace_workflows()

def setup_workspace_workflows():
    """Configure workflow nodes for each workspace sidebar"""

    # Example: Configure Buying workflow
    buying_workflow = [
        {
            "label": "Yêu cầu & Đặt hàng",
            "sequence": 1,
            "row": 1,
            "style": "rounded-square",
            "color": "blue",
            "connects_to": ["Nhận hàng"]
        },
        {
            "label": "Nhận hàng",
            "sequence": 2,
            "row": 1,
            "style": "rounded-square",
            "color": "green",
            "connects_to": ["Hóa đơn & Thanh toán"]
        },
        {
            "label": "Hóa đơn & Thanh toán",
            "sequence": 3,
            "row": 1,
            "style": "rounded-square",
            "color": "orange",
            "connects_to": []
        }
    ]

    apply_workflow_config("Mua hàng", buying_workflow)

def apply_workflow_config(sidebar_name, workflow_config):
    """Apply workflow configuration to sidebar items"""
    import frappe
    import json

    if not frappe.db.exists("Workspace Sidebar", sidebar_name):
        return

    sidebar = frappe.get_doc("Workspace Sidebar", sidebar_name)

    for config in workflow_config:
        for item in sidebar.items:
            if item.label == config["label"]:
                item.is_workflow_node = 1
                item.workflow_sequence = config["sequence"]
                item.workflow_row = config["row"]
                item.workflow_icon_style = config["style"]
                item.workflow_color = config["color"]
                item.workflow_connects_to = json.dumps(config["connects_to"])
                break

    sidebar.save()
```

### 5.2 Option B: Custom Block in Workspace Content

Alternatively, add workflow block directly to Workspace `content` JSON:

```json
{
  "content": [
    {
      "id": "workflow_1",
      "type": "workflow_diagram",
      "data": {
        "sidebar_name": "Mua hàng",
        "col": 12
      }
    },
    // ... other blocks
  ]
}
```

---

## 6. Cấu trúc files đề xuất

```
dcnet_apps/
├── dcnet_apps/
│   ├── api/
│   │   └── workflow.py                    # API endpoint
│   ├── custom_fields/
│   │   └── workspace_sidebar_item.json    # Custom fields
│   ├── public/
│   │   ├── js/
│   │   │   ├── workflow_diagram.js        # Main component
│   │   │   └── workflow_diagram.bundle.js # Built bundle
│   │   └── css/
│   │       └── workflow_diagram.css       # Styles
│   ├── fixtures/
│   │   └── workflow_configs/              # Predefined workflows
│   │       ├── buying.json
│   │       ├── selling.json
│   │       ├── stock.json
│   │       └── ...
│   ├── hooks.py                           # Include JS/CSS
│   └── install.py                         # Setup workflows
```

---

## 7. Workflow Configuration cho từng module

### 7.1 Mua hàng (Buying)

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Yêu cầu  │───▶│ Nhận     │───▶│ Hóa đơn  │───▶│ Nhà CC   │
│ & Đặt    │    │ hàng     │    │ & TT     │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
• Material Req  • Purchase Rcpt • Purchase Inv  • Supplier
• RFQ           • Landed Cost   • Payment Entry • Supplier Grp
• Supplier Quot • Purchase Ret  • Payment Terms • Price List
• Purchase Ord                                   • Contact
```

### 7.2 Bán hàng (Selling)

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Báo giá  │───▶│ Giao     │───▶│ Hóa đơn  │───▶│ Khách    │
│ & Đơn    │    │ hàng     │    │ & TT     │    │ hàng     │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
• Quotation     • Delivery Note • Sales Invoice • Customer
• Sales Order   • Sales Return  • Payment Entry • Customer Grp
• Blanket Order • Delivery Trip • Credit Note   • Territory
```

### 7.3 Tồn kho (Stock)

```
┌──────────┐
│ Yêu cầu  │
└────┬─────┘
     │
     ├────────────┬────────────┐
     ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Đơn hàng │ │ Phiếu    │ │ Kiểm kê  │
│ mua      │ │ xuất bán │ │ kho      │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Nhận     │ │ Delivery │ │ Stock    │
│ hàng     │ │ Note     │ │ Recon    │
└──────────┘ └──────────┘ └──────────┘
```

---

## 8. Auto-Layout Algorithm

### 8.1 Vấn đề với Manual Layout

Cấu hình `workflow_sequence`, `workflow_row` thủ công có nhược điểm:
- Dễ sai vị trí khi thêm/xóa node
- Khó duy trì khi workflow phức tạp
- Không responsive

### 8.2 Đề xuất: Dagre.js Auto-Layout

**Dagre** là thư viện layout cho directed graphs, tự động tính toán vị trí nodes sao cho:
- Minimize edge crossings
- Consistent left-to-right flow
- Even spacing
- Proper layering

**Install:** `npm install dagre` hoặc CDN

**Cách hoạt động:**

```javascript
import dagre from 'dagre';

function calculateLayout(nodes, connections) {
    // Create graph
    const g = new dagre.graphlib.Graph();
    g.setGraph({
        rankdir: 'LR',      // Left to Right
        ranksep: 80,        // Space between ranks
        nodesep: 40,        // Space between nodes
        marginx: 40,
        marginy: 40
    });
    g.setDefaultEdgeLabel(() => ({}));

    // Add nodes
    nodes.forEach(node => {
        g.setNode(node.id, {
            width: 100,
            height: 80,
            label: node.label
        });
    });

    // Add edges
    connections.forEach(conn => {
        g.setEdge(conn.from, conn.to);
    });

    // Run layout algorithm
    dagre.layout(g);

    // Extract positions
    const positions = {};
    g.nodes().forEach(id => {
        const node = g.node(id);
        positions[id] = { x: node.x, y: node.y };
    });

    return positions;
}
```

### 8.3 Simplified Sidebar Config

Với auto-layout, chỉ cần cấu hình:

| Field | Bắt buộc | Mô tả |
|-------|----------|-------|
| `is_workflow_node` | ✅ | Đánh dấu là node |
| `workflow_connects_to` | ✅ | Danh sách node đích |
| `workflow_color` | ❌ | Màu (optional, auto từ group) |
| `workflow_group` | ❌ | Nhóm để gom cluster |

**KHÔNG cần:** `workflow_sequence`, `workflow_row` (tự động tính)

### 8.4 Grouping & Clustering

Để tạo các box nhóm như MISA:

```javascript
function renderGroups(nodes, groups) {
    // Find bounding box for each group
    groups.forEach(group => {
        const groupNodes = nodes.filter(n => n.group === group.name);
        if (groupNodes.length === 0) return;

        const minX = Math.min(...groupNodes.map(n => n.x)) - 20;
        const minY = Math.min(...groupNodes.map(n => n.y)) - 30;
        const maxX = Math.max(...groupNodes.map(n => n.x + 100)) + 20;
        const maxY = Math.max(...groupNodes.map(n => n.y + 80)) + 20;

        // Draw group box
        svg.append('rect')
            .attr('x', minX)
            .attr('y', minY)
            .attr('width', maxX - minX)
            .attr('height', maxY - minY)
            .attr('fill', group.bgColor)
            .attr('stroke', group.borderColor)
            .attr('rx', 8);

        // Group label
        svg.append('text')
            .attr('x', minX + 10)
            .attr('y', minY - 8)
            .text(group.label);
    });
}
```

### 8.5 Edge Routing

Dagre tự động tính edge routing, nhưng cần smooth:

```javascript
function renderEdges(edges) {
    edges.forEach(edge => {
        const points = edge.points; // Dagre returns control points

        const line = d3.line()
            .x(d => d.x)
            .y(d => d.y)
            .curve(d3.curveBasis); // Smooth curve

        svg.append('path')
            .attr('d', line(points))
            .attr('stroke', '#94a3b8')
            .attr('stroke-width', 2)
            .attr('fill', 'none')
            .attr('marker-end', 'url(#arrowhead)');
    });
}
```

### 8.6 Layout Examples

**Buying (đơn giản - linear):**
```
[Yêu cầu] → [Nhận hàng] → [Hóa đơn] → [NCC]
```
Dagre output: 4 nodes trên 1 hàng, spacing đều

**Stock (phức tạp - branching):**
```
        ┌→ [Đơn mua] → [Nhận hàng] ─┐
[Yêu cầu]                           ├→ [Kiểm kê]
        └→ [Đơn bán] → [Xuất kho] ──┘
```
Dagre output: Multi-layer với branching, auto-balanced

**Cash Accounting (tree):**
```
           ┌→ [Phiếu thu]
[Tiền mặt] ┤
           └→ [Phiếu chi]
```
Dagre output: Center node với 2 nhánh đối xứng

### 8.7 Responsive Considerations

```javascript
function renderResponsive(container, config) {
    const containerWidth = container.offsetWidth;

    if (containerWidth < 600) {
        // Mobile: Stack vertically
        g.setGraph({ rankdir: 'TB' }); // Top to Bottom
    } else {
        // Desktop: Left to Right
        g.setGraph({ rankdir: 'LR' });
    }

    // Re-run layout
    dagre.layout(g);
}
```

### 8.8 Alternative: Grid-based Rank Layout (No External Library)

Nếu không muốn dùng Dagre, có thể dùng thuật toán đơn giản hơn:

```javascript
/**
 * Simple grid-based layout algorithm
 * - Group nodes by "rank" (distance from start)
 * - Position each rank in a column
 * - Center nodes within each rank
 */
function gridLayout(nodes, connections) {
    // 1. Find start nodes (no incoming edges)
    const hasIncoming = new Set(connections.map(c => c.to));
    const startNodes = nodes.filter(n => !hasIncoming.has(n.id));

    // 2. Calculate ranks using BFS
    const ranks = {};
    const queue = startNodes.map(n => ({ id: n.id, rank: 0 }));
    const visited = new Set();

    while (queue.length > 0) {
        const { id, rank } = queue.shift();
        if (visited.has(id)) continue;
        visited.add(id);
        ranks[id] = Math.max(ranks[id] || 0, rank);

        // Find connected nodes
        connections
            .filter(c => c.from === id)
            .forEach(c => {
                queue.push({ id: c.to, rank: rank + 1 });
            });
    }

    // 3. Group by rank
    const byRank = {};
    Object.entries(ranks).forEach(([id, rank]) => {
        if (!byRank[rank]) byRank[rank] = [];
        byRank[rank].push(id);
    });

    // 4. Calculate positions
    const nodeWidth = 120;
    const nodeHeight = 80;
    const gapX = 60;
    const gapY = 40;
    const positions = {};

    Object.entries(byRank).forEach(([rank, ids]) => {
        const x = parseInt(rank) * (nodeWidth + gapX) + 40;
        const totalHeight = ids.length * nodeHeight + (ids.length - 1) * gapY;
        const startY = (400 - totalHeight) / 2; // Center vertically

        ids.forEach((id, index) => {
            positions[id] = {
                x: x,
                y: startY + index * (nodeHeight + gapY)
            };
        });
    });

    return positions;
}
```

**Ưu điểm:** Đơn giản, không dependency, dễ debug
**Nhược điểm:** Không tối ưu edge crossings như Dagre

---

## 9. Visual Mockups

### 9.1 Mua hàng (Buying)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ┌─ Yêu cầu & Đặt hàng ─┐      ┌─ Nhận hàng ─┐      ┌─ Thanh toán ─┐      │
│   │                      │      │             │      │              │      │
│   │  ┌──────────────┐    │      │ ┌─────────┐ │      │ ┌──────────┐ │      │
│   │  │     📋       │────┼──────┼▶│   📦    │─┼──────┼▶│    💳    │ │      │
│   │  │  Yêu cầu     │    │      │ │  Nhận   │ │      │ │  Thanh   │ │      │
│   │  │  & Đặt hàng  │    │      │ │  hàng   │ │      │ │  toán    │ │      │
│   │  └──────┬───────┘    │      │ └────┬────┘ │      │ └────┬─────┘ │      │
│   │         │            │      │      │      │      │      │       │      │
│   └─────────┼────────────┘      └──────┼──────┘      └──────┼───────┘      │
│             │ hover                    │                    │              │
│             ▼                          │                    │              │
│   ┌──────────────────┐                 │                    │              │
│   │ • Material Req   │                 │                    │              │
│   │ • RFQ            │                 │                    │              │
│   │ • Supplier Quot  │                 │                    │              │
│   │ • Purchase Order │                 │                    │              │
│   └──────────────────┘                 │                    │              │
│                                        │                    │              │
│            ┌───────────────────────────┘                    │              │
│            ▼                                                │              │
│   ┌────────────────────┐                                    │              │
│   │ • Purchase Receipt │                   ┌────────────────┘              │
│   │ • Landed Cost      │                   ▼                               │
│   │ • Purchase Return  │          ┌────────────────┐                       │
│   └────────────────────┘          │ • Purch Invoice│                       │
│                                   │ • Payment Entry│                       │
│                                   │ • Payment Terms│                       │
│                                   └────────────────┘                       │
│                                                                             │
│   ┌─ Nhà cung cấp ──────────────────────────────────────────────────────┐  │
│   │                                                                      │  │
│   │  ┌──────────────┐                                                    │  │
│   │  │     👥       │                                                    │  │
│   │  │  Nhà CC      │                                                    │  │
│   │  └──────┬───────┘                                                    │  │
│   │         │ • Supplier         • Supplier Group                        │  │
│   │         │ • Price List       • Contact                               │  │
│   └─────────┴────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Tồn kho (Stock) - Complex Branching

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│              ┌─ Yêu cầu ─────────────────────────────────────┐              │
│              │                                               │              │
│              │       ┌──────────────┐                        │              │
│              │       │     📝       │                        │              │
│              │       │   Yêu cầu    │                        │              │
│              │       └──────┬───────┘                        │              │
│              │              │                                │              │
│              └──────────────┼────────────────────────────────┘              │
│                             │                                               │
│              ┌──────────────┼──────────────┐                                │
│              │              │              │                                │
│              ▼              ▼              ▼                                │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│   │     🛒       │  │     📦       │  │     📋       │                     │
│   │  Đơn mua     │  │  Điều chuyển │  │  Đơn bán     │                     │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                     │
│          │                 │                 │                              │
│          ▼                 ▼                 ▼                              │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│   │     📥       │  │     🔄       │  │     📤       │                     │
│   │  Nhập kho    │  │  Stock Entry │  │  Xuất kho    │                     │
│   └──────┬───────┘  └──────────────┘  └──────┬───────┘                     │
│          │                                   │                              │
│          └───────────────┬───────────────────┘                              │
│                          ▼                                                  │
│                   ┌──────────────┐                                          │
│                   │     📊       │                                          │
│                   │  Kiểm kê     │                                          │
│                   └──────────────┘                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.3 Kế toán Tiền (Cash) - Tree Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                                                                             │
│                          ┌──────────────┐                                   │
│              ┌───────────│     💰       │───────────┐                       │
│              │           │  Tiền mặt    │           │                       │
│              │           │  & Ngân hàng │           │                       │
│              │           └──────────────┘           │                       │
│              │                                      │                       │
│              ▼                                      ▼                       │
│   ┌──────────────────┐                   ┌──────────────────┐               │
│   │       📥         │                   │       📤         │               │
│   │    Thu tiền      │                   │    Chi tiền      │               │
│   └────────┬─────────┘                   └────────┬─────────┘               │
│            │                                      │                         │
│            ▼                                      ▼                         │
│   ┌────────────────────┐              ┌────────────────────┐                │
│   │ • Thu tiền mặt     │              │ • Chi tiền mặt     │                │
│   │ • Thu chuyển khoản │              │ • Chi chuyển khoản │                │
│   │ • Thu từ KH        │              │ • Chi cho NCC      │                │
│   │ • Thu khác         │              │ • Chi khác         │                │
│   └────────────────────┘              └────────────────────┘                │
│                                                                             │
│                          ┌──────────────┐                                   │
│                          │     🏦       │                                   │
│                          │  Đối chiếu   │                                   │
│                          │  Ngân hàng   │                                   │
│                          └──────────────┘                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.4 Trade-in - Vertical Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ┌──────────────┐                                                          │
│   │     🏷️       │  KH mang gậy cũ                                         │
│   │  Tiếp nhận   │                                                          │
│   └──────┬───────┘                                                          │
│          │                                                                  │
│          ▼                                                                  │
│   ┌──────────────┐                                                          │
│   │     🔍       │  Kiểm tra tình trạng: Scratches, Shaft, Grip, Head      │
│   │  Kiểm tra    │                                                          │
│   └──────┬───────┘                                                          │
│          │                                                                  │
│          ▼                                                                  │
│   ┌──────────────┐                                                          │
│   │     💵       │  Đề xuất giá thu mua                                     │
│   │  Định giá    │                                                          │
│   └──────┬───────┘                                                          │
│          │                                                                  │
│          ▼                                                                  │
│   ┌──────────────┐                                                          │
│   │     ✅       │  Manager duyệt giá                                       │
│   │  Duyệt       │                                                          │
│   └──────┬───────┘                                                          │
│          │                                                                  │
│    ┌─────┴─────┐                                                            │
│    │           │                                                            │
│    ▼           ▼                                                            │
│ ┌──────┐   ┌──────┐                                                         │
│ │  📥  │   │  📤  │                                                         │
│ │ Nhập │   │ Xuất │  Nhập cũ / Xuất mới                                     │
│ │ cũ   │   │ mới  │                                                         │
│ └──┬───┘   └──┬───┘                                                         │
│    │          │                                                             │
│    └────┬─────┘                                                             │
│         ▼                                                                   │
│   ┌──────────────┐                                                          │
│   │     🎉       │  Hoàn thành Trade-in                                     │
│   │  Hoàn thành  │                                                          │
│   └──────────────┘                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. So sánh Layout Options

| Tiêu chí | Manual (sequence/row) | Grid-based Rank | Dagre.js |
|----------|----------------------|-----------------|----------|
| **Dependencies** | Không | Không | dagre (16KB gzip) |
| **Cấu hình** | Nhiều fields | Chỉ `connects_to` | Chỉ `connects_to` |
| **Tự động cân đối** | ❌ | ✅ Cơ bản | ✅ Tối ưu |
| **Edge crossing** | Thủ công | Không xử lý | ✅ Minimize |
| **Complex graphs** | Khó | OK | ✅ Tốt |
| **Maintenance** | Cao | Thấp | Thấp |
| **Recommend** | ❌ | ✅ MVP | ✅ Production |

**Đề xuất:**
1. **MVP:** Dùng Grid-based Rank (không dependency)
2. **Production:** Upgrade lên Dagre.js

---

## 11. Roadmap triển khai

| Phase | Công việc | Thời gian |
|-------|-----------|-----------|
| **1. Backend** | Custom Fields (simplified) + API | 2 ngày |
| **2. Frontend** | Grid-based layout + SVG rendering | 3 ngày |
| **3. Dropdown** | Hover menu + navigation | 1 ngày |
| **4. Integration** | hooks + workspace injection | 1 ngày |
| **5. Config** | Workflow config cho 11 workspaces | 2 ngày |
| **6. Upgrade** | Dagre.js + edge optimization | 2 ngày |
| **7. Polish** | Dark mode, responsive, animations | 1-2 ngày |

**Tổng:** ~12-14 ngày

---

## 12. Simplified Custom Fields (Revised)

Với auto-layout, chỉ cần **4 fields** thay vì 7:

```json
{
  "custom_fields": [
    {
      "fieldname": "is_workflow_node",
      "fieldtype": "Check",
      "label": "Is Workflow Node",
      "description": "Hiển thị item này như một node trong workflow diagram"
    },
    {
      "fieldname": "workflow_connects_to",
      "fieldtype": "Small Text",
      "label": "Connects To",
      "description": "JSON array: [\"Nhận hàng\", \"Thanh toán\"]"
    },
    {
      "fieldname": "workflow_color",
      "fieldtype": "Select",
      "label": "Color",
      "options": "auto\nred\norange\ngreen\nblue\npurple",
      "default": "auto"
    },
    {
      "fieldname": "workflow_group",
      "fieldtype": "Data",
      "label": "Group",
      "description": "Nhóm để gom các nodes liên quan"
    }
  ]
}
```

**Bỏ:** `workflow_sequence`, `workflow_row`, `workflow_icon_style` (tự động tính)

---

## 13. Implementation Priority

```
Week 1:
├── Day 1-2: Backend (Custom Fields + API)
├── Day 3-5: Frontend (SVG + Grid Layout)
└── Day 5: Integration + Basic dropdown

Week 2:
├── Day 1-2: Config 11 workspaces
├── Day 3-4: Dagre upgrade + optimization
└── Day 5: Polish + dark mode
```

---

## 9. Lưu ý kỹ thuật

1. **Performance:** Lazy-load workflow diagram, cache config
2. **Responsive:** Scale SVG on mobile, horizontal scroll
3. **Accessibility:** Keyboard navigation, ARIA labels
4. **Dark mode:** CSS variables hoặc data-theme attribute
5. **i18n:** Label translation qua `__()` function
6. **Permissions:** Check user roles before showing actions
7. **Custom blocks:** Sử dụng Shadow DOM để isolate CSS

---

**Tác giả:** Nguyễn Hoàng Long
**Review:** Cần review từ team trước khi triển khai
