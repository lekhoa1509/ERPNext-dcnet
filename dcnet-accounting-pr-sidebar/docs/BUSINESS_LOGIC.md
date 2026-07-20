# Business Logic — VN Accounting

App bản địa hóa kế toán Việt Nam cho ERPNext theo Thông tư 99/2025/TT-BTC.

Tài liệu này mô tả **nghiệp vụ thuần túy** mà app đang phục vụ, viết cho kế toán trưởng đọc và xác nhận. Tài liệu không chứa chi tiết kỹ thuật (tên trường, tên module, API). Phần kỹ thuật nằm ở các spec thiết kế riêng.

---

## 1. Bối cảnh & Mục đích

### 1.1 Vấn đề cần giải quyết

ERPNext bản chuẩn được thiết kế theo thông lệ kế toán quốc tế. Khi áp dụng tại Việt Nam, hệ thống mặc định không đáp ứng các yêu cầu bản địa:

- Hệ thống tài khoản không theo số hiệu và cấu trúc của TT99/2025/TT-BTC
- Thiếu các sổ sách pháp định (sổ quỹ tiền mặt, sổ tiền gửi ngân hàng, sổ chi tiết tài khoản, bảng cân đối số phát sinh) theo biểu mẫu Việt Nam
- Không có quy trình kiểm kê quỹ tiền mặt theo VAS
- Không quản lý trực tiếp tiền gửi có kỳ hạn (TK 1281) và vay ngân hàng (TK 3411) như một nghiệp vụ ngân quỹ riêng biệt
- Các tài khoản mặc định khi tạo công ty mới không khớp với số hiệu Việt Nam

App `vn_accounting` lấp các khoảng trống này, giữ nguyên phần lõi ERPNext.

### 1.2 Người dùng mục tiêu

- **Kế toán viên** tại doanh nghiệp vừa và lớn của Việt Nam
- **Kế toán trưởng** cần duyệt chứng từ, đối soát cân đối, xuất báo cáo
- **Kiểm toán / cơ quan thuế** cần truy vết sổ cái, số dư, chứng từ gốc
- **Giám đốc / thủ quỹ** tham gia ký biên bản kiểm kê quỹ

### 1.3 Khi nào dùng

Áp dụng cho công ty có quốc gia là Việt Nam, hạch toán theo TT99/2025 (hợp nhất TT200 và TT133 cũ). App kích hoạt khi tạo Company mới chọn Country = Vietnam, hoặc cài thủ công cho công ty đã có.

---

## 2. Phạm vi nghiệp vụ

App hiện bao phủ các nhóm nghiệp vụ sau:

| Nhóm | Tóm tắt |
|------|---------|
| Hệ thống tài khoản (COA) | 2 mẫu COA theo TT99/2025: doanh nghiệp lớn và doanh nghiệp nhỏ. Tự động hiện khi tạo công ty Việt Nam. |
| Thiết lập mặc định công ty | Sau khi COA được tạo, hệ thống tự gán các tài khoản chuẩn (tiền mặt, ngân hàng, phải thu, phải trả, doanh thu, giá vốn, khấu hao…) vào các trường mặc định của công ty. |
| Báo cáo kế toán | Bảng cân đối số phát sinh, sổ chi tiết tài khoản, sổ quỹ tiền mặt, sổ tiền gửi ngân hàng, thu/chi tiền mặt, thu/chi ngân hàng, chuyển khoản nội bộ. |
| Dashboard quản trị | 5 chỉ tiêu tồn quỹ/doanh thu/chi phí/công nợ + các biểu đồ diễn biến theo tháng, quý, năm, tuần. |
| Ngân quỹ — Tiền gửi có kỳ hạn | Quản lý sổ tiền gửi (TK 1281), sinh lịch trả lãi, bút toán gửi — trả lãi — tất toán — tái tục. |
| Ngân quỹ — Vay ngân hàng | Quản lý khoản vay (TK 3411), sinh lịch trả nợ, bút toán giải ngân — trả lãi — trả gốc — tất toán. |
| Dự thu / dự chi lãi (VAS) | Ghi nhận lãi chưa nhận/chưa trả cuối kỳ theo chuẩn VAS cho tiền gửi và vay. |
| Kiểm kê quỹ tiền mặt | Sắp triển khai: quy trình kiểm kê định kỳ/đột xuất, bảng kê mệnh giá, bút toán chênh lệch 2 bước theo VAS, in biên bản Mẫu 08a. |
| Điều hướng & bản địa hóa | Sidebar 40+ mục xếp theo phần hành kế toán Việt Nam, giao diện tiếng Việt đầy đủ dấu. |

---

## 3. Vai trò & Người dùng

### 3.1 Kế toán viên (Accounts User)

Làm việc hằng ngày với:
- Nhập chứng từ thu/chi tiền mặt và ngân hàng
- Tạo và nhập sổ tiền gửi có kỳ hạn, khoản vay ngân hàng
- Thực hiện kiểm đếm thực tế quỹ tiền mặt, nhập số liệu kiểm kê
- Xem sổ quỹ, sổ tiền gửi ngân hàng, sổ chi tiết tài khoản
- Tạo bản nháp bút toán cho các nghiệp vụ phát sinh

Kế toán viên chỉ được phép tạo và sửa ở trạng thái Nháp, không tự duyệt chứng từ ảnh hưởng sổ cái.

### 3.2 Kế toán trưởng (Accounts Manager)

Chịu trách nhiệm:
- Duyệt và ghi sổ (submit) các bút toán nháp do hệ thống hoặc kế toán viên tạo
- Kiểm tra bảng cân đối số phát sinh, đối soát công nợ, đối soát quỹ
- Duyệt biên bản kiểm kê quỹ sau khi kiểm đếm xong
- Cấu hình tài khoản mặc định (tiền gửi 1281, doanh thu lãi 515, nợ vay 3411, chi phí lãi vay 635, thừa quỹ 3381, thiếu quỹ 1381, phải thu khác 1388, chi phí bằng tiền khác 6425, thu nhập khác 711…)
- Nhận cảnh báo đáo hạn tiền gửi / khoản vay
- Xem dashboard quản trị

### 3.3 Thủ quỹ

- Tham gia đếm thực tế tiền mặt khi kiểm kê
- Ký biên bản kiểm kê
- Trong trường hợp thiếu quỹ do lỗi thủ quỹ, có thể là đối tượng bồi thường (hạch toán TK 1388)

### 3.4 Giám đốc

- Ký biên bản kiểm kê quỹ (theo yêu cầu pháp lý của Mẫu 08a)
- Xem dashboard quản trị
- Không thao tác trên hệ thống cho nghiệp vụ hằng ngày

### 3.5 Kiểm toán / Cơ quan thuế

- Truy vết sổ cái qua sổ chi tiết tài khoản và bảng cân đối số phát sinh
- Lấy dữ liệu cho báo cáo tài chính pháp định (B01-DN, B02-DN, B03-DN, B09-DN — các báo cáo này thuộc kế hoạch phát triển tiếp theo, xem phần 8)
- In biên bản kiểm kê quỹ theo Mẫu 08a

---

## 4. Quy tắc nghiệp vụ chính

### 4.1 Hệ thống tài khoản

Áp dụng **TT99/2025/TT-BTC** (hợp nhất và thay thế TT200/2014 và TT133/2016). App cung cấp 2 mẫu để lựa chọn khi tạo công ty:

- **Doanh nghiệp lớn** — hệ thống tài khoản đầy đủ (khoảng 185 tài khoản), dùng cho công ty quy mô lớn, có hoạt động sản xuất.
- **Doanh nghiệp nhỏ** — hệ thống tài khoản rút gọn (khoảng 141 tài khoản), phù hợp doanh nghiệp vừa và nhỏ, không có các tài khoản 621/622/627 (chi phí sản xuất theo yếu tố).

Khi người dùng tạo Company mới và chọn Country = Vietnam, cả hai mẫu xuất hiện trong danh sách chọn COA. Hệ thống tự nhận diện mẫu đã chọn (dựa vào sự hiện diện của các tài khoản đặc trưng) và áp các thiết lập mặc định tương ứng.

**Các tài khoản chuẩn và vai trò nghiệp vụ chính:**

| Tài khoản | Tên | Vai trò nghiệp vụ |
|-----------|-----|-------------------|
| 111 | Tiền mặt | Quỹ tiền mặt, chứng từ thu chi trực tiếp |
| 112 | Tiền gửi ngân hàng | Sổ phụ ngân hàng |
| 1281 | Tiền gửi có kỳ hạn | Sổ tiết kiệm, chứng chỉ tiền gửi |
| 131 | Phải thu khách hàng | Công nợ bán hàng |
| 1381 | Tài sản thiếu chờ xử lý | Chênh lệch thiếu khi kiểm kê |
| 1388 | Phải thu khác | Bồi thường của nhân viên (ví dụ thủ quỹ) |
| 156 | Hàng hoá (group, cha của 1561 + 1562) | Cấu trúc cha — không hạch toán trực tiếp |
| 1561 | Giá mua hàng hoá | Tồn kho thương mại — TK kho gốc của Item (default_inventory_account) |
| 1562 | Chi phí thu mua hàng hoá | Phụ phí LCV (vận chuyển, bốc xếp, bảo hiểm) — JE bù tự lập sau LCV submit |
| 214 | Hao mòn TSCĐ | Khấu hao luỹ kế |
| 242 | Chi phí trả trước | Phân bổ CCDC, chi phí trả trước |
| 331 | Phải trả người bán | Công nợ mua hàng |
| 3381 | Tài sản thừa chờ xử lý | Chênh lệch thừa khi kiểm kê |
| 335 | Chi phí phải trả | Dự chi lãi vay |
| 3411 | Vay ngân hàng | Dư nợ khoản vay |
| 511 | Doanh thu bán hàng và cung cấp dịch vụ | |
| 515 | Doanh thu hoạt động tài chính | Lãi tiền gửi |
| 632 | Giá vốn hàng bán | |
| 635 | Chi phí tài chính | Lãi vay |
| 6425 | Chi phí bằng tiền khác | Xử lý chênh lệch thiếu quỹ (chi phí quản lý) |
| 711 | Thu nhập khác | Xử lý chênh lệch thừa quỹ (nếu ghi nhận thu nhập) |

Sau khi tạo công ty, hệ thống tự động gán các tài khoản trên làm tài khoản mặc định tương ứng của công ty (tiền mặt, ngân hàng, phải thu, phải trả, doanh thu, giá vốn, kho, khấu hao luỹ kế, chi phí khấu hao…). Kế toán trưởng có thể điều chỉnh sau nếu cần.

### 4.2 Báo cáo kế toán

App cung cấp các báo cáo cơ bản mà ERPNext chuẩn chưa có theo đúng biểu mẫu Việt Nam:

