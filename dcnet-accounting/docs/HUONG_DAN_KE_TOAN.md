# Hệ thống Kế toán — Hướng dẫn dành cho Kế toán trưởng

Tài liệu này mô tả các chức năng kế toán hiện có, viết theo góc nhìn công việc hàng ngày của Phòng Kế toán. Mỗi chức năng đều ghi rõ **khi nào dùng** và **kết quả mang lại**.

> Quy ước trong tài liệu:
> - TK = tài khoản (theo Thông tư 99/2025/TT-BTC)
> - "Phiếu" = chứng từ; "Sổ" = báo cáo chi tiết; "Bảng" = báo cáo tổng hợp
> - Viết tắt tiêu chuẩn dùng trong tài liệu: GTGT (Giá trị gia tăng), TNDN (Thu nhập doanh nghiệp), TNCN (Thu nhập cá nhân), BHXH (Bảo hiểm xã hội), BHYT (Bảo hiểm y tế), MST (Mã số thuế)

---

## I. Trang Tổng quan

| Chức năng | Khi nào dùng | Nó cho biết điều gì |
|---|---|---|
| **Tổng quan** | Mở đầu ngày làm việc | Năm chỉ số chính (Doanh thu, Chi phí, Lợi nhuận gộp, Công nợ phải thu, Dòng tiền) cùng tám biểu đồ chia theo Tuần / Tháng / Quý / Năm. Giúp Kế toán trưởng nắm tình hình tài chính trong nửa phút. |

---

## II. Quản lý Tiền mặt

Kế toán trưởng nào cũng bắt đầu ngày bằng việc kiểm soát quỹ tiền mặt. Phần này hỗ trợ ghi chép thu-chi, đối chiếu quỹ, theo dõi quỹ chi nhánh.

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Phiếu thu** | Khi khách trả tiền mặt, hoàn tạm ứng, thu hộ | Danh sách phiếu thu trong kỳ (Nợ TK 111). Có thể lọc theo ngày, tài khoản, chi nhánh. |
| **Phiếu chi** | Khi chi tiền mặt (mua hàng, tạm ứng, lương, chi khác) | Danh sách phiếu chi (Có TK 111). Cùng bộ lọc với Phiếu thu. |
| **Kiểm kê quỹ** | Định kỳ cuối tháng hoặc đột xuất, đối chiếu tiền mặt thực tế với sổ sách | Nhập tồn theo từng mệnh giá, hệ thống tự so với số dư trên sổ. Nếu chênh lệch, tự gợi ý tài khoản chênh lệch (1381 nếu thiếu, 3381 nếu thừa) và lập phiếu kế toán xử lý. Trạng thái có ba bước: Lập phiếu → Chờ xử lý chênh lệch → Đã xử lý (khóa). |
| **Sổ quỹ tiền mặt** | Khi cần in/xuất sổ quỹ theo từng TK 111 con | Theo mẫu sổ quỹ Việt Nam: số dư đầu kỳ, phát sinh thu, phát sinh chi, số dư cuối, theo từng dòng nghiệp vụ. |
| **Phiếu quỹ chi nhánh** | Ghi thu-chi nội bộ ở chi nhánh chưa hợp nhất quỹ | Phiếu chỉ lưu vết nội bộ, không sinh bút toán lên Sổ Cái. Người dùng chỉ thao tác được trên quỹ chi nhánh mình phụ trách. |
| **Sổ quỹ chi nhánh** | Khi cần sổ quỹ riêng cho từng chi nhánh | Hiển thị thu-chi nội bộ của một chi nhánh và đơn vị hạch toán. |

---

## III. Ngân hàng & Dòng tiền

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Thu ngân hàng** | Khi khách chuyển khoản về | Danh sách thu ngân hàng (Nợ TK 112). Lọc theo ngân hàng, ngày, đối ứng. |
| **Chi ngân hàng** | Khi lập Ủy nhiệm chi, séc, lệnh chuyển ra | Danh sách chi ngân hàng (Có TK 112). |
| **Sổ Tài khoản ngân hàng** | In sổ chi tiết theo từng tài khoản ngân hàng | Tương tự sổ quỹ tiền mặt nhưng theo TK 112 con (mỗi tài khoản tại mỗi ngân hàng có thể tách 1121, 1122, 1123…). |
| **Đối soát sao kê** | Đối chiếu sao kê ngân hàng với sổ kế toán | Tải lên file Excel sao kê (BIDV, MB, Sacombank, PG Bank), hệ thống tự đối chiếu với hóa đơn / phiếu thanh toán đã ghi. Liệt kê các giao dịch chưa khớp để Kế toán xử lý. |
| **Điều chuyển nội bộ** | Khi rút tiền mặt từ ngân hàng, nộp tiền mặt vào ngân hàng, hoặc chuyển giữa các tài khoản | Tra cứu các phiếu điều chuyển nội bộ giữa TK 111 và 112, hoặc giữa các tài khoản 112. |
| **Bút toán ngân hàng** | Lập phiếu kế toán liên quan ngân hàng — lãi tiền gửi, phí ngân hàng, đánh giá lại tỷ giá | Phiếu kế toán chuyên ngân hàng — dùng khi không phù hợp dùng Phiếu thu / Phiếu chi (ví dụ phí ngân hàng tự động trừ). |
| **Tiền gửi có kỳ hạn** | Khi doanh nghiệp gửi tiết kiệm có kỳ hạn tại ngân hàng | Nhập hợp đồng tiền gửi: số tiền gốc, kỳ hạn, lãi suất. Hệ thống tự lập lịch nhận lãi từng kỳ, ngày đáo hạn, tổng lãi dự kiến. Đến kỳ, Kế toán ghi nhận lãi (Nợ TK 112 / Có TK 515). |
| **Tổng hợp tiền gửi có kỳ hạn** | Khi muốn xem toàn bộ tiền gửi đang có | Bảng tổng hợp: số dư đầu kỳ, kỳ hạn còn lại, lãi đã ghi, lãi dự kiến nhận. |
| **Khoản vay ngân hàng** | Khi doanh nghiệp vay ngân hàng | Nhập hợp đồng vay: gốc, kỳ hạn, lãi suất, lịch trả gốc và lãi. Hệ thống lập lịch trả hàng tháng. |
| **Tổng hợp khoản vay ngân hàng** | Xem toàn bộ nợ ngân hàng | Bảng tổng hợp: dư nợ gốc còn lại, kỳ trả tiếp theo, tổng lãi đã trả. |
| **Dự báo dòng tiền** | Lập kế hoạch dòng tiền cho tuần / tháng tới | Dựa trên công nợ phải thu (theo hạn), công nợ phải trả, lịch trả vay, lương, và kỳ phải nộp thuế. Chia theo Ngày / Tuần / Tháng / Quý. Phân biệt phần "Hiện hành" (đã chắc chắn) và "Dự báo" (ước tính). |

