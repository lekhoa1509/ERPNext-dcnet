# Báo Cáo Liệt Kê Chức Năng Phân Hệ Kế Toán Việt Nam (vn_accounting)
*Tài liệu bàn giao cho Project Manager và Kế toán trưởng*

Tài liệu này hệ thống hóa toàn bộ các chức năng thuộc ứng dụng **VN Accounting** (`vn_accounting`) tích hợp trên nền tảng Frappe v16 và ERPNext v16, tuân thủ các quy định hiện hành về kế toán tại Việt Nam (đặc biệt là Thông tư 99/2025/TT-BTC thay thế cho các mẫu biểu cũ, và các tiêu chuẩn của Thông tư 200/2014/TT-BTC).

Hệ thống menu được ánh xạ trực tiếp từ cấu trúc thanh điều hướng bên (Sidebar) của phân hệ nhằm giúp Ban dự án và Kế toán trưởng dễ dàng đối chiếu, vận hành và bàn giao phần mềm.

---

## Danh Sách Các Chức Năng Theo Sidebar Section

### 1. Tổng quan (Overview)

Bao gồm giao diện Dashboard trung tâm và công cụ phân tích dự báo tài chính ngắn và trung hạn của doanh nghiệp.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Tổng quan** | Trang (Page) | Dashboard quản trị kế toán tích hợp 5 thẻ số liệu KPI chính (Tồn quỹ, Doanh thu, Chi phí, Công nợ phải thu, Công nợ phải trả) và 8 biểu đồ phân tích (Doanh thu & Chi phí 12 tháng rolling, Biến động dòng tiền, Công nợ theo đối tác lớn...) hỗ trợ lọc linh hoạt theo Tuần/Tháng/Quý/Năm. |
| **Dự báo dòng tiền** | Trang (Page) | Giao diện phân tích và dự báo dòng tiền thông minh, tổng hợp tự động số liệu thu/chi từ các phân hệ (Đơn hàng SO/PO, Báo giá, Hóa đơn SI/PI chưa thanh toán, Lịch lương, Thuế phải nộp, Lịch trả nợ gốc/lãi vay ngân hàng, Tiền gửi có kỳ hạn) có điều chỉnh theo hệ số trễ thanh toán của từng khách hàng (Payment delay factor) và cảnh báo theo ngưỡng an toàn quỹ. |

---

### 2. Tiền mặt (Cash)

Quản lý luồng tiền mặt tại quỹ của công ty và các chi nhánh.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Phiếu thu** | Báo cáo (Report) | Tổng hợp danh sách và chi tiết các nghiệp vụ thu tiền mặt (ghi Nợ TK 111%), hỗ trợ in Phiếu thu kế toán theo mẫu chuẩn quy định. |
| **Phiếu chi** | Báo cáo (Report) | Tổng hợp danh sách và chi tiết các nghiệp vụ chi tiền mặt (ghi Có TK 111%), hỗ trợ in Phiếu chi kế toán theo mẫu chuẩn quy định. |
| **Kiểm kê quỹ** | Chứng từ (DocType) | Hỗ trợ hội đồng kiểm kê lập bảng kê kiểm đếm mệnh giá tiền mặt thực tế tại quỹ (VND), tự động đối chiếu số dư sổ sách kế toán (sổ cái TK 111%) tại thời điểm kiểm kê và sinh bút toán xử lý chênh lệch thừa/thiếu (Nợ 1381/Có 111 hoặc Nợ 111/Có 3381), kèm in Biên bản kiểm kê Mẫu 08a-TT. |
| **Sổ quỹ tiền mặt** | Báo cáo (Report) | Báo cáo chi tiết Sổ quỹ tiền mặt ghi chép các khoản thu, chi tiền mặt của TK 111% theo trình tự thời gian, hỗ trợ thủ quỹ và kế toán đối chiếu số dư hàng ngày. |
| **Phiếu quỹ chi nhánh** | Chứng từ (DocType) | Chứng từ ghi nhận thu/chi tiền mặt độc lập của các chi nhánh/cửa hàng con (Branch Cash Entry), tích hợp luồng phê duyệt nội bộ trước khi ghi sổ chính thức. |
| **Sổ quỹ chi nhánh** | Báo cáo (Report) | Báo cáo Sổ quỹ nội bộ (Sổ Nội Bộ) dành riêng cho từng chi nhánh để theo dõi dòng tiền độc lập. |