**Đã có:**
- **Bảng cân đối số phát sinh** — số dư đầu kỳ, phát sinh nợ/có trong kỳ, số dư cuối kỳ theo từng tài khoản.
- **Sổ chi tiết tài khoản** — diễn biến từng giao dịch trên một tài khoản, có số dư luỹ kế (running balance).
- **Sổ quỹ tiền mặt** — thu chi tiền mặt (TK 111), có đối ứng.
- **Sổ tiền gửi ngân hàng** — thu chi ngân hàng (TK 112).
- **Thu tiền mặt / Chi tiền mặt** — danh sách các bút toán ghi nợ/có TK 111.
- **Thu ngân hàng / Chi ngân hàng** — danh sách các bút toán ghi nợ/có TK 112.
- **Chuyển khoản nội bộ** — các bút toán có cả bên nợ và bên có thuộc nhóm tiền mặt / ngân hàng.

**Báo cáo kế thừa từ ERPNext** (liên kết sẵn trong sidebar): Công nợ phải thu, Công nợ phải trả, Bảng tổng hợp công nợ khách hàng / nhà cung cấp, Thẻ kho, Báo cáo nhập xuất tồn, Sổ TSCĐ, Bảng tính khấu hao, Báo cáo bán hàng, Báo cáo mua hàng.

### 4.3 Dashboard quản trị

Trang tổng quan cung cấp cho giám đốc và kế toán trưởng các chỉ tiêu điều hành nhanh:

- **5 chỉ tiêu số (KPI):** Tồn quỹ (tiền mặt + ngân hàng), Tổng doanh thu, Tổng chi phí, Công nợ phải thu, Công nợ phải trả.
- **Biểu đồ diễn biến:** Doanh thu so với chi phí (cuộn 12 tháng gần nhất), biến động tiền (tách riêng tiền mặt TK 111 và ngân hàng TK 112), công nợ phải thu / phải trả theo nhóm tuổi nợ (aging theo đối tác lớn nhất).
- **Bộ lọc độ mịn:** Tháng / Quý / Năm / Tuần. Trục Y rút gọn số lớn (1.000.000 hiển thị thành 1M) cho dễ đọc.

Dashboard phiên bản 2 (Frappe Page tuỳ biến) mở rộng thêm: 5 KPI + 8 biểu đồ + lọc theo khoảng thời gian (Quý này, 12 tháng rolling…).

### 4.4 Quản lý quỹ tiền mặt — Kiểm kê (sắp triển khai)

Nghiệp vụ kiểm kê quỹ là yêu cầu pháp lý định kỳ, đồng thời là công cụ kiểm soát nội bộ.

**Khi nào kiểm kê:**
- Định kỳ — cuối tháng, cuối quý, cuối năm
- Đột xuất — khi bàn giao thủ quỹ, khi nghi ngờ sai lệch, khi có yêu cầu của ban giám đốc hoặc kiểm toán

**Ai tham gia và ai duyệt:**
- Thủ quỹ: đếm thực tế, ký biên bản
- Kế toán (thường là kế toán thanh toán): ghi nhận số sổ sách, so sánh, lập biên bản
- Kế toán trưởng: kiểm tra, duyệt biên bản, tạo bút toán chênh lệch
- Giám đốc: ký xác nhận biên bản kiểm kê

**Quy trình nghiệp vụ:**

1. Lập phiếu kiểm kê (định kỳ hoặc đột xuất — đột xuất cần ghi lý do).
2. Hệ thống tự lấy số dư sổ sách của tài khoản tiền mặt tại ngày kiểm kê.
3. Thủ quỹ đếm tiền thực tế. Có 2 cách nhập:
   - Nhập tổng số tiền thực tế (nhanh, đơn giản)
   - Chi tiết theo bảng kê mệnh giá (500.000, 200.000, 100.000, 50.000, 20.000, 10.000, 5.000, 2.000, 1.000 VND) — bắt buộc với biên bản chính thức theo Mẫu 08a
4. Hệ thống tính chênh lệch = thực tế − sổ sách:
   - = 0 → "Cân bằng", kết thúc
   - > 0 → "Thừa quỹ"
   - < 0 → "Thiếu quỹ"
5. Duyệt biên bản (cần đủ 3 người: thủ quỹ, kế toán trưởng, giám đốc).
6. **Bước 1 của VAS — Ghi nhận chênh lệch chờ xử lý:**
   - Thiếu quỹ: Nợ 1381 (Tài sản thiếu chờ xử lý) / Có 111
   - Thừa quỹ: Nợ 111 / Có 3381 (Tài sản thừa chờ xử lý)
   - Bút toán ở trạng thái nháp, kế toán trưởng kiểm tra rồi ghi sổ.
7. **Bước 2 của VAS — Xử lý chênh lệch** (sau khi điều tra nguyên nhân):
   - **Thiếu quỹ do thủ quỹ bồi thường:** Nợ 1388 / Có 1381
   - **Thiếu quỹ tính vào chi phí quản lý:** Nợ 6425 / Có 1381
   - **Thừa quỹ trả lại đối tượng:** Nợ 3381 / Có 111
   - **Thừa quỹ ghi nhận thu nhập:** Nợ 3381 / Có 711

**In biên bản kiểm kê theo Mẫu 08a** — khổ A4 dọc, font Times New Roman, có 3 ô ký tên (Giám đốc — Kế toán trưởng — Thủ quỹ), bảng mệnh giá (nếu có), kết luận và kiến nghị xử lý.

**Tài khoản mặc định cho xử lý chênh lệch** (1381, 3381, 1388, 6425, 711) cấu hình trong phần Thiết lập. Khi kế toán chọn tài khoản lần đầu, có thể tick "Lưu làm mặc định" để lần sau tự điền.

### 4.5 Tiền gửi có kỳ hạn

Quản lý sổ tiền gửi có kỳ hạn (TK 1281) — nghiệp vụ ngân quỹ thường xuyên của doanh nghiệp có dòng tiền dư.

**5 kiểu trả lãi hỗ trợ:**

| Kiểu | Mô tả | Lịch trả lãi |
|------|-------|--------------|
| Lãi cuối kỳ | Nhận lãi 1 lần khi đáo hạn | 1 lần, đúng ngày đáo hạn |
| Lãi hàng tháng | Nhận lãi mỗi tháng | N kỳ, mỗi tháng |
| Lãi hàng quý | Nhận lãi mỗi 3 tháng | N kỳ, mỗi quý |
| Lãi trả trước | Ngân hàng trừ lãi ngay khi gửi, cuối kỳ chỉ nhận gốc | 1 lần, ngay ngày gửi |
| Lãi kép | Lãi được cộng dồn vào gốc mỗi tháng, cuối kỳ nhận cả gốc lẫn lãi | N kỳ, lãi nhập gốc |

Công thức tính lãi dùng chuẩn **actual/365** (số ngày thực tế chia 365), theo quy định của Ngân hàng Nhà nước Việt Nam.

**Các bút toán chính:**

| Nghiệp vụ | Nợ | Có | Thời điểm |
|-----------|-----|-----|-----------|
| Gửi tiền | 1281 | 112 | Khi mở sổ |
| Gửi tiền (lãi trả trước) | 1281 (gốc danh nghĩa) | 112 (gốc thực) + 515 (lãi nhận trước) | Khi mở sổ |
| Nhận lãi định kỳ | 112 | 515 | Đến ngày trả lãi |
| Lãi nhập gốc (lãi kép) | 1281 | 515 | Đến ngày cộng lãi |
| Dự thu lãi cuối kỳ (VAS) | 1388 (phải thu khác) | 515 | Cuối kỳ kế toán |
| Tất toán đúng hạn | 112 | 1281 (+ 515 nếu còn lãi cuối kỳ) | Đáo hạn |
| Tất toán trước hạn | 112 | 1281 (+ 515 theo lãi suất không kỳ hạn) | Ngày tất toán |

**Tái tục:** khi đáo hạn, kế toán có thể tạo sổ mới từ sổ cũ. Nếu là lãi kép hoặc lãi cuối kỳ, số gốc sổ mới = gốc cũ + lãi luỹ kế.

**Quan trọng — bút toán luôn tạo ở trạng thái nháp.** Chứng từ ảnh hưởng sổ cái phải được kế toán trưởng kiểm tra trước khi ghi sổ.

**Cảnh báo đáo hạn:** trước X ngày (mặc định 7, cấu hình trong Thiết lập), kế toán trưởng nhận thông báo để chủ động kế hoạch (tất toán, tái tục, chuyển khoản mới).

### 4.6 Vay ngân hàng

Quản lý hợp đồng vay ngân hàng (TK 3411).

**2 kiểu trả nợ hỗ trợ:**

| Kiểu | Mô tả |
|------|-------|
| Trả lãi hàng kỳ + gốc cuối kỳ | Mỗi kỳ chỉ trả lãi, gốc trả 1 lần khi đáo hạn |
| Trả đều gốc lẫn lãi (EMI) | Mỗi kỳ trả một khoản đều nhau, phần gốc tăng dần và phần lãi giảm dần |

Lãi vay có thể là **lãi suất cố định** hoặc **lãi suất thả nổi** (cho phép cập nhật giữa chu kỳ, các kỳ đã ghi sổ không thay đổi, các kỳ chưa đến hạn tính lại theo lãi suất mới).

**Các bút toán chính:**

| Nghiệp vụ | Nợ | Có | Thời điểm |
|-----------|-----|-----|-----------|
| Giải ngân | 112 | 3411 | Nhận tiền vay |
| Trả lãi định kỳ | 635 | 112 | Đến ngày trả |
| Trả gốc | 3411 | 112 | Đến ngày trả |
| Trả đều gốc + lãi (EMI) | 3411 (phần gốc) + 635 (phần lãi) | 112 | Đến ngày trả |
| Dự chi lãi vay (VAS) | 635 | 335 (chi phí phải trả) | Cuối kỳ kế toán |
| Tất toán trước hạn | 3411 + 635 (lãi pro-rata) | 112 | Ngày tất toán |

Như tiền gửi, **bút toán luôn ở trạng thái nháp**, kế toán trưởng duyệt. Có cảnh báo đáo hạn trước X ngày.

### 4.7 Dự thu / dự chi lãi (VAS)

Theo chuẩn mực VAS, lãi phải được ghi nhận theo cơ sở dồn tích:

- **Dự thu lãi tiền gửi** tại thời điểm cuối kỳ nếu kỳ lãi chưa đến ngày nhận: Nợ 1388 / Có 515.
- **Dự chi lãi vay** tại thời điểm cuối kỳ nếu kỳ lãi chưa đến ngày trả: Nợ 635 / Có 335.

Kế toán có thể tạo các bút toán này thủ công trên form tiền gửi / khoản vay (nút riêng). Tài khoản dự thu / dự chi cấu hình trong Thiết lập.

### 4.8 Tự động hoá & Cảnh báo