---

## IV. Mua hàng & Công nợ phải trả

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Đơn mua hàng** | Lập đơn đặt mua từ Nhà cung cấp | Lưu đơn mua, có quy trình duyệt, sinh phiếu nhập kho và hóa đơn theo dõi tiến độ. |
| **Đơn mua hàng cần lập hóa đơn** | Khi cần đối chiếu các đơn đã nhận hàng nhưng Nhà cung cấp chưa gửi hóa đơn | Danh sách đơn mua có hàng về kho nhưng chưa khớp hóa đơn — gợi ý Kế toán đôn thúc lấy hóa đơn. |
| **Hoá đơn mua hàng** | Khi nhận hóa đơn giá trị gia tăng từ Nhà cung cấp | Ghi nhận hóa đơn, sinh các bút toán Nợ TK 1331 (thuế GTGT đầu vào), Nợ TK 133 / 152 / 156 (chi phí mua), Có TK 331 (phải trả). Có ô đánh dấu "Không được trừ thuế Thu nhập doanh nghiệp" để khoanh chi phí không hợp lệ ngay khi nhập. |
| **Nhập kho mua hàng** | Khi hàng về kho | Sinh bút toán Nợ TK 152 / 156 / Có TK 331 (hoặc Nợ TK 154 nếu mua dùng ngay). |
| **Điều khoản thanh toán** | Khi cấu hình kỳ hạn thanh toán theo Nhà cung cấp | Ví dụ 30/60/90 ngày, phần trăm theo đợt, chiết khấu nếu trả sớm. |
| **Công nợ phải trả** | Báo cáo công nợ Nhà cung cấp tại một thời điểm | Theo từng Nhà cung cấp và tuổi nợ (0-30, 31-60, 61-90, trên 90 ngày). |
| **Bảng tổng hợp công nợ Nhà cung cấp** | Tổng hợp công nợ theo Nhà cung cấp theo khoảng kỳ | Một Nhà cung cấp một dòng — tổng dư đầu, phát sinh trong kỳ, dư cuối. |
| **Báo cáo mua hàng** | Phân tích chi tiêu mua hàng theo thời gian / Nhà cung cấp / mặt hàng | Biểu đồ và bảng. |
| **Mua không VAT** | Khi cần tách chi phí đầu vào không có thuế GTGT (không được khấu trừ) | Liệt kê hóa đơn mua hàng có TK 1331 bằng 0 — phục vụ tính thuế GTGT phải nộp. |
| **Báo cáo theo mặt hàng** | Phân tích mua hàng theo từng mã hàng | Số lượng và giá trị mua, biến động giá theo thời gian. |
| **Bút toán chung** | Khi nghiệp vụ mua hàng không phù hợp lập trên Hóa đơn mua hàng — ví dụ phân bổ chi phí, kết chuyển | Phiếu kế toán tự do. |

---

## V. Bán hàng & Công nợ phải thu

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Báo giá** | Lập báo giá cho khách hàng | Báo giá — khi khách chốt, chuyển thành Đơn bán hàng. |
| **Đơn bán hàng** | Khi khách đặt hàng | Theo dõi tiến độ giao hàng, xuất hóa đơn theo đợt. |
| **Đơn bán hàng cần xuất hóa đơn** | Khi cần đôn thúc xuất hóa đơn cho đơn đã giao hàng | Danh sách đơn bán đã giao xong nhưng chưa lập hóa đơn bán hàng. |
| **Hoá đơn bán hàng** | Khi xuất hóa đơn cho khách hàng | Sinh bút toán Nợ TK 131 / Có TK 511 và Có TK 33311 (thuế GTGT đầu ra). Tùy cấu hình, có thể ký số và gửi hóa đơn điện tử qua nhà cung cấp dịch vụ hóa đơn điện tử. |
| **Điều khoản thanh toán** | Cấu hình kỳ hạn theo Khách hàng | Tương tự bên Mua hàng. |
| **Công nợ phải thu** | Báo cáo công nợ Khách hàng tại một thời điểm | Phân loại theo tuổi nợ. |
| **Bảng tổng hợp công nợ Khách hàng** | Tổng hợp theo Khách hàng | Một Khách hàng một dòng — tổng dư đầu, phát sinh trong kỳ, dư cuối. |
| **Báo cáo bán hàng** | Phân tích bán hàng theo thời gian / Khách hàng / mặt hàng | Biểu đồ và bảng. |
| **Phiếu xuất kho** | Khi giao hàng cho khách hàng | Sinh bút toán Có TK 156 / Nợ TK 632 (giá vốn hàng bán). |
| **Bút toán chung** | Phiếu kế toán tự do liên quan bán hàng | Cùng chức năng với mục cùng tên bên Mua hàng. |

