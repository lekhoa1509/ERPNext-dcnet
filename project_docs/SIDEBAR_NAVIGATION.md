# Cấu trúc Sidebar Điều Hướng — DCNET Flow (Nhật Minh)

> Căn cứ: `Tính năng - nội bộ DEV - Nhật Minh - Detail Schedule.csv` | `Danh sách báo cáo thống nhất.csv` | `QUY_TRINH_ERP_PHAN_TICH.md`
> Cập nhật: 2026-03-16

---

## 🛒 MUA HÀNG

### Yêu cầu mua hàng
- [Tạo phiếu yêu cầu mua hàng](/desk/material-request/new-material-request) — Yêu cầu từ kho/bộ phận khi tồn xuống dưới mức tối thiểu *(Nguồn: QUY_TRINH)*
- [Danh sách phiếu yêu cầu mua hàng](/desk/material-request) — Theo dõi trạng thái phiếu yêu cầu *(Nguồn: QUY_TRINH)*

### Đơn mua hàng (PO)
- [Danh sách đơn mua hàng](/desk/purchase-order) — #06 Theo dõi PO theo số PO
- [Tạo đơn mua hàng](/desk/purchase-order/new-purchase-order) — #04 Số đơn tự động + NCC + Kho nhận + Ngày đặt
- [Chi tiết đơn mua hàng](/desk/purchase-order) — #05 Model + SKU + Số lượng + Giá mua
- [Theo dõi thực hiện mua hàng](/desk/purchase-order) — #08 Đã đặt + Đã nhận một phần (%) + Đã nhận đủ
- [Lịch đặt hàng cố định theo mùa vụ](/desk/purchase-order) — Nhắc nhở tự động: Gậy tháng 9–10, Hàng quần áo & phụ kiện hàng tháng, Hàng JP tháng 6–7/11–12 *(Nguồn: QUY_TRINH)*
- [Quy trình duyệt đơn mua hàng](/desk/purchase-order) — Duyệt đa cấp: GĐ Kinh Doanh → Ban Lãnh Đạo *(Nguồn: QUY_TRINH)*

### Phiếu nhập kho
- [Danh sách phiếu nhập](/desk/purchase-receipt) — #71 Trạng thái: Nháp → Chờ duyệt → Đã nhập kho
- [Tạo phiếu nhập (từ đơn mua hàng)](/desk/purchase-receipt) — #07 Sinh lệnh nhập từ PO + Nhập một phần / nhiều lần
- [Nhập hàng theo lô](/desk/purchase-receipt) — #09 Mã lô + Ngày nhập + Gắn với PO
- [Nhập hàng theo số sê-ri](/desk/purchase-receipt) — #10 Số sê-ri duy nhất + Quét sê-ri khi nhập
- [Nhập hàng theo mã vạch](/desk/purchase-receipt) — #11 Gán mã vạch + Nhập kho bằng quét mã
- [Khai báo vòng đời sản phẩm](/desk/purchase-receipt) — #12 6 tháng / 1 năm / 2 năm + Tính từ ngày nhập
- [Phiếu phân bổ chi phí nhập khẩu](/desk/landed-cost-voucher) — Phân bổ thuế NK, phí vận chuyển, phụ phí vào giá vốn sau khi nhập kho *(Nguồn: QUY_TRINH — Bắt buộc)*
- [Biên bản kiểm nhận hàng](/desk/purchase-receipt) — Mẫu in: Biên bản kiểm tra số lượng/chất lượng hàng nhập, xử lý sai lệch *(Nguồn: QUY_TRINH)*

### Nhà cung cấp
- [Danh mục nhà cung cấp](/desk/supplier) — #42 Mã + Tên + Nhóm + Điều khoản thanh toán
- [Bảng giá nhà cung cấp](/desk/price-list) — #43 Giá theo model/SKU + Hiệu lực giá
- [Báo giá nhà cung cấp](/desk/supplier-quotation) — #65 Ưu đãi: Chiết khấu % + Chiết khấu tiền + Quà tặng

### Thanh toán mua hàng
- [Thông tin nguồn tiền](/desk/mode-of-payment) — #67 Quỹ tiền mặt / Tài khoản ngân hàng
- [Phương thức thanh toán](/desk/mode-of-payment) — #68 Tiền mặt + Chuyển khoản + Công nợ
- [Theo dõi thanh toán đơn mua](/desk/purchase-order) — #69 Đã thanh toán + Thanh toán một phần + Còn nợ
- [Đính kèm chứng từ](/desk/purchase-receipt) — #70 Hóa đơn NCC + Phiếu giao hàng + Hợp đồng

### Danh mục & Cài đặt
- [Hình ảnh sản phẩm](/desk/item) — #66 Nhập ảnh theo model + Quy tắc đặt tên ảnh