- **Công việc nền chạy hàng ngày:** quét các kỳ trả lãi / trả nợ đã đến hạn, tự tạo bút toán nháp; đánh dấu các sổ / khoản vay đã đáo hạn; gửi cảnh báo trước X ngày.
- **Nguyên tắc:** hệ thống tạo nháp, con người duyệt. Không có trường hợp hệ thống tự ghi sổ chứng từ ảnh hưởng sổ cái.
- Các tài khoản mặc định (tiền gửi, doanh thu lãi, nợ vay, chi phí lãi vay, các tài khoản chờ xử lý, tài khoản xử lý chênh lệch quỹ) đặt tại một trang **Thiết lập kế toán Việt Nam** duy nhất, chỉ kế toán trưởng được sửa. Mỗi sổ / khoản vay kế thừa mặc định nhưng cho phép override từng chứng từ nếu công ty có nhiều tài khoản chi tiết (ví dụ 1281 VCB, 1281 BIDV).

### 4.9 Kho hàng — cấm xuất âm (FB-2026-00832)

- **Quy tắc:** Stock Settings.allow_negative_stock = **0** mặc định cho mọi site cài vn_accounting. Mọi Stock Entry / Sales Invoice / Delivery Note xuất kho làm balance < 0 sẽ bị ERPNext chặn với `NegativeStockError`.
- **Vì sao:** Yêu cầu của kế toán trưởng — DN có bán thiết bị + thi công công trình thì kho phải có hàng thật trước khi xuất, không thể xuất "khống". Tránh sai lệch giá vốn khi xuất từ một số dư âm.
- **Cách áp dụng:** Hook `vn_accounting.install._enforce_no_negative_stock` chạy mỗi `after_install` + `after_migrate`, idempotent — chỉ ghi khi giá trị hiện tại ≠ 0. Nếu kế toán muốn tạm bật lại (gia công, tạm xuất tái nhập), vào Desk → Stock Settings → tick "Allow Negative Stock" — hook sẽ trả về 0 ở migrate kế tiếp; nên giữ tay tới khi xong nghiệp vụ rồi tắt lại.

---

## 5. Workflow & Trạng thái

### 5.1 Tiền gửi có kỳ hạn

```
Nháp → (duyệt & gửi tiền) → Đang hiệu lực → (đến ngày đáo hạn) → Đáo hạn → (tất toán) → Đã tất toán
                                         ↘ (tất toán trước hạn) → Đã tất toán trước hạn
```

- **Nháp:** kế toán viên nhập thông tin. Chưa tạo bút toán.
- **Đang hiệu lực:** sau khi kế toán trưởng duyệt. Hệ thống tạo bút toán gửi tiền (nháp) và sinh lịch trả lãi.
- **Đáo hạn:** khi đến ngày đáo hạn, hệ thống tự chuyển trạng thái.
- **Đã tất toán / Đã tất toán trước hạn:** sau khi bút toán tất toán được ghi sổ.

### 5.2 Khoản vay ngân hàng

```
Nháp → (duyệt & giải ngân) → Đang hiệu lực → (trả hết) → Đã tất toán
                                         ↘ (tất toán trước hạn) → Đã tất toán
```

### 5.3 Kiểm kê quỹ (sắp triển khai)

```
Nháp → Đã kiểm đếm → Đã duyệt → Đóng                          (không chênh lệch)
                                → Chờ xử lý chênh lệch → Đã xử lý  (có chênh lệch)
```

- Kế toán viên tạo và nhập số đếm → Đã kiểm đếm.
- Kế toán trưởng kiểm tra + gán người ký → Đã duyệt.
- Nếu cân bằng → Đóng.
- Nếu lệch → tạo bút toán bước 1 (chờ xử lý) → Chờ xử lý chênh lệch → tạo bút toán bước 2 (xử lý cụ thể) → Đã xử lý.

---

## 6. Edge cases nghiệp vụ

Các tình huống bất thường mà app đã tính đến:

1. **Kiểm kê cùng ngày có giao dịch chưa ghi sổ.** Số dư sổ sách chỉ lấy các bút toán đã ghi sổ (post). Các bút toán nháp không ảnh hưởng. Kế toán có trách nhiệm đảm bảo sổ được cập nhật trước khi kiểm kê.
2. **Công ty có nhiều quỹ tiền mặt (nhiều tài khoản 111x).** Mỗi biên bản kiểm kê ứng với 1 tài khoản quỹ. Kiểm kê toàn bộ = nhiều biên bản cùng ngày.
3. **Kiểm kê đột xuất khi bàn giao thủ quỹ.** Chọn loại "Đột xuất", ghi rõ lý do trong biên bản. Không có logic khác biệt về bút toán.
4. **Tất toán tiền gửi trước hạn.** Lãi tính lại theo lãi suất không kỳ hạn × số ngày thực tế / 365. Các kỳ lãi đã ghi sổ trước đó vẫn giữ nguyên; nếu có chênh lệch (lãi đã trả vượt lãi thực hưởng) sẽ là bút toán điều chỉnh bổ sung.
5. **Tiền gửi lãi trả trước — gốc danh nghĩa so với gốc thực.** Gốc ghi sổ trên TK 1281 là gốc danh nghĩa của sổ. Số tiền thực chuyển từ TK 112 = gốc danh nghĩa trừ lãi trả trước. Phần lãi trả trước ghi ngay vào doanh thu hoạt động tài chính TK 515.
6. **Đáo hạn rơi vào ngày nghỉ.** Hệ thống vẫn tạo bút toán nháp đúng ngày đáo hạn theo hợp đồng. Kế toán tự điều chỉnh ngày ghi sổ khi duyệt, căn cứ ngày tiền thực về tài khoản.
7. **Vay lãi suất thả nổi, ngân hàng cập nhật giữa chu kỳ.** Kế toán dùng nút "Cập nhật lãi suất", nhập lãi mới và ngày hiệu lực. Hệ thống sinh lại lịch từ kỳ chưa ghi sổ đầu tiên. Các kỳ đã ghi sổ giữ nguyên.
8. **Trả nợ vay sớm hơn kỳ hạn.** Kế toán có thể duyệt bút toán trước ngày dự kiến. Kỳ đó được đánh dấu đã ghi sổ, công việc nền hàng ngày bỏ qua khi gặp.
9. **Vay giải ngân nhiều đợt.** Mỗi đợt là một hợp đồng vay riêng. App không hỗ trợ giải ngân từng phần trên cùng 1 record để tránh phức tạp hoá lịch trả nợ.
10. **Công ty có nhiều tài khoản chi tiết cho tiền gửi** (ví dụ 1281.01 VCB, 1281.02 BIDV). Mặc định từ Thiết lập, mỗi sổ cho phép override tài khoản chi tiết.
11. **Lãi kép.** Mỗi kỳ, lãi được cộng vào gốc, kỳ tiếp theo tính lãi trên gốc đã tăng. Cuối kỳ nhận cả gốc luỹ kế.
12. **Chênh lệch kiểm kê quỹ đã tạo bút toán bước 1 nhưng chưa xử lý bước 2.** Biên bản ở trạng thái "Chờ xử lý chênh lệch". TK 1381/3381 vẫn còn số dư cho đến khi bước 2 được ghi sổ. Đây là hành vi đúng chuẩn VAS.

---

## 7. Tham chiếu pháp lý

- **Thông tư 99/2025/TT-BTC** — Chế độ kế toán doanh nghiệp hiện hành. Hợp nhất và thay thế TT200/2014/TT-BTC (doanh nghiệp lớn) và TT133/2016/TT-BTC (doanh nghiệp nhỏ và vừa).
- **Chuẩn mực kế toán Việt Nam (VAS)** — cơ sở cho các nghiệp vụ dồn tích (dự thu/dự chi lãi), quy trình kiểm kê tài sản 2 bước (chờ xử lý → xử lý).
- **Mẫu 08a-TT** (Biên bản kiểm kê quỹ tiền mặt) — biểu mẫu pháp định, app tuân thủ format 3 chữ ký (thủ quỹ + kế toán trưởng + giám đốc).
- **Quy định actual/365 của Ngân hàng Nhà nước Việt Nam** — cơ sở tính lãi tiền gửi / lãi vay theo số ngày thực tế.

Các thông tư cũ (TT200, TT133) được nhắc đến như ngữ cảnh lịch sử, nhưng mọi tính năng bản địa hoá của app đều dựa trên TT99/2025 hiện hành.

---

## 8. Ngoài phạm vi

Các tính năng dưới đây chưa có trong app (sẽ bổ sung ở các phase sau, hoặc nằm ở các app khác).

> **Cập nhật 2026-05-11:** Báo cáo tài chính pháp định (B01–B09-DN), sổ nhật ký chung & sổ cái, kết chuyển cuối kỳ, khóa sổ kỳ, phân bổ chi phí mua hàng (LCV), và giá thành sản xuất cơ bản — đã chuyển từ "Ngoài phạm vi" vào kế hoạch phát triển hiện tại. Xem các mục 11–14 dưới đây.

**Thuế** (vẫn ngoài phạm vi, sẽ bổ sung sau):
- Tờ khai thuế GTGT (Mẫu 01/GTGT)
- Tờ khai thuế TNDN (Mẫu 03/TNDN)
- Tờ khai thuế TNCN (Mẫu 05/KK-TNCN)
- Bảng kê hoá đơn GTGT đầu vào / đầu ra

**Hoá đơn điện tử** — chưa tích hợp trong app này. Đang do module riêng (einvoice) đảm nhiệm.

## 10. Dự báo dòng tiền

### 10.1 Mục đích

Cho phép kế toán trưởng và ban giám đốc nhìn trước dòng tiền vào/ra trong 3-12 tháng tới, từ tất cả nguồn: hợp đồng dịch vụ, phương án kinh doanh (hoa hồng), ngân quỹ (tiền gửi/vay), pipeline mua bán (báo giá, đơn hàng, hoá đơn chưa thanh toán), lương, thuế, và chi phí hoạt động dự báo từ lịch sử.

Dự báo dòng tiền không lưu vào cơ sở dữ liệu — dữ liệu được tính toán theo thời gian thực mỗi lần người dùng mở trang, đảm bảo luôn phản ánh đúng trạng thái hiện tại của tất cả chứng từ.

### 10.2 Nguyên tắc nghiệp vụ

**Số dư đầu kỳ** = TK 111 (tiền mặt) + TK 112 (tiền gửi ngân hàng) + TK 113 (tiền đang chuyển) tại ngày hiện tại. Đây là số dư sổ cái thực tế (chỉ tính các bút toán đã ghi sổ, không tính nháp).

**Mức độ chắc chắn** — mỗi khoản dự báo được phân loại theo 4 cấp:

| Cấp | Tên | Ý nghĩa | Ví dụ |
|-----|-----|---------|-------|
| 1 | **Quá hạn** | Đã quá hạn thanh toán, chưa thu/chi — chỉ số sức khoẻ tài chính | Hoá đơn bán SI-001 due_date 15/3 nhưng nay 22/4 vẫn chưa nhận tiền |
| 2 | **Cam kết** | Ràng buộc pháp lý: đã xuất hoá đơn, đã ký hợp đồng, lịch ngân hàng | Hoá đơn mua PI-045 due_date 30/4, lãi tiền gửi đáo hạn 15/5 |
| 3 | **Khả năng cao** | Đã xác nhận nhưng chưa xuất hoá đơn | Đơn hàng bán SO-023 chưa bill, PAKD đang chờ duyệt |
| 4 | **Có thể** | Ước tính từ lịch sử hoặc chứng từ chưa chốt | Báo giá Q-007 còn hiệu lực, dự báo OpEx từ GL, thuế ước tính |

Người dùng có thể bật/tắt từng cấp trên giao diện để xem kịch bản khác nhau (ví dụ: chỉ xem "Cam kết" để có dự báo thận trọng, hoặc bật tất cả để có bức tranh đầy đủ).

**Quy tắc không đếm trùng** — mỗi khoản tiền chỉ được tính 1 lần trong forecast. Pipeline bán hàng tự động loại trùng theo giai đoạn:

```
Báo giá (status=Open) → chuyển SO → Báo giá tự mất status Open → loại khỏi forecast
  SO (per_billed < 100) → xuất SI → SO.per_billed = 100 → loại khỏi forecast
  SI (outstanding > 0) → nhận Payment → SI.outstanding = 0 → loại khỏi forecast
  Payment Entry → đã ghi vào GL → nằm trong số dư đầu kỳ
```

Mỗi provider chỉ query chứng từ thuộc giai đoạn của nó (dựa trên status, per_billed, outstanding_amount). Không cần phối hợp giữa các provider — bản thân dữ liệu đã loại trùng tự nhiên.

**Ngày dự kiến thu/chi** — không dùng ngày tạo chứng từ mà dùng ngày đến hạn (due_date hoặc ngày lịch trả nợ/lãi). Với mỗi nguồn, quy tắc xác định ngày cụ thể:

| Nguồn | Cách tính ngày dự kiến |
|-------|----------------------|
| Hoá đơn bán (SI) | `due_date`, điều chỉnh bởi hệ số trả chậm (xem 10.3) |
| Hoá đơn mua (PI) | `due_date` (công ty kiểm soát lịch trả nợ, không cần điều chỉnh) |
| Đơn hàng bán (SO) | Kỳ thanh toán đầu tiên chưa trả, hoặc `transaction_date + 30` |
| Đơn hàng mua (PO) | `schedule_date + 30` (buffer nhận hàng → nhận hoá đơn) |
| Báo giá (Q) | `valid_till`, hoặc `transaction_date + 30` nếu không có |
| Treasury (tiền gửi/vay) | Ngày trả lãi/gốc theo lịch trình trên form |
| Lương | Ngày 5 hàng tháng (ngày trả lương phổ biến VN) |
| Bảo hiểm (BHXH/BHYT/BHTN) | Ngày 20 hàng tháng |
| Thuế | GTGT/TNCN: ngày 20 tháng sau; TNDN: ngày 30 quý sau |
| OpEx recurring | Ngày 15 hàng tháng (ước lượng giữa tháng) |

### 10.3 Hệ số trả chậm (Payment Delay Factor)

Thanh toán B2B tại Việt Nam thường trễ hơn due_date. Nếu chỉ dùng due_date, dự báo sẽ lạc quan sai: hiển thị dòng tiền thu vào sớm hơn thực tế.

**Cách tính:** Với mỗi khách hàng, hệ thống quét lịch sử 12 tháng gần nhất — so sánh ngày thực nhận tiền (Payment Entry posting_date) với ngày hẹn (SI due_date). Lấy **trung vị** (median) của khoảng chênh lệch → đó là hệ số trả chậm.

Ví dụ: Khách hàng VNPT có 20 hoá đơn đã thanh toán, trung vị trả chậm = 18 ngày → mọi SI chưa thu của VNPT sẽ có `expected_date = due_date + 18 ngày`.

**Chỉ áp dụng cho thu vào (inflow)** từ hoá đơn bán. Các khoản chi ra do công ty kiểm soát, không cần điều chỉnh.

**Khách hàng mới** (chưa có lịch sử thanh toán) → hệ số = 0, dùng due_date gốc.

### 10.4 Số dư cuối kỳ cuộn (Rolling Balance)

Dự báo tính số dư cuối kỳ theo phương pháp cuộn:

```
Kỳ 1: Mở đầu = Số dư GL hôm nay (TK 111+112+113)
       Cuối kỳ = Mở đầu + Thu vào − Chi ra

Kỳ 2: Mở đầu = Cuối kỳ 1
       Cuối kỳ = Mở đầu + Thu vào − Chi ra

... tiếp tục cho mỗi kỳ (tuần hoặc tháng)
```

**Cảnh báo 3 cấp:**
- **Đỏ** — Số dư cuối kỳ < 0: thiếu hụt tiền mặt, cần vay ngắn hạn hoặc thu hồi công nợ gấp
- **Vàng** — Số dư cuối kỳ > 0 nhưng < ngưỡng tối thiểu: sắp cạn, cần theo dõi chặt
- **Bình thường** — Số dư cuối kỳ ≥ ngưỡng tối thiểu

**Ngưỡng tiền mặt tối thiểu** cấu hình trong Thiết lập kế toán Việt Nam (mặc định 500 triệu VND). Kế toán trưởng tự điều chỉnh theo quy mô doanh nghiệp. Trả lời câu hỏi CFO: "Tháng nào cần vay ngắn hạn? Tháng nào dư để gửi tiết kiệm?"

### 10.5 Các nguồn dữ liệu

#### Nhóm A — Chứng từ trực tiếp (7 nguồn)

Đọc số liệu trực tiếp từ các chứng từ hiện có trong hệ thống:

| # | Nguồn | Chiều | Chắc chắn | Số tiền | Ghi chú |
|---|-------|-------|-----------|---------|---------|
| 1 | Báo giá còn hiệu lực | Thu vào | Có thể | grand_total | Chưa chuyển SO |
| 2 | Đơn hàng bán chưa xuất HĐ | Thu vào | Khả năng cao | Phần chưa bill (grand_total × (100−per_billed)/100) | |
| 3 | Đơn hàng mua chưa nhận HĐ | Chi ra | Khả năng cao | Phần chưa bill | |
| 4 | Hoá đơn bán chưa thanh toán | Thu vào | Cam kết / Quá hạn | outstanding_amount | Có hệ số trả chậm |
| 5 | Hoá đơn mua chưa thanh toán | Chi ra | Cam kết / Quá hạn | outstanding_amount | |
| 6 | Lãi tiền gửi + đáo hạn gốc | Thu vào | Cam kết | Theo lịch trình Term Deposit | TK 1281 |
| 7 | Trả nợ vay (gốc + lãi) | Chi ra | Cam kết | Theo lịch trình Bank Loan | TK 3411 |

#### Nhóm B — Dự báo từ lịch sử (4 nguồn)

Phân tích sổ cái 6-12 tháng gần nhất để dự báo các khoản chi recurring:

| # | Nguồn | Chiều | Chắc chắn | Phương pháp dự báo | Ghi chú |
|---|-------|-------|-----------|-------------------|---------|
| 8 | Chi phí hoạt động recurring | Chi ra | Có thể | Phân tích GL TK 6xx (trừ lương) 12 tháng. Khoản nào xuất hiện ≥8/12 tháng = recurring. Dùng same-month-last-year (bắt mùa vụ), fallback trung vị. Cap 2× trung vị | Thuê VP, điện, internet, bảo trì... |
| 9 | Lương | Chi ra | Khả năng cao / Có thể | Nếu có HRMS: dùng Payroll Entry gần nhất. Không có: trung vị GL TK 334 6 tháng | Ngày 5 hàng tháng |
| 10 | Bảo hiểm XH/YT/TN | Chi ra | Có thể | Trung vị GL TK 3383+3384+3386 6 tháng | Ngày 20 hàng tháng |
| 11 | Thuế (GTGT + TNDN + TNCN) | Chi ra | Có thể | GTGT: GL TK 33311 trung vị 3 tháng, nộp tháng sau. TNDN: GL TK 3334, nộp theo quý (30/1, 30/4, 30/7, 30/10). TNCN: GL TK 3335 trung vị 3 tháng, nộp tháng sau | Theo lịch nộp thuế VN |

#### Nhóm C — App bên ngoài (mở rộng)

Các app khác tự đăng ký nguồn dữ liệu forecast qua cơ chế hook:

| App | Nguồn | Chiều | Chắc chắn |
|-----|-------|-------|-----------|
| dcnet_contract | Thu hợp đồng dịch vụ (billing projected) | Thu vào | Cam kết |
| dcnet_pakd | Chi hoa hồng/phí (commission pending) | Chi ra | Cam kết / Khả năng cao |
| (app tương lai) | Bất kỳ nguồn nào tuân theo schema | Tuỳ | Tuỳ |

### 10.6 Cơ chế mở rộng (Plugin Architecture)

Hệ thống dự báo không phụ thuộc vào bất kỳ app ngoài nào. Mỗi app tự đăng ký qua cơ chế hook `cash_flow_forecast_providers` của Frappe.

**Cách hoạt động:**
1. Khi người dùng mở trang Dự báo, hệ thống đọc danh sách tất cả provider đã đăng ký từ hooks
2. Gọi lần lượt từng provider → mỗi provider trả về danh sách các khoản dự báo
3. Mỗi khoản được kiểm tra tính hợp lệ (ngày, số tiền, chiều, mức chắc chắn)
4. Khoản không hợp lệ bị bỏ qua và ghi log — **không làm sập toàn bộ dự báo**
5. Nếu 1 provider lỗi (ví dụ app dcnet_contract bị lỗi), các provider còn lại vẫn chạy bình thường

Nếu app không cài đặt, forecast vẫn chạy bình thường với 11 provider mặc định (7 chứng từ + 4 dự báo). Khi cài thêm app có provider, dữ liệu tự động xuất hiện trên trang forecast mà không cần cấu hình gì.

### 10.7 Giao diện người dùng

Trang Dự báo dòng tiền (Frappe Page) cung cấp:

**Bộ lọc:**
- Chọn Công ty (bắt buộc)
- Chọn kỳ dự báo: 3, 6, hoặc 12 tháng
- Nhóm theo: Tháng hoặc Tuần

**Bật/tắt nguồn và mức chắc chắn:**
- 4 toggle mức chắc chắn: Quá hạn / Cam kết / Khả năng cao / Có thể — cho phép xem kịch bản thận trọng vs toàn diện
- Toggle từng nguồn riêng lẻ (ví dụ: tắt "OpEx projected" để xem ảnh hưởng)
- Tất cả toggle hoạt động ngay trên dữ liệu đã tải, không cần gọi lại server