---

## VI. Hợp đồng & Phương án kinh doanh

Phần này dành riêng cho mô hình doanh nghiệp có hợp đồng dài hạn, thanh toán theo nhiều đợt, có hoa hồng cho nhân viên kinh doanh.

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Danh sách hợp đồng** | Quản lý hợp đồng với Khách hàng | Lưu thông tin từng hợp đồng: nội dung, giá trị, lịch xuất hóa đơn, lịch thu tiền. |
| **Phương án kinh doanh** | Khi bộ phận Kinh doanh lập đề xuất hoa hồng cho một hợp đồng | Liệt kê các bên hưởng hoa hồng (Nhân viên bán hàng, Quản lý kinh doanh, hoàn tiền cho khách, chia hoa hồng cho bên giới thiệu). Khi duyệt và thanh toán, hệ thống tự sinh phiếu kế toán hoa hồng. Nếu bên nhận hoa hồng không xuất hóa đơn hợp lệ (cá nhân không khấu trừ thuế TNCN, đại lý không thuộc doanh nghiệp), hệ thống tự đánh dấu **chi phí không được trừ thuế Thu nhập doanh nghiệp**. |
| **Hóa đơn cần ghi sổ** | Khi có hóa đơn đã xuất nhưng chưa hạch toán | Danh sách hóa đơn theo từng hợp đồng. |
| **Hóa đơn quá hạn cần đôn thúc** | Khi cần thông báo cho Nhân viên thu tiền | Hóa đơn quá hạn theo từng hợp đồng — phục vụ đôn thúc. |
| **Thu tiền theo hợp đồng** | Theo dõi thanh toán theo từng hợp đồng | Phiếu thu phân chia theo hợp đồng. |
| **Sổ hoa hồng Nhân viên kinh doanh (phải trả)** | Báo cáo hoa hồng phải trả cho Nhân viên kinh doanh | Phân biệt: đã hạch toán (đã sinh phiếu kế toán) và Đang chờ (hóa đơn đã thu nhưng phiếu hoa hồng chưa lập). |
| **Phải trả phía khách (hoàn tiền / chia hoa hồng / giới thiệu)** | Theo dõi phần phải trả ra ngoài doanh nghiệp | Hoàn tiền cho khách, chia hoa hồng cho bên thứ ba, phí giới thiệu. |
| **Công nợ theo hợp đồng** | Báo cáo công nợ phải thu chi tiết theo từng hợp đồng | Đã xuất hóa đơn - Đã thu = Còn phải thu, theo từng hợp đồng. |
| **Kỳ thu tiền quá hạn** | Khi có hợp đồng tính phí định kỳ (thuê bao) | Liệt kê các kỳ đã quá hạn của các hợp đồng định kỳ. |

---

## VII. Kho & Vật tư

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Cài đặt Phương án kinh doanh** | Cấu hình hoa hồng — tài khoản hạch toán, ngưỡng duyệt | Trang cấu hình tập trung cho phần Phương án kinh doanh. |
| **Nhập xuất kho** | Nhập, xuất, chuyển kho, hủy hàng | Phiếu nhập-xuất kho đa năng (sản xuất, hủy hàng hỏng, chuyển nội bộ). |
| **Lịch sử nhắc duyệt Phương án kinh doanh** | Khi cần kiểm tra ai đã được nhắc duyệt | Lưu lịch sử các thông báo nhắc duyệt. |
| **Kiểm kê kho** | Khi kiểm kê thực tế kho | So tồn thực tế với sổ — sinh phiếu điều chỉnh nếu có chênh lệch. |
| **Số lô** | Quản lý hàng theo lô (theo ngày nhập, hạn dùng) | Theo dõi từng lô nhập kho, hạn dùng. |
| **Số seri** | Quản lý hàng theo số seri (ví dụ thiết bị) | Theo dõi từng máy theo số seri. |
| **Báo cáo nhập xuất tồn** | Báo cáo theo từng mặt hàng và kho | Đầu kỳ + Nhập trong kỳ + Xuất trong kỳ = Tồn cuối kỳ. |
| **Báo cáo tuổi kho** | Khi cần phân tích hàng tồn lâu | Phân nhóm theo tuổi: dưới 30, 31-60, 61-90, 91-180, trên 180 ngày. |
| **Sổ chi tiết kho** | Sổ chi tiết theo từng mặt hàng | Từng dòng nhập-xuất theo thứ tự thời gian. |
| **Định mức tồn kho** | Khi cần thiết lập điểm đặt hàng lại | Gợi ý mức tối thiểu cần đặt hàng dựa trên lịch sử. |
| **Gói sản phẩm** | Khi bán hàng theo gói trọn | Định nghĩa một mã bán bằng nhiều mã xuất kho. |

---