---

### 3. Ngân hàng (Banking)

Quản lý tiền gửi ngân hàng, đối soát và các hoạt động quản lý ngân quỹ (Term Deposit, Bank Loan).

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Thu ngân hàng** | Báo cáo (Report) | Tổng hợp danh sách các báo Có (Nợ TK 112%) tiền về tài khoản ngân hàng. |
| **Chi ngân hàng** | Báo cáo (Report) | Tổng hợp danh sách các báo Nợ (Có TK 112%) tiền chuyển đi khỏi tài khoản ngân hàng. |
| **Sổ Tài khoản ngân hàng** | Báo cáo (Report) | Sổ tiền gửi ngân hàng chi tiết theo từng số tài khoản ngân hàng (TK 112%), hỗ trợ đối chiếu với sao kê của ngân hàng. |
| **Đối soát sao kê** | Trang (Page) | Giao diện đối soát tự động sao kê ngân hàng với các hóa đơn bán hàng/mua hàng chưa thanh toán. Tích hợp thuật toán fuzzy logic nhận diện đối tác và gợi ý hóa đơn thông minh theo sai số tiền và thời gian. |
| **Điều chuyển nội bộ** | Báo cáo (Report) | Theo dõi các giao dịch chuyển tiền qua lại giữa các tài khoản ngân hàng hoặc nộp tiền mặt vào ngân hàng/rút tiền mặt về quỹ. |
| **Bút toán ngân hàng** | Chứng từ (DocType) | Lập trực tiếp bút toán nhật ký liên quan đến ngân hàng (Journal Entry với phân loại Voucher Type là "Bank Entry"). |
| **Tiền gửi có kỳ hạn** | Chứng từ (DocType) | Quản lý sổ tiền gửi tiết kiệm/có kỳ hạn ngân hàng (TK 1281). Hỗ trợ 5 phương thức tính lãi (cuối kỳ, định kỳ tháng/quý, trả trước, lãi kép) theo quy tắc actual/365, tự động hạch toán chuyển tiền gửi, sinh bút toán dự thu lãi hàng tháng (Nợ 1388 / Có 515) và thực hiện các nút tất toán/tái tục nhanh. |
| **Tổng hợp tiền gửi có kỳ hạn** | Báo cáo (Report) | Báo cáo tổng hợp số dư, lãi suất, ngày đáo hạn và trạng thái của tất cả các hợp đồng tiền gửi có kỳ hạn hiện tại. |
| **Khoản vay ngân hàng** | Chứng từ (DocType) | Quản lý các khế ước nhận nợ/hợp đồng vay vốn ngân hàng (TK 3411). Tự động sinh lịch trả gốc và lãi theo 2 phương thức: trả lãi định kỳ - gốc cuối kỳ (Interest Only) hoặc trả góp đều hàng tháng (EMI) theo actual/365; tự động hạch toán giải ngân vay, hạch toán dự chi chi phí lãi vay hàng tháng (Nợ 635 / Có 335) và cập nhật dư nợ thực tế. |
| **Tổng hợp khoản vay ngân hàng** | Báo cáo (Report) | Báo cáo tổng hợp dư nợ gốc, lãi suất và lịch thanh toán của tất cả các khoản vay ngân hàng. |
| **Dự báo dòng tiền** | Trang (Page) | Dự báo dòng tiền (đồng bộ dữ liệu liên kết hiển thị). |

---

### 4. Mua hàng (Purchasing)

