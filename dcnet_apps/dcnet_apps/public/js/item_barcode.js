// JsBarcode is loaded via build.json before this file

// Item Barcode Display Logic
frappe.ui.form.on('Item', {
    refresh: function(frm) {
        // Log 1: Script có chạy không?
        console.log("--- Barcode Debugging: Script Start ---");

        if (frm.fields_dict['barcode_display_html']) {
            // Log 2: Có tìm thấy trường HTML không?
            console.log("Condition PASSED: Found 'barcode_display_html' field.");
            
            const wrapper = frm.get_field("barcode_display_html").$wrapper;
            wrapper.html('');

            if (frm.doc.barcodes && frm.doc.barcodes.length > 0) {
                // Log 3: Có tìm thấy dữ liệu trong bảng con không?
                console.log(`Condition PASSED: Found ${frm.doc.barcodes.length} row(s) in 'barcodes' table.`);
                
                let first_barcode_row = frm.doc.barcodes[0];
                console.log("Data found in first row:", first_barcode_row);

                if (first_barcode_row.barcode) {
                    console.log("Condition PASSED: The 'barcode' field has a value.");
                    let svg_id = `item-barcode-${frappe.utils.get_random(10)}`;
                    wrapper.html(`<svg id="${svg_id}"></svg>`);
                    let barcode_format = first_barcode_row.barcode_type || "CODE128";
                    
                    // Normalize format for JsBarcode (e.g., "EAN-13" -> "EAN13")
                    if (barcode_format === "EAN-13") barcode_format = "EAN13";
                    if (barcode_format === "EAN-8") barcode_format = "EAN8";
                    if (barcode_format === "UPC-A") barcode_format = "UPC";
                    
                    try {
                        JsBarcode(`#${svg_id}`, first_barcode_row.barcode, {
                            format: barcode_format,
                            lineColor: "#000",
                            width: 2,
                            height: 40,
                            displayValue: true
                        });
                    } catch (e) {
                        console.error("JsBarcode Error:", e);
                    }
                } else {
                    console.log("Condition FAILED: The 'barcode' field in the first row is empty/null.");
                }
            } else {
                // Log 4: Chạy nếu bảng con rỗng
                console.log("Condition FAILED: The 'frm.doc.barcodes' table is empty or does not exist for this Item.");
            }
        } else {
            // Log 5: Chạy nếu không tìm thấy trường HTML
            console.log("Condition FAILED: Could not find 'barcode_display_html' field. Please check the fieldname in Customize Form.");
        }
        console.log("--- Barcode Debugging: Script End ---");
    }
});