## VIII. Tài sản cố định

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Danh sách** | Quản lý tài sản cố định | Thông tin từng tài sản: nguyên giá, ngày bắt đầu sử dụng, kỳ khấu hao, TK 211 / 214. Có ô đánh dấu **"Tài sản phúc lợi"** — nếu đánh dấu, phần khấu hao tự đánh dấu không được trừ thuế Thu nhập doanh nghiệp. |
| **Tính khấu hao** | Lịch khấu hao tự động hàng tháng | Lịch trích khấu hao tự lập khi tạo tài sản. Hệ thống tự đẩy bút toán Nợ TK 6424 (hoặc 6271 / 641…) / Có TK 2141 mỗi kỳ. |
| **Sửa chữa** | Khi tài sản cần sửa chữa | Lập phiếu sửa chữa, ghi nhận chi phí (Nợ TK 6427 / Có TK 111 hoặc 331). Nếu chi phí lớn, có thể vốn hóa làm tăng nguyên giá tài sản. |
| **Bàn giao Tài sản cố định** | Khi giao tài sản cho người sử dụng hoặc bộ phận | Phiếu bàn giao có hội đồng, biên bản. Theo dõi từng tài sản đang ở ai / bộ phận nào. |
| **Kiểm kê Tài sản cố định** | Định kỳ cuối năm hoặc cuối quý | Hệ thống tự nạp danh sách tài sản cố định theo địa điểm / bộ phận, Kế toán chỉ đánh dấu "có / không có / khác". Hiển thị giá trị sổ và giá trị thực kiểm. |
| **Thanh lý tài sản** | Khi bán hoặc loại bỏ tài sản | Phiếu thanh lý sinh phiếu kế toán: Nợ TK 214 (xóa khấu hao lũy kế), Nợ TK 811 (giá trị còn lại), Nợ TK 111/112 (thu thanh lý) / Có TK 211, Có TK 711 (thu nhập thanh lý), Có TK 33311 (thuế GTGT). |
| **Sổ S21-DN** | Sổ tài sản cố định theo Thông tư 99/2025 | Mẫu S21-DN chuẩn cho cơ quan thuế và kiểm toán. |
| **Lịch sử khấu hao** | Tra cứu lịch sử trích khấu hao | Theo từng tài sản / theo kỳ. |

---

## IX. Công cụ dụng cụ

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Danh sách Công cụ dụng cụ** | Quản lý Công cụ dụng cụ (giá trị nhỏ hơn tài sản cố định, thường dưới 30 triệu) | Khi ghi nhận, hệ thống tự sinh bút toán Nợ TK 242 (chi phí chờ phân bổ) / Có TK 153, đồng thời lập lịch phân bổ vào chi phí theo thời gian sử dụng (thường 12-36 tháng). Trạng thái: Đang sử dụng → Đã ghi giảm. |
| **Ghi giảm Công cụ dụng cụ** | Khi Công cụ dụng cụ hư hỏng, mất, hết sử dụng | Phiếu ghi giảm: phần còn chưa phân bổ đẩy thẳng chi phí (Nợ TK 6423 / Có TK 242). Hủy các kỳ phân bổ còn lại trong lịch. |
| **Bàn giao Công cụ dụng cụ** | Khi giao Công cụ dụng cụ cho người sử dụng | Cùng cơ chế với Bàn giao Tài sản cố định, phạm vi Công cụ dụng cụ. |
| **Kiểm kê Công cụ dụng cụ** | Định kỳ kiểm kê | Cùng cơ chế với Kiểm kê Tài sản cố định, phạm vi Công cụ dụng cụ. |
| **Sổ S22-DN** | Sổ theo dõi Công cụ dụng cụ theo Thông tư 99/2025 | Mẫu S22-DN chuẩn. |
| **Lịch phân bổ Công cụ dụng cụ (242 → 6423)** | Theo dõi tiến độ phân bổ Công cụ dụng cụ | Lịch hàng tháng — đã phân bổ bao nhiêu, còn lại bao nhiêu. |

---

## X. Tiền lương

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Bảng chấm công** | Ghi nhận chấm công nhân viên | Theo ngày, có / không / nghỉ phép. |
| **Bảng giờ công (theo dự án)** | Khi cần chia giờ làm theo dự án | Phục vụ tính giá thành công trình. |
| **Bảng lương** | Tính lương cuối tháng cho một đợt | Sinh phiếu lương cho từng nhân viên. |
| **Phiếu lương** | Chi tiết lương từng nhân viên | Lương cơ bản, phụ cấp, Bảo hiểm xã hội, thuế Thu nhập cá nhân, trừ tạm ứng, lương thực lĩnh. |
| **Cơ cấu lương** | Cấu hình mẫu lương | Ví dụ Lương cơ bản + Phụ cấp ăn + Phụ cấp đi lại - Bảo hiểm xã hội (8%) - Bảo hiểm y tế (1.5%) - thuế Thu nhập cá nhân. |
| **Thành phần lương** | Định nghĩa từng thành phần | Mỗi thành phần có công thức tính và ô đánh dấu "Không được trừ thuế Thu nhập doanh nghiệp" (ví dụ lương phúc lợi không có chứng từ rõ ràng). |
| **Gán Cơ cấu lương** | Gán mẫu cơ cấu cho từng nhân viên | Mỗi nhân viên một cấu trúc lương. |
| **Lương bổ sung** | Khi cần cộng hoặc trừ ngoài kỳ (thưởng đột xuất, phạt) | Phiếu lương bổ sung cho một hoặc nhiều nhân viên. |
| **Danh sách nhân viên** | Quản lý nhân viên | Thông tin cá nhân, hợp đồng, lương. |