### Báo cáo mua hàng
- [Lịch sử mua hàng](/desk/purchase-order) — #72 Theo NCC + Theo PO + Theo SP
- [Phân tích mua hàng](/desk/query-report/Purchase%20Analytics) — #73 Giá mua bình quân + NCC tốt nhất + Chi phí mua
- [BC-01 Theo dõi mua hàng và dự kiến bán](/desk/query-report/Purchase%20Order%20Analysis) — Theo dõi PO + dự kiến bán ra theo thuộc tính chi tiết (Người yêu cầu: Hạnh) *(Nguồn: Danh sách BC)*
- [BC-02 Tổng hợp theo dõi đơn hàng](/desk/query-report/Purchase%20Order%20Analysis) — Số lượng trên đơn mua + đơn bán (Người yêu cầu: Hạnh) *(Nguồn: Danh sách BC)*
- [BC-03 Theo dõi kế hoạch mua hàng](/desk/query-report/Purchase%20Order%20Analysis) — Nguồn từ đơn mua + phiếu nhập, nhóm theo Nhóm SP→Danh mục (Người yêu cầu: Hạnh + Dung) *(Nguồn: Danh sách BC)*
- [BC-04 Dự kiến chia hàng theo lệnh](/desk/query-report/Purchase%20Receipt%20Item%20Report) — Phân bổ dự kiến từ lệnh nhập + phiếu chia hàng (Người yêu cầu: Hạnh + Dung) *(Nguồn: Danh sách BC)*
- [BC-05 So sánh kế hoạch và đơn hàng](/desk/query-report/Purchase%20Order%20Analysis) — Kế hoạch mua vs thực tế đặt hàng (Người yêu cầu: Hạnh + Dung) *(Nguồn: Danh sách BC)*
- [BC-12 Tổng hợp nhập kho](/desk/query-report/Stock%20Balance) — Nhóm theo năm / Nhóm SP→Danh mục (Người yêu cầu: Dung) *(Nguồn: Danh sách BC)*
- [BC-13 Theo dõi đặt hàng Gậy](/desk/query-report/Purchase%20Order%20Analysis) — Theo dõi đơn mua riêng dòng gậy golf (Người yêu cầu: Hạnh) *(Nguồn: Danh sách BC)*
- [BC-14 Theo dõi đặt hàng Quần áo & Phụ kiện](/desk/query-report/Purchase%20Order%20Analysis) — Theo dõi đơn mua riêng dòng quần áo/phụ kiện (Người yêu cầu: Hạnh) *(Nguồn: Danh sách BC)*

---

## 💰 BÁN HÀNG

### Báo giá bán
- [Danh sách báo giá](/desk/quotation) — Báo giá bán cho đại lý B2B *(Nguồn: QUY_TRINH)*
- [Tạo báo giá](/desk/quotation/new-quotation) — Báo giá → Đơn bán hàng *(Nguồn: QUY_TRINH)*

### Đơn bán hàng (SO)
- [Danh sách đơn hàng](/desk/sales-order) — #55 Danh sách + Loại đơn (Vật dụng, Fitting, Coaching, Thu cũ) + 6 bộ lọc
- [Tạo đơn hàng Vật dụng](/desk/sales-order/new-sales-order) — #56 Biểu mẫu 13 trường + 2 loại (Bán lẻ, Bán buôn)
- [Kiểm tra tồn kho khi tạo đơn](/desk/sales-order) — #57 Kiểm tra tồn + Hiển thị số lượng theo kho
- [Xem chi tiết đơn hàng](/desk/sales-order) — #60 Xem đơn + Bảo hành + Công nợ
- [Cập nhật đơn hàng](/desk/sales-order) — #61 Cập nhật đơn + Chuyển kho xử lý
- [Nhập đơn hàng từ Excel](/desk/sales-order) — #58 Nhập từ file Excel
- [Xuất đơn hàng ra Excel](/desk/sales-order) — #59 Xuất ra file Excel
- [Đề xuất mua lại / Bán chéo](/desk/sales-order) — #62 Tự động cập nhật trạng thái + Phản hồi + Gợi ý mua lại

### Bán lẻ
- [Bảng giá bán lẻ](/desk/price-list) — #78 Cập nhật giá bán cho khách lẻ
- [Chính sách chiết khấu bán lẻ](/desk/pricing-rule) — #79 Thêm/xóa/sửa + Đính kèm file
- [Hóa đơn bán lẻ](/desk/sales-invoice) — #80 Lập phiếu + Tự động tính chiết khấu + Thẻ thanh toán + Xuất HĐĐT