**4 thẻ tổng hợp:** Tổng thu vào / Tổng chi ra / Thặng dư ròng / Số dư cuối kỳ dự kiến

**Biểu đồ:**
- Cột xanh = Thu vào, cột đỏ = Chi ra (theo kỳ)
- Đường xanh dương nét đứt = Số dư cuối kỳ cuộn
- Đường cam nét đứt = Ngưỡng tối thiểu
- Trục Y rút gọn theo đơn vị Việt: 1 tỷ = 1B, 1 triệu = 1M, 1 nghìn = 1K

**Bảng dữ liệu:**
- Dòng tổng hợp theo kỳ: Mở đầu | Thu vào | Chi ra | Ròng | MoM% | Cuối kỳ
- Dòng màu đỏ nếu cuối kỳ < 0 (thiếu hụt), vàng nếu < ngưỡng
- Click để mở chi tiết: từng khoản trong kỳ đó, có link đến chứng từ gốc

**Xuất dữ liệu:** Tải CSV gồm 2 phần — Summary (theo kỳ) + Detail (từng khoản).

### 10.8 Edge cases

1. **Khách hàng mới, chưa có lịch sử thanh toán.** Hệ số trả chậm = 0, dùng due_date gốc. Khi khách hàng có ≥3 Payment Entry, hệ số bắt đầu có ý nghĩa thống kê.
2. **Hoá đơn không có due_date.** Dùng posting_date + 30 ngày làm due_date ước lượng.
3. **Đơn hàng mua chưa nhận hàng.** PO expected_date = schedule_date + 30 ngày (buffer từ nhận hàng → nhận hoá đơn → thanh toán).
4. **Tiền gửi đáo hạn nhưng chưa tất toán.** Vẫn hiện trong forecast (status Matured, chưa Settled) — lãi + gốc sẽ thu về khi tất toán.
5. **Khoản vay đã trả 1 phần.** Chỉ các kỳ chưa Booked mới xuất hiện trong forecast.
6. **Không có dữ liệu lịch sử (công ty mới).** Các provider dự báo (OpEx, lương, thuế) trả về danh sách rỗng — forecast chỉ hiện các khoản chứng từ trực tiếp.
7. **Chi phí có tính mùa vụ.** Provider OpEx dùng same-month-last-year (nếu có dữ liệu cùng tháng năm trước) để bắt chu kỳ mùa vụ (ví dụ: Q4 spike do thưởng cuối năm, gia hạn license).
8. **Một app provider bị lỗi.** Các provider còn lại vẫn trả dữ liệu bình thường. Lỗi được ghi log và hiển thị cho người dùng biết có nguồn bị thiếu.

Chi tiết kỹ thuật: xem spec `docs/specs/2026-04-20-cash-flow-forecast-design.md`.

---

**Nghiệp vụ ngân quỹ mở rộng** (phase 2):
- Trái phiếu (TK 1282), cho vay (TK 1283)
- Nợ thuê tài chính (TK 3412)
- Đa ngoại tệ cho tiền gửi / vay
- Kiểu trả nợ "Gốc đều + lãi giảm dần"
- Tài sản đảm bảo (thế chấp)
- Phạt lãi quá hạn

**Kế toán lương** — được đảm nhiệm bởi HRMS chuẩn của Frappe, chưa có bản địa hoá theo mẫu VN (BHXH/BHYT/BHTN, thuế TNCN). Sẽ bổ sung.

**Khấu hao TSCĐ theo TT45/2013** — ERPNext có module Asset chuẩn; phần bản địa hoá (sổ TSCĐ mẫu S21-DN, phân bổ CCDC) thuộc kế hoạch bổ sung.

**Nhập số dư đầu kỳ từ Misa** — công cụ migration dự kiến phát triển riêng cho dự án chuyển đổi DCNET.

**Đối soát sao kê ngân hàng tự động** — do app riêng `vn_banking` đảm nhiệm (import sao kê, tự động match hoá đơn bán / mua, tạo Payment Entry).

---

## 11. Phân bổ chi phí mua hàng vào giá vốn (LCV)

### 11.1 Mục đích

Khi doanh nghiệp mua hàng hóa hoặc nguyên vật liệu, ngoài giá trị hóa đơn của nhà cung cấp còn phát sinh các chi phí phụ — vận chuyển, bốc xếp, bảo hiểm, lưu kho lưu bãi, phí hải quan, thuế nhập khẩu, hoa hồng mua hàng. Theo chuẩn VAS và TT99/2025, các khoản này phải được **cộng vào giá vốn hàng nhập kho** (TK 156 cho hàng hóa, TK 152 cho NVL, TK 153 cho CCDC, TK 155 cho thành phẩm gia công), KHÔNG hạch toán vào chi phí bán hàng (TK 641) hoặc chi phí quản lý (TK 642).

Nếu hạch toán sai (đẩy thẳng vào 641/642), giá vốn xuất kho sẽ thấp giả tạo, biên lợi nhuận gộp bị méo, báo cáo P&L mất ý nghĩa quản trị.

Mục này áp dụng cho **mọi doanh nghiệp** có hoạt động mua hàng — thương mại, sản xuất, dịch vụ có vật tư đầu vào.

### 11.2 Người dùng

- **Kế toán viên (mua hàng / kho):** nhập phiếu phân bổ chi phí khi nhận hóa đơn vận chuyển, hóa đơn hải quan, hóa đơn bảo hiểm liên quan đến lô hàng đã nhập kho.
- **Kế toán trưởng:** duyệt phiếu phân bổ, kiểm tra tiêu thức phân bổ hợp lý, cấu hình tài khoản chi phí mặc định cho từng loại phụ phí.

### 11.3 Nguyên tắc nghiệp vụ

**Cơ sở dữ liệu:** dùng tính năng **Phiếu phân bổ chi phí mua hàng** (Landed Cost Voucher — LCV) sẵn có của ERPNext. App vn_accounting bổ sung cấu hình mặc định theo TT99/2025 và bản địa hóa giao diện.

**3 loại tình huống chính:**

| Tình huống | Ví dụ | Phân bổ vào TK |
|---|---|---|
| Mua trong nước có chi phí vận chuyển | Mua thiết bị từ tỉnh khác, có hóa đơn vận chuyển riêng | 156 / 152 / 155 / 153 (theo loại hàng) |
| Nhập khẩu chính ngạch | Hàng nhập khẩu có tờ khai hải quan, thuế NK, VAT NK | 156 / 152 + 3333 + 1331 (xem 11.4) |
| Mua hàng kèm phụ phí giao tận kho | Phí giao hàng do nhà cung cấp tính trên hóa đơn riêng | 156 / 152 |

**Tiêu thức phân bổ:** mỗi phiếu LCV phân bổ tổng phụ phí xuống các dòng hàng theo 1 trong 4 tiêu thức (kế toán chọn theo bản chất chi phí):

| Tiêu thức | Khi nào dùng |
|---|---|
| Theo giá trị (Amount) | Mặc định. Phụ phí tỷ lệ với giá hàng (hoa hồng, bảo hiểm theo % giá trị). |
| Theo số lượng (Qty) | Khi phụ phí cố định trên mỗi đơn vị (phí kiểm dịch theo con, theo container). |
| Theo khối lượng (Weight) | Phí vận chuyển tính theo kg/tấn. |
| Theo thể tích (Volume) | Phí vận chuyển hàng cồng kềnh tính theo m³. |

### 11.4 Đặc thù nhập khẩu (VN)

Hàng nhập khẩu chính ngạch có **3 khoản thuế + phí** đặc thù, mỗi khoản đi vào tài khoản khác nhau:

| Khoản | TK | Có cộng vào giá vốn không? |
|---|---|---|
| Thuế nhập khẩu (NK) | 3333 | ✅ Có — toàn bộ cộng vào TK 156/152 |
| Thuế tiêu thụ đặc biệt (TTĐB) nhập khẩu | 3332 | ✅ Có — toàn bộ cộng vào giá vốn |
| VAT nhập khẩu — phần được khấu trừ | 33312 → 1331 | ❌ Không cộng giá vốn (được khấu trừ đầu vào) |
| VAT nhập khẩu — phần KHÔNG được khấu trừ | 33312 | ✅ Có — cộng vào giá vốn (DN không kinh doanh hàng chịu thuế, hoặc hàng dùng phúc lợi, biếu tặng) |
| Phí hải quan, kiểm dịch, kiểm hóa | (TK theo cấu hình) | ✅ Có — cộng giá vốn |
| Phí lưu container, lưu bãi | (TK theo cấu hình) | ✅ Có — cộng giá vốn |
| Phí giao nhận, đại lý hải quan | (TK theo cấu hình) | ✅ Có — cộng giá vốn |

Kế toán trưởng cần khai báo trên LCV: phần VAT NK nào được khấu trừ (1331), phần nào cộng giá vốn. Mặc định: toàn bộ được khấu trừ (giả định DN kinh doanh hàng chịu VAT bình thường).

### 11.5 Quy trình

1. Kế toán mua hàng tạo **Phiếu nhập mua (Purchase Receipt)** hoặc **Hóa đơn mua (Purchase Invoice)** từ nhà cung cấp chính → hàng vào kho với giá vốn = giá hóa đơn.
2. Khi nhận thêm hóa đơn của bên vận chuyển / hải quan / bảo hiểm → kế toán tạo **Phiếu phân bổ chi phí mua hàng (LCV)** mới.
3. Chọn các Phiếu nhập mua liên quan (1 hoặc nhiều) → hệ thống liệt kê tất cả dòng hàng.
4. Nhập từng dòng phụ phí: loại chi phí, số tiền, tài khoản chi phí (mặc định từ cấu hình, được sửa).
5. Chọn tiêu thức phân bổ → hệ thống tính giá trị phụ phí cộng vào từng dòng hàng.
6. Duyệt phiếu → hệ thống cập nhật giá vốn hàng nhập kho và sinh bút toán điều chỉnh.

### 11.6 Cấu hình tài khoản

**Mỗi loại phụ phí có TK riêng cấu hình trong Thiết lập kế toán Việt Nam → mục "Phân bổ chi phí mua hàng":**

| Loại phụ phí | TK gợi ý (mặc định TT99/2025) | Sửa được |
|---|---|---|
| Vận chuyển | 1561 (hoặc 152/155) | ✅ |
| Bốc xếp | 1561 | ✅ |
| Bảo hiểm hàng hóa | 1561 | ✅ |
| Lưu kho, lưu bãi | 1561 | ✅ |
| Hoa hồng mua hàng | 1561 | ✅ |
| Thuế nhập khẩu | 3333 | ✅ |
| Thuế TTĐB nhập khẩu | 3332 | ✅ |
| VAT NK (khấu trừ) | 1331 | ✅ |
| VAT NK (không khấu trừ) | 1561 | ✅ |
| Phí hải quan, kiểm dịch | 1561 | ✅ |
| Phí lưu cont | 1561 | ✅ |
| Phí đại lý hải quan | 1561 | ✅ |
| Khác (tự đặt tên) | (do người dùng nhập) | ✅ |