---

## XI. Giá thành công trình & Dự án

Phần này phục vụ doanh nghiệp xây lắp, doanh nghiệp có dự án dài hạn, hoặc doanh nghiệp sản xuất theo đơn đặt hàng.

Theo Thông tư 99/2025, doanh nghiệp xây lắp **bắt buộc dùng TK 627** cho chi phí sản xuất chung — không được hạch toán thẳng vào TK 642. Hệ thống đã được thiết kế theo chuỗi TK 627 → 154 → 632.

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Phân bổ chi phí vào giá vốn** | Phân bổ chi phí phụ (vận chuyển, kiểm định, thuế nhập khẩu) vào giá vốn hàng nhập | Phiếu phân bổ tự chia phụ phí ra từng mặt hàng, làm tăng giá nhập kho (TK 156 / 152) tương ứng. |
| **Chi phí chờ phân bổ (TK 242)** | Báo cáo chi phí đã ghi TK 242 nhưng chưa phân bổ vào chi phí | Liệt kê các hóa đơn mua hàng đã ghi TK 242 chờ phân bổ, kèm tiến độ phân bổ đến đâu. |
| **Dự án — Giá thành** | Theo dõi giá thành từng công trình / dự án | Thông tin chung dự án và các giai đoạn nghiệm thu. Mỗi giai đoạn có ngày dự kiến xuất hóa đơn và giá. Khi đóng dự án, phần chi phí sản xuất kinh doanh dở dang (TK 154) còn lại sẽ chuyển ra giá vốn (TK 632) hoặc chi phí Quản lý doanh nghiệp (TK 642). |
| **Tiến độ xuất hóa đơn** | Khi cần theo dõi nghiệm thu xuất hóa đơn theo dự án | Liệt kê từng giai đoạn: ngày dự kiến, trạng thái, số ngày còn lại, giá xuất, hóa đơn liên kết. Phục vụ kế hoạch xuất hóa đơn. |
| **Kết chuyển chi phí sản xuất chung (627 → 154)** | Cuối kỳ, Kế toán phân bổ chi phí gián tiếp (lương quản lý công trường, khấu hao máy thi công…) ra các dự án | Nhập tỷ lệ phần trăm chia, hoặc chia theo định mức vật tư / giờ công. Khi duyệt, sinh phiếu kế toán Nợ TK 154 (theo từng dự án) / Có TK 627. |
| **Cài đặt phân bổ chi phí vào giá vốn** | Cấu hình tài khoản TK 156 con mặc định cho từng loại phụ phí | Ví dụ: phí vận chuyển vào TK 1562 (chi phí thu mua), thuế nhập khẩu vào TK 1561 (giá mua). |

---

## XII. Thuế

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Hoá đơn GTGT đầu vào** | Khi nhận hóa đơn điện tử từ Nhà cung cấp | Lấy về hóa đơn điện tử tự động từ nhà cung cấp dịch vụ hóa đơn điện tử (Mắt Bão, EasyInvoice…). Cũng có thể nhập thủ công. |
| **Hoá đơn GTGT đầu ra** | Khi xuất hóa đơn cho khách | Cùng chức năng với "Hoá đơn bán hàng". Tích hợp ký số và đẩy lên Tổng cục Thuế. |
| **Tờ khai thuế GTGT (01/GTGT)** | Khi lập tờ khai 01/GTGT hàng tháng hoặc quý | Tổng hợp hóa đơn bán và hóa đơn mua theo nhóm thuế suất (0%, 5%, 8%, 10%). Xuất file XML hoặc Excel để nộp lên hệ thống HTKK của Tổng cục Thuế. |
| **Mẫu thuế bán hàng** | Cấu hình bộ thuế GTGT đầu ra | Mỗi mức thuế suất một mẫu. |
| **Mẫu thuế mua hàng** | Cấu hình bộ thuế GTGT đầu vào | Tương tự. |
| **Mẫu thuế hàng hoá** | Cấu hình thuế theo từng mặt hàng (nếu khác mặc định) | Ví dụ hàng xuất khẩu 0%, dịch vụ 5%, hàng phổ thông 10%. |
| **[Đang phát triển] Kiểm tra Mã số thuế** | Tra cứu Mã số thuế Khách hàng / Nhà cung cấp qua cổng Tổng cục Thuế | Đang phát triển. |

---

## XIII. Tổng hợp & Khóa sổ

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Đánh giá lại ngoại tệ** | Cuối kỳ (tháng / quý / năm) khi doanh nghiệp có số dư ngoại tệ | Tự sinh phiếu kế toán Nợ / Có TK 413 (chênh lệch tỷ giá) cho từng tài khoản có gốc ngoại tệ. |
| **Phiếu khóa sổ kỳ** | Cuối năm, sau khi lập Báo cáo tài chính | Kết chuyển TK loại 5 (doanh thu), 7 (thu nhập khác), 6 (chi phí), 8 (chi phí khác) về TK 911, sau đó về TK 421 (Lợi nhuận chưa phân phối). Khóa kỳ kế toán. |
| **Định nghĩa kỳ kế toán** | Khi cấu hình kỳ kế toán cho phép ghi nhận | Ví dụ tháng 1/2026 đã khóa thì không cho phép thêm phiếu nào ngày 1/2026 nữa. |
| **Sổ nhật ký chung** | Mẫu S03a-DN — sổ nhật ký chung | Toàn bộ phiếu kế toán trong kỳ theo thứ tự thời gian. |
| **Sổ chi tiết tài khoản** | Mẫu S38-DN — sổ chi tiết theo từng tài khoản | Theo từng tài khoản và đối tượng (Khách hàng, Nhà cung cấp, Nhân viên, Dự án). |
| **Bảng cân đối số phát sinh** | Mẫu F01-DN — bảng cân đối số phát sinh | Mỗi tài khoản: Số dư đầu, Phát sinh Nợ kỳ, Phát sinh Có kỳ, Lũy kế Nợ, Lũy kế Có, Số dư cuối. Phục vụ kiểm tra cân đối và lập Báo cáo tài chính. |