### Bán buôn
- [Kế hoạch bán hàng theo năm](/desk/sales-person) — #112 Cập nhật kế hoạch theo năm cho từng khách hàng
- [Bảng giá niêm yết](/desk/price-list) — #113 Cập nhật giá bán + Đính kèm file quyết định giá
- [Chính sách chiết khấu bán buôn](/desk/pricing-rule) — #114 Tỷ lệ chiết khấu theo KH + SP + Đính kèm file
- [Đơn đặt hàng bán](/desk/sales-order) — #115 Biểu mẫu 13 trường + Tự động tính tiền từ bảng giá + Chiết khấu
- [Kiểm tra tồn kho trước khi xuất](/desk/sales-order) — #116 Kiểm tra tồn trước khi xuất hàng
- [Phiếu giao hàng](/desk/delivery-note) — #117 Kế thừa từ đơn hàng + Kiểm tra công nợ
- [Kiểm tra hạn mức công nợ](/desk/customer) — #118 Công nợ thực tế + dự kiến + số hóa đơn quá hạn
- [Cảnh báo công nợ quá hạn](/desk/customer) — #119 Tự động cảnh báo + Yêu cầu duyệt Kế toán trưởng nếu vượt hạn
- [Hóa đơn bán buôn](/desk/sales-invoice) — #120 Kế thừa từ phiếu giao hàng + Tự động lấy giá
- [Hàng bán bị trả lại](/desk/sales-return) — #121/#122 Lệnh nhập trả + Kiểm tra số sê-ri trên hóa đơn
- [Tính thưởng đạt kế hoạch doanh số](/desk/sales-invoice) — #123 Tính chiết khấu khuyến mại + Công nợ KH + Ghi nhận phiếu thu

### Thu cũ (Trade-in)
- [Danh sách đơn thu cũ](/desk/trade-in-order) — #124 Danh sách + Bộ lọc
- [Tạo đơn thu cũ](/desk/trade-in-order/new-trade-in-order) — #125 SP cũ (tên, thương hiệu, tình trạng, giá, ảnh) + SP mới + Phiếu ưu đãi
- [Trạng thái đơn thu cũ](/desk/trade-in-order) — #126 7 trạng thái: Mới → Kiểm tra → Định giá → KH xác nhận → Xử lý → Hoàn thành/Hủy
- [Chi tiết đơn thu cũ](/desk/trade-in-order) — #127 Thông tin KH + SP cũ + SP mới + Chi tiết thanh toán + Lịch sử
- [Cập nhật đơn thu cũ](/desk/trade-in-order) — #128 SP cũ + Giá thu + SP mới + Phiếu ưu đãi
- [Quy trình kiểm tra & định giá SP cũ](/desk/trade-in-order) — #129 Danh sách kiểm tra + Ảnh + Đề xuất giá + Quản lý duyệt
- [Tích hợp kho thu cũ](/desk/stock-entry) — #130 Nhập SP cũ + Xuất SP mới + Tự động cập nhật tồn kho
- [Báo cáo thu cũ](/desk/query-report/Trade-in%20Report) — #131 Tổng đơn + Doanh thu chênh lệch + Giá trị SP cũ + BC chi nhánh/NV
- [Thống kê thu cũ trên Dashboard](/desk/dashboard) — #132 Số đơn + Giá trị chênh lệch + SP cũ + Top SP

### Quản lý bảng giá
- [Danh sách bảng giá](/desk/price-list) — #99 Danh sách + Trạng thái + Chi nhánh + Nhãn KH
- [Tạo bảng giá](/desk/price-list/new-price-list) — #100
- [Xem bảng giá](/desk/price-list) — #101
- [Cập nhật bảng giá](/desk/price-list) — #102 Thời gian + Chi nhánh + Nhãn KH + Mặc định
- [Xóa bảng giá](/desk/price-list) — #103

### Quản lý khách hàng
- [Danh sách khách hàng](/desk/customer) — #104 Danh sách + Ẩn/hiện cột + Nhãn + 10 bộ lọc
- [Chi tiết khách hàng](/desk/customer) — #105 Thông tin + Công nợ + Lịch sử giao dịch + Điểm + Hàng đã mua + Bảng giá
- [Cập nhật khách hàng](/desk/customer) — #106 Cập nhật thông tin + Chiết khấu theo danh mục SP + Lịch chăm sóc
- [Nguồn khách hàng](/desk/lead-source) — #107 Thêm/xóa/sửa
- [Nhập khách hàng từ Excel](/desk/customer) — #110 Nhập từ file Excel
- [Xuất khách hàng ra Excel](/desk/customer) — #111 Xuất ra file Excel

### Kết nối sàn thương mại điện tử
- [Đồng bộ Shopee / TikTok / Lazada / Website](/desk/ecommerce-integration) — #74 Kết nối nền tảng TMĐT, đồng bộ đơn hàng 2 chiều *(T3 - 31/03)*
- [Danh sách đơn giao vận](/desk/shipment) — #168 Danh sách đơn giao vận + Bộ lọc theo trạng thái *(T5)*
- [Liên kết Viettel Post / GHTK](/desk/shipment) — #169 Tạo đơn CRM→VP + Đồng bộ mã/dịch vụ/giá/trạng thái *(T5)*
- [Đồng bộ danh mục khách hàng](/desk/customer) — #170 Đồng bộ khách hàng giữa CRM và Website (2 chiều) *(T5)*
- [Đồng bộ danh mục hàng hóa](/desk/item) — #171 Đồng bộ danh mục SP (hình ảnh, mô tả, giá) CRM→Website *(T5)*
- [Đồng bộ tồn kho thời gian thực](/desk/item) — #174 Đồng bộ tồn kho khả dụng → Website *(T5)*
- [Đồng bộ đơn hàng từ Website](/desk/sales-order) — #173 Tự động tạo đơn bán từ Website + Cập nhật trạng thái *(T5)*

