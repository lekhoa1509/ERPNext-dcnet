/**
 * Period Closing Voucher (ERPNext) — VN hint banner.
 *
 * ERPNext PCV và VN Period Close có chức năng GIỐNG MỘT PHẦN nhưng KHÁC mục đích:
 *   - PCV: chỉ KHOÁ kỳ — ngăn hạch toán lùi vào kỳ đã đóng. Không sinh phiếu kế toán
 *     Nợ/Có 911. Chạy năm 1 lần.
 *   - VN Period Close: TẠO phiếu kế toán đầy đủ Nợ/Có 5xx-6xx → 911 → 4212. Chạy
 *     tháng / quý / năm.
 *
 * Hint banner trên PCV form để kế toán không nhầm 2 chứng từ.
 */
frappe.ui.form.on("Period Closing Voucher", {
    refresh: function (frm) {
        // Inline hint at top of form via set_intro (works on new + saved)
        frm.set_intro(
            __(
                "<b>⚠️ Đây là Phiếu khoá sổ kỳ kế toán (ERPNext core).</b> " +
                "Chứng từ này CHỈ <b>khoá kỳ</b> — không cho hạch toán lùi vào ngày trước Ngày khoá sổ. " +
                "<b>Không</b> sinh bút toán kết chuyển Nợ/Có 5xx-6xx → 911 → 4212.<br>" +
                "👉 Để kết chuyển Nợ/Có doanh thu - chi phí sang TK 911 → 4212 (hàng tháng / quý / năm), " +
                "dùng <a href='/app/vn-period-close/new'><b>Phiếu kết chuyển định kỳ</b></a> " +
                "(thuộc Cài đặt kế toán VN) — bước này phải làm <b>TRƯỚC</b> khi khoá sổ."
            ),
            "orange"
        );

        // Add custom button to jump to VN Period Close
        if (frm.doc.docstatus !== 2) {
            frm.add_custom_button(
                __("Mở Phiếu kết chuyển định kỳ"),
                function () {
                    frappe.set_route("List", "VN Period Close", {
                        company: frm.doc.company,
                    });
                },
                __("Hành động"),
            );
        }
    },
});