Hạch toán chi tiết nghiệp vụ mua vật tư, hàng hóa và quản lý công nợ phải trả nhà cung cấp.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Đơn mua hàng** | Chứng từ (DocType) | Lập và theo dõi các đơn đặt mua hàng hóa/dịch vụ gửi nhà cung cấp. |
| **Đơn mua hàng cần lập hóa đơn** | Chứng từ (DocType) | Danh sách theo dõi các đơn đặt mua hàng đã nhận hàng vào kho nhưng nhà cung cấp chưa xuất hóa đơn, phục vụ kế toán đôn đốc chứng từ đầu vào. |
| **Hoá đơn mua hàng** | Chứng từ (DocType) | Lập hóa đơn mua hàng (Purchase Invoice) để hạch toán tăng công nợ phải trả người bán (331) và thuế GTGT đầu vào được khấu trừ. |
| **Nhập kho mua hàng** | Chứng từ (DocType) | Phiếu nhập kho vật tư, hàng hóa mua ngoài (Purchase Receipt) để ghi nhận tăng số lượng tồn kho. |
| **Điều khoản thanh toán** | Danh mục (DocType) | Định nghĩa các mẫu điều khoản thanh toán (kỳ hạn thanh toán, tỷ lệ thanh toán theo từng đợt) áp dụng khi giao dịch với nhà cung cấp. |
| **Công nợ phải trả** | Báo cáo (Report) | Báo cáo chi tiết công nợ phải trả người bán theo hóa đơn và theo tuổi nợ (Accounts Payable). |
| **Bảng tổng hợp công nợ NCC** | Báo cáo (Report) | Bảng tổng hợp số dư đầu kỳ, số phát sinh tăng/giảm và số dư nợ cuối kỳ của tất cả các nhà cung cấp. |
| **BC mua hàng** | Báo cáo (Report) | Báo cáo phân tích số liệu mua hàng (Purchase Analytics) theo thời gian, nhà cung cấp, nhóm hàng. |
| **Mua không VAT** | Báo cáo (Report) | Tổng hợp các hóa đơn mua hàng không chịu thuế GTGT hoặc thuế suất 0% phục vụ việc đối chiếu khi kê khai thuế đầu vào. |
| **BC theo mặt hàng** | Báo cáo (Report) | Chi tiết sổ nhật ký mua hàng theo từng mặt hàng cụ thể (Item-wise Purchase Register). |
| **Bút toán chung** | Chứng từ (DocType) | Lập chứng từ kế toán tổng hợp khác liên quan đến nghiệp vụ mua hàng. |

---

### 5. Bán hàng (Sales)

Hạch toán nghiệp vụ bán sản phẩm, hàng hóa, dịch vụ và theo dõi công nợ phải thu khách hàng.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Báo giá** | Chứng từ (DocType) | Lập và gửi báo giá thương mại cho khách hàng. |
| **Đơn bán hàng** | Chứng từ (DocType) | Ghi nhận đơn đặt hàng chính thức ký kết với khách hàng. |
| **Đơn bán hàng cần xuất hóa đơn** | Chứng từ (DocType) | Danh sách đơn hàng đã giao hoặc đến kỳ cần phải xuất hóa đơn tài chính gửi khách hàng. |
| **Hoá đơn bán hàng** | Chứng từ (DocType) | Hóa đơn bán hàng tài chính (Sales Invoice), ghi nhận doanh thu (TK 511), công nợ phải thu (TK 131) và thuế GTGT đầu ra, tích hợp với hệ thống hóa đơn điện tử để phát hành trực tiếp. |
| **Điều khoản thanh toán** | Danh mục (DocType) | Các quy định mẫu về kỳ hạn thanh toán dành cho khách hàng. |
| **Công nợ phải thu** | Báo cáo (Report) | Báo cáo chi tiết công nợ phải thu khách hàng theo hóa đơn và phân tích tuổi nợ (Accounts Receivable). |
| **Bảng tổng hợp công nợ KH** | Báo cáo (Report) | Bảng tổng hợp số dư công nợ đầu/cuối kỳ của tất cả các khách hàng. |
| **BC bán hàng** | Báo cáo (Report) | Báo cáo phân tích doanh thu bán hàng (Sales Analytics) đa chiều. |
| **Phiếu xuất kho** | Chứng từ (DocType) | Phiếu xuất kho hàng hóa giao cho khách hàng (Delivery Note) đã ghi sổ thành công. |
| **Bút toán chung** | Chứng từ (DocType) | Chứng từ kế toán tổng hợp phát sinh trong hoạt động bán hàng. |

---

### 6. Hợp đồng & PAKD (Contracts & Business Plans)