### Quản lý Chi nhánh
- [Danh sách Chi nhánh](/desk/branch) — #87 Danh sách + tìm kiếm/lọc *(T4 - 30/04)*
- [Tạo Chi nhánh](/desk/branch/new-branch) — #88 Tên + Địa chỉ + SĐT + Email + Gán kho hàng *(T4)*
- [Chi tiết Chi nhánh](/desk/branch) — #89 Xem thông tin + Kho hàng liên kết + Danh sách nhân viên *(T4)*
- [Cập nhật Chi nhánh](/desk/branch) — #90 *(T4)*
- [Xóa Chi nhánh](/desk/branch) — #91 *(T4)*

### Quản lý Nhân viên
- [Danh sách Nhân viên](/desk/employee) — #92 Danh sách + tìm kiếm/lọc *(T4 - 30/04)*
- [Tạo Nhân viên](/desk/employee/new-employee) — #93 Tạo đơn lẻ / hàng loạt *(T4)*
- [Chi tiết Nhân viên](/desk/employee) — #94 Xem chi tiết *(T4)*
- [Cập nhật Nhân viên](/desk/employee) — #95 *(T4)*
- [Xóa Nhân viên](/desk/employee) — #96 *(T4)*
- [Nhập Nhân viên từ Excel](/desk/employee) — #97 Nhập từ file Excel *(T4)*
- [Xuất Nhân viên ra Excel](/desk/employee) — #98 Xuất ra file Excel *(T4)*
- [Hoa hồng nhân viên](/desk/sales-person) — Tính hoa hồng Fitting/Coaching/Bán hàng theo nhân viên kinh doanh *(Nguồn: QUY_TRINH)*

### Danh mục bán hàng
- [Danh mục đối tượng KH/NCC](/desk/customer) — #75 Mã + Tên + Loại + Địa chỉ + MST + Tài khoản ngân hàng
- [Danh mục vật tư hàng hóa](/desk/item) — #76 Mã + Tên + Đơn vị tính + Nhóm sản phẩm + Màu sắc + Danh mục
- [Kế hoạch doanh số năm](/desk/sales-person) — #77 Nhập giá trị doanh số tiêu thụ theo kế hoạch của từng KH

### Chính sách bán hàng
- [Kế hoạch bán hàng](/desk/sales-person) — #81 Thêm/xóa/sửa + Danh sách
- [Chính sách chiết khấu](/desk/pricing-rule) — #82 Thêm/xóa/sửa + Danh sách
- [Hàng trả lại](/desk/sales-return) — #84 Thêm/xóa/sửa + Danh sách
- [Tính thưởng doanh số](/desk/sales-person) — #85 Thêm/xóa/sửa + Danh sách + Quy trình 3 bước + Tính theo quy tắc
- [Phiếu ưu đãi (Voucher)](/desk/coupon-code) — #86 Danh sách + Chi tiết + Tạo + Xóa

### Báo cáo bán hàng
- [Phân tích bán hàng](/desk/query-report/Sales%20Analytics) — #44 Số lượng bán + Theo thời gian + Theo kênh bán
- [Doanh số theo đại lý](/desk/query-report/Sales%20Analytics) — #45 Doanh số từng đại lý + Sản lượng bán
- [Luân chuyển hàng hóa](/desk/query-report/Stock%20Ageing) — #46 Tốc độ bán + Thời gian lưu kho
- [Tổng hợp theo dõi đơn hàng](/desk/query-report/Sales%20Order%20Analysis) — #133 Tổng đơn + Theo cửa hàng + Theo trạng thái
- [Doanh số theo thời gian](/desk/query-report/Sales%20Analytics) — #137 Theo ngày/tuần/tháng + chi nhánh + nhãn KH + nguồn KH + sỉ/lẻ + top 10 SP
- [Báo cáo khách hàng](/desk/query-report/Customer%20Acquisition%20and%20Loyalty) — #136 Đơn Lead + Top KH doanh thu + KH mới + Mức độ hài lòng
- [Báo cáo quản trị](/desk/query-report/Sales%20Analytics) — #134/#135 Theo thời gian + SP + Đại lý + Xuất Excel/PDF
- [Báo cáo nhân viên — 4 chỉ số](/desk/query-report/Sales%20Person%20Commission%20Summary) — #109 Tỉ lệ chốt đơn + Số đơn + Doanh thu theo NV + Hiệu suất *(T4)* *(Nguồn: Detail Schedule)*
- [BC-06 Tổng hợp theo dõi đơn — Nhật Minh](/desk/query-report/Sales%20Order%20Analysis) — Tổng hợp đơn hàng riêng cho Nhật Minh (Người yêu cầu: Dung) *(Nguồn: Danh sách BC)*
- [BC-09 Bán hàng theo đại lý (TM)](/desk/query-report/Sales%20Analytics) — Doanh số + sản lượng từng đại lý của TM (Người yêu cầu: Chị Ngân) *(Nguồn: Danh sách BC)*
- [BC-11 Tổng hợp bán hàng](/desk/query-report/Sales%20Analytics) — Nhóm theo năm / Nhóm SP→Danh mục, lọc theo cửa hàng (Người yêu cầu: Dung) *(Nguồn: Danh sách BC)*