Mỗi dòng có nút **"Sửa TK"** ngay trên form LCV để override cho lô hàng cụ thể (vd: lô hàng NVL → đổi TK 1561 thành TK 152). Không hardcode TK trong code.

### 11.6a Tách 1561 / 1562 theo VAS TT99/2025 (FB-2026-00836)

Theo TT99/2025, **TK 156 là group**, gồm 2 con: **1561 - Giá mua hàng hoá** và **1562 - Chi phí thu mua hàng hoá**. ERPNext core không phân biệt cấu trúc này (1 warehouse = 1 inventory account), do đó vn_accounting áp dụng cơ chế 3 lớp:

**Lớp 1 — LCV core (ERPNext, tự động):** Khi LCV submit, ERPNext recompute valuation_rate Item bao gồm cả phụ phí, sinh GL Dr 1561 (warehouse account của Item) / Cr expense_account của row.

**Lớp 2 — JE bù (vn_accounting hook on_submit LCV, tự động):** Sau khi LCV submit, hook `lcv_create_inventory_split_je` lập + submit thêm 1 JE: Dr `<landed_cost_inventory_account>` (default 1562) / Cr `<warehouse account của Item>` (1561) với amount = tổng phụ phí. Net effect: 1561 chỉ chứa giá mua, 1562 chứa phụ phí. Stock Ledger không thay đổi (ERPNext core đã update valuation_rate đầy đủ).

JE bù **link reference đến LCV** (Comment có hyperlink, plus `reference_type=Landed Cost Voucher` trong JE accounts). Hủy LCV → JE bù tự hủy.

**Lớp 3 — Phân bổ cuối kỳ vào COGS (DocType `Inventory Cost Reallocation`, manual):** Khi xuất kho, ERPNext core post Dr 632 / Cr 1561 (full giá vốn = giá mua + phụ phí). Vì 1561 chỉ chứa giá mua, càng xuất kho 1561 càng âm; 1562 chỉ tăng từ LCV không bao giờ giảm. Cuối tháng/quý, kế toán mở **Sidebar → Giá thành → Phân bổ phụ phí vào giá vốn (cuối kỳ)** → tạo phiếu mới → bấm "Tính lại" → submit. JE: Dr 1561 / Cr 1562, amount = (số dư 1562) × (COGS kỳ / tổng giá vốn cộng dồn). Phương pháp xấp xỉ chấp nhận được cho audit VAS — có thể chỉnh tay trước khi submit.

**Cấu hình:**
- `LCV Allocation Settings.default_landed_cost_inventory_account` (Settings, default 1562)
- `LCV Allocation Settings.auto_create_inventory_split_je` (Settings, default ON — tắt nếu DN không tách 1561/1562 mà giữ flat 156)
- `Landed Cost Voucher.landed_cost_inventory_account` (header, override per LCV)
- `Landed Cost Taxes and Charges.landed_cost_inventory_account` (per-row, override per dòng phụ phí)

**Edge case — DN không muốn tách:** đặt Settings field `auto_create_inventory_split_je = 0`. Khi đó LCV chỉ chạy lớp 1 (mọi phụ phí lump vào 1561 — sai cấu trúc VAS chặt nhưng chấp nhận được cho DN nhỏ + audit ít khắt khe).

### 11.7 Edge cases

1. **Hóa đơn vận chuyển nhận trước hóa đơn mua hàng.** Chi phí vận chuyển treo tạm trên TK 1388 hoặc 331, chờ đến khi có Phiếu nhập mua thì tạo LCV để chuyển sang giá vốn. Cảnh báo: "X khoản phí chưa phân bổ tới lô hàng nào" trên dashboard mua hàng.
2. **1 lô hàng có nhiều hóa đơn phụ phí.** Mỗi hóa đơn phụ phí = 1 LCV. Một Phiếu nhập mua có thể nhận nhiều LCV phân bổ tới cùng các dòng hàng.
3. **Mua hàng nhiều loại trong cùng container.** Phân bổ vận chuyển theo khối lượng/thể tích, không theo giá trị — tránh hàng nhẹ giá cao gánh phí vận chuyển bất hợp lý.
4. **VAT nhập khẩu một phần khấu trừ một phần không.** DN có hàng vừa kinh doanh (chịu VAT) vừa biếu tặng — kế toán tự nhập tỷ lệ khấu trừ vào LCV (vd: 80% khấu trừ → 1331, 20% cộng giá vốn).
5. **Đã duyệt LCV nhưng phát hiện sai số tiền hoặc tiêu thức.** Hủy LCV → giá vốn hàng nhập tự cập nhật lại theo trạng thái trước. Tạo LCV mới.
6. **Hàng đã xuất bán trước khi LCV được tạo.** Giá vốn xuất bán dựa trên giá tại thời điểm xuất → có chênh lệch sau khi LCV duyệt. ERPNext tự sinh bút toán điều chỉnh chênh lệch vào TK 632 kỳ hiện hành. Không sửa retroactive sang kỳ đã khóa.
7. **DN nhỏ không nhập khẩu.** Chỉ cần cấu hình các loại chi phí phổ thông (vận chuyển, bốc xếp, bảo hiểm). Phần nhập khẩu để mặc định, không dùng đến.

---

## 12. Giá thành sản xuất

### 12.1 Mục đích

Cho doanh nghiệp **sản xuất** (chế tạo sản phẩm, gia công, dịch vụ có tập hợp chi phí theo đối tượng) — tính giá thành thực tế của sản phẩm/đơn hàng theo từng kỳ kế toán, làm cơ sở:

- Nhập kho thành phẩm với giá vốn đúng (TK 155 nhận từ TK 154)
- Tính giá vốn hàng bán (TK 632) khi xuất bán
- So sánh giá thành kế hoạch và thực tế để quản trị chi phí

Mục này **không bắt buộc với doanh nghiệp thương mại thuần** (không có hoạt động sản xuất, chỉ mua đi bán lại). Doanh nghiệp dịch vụ và xây lắp dùng mẫu cấu hình tương tự nhưng có thể đơn giản hóa.

### 12.2 Người dùng

- **Kế toán sản xuất:** tập hợp chi phí 621/622/627 theo đối tượng tính giá thành (sản phẩm, đơn hàng, công trình); chốt sản phẩm dở dang cuối kỳ; chạy tính giá thành cuối kỳ.
- **Kế toán trưởng:** duyệt bút toán kết chuyển 621/622/627 → 154 và 154 → 155; cấu hình tiêu thức phân bổ TK 627.
- **Quản đốc / quản lý sản xuất:** cung cấp dữ liệu vật lý (giờ máy, giờ công, sản lượng hoàn thành, sản phẩm dở dang) — không trực tiếp thao tác trên hệ thống.

### 12.3 Nguyên tắc nghiệp vụ

**3 yếu tố chi phí cốt lõi theo TT99/2025:**

| TK | Tên | Bản chất |
|---|---|---|
| 621 | Chi phí nguyên liệu, vật liệu trực tiếp | NVL chính, NVL phụ dùng trực tiếp cho sản xuất sản phẩm. Tập hợp trực tiếp theo đối tượng nếu được. |
| 622 | Chi phí nhân công trực tiếp | Lương + các khoản trích theo lương của công nhân sản xuất trực tiếp. |
| 627 | Chi phí sản xuất chung | Chi phí phân xưởng: khấu hao máy, điện nước phân xưởng, lương quản đốc, vật liệu phụ chung. Phân bổ theo tiêu thức. |

**Đối tượng tập hợp chi phí (Cost Object):** đây là điểm cấu hình quan trọng. Mỗi DN có cách tập hợp khác nhau:

| Loại DN | Đối tượng phổ biến |
|---|---|
| Sản xuất hàng loạt | Sản phẩm (mỗi SKU) |
| Sản xuất theo đơn hàng | Đơn hàng sản xuất (Work Order) |
| Xây lắp | Công trình / Hạng mục |
| Dịch vụ | Hợp đồng / Tuyến / Khách hàng |
| Gia công | Lô gia công |

App cho phép cấu hình đối tượng tập hợp trong Thiết lập kế toán Việt Nam → mục "Giá thành sản xuất". Mặc định: theo Sản phẩm.

**Tiêu thức phân bổ TK 627:** TK 627 không tập hợp trực tiếp được — phải phân bổ. Hỗ trợ các tiêu thức:

| Tiêu thức | Khi nào dùng |
|---|---|
| Giờ máy | DN có nhiều máy, sản phẩm khác nhau dùng máy khác nhau |
| Giờ công trực tiếp | Lao động thủ công chiếm tỷ trọng cao |
| Sản lượng hoàn thành | Sản phẩm tương đồng, đo bằng đơn vị tự nhiên |
| Chi phí NVL trực tiếp | Phân bổ đơn giản, theo tỷ lệ 621 |
| Chi phí nhân công trực tiếp | Phân bổ theo tỷ lệ 622 |
| Tổng chi phí trực tiếp | Phân bổ theo tỷ lệ (621+622) |

**Công thức giá thành đơn vị:**

```
Giá thành đơn vị = (DD đầu kỳ + Tổng chi phí phát sinh trong kỳ − DD cuối kỳ) / Sản lượng hoàn thành
DD = Sản phẩm dở dang (giá trị treo trên TK 154)
```

### 12.4 Quy trình cuối kỳ

1. **Khóa nghiệp vụ sản xuất kỳ:** đảm bảo tất cả Phiếu xuất kho NVL, Phiếu nhập kho thành phẩm, công làm sản xuất đã được ghi sổ.
2. **Tập hợp chi phí 621/622/627:** chạy báo cáo "Tập hợp chi phí sản xuất kỳ" theo đối tượng — kế toán đối chiếu số.
3. **Đánh giá sản phẩm dở dang cuối kỳ:** chọn phương pháp đánh giá DDCK (NVL chính, sản lượng tương đương, hoặc 50% chi phí chế biến). Nhập số liệu DDCK theo đối tượng.
4. **Phân bổ TK 627:** hệ thống áp tiêu thức cấu hình → phân bổ 627 xuống từng đối tượng.
5. **Tính giá thành:** hệ thống chạy công thức → ra giá thành đơn vị + tổng giá trị nhập kho thành phẩm theo từng đối tượng.
6. **Kế toán trưởng duyệt Bảng tính giá thành** → sinh 2 bút toán:
   - Kết chuyển 621/622/627 → 154 (chi phí về sản phẩm dở dang)
   - Nhập kho thành phẩm 154 → 155 (giá vốn = giá thành vừa tính)
7. Bút toán ở trạng thái nháp → kế toán trưởng ghi sổ.

### 12.5 Cấu hình tài khoản

