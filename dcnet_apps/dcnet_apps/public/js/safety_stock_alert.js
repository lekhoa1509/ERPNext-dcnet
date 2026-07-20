/**
 * Safety Stock Alert for Sales Order
 * After submit, calls API to check low stock items and shows a dialog.
 */

frappe.ui.form.on('Sales Order', {
	on_submit: function(frm) {
		check_low_stock(frm);
	},
	after_submit: function(frm) {
	}
});

function check_low_stock(frm) {
	frappe.call({
		method: 'dcnet_apps.stock.safety_stock_check.get_low_stock_items',
		args: { sales_order: frm.doc.name },
		async: false,
		callback: function(r) {
			if (r.message && r.message.items && r.message.items.length) {
				show_low_stock_dialog(r.message);
			}
		}
	});
}

function show_low_stock_dialog(data) {
	let rows = data.items.map(item => `
		<tr>
			<td>${item.item_code}</td>
			<td>${item.warehouse}</td>
			<td style="text-align: right;">${item.ordered_qty}</td>
			<td style="text-align: right; color: #e53e3e; font-weight: bold;">${item.actual_qty}</td>
			<td style="text-align: right;">${item.safety_stock}</td>
		</tr>
	`).join('');

	let dialog = new frappe.ui.Dialog({
		title: __('Low Stock Warning'),
		size: 'large',
		indicator: 'orange',
	});

	dialog.$body.html(`
		<div style="padding: 15px;">
			<p><strong>⚠️ ${__('The following products are running low on stock')}:</strong></p>
			<table class="table table-bordered table-condensed" style="margin-top: 10px;">
				<thead>
					<tr style="background-color: #f7fafc;">
						<th>${__('Item Code')}</th>
						<th>${__('Warehouse')}</th>
						<th style="text-align: right;">${__('Ordered Qty')}</th>
						<th style="text-align: right;">${__('Actual Qty')}</th>
						<th style="text-align: right;">${__('Safety Stock')}</th>
					</tr>
				</thead>
				<tbody>${rows}</tbody>
			</table>
			<p style="margin-top: 10px; color: #6c757d;">
				${__('Please create a Material Request to replenish stock')}.
			</p>
		</div>
	`);

	// Primary action button: Create Material Request
	dialog.set_primary_action(__('Create Material Request'), function() {
		dialog.hide();
		let mr_data = data.mr_data;
		frappe.model.with_doctype('Material Request', () => {
			let doc = frappe.model.get_new_doc('Material Request', null, null, true);
			doc.material_request_type = mr_data.material_request_type;
			doc.items = [];
			(mr_data.items || []).forEach(item => {
				let child = frappe.model.add_child(doc, 'items');
				Object.assign(child, item);
			});
			frappe.set_route('Form', 'Material Request', doc.name);
		});
	});

	dialog.set_secondary_action_label(__('Cancel'));
	dialog.set_secondary_action(function() {
		dialog.hide();
	});

	dialog.show();
}