---

## XIV. Báo cáo tài chính

Tất cả báo cáo theo Thông tư 99/2025/TT-BTC (có hiệu lực từ 01/01/2026).

| Báo cáo | Khi nào dùng | Mô tả |
|---|---|---|
| **Báo cáo tình hình tài chính (B01-DN)** | Cuối kỳ — Bảng cân đối kế toán (đã đổi tên theo Thông tư 99/2025) | Tài sản (ngắn hạn + dài hạn), Nợ phải trả (ngắn hạn + dài hạn), Vốn chủ sở hữu. Cấu trúc các dòng 100, 110, 111… theo mẫu B01-DN. |
| **Báo cáo kết quả hoạt động kinh doanh (B02-DN)** | Cuối kỳ | Doanh thu - Giá vốn = Lợi nhuận gộp - Chi phí bán hàng - Chi phí Quản lý doanh nghiệp + Doanh thu tài chính - Chi phí tài chính + Lợi nhuận khác - Chi phí khác - thuế Thu nhập doanh nghiệp = Lợi nhuận sau thuế. |
| **Báo cáo lưu chuyển tiền tệ (B03-DN)** | Cuối kỳ | Theo phương pháp gián tiếp: Lưu chuyển tiền từ Hoạt động kinh doanh / Hoạt động đầu tư / Hoạt động tài chính. |
| **Thuyết minh Báo cáo tài chính (B09-DN)** | Cuối năm — bắt buộc đi kèm Báo cáo tài chính | Sinh file Excel nhiều trang: chính sách kế toán, biến động tài sản cố định, vốn chủ, công nợ chi tiết… Kế toán chỉ cần kiểm tra và bổ sung diễn giải. |
| **Quyết toán thuế TNDN (Mẫu 03)** | Cuối năm — tờ khai Mẫu 03 thuế Thu nhập doanh nghiệp | Cấu trúc 19 dòng: A (Lợi nhuận kế toán) → B (điều chỉnh tăng / giảm) → C (Thu nhập chịu thuế) → D (Thuế Thu nhập doanh nghiệp phải nộp), kèm phân tích tỷ lệ thuế hiệu lực. Dòng **B4 (Chi phí không được trừ)** tự tổng hợp từ các phiếu đã đánh dấu "Không được trừ thuế Thu nhập doanh nghiệp". |
| **Chi phí không được trừ (B4)** | Khi cần xem chi tiết từng dòng chi phí đã loại khỏi tính thuế Thu nhập doanh nghiệp | Liệt kê tất cả các dòng đã đánh dấu "Không được trừ", kèm lý do (sáu nhóm: Không hóa đơn hợp lệ / Vượt định mức / Không liên quan sản xuất kinh doanh / Tiền phạt / Bên liên kết không có chứng từ chuyển giá / Khác). Có biểu đồ theo nhóm và tổng B4. |
| **Tư vấn — Chi phí không trừ thuế Thu nhập doanh nghiệp** | Khi Kế toán cần ôn lại quy định pháp luật | Bài tư vấn tiếng Việt thuần: căn cứ pháp lý (Nghị định 320/2025/NĐ-CP và Chuẩn mực kế toán Việt Nam số 17), phân biệt chênh lệch vĩnh viễn và chênh lệch tạm thời, sáu lý do thường gặp, sáu hiểu lầm phổ biến, câu hỏi thường gặp. |
| **Phân tích lợi nhuận (theo Trung tâm chi phí / Dự án)** | Khi cần phân tích lợi nhuận theo trung tâm chi phí hoặc dự án | Doanh thu - Chi phí theo từng phòng ban hoặc dự án — phục vụ kế toán quản trị. |
| **So sánh ngân sách (Thực tế và Kế hoạch)** | Khi doanh nghiệp có lập ngân sách hàng năm | So sánh phát sinh thực tế với ngân sách đã duyệt theo từng tài khoản và kỳ. Hiển thị phần trăm thực hiện và mức chênh lệch. |
| **Báo cáo lãi lỗ quản trị** | Báo cáo lãi lỗ theo cách trình bày quản trị (khác với Báo cáo tài chính chuẩn) | Có thể tùy chỉnh hiển thị theo nhóm chi phí (biến đổi / cố định, hoặc theo phòng ban). |
| **Tóm tắt Dự án** | Tổng quan tài chính từng dự án | Doanh thu - Chi phí = Lợi nhuận theo dự án, kèm tiến độ xuất hóa đơn. |
| **Cấu hình Mapping Báo cáo tài chính** | Khi cần điều chỉnh công thức tính từng dòng Báo cáo tài chính | Kế toán có thể sửa công thức tính dòng B01 / B02 / B03 nếu doanh nghiệp có tài khoản đặc thù. Hệ thống có sẵn mẫu chuẩn cho Doanh nghiệp lớn và Doanh nghiệp nhỏ thương mại — Kế toán có thể khôi phục mẫu gốc nếu lỡ sửa sai. |

