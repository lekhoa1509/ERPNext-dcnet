// CCDC Allocation Schedule — VN inline guidance
// Lịch phân bổ giá trị CCDC (TK 242 → TK 6423) theo kỳ
(function () {
    const GUIDE_KEY = "vn_ccdc_alloc_guide_collapsed";

    frappe.ui.form.on("CCDC Allocation Schedule", {
        refresh(frm) {
            if ($(frm.layout.wrapper).find(".vn-ccdc-guide").length) return;

            const collapsed = localStorage.getItem(GUIDE_KEY) === "1";
            const html = `
            <div class="vn-ccdc-guide" style="background:#f0f7fa; border:1px solid #d0e3ed; border-radius:8px; margin:8px 0 16px; font-size:13px; line-height:1.7; color:#1a3a4a">
                <div class="vn-ccdc-guide-header" style="display:flex; justify-content:space-between; align-items:center; padding:12px 18px; cursor:pointer; user-select:none">
                    <span style="font-size:14px; font-weight:600">Hướng dẫn: Phân bổ giá trị CCDC theo kỳ</span>
                    <span class="vn-ccdc-guide-toggle" style="font-size:12px; color:#5a7a8a; white-space:nowrap">${collapsed ? "▸ Mở rộng" : "▾ Thu gọn"}</span>
                </div>
                <div class="vn-ccdc-guide-body" style="padding:0 18px 14px; ${collapsed ? "display:none" : ""}">
                    <div style="margin-bottom:10px">
                        <strong>Mục đích:</strong> Phân bổ giá trị công cụ dụng cụ (CCDC) vào chi phí qua nhiều kỳ kế toán. Theo TT99/2025, CCDC được ghi nhận ban đầu vào TK 242 (Chi phí chờ phân bổ), sau đó phân bổ dần vào TK 6423 (Chi phí CCDC) theo số kỳ sử dụng.
                    </div>

                    <div style="margin-bottom:10px">
                        <strong>Bút toán mỗi kỳ phân bổ:</strong><br>
                        <code style="background:#e8f0f5; padding:2px 6px; border-radius:3px">Nợ TK 6423 — Chi phí CCDC (= tổng giá trị ÷ số kỳ)</code><br>
                        <code style="background:#e8f0f5; padding:2px 6px; border-radius:3px">Có TK 242 — Chi phí chờ phân bổ</code>
                    </div>

                    <div style="margin-bottom:8px">
                        <strong>Cách sử dụng:</strong>
                        <ol style="margin:4px 0 0 -20px; padding-left:20px">
                            <li><strong>Chọn CCDC:</strong> Link tới CCDC Item đã được tạo trong danh mục CCDC</li>
                            <li><strong>Thiết lập:</strong> Nhập tổng giá trị, số kỳ phân bổ, tần suất (hàng tháng)</li>
                            <li><strong>Duyệt:</strong> Hệ thống tự tạo lịch phân bổ N kỳ</li>
                            <li><strong>Ghi sổ:</strong> Mỗi kỳ, kế toán xác nhận (Post) từng dòng → hệ thống tạo bút toán Nợ 6423 / Có 242</li>
                        </ol>
                    </div>

                    <div style="font-size:12px; color:#5a7a8a; border-top:1px solid #d0e3ed; padding-top:8px; margin-top:4px">
                        <strong>Tiến độ:</strong> Thanh trạng thái hiển thị "X/Y" — số kỳ đã ghi sổ / tổng số kỳ. Khi hoàn tất tất cả kỳ, trạng thái chuyển sang "Completed".
                    </div>
                </div>
            </div>`;

            $(frm.layout.wrapper).prepend(html);

            $(frm.layout.wrapper).find(".vn-ccdc-guide-header").on("click", function () {
                const $body = $(this).siblings(".vn-ccdc-guide-body");
                const $toggle = $(this).find(".vn-ccdc-guide-toggle");
                const isVisible = $body.is(":visible");
                $body.slideToggle(200);
                $toggle.text(isVisible ? "▸ Mở rộng" : "▾ Thu gọn");
                localStorage.setItem(GUIDE_KEY, isVisible ? "1" : "0");
            });
        },
    });
})();
