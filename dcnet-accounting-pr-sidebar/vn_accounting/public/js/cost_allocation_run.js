// Cost Allocation Run — VN inline guidance
// Kết chuyển CP SXC (TK 627) vào giá thành dở dang (TK 154) theo dự án
(function () {
    const GUIDE_KEY = "vn_car_guide_collapsed";

    frappe.ui.form.on("Cost Allocation Run", {
        refresh(frm) {
            if (frm.doc.docstatus > 0) return;
            if ($(frm.layout.wrapper).find(".vn-car-guide").length) return;

            const collapsed = localStorage.getItem(GUIDE_KEY) === "1";
            const html = `
            <div class="vn-car-guide" style="background:#f0f7fa; border:1px solid #d0e3ed; border-radius:8px; margin:8px 0 16px; font-size:13px; line-height:1.7; color:#1a3a4a">
                <div class="vn-car-guide-header" style="display:flex; justify-content:space-between; align-items:center; padding:12px 18px; cursor:pointer; user-select:none">
                    <span style="font-size:14px; font-weight:600">Hướng dẫn: Kết chuyển chi phí sản xuất chung vào giá thành dự án</span>
                    <span class="vn-car-guide-toggle" style="font-size:12px; color:#5a7a8a; white-space:nowrap">${collapsed ? "▸ Mở rộng" : "▾ Thu gọn"}</span>
                </div>
                <div class="vn-car-guide-body" style="padding:0 18px 14px; ${collapsed ? "display:none" : ""}">
                    <div style="margin-bottom:10px">
                        <strong>Mục đích:</strong> Cuối kỳ, kết chuyển chi phí sản xuất chung (TK 627) vào giá thành dở dang (TK 154) của từng dự án, theo tỷ lệ phân bổ do kế toán xác định. Theo TT99/2025, DN xây lắp/thi công <strong>bắt buộc</strong> dùng TK 627 cho CP gián tiếp công trình.
                    </div>

                    <div style="margin-bottom:10px">
                        <strong>Bút toán khi duyệt:</strong><br>
                        <code style="background:#e8f0f5; padding:2px 6px; border-radius:3px">Nợ TK 154 (Dự án A) — xx%</code><br>
                        <code style="background:#e8f0f5; padding:2px 6px; border-radius:3px">Nợ TK 154 (Dự án B) — yy%</code><br>
                        <code style="background:#e8f0f5; padding:2px 6px; border-radius:3px">Có TK 627 — tổng CP SXC trong kỳ</code>
                    </div>

                    <div style="margin-bottom:8px">
                        <strong>Các bước:</strong>
                        <ol style="margin:4px 0 0 -20px; padding-left:20px">
                            <li><strong>Chọn kỳ:</strong> Nhập ngày bắt đầu / kết thúc kỳ phân bổ</li>
                            <li><strong>Nguồn chi phí:</strong> Hệ thống tự lấy số dư TK 627 trong kỳ, hoặc kế toán nhập thủ công</li>
                            <li><strong>Phân bổ:</strong> Chọn phương pháp Đều (chia đều N dự án) hoặc Thủ công (nhập % từng dự án)</li>
                            <li><strong>Duyệt:</strong> Kiểm tra → Lưu → Gửi duyệt → Hệ thống tự tạo bút toán kết chuyển</li>
                        </ol>
                    </div>

                    <div style="font-size:12px; color:#5a7a8a; border-top:1px solid #d0e3ed; padding-top:8px; margin-top:4px">
                        <strong>Lưu ý:</strong><br>
                        • Kỳ kết chuyển không được trùng với kỳ đã đóng sổ (Period Closing Voucher).<br>
                        • Sau khi duyệt, hệ thống tự kiểm tra: nếu TK 627 còn số dư → cảnh báo (TT99/2025: cuối kỳ TK 627 phải kết chuyển hết).<br>
                        • Nếu dự án đã hoàn thành mà TK 154 còn số dư → cảnh báo cần kết chuyển 154→632 để đóng sổ dự án.
                    </div>
                </div>
            </div>`;

            $(frm.layout.wrapper).prepend(html);

            $(frm.layout.wrapper).find(".vn-car-guide-header").on("click", function () {
                const $body = $(this).siblings(".vn-car-guide-body");
                const $toggle = $(this).find(".vn-car-guide-toggle");
                const isVisible = $body.is(":visible");
                $body.slideToggle(200);
                $toggle.text(isVisible ? "▸ Mở rộng" : "▾ Thu gọn");
                localStorage.setItem(GUIDE_KEY, isVisible ? "1" : "0");
            });
        },
    });
})();