Phân hệ quản trị hợp đồng kinh tế và kiểm soát hiệu quả phương án kinh doanh (PAKD) của DCNET.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Danh sách hợp đồng** | Chứng từ (DocType) | Quản lý chi tiết thông tin hợp đồng kinh tế ký với khách hàng/đối tác (DCNET Contract), theo dõi lịch xuất hóa đơn và lịch thu tiền. |
| **Phương án kinh doanh** | Chứng từ (DocType) | Lập phương án kinh doanh (PAKD) dự toán cho dự án/hợp đồng, tính toán doanh thu dự kiến, chi phí trực tiếp, chi phí hoa hồng và biên lợi nhuận trước khi duyệt ký hợp đồng. |
| **Hóa đơn cần ghi sổ** | Báo cáo (Report) | Danh sách các hóa đơn đến kỳ cần phải hạch toán và ghi sổ theo cam kết hợp đồng. |
| **Hóa đơn quá hạn cần đôn thúc** | Báo cáo (Report) | Danh sách hóa đơn của các hợp đồng đã quá hạn thanh toán cần bộ phận công nợ đôn đốc khách hàng. |
| **Thu tiền theo hợp đồng** | Báo cáo (Report) | Báo cáo tổng hợp số tiền thực thu so với kế hoạch thu tiền của từng hợp đồng. |
| **Sổ hoa hồng NVKD (phải trả)** | Báo cáo (Report) | Báo cáo tổng hợp số tiền hoa hồng phải chi trả cho nhân viên kinh doanh dựa trên doanh số và tiến độ thanh toán của hợp đồng. |
| **Phải trả phía khách (kickback/markup/referral)** | Báo cáo (Report) | Quản lý và theo dõi các khoản phí giới thiệu, chiết khấu thương mại phải trả cho bên thứ ba theo hợp đồng (Beneficiary Payable). |
| **Công nợ theo hợp đồng** | Báo cáo (Report) | Chi tiết số dư công nợ phải thu chia theo từng hợp đồng kinh tế cụ thể. |
| **Kỳ thu tiền quá hạn** | Báo cáo (Report) | Báo cáo thống kê các kỳ thanh toán trên hợp đồng bị quá hạn. |

---

### 7. Kho (Inventory)

Theo dõi số lượng vật tư, hàng hóa trong kho bãi và các kiểm soát liên quan đến PAKD.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Cài đặt PAKD** | Thiết lập (DocType) | Cấu hình tham số chung cho phương án kinh doanh (PAKD Settings). |
| **Nhập xuất kho** | Chứng từ (DocType) | Phiếu xuất kho nguyên vật liệu, nhập kho thành phẩm hoặc chuyển kho nội bộ (Stock Entry). |
| **Lịch sử nhắc duyệt PAKD** | Nhật ký (DocType) | Ghi nhận lịch sử gửi email/thông báo phê duyệt các phương án kinh doanh cho ban giám đốc. |
| **Kiểm kê kho** | Chứng từ (DocType) | Chứng từ đối chiếu số lượng tồn kho thực tế và sổ sách (Stock Reconciliation), tự động cập nhật số lượng và hạch toán chênh lệch. |
| **Số lô** | Danh mục (DocType) | Quản lý vật tư, hàng hóa theo số lô sản xuất (Batch) để theo dõi hạn sử dụng. |
| **Số seri** | Danh mục (DocType) | Quản lý thiết bị, sản phẩm theo số seri riêng lẻ (Serial No). |
| **BC nhập xuất tồn** | Báo cáo (Report) | Báo cáo tổng hợp Nhập - Xuất - Tồn kho (Stock Balance) của vật tư hàng hóa theo kỳ. |
| **BC tuổi kho** | Báo cáo (Report) | Phân tích tuổi hàng tồn kho (Stock Ageing) để nhận diện hàng chậm luân chuyển. |
| **Sổ chi tiết kho** | Báo cáo (Report) | Sổ thẻ kho chi tiết (Stock Ledger) theo dõi từng giao dịch phát sinh của mặt hàng. |
| **Định mức tồn kho** | Báo cáo (Report) | Báo cáo gợi ý mức tồn kho tối thiểu và điểm đặt hàng lại tối ưu (Reorder Level). |
| **Gói sản phẩm** | Danh mục (DocType) | Định nghĩa các gói/combo sản phẩm (Product Bundle) phục vụ xuất kho đồng thời. |

---

### 8. TSCĐ (Fixed Assets)