---

## 📦 KHO

### Quản lý kho
- [Danh sách kho](/desk/warehouse) — #47 Mã kho + Tên kho + Địa chỉ + NV phụ trách + Trạng thái
- [Vị trí kho (dạng cây)](/desk/warehouse) — #48 Khu vực + Kệ + Ô/Vị trí + Gán vị trí cho SP
- [Danh mục vật tư hàng hóa trong kho](/desk/stock-ledger) — #49 Mã SP + Model + SKU + Nhóm SP + Tồn kho

### Nhập – Xuất – Điều chuyển
- [Phiếu nhập kho](/desk/purchase-receipt) — #25 Nhập từ NCC + Nhập điều chuyển + Nhập trả hàng
- [Phiếu xuất kho / Phiếu giao hàng](/desk/delivery-note) — #26 Xuất bán hàng + Xuất điều chuyển + Xuất hao hụt
- [Sổ cái kho](/desk/stock-ledger) — #27 Nhập xuất theo mã SP + Theo kho + Theo lô + Theo vị trí
- [Điều chuyển kho (phiếu kho)](/desk/stock-entry) — #32 Kho đi / kho đến + SP / lô / số sê-ri
- [Điều chuyển kho liên công ty TM → NM](/desk/stock-entry) — Điều chuyển nội bộ giữa Kho TM và Kho NM *(Nguồn: QUY_TRINH — Bắt buộc)*
- [Phân bổ hàng trước nhập](/desk/purchase-order) — Dự kiến chia hàng từ đơn mua trước khi hàng về, đặt giữ số lượng theo đại lý *(Nguồn: QUY_TRINH)*
- [Biên bản kiểm nhận hàng (mẫu in)](/desk/purchase-receipt) — Mẫu in biên bản kiểm tra số lượng/chất lượng khi nhập, xử lý sai lệch *(Nguồn: QUY_TRINH)*

### Quản lý theo mùa vụ
- [Theo dõi hàng theo mùa vụ](/desk/item) — Trường tùy chỉnh "Mùa vụ" (SS/FW + năm) trên sản phẩm/lô: phân biệt hàng Xuân/Hè vs Thu/Đông trong kho và báo cáo *(Nguồn: QUY_TRINH)*
- [Lọc báo cáo theo mùa vụ](/desk/query-report/Stock%20Balance) — Lọc tồn kho / nhập xuất tồn theo mùa vụ *(Nguồn: QUY_TRINH)*

### Quản lý lô & Số sê-ri
- [Quản lý theo lô](/desk/batch) — #23 Mã lô + Ngày nhập + Vòng đời SP + Tồn theo lô
- [Quản lý theo số sê-ri](/desk/serial-no) — #24 Số sê-ri + Trạng thái (tồn/ký gửi/đã bán) + Lịch sử
- [Mã vạch sản phẩm](/desk/barcode-label) — #29 Gán mã vạch cho SP/số sê-ri + Quét khi nhập–xuất
- [Tạo tem sản phẩm](/desk/item) — #30 Tem mã SP + Tem số sê-ri + Tem lô
- [In tem](/desk/item) — #31 In đơn chiếc + In hàng loạt + Tùy chỉnh mẫu tem

### Tồn kho & Kiểm kê
- [Theo dõi tồn kho dự kiến](/desk/query-report/Stock%20Projected%20Qty) — #28 Tồn thực tế + Tồn khả dụng + Tồn giữ
- [Giữ hàng theo đơn](/desk/sales-order) — #50 Đặt giữ tồn khi tạo đơn bán + Hoàn tồn khi hủy đơn
- [Kiểm kê kho](/desk/stock-reconciliation) — #51 Theo kho + Theo vị trí + So sánh thực tế & hệ thống
- [Điều chỉnh kho](/desk/stock-reconciliation) — #52 Thừa/thiếu + Ghi nhận lý do
- [Cảnh báo tồn kho thấp / hết vòng đời](/desk/query-report/Batch%20Item%20Expiry%20Status) — #53 Tồn thấp (MIN) + Sắp hết vòng đời
- [Lịch sử xuất nhập kho](/desk/query-report/Stock%20Ledger) — #54 Nhập + Xuất + Điều chuyển + Người thao tác

