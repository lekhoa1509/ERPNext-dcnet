"""
Final workflow diagram embed with interactive dropdowns.
Run: bench --site flow.local execute dcnet_apps.workflow_diagram.embed_final.embed
"""

import frappe
import json


def embed():
    """Embed polished workflow diagram with dropdowns."""

    workspace = frappe.get_doc("Workspace", "Buying")
    content = json.loads(workspace.content or "[]")

    # Remove any existing workflow blocks
    content = [b for b in content if not (
        b.get("type") == "header" and
        "workflow-diagram" in b.get("data", {}).get("text", "")
    )]
    content = [b for b in content if not (
        b.get("type") == "custom_block" and
        "Workflow" in b.get("data", {}).get("custom_block_name", "")
    )]

    # Create workflow diagram HTML with dropdowns
    diagram_html = '''<div class="workflow-diagram-container" id="buying-workflow-diagram">
<style>
.workflow-diagram-container {
    padding: 20px;
    background: var(--card-bg);
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--border-color);
    margin-bottom: 15px;
}
.workflow-diagram-container .wf-title {
    margin: 0 0 20px;
    font-size: 15px;
    font-weight: 600;
    color: var(--heading-color);
    display: flex;
    align-items: center;
    gap: 8px;
}
.workflow-diagram-container .wf-flow {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    gap: 8px;
}
.workflow-diagram-container .wf-node-wrapper {
    position: relative;
}
.workflow-diagram-container .wf-node {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border-radius: var(--border-radius-md);
    font-weight: 500;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 2px solid;
    white-space: nowrap;
}
.workflow-diagram-container .wf-node:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.workflow-diagram-container .wf-node.active {
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}
.workflow-diagram-container .wf-node-icon {
    font-size: 14px;
}
.workflow-diagram-container .wf-arrow {
    display: flex;
    align-items: center;
    padding: 0 4px;
}
.workflow-diagram-container .wf-arrow svg {
    width: 24px;
    height: 24px;
    color: var(--text-muted);
}
.workflow-diagram-container .node-blue {
    background: #eff6ff;
    color: #1e40af;
    border-color: #3b82f6;
}
.workflow-diagram-container .node-green {
    background: #f0fdf4;
    color: #166534;
    border-color: #22c55e;
}
.workflow-diagram-container .node-orange {
    background: #fff7ed;
    color: #9a3412;
    border-color: #f97316;
}
.workflow-diagram-container .node-purple {
    background: #faf5ff;
    color: #7c3aed;
    border-color: #a855f7;
}
.workflow-diagram-container .wf-group {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px dashed var(--border-color);
}
.workflow-diagram-container .wf-group-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 12px;
    font-weight: 600;
}
/* Dropdown */
.workflow-diagram-container .wf-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 100;
    min-width: 220px;
    margin-top: 8px;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    box-shadow: var(--shadow-lg);
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all 0.2s ease;
}
.workflow-diagram-container .wf-dropdown.show {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
.workflow-diagram-container .wf-dropdown-header {
    padding: 10px 14px;
    font-size: 12px;
    font-weight: 600;
    color: var(--heading-color);
    border-bottom: 1px solid var(--border-color);
    background: var(--control-bg);
    border-radius: var(--border-radius-md) var(--border-radius-md) 0 0;
}
.workflow-diagram-container .wf-dropdown-list {
    padding: 6px 0;
    max-height: 250px;
    overflow-y: auto;
}
.workflow-diagram-container .wf-dropdown-item {
    display: block;
    padding: 8px 14px;
    font-size: 13px;
    color: var(--text-color);
    text-decoration: none;
    transition: background 0.15s;
}
.workflow-diagram-container .wf-dropdown-item:hover {
    background: var(--control-bg);
    color: var(--primary);
    text-decoration: none;
}
/* Dark mode */
[data-theme="dark"] .workflow-diagram-container .node-blue {
    background: #1e3a5f;
    color: #93c5fd;
}
[data-theme="dark"] .workflow-diagram-container .node-green {
    background: #14532d;
    color: #86efac;
}
[data-theme="dark"] .workflow-diagram-container .node-orange {
    background: #7c2d12;
    color: #fdba74;
}
[data-theme="dark"] .workflow-diagram-container .node-purple {
    background: #4c1d95;
    color: #c4b5fd;
}
</style>

<div class="wf-title">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
    </svg>
    Quy trình Mua hàng
</div>

<div class="wf-flow" id="wf-main-flow">
    <!-- Node 1: Yêu cầu & Đặt hàng -->
    <div class="wf-node-wrapper">
        <div class="wf-node node-blue" data-node="request" onclick="toggleWfDropdown(this)">
            <span class="wf-node-icon">📋</span>
            <span>Yêu cầu & Đặt hàng</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9l6 6 6-6"/>
            </svg>
        </div>
        <div class="wf-dropdown" id="dropdown-request">
            <div class="wf-dropdown-header">Yêu cầu & Đặt hàng</div>
            <div class="wf-dropdown-list">
                <a class="wf-dropdown-item" href="/app/material-request">Yêu cầu mua hàng</a>
                <a class="wf-dropdown-item" href="/app/request-for-quotation">Yêu cầu báo giá (RFQ)</a>
                <a class="wf-dropdown-item" href="/app/supplier-quotation">Báo giá NCC</a>
                <a class="wf-dropdown-item" href="/app/purchase-order">Đơn mua hàng (PO)</a>
            </div>
        </div>
    </div>

    <!-- Arrow -->
    <div class="wf-arrow">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
    </div>

    <!-- Node 2: Nhận hàng -->
    <div class="wf-node-wrapper">
        <div class="wf-node node-green" data-node="receive" onclick="toggleWfDropdown(this)">
            <span class="wf-node-icon">📦</span>
            <span>Nhận hàng</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9l6 6 6-6"/>
            </svg>
        </div>
        <div class="wf-dropdown" id="dropdown-receive">
            <div class="wf-dropdown-header">Nhận hàng</div>
            <div class="wf-dropdown-list">
                <a class="wf-dropdown-item" href="/app/purchase-receipt">Phiếu nhập kho</a>
                <a class="wf-dropdown-item" href="/app/landed-cost-voucher">Chi phí nhập khẩu</a>
                <a class="wf-dropdown-item" href="/app/purchase-receipt?is_return=1">Trả hàng NCC</a>
            </div>
        </div>
    </div>

    <!-- Arrow -->
    <div class="wf-arrow">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
    </div>

    <!-- Node 3: Hóa đơn & Thanh toán -->
    <div class="wf-node-wrapper">
        <div class="wf-node node-orange" data-node="payment" onclick="toggleWfDropdown(this)">
            <span class="wf-node-icon">💳</span>
            <span>Hóa đơn & Thanh toán</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9l6 6 6-6"/>
            </svg>
        </div>
        <div class="wf-dropdown" id="dropdown-payment">
            <div class="wf-dropdown-header">Hóa đơn & Thanh toán</div>
            <div class="wf-dropdown-list">
                <a class="wf-dropdown-item" href="/app/purchase-invoice">Hóa đơn mua</a>
                <a class="wf-dropdown-item" href="/app/payment-entry?payment_type=Pay">Phiếu thanh toán NCC</a>
                <a class="wf-dropdown-item" href="/app/payment-terms-template">Điều khoản thanh toán</a>
            </div>
        </div>
    </div>
</div>

<!-- Danh mục group -->
<div class="wf-group">
    <div class="wf-group-label">Danh mục</div>
    <div class="wf-flow">
        <div class="wf-node-wrapper">
            <div class="wf-node node-purple" data-node="supplier" onclick="toggleWfDropdown(this)">
                <span class="wf-node-icon">👥</span>
                <span>Nhà cung cấp</span>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M6 9l6 6 6-6"/>
                </svg>
            </div>
            <div class="wf-dropdown" id="dropdown-supplier">
                <div class="wf-dropdown-header">Nhà cung cấp</div>
                <div class="wf-dropdown-list">
                    <a class="wf-dropdown-item" href="/app/supplier">Nhà cung cấp</a>
                    <a class="wf-dropdown-item" href="/app/supplier-group">Nhóm NCC</a>
                    <a class="wf-dropdown-item" href="/app/price-list">Bảng giá NCC</a>
                    <a class="wf-dropdown-item" href="/app/contact">Liên hệ NCC</a>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
(function() {
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.wf-node-wrapper')) {
            document.querySelectorAll('.wf-dropdown.show').forEach(d => d.classList.remove('show'));
            document.querySelectorAll('.wf-node.active').forEach(n => n.classList.remove('active'));
        }
    });
})();

function toggleWfDropdown(node) {
    event.stopPropagation();
    const wrapper = node.closest('.wf-node-wrapper');
    const dropdown = wrapper.querySelector('.wf-dropdown');
    const isOpen = dropdown.classList.contains('show');

    // Close all dropdowns
    document.querySelectorAll('.wf-dropdown.show').forEach(d => d.classList.remove('show'));
    document.querySelectorAll('.wf-node.active').forEach(n => n.classList.remove('active'));

    // Toggle current
    if (!isOpen) {
        dropdown.classList.add('show');
        node.classList.add('active');
    }
}
</script>
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

    print("✅ Embedded polished workflow diagram with dropdowns")
    print("ℹ️ Hard refresh (Ctrl+Shift+R) to see changes")


if __name__ == "__main__":
    embed()