Quản lý vòng đời tài sản cố định của doanh nghiệp và tính toán khấu hao tự động.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Danh sách** | Chứng từ (DocType) | Quản lý hồ sơ thẻ tài sản cố định (Asset) bao gồm nguyên giá, ngày mua, thời gian khấu hao, loại tài sản. |
| **Tính khấu hao** | Chứng từ (DocType) | Lập và theo dõi lịch trình tính khấu hao tài sản cố định (Asset Depreciation Schedule) theo phương pháp đường thẳng hoặc số dư giảm dần chuẩn mực Việt Nam. |
| **Sửa chữa** | Chứng từ (DocType) | Ghi nhận các chi phí sửa chữa, nâng cấp, bảo dưỡng TSCĐ (Asset Repair) và hạch toán vốn hóa hoặc đưa vào chi phí trong kỳ. |
| **Bàn giao TSCĐ** | Chứng từ (DocType) | Chứng từ ghi nhận bàn giao TSCĐ cho nhân viên/phòng ban chịu trách nhiệm sử dụng (Asset Handover có scope="TSCĐ"), xác định vị trí tài sản. |
| **Kiểm kê TSCĐ** | Chứng từ (DocType) | Biên bản kiểm kê thực tế tài sản cố định định kỳ (Asset Stocktake), ghi nhận tài sản mất mát, hư hỏng và hạch toán chênh lệch. |
| **Thanh lý tài sản** | Chứng từ (DocType) | Chứng từ ghi giảm và thanh lý tài sản cố định (Asset Disposal) do hết hạn sử dụng hoặc nhượng bán. |
| **Sổ S21-DN** | Báo cáo (Report) | Sổ tài sản cố định chuẩn theo Mẫu S21-DN quy định tại Thông tư 99/2025/TT-BTC. |
| **Lịch sử khấu hao** | Báo cáo (Report) | Báo cáo chi tiết các bút toán khấu hao hàng tháng đã ghi sổ (Asset Depreciation Ledger). |

---

### 9. CCDC (Tools & Instruments)

Quản lý công cụ dụng cụ và phân bổ chi phí trả trước dài hạn (tài khoản 242).

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Danh sách CCDC** | Chứng từ (DocType) | Quản lý danh mục công cụ dụng cụ đang sử dụng (CCDC Item), liên kết tài khoản phân bổ (TK 242). |
| **Ghi giảm CCDC** | Chứng từ (DocType) | Ghi giảm công cụ dụng cụ do hỏng hóc, mất mát hoặc thanh lý trước hạn. |
| **Bàn giao CCDC** | Chứng từ (DocType) | Biên bản bàn giao công cụ dụng cụ cho nhân viên sử dụng (scope="CCDC"). |
| **Kiểm kê CCDC** | Chứng từ (DocType) | Thực hiện kiểm kê CCDC thực tế tại các phòng ban/địa điểm. |
| **Sổ S22-DN** | Báo cáo (Report) | Sổ theo dõi công cụ dụng cụ và tài sản cố định tại nơi sử dụng theo Mẫu S22-DN của Thông tư 99/2025/TT-BTC. |
| **Lịch phân bổ CCDC (242→6423)** | Chứng từ (DocType) | Thiết lập lịch phân bổ chi phí CCDC dài hạn từ tài khoản chi phí trả trước (TK 242) sang tài khoản chi phí quản lý doanh nghiệp (TK 6423) hàng tháng. |

---

### 10. Tiền lương (Payroll)

Quản lý dữ liệu chấm công, tính lương và hồ sơ nhân sự.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Bảng chấm công** | Chứng từ (DocType) | Ghi nhận ngày công làm việc của nhân viên (Attendance). |
| **Bảng giờ công (theo dự án)** | Chứng từ (DocType) | Theo dõi giờ làm việc chi tiết của nhân viên theo từng dự án/công việc (Timesheet) làm cơ sở tính lương và tính giá thành dự án. |
| **Bảng lương** | Chứng từ (DocType) | Lập bảng tính lương tổng hợp cho toàn doanh nghiệp hàng tháng (Payroll Entry). |
| **Phiếu lương** | Chứng từ (DocType) | Phiếu chi tiết lương cá nhân gửi cho từng nhân viên (Salary Slip). |
| **Cơ cấu lương** | Danh mục (DocType) | Cấu hình các công thức tính lương dựa trên lương cơ bản, phụ cấp và các khoản giảm trừ. |
| **Thành phần lương** | Danh mục (DocType) | Định nghĩa các khoản thu nhập (lương chính, phụ cấp) và khoản khấu trừ (BHXH, thuế TNCN). |
| **Gán Cơ cấu lương** | Chứng từ (DocType) | Quyết định áp dụng cơ cấu lương cụ thể cho từng nhân viên. |
| **Lương bổ sung** | Chứng từ (DocType) | Ghi nhận các khoản thưởng hoặc phạt phát sinh ngoài cơ cấu lương thường xuyên trong tháng. |
| **Danh sách nhân viên** | Danh mục (DocType) | Quản lý hồ sơ nhân sự của công ty. |