### Báo cáo kho
- [Nhập xuất tồn theo số sê-ri/lô](/desk/query-report/Serial%20No%20and%20Batch%20Traceability) — #33 Theo kho + Theo SP + Theo lô
- [Báo cáo theo số sê-ri](/desk/query-report/Serial%20No%20Ledger) — #34 Số sê-ri tồn + Số sê-ri đã bán
- [Tồn kho khả dụng](/desk/query-report/Stock%20Projected%20Qty) — #35 Tồn thực tế vs tồn giữ
- [Vòng đời sản phẩm / Hết hạn lô](/desk/query-report/Batch%20Item%20Expiry%20Status) — #36 Còn 60 ngày + Còn 45 ngày
- [Phân tích hàng bán nhanh/chậm](/desk/query-report/Stock%20Ageing) — #37/#19 Hàng bán nhanh/chậm + Hàng cần giảm giá
- [Tồn kho theo từng kho](/desk/query-report/Warehouse%20Wise%20Stock%20Balance) — #38a Tồn kho theo từng kho/chi nhánh
- [Giá trị tồn kho](/desk/query-report/Stock%20Balance) — #38b Giá trị tồn theo SP + Theo kho
- [SP dưới mức tồn kho tối thiểu](/desk/query-report/Item%20Shortage%20Report) — #38c SP cần đặt hàng bổ sung
- [Sổ cái kho chi tiết](/desk/query-report/Stock%20Ledger) — #54 Chi tiết nhập xuất tồn
- [Hàng điều chuyển](/desk/query-report/Stock%20Balance) — #21 Điều chuyển giữa kho + Điều chuyển cho đại lý
- [Hàng thanh lý / chiến dịch giảm giá](/desk/query-report/Stock%20Ageing) — #22 Chiến dịch giảm giá + Thanh lý
- [Hàng sắp hết vòng đời](/desk/query-report/Batch%20Item%20Expiry%20Status) — #20 Còn 60 ngày + Còn 45 ngày
- [BC-07 Nhập xuất tồn chi tiết — Nhật Minh](/desk/query-report/Stock%20Ledger) — 3 bố cục (số lượng / giá trị / cả hai), 2 chế độ xem (Nhóm SP→Danh mục→Mã / Nhóm SP→Danh mục), giá trị theo bảng giá TM × tỷ lệ chiết khấu NM (Người yêu cầu: Dung) *(Nguồn: Danh sách BC)*
- [BC-08 Nhập xuất tồn chi tiết — TM](/desk/query-report/Stock%20Ledger) — Tương tự BC-07 cho TM (Người yêu cầu: Chị Ngân) *(Nguồn: Danh sách BC)*
- [BC-10 Tổng hợp tồn kho](/desk/query-report/Stock%20Balance) — Nhóm theo năm/Nhóm SP→Danh mục, giá trị = SL tồn × giá TM niêm yết × tỷ lệ chiết khấu NM, cho phép loại trừ kho (Người yêu cầu: Dung) *(Nguồn: Danh sách BC)*

---

## 🏦 KẾ TOÁN

### Giao dịch liên công ty (TM ↔ NM)
- [Hóa đơn bán liên công ty TM → NM](/desk/sales-invoice) — TM xuất hóa đơn bán cho NM thay vì điều chuyển kho, tự động tạo hóa đơn mua phía NM *(Nguồn: QUY_TRINH — Bắt buộc)*
- [Hóa đơn mua liên công ty (NM từ TM)](/desk/purchase-invoice) — NM nhận hóa đơn mua từ TM, tự động liên kết với hóa đơn bán của TM *(Nguồn: QUY_TRINH — Bắt buộc)*
- [Cấu hình liên công ty](/desk/company) — Thiết lập liên kết 2 pháp nhân TM + NM, tránh tính trùng doanh thu/chi phí *(Nguồn: QUY_TRINH)*

### Tiền mặt & Ngân hàng
- [Quản lý tiền mặt (Sổ quỹ)](/desk/payment-entry) — #138 Số dư đầu kỳ + Thu – Chi + Sổ quỹ
- [Quản lý tiền ngân hàng](/desk/bank-account) — #139 Nhiều tài khoản + Biến động số dư + Sao kê
- [Đối chiếu sao kê ngân hàng](/desk/bank-reconciliation) — #139 Đối chiếu sao kê ngân hàng
- [BC-15 Báo cáo theo dõi dòng tiền](/desk/query-report/Cash%20Flow) — Theo dõi dòng tiền vào/ra + tình trạng thanh toán (Người yêu cầu: Chị Ngân) *(Nguồn: Danh sách BC)*

