/**
 * DCNET Sidebar Preservation
 * 
 * Prevents automatic workspace switching when clicking sidebar items.
 * Scope: All workspaces (global)
 * Behavior: Always preserve current sidebar regardless of entity location
 */

(function() {
    'use strict';
    
    const MODULE_NAME = '[DCNET SidebarPreserve]';
    const STORAGE_KEY = 'dcnet_current_sidebar';
    
    let sidebarAtPageLoad = null;
    
    /**
     * Get current sidebar
     */
    function getCurrentSidebar() {
        if (frappe.app && frappe.app.sidebar && frappe.app.sidebar.sidebar_title) {
            return frappe.app.sidebar.sidebar_title;
        }
        const el = document.querySelector('.body-sidebar[data-title]');
        if (el) return el.getAttribute('data-title');
        return localStorage.getItem(STORAGE_KEY);
    }
    
    /**
     * Save sidebar
     */
    function saveSidebar() {
        const sidebar = getCurrentSidebar();
        if (sidebar) {
            localStorage.setItem(STORAGE_KEY, sidebar);
            return sidebar;
        }
        return null;
    }
    
    /**
     * Get DocType from route
     */
    function getDocType(route) {
        if (route && route.length >= 2) {
            if (route[0] === 'Form' || route[0] === 'List') {
                return route[1];
            }
        }
        return null;
    }
    
    /**
     * Check if DocType is in sidebar
     */
    function isDocTypeInSidebar(docType, sidebarName) {
        if (!frappe.app || !frappe.app.sidebar || !frappe.app.sidebar.get_workspace_sidebars) {
            return true;
        }
        try {
            const sidebars = frappe.app.sidebar.get_workspace_sidebars(docType);
            return sidebars.includes(sidebarName);
        } catch (e) {
            return true;
        }
    }
    
    /**
     * Patch set_workspace_sidebar
     */
    function patchSetWorkspaceSidebar() {
        if (!frappe.ui?.Sidebar?.prototype?.set_workspace_sidebar) return false;
        
        const original = frappe.ui.Sidebar.prototype.set_workspace_sidebar;
        
        frappe.ui.Sidebar.prototype.set_workspace_sidebar = function(router) {
            const current = this.sidebar_title;
            const route = frappe.get_route();
            const docType = getDocType(route);
            
            // If we have a sidebar at page load and current is different
            if (sidebarAtPageLoad && current !== sidebarAtPageLoad && docType) {
                const inOriginal = isDocTypeInSidebar(docType, sidebarAtPageLoad);
                
                if (inOriginal) {
                    // Restore to original sidebar
                    this.setup(sidebarAtPageLoad);
                    
                    // Highlight after restore
                    setTimeout(() => {
                        if (this.set_active_workspace_item) {
                            this.set_active_workspace_item();
                        }
                    }, 100);
                    
                    return;
                }
            }
            
            // Normal flow
            return original.call(this, router);
        };
        
        return true;
    }
    
    /**
     * Patch sidebar.setup
     */
    function patchSidebarSetup() {
        if (!frappe.ui?.Sidebar?.prototype?.setup) return false;
        
        const originalSetup = frappe.ui.Sidebar.prototype.setup;
        
        frappe.ui.Sidebar.prototype.setup = function(workspace_title) {
            const current = this.sidebar_title;
            const route = frappe.get_route();
            const docType = getDocType(route);
            
            // If trying to switch away from sidebarAtPageLoad
            if (sidebarAtPageLoad && workspace_title !== sidebarAtPageLoad && docType) {
                const inOriginal = isDocTypeInSidebar(docType, sidebarAtPageLoad);
                
                if (inOriginal) {
                    return originalSetup.call(this, sidebarAtPageLoad);
                }
            }
            
            return originalSetup.call(this, workspace_title);
        };
        
        return true;
    }
    
    /**
     * Install click handler
     */
    function installClickHandler() {
        document.addEventListener('click', function(e) {
            const target = e.target.closest('a[href^="/app/"], .item-anchor');
            if (target) {
                const current = getCurrentSidebar();
                if (current) {
                    sidebarAtPageLoad = current;
                    saveSidebar();
                }
            }
        }, true);
    }
    
    /**
     * Initialize
     */
    function init() {
        // Capture immediately
        sidebarAtPageLoad = getCurrentSidebar();
        
        // Install patches
        installClickHandler();
        
        let success = true;
        if (!patchSidebarSetup()) success = false;
        if (!patchSetWorkspaceSidebar()) success = false;
        
        if (success) {
            window.dcnet = window.dcnet || {};
            window.dcnet.sidebarPreserve = {
                version: '1.0.0',
                getPageLoadSidebar: () => sidebarAtPageLoad,
                getCurrent: getCurrentSidebar,
                restore: (name) => {
                    if (frappe.app && frappe.app.sidebar) {
                        frappe.app.sidebar.setup(name);
                    }
                }
            };
        } else {
            setTimeout(init, 300);
        }
    }
    
    // Start
    init();
    setTimeout(init, 500);
    
})();