Mỗi DN có cấu trúc tài khoản chi tiết riêng. App cấu hình mặc định + cho phép override:

| Vai trò | TK gợi ý (TT99/2025) | Sửa được |
|---|---|---|
| Chi phí NVL trực tiếp | 621 | ✅ Có thể chi tiết 6211 (NVL chính), 6212 (NVL phụ) |
| Chi phí nhân công trực tiếp | 622 | ✅ |
| Chi phí sản xuất chung | 627 | ✅ Có thể chi tiết 6271 (lương quản đốc), 6272 (vật liệu phụ), 6273 (CCDC), 6274 (khấu hao), 6277 (dịch vụ mua ngoài), 6278 (khác) |
| Sản phẩm dở dang | 154 | ✅ |
| Thành phẩm | 155 | ✅ |
| Giá vốn hàng bán | 632 | ✅ |

Trong wizard tính giá thành, hệ thống **luôn hiện sơ đồ bút toán** trước khi sinh JE (kế toán nhìn thấy "Nợ 154 / Có 621 + 622 + 627", "Nợ 155 / Có 154") — có nút "Sửa TK" cho từng dòng nếu DN dùng cấu trúc TK chi tiết khác.

### 12.6 Edge cases

1. **DN sản xuất nhỏ chỉ dùng TT99/2025 mẫu DN nhỏ — không có TK 621/622/627.** Mẫu DN nhỏ gộp chi phí sản xuất vào TK 154 trực tiếp. App tự nhận diện mẫu (đã có sẵn) → ẩn các trường 621/622/627, kế toán hạch toán thẳng 154.
2. **Sản xuất theo đơn hàng có sản phẩm hoàn thành dở chừng.** Đơn hàng X làm 100 SP, kỳ này hoàn thành 70, dở 30. Giá thành đơn vị tính trên 70 SP hoàn thành; chi phí của 30 SP dở dang chuyển sang kỳ sau (DDCK).
3. **DN gia công thuần** (chỉ nhận NVL của khách, không sở hữu NVL). Không có TK 621 — chỉ có 622 + 627. Doanh thu là phí gia công. Giá thành = (622 + 627) / sản lượng.
4. **Sản phẩm phụ phát sinh từ quy trình sản xuất.** Nếu sản phẩm phụ có giá trị → ghi giảm giá thành sản phẩm chính (Nợ 155 sản phẩm phụ / Có 154). Nếu giá trị không đáng kể → bỏ qua.
5. **Phế liệu thu hồi.** Bán phế liệu thu được tiền → ghi giảm giá thành (Nợ 111/112 / Có 154). Đây là điều chỉnh kỳ phát sinh.
6. **Sai sót phát hiện sau khi đã ghi sổ giá thành kỳ trước.** Không sửa retroactive. Tạo bút toán điều chỉnh kỳ hiện hành: nếu giá thành kỳ trước tính thiếu → Nợ 632 / Có 1388 (hoặc 154 tùy bản chất); nếu tính dư → Nợ 1388 / Có 632.
7. **DN thương mại được hỏi giá vốn nhập từ nước ngoài.** Đó không phải "giá thành sản xuất" — đó là **giá vốn hàng nhập khẩu**, dùng cơ chế LCV ở mục 11. Đừng nhầm.
8. **DN dịch vụ tính giá thành theo hợp đồng.** Đối tượng tập hợp = Hợp đồng. Khi hợp đồng kết thúc, kết chuyển giá thành về TK 632 (giá vốn dịch vụ) theo từng hợp đồng — không qua TK 155.

---

## 13. Kết chuyển cuối kỳ & Khóa sổ kỳ kế toán

### 13.1 Mục đích

Cuối mỗi kỳ kế toán (tháng / quý / năm), kế toán trưởng phải:

1. **Kết chuyển doanh thu và chi phí** về TK 911 (Xác định kết quả kinh doanh) → ra lãi/lỗ kỳ.
2. **Chuyển lãi/lỗ kỳ** về TK 421 (Lợi nhuận sau thuế chưa phân phối).
3. **Khóa sổ kỳ** — chốt số liệu, không cho phép sửa/xóa chứng từ trong kỳ đã khóa.

Đây là 2 nghiệp vụ pháp lý bắt buộc, phải làm trước khi xuất Báo cáo tài chính.

### 13.2 Người dùng

- **Kế toán trưởng:** chạy wizard kết chuyển, kiểm tra bút toán, duyệt, khóa sổ. Không ủy quyền cho kế toán viên.

### 13.3 Nguyên tắc nghiệp vụ

**Bút toán kết chuyển 1 — Doanh thu, thu nhập về 911 (bên Có):**

| TK chuyển | Nợ | Có |
|---|---|---|
| 511 — Doanh thu BH&CCDV | 511 (số dư Có cuối kỳ) | 911 |
| 512 — Doanh thu nội bộ | 512 | 911 |
| 515 — Doanh thu hoạt động tài chính | 515 | 911 |
| 711 — Thu nhập khác | 711 | 911 |

**Bút toán kết chuyển 2 — Chi phí về 911 (bên Nợ):**

| TK chuyển | Nợ | Có |
|---|---|---|
| 632 — Giá vốn hàng bán | 911 | 632 |
| 635 — Chi phí tài chính | 911 | 635 |
| 641 — Chi phí bán hàng | 911 | 641 |
| 642 — Chi phí quản lý DN | 911 | 642 |
| 811 — Chi phí khác | 911 | 811 |
| 821 — Chi phí thuế TNDN | 911 | 821 |

**Bút toán xác định kết quả — Lãi/lỗ về 421:**

- Nếu TK 911 dư Có (lãi): Nợ 911 / Có 4212 (Lợi nhuận sau thuế chưa phân phối kỳ này)
- Nếu TK 911 dư Nợ (lỗ): Nợ 4212 / Có 911

Sau bút toán này, TK 911 cân bằng (số dư = 0), TK 4212 phản ánh kết quả kỳ.

### 13.4 Quy trình kết chuyển

1. Kế toán trưởng mở wizard **Kết chuyển cuối kỳ** → chọn kỳ (tháng / quý / năm), chọn ngày kết chuyển (mặc định ngày cuối kỳ).
2. Hệ thống **hiện bảng đầy đủ các TK sẽ kết chuyển** + số dư hiện tại + TK đích (911) + nút "Sửa" cho từng dòng.
3. Hệ thống **hiện sơ đồ bút toán dự kiến** — đầy đủ 3 bút toán (doanh thu → 911, chi phí → 911, 911 → 421).
4. Kế toán trưởng kiểm tra, có thể:
   - Loại trừ TK nào đó (nếu không muốn kết chuyển kỳ này — vd: có TK đặc thù)
   - Đổi TK đích (mặc định 911, có thể dùng TK chi tiết 9111 nếu DN tách)
   - Đổi TK 421 đích (4212 cho lãi/lỗ kỳ, hoặc 4211 cho năm trước, hoặc TK chi tiết khác)
5. Duyệt wizard → hệ thống sinh **3 Phiếu kế toán (Journal Entry) ở trạng thái nháp** trong cùng ngày.
6. Kế toán trưởng kiểm tra từng phiếu nháp → ghi sổ (submit) tuần tự.

### 13.5 Quy trình khóa sổ kỳ

Sau khi kết chuyển xong:

1. Kế toán trưởng mở chức năng **Khóa sổ kỳ** → chọn ngày khóa.
2. Hệ thống **kiểm tra điều kiện** trước khi khóa:
   - Tất cả Phiếu kế toán trong kỳ phải ở trạng thái đã ghi sổ (không còn nháp / hủy)
   - Tất cả bút toán kết chuyển đã được tạo và ghi sổ
   - Bảng cân đối số phát sinh cân (tổng Nợ = tổng Có)
3. Nếu pass điều kiện → tạo **Phiếu khóa sổ kỳ (Period Closing Voucher)** ở trạng thái ghi sổ.
4. Sau khi khóa, các chứng từ trong kỳ:
   - **Không thể sửa hoặc hủy** — chỉ Quản trị viên hệ thống được mở khóa với lý do bằng văn bản (audit log).
   - Có thể **xem** bình thường.
   - Bút toán điều chỉnh kỳ sau (nếu phát hiện sai sót sau kiểm toán) hạch toán vào kỳ hiện hành, không sửa kỳ đã khóa.

### 13.6 Cấu hình tài khoản

Trong Thiết lập kế toán Việt Nam → mục "Kết chuyển cuối kỳ":

| Vai trò | TK mặc định (TT99/2025) | Sửa được |
|---|---|---|
| TK trung gian xác định KQKD | 911 | ✅ |
| TK lãi/lỗ kỳ | 4212 | ✅ |
| TK lãi/lỗ năm trước (nếu kết chuyển năm) | 4211 | ✅ |
| TK doanh thu được kết chuyển | 511, 512, 515, 711 | ✅ (chọn nhiều, có thể thêm/bớt) |
| TK chi phí được kết chuyển | 632, 635, 641, 642, 811, 821 | ✅ (chọn nhiều) |
| TK loại trừ khỏi kiểm tra cân đối khi khóa sổ | (rỗng) | ✅ (cho TK ngoại bảng nếu có) |

Trong wizard kết chuyển, kế toán có nút **"Cấu hình tài khoản kết chuyển"** mở thẳng tới mục này.

### 13.7 Edge cases

1. **DN có hoạt động đa ngoại tệ — cần đánh giá lại trước khi kết chuyển.** Bút toán đánh giá lại số dư gốc ngoại tệ (đánh giá lại 1112, 1122, 131, 331) thực hiện riêng, KHÔNG nằm trong wizard kết chuyển. Wizard sẽ cảnh báo nếu có TK ngoại tệ chưa được đánh giá lại trong kỳ.
2. **Kỳ đã khóa, phát hiện sai sót.** Không mở khóa kỳ. Hạch toán điều chỉnh vào kỳ hiện hành: tăng chi phí thì Nợ 632/642/... / Có 421 (hoặc 1388/331 tùy bản chất). Có ghi chú rõ trong diễn giải.
3. **DN khóa sổ theo tháng nhưng kết chuyển theo quý/năm.** Phiếu khóa sổ tháng KHÔNG bao gồm bút toán kết chuyển 911. Wizard kết chuyển và Khóa sổ là 2 chức năng riêng biệt — có thể chạy độc lập theo kỳ khác nhau.
4. **TK 911 không cân sau kết chuyển.** Có thể do TK chi phí/doanh thu chưa kết chuyển hết. Wizard kiểm tra: số dư TK 911 sau bút toán 2 phải = lãi/lỗ kỳ. Nếu không khớp → cảnh báo, kế toán phải tìm TK còn sót.
5. **Năm tài chính không trùng năm dương lịch.** App cho phép cấu hình năm tài chính bắt đầu từ tháng nào (mặc định 01/01). Kết chuyển năm vào ngày cuối năm tài chính.
6. **Kết chuyển nhiều lần trong kỳ (sửa sai).** Nếu kế toán phát hiện kết chuyển sai trước khi khóa sổ — hủy phiếu kế toán kết chuyển, sửa nguyên nhân, chạy lại wizard. Sau khi khóa sổ → không sửa được nữa.
7. **DN mới thành lập kỳ đầu tiên.** Không có số dư đầu kỳ. Kết chuyển bình thường. TK 4212 trước kết chuyển = 0.