### Kế toán mua hàng
- [Hóa đơn mua](/desk/purchase-invoice) — #140 Nhận dữ liệu từ đơn mua & phiếu nhập + Giá vốn
- [Phiếu thanh toán mua](/desk/payment-entry) — #141 Đã thanh toán + Thanh toán một phần + Công nợ NCC
- [Phiếu phân bổ chi phí nhập khẩu](/desk/landed-cost-voucher) — Phân bổ thuế NK (TK 3333) + phí vận chuyển vào giá vốn nhập kho (TK 1561) *(Nguồn: QUY_TRINH — Bắt buộc)*
- [Điều khoản thanh toán theo đại lý](/desk/payment-terms) — Cấu hình riêng từng KH/đại lý (30 ngày, 45 ngày, v.v.) *(Nguồn: QUY_TRINH — Bắt buộc)*

### Kế toán bán hàng
- [Hóa đơn bán](/desk/sales-invoice) — #142 Ghi nhận doanh thu theo đơn hàng + Theo kênh bán
- [Phiếu thu tiền](/desk/payment-entry) — Thu tiền từ khách hàng

### Kế toán công nợ
- [Công nợ phải thu](/desk/query-report/Accounts%20Receivable) — #143 Hạn thanh toán + Phân tích tuổi nợ
- [Công nợ phải trả](/desk/query-report/Accounts%20Payable) — #144 Gắn với đơn mua / phiếu nhập
- [Tạm ứng & Hoàn ứng](/desk/payment-entry) — #145 Nhân viên / NCC + Đối trừ công nợ

### Kế toán hàng tồn kho
- [Giá trị tồn kho](/desk/query-report/Stock%20Balance) — #146 Theo kho + Theo lô
- [Giá vốn hàng bán (COGS)](/desk/query-report/Gross%20Profit) — #147 FIFO / Bình quân di động

### Phân bổ & Kiểm soát chi phí
- [Trung tâm chi phí](/desk/cost-center) — Phân bổ chi phí theo bộ phận / chi nhánh / dự án *(Nguồn: QUY_TRINH)*
- [Hoa hồng nhân viên](/desk/sales-person) — Tính hoa hồng nhân viên kinh doanh cho Fitting/Coaching/Bán hàng *(Nguồn: QUY_TRINH)*
- [Mẫu in hóa đơn chuẩn Việt Nam](/desk/sales-invoice) — Mẫu in hóa đơn bán hàng + phiếu thu/chi theo chuẩn TT200 *(Nguồn: QUY_TRINH)*

### Chi phí & Hỗ trợ từ hãng
- [Chi phí hỗ trợ hãng](/desk/journal-entry) — #148 Marketing + Trưng bày + Demo
- [Phân bổ chi phí chiến dịch](/desk/journal-entry) — #149 Theo SP + Theo chiến dịch/dự án

### Tài sản & Công cụ dụng cụ
- [Quản lý tài sản cố định](/desk/asset) — #150 Nguyên giá + Khấu hao
- [Khấu hao tài sản theo giờ](/desk/asset-depreciation-schedule) — #151 Khấu hao theo số giờ sử dụng thực tế
- [Công cụ dụng cụ (CCDC)](/desk/asset) — #152 Phân bổ nhiều kỳ

### Kế toán thuế
- [Kế toán thuế GTGT (Hóa đơn điện tử)](/desk/sales-invoice) — #153 VAT đầu vào/ra + Hóa đơn điện tử
- [Kết xuất dữ liệu thuế (HTKK)](/desk/query-report/HTKK%20Export) — #154 Xuất file HTKK theo chuẩn khai thuế

### Báo cáo kế toán tổng hợp
- [Báo cáo kết quả kinh doanh](/desk/query-report/Profit%20and%20Loss%20Statement) — #155 Doanh thu + Chi phí + Lợi nhuận
- [Báo cáo chi phí](/desk/query-report/Budget%20Variance%20Report) — #156 Marketing + Demo + Bán hàng
- [Báo cáo quản trị](/desk/query-report/Sales%20Analytics) — #157 Theo chi nhánh + Theo đại lý
- [Bảng cân đối kế toán](/desk/query-report/Balance%20Sheet) — Tài sản / Nợ phải trả / Vốn chủ sở hữu *(Nguồn: QUY_TRINH)*
- [Báo cáo lưu chuyển tiền tệ](/desk/query-report/Cash%20Flow) — Dòng tiền từ hoạt động kinh doanh + đầu tư + tài chính *(Nguồn: QUY_TRINH — Bắt buộc)*
- [Báo cáo tình trạng thanh toán](/desk/query-report/Accounts%20Receivable) — Tùy chỉnh: KH/đại lý đã TT + chưa TT + quá hạn theo kỳ *(Nguồn: QUY_TRINH)*
- [Báo cáo tuổi nợ — Công nợ phải thu](/desk/query-report/Accounts%20Receivable%20Summary) — Chi tiết công nợ theo đại lý, phân loại theo tuổi nợ *(Nguồn: QUY_TRINH — Bắt buộc)*