---

### 11. Giá thành (Cost Accounting)

Tập hợp và phân bổ chi phí để tính giá thành sản phẩm sản xuất và giá trị nhập kho của hàng hóa.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Phân bổ CP vào giá vốn** | Chứng từ (DocType) | Phân bổ phụ phí mua hàng (phí vận chuyển, bốc xếp, thuế nhập khẩu...) vào giá trị nhập kho của hàng hóa (Landed Cost Voucher - LCV) theo các tiêu thức Số lượng, Giá trị, Trọng lượng hoặc Thể tích. |
| **CP chờ phân bổ (TK 242)** | Báo cáo (Report) | Báo cáo theo dõi các hóa đơn chi phí mua hàng đã hạch toán tạm tính nhưng chưa được phân bổ vào phiếu nhập kho nào. |
| **Dự án — Giá thành** | Chứng từ (DocType) | Tập hợp chi phí và tính toán giá thành chi tiết cho từng công trình, dự án (Project Costing). |
| **Tiến độ xuất hóa đơn** | Báo cáo (Report) | Đối chiếu tiến độ xuất hóa đơn thực tế của dự án so với kế hoạch doanh thu. |
| **Kết chuyển CP SXC (627→154)** | Chứng từ (DocType) | Bút toán tự động tập hợp chi phí và kết chuyển chi phí sản xuất chung (TK 627) sang chi phí sản xuất kinh doanh dở dang (TK 154) cuối kỳ. |
| **Cài đặt phân bổ CP vào giá vốn** | Thiết lập (DocType) | Định nghĩa tài khoản hạch toán mặc định cho 12 loại chi phí phụ phí mua hàng trong và ngoài nước (vận chuyển, hải quan, bốc xếp, thuế nhập khẩu...). |

---

### 12. Thuế (Taxation)

Theo dõi và lập báo cáo thuế giá trị gia tăng (GTGT) đầu vào, đầu ra.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **HĐ GTGT đầu vào** | Chứng từ (DocType) | Quản lý hóa đơn giá trị gia tăng đầu vào nhận từ nhà cung cấp (EInvoice Inward), hỗ trợ kiểm tra tính hợp lệ. |
| **HĐ GTGT đầu ra** | Chứng từ (DocType) | Quản lý hóa đơn giá trị gia tăng xuất cho khách hàng đã phát hành thành công (einvoice_issued=1). |
| **Tờ khai thuế GTGT (01/GTGT)** | Báo cáo (Report) | Báo cáo tờ khai thuế GTGT Mẫu 01/GTGT theo quy định của Thông tư 80/2021/TT-BTC, tự động lấy số liệu từ GL. |
| **Mẫu thuế bán hàng** | Thiết lập (DocType) | Cấu hình các nhóm thuế suất GTGT đầu ra mặc định áp dụng khi lập hóa đơn bán hàng. |
| **Mẫu thuế mua hàng** | Thiết lập (DocType) | Cấu hình các nhóm thuế suất GTGT đầu vào mặc định áp dụng khi lập hóa đơn mua hàng. |
| **Mẫu thuế hàng hoá** | Thiết lập (DocType) | Áp dụng thuế suất đặc thù cho từng loại hàng hóa, dịch vụ cụ thể. |
| **[Pending] Kiểm tra MST** | Trang (Page) | Công cụ tra cứu và xác thực mã số thuế của khách hàng/nhà cung cấp trực tuyến (đang phát triển). |

---

### 13. Tổng hợp (General Ledger)