---

## 14. Báo cáo tài chính pháp định (BCTC theo TT99/2025)

### 14.1 Mục đích

Sinh 4 báo cáo tài chính pháp định mà mọi doanh nghiệp **phải nộp cho cơ quan thuế** theo Thông tư 99/2025/TT-BTC:

| Mã | Tên (TT99/2025) | Mục đích |
|---|---|---|
| **B01-DN** | **Báo cáo tình hình tài chính** (đổi tên từ "Bảng cân đối kế toán" của TT200) | Cấu trúc tài sản và nguồn vốn tại thời điểm cuối kỳ |
| **B02-DN** | Báo cáo kết quả hoạt động kinh doanh | Doanh thu, chi phí, lợi nhuận trong kỳ |
| **B03-DN** | Báo cáo lưu chuyển tiền tệ (gián tiếp) | Dòng tiền vào/ra theo 3 hoạt động: kinh doanh, đầu tư, tài chính |
| **B09-DN** | Bản thuyết minh báo cáo tài chính | Diễn giải các chỉ tiêu trong B01-B03 |

> **Lưu ý đổi tên TT99/2025:** B01-DN không còn gọi là "Bảng cân đối kế toán" mà là **"Báo cáo tình hình tài chính"** (đồng bộ thuật ngữ IFRS — Statement of Financial Position). Sidebar, tiêu đề báo cáo, file xuất Excel phải dùng tên mới.

### 14.2 Người dùng

- **Kế toán trưởng:** chạy báo cáo, kiểm tra số liệu, xuất Excel theo mẫu để nộp; cấu hình mapping TK ↔ mã chỉ tiêu BCTC.
- **Cơ quan thuế / kiểm toán:** đọc báo cáo, drill từ mã chỉ tiêu xuống TK gốc và chứng từ.

### 14.3 Nguyên tắc nghiệp vụ — "Mã chỉ tiêu lấy số liệu từ TK nào?"

Mỗi báo cáo BCTC gồm hàng chục dòng (mã chỉ tiêu). Mỗi mã chỉ tiêu được tính từ **một công thức trên các tài khoản kế toán**.

**Ví dụ B01-DN:**

| Mã | Tên chỉ tiêu | Công thức mặc định (TT99/2025) |
|---|---|---|
| 110 | Tiền và các khoản tương đương tiền | Số dư Nợ cuối kỳ TK 111 + 112 + 113 |
| 121 | Đầu tư tài chính ngắn hạn | Số dư Nợ TK 121 + 128 (trừ 1281 tiền gửi NH) |
| 130 | Các khoản phải thu ngắn hạn | Số dư Nợ TK 131 + 136 + 138 + 141 + 1388 + (...) |
| 140 | Hàng tồn kho | Số dư Nợ TK 151 + 152 + 153 + 154 + 155 + 156 + 157 + 158 − Số dư Có TK 2294 (dự phòng) |

**Ví dụ B02-DN:**

| Mã | Tên chỉ tiêu | Công thức mặc định |
|---|---|---|
| 01 | Doanh thu BH&CCDV | Phát sinh Có TK 511 + 512 trong kỳ |
| 02 | Các khoản giảm trừ doanh thu | Phát sinh Nợ TK 521 trong kỳ |
| 10 | Doanh thu thuần (10 = 01 − 02) | (công thức tính giữa các mã) |
| 11 | Giá vốn hàng bán | Phát sinh Nợ TK 632 trong kỳ |

**Quy tắc cốt lõi: mỗi mã chỉ tiêu — kế toán trưởng phải SỬA được công thức.**

Lý do: DN khác nhau dùng TK chi tiết khác nhau. Vd:
- DN A dùng TK 511 phẳng → mã 01 = phát sinh Có 511.
- DN B tách chi tiết 5111 (hàng hóa), 5112 (thành phẩm), 5113 (dịch vụ) → mã 01 = 5111 + 5112 + 5113.
- DN C tách hơn nữa 51111, 51112... → mã 01 = filter all 5111x + 5112x + 5113x.

Không thể hardcode "TK 511" trong code. Phải cấu hình.

### 14.4 Cấu hình mapping TK ↔ mã chỉ tiêu

App cung cấp DocType cấu hình **BCTC Mapping** chứa toàn bộ công thức cho 4 báo cáo:

- **Khi cài app:** seed đầy đủ mapping mặc định theo TT99/2025 (lấy từ Phụ lục IV của thông tư).
- **Khi tạo Company mới (Vietnam):** clone mapping từ template → mỗi Company có 1 bản mapping riêng để có thể tùy chỉnh độc lập.
- **Trên trang BCTC Mapping:** mỗi dòng = 1 mã chỉ tiêu với các trường:
  - Mã (110, 01, ...) — read-only theo TT99/2025
  - Tên chỉ tiêu — read-only
  - Công thức TK — **sửa được**. Cú pháp đơn giản: `+TK,+TK,-TK` (cho TK lấy số dư hoặc phát sinh).
  - Loại số liệu: Số dư Nợ cuối kỳ / Số dư Có cuối kỳ / Phát sinh Nợ kỳ / Phát sinh Có kỳ / Công thức (tính từ mã khác)
  - Wildcard hỗ trợ: `511%` = mọi TK bắt đầu bằng 511.
- **Nút "Khôi phục mặc định TT99/2025"** — rollback toàn bộ mapping về template.
- **Nút "Khôi phục mặc định cho dòng này"** — rollback 1 mã chỉ tiêu cụ thể.

### 14.5 Quy trình xuất BCTC

1. Kế toán trưởng vào sidebar → mục **"Báo cáo tình hình tài chính (B01-DN)"** (hoặc B02/B03/B09).
2. Chọn Company + Kỳ báo cáo (Năm tài chính, Quý, Tháng).
3. Hệ thống chạy mapping → trả về bảng đầy đủ mã chỉ tiêu, tên, số kỳ này, số kỳ trước.
4. **Mỗi dòng có icon "ℹ" hover hiện công thức tính** (vd: "Mã 110 = 111 + 112 + 113 → tổng số dư Nợ cuối kỳ").
5. **Click vào số trên dòng** → drill xuống danh sách chứng từ gốc (Phiếu kế toán / Hóa đơn) đóng góp vào số đó.
6. Nút **"Cấu hình mapping"** mở thẳng BCTC Mapping của Company hiện tại.
7. Nút **"Xuất Excel"** → file Excel đúng layout TT99/2025 (font, cột, ký hiệu, ô trống) — có thể nộp trực tiếp.

### 14.6 4 báo cáo cụ thể

**B01-DN — Báo cáo tình hình tài chính**

- Cấu trúc 2 phần: **TÀI SẢN** (mã 100–270) và **NGUỒN VỐN** (mã 300–440). Phương trình: Tổng tài sản (mã 270) = Tổng nguồn vốn (mã 440).
- 2 cột số liệu: Số cuối kỳ + Số đầu năm.
- Lấy chủ yếu **số dư Nợ/Có cuối kỳ** của các TK.

**B02-DN — Báo cáo kết quả hoạt động kinh doanh**

- 18 mã chỉ tiêu từ Doanh thu (mã 01) → LN sau thuế (mã 60).
- 2 cột: Kỳ này + Kỳ trước.
- Lấy chủ yếu **phát sinh trong kỳ** của TK 5xx, 6xx, 7xx, 8xx.

**B03-DN — Báo cáo lưu chuyển tiền tệ (phương pháp gián tiếp)**

- 3 mục lớn:
  - I. Lưu chuyển tiền từ hoạt động kinh doanh (bắt đầu từ LN trước thuế + điều chỉnh)
  - II. Lưu chuyển tiền từ hoạt động đầu tư
  - III. Lưu chuyển tiền từ hoạt động tài chính
- Số tiền cuối kỳ trên báo cáo = số dư đầu kỳ + LCTT thuần kỳ. Đây là chỉ số đối chiếu với B01 (mã 110).

**B09-DN — Bản thuyết minh BCTC**

- Bản Word/Excel chứa diễn giải 100+ chỉ tiêu của B01-B03. App sinh **khung mẫu** + **số liệu sẵn** (chi tiết các TK lớn, biến động giữa 2 kỳ, các giao dịch trọng yếu). Kế toán trưởng điền nốt phần diễn giải bằng văn xuôi (chính sách kế toán, đặc thù DN, sự kiện sau ngày kết thúc kỳ).

### 14.7 Edge cases

1. **Kỳ đầu tiên — không có số liệu kỳ trước.** Cột "Kỳ trước" / "Số đầu năm" để trống (không hiển thị 0 — phân biệt với số dư thực = 0).
2. **DN dùng năm tài chính khác năm dương lịch.** Mặc định lấy theo năm tài chính trong Company. Người dùng có thể override khi chạy báo cáo.
3. **TK ngoài bảng (TK 00x).** Không vào BCTC chính. Phần thuyết minh B09 có mục riêng cho ngoại bảng.
4. **DN có công ty con — BCTC hợp nhất.** Ngoài phạm vi phase 1. Hệ thống chỉ sinh BCTC riêng từng Company; hợp nhất thủ công ngoài hệ thống.
5. **DN không hoạt động liên tục (giải thể, phá sản, ngừng hoạt động).** TT99/2025 quy định 4 mẫu riêng: B01-DNKLT, B02-DNKLT, B03-DNKLT, B09-DNKLT. Cấu hình "Tình trạng hoạt động" trên Company Settings → "Đang giải thể" / "Đang phá sản" / "Ngừng hoạt động" → hệ thống tự chuyển dùng bộ KLT thay vì DN thường. **Phase 1: chỉ làm bộ DN thường (liên tục)**. Bộ KLT bổ sung sau khi có Company thực tế cần dùng.
6. **Mapping bị sửa sai làm Tài sản ≠ Nguồn vốn.** Hệ thống kiểm tra phương trình B01 và cảnh báo nếu lệch. Có nút "Khôi phục mặc định TT99/2025" cho từng dòng để rollback nhanh.
7. **Số liệu BCTC khác Bảng cân đối số phát sinh.** Nếu lệch — luôn do mapping. Drill từ chỉ tiêu xuống TK gốc → tìm TK bị bỏ sót hoặc tính sai. Bảng cân đối số phát sinh (S06-DN) là nguồn dữ liệu gốc — BCTC chỉ là tái cấu trúc.
8. **DN cần báo cáo theo cấu trúc IFRS song song.** Ngoài phạm vi phase 1. Chỉ sinh BCTC theo TT99/2025.

---