### Báo cáo hàng tồn kho (Kế toán)
- [Tổng hợp nhập – xuất – tồn](/desk/query-report/Stock%20Balance) — #158 Tổng NXT + Tồn cuối kỳ
- [Tồn kho theo từng kho](/desk/query-report/Warehouse%20Wise%20Stock%20Balance) — #159 Từng kho/chi nhánh + Giá trị tồn
- [Tồn kho theo model/SKU](/desk/query-report/Item%20Wise%20Sales%20History) — #160 Model + SKU + Số lượng tồn + Tỷ trọng tồn
- [Tồn kho theo lô](/desk/query-report/Batch%20Item%20Expiry%20Status) — #161 Mã lô + Ngày nhập + Tồn theo lô
- [Tồn kho theo vòng đời](/desk/query-report/Batch%20Item%20Expiry%20Status) — #162 Hàng mới + Hàng chậm bán + Sắp hết vòng đời

---

## 📊 DASHBOARD

### Doanh số tổng quan
- [Doanh số theo ngày / tuần / tháng](/desk/dashboard) — #63 *(T3 - 16/03)*
- [Doanh số bán lẻ tổng](/desk/dashboard) — #64 Lọc nhóm KH = Khách lẻ *(T3 - 17/03)*
- [Doanh số theo nguồn khách hàng](/desk/dashboard) — #39 UTM Source từ Đơn Lead *(T3 - 15/03)*
- [Doanh số theo nguồn đơn hàng](/desk/dashboard) — #40 Theo UTM source *(T3 - 15/03)*
- [Top 20 sản phẩm bán chạy](/desk/dashboard) — #41 *(T3 - 15/03)*

### Dự báo & Cảnh báo
- [Dự báo doanh thu / Cảnh báo hụt doanh số](/desk/dashboard) — #167 Cài đặt doanh số mong đợi + cảnh báo khi hụt *(T5 - 31/05)*

---


### Tính năng bổ sung từ rà soát tài liệu
>  chưa có số thứ tự trong lịch triển khai

| Tính năng | Phân hệ | Mức ưu tiên | Ghi chú |
|-----------|---------|:-----------:|---------|
| Phiếu yêu cầu mua hàng | Mua hàng | Cao | Yêu cầu nội bộ từ kho/bộ phận |
| Phiếu phân bổ chi phí nhập khẩu | Mua hàng / Kế toán | **Bắt buộc** | Thuế NK, phí vận chuyển |
| Lịch đặt hàng cố định theo mùa vụ | Mua hàng | Cao | Gậy T9-10, Hàng Q.áo tháng, Hàng JP T6-7/11-12 |
| Biên bản kiểm nhận hàng (mẫu in) | Mua hàng / Kho | Cao | Mẫu in tùy chỉnh |
| Phân bổ hàng trước nhập | Kho | Cao | BC-04 |
| Theo dõi mùa vụ (trường tùy chỉnh) | Kho | Cao | SS/FW trên sản phẩm/lô |
| Giao dịch liên công ty TM ↔ NM | Kế toán | **Bắt buộc** | 2 pháp nhân riêng biệt |
| Trung tâm chi phí | Kế toán | Trung bình | Phân bổ theo bộ phận |
| Hoa hồng nhân viên | Kế toán / Bán hàng | Cao | Fitting, Coaching, Bán hàng |
| Bảng cân đối kế toán | Kế toán | Trung bình | Báo cáo tài chính |
| Báo cáo lưu chuyển tiền tệ | Kế toán | **Bắt buộc** | BC-15 |
| Mẫu in hóa đơn chuẩn Việt Nam | Kế toán | Cao | Theo TT200 |
| Điều khoản thanh toán theo đại lý | Kế toán | **Bắt buộc** | 30/45 ngày theo từng đại lý |
| Báo giá bán (B2B) | Bán hàng | Trung bình | Báo giá → Đơn bán hàng |
| BC-07 Nhập xuất tồn chi tiết NM | Kho | Cao | 3 bố cục + 2 chế độ xem |
| BC-08 Nhập xuất tồn chi tiết TM | Kho | Cao | Người yêu cầu: Chị Ngân |
| BC-10 Tổng hợp tồn kho | Kho | Cao | Giá trị = SL × giá TM × chiết khấu NM |
| BC-11 Tổng hợp bán hàng | Bán hàng | Cao | Lọc theo cửa hàng |
| BC-12 Tổng hợp nhập kho | Mua hàng | Cao | Nhóm theo năm/nhóm SP |
| BC-13 Theo dõi đặt hàng Gậy | Mua hàng | Cao | Theo dõi PO riêng dòng gậy |
| BC-14 Theo dõi đặt hàng Quần áo/Phụ kiện | Mua hàng | Cao | Theo dõi PO riêng dòng quần áo |
