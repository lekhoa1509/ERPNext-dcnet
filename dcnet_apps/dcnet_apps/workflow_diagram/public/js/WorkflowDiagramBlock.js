/**
 * WorkflowDiagramBlock
 *
 * Custom EditorJS Block dùng để render sơ đồ quy trình nghiệp vụ tương tác
 * dựa trên cấu hình Workspace Sidebar.
 *
 * Các tính năng chính:
 * - Tự động sắp xếp (Auto-layout) sử dụng thuật toán Grid-based Rank (không phụ thuộc thư viện ngoài)
 * - Menu dropdown tương tác khi hover để hiển thị các hành động con
 * - Render bằng SVG với các đường nối mượt mà
 * - Phân nhóm (Clustering) các node với hộp nền (background box)
 * - Hỗ trợ chế độ tối (Dark mode)
 */

frappe.provide("dcnet.workflow_diagram");

dcnet.workflow_diagram.WorkflowDiagramBlock = class WorkflowDiagramBlock {
    // Định nghĩa thông tin hiển thị trong toolbox của EditorJS
    static get toolbox() {
        return {
            title: "Workflow Diagram",
            icon: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>'
        };
    }

    constructor({ data, api, config, readOnly }) {
        this.api = api;
        this.config = config;
        this.readOnly = readOnly;
        // Khởi tạo dữ liệu block
        this.data = {
            workspace: data.workspace || "",
            showTitle: data.showTitle !== false,
            compact: data.compact || false
        };
        this.wrapper = null;
        this.workflowData = null;

        // Các hằng số định nghĩa kích thước layout
        this.NODE_WIDTH = 120;  // Chiều rộng của một node
        this.NODE_HEIGHT = 80;  // Chiều cao của một node
        this.GAP_X = 60;        // Khoảng cách ngang giữa các node
        this.GAP_Y = 40;        // Khoảng cách dọc giữa các node
        this.PADDING = 40;      // Padding bao quanh sơ đồ

        // Bảng màu sắc cho các loại node khác nhau
        this.COLORS = {
            auto: { bg: "#e0f2fe", border: "#0284c7", text: "#0c4a6e" },
            blue: { bg: "#dbeafe", border: "#2563eb", text: "#1e40af" },
            green: { bg: "#dcfce7", border: "#16a34a", text: "#166534" },
            orange: { bg: "#ffedd5", border: "#ea580c", text: "#9a3412" },
            red: { bg: "#fee2e2", border: "#dc2626", text: "#991b1b" },
            purple: { bg: "#f3e8ff", border: "#9333ea", text: "#6b21a8" }
        };
    }

    /**
     * Hàm render chính của block EditorJS
     */
    render() {
        this.wrapper = document.createElement("div");
        this.wrapper.classList.add("workflow-diagram-block");

        // Nếu đã chọn workspace thì tải dữ liệu, ngược lại hiện placeholder
        if (this.data.workspace) {
            this.loadWorkflowData();
        } else {
            this.renderPlaceholder();
        }

        return this.wrapper;
    }

    /**
     * Hiển thị trạng thái chờ cấu hình khi chưa chọn Workspace
     */
    renderPlaceholder() {
        this.wrapper.innerHTML = `
            <div class="workflow-placeholder">
                <p>Workflow Diagram</p>
                <small>Cấu hình workspace trong phần cài đặt block</small>
            </div>
        `;
    }

    /**
     * Tải dữ liệu workflow từ backend API của Frappe
     */
    async loadWorkflowData() {
        this.wrapper.innerHTML = '<div class="workflow-loading">Đang tải quy trình...</div>';

        try {
            const response = await frappe.call({
                method: "dcnet_apps.workflow_diagram.api.get_workflow_config",
                args: { workspace_name: this.data.workspace }
            });

            this.workflowData = response.message;
            this.renderDiagram();
        } catch (error) {
            console.error("Lỗi tải workflow:", error);
            this.wrapper.innerHTML = `
                <div class="workflow-error">
                    Không thể tải sơ đồ quy trình cho "${this.data.workspace}"
                </div>
            `;
        }
    }

    /**
     * Thực hiện render sơ đồ SVG dựa trên dữ liệu đã tải
     */
    renderDiagram() {
        if (!this.workflowData || this.workflowData.nodes.length === 0) {
            this.wrapper.innerHTML = `
                <div class="workflow-empty">
                    Chưa có cấu hình node workflow cho "${this.data.workspace}"
                </div>
            `;
            return;
        }

        // Tính toán vị trí (X, Y) cho từng node
        const layout = this.calculateLayout(
            this.workflowData.nodes,
            this.workflowData.connections
        );

        // Tính toán kích thước tổng thể của SVG
        const positions = Object.values(layout);
        const maxX = Math.max(...positions.map(p => p.x)) + this.NODE_WIDTH + this.PADDING;
        const maxY = Math.max(...positions.map(p => p.y)) + this.NODE_HEIGHT + this.PADDING;

        // Tạo phần tử SVG
        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("width", maxX);
        svg.setAttribute("height", maxY);
        svg.setAttribute("viewBox", `0 0 ${maxX} ${maxY}`);
        svg.classList.add("workflow-svg");

        // Định nghĩa các marker (ví dụ: mũi tên) trong SVG
        const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
        defs.innerHTML = `
            <marker id="arrowhead" markerWidth="10" markerHeight="7"
                    refX="10" refY="3.5" orient="auto" fill="#94a3b8">
                <polygon points="0 0, 10 3.5, 0 7" />
            </marker>
        `;
        svg.appendChild(defs);

        // Render các hộp nền phân nhóm trước (để nằm dưới các node)
        this.renderGroups(svg, layout, this.workflowData.groups);

        // Render các đường nối (connections)
        this.renderConnections(svg, layout, this.workflowData.connections);

        // Render các node chính
        this.renderNodes(svg, layout, this.workflowData.nodes);

        // Xóa nội dung cũ và chèn sơ đồ mới vào wrapper
        this.wrapper.innerHTML = "";

        if (this.data.showTitle) {
            const title = document.createElement("h3");
            title.className = "workflow-title";
            title.textContent = `Quy trình ${this.data.workspace}`;
            this.wrapper.appendChild(title);
        }

        const container = document.createElement("div");
        container.className = "workflow-container";
        container.appendChild(svg);
        this.wrapper.appendChild(container);
    }

    /**
     * Thuật toán sắp xếp Layout dựa trên Rank (Bậc của node)
     *
     * Các bước thực hiện:
     * 1. Tìm các node gốc (không có cạnh đi vào)
     * 2. Tính toán rank (khoảng cách từ node gốc) bằng thuật toán Duyệt theo chiều rộng (BFS)
     * 3. Xếp các node vào các cột dựa trên rank
     * 4. Căn giữa các node theo chiều dọc trong mỗi cột
     */
    calculateLayout(nodes, connections) {
        // Xây dựng danh sách kề (outgoing) và danh sách kề ngược (incoming)
        const outgoing = {};
        const incoming = {};
        nodes.forEach(n => {
            outgoing[n.id] = [];
            incoming[n.id] = [];
        });

        connections.forEach(c => {
            if (outgoing[c.from]) outgoing[c.from].push(c.to);
            if (incoming[c.to]) incoming[c.to].push(c.from);
        });

        // Tìm các node bắt đầu (không có kết nối đến)
        const startNodes = nodes.filter(n => incoming[n.id].length === 0);

        // Nếu không tìm thấy node gốc, lấy node đầu tiên làm gốc
        if (startNodes.length === 0 && nodes.length > 0) {
            startNodes.push(nodes[0]);
        }

        // Tính rank bằng BFS
        const ranks = {};
        const queue = startNodes.map(n => ({ id: n.id, rank: 0 }));
        const visited = new Set();

        while (queue.length > 0) {
            const { id, rank } = queue.shift();
            if (visited.has(id)) {
                // Cập nhật rank nếu tìm thấy đường đi dài hơn
                ranks[id] = Math.max(ranks[id] || 0, rank);
                continue;
            }
            visited.add(id);
            ranks[id] = rank;

            // Thêm các node kết nối vào hàng đợi
            (outgoing[id] || []).forEach(target => {
                queue.push({ id: target, rank: rank + 1 });
            });
        }

        // Xử lý các node bị rời rạc (không kết nối)
        nodes.forEach(n => {
            if (ranks[n.id] === undefined) {
                ranks[n.id] = 0;
            }
        });

        // Gom nhóm node theo rank (để xếp vào cột)
        const byRank = {};
        Object.entries(ranks).forEach(([id, rank]) => {
            if (!byRank[rank]) byRank[rank] = [];
            byRank[rank].push(id);
        });

        // Tính toán tọa độ thực tế
        const positions = {};
        const maxNodesInRank = Math.max(...Object.values(byRank).map(arr => arr.length));
        const totalHeight = maxNodesInRank * this.NODE_HEIGHT + (maxNodesInRank - 1) * this.GAP_Y + this.PADDING * 2;

        Object.entries(byRank).forEach(([rank, ids]) => {
            const x = parseInt(rank) * (this.NODE_WIDTH + this.GAP_X) + this.PADDING;
            const columnHeight = ids.length * this.NODE_HEIGHT + (ids.length - 1) * this.GAP_Y;
            const startY = (totalHeight - columnHeight) / 2;

            ids.forEach((id, index) => {
                positions[id] = {
                    x: x,
                    y: startY + index * (this.NODE_HEIGHT + this.GAP_Y)
                };
            });
        });

        return positions;
    }

    /**
     * Render các hộp nền đại diện cho các nhóm node (Clusters)
     */
    renderGroups(svg, positions, groups) {
        groups.forEach((group, index) => {
            const groupNodes = group.nodes
                .filter(id => positions[id])
                .map(id => positions[id]);

            if (groupNodes.length === 0) return;

            const padding = 15;
            const minX = Math.min(...groupNodes.map(p => p.x)) - padding;
            const minY = Math.min(...groupNodes.map(p => p.y)) - padding - 20; // Chừa chỗ cho nhãn nhóm
            const maxX = Math.max(...groupNodes.map(p => p.x + this.NODE_WIDTH)) + padding;
            const maxY = Math.max(...groupNodes.map(p => p.y + this.NODE_HEIGHT)) + padding;

            // Hình chữ nhật nền của nhóm
            const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            rect.setAttribute("x", minX);
            rect.setAttribute("y", minY);
            rect.setAttribute("width", maxX - minX);
            rect.setAttribute("height", maxY - minY);
            rect.setAttribute("fill", "var(--workflow-group-bg, #f8fafc)");
            rect.setAttribute("stroke", "var(--workflow-group-border, #e2e8f0)");
            rect.setAttribute("stroke-width", "1");
            rect.setAttribute("rx", "8");
            rect.classList.add("workflow-group-rect");
            svg.appendChild(rect);

            // Nhãn tên nhóm
            const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
            label.setAttribute("x", minX + 10);
            label.setAttribute("y", minY + 14);
            label.setAttribute("fill", "var(--workflow-group-text, #64748b)");
            label.setAttribute("font-size", "11");
            label.setAttribute("font-weight", "500");
            label.textContent = group.name;
            label.classList.add("workflow-group-label");
            svg.appendChild(label);
        });
    }

    /**
     * Render các đường nối giữa các node bằng đường cong Bezier
     */
    renderConnections(svg, positions, connections) {
        connections.forEach(conn => {
            const fromPos = positions[conn.from];
            const toPos = positions[conn.to];

            if (!fromPos || !toPos) return;

            // Điểm bắt đầu và kết thúc của đường nối
            const startX = fromPos.x + this.NODE_WIDTH;
            const startY = fromPos.y + this.NODE_HEIGHT / 2;
            const endX = toPos.x;
            const endY = toPos.y + this.NODE_HEIGHT / 2;

            // Tạo đường dẫn (path) sử dụng đường cong Bezier bậc 3
            const midX = (startX + endX) / 2;
            const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path.setAttribute("d", `M ${startX} ${startY} C ${midX} ${startY}, ${midX} ${endY}, ${endX} ${endY}`);
            path.setAttribute("stroke", "var(--workflow-edge-color, #94a3b8)");
            path.setAttribute("stroke-width", "2");
            path.setAttribute("fill", "none");
            path.setAttribute("marker-end", "url(#arrowhead)");
            path.classList.add("workflow-edge");
            svg.appendChild(path);
        });
    }

    /**
     * Render từng node riêng lẻ trong sơ đồ
     */
    renderNodes(svg, positions, nodes) {
        nodes.forEach(node => {
            const pos = positions[node.id];
            if (!pos) return;

            const colors = this.COLORS[node.color] || this.COLORS.auto;

            // Tạo group SVG cho node
            const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
            g.setAttribute("transform", `translate(${pos.x}, ${pos.y})`);
            g.classList.add("workflow-node");
            g.dataset.nodeId = node.id;

            // Hình chữ nhật đại diện cho node
            const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            rect.setAttribute("width", this.NODE_WIDTH);
            rect.setAttribute("height", this.NODE_HEIGHT);
            rect.setAttribute("rx", "8");
            rect.setAttribute("fill", colors.bg);
            rect.setAttribute("stroke", colors.border);
            rect.setAttribute("stroke-width", "2");
            rect.classList.add("workflow-node-rect");
            g.appendChild(rect);

            // Icon (hiển thị bằng Emoji tương ứng với tên icon)
            const iconText = document.createElementNS("http://www.w3.org/2000/svg", "text");
            iconText.setAttribute("x", this.NODE_WIDTH / 2);
            iconText.setAttribute("y", 30);
            iconText.setAttribute("text-anchor", "middle");
            iconText.setAttribute("font-size", "20");
            iconText.textContent = this.getIconEmoji(node.icon);
            g.appendChild(iconText);

            // Nhãn tên node (cắt ngắn nếu quá dài)
            const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
            label.setAttribute("x", this.NODE_WIDTH / 2);
            label.setAttribute("y", 55);
            label.setAttribute("text-anchor", "middle");
            label.setAttribute("fill", colors.text);
            label.setAttribute("font-size", "12");
            label.setAttribute("font-weight", "500");
            label.textContent = this.truncateLabel(node.label, 14);
            g.appendChild(label);

            // Thêm tương tác hover để hiển thị dropdown hành động
            if (node.actions && node.actions.length > 0) {
                this.addDropdownInteraction(g, node, pos);
            }

            svg.appendChild(g);
        });
    }

    /**
     * Xử lý hiển thị menu dropdown khi người dùng hover chuột vào node
     */
    addDropdownInteraction(nodeGroup, node, pos) {
        // Tạo container cho dropdown (ẩn mặc định)
        const dropdown = document.createElement("div");
        dropdown.className = "workflow-dropdown";
        dropdown.style.display = "none";

        // Xây dựng nội dung HTML cho dropdown
        let html = `<div class="workflow-dropdown-header">${node.label}</div>`;
        html += '<ul class="workflow-dropdown-list">';
        node.actions.forEach(action => {
            const url = this.getActionUrl(action);
            html += `
                <li class="workflow-dropdown-item">
                    <a href="${url}" class="workflow-dropdown-link">
                        ${action.label}
                    </a>
                </li>
            `;
        });
        html += "</ul>";
        dropdown.innerHTML = html;

        // Thêm dropdown vào wrapper (dropdown là HTML thuần, không phải SVG)
        this.wrapper.appendChild(dropdown);

        // Định vị và hiển thị dropdown khi hover
        nodeGroup.addEventListener("mouseenter", () => {
            dropdown.style.display = "block";
            dropdown.style.position = "absolute";
            dropdown.style.left = `${pos.x + this.NODE_WIDTH / 2 - 80}px`;
            dropdown.style.top = `${pos.y + this.NODE_HEIGHT + 5}px`;
        });

        nodeGroup.addEventListener("mouseleave", (e) => {
            // Độ trễ nhỏ để người dùng có thể di chuyển chuột sang menu dropdown
            setTimeout(() => {
                if (!dropdown.matches(":hover")) {
                    dropdown.style.display = "none";
                }
            }, 100);
        });

        // Ẩn dropdown khi chuột rời khỏi menu
        dropdown.addEventListener("mouseleave", () => {
            dropdown.style.display = "none";
        });
    }

    /**
     * Xác định URL điều hướng cho từng hành động dựa trên cấu hình link_type
     */
    getActionUrl(action) {
        if (action.url) return action.url;
        if (action.link_type === "DocType" && action.link_to) {
            return `/app/${frappe.router.slug(action.link_to)}`;
        }
        if (action.link_type === "Report" && action.link_to) {
            return `/app/query-report/${action.link_to}`;
        }
        if (action.link_type === "Page" && action.link_to) {
            return `/app/${action.link_to}`;
        }
        return "#";
    }

    /**
     * Bản đồ chuyển đổi từ tên icon (Lucide/Feather) sang Emoji tương ứng
     */
    getIconEmoji(iconName) {
        const iconMap = {
            "clipboard-list": "📋",
            "package": "📦",
            "credit-card": "💳",
            "users": "👥",
            "shopping-cart": "🛒",
            "truck": "🚚",
            "file-text": "📄",
            "dollar-sign": "💰",
            "wallet": "👛",
            "receipt": "🧾",
            "building": "🏢",
            "settings": "⚙️",
            "bar-chart": "📊",
            "target": "🎯",
            "tag": "🏷️",
            "search": "🔍",
            "check-circle": "✅",
            "plus-circle": "➕",
            "refresh-cw": "🔄",
            "home": "🏠",
            "store": "🏪",
            "award": "🏆",
            "headphones": "🎧",
            "database": "💾",
            "plug": "🔌",
            "shopping-bag": "🛍️",
            "circle": "⭕"
        };
        return iconMap[iconName] || "📌";
    }

    /**
     * Cắt ngắn nhãn văn bản nếu vượt quá độ dài tối đa cho phép
     */
    truncateLabel(text, maxLen) {
        if (!text) return "";
        if (text.length <= maxLen) return text;
        return text.substring(0, maxLen - 1) + "…";
    }

    /**
     * Lưu dữ liệu cấu hình block (EditorJS API)
     */
    save() {
        return this.data;
    }

    /**
     * Kiểm tra tính hợp lệ của dữ liệu trước khi lưu
     */
    validate(savedData) {
        return !!savedData.workspace;
    }

    /**
     * Render giao diện cài đặt của block (EditorJS API)
     */
    renderSettings() {
        const settingsContainer = document.createElement("div");

        // Bộ chọn Workspace (Workspace Selector)
        const workspaceLabel = document.createElement("label");
        workspaceLabel.textContent = "Workspace:";
        workspaceLabel.style.display = "block";
        workspaceLabel.style.marginBottom = "5px";

        const workspaceSelect = document.createElement("select");
        workspaceSelect.style.width = "100%";
        workspaceSelect.style.marginBottom = "10px";

        const workspaces = [
            "", "Mua hàng", "Bán hàng", "Tồn kho", "Sản phẩm",
            "Trade-in", "Fitting", "Coaching", "Khách hàng & CRM",
            "Kế toán", "Nhân sự & Chi nhánh", "Tích hợp"
        ];

        workspaces.forEach(ws => {
            const option = document.createElement("option");
            option.value = ws;
            option.textContent = ws || "-- Chọn Workspace --";
            option.selected = ws === this.data.workspace;
            workspaceSelect.appendChild(option);
        });

        workspaceSelect.addEventListener("change", () => {
            this.data.workspace = workspaceSelect.value;
            if (this.data.workspace) {
                this.loadWorkflowData();
            } else {
                this.renderPlaceholder();
            }
        });

        // Checkbox hiển thị/ẩn tiêu đề
        const showTitleLabel = document.createElement("label");
        showTitleLabel.style.display = "flex";
        showTitleLabel.style.alignItems = "center";
        showTitleLabel.style.marginBottom = "10px";

        const showTitleCheckbox = document.createElement("input");
        showTitleCheckbox.type = "checkbox";
        showTitleCheckbox.checked = this.data.showTitle;
        showTitleCheckbox.style.marginRight = "8px";
        showTitleCheckbox.addEventListener("change", () => {
            this.data.showTitle = showTitleCheckbox.checked;
            if (this.workflowData) this.renderDiagram();
        });

        showTitleLabel.appendChild(showTitleCheckbox);
        showTitleLabel.appendChild(document.createTextNode("Hiển thị tiêu đề"));

        settingsContainer.appendChild(workspaceLabel);
        settingsContainer.appendChild(workspaceSelect);
        settingsContainer.appendChild(showTitleLabel);

        return settingsContainer;
    }
};

/**
 * Đăng ký Web Component <workflow-diagram> để có thể sử dụng ở bất kỳ đâu trong ứng dụng
 */
if (typeof customElements !== "undefined" && !customElements.get("workflow-diagram")) {
    class WorkflowDiagramElement extends HTMLElement {
        connectedCallback() {
            const workspace = this.getAttribute("workspace");
            if (workspace) {
                this.renderDiagram(workspace);
            }
        }

        async renderDiagram(workspace) {
            try {
                const response = await frappe.call({
                    method: "dcnet_apps.workflow_diagram.api.get_workflow_config",
                    args: { workspace_name: workspace }
                });

                const block = new dcnet.workflow_diagram.WorkflowDiagramBlock({
                    data: { workspace, showTitle: true },
                    readOnly: true
                });

                block.workflowData = response.message;
                const rendered = block.render();
                block.renderDiagram();
                this.appendChild(rendered);
            } catch (error) {
                console.error("Không thể render sơ đồ quy trình:", error);
                this.innerHTML = `<div class="workflow-error">Lỗi tải quy trình</div>`;
            }
        }
    }

    customElements.define("workflow-diagram", WorkflowDiagramElement);
}