---

## XV. Danh mục

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Hệ thống tài khoản** | Quản lý cây tài khoản | Theo Thông tư 99/2025 — chín loại tài khoản chính, cấp 1 đến 5. |
| **Khách hàng** | Quản lý Khách hàng | Thông tin: tên, Mã số thuế, địa chỉ, điều khoản thanh toán. |
| **Nhà cung cấp** | Quản lý Nhà cung cấp | Tương tự Khách hàng. |
| **Hàng hoá, vật tư** | Quản lý danh mục hàng | Mã hàng, tên, đơn vị tính, tài khoản doanh thu / giá vốn / kho mặc định. |
| **Kho** | Quản lý kho | Mỗi kho một tài khoản TK 152 / 156 con (nếu cần). |
| **Nhân viên** | Quản lý Nhân viên | Liên kết với phần Tiền lương. |
| **Định mức vật tư** | Cấu trúc nguyên vật liệu sản phẩm | Doanh nghiệp sản xuất / xây lắp cần — định nghĩa một sản phẩm cần các nguyên liệu gì, định mức bao nhiêu. |

---

## XVI. Thiết lập

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Mẫu hợp đồng** | Mẫu hợp đồng (file Word có chỗ điền) | Mỗi loại hợp đồng một mẫu — khi tạo hợp đồng mới chỉ điền các trường biến. |
| **Cây tài khoản** | Quản lý cây tài khoản theo cấu trúc Thông tư 99/2025 | Có thể thêm tài khoản con khi doanh nghiệp cần chi tiết hơn (ví dụ tách TK 1561 thành 15611, 15612). |
| **Cài đặt Hợp đồng** | Cấu hình hợp đồng — kỳ thanh toán mặc định, nhắc đáo hạn… | Áp dụng chung cho mọi hợp đồng. |
| **Nạp cây tài khoản** | Khi triển khai mới, nạp cây tài khoản từ Excel | Hỗ trợ nạp hàng loạt cây tài khoản. |
| **Mẫu quy tắc hoa hồng** | Mẫu tính hoa hồng cho từng loại Phương án kinh doanh | Ví dụ Nhân viên kinh doanh trực tiếp 5%, Quản lý kinh doanh 2%, hoàn tiền khách 3%. |
| **Năm tài chính** | Định nghĩa năm tài chính doanh nghiệp | Mặc định 01/01 đến 31/12. |
| **Cài đặt Phương án kinh doanh** | Cấu hình chung cho Phương án kinh doanh | Cùng nội dung với mục tương ứng bên Kho. |
| **Kỳ kế toán** | Định nghĩa kỳ kế toán | Cùng nội dung với mục tương ứng bên Tổng hợp. |
| **Lịch sử nhắc duyệt Phương án kinh doanh** | Lưu lịch sử các thông báo nhắc duyệt | Cùng nội dung với mục tương ứng bên Kho. |
| **Trung tâm chi phí** | Phân chia chi phí theo phòng ban hoặc bộ phận | Doanh nghiệp quy mô trung-lớn nên dùng để phân tích chi phí theo trung tâm chi phí. |
| **Dự án** | Quản lý dự án | Liên kết với phần Giá thành công trình. |
| **Ngân sách** | Lập ngân sách năm theo tài khoản và trung tâm chi phí / dự án | Để báo cáo So sánh ngân sách hoạt động được. |
| **Cài đặt kho** | Cấu hình chính sách kho — Nhập trước Xuất trước, định mức tồn… | Áp dụng chung cho mọi kho. |
| **Cài đặt kế toán** | Cấu hình trung tâm của hệ thống kế toán | Tài khoản chênh lệch, ngưỡng giá trị tài sản cố định, kho mặc định, quy tắc phân quyền theo vai trò. Đây là **màn hình quan trọng nhất khi triển khai** — Kế toán trưởng cần kiểm tra kỹ trước khi đưa vào vận hành. |

---

## XVII. Công cụ chuyển dữ liệu từ phần mềm cũ

| Chức năng | Khi nào dùng | Nó cho biết / cho phép làm |
|---|---|---|
| **Trang chuyển dữ liệu từ Misa** | Khi chuyển dữ liệu từ Misa sang hệ thống mới | Trang chính của chuyển dữ liệu: tải lên file xuất từ Misa (Excel), hệ thống tự đọc năm loại trang (Cây tài khoản / Số dư đầu kỳ / Khách hàng / Nhà cung cấp / Phiếu kế toán). Xem trước, kiểm tra, ghi nhận lô lớn vào hệ thống. |
| **Lịch sử các đợt chuyển dữ liệu** | Theo dõi các đợt chuyển dữ liệu đã chạy | Mỗi đợt là một bản ghi với tám trạng thái: Mới lập → Đã tải lên → Đã đọc → Đã duyệt → Đang ghi nhận → Đã ghi nhận (hoặc Đang hoàn tác → Đã hoàn tác). Hỗ trợ hoàn tác toàn bộ nếu phát hiện sai sau khi ghi nhận. |

---

## Các tính năng có mặt trong nhiều màn hình

Một số tính năng không có "menu" riêng nhưng xuất hiện trong nhiều màn hình:

### 1. Đánh dấu "Không được trừ thuế Thu nhập doanh nghiệp"

**Khi nào dùng**: Khi Kế toán phát sinh chi phí mà luật thuế **không cho phép trừ** khi tính thuế Thu nhập doanh nghiệp. Có sáu lý do thường gặp (theo Nghị định 320/2025/NĐ-CP):

