"""
Workflow Diagram API

Cung cấp các endpoint để lấy cấu hình quy trình (workflow) từ các file JSON của Workspace Sidebar.
Được sử dụng bởi component frontend WorkflowDiagramBlock và script tự động render.
"""

import json
import os
import frappe


@frappe.whitelist(allow_guest=False)
def get_workflow_config(workspace_name: str) -> dict:
    """
    Lấy cấu hình sơ đồ quy trình từ JSON sidebar của workspace.

    Args:
        workspace_name: Tên của workspace (ví dụ: "Mua hàng", "Tồn kho")

    Returns:
        dict chứa danh sách các node, connections và groups cho sơ đồ quy trình
    """
    sidebar_config = get_sidebar_config(workspace_name)
    if not sidebar_config:
        return {"nodes": [], "connections": [], "groups": []}

    return parse_workflow_from_sidebar(sidebar_config)


def get_sidebar_config(workspace_name: str) -> dict | None:
    """
    Tải cấu hình sidebar từ database hoặc từ file JSON.

    Đầu tiên thử tải từ DocType 'Workspace Sidebar',
    nếu không có sẽ tìm trong các file JSON trong thư mục workspace_sidebar.
    """
    # Thử lấy từ database trước
    try:
        sidebar = frappe.get_doc("Workspace Sidebar", workspace_name)
        return sidebar.as_dict()
    except frappe.DoesNotExistError:
        pass

    # Nếu không có trong DB, tìm trong thư mục JSON
    app_path = frappe.get_app_path("dcnet_apps")
    sidebar_folder = os.path.join(app_path, "workspace_sidebar")

    # Bản đồ ánh xạ tên workspace sang tên file JSON tương ứng
    name_to_file = {
        "Buying": "buying.json",
        "Selling": "selling.json",
        "Stock": "stock.json",
        "Products": "products.json",
        "Trade-in": "trade_in.json",
        "Fitting": "fitting.json",
        "Coaching": "coaching.json",
        "CRM": "crm.json",
        "Accounts": "accounts.json",
        "HR": "hr.json",
        "E-Invoice": "integrations.json",
    }

    filename = name_to_file.get(workspace_name)
    if not filename:
        # Nếu không có trong bản đồ ánh xạ, duyệt qua tất cả file JSON để tìm theo trường 'title'
        for file in os.listdir(sidebar_folder):
            if file.endswith(".json"):
                filepath = os.path.join(sidebar_folder, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    if config.get("title") == workspace_name or config.get("name") == workspace_name:
                        return config
        return None

    filepath = os.path.join(sidebar_folder, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    return None


def parse_workflow_from_sidebar(sidebar_config: dict) -> dict:
    """
    Phân tích cấu hình sidebar để trích xuất các node và kết nối của quy trình.

    Các node quy trình là các item loại 'Section Break' có đánh dấu is_workflow_node=1.
    Các item con nằm dưới Section Break đó sẽ trở thành các hành động trong menu dropdown của node.
    """
    items = sidebar_config.get("items", [])

    nodes = []
    connections = []
    groups = {}

    current_section = None
    current_children = []

    for item in items:
        item_type = item.get("type", "Link")

        if item_type == "Section Break":
            # Save previous section if it was a workflow node
            # Kiểm tra cả giá trị integer 1 hoặc string "1"
            if current_section and (current_section.get("is_workflow_node") == 1 or current_section.get("is_workflow_node") == "1"):
                node = create_node_from_section(current_section, current_children)
                nodes.append(node)

                # Phân tích các kết nối (connections) của node này
                connects_to = current_section.get("workflow_connects_to", "")
                if connects_to:
                    try:
                        targets = json.loads(connects_to) if isinstance(connects_to, str) else connects_to
                        if isinstance(targets, list):
                            for target in targets:
                                connections.append({
                                    "from": current_section.get("label"),
                                    "to": target
                                })
                    except (json.JSONDecodeError, TypeError):
                        pass

                # Phân loại vào nhóm quy trình (workflow group)
                group = current_section.get("workflow_group")
                if group:
                    if group not in groups:
                        groups[group] = {
                            "name": group,
                            "nodes": []
                        }
                    groups[group]["nodes"].append(current_section.get("label"))

            # Bắt đầu một section mới
            current_section = item
            current_children = []

        elif item_type == "Link" and item.get("child"):
            # Đây là một item con thuộc về section hiện tại
            current_children.append({
                "label": item.get("label"),
                "link_to": item.get("link_to"),
                "link_type": item.get("link_type", "DocType"),
                "url": item.get("url"),
                "icon": item.get("icon")
            })

    # Xử lý section cuối cùng trong danh sách
    if current_section and (current_section.get("is_workflow_node") == 1 or current_section.get("is_workflow_node") == "1"):
        node = create_node_from_section(current_section, current_children)
        nodes.append(node)

        connects_to = current_section.get("workflow_connects_to", "")
        if connects_to:
            try:
                targets = json.loads(connects_to) if isinstance(connects_to, str) else connects_to
                if isinstance(targets, list):
                    for target in targets:
                        connections.append({
                            "from": current_section.get("label"),
                            "to": target
                        })
            except (json.JSONDecodeError, TypeError):
                pass

        group = current_section.get("workflow_group")
        if group:
            if group not in groups:
                groups[group] = {
                    "name": group,
                    "nodes": []
                }
            groups[group]["nodes"].append(current_section.get("label"))

    return {
        "nodes": nodes,
        "connections": connections,
        "groups": list(groups.values())
    }


def create_node_from_section(section: dict, children: list) -> dict:
    """Tạo đối tượng node quy trình từ một section sidebar."""
    return {
        "id": section.get("label"),
        "label": section.get("label"),
        "icon": section.get("icon", "circle"),
        "color": section.get("workflow_color", "auto"),
        "group": section.get("workflow_group"),
        "lane": section.get("custom_lane") or section.get("lane") or "Main",
        "actions": children
    }


@frappe.whitelist(allow_guest=False)
def get_all_workflow_configs() -> dict:
    """
    Lấy toàn bộ cấu hình quy trình cho tất cả các workspace.

    Returns:
        dict ánh xạ tên workspace sang cấu hình quy trình tương ứng
    """
    app_path = frappe.get_app_path("dcnet_apps")
    sidebar_folder = os.path.join(app_path, "workspace_sidebar")

    configs = {}

    if os.path.exists(sidebar_folder):
        for filename in os.listdir(sidebar_folder):
            if filename.endswith(".json"):
                filepath = os.path.join(sidebar_folder, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    sidebar_config = json.load(f)
                    workspace_name = sidebar_config.get("title") or sidebar_config.get("name")
                    if workspace_name:
                        configs[workspace_name] = parse_workflow_from_sidebar(sidebar_config)

    return configs
