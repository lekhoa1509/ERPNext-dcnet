/**
 * Auto-render Workflow Diagram for Workspaces
 *
 * Automatically detects workspace pages and renders workflow diagram
 * based on sidebar configuration (workflow nodes).
 */

console.log('[WorkflowDiagram] Script loaded');

frappe.provide('dcnet.workflow_diagram');

dcnet.workflow_diagram = {
    // Cache for workflow configs
    cache: {},
    rendered_for: null,
    observer: null,

    init: function() {
        const self = this;
        console.log('[WorkflowDiagram] Initializing...');

        // Listen for workspace page show
        $(document).on('page-change', function() {
            console.log('[WorkflowDiagram] page-change event');
            setTimeout(() => self.check_and_render(), 300);
        });

        // Initial check after page loads
        $(document).ready(function() {
            console.log('[WorkflowDiagram] document ready');
            setTimeout(() => self.check_and_render(), 500);
        });

        // Watch for workspace container to appear (MutationObserver)
        self.setup_observer();

        // Also try on frappe.after_ajax
        if (frappe.after_ajax) {
            frappe.after_ajax(() => {
                console.log('[WorkflowDiagram] after_ajax');
                setTimeout(() => self.check_and_render(), 500);
            });
        }

        // Poll periodically for 10 seconds after page load (fallback)
        let attempts = 0;
        const pollInterval = setInterval(() => {
            attempts++;
            self.check_and_render();
            if (attempts >= 20) {
                clearInterval(pollInterval);
            }
        }, 500);
    },

    setup_observer: function() {
        const self = this;

        // Observe for workspace-main-section appearing
        this.observer = new MutationObserver(function(mutations) {
            const container = document.querySelector('.workspace-main-section');
            if (container && !container.querySelector('.wf-auto-diagram')) {
                console.log('[WorkflowDiagram] Observer detected workspace-main-section');
                self.check_and_render();
            }
        });

        this.observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    },

    check_and_render: function() {
        // Get workspace name from URL or frappe.workspace
        let workspace_name = this.get_workspace_name();

        if (!workspace_name) {
            return;
        }

        console.log('[WorkflowDiagram] Checking workspace:', workspace_name);

        // Don't re-render for same workspace
        if (this.rendered_for === workspace_name) {
            // But check if element still exists
            if (document.querySelector('.wf-auto-diagram')) {
                return;
            }
        }

        this.render_for_workspace(workspace_name);
    },

    get_workspace_name: function() {
        // Method 1: Check frappe.workspace._page
        if (frappe.workspace && frappe.workspace._page) {
            const page = frappe.workspace._page;
            return page.name || page.title;
        }

        // Method 2: Parse from URL route
        const route = frappe.get_route();
        if (route && route.length >= 1) {
            // Routes like ['Workspaces', 'Buying'] or just ['buying']
            if (route[0] === 'Workspaces' && route[1]) {
                return route[1];
            }
            // Direct workspace route - need to check if it's a workspace
            // Common workspace names
            const workspaces = ['Buying', 'Selling', 'Stock', 'Accounts', 'CRM', 'HR', 'Manufacturing', 'Projects'];
            const routeName = route[0];
            // Capitalize first letter for comparison
            const normalized = routeName.charAt(0).toUpperCase() + routeName.slice(1).toLowerCase();
            if (workspaces.includes(normalized)) {
                return normalized;
            }
        }

        // Method 3: Check if we're on a workspace page by DOM
        const workspaceContainer = document.querySelector('.workspace-main-section');
        if (workspaceContainer) {
            // Try to get name from sidebar or breadcrumb
            const activeLink = document.querySelector('.sidebar-menu .desk-sidebar-item.selected');
            if (activeLink) {
                return activeLink.getAttribute('data-page-name') || activeLink.textContent.trim();
            }
        }

        return null;
    },

    render_for_workspace: function(workspace_name) {
        const self = this;

        // Check cache first
        if (this.cache[workspace_name]) {
            this.inject_diagram(workspace_name, this.cache[workspace_name]);
            return;
        }

        // Fetch workflow config
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

    inject_diagram: function(workspace_name, config) {
        // Find the workspace content area
        const workspace_container = document.querySelector('.workspace-main-section');
        if (!workspace_container) {
            console.log('[WorkflowDiagram] No workspace-main-section found');
            return;
        }

        // Remove existing diagram
        const existing = workspace_container.querySelector('.wf-auto-diagram');
        if (existing) {
            existing.remove();
        }

        // Create diagram element
        const diagram = this.create_diagram_html(workspace_name, config);

        // Insert at the beginning of workspace content
        workspace_container.insertAdjacentHTML('afterbegin', diagram);

        // Mark as rendered
        this.rendered_for = workspace_name;

        // Add click handlers
        this.attach_handlers(workspace_name);

        console.log('[WorkflowDiagram] Rendered for', workspace_name);
    },

    create_diagram_html: function(workspace_name, config) {
        const nodes = config.nodes || [];
        const connections = config.connections || [];
        const groups = config.groups || [];

        // Find main group (the one with most connected nodes)
        let mainGroupName = null;
        let mainGroupNodes = [];

        if (groups.length > 0) {
            // Find group with connected nodes
            groups.forEach(g => {
                const groupNodeIds = g.nodes || [];
                const connectedNodes = nodes.filter(n =>
                    groupNodeIds.includes(n.id) &&
                    connections.some(c => c.from === n.id || c.to === n.id)
                );
                if (connectedNodes.length > mainGroupNodes.length) {
                    mainGroupName = g.name;
                    mainGroupNodes = connectedNodes;
                }
            });
        }

        // If no connected nodes found, use first 3 nodes
        if (mainGroupNodes.length === 0) {
            mainGroupNodes = nodes.slice(0, 3);
        }

        // Color classes
        const colorClass = {
            'blue': 'wf-blue',
            'green': 'wf-green',
            'orange': 'wf-orange',
            'purple': 'wf-purple',
            'red': 'wf-red',
            'auto': 'wf-gray'
        };

        // Build main flow HTML (connected nodes in order)
        let mainFlowHtml = '';
        let orderedNodes = this.orderNodesByConnections(mainGroupNodes, connections);

        orderedNodes.forEach((node, idx) => {
            const cls = colorClass[node.color] || 'wf-gray';
            const hasDropdown = node.actions && node.actions.length > 0;

            mainFlowHtml += `
                <div class="wf-node-wrap" data-node="${this.escapeHtml(node.id)}">
                    <div class="wf-node ${cls}" ${hasDropdown ? 'data-dropdown="true"' : ''}>
                        <span>${this.escapeHtml(node.label)}</span>
                        ${hasDropdown ? '<svg class="wf-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>' : ''}
                    </div>
                    ${hasDropdown ? this.create_dropdown_html(node) : ''}
                </div>
            `;

            // Add arrow if not last
            if (idx < orderedNodes.length - 1) {
                mainFlowHtml += '<div class="wf-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>';
            }
        });

        // Build other groups HTML (nodes not in main flow)
        let otherGroupsHtml = '';
        const mainNodeIds = orderedNodes.map(n => n.id);
        const otherNodes = nodes.filter(n => !mainNodeIds.includes(n.id));

        if (otherNodes.length > 0) {
            // Group by workflow_group
            const groupedOther = {};
            otherNodes.forEach(node => {
                const groupName = node.group || 'Khác';
                if (!groupedOther[groupName]) groupedOther[groupName] = [];
                groupedOther[groupName].push(node);
            });

            Object.keys(groupedOther).forEach(groupName => {
                let groupNodesHtml = '';
                groupedOther[groupName].forEach(node => {
                    const cls = colorClass[node.color] || 'wf-gray';
                    const hasDropdown = node.actions && node.actions.length > 0;

                    groupNodesHtml += `
                        <div class="wf-node-wrap" data-node="${this.escapeHtml(node.id)}">
                            <div class="wf-node ${cls}" ${hasDropdown ? 'data-dropdown="true"' : ''}>
                                <span>${this.escapeHtml(node.label)}</span>
                                ${hasDropdown ? '<svg class="wf-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>' : ''}
                            </div>
                            ${hasDropdown ? this.create_dropdown_html(node) : ''}
                        </div>
                    `;
                });

                otherGroupsHtml += `
                    <div class="wf-group">
                        <div class="wf-group-label">${this.escapeHtml(groupName)}</div>
                        <div class="wf-flow">${groupNodesHtml}</div>
                    </div>
                `;
            });
        }

        return `
            <div class="wf-auto-diagram" data-workspace="${this.escapeHtml(workspace_name)}">
                <div class="wf-title">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                    </svg>
                    <span>Quy trình</span>
                </div>
                <div class="wf-flow">${mainFlowHtml}</div>
                ${otherGroupsHtml}
            </div>
        `;
    },

    orderNodesByConnections: function(nodes, connections) {
        // Order nodes by following connections
        if (nodes.length <= 1) return nodes;

        const nodeMap = {};
        nodes.forEach(n => nodeMap[n.id] = n);

        // Find start node (has outgoing but no incoming in this set)
        const nodeIds = new Set(nodes.map(n => n.id));
        const hasIncoming = new Set();
        const hasOutgoing = new Set();

        connections.forEach(c => {
            if (nodeIds.has(c.from) && nodeIds.has(c.to)) {
                hasOutgoing.add(c.from);
                hasIncoming.add(c.to);
            }
        });

        let startNode = nodes.find(n => hasOutgoing.has(n.id) && !hasIncoming.has(n.id));
        if (!startNode) startNode = nodes[0];

        // Follow connections to order
        const ordered = [startNode];
        const visited = new Set([startNode.id]);

        let current = startNode;
        while (ordered.length < nodes.length) {
            const nextConn = connections.find(c => c.from === current.id && nodeIds.has(c.to) && !visited.has(c.to));
            if (nextConn && nodeMap[nextConn.to]) {
                current = nodeMap[nextConn.to];
                ordered.push(current);
                visited.add(current.id);
            } else {
                // Add remaining unvisited nodes
                nodes.forEach(n => {
                    if (!visited.has(n.id)) {
                        ordered.push(n);
                        visited.add(n.id);
                    }
                });
                break;
            }
        }

        return ordered;
    },

    create_dropdown_html: function(node) {
        if (!node.actions || node.actions.length === 0) return '';

        let items = '';
        node.actions.forEach(action => {
            let href = '#';
            if (action.url) {
                href = action.url;
            } else if (action.link_to) {
                if (action.link_type === 'DocType') {
                    href = '/app/' + frappe.router.slug(action.link_to);
                } else if (action.link_type === 'Report') {
                    href = '/app/query-report/' + encodeURIComponent(action.link_to);
                }
            }
            items += `<a class="wf-dropdown-item" href="${href}">${this.escapeHtml(action.label)}</a>`;
        });

        return `
            <div class="wf-dropdown">
                <div class="wf-dropdown-header">${this.escapeHtml(node.label)}</div>
                <div class="wf-dropdown-body">${items}</div>
            </div>
        `;
    },

    escapeHtml: function(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    attach_handlers: function(workspace_name) {
        const container = document.querySelector(`.wf-auto-diagram[data-workspace="${workspace_name}"]`);
        if (!container) return;

        // Click on node with dropdown
        container.querySelectorAll('.wf-node[data-dropdown="true"]').forEach(node => {
            node.addEventListener('click', function(e) {
                e.stopPropagation();
                const wrap = node.closest('.wf-node-wrap');
                const dropdown = wrap.querySelector('.wf-dropdown');
                const isOpen = dropdown.classList.contains('show');

                // Close all
                container.querySelectorAll('.wf-dropdown.show').forEach(d => d.classList.remove('show'));
                container.querySelectorAll('.wf-node.active').forEach(n => n.classList.remove('active'));

                if (!isOpen) {
                    dropdown.classList.add('show');
                    node.classList.add('active');
                }
            });
        });

        // Close on outside click
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.wf-node-wrap')) {
                container.querySelectorAll('.wf-dropdown.show').forEach(d => d.classList.remove('show'));
                container.querySelectorAll('.wf-node.active').forEach(n => n.classList.remove('active'));
            }
        });
    }
};

// Initialize when ready
$(document).ready(function() {
    dcnet.workflow_diagram.init();
});