| Lý do | Ví dụ |
|---|---|
| Không hóa đơn hợp lệ | Mua hàng cá nhân không có hóa đơn GTGT, hóa đơn sai quy cách |
| Vượt định mức quy định | Chi phí tiếp khách vượt 5% doanh thu, lương vượt định mức |
| Không liên quan sản xuất kinh doanh | Chi phí cá nhân của lãnh đạo, chi tài trợ ngoài kế hoạch |
| Tiền phạt (thuế / Bảo hiểm xã hội / hợp đồng) | Phạt chậm nộp thuế, phạt vi phạm hợp đồng |
| Bên liên kết không có chứng từ chuyển giá | Giao dịch với bên liên kết không có Hồ sơ xác định giá giao dịch |
| Khác | Trường hợp đặc thù, Kế toán ghi rõ trong ghi chú |

Đánh dấu này xuất hiện trên:
- **Dòng phiếu kế toán** (mỗi dòng Nợ / Có có ô đánh dấu và ô chọn lý do)
- **Dòng hóa đơn mua hàng**
- **Dòng yêu cầu chi phí**
- **Thành phần lương** (ví dụ trợ cấp phúc lợi)
- **Tài sản** (ô đánh dấu "Tài sản phúc lợi" — khấu hao tự đánh dấu)

Cuối năm, **báo cáo "Chi phí không được trừ (B4)"** tự tổng hợp tất cả các dòng đã đánh dấu, đẩy vào dòng B4 của **Quyết toán thuế Thu nhập doanh nghiệp (Mẫu 03)**. Kế toán không phải tính tay.

**Khuyến nghị**: Đánh dấu ngay khi nhập phiếu (chứ không đợi cuối năm) — nhanh hơn, không sót, không phải truy ngược lại.

### 2. Phân quyền theo chi nhánh

Doanh nghiệp có nhiều chi nhánh có thể cấu hình:
- Kế toán chi nhánh A chỉ thấy và lập phiếu thu-chi của chi nhánh A
- Kế toán trụ sở thấy toàn bộ
- Quản lý cấp trên thấy hợp nhất

Cài đặt qua màn hình **Cài đặt kế toán** → bảng phân quyền theo vai trò.

### 3. Báo cáo theo Thông tư 99/2025

Mọi báo cáo (B01 / B02 / B03 / B09 / S03a / S03b / S21 / S22-DN) đều đã cập nhật theo **Thông tư 99/2025/TT-BTC** có hiệu lực từ 01/01/2026. Hệ thống không hỗ trợ định dạng cũ của Thông tư 200/2014 — nếu cần báo cáo theo Thông tư 200 cho năm tài chính 2025, vui lòng làm việc với đội triển khai.

### 4. Sổ kế toán bắt buộc

Theo Thông tư 99/2025, doanh nghiệp phải lưu các sổ kế toán sau:

| Sổ | Mã mẫu | Có sẵn trong hệ thống |
|---|---|---|
| Sổ nhật ký chung | S03a-DN | Có |
| Sổ cái | S03b-DN | Có (in được từng tài khoản) |
| Sổ chi tiết tài khoản | S38-DN | Có |
| Sổ quỹ tiền mặt | S06-DN | Có |
| Sổ tài sản cố định | S21-DN | Có |
| Sổ theo dõi Công cụ dụng cụ | S22-DN | Có |

---

## Cách tiếp cận khuyến nghị cho Kế toán mới làm quen

1. **Tuần đầu**: Quen với màn hình **Tổng quan** và cách lập **Phiếu thu / Phiếu chi**, xem **Sổ quỹ tiền mặt** và **Sổ Tài khoản ngân hàng**.
2. **Tuần thứ hai và thứ ba**: Lập **Hóa đơn bán hàng / Hóa đơn mua hàng**, theo dõi **Công nợ phải thu / phải trả**.
3. **Tháng đầu**: Quen với **Kiểm kê quỹ**, **Đánh giá lại ngoại tệ** (nếu doanh nghiệp có ngoại tệ), **Khấu hao tài sản cố định / Phân bổ Công cụ dụng cụ**.
4. **Cuối kỳ đầu tiên**: Chạy thử **Bảng cân đối số phát sinh**, **B01 / B02 / B03-DN**. Nếu có chi phí không hợp lệ thì đánh dấu **"Không được trừ thuế Thu nhập doanh nghiệp"** ngay khi nhập.
5. **Tham khảo bài tư vấn**: Trong các báo cáo Thu nhập doanh nghiệp có nút **Trợ giúp** mở các bài tư vấn pháp lý tiếng Việt thuần.

---

## Khi cần hỗ trợ

| Loại vướng mắc | Tham khảo |
|---|---|
| Nghiệp vụ kế toán (cách hạch toán, công thức tính) | Thông tư 99/2025/TT-BTC, Chuẩn mực kế toán Việt Nam |
| Cách sử dụng tính năng | Các bài viết trong **Trợ giúp** trên hệ thống |
| Lỗi kỹ thuật hoặc cần thêm tính năng | Liên hệ đội triển khai |
| Quy định thuế | Nghị định 320/2025/NĐ-CP (Thu nhập doanh nghiệp), Thông tư 80/2021/TT-BTC (Giá trị gia tăng), Thông tư 99/2025/TT-BTC (Kế toán) |

---

*Tài liệu này lập ngày 25/05/2026 trên cơ sở phiên bản hệ thống đang vận hành. Sẽ cập nhật theo các tính năng mới.*
