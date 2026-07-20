/**
 * Tự động render sơ đồ quy trình nghiệp vụ cho các Workspace
 * 
 * Script này tự động phát hiện trang Workspace và render sơ đồ dựa trên 
 * cấu hình các node workflow trong Sidebar (Workspace Sidebar).
 */

frappe.provide('dcnet.workflow_diagram');

dcnet.workflow_diagram = {
    // Cache lưu trữ cấu hình workflow để tránh gọi API nhiều lần
    cache: {},
    rendered_for: null,
    observer: null,

    /**
     * Khởi tạo script, lắng nghe các sự kiện thay đổi trang của Frappe
     */
    init: function() {
        const self = this;

        // Lắng nghe sự kiện chuyển trang trong Frappe Desk
        $(document).on('page-change', function() {
            setTimeout(() => self.check_and_render(), 300);
        });

        // Kiểm tra render ngay khi trang web sẵn sàng
        $(document).ready(function() {
            setTimeout(() => self.check_and_render(), 500);
        });

        // Thiết lập observer để theo dõi khi container của workspace xuất hiện trong DOM
        self.setup_observer();

        // Thử render lại sau khi các yêu cầu AJAX của Frappe hoàn tất
        if (frappe.after_ajax) {
            frappe.after_ajax(() => {
                setTimeout(() => self.check_and_render(), 500);
            });
        }

        // Cơ chế fallback: kiểm tra định kỳ trong 10 giây đầu sau khi load trang
        let attempts = 0;
        const pollInterval = setInterval(() => {
            attempts++;
            self.check_and_render();
            if (attempts >= 20) {
                clearInterval(pollInterval);
            }
        }, 500);
    },

    /**
     * Sử dụng MutationObserver để phát hiện khi nội dung Workspace được render động
     */
    setup_observer: function() {
        const self = this;

        this.observer = new MutationObserver(function(mutations) {
            const container = document.querySelector('#editorjs');
            // Nếu tìm thấy container workspace mà chưa có sơ đồ thì tiến hành render
            if (container && !container.querySelector('.wf-auto-diagram')) {
                self.check_and_render();
            }
        });

        this.observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    },

    /**
     * Kiểm tra điều kiện và thực hiện render sơ đồ
     */
    check_and_render: function() {
        // Lấy tên workspace hiện tại từ URL hoặc state của Frappe
        let workspace_name = this.get_workspace_name();

        if (!workspace_name) {
            return;
        }

        // Tránh render lại nếu đã render cho workspace này rồi
        if (this.rendered_for === workspace_name) {
            if (document.querySelector('.wf-auto-diagram')) {
                return;
            }
        }

        this.render_for_workspace(workspace_name);
    },

    /**
     * Xác định tên Workspace hiện tại thông qua nhiều phương thức (URL, DOM, Frappe state)
     */
    get_workspace_name: function() {
        // Cách 1: Kiểm tra trong đối tượng workspace của Frappe
        if (frappe.workspace && frappe.workspace._page) {
            const page = frappe.workspace._page;
            return page.name || page.title;
        }

        // Cách 2: Phân tích từ lộ trình (route) trên URL
        const route = frappe.get_route();
        if (route && route.length >= 1) {
            if (route[0] === 'Workspaces' && route[1]) {
                return route[1];
            }
            const workspaces = ['Buying', 'Selling', 'Stock', 'Accounts', 'CRM', 'HR', 'Manufacturing', 'Projects'];
            const routeName = route[0];
            const normalized = routeName.charAt(0).toUpperCase() + routeName.slice(1).toLowerCase();
            if (workspaces.includes(normalized)) {
                return normalized;
            }
        }

        // Cách 3: Kiểm tra phần tử Sidebar đang được chọn
        const workspaceContainer = document.querySelector('.layout-main-section');
        if (workspaceContainer) {
            const activeLink = document.querySelector('.sidebar-menu .desk-sidebar-item.selected');
            if (activeLink) {
                return activeLink.getAttribute('data-page-name') || activeLink.textContent.trim();
            }
        }

        return null;
    },

    /**
     * Gọi API backend để lấy cấu hình workflow và render
     */
    render_for_workspace: function(workspace_name) {
        const self = this;

        // Ưu tiên lấy từ cache
        if (this.cache[workspace_name]) {
            this.inject_diagram(workspace_name, this.cache[workspace_name]);
            return;
        }

        // Gọi hàm Python backend để lấy dữ liệu
        frappe.call({
            method: 'dcnet_apps.workflow_diagram.api.get_workflow_config',
            args: { workspace_name: workspace_name },
            async: true,
            callback: function(r) {
                if (r.message && r.message.nodes && r.message.nodes.length > 0) {
                    self.cache[workspace_name] = r.message;
                    self.inject_diagram(workspace_name, r.message);
                }
            }
        });
    },

    /**
     * Chèn HTML của sơ đồ vào vị trí đầu tiên của nội dung Workspace
     */
    inject_diagram: function(workspace_name, config) {
        let workspace_container = document.querySelector('#editorjs');
        if (!workspace_container) {
            workspace_container = document.querySelector('.editor-js-container');
        }
        if (!workspace_container) {
            workspace_container = document.querySelector('.desk-page.page-main-content');
        }
        if (!workspace_container) {
            workspace_container = document.querySelector('#page-Workspaces .layout-main-section');
        }
        if (!workspace_container) {
            return;
        }

        // Xóa sơ đồ cũ nếu có
        const existing = workspace_container.querySelector('.wf-auto-diagram');
        if (existing) {
            existing.remove();
        }

        // Tạo HTML mới
        const diagram = this.create_diagram_html(workspace_name, config);

        // Chèn vào đầu container (afterbegin)
        workspace_container.insertAdjacentHTML('afterbegin', diagram);

        this.rendered_for = workspace_name;

        // Gán các sự kiện click cho các node
        this.attach_handlers(workspace_name);

        console.log('[WorkflowDiagram] Rendered for', workspace_name);
    },

    /**
     * Tạo cấu trúc HTML cho sơ đồ (Diagram hoặc Standalone Buttons)
     */
    create_diagram_html: function(workspace_name, config) {
        const nodes = config.nodes || [];
        const connections = config.connections || [];
        const groups = config.groups || [];
        
        let groupsHtml = '';

        // Nếu không có nhóm, tạo một nhóm mặc định chứa tất cả các node
        const displayGroups = groups.length > 0 ? groups : [{ name: 'Quy trình', nodes: nodes.map(n => n.id) }];

        displayGroups.forEach((group, groupIdx) => {
            const groupNodeIds = group.nodes || [];
            const groupNodes = nodes.filter(n => groupNodeIds.includes(n.id));
            
            if (groupNodes.length === 0) return;

            let groupContentHtml = '';
            
            // LOGIC: Nếu nhóm có trên 2 node thì mới vẽ Diagram (Fishbone), ngược lại hiện dạng Button
            if (groupNodes.length > 2) {
                // Sắp xếp các node vào các cột dựa trên quan hệ kết nối
                let columns = this.getNodesInColumns(groupNodes, connections);
                
                // Chia các cột thành từng hàng để tránh scroll ngang quá dài
                const maxColumnsPerRow = 10;
                const rows = [];
                for (let i = 0; i < columns.length; i += maxColumnsPerRow) {
                    rows.push(columns.slice(i, i + maxColumnsPerRow));
                }

                rows.forEach((rowColumns, rowIdx) => {
                    let rowHtml = '';
                    let hasTop = false;
                    let hasBottom = false;

                    rowColumns.forEach((columnNodes, colIdx) => {
                        let columnInnerHtml = '';
                        let hasColumnActions = false;

                        columnNodes.forEach((node, nodeIdx) => {
                            // Xác định vị trí của node: Top (trên), Bottom (dưới) hoặc Main (giữa trục)
                            let posClass = 'wf-node-main';
                            if (node.lane === 'Top') {
                                posClass = 'wf-node-top';
                                hasTop = true;
                            } else if (node.lane === 'Bottom') {
                                posClass = 'wf-node-bottom';
                                hasBottom = true;
                            } else if (node.lane === 'Main') {
                                posClass = 'wf-node-main';
                            } else {
                                // Nếu không khai báo lane, tự động phân bổ nếu có nhiều node trong 1 cột
                                if (columnNodes.length === 1) {
                                    posClass = 'wf-node-main';
                                } else {
                                    if (nodeIdx === 0) { posClass = 'wf-node-top'; hasTop = true; }
                                    else if (nodeIdx === 1) { posClass = 'wf-node-bottom'; hasBottom = true; }
                                    else posClass = 'wf-node-main';
                                }
                            }
                            
                            const colorCls = node.color ? `wf-${node.color}` : 'wf-gray';
                            const actions = node.actions || [];
                            const hasActions = actions.length > 0;
                            if (hasActions) hasColumnActions = true;
                            
                            // Tạo link điều hướng cho node
                            let viewHref = '#';
                            if (node.link_to) {
                                if (node.link_type === 'DocType') {
                                    viewHref = `/app/${frappe.router.slug(node.link_to)}`;
                                } else if (node.link_type === 'Report') {
                                    viewHref = `/app/query-report/${encodeURIComponent(node.link_to)}`;
                                }
                            }

                            // Xử lý SVG Icon dựa trên tên icon trong config
                            let icon = node.icon || 'file-search';
                            let iconName = icon;
                            if (icon.startsWith('fa fa-')) {
                                iconName = icon.replace('fa fa-', '');
                            } else if (icon.startsWith('fa-')) {
                                iconName = icon.replace('fa-', '');
                            }

                            let cardContentHtml = `
                                <div class="wf-compact-node" data-href="${viewHref}">
                                    <div class="wf-node-icon">
                                        <svg class="icon text-ink-gray-7 current-color icon-sm" stroke="currentColor" aria-hidden="true">
                                            <use href="#icon-${iconName}"></use>
                                        </svg>
                                        ${hasActions ? this.create_dropdown_html(node) : ''}
                                    </div>
                                    <div class="wf-node-label">${this.escapeHtml(node.label)}</div>
                                </div>
                            `;

                            columnInnerHtml += `
                                <div class="wf-node-card ${posClass} ${colorCls} ${hasActions ? 'has-actions' : ''}" data-node="${this.escapeHtml(node.id)}">
                                    <div class="wf-v-line"></div>
                                    ${cardContentHtml}
                                </div>
                            `;
                        });

                        // Một point trên trục có thể chứa nhiều node (Top/Bottom/Main đối xứng)
                        rowHtml += `
                            <div class="wf-node-point">
                                ${columnInnerHtml}
                            </div>
                        `;
                    });

                    // Render trục ngang (Main Axis) và các node container
                    // Gán class để CSS điều chỉnh chiều cao linh hoạt (auto height)
                    const canvasClasses = ['wf-canvas'];
                    if (hasTop) canvasClasses.push('has-top');
                    if (hasBottom) canvasClasses.push('has-bottom');

                    groupContentHtml += `
                        <div class="${canvasClasses.join(' ')}" data-row="${rowIdx}">
                            <div class="wf-nodes-container">
                                ${rowColumns.length > 1 ? '<div class="wf-main-axis"></div>' : ''}
                                ${rowHtml}
                            </div>
                        </div>
                    `;
                });
            } else {
                // Hiển thị dạng Nút bấm đơn giản cho các nhóm có 1-2 node
                let buttonsHtml = '';
                groupNodes.forEach(node => {
                    const colorCls = node.color ? `wf-${node.color}` : 'wf-gray';
                    const actions = node.actions || [];
                    const hasActions = actions.length > 0;
                    
                    let viewHref = '#';
                    if (node.link_to) {
                        if (node.link_type === 'DocType') {
                            viewHref = `/app/${frappe.router.slug(node.link_to)}`;
                        } else if (node.link_type === 'Report') {
                            viewHref = `/app/query-report/${encodeURIComponent(node.link_to)}`;
                        }
                    }

                    let icon = node.icon || 'file-search';
                    let iconName = icon;
                    if (icon.startsWith('fa fa-')) iconName = icon.replace('fa fa-', '');
                    else if (icon.startsWith('fa-')) iconName = icon.replace('fa-');

                    buttonsHtml += `
                        <div class="wf-standalone-node ${colorCls} ${hasActions ? 'has-actions' : ''}" data-node="${this.escapeHtml(node.id)}">
                            <div class="wf-standalone-btn" data-href="${viewHref}">
                                <div class="wf-node-icon">
                                    <svg class="icon text-ink-gray-7 current-color icon-sm" stroke="currentColor" aria-hidden="true">
                                        <use href="#icon-${iconName}"></use>
                                    </svg>
                                </div>
                                <div class="wf-node-label">${this.escapeHtml(node.label)}</div>
                                ${hasActions ? '<i class="fa fa-chevron-down wf-dropdown-icon"></i>' : ''}
                            </div>
                            ${hasActions ? this.create_dropdown_html(node) : ''}
                        </div>
                    `;
                });
                groupContentHtml = `<div class="wf-buttons-container">${buttonsHtml}</div>`;
            }

            const groupIcon = group.icon ? `<i class="${group.icon.startsWith('fa ') ? group.icon : 'fa fa-' + group.icon}"></i>` : '';

            groupsHtml += `
                <div class="wf-group-section">
                    <div class="wf-group-header">
                        ${groupIcon}
                        <span>${this.escapeHtml(group.name)}</span>
                    </div>
                    ${groupContentHtml}
                </div>
            `;
        });

        return `
            <div class="wf-auto-diagram" data-workspace="${this.escapeHtml(workspace_name)}">
                <div class="wf-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                    </svg>
                    <span>Quy trình nghiệp vụ</span>
                </div>
                <div class="wf-groups-wrapper">
                    ${groupsHtml}
                </div>
            </div>
        `;
    },

    /**
     * Thuật toán quan trọng nhất: Sắp xếp các node vào các cột (depth) dựa trên kết nối.
     * 
     * Nguyên lý hoạt động:
     * 1. Xây dựng Đồ thị có hướng (Directed Graph) từ danh sách node và kết nối.
     * 2. Sử dụng thuật toán Duyệt theo chiều rộng (BFS) để tính toán "độ sâu" (depth) của từng node.
     *    - Độ sâu đại diện cho vị trí cột (trục X) của node trong sơ đồ xương cá.
     *    - Các node có cùng độ sâu sẽ được xếp vào cùng một cột dọc (đối xứng qua trục chính).
     * 3. Xử lý các node rẽ nhánh: Nếu nhiều node cùng kết nối tới một node cha, chúng sẽ được 
     *    gán cùng một độ sâu để hiển thị song song (trên/dưới).
     * 4. Xử lý các node đơn lẻ (Standalone): Các node không có kết nối nào sẽ được tự động 
     *    xếp vào các cột riêng biệt ở phía cuối sơ đồ để tránh chồng lấn.
     */
    getNodesInColumns: function(nodes, connections) {
        if (!nodes || nodes.length === 0) return [];
        
        const normalize = (id) => (id || "").toString().trim().toLowerCase();
        
        // 1. Map ID -> Node
        const nodeMap = new Map();
        nodes.forEach(n => {
            const normId = normalize(n.id);
            nodeMap.set(normId, n);
        });

        // 2. Xây dựng đồ thị và tính bậc vào
        const adj = new Map();
        const inDegree = new Map();
        const allNodeIds = new Set();
        
        nodes.forEach(n => {
            const normId = normalize(n.id);
            allNodeIds.add(normId);
            adj.set(normId, []);
            inDegree.set(normId, 0);
        });
        
        connections.forEach(c => {
            const fromNorm = normalize(c.from);
            const toNorm = normalize(c.to);
            if (allNodeIds.has(fromNorm) && allNodeIds.has(toNorm)) {
                adj.get(fromNorm).push(toNorm);
                inDegree.set(toNorm, (inDegree.get(toNorm) || 0) + 1);
            }
        });

        // 3. Tính depth bằng BFS
        let depthMap = new Map();
        let queue = [];
        
        // Node gốc là node có bậc vào = 0 (bao gồm cả node có kết nối và node standalone)
        nodes.forEach(n => {
            const normId = normalize(n.id);
            if (inDegree.get(normId) === 0) {
                queue.push({ id: normId, depth: 0 });
                depthMap.set(normId, 0);
            }
        });

        while (queue.length > 0) {
            let { id, depth } = queue.shift();
            (adj.get(id) || []).forEach(nextId => {
                let nextDepth = depth + 1;
                if (!depthMap.has(nextId) || depthMap.get(nextId) < nextDepth) {
                    depthMap.set(nextId, nextDepth);
                    queue.push({ id: nextId, depth: nextDepth });
                }
            });
        }

        // 4. Phân bổ node vào các cột (columnsMap)
        let columnsMap = new Map();
        let maxDepth = -1;

        // Xử lý tất cả các node dựa trên depthMap
        // Sắp xếp theo depth tăng dần. Nếu cùng depth, thứ tự sẽ dựa trên vị trí xuất hiện trong JSON
        const sortedDepthEntries = Array.from(depthMap.entries()).sort((a, b) => a[1] - b[1]);

        sortedDepthEntries.forEach(([id, d]) => {
            const node = nodeMap.get(id);
            if (!node) return;

            let targetDepth = d;
            while (true) {
                let currentColumnNodes = columnsMap.get(targetDepth) || [];
                let hasSameLane = currentColumnNodes.some(n => n.lane === node.lane);
                
                if (!hasSameLane) {
                    if (!columnsMap.has(targetDepth)) columnsMap.set(targetDepth, []);
                    columnsMap.get(targetDepth).push(node);
                    if (targetDepth > maxDepth) maxDepth = targetDepth;
                    break;
                }
                targetDepth++;
            }
        });

        // 5. Chuyển đổi thành mảng các cột đã sắp xếp
        let columns = [];
        const sortedColumnKeys = Array.from(columnsMap.keys()).sort((a, b) => a - b);
        
        sortedColumnKeys.forEach(k => {
            let col = columnsMap.get(k).sort((a, b) => {
                const order = { 'Top': 0, 'Main': 1, 'Bottom': 2 };
                return (order[a.lane] || 1) - (order[b.lane] || 1);
            });
            columns.push(col);
        });

        return columns;
    },

    /**
     * Tạo HTML cho menu dropdown chứa các hành động (Xem danh sách / Thêm mới)
     */
    create_dropdown_html: function(node) {
        if (!node.actions || node.actions.length === 0) return '';

        let actionRows = '';
        node.actions.forEach(action => {
            let viewHref = '#';
            let newHref = '#';
            
            if (action.link_to) {
                if (action.link_type === 'DocType') {
                    viewHref = `/app/${frappe.router.slug(action.link_to)}`;
                    newHref = `/app/${frappe.router.slug(action.link_to)}/new`;
                } else if (action.link_type === 'Report') {
                    viewHref = `/app/query-report/${encodeURIComponent(action.link_to)}`;
                    newHref = viewHref;
                }
            }

            actionRows += `
                <div class="wf-action-row">
                    <div class="wf-action-label">${this.escapeHtml(action.label)}</div>
                    <div class="wf-action-btns">
                        <a href="${viewHref}" class="wf-btn-view">Xem danh sách</a>
                        <a href="${newHref}" class="wf-btn-new">Thêm mới</a>
                    </div>
                </div>
            `;
        });

        return `
            <div class="wf-dropdown">
                ${actionRows}
            </div>
        `;
    },

    /**
     * Helper để an toàn hóa nội dung text trước khi render HTML
     */
    escapeHtml: function(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Gán các sự kiện click và hover cho các node trong sơ đồ.
     */
    attach_handlers: function(workspace_name) {
        const self = this;
        const container = document.querySelector(`.wf-auto-diagram[data-workspace="${workspace_name}"]`);
        if (!container) return;

        // Gán sự kiện click cho thẻ node để chuyển hướng trang
        container.querySelectorAll('.wf-node-card, .wf-standalone-btn').forEach(card => {
            card.addEventListener('click', function(e) {
                // Nếu click vào các nút con trong dropdown thì không kích hoạt chuyển hướng của thẻ cha
                if (e.target.closest('.wf-action-btns')) return;

                const href = this.getAttribute('data-href') || this.querySelector('.wf-compact-node')?.getAttribute('data-href');
                if (href && href !== '#') {
                    e.preventDefault();
                    frappe.set_route(href);
                }
            });
        });

        // Xử lý z-index khi hover để đảm bảo dropdown luôn nổi lên trên các node khác
        container.querySelectorAll('.wf-node-card .wf-node-icon').forEach(icon => {
            const card = icon.closest('.wf-node-card');
            if (!card) return;

            const dropdown = card.querySelector('.wf-dropdown');

            icon.addEventListener('mouseenter', () => {
                // Tăng z-index của card cha để nó và dropdown con được ưu tiên hiển thị
                card.style.zIndex = 200;
            });

            const resetZIndex = () => {
                // Dùng timeout để kiểm tra xem chuột có đang ở trên dropdown hay không
                setTimeout(() => {
                    if (!dropdown || !dropdown.matches(':hover')) {
                        card.style.zIndex = ''; // Trả về z-index mặc định
                    }
                }, 100);
            };

            icon.addEventListener('mouseleave', resetZIndex);

            if (dropdown) {
                // Reset z-index ngay khi chuột rời khỏi dropdown
                dropdown.addEventListener('mouseleave', () => {
                    card.style.zIndex = '';
                });
            }
        });
    }

};

// Khởi chạy script ngay khi tài liệu sẵn sàng
$(document).ready(function() {
    dcnet.workflow_diagram.init();
});
