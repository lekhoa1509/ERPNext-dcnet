"""
Simple workflow diagram embed - minimal HTML, external styling.
Run: bench --site flow.local execute dcnet_apps.workflow_diagram.embed_simple.embed
"""

import frappe
import json


def embed():
    """Embed simple workflow diagram."""

    workspace = frappe.get_doc("Workspace", "Buying")
    content = json.loads(workspace.content or "[]")

    # Simple HTML without complex inline styles
    diagram_html = '''<div class="buying-workflow">
<b>Quy trinh Mua hang</b>
<div class="wf-nodes">
<a href="/app/material-request" class="wf-n wf-blue">Yeu cau &amp; Dat hang</a>
<span class="wf-arr">&#8594;</span>
<a href="/app/purchase-receipt" class="wf-n wf-green">Nhan hang</a>
<span class="wf-arr">&#8594;</span>
<a href="/app/purchase-invoice" class="wf-n wf-orange">Hoa don &amp; Thanh toan</a>
</div>
<div class="wf-sep"></div>
<small>Danh muc:</small>
<a href="/app/supplier" class="wf-n wf-purple">Nha cung cap</a>
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

    print("✅ Embedded simple workflow diagram")


if __name__ == "__main__":
    embed()