Thực hiện các nghiệp vụ kế toán tổng hợp, đánh giá ngoại tệ và khóa sổ kỳ kế toán.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Đánh giá lại ngoại tệ** | Chứng từ (DocType) | Đánh giá lại số dư các tài khoản có gốc ngoại tệ (tiền mặt, tiền gửi, công nợ) theo tỷ giá giao dịch thực tế cuối kỳ kế toán. |
| **Phiếu khóa sổ kỳ** | Chứng từ (DocType) | Chứng từ khóa sổ kế toán cuối kỳ (Period Closing Voucher), ngăn chặn việc chỉnh sửa dữ liệu của kỳ đã chốt. |
| **Định nghĩa kỳ kế toán** | Danh mục (DocType) | Chia năm tài chính thành các kỳ kế toán (tháng, quý) để phục vụ lập báo cáo và khóa sổ. |
| **Sổ nhật ký chung** | Báo cáo (Report) | Sổ Nhật ký chung ghi chép toàn bộ các định khoản kế toán phát sinh theo trình tự thời gian (Mẫu S03a-DN). |
| **Sổ cái** | Báo cáo (Report) | Sổ cái chi tiết tài khoản (Mẫu S03b-DN) dùng để theo dõi biến động tăng/giảm và số dư của từng tài khoản kế toán. |
| **Bảng cân đối số phát sinh** | Báo cáo (Report) | Báo cáo Bảng cân đối số phát sinh tài khoản (Trial Balance) hiển thị số dư đầu kỳ, phát sinh Nợ/Có và số dư cuối kỳ của tất cả các tài khoản. |

---

### 14. Báo cáo tài chính (Financial Statements)

Hệ thống Báo cáo Tài chính bắt buộc tuân thủ mẫu biểu và công thức của Thông tư 99/2025/TT-BTC cùng các báo cáo thuế/tư vấn TNDN đi kèm.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Báo cáo tình hình tài chính (B01-DN)** | Báo cáo (Report) | Báo cáo tài chính bắt buộc phản ánh tổng quát tình hình tài sản, nguồn vốn của doanh nghiệp tại một thời điểm cuối kỳ (chuẩn mực TT99/2025/TT-BTC - thay thế Bảng cân đối kế toán trước đây). |
| **Báo cáo kết quả HĐKD (B02-DN)** | Báo cáo (Report) | Báo cáo tài chính bắt buộc phản ánh doanh thu, chi phí và kết quả hoạt động kinh doanh (lợi nhuận/lỗ) của doanh nghiệp trong kỳ. |
| **Báo cáo lưu chuyển tiền tệ (B03-DN)** | Báo cáo (Report) | Báo cáo lưu chuyển tiền tệ theo phương pháp gián tiếp, chỉ ra các dòng tiền vào/ra từ hoạt động Kinh doanh, Đầu tư và Tài chính. |
| **Thuyết minh BCTC (B09-DN)** | Trang (Page) | Công cụ sinh file Thuyết minh báo cáo tài chính tự động (Mẫu B09-DN) kết xuất số liệu thô từ B01-DN, B02-DN, B03-DN sang biểu mẫu Word/Excel để kế toán nhập bổ sung phần thuyết minh văn bản. |
| **Quyết toán TNDN (Form 03)** | Báo cáo (Report) | Báo cáo quyết toán thuế thu nhập doanh nghiệp Mẫu số 03/TNDN (Thông tư 80/2021/TT-BTC), đối chiếu tự động giữa Doanh thu - Chi phí kế toán và các khoản điều chỉnh luật Thuế (chỉ tiêu B). |
| **Chi phí không được trừ (B4)** | Báo cáo (Report) | Báo cáo chi tiết các khoản chi phí không được trừ khi tính thuế TNDN (chỉ tiêu B4), tổng hợp từ các chứng từ được gắn cờ `is_non_deductible` theo 6 nhóm lý do pháp lý. |
| **Tư vấn — Chi phí không trừ TNDN** | URL (Trang hỗ trợ) | Cẩm nang hướng dẫn trực quan (Wiki/Help) tích hợp trên phần mềm giải thích chi tiết quy định và cách xử lý chứng từ chi phí không được trừ theo Nghị định 320/2025/NĐ-CP và VAS 17. |
| **Phân tích lợi nhuận (theo TTCP/Dự án)** | Báo cáo (Report) | Báo cáo phân tích lãi lỗ chi tiết theo trung tâm chi phí hoặc dự án cụ thể. |
| **So sánh ngân sách (Thực tế vs KH)** | Báo cáo (Report) | Đối chiếu số liệu chi phí thực tế phát sinh so với ngân sách kế hoạch được phê duyệt để đánh giá chênh lệch. |
| **BC lãi lỗ quản trị** | Báo cáo (Report) | Báo cáo Kết quả hoạt động kinh doanh nội bộ phục vụ nhu cầu quản trị của Ban giám đốc. |
| **Tóm tắt Dự án** | Báo cáo (Report) | Tổng hợp các chỉ số tài chính cơ bản của từng dự án đang triển khai. |
| **Cấu hình BCTC Mapping** | Chứng từ (DocType) | Thiết lập công thức tính toán và mapping tài khoản kế toán sang các chỉ tiêu trên Báo cáo tài chính (B01-DN, B02-DN, B03-DN) theo đặc thù doanh nghiệp. |

