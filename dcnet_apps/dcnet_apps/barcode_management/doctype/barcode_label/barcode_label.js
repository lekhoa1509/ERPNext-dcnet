// Copyright (c) 2026, DCNET Cloud and contributors
// For license information, please see license.txt

frappe.ui.form.on('Barcode Label', {
	refresh: function(frm) {
		frm.trigger('render_barcode');
	},
	item: function(frm) {
		// When item is changed, we don't necessarily fetch (unless we want to default to something)
		// but we should refresh the preview
		frm.trigger('render_barcode');
	},
	barcode: function(frm) {
		// Update barcode_value and preview instantly
		frm.set_value('barcode_value', frm.doc.barcode);
		frm.trigger('render_barcode');
	},
	barcode_type: function(frm) {
		frm.trigger('render_barcode');
	},
	render_barcode: function(frm) {
		let wrapper = frm.get_field("barcode_display_html").$wrapper;
		wrapper.html('');

		if (frm.doc.barcode) {
			let svg_id = `preview-barcode-${frappe.utils.get_random(10)}`;
			wrapper.html(`<div class="text-center" style="padding: 10px; border: 1px solid #d1d8dd; border-radius: 4px; background: #fff;">
				<svg id="${svg_id}"></svg>
			</div>`);
			
			let barcode_format = frm.doc.barcode_type || "CODE128";
			
			// Normalize format for JsBarcode
			if (barcode_format === "EAN-13") barcode_format = "EAN13";
			if (barcode_format === "EAN-8") barcode_format = "EAN8";
			if (barcode_format === "UPC-A") barcode_format = "UPC";
			
			try {
				JsBarcode(`#${svg_id}`, frm.doc.barcode, {
					format: barcode_format,
					lineColor: "#000",
					width: 2,
					height: 60,
					displayValue: true
				});
			} catch (e) {
				// Don't log to console anymore, just show error in wrapper if needed
				// console.error("JsBarcode Error:", e);
			}
		}
	}
});