---

### 15. Danh mục (Master Data)

Các danh mục dữ liệu dùng chung cốt lõi của doanh nghiệp.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Hệ thống tài khoản** | Danh mục (DocType) | Quản lý danh mục tài khoản kế toán của doanh nghiệp, phân nhóm tài khoản mẹ - con. |
| **Khách hàng** | Danh mục (DocType) | Quản lý hồ sơ đối tác khách hàng. |
| **Nhà cung cấp** | Danh mục (DocType) | Quản lý hồ sơ đối tác nhà cung cấp. |
| **Hàng hoá, vật tư** | Danh mục (DocType) | Quản lý thông tin mã hàng hóa, vật tư, dịch vụ. |
| **Kho** | Danh mục (DocType) | Danh sách các kho bãi chứa hàng. |
| **Nhân viên** | Danh mục (DocType) | Quản lý danh sách lao động trong công ty. |
| **Định mức vật tư (BOM)** | Danh mục (DocType) | Thiết lập định mức nguyên vật liệu sản xuất (Bill of Materials) cho sản phẩm. |

---

### 16. Thiết lập (Settings)

Cấu hình chuyên sâu cho toàn bộ phân hệ và các quy tắc nghiệp vụ liên quan.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Mẫu hợp đồng** | Thiết lập (DocType) | Quản lý các điều khoản mẫu của hợp đồng kinh tế. |
| **Cây tài khoản** | Thiết lập (DocType) | Trình bày hệ thống tài khoản kế toán dưới dạng cây phân cấp trực quan để dễ quản lý. |
| **Cài đặt Hợp đồng** | Thiết lập (DocType) | Các cấu hình chung liên quan đến hợp đồng kinh tế. |
| **Import cây tài khoản** | Thiết lập (DocType) | Tiện ích tải danh mục tài khoản từ file Excel/CSV vào hệ thống. |
| **Mẫu quy tắc hoa hồng** | Thiết lập (DocType) | Thiết lập công thức tính hoa hồng bán hàng cho nhân viên kinh doanh theo PAKD. |
| **Năm tài chính** | Thiết lập (DocType) | Khởi tạo và quản lý các năm tài chính của doanh nghiệp. |
| **Cài đặt PAKD** | Thiết lập (DocType) | Cài đặt các tham số cho phương án kinh doanh. |
| **Kỳ kế toán** | Thiết lập (DocType) | Định cấu hình kỳ hạn chốt số liệu. |
| **Lịch sử nhắc duyệt PAKD** | Nhật ký (DocType) | Ghi nhận nhật ký nhắc phê duyệt phương án kinh doanh. |
| **Trung tâm chi phí** | Danh mục (DocType) | Quản lý sơ đồ phân cấp các phòng ban, trung tâm chi phí để tập hợp chi phí. |
| **Dự án** | Danh mục (DocType) | Quản lý danh sách dự án của công ty. |
| **Ngân sách** | Thiết lập (DocType) | Thiết lập ngân sách chi phí cho từng tài khoản/trung tâm chi phí theo năm. |
| **Cài đặt kho** | Thiết lập (DocType) | Các cấu hình quản trị kho vận của hệ thống. |
| **Cài đặt kế toán** | Thiết lập (DocType) | Cấu hình các tài khoản mặc định và tham số chung cho phân hệ kế toán Việt Nam. |

---

### 17. Công cụ Import (Import Tools)

Bộ công cụ phục vụ quá trình chuyển giao và kế thừa dữ liệu từ hệ thống cũ sang ERPNext.

| Tên chức năng (Sidebar Item) | Loại | Mô tả chức năng vắn tắt |
| :--- | :--- | :--- |
| **Misa Migration Hub** | Trang (Page) | Trung tâm điều khiển nhập liệu tự động dữ liệu lịch sử từ MISA sang ERPNext (số dư đầu kỳ, danh mục khách hàng/nhà cung cấp, chứng từ kế toán phát sinh). |
| **Lịch sử Migration** | Chứng từ (DocType) | Nhật ký ghi nhận các lô dữ liệu đã được import từ MISA, hỗ trợ kiểm tra lỗi, đối soát số liệu và rollback khi xảy ra sai sót. |
