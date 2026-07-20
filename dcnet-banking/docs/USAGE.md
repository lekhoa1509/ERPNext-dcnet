# Hướng dẫn sử dụng VN Banking

Hướng dẫn dành cho kế toán viên — quy trình hàng ngày import sao kê ngân hàng và đối soát công nợ.

## Quy trình tổng quan

1. **Tải sao kê** — Mở workspace "Banking VN" → nhấn "Bank Reconcile"
2. **Chọn tài khoản ngân hàng** — chọn Bank Account từ dropdown
3. **Upload file** — kéo thả file Excel (.xlsx/.xls) hoặc HTML từ Internet Banking
4. **Xem kết quả đối soát** — hệ thống tự động phân tích và gợi ý khớp công nợ
5. **Xác nhận & tạo Payment Entry** — nhấn nút tạo phiếu thu/chi

## Ngân hàng hỗ trợ (v1)

| Ngân hàng | Định dạng | Ghi chú |
|-----------|-----------|---------|
| BIDV | Excel (.xlsx) | Sao kê tài khoản thanh toán |
| MB Bank | Excel (.xlsx) | Sao kê giao dịch |
| Sacombank | Excel (.xlsx) | Bảng sao kê |
| PG Bank | Excel (.xlsx) | Sao kê tài khoản |

## Bảng màu mức độ tin cậy

Mỗi giao dịch sau khi đối soát sẽ được gắn màu theo mức độ tin cậy:

| Màu | Mức | Ý nghĩa | Hành động |
|-----|-----|---------|-----------|
| :green_circle: Xanh lá | **High** | Khớp chính xác — số hóa đơn + số tiền đúng | Tự động tạo Payment Entry nháp; có thể submit hàng loạt |
| :yellow_circle: Vàng | **Medium** | Gợi ý tốt — số tiền khớp trong phạm vi dung sai | Xem chi tiết ở bảng bên, nhấn xác nhận để tạo PE |
| :orange_circle: Cam | **Low** | Khớp mờ — tên đối tác tương tự | Cần xác nhận thủ công (badge "Cần xác nhận") |
| :red_circle: Đỏ | **None** | Không tìm thấy khớp | Chọn đối tác/hóa đơn thủ công |

## Chi tiết bảng bên (Side Panel)

Khi nhấn vào một giao dịch, bảng bên hiển thị:

- **Thông tin giao dịch**: ngày, số tiền, nội dung chuyển khoản, số tham chiếu
- **Đối tác gợi ý**: tên, loại (Khách hàng / Nhà cung cấp)
- **Hóa đơn gợi ý**: danh sách hóa đơn khớp với số tiền phân bổ
- **Giải thích**: matcher nào đã khớp và lý do (ví dụ: "InvoiceNoMatcher: tìm thấy ACC-SI-2026-00045 trong nội dung chuyển khoản")
- **Chênh lệch**: nếu có chênh lệch nhỏ trong dung sai, hiển thị số tiền chênh lệch

## Tạo Payment Entry

### Tạo đơn lẻ
1. Nhấn vào giao dịch trong bảng
2. Xem chi tiết ở bảng bên → xác nhận đối tác và hóa đơn đúng
3. Nhấn nút "Tạo Payment Entry"
4. PE được tạo với: ngày giao dịch, số tiền, liên kết hóa đơn, phương thức thanh toán

### Tạo hàng loạt (Bulk)
1. Tích chọn nhiều giao dịch :green_circle: High
2. Nhấn "Tạo PE hàng loạt" → N phiếu PE nháp được tạo
3. Nhấn "Submit hàng loạt" → submit tất cả PE nháp của đợt import này

### Xử lý chênh lệch nhỏ
Khi chênh lệch nằm trong dung sai (ví dụ: phí chuyển khoản 1,000 VND):
- Nếu admin đã cấu hình **Tài khoản chênh lệch** trong Settings → PE tự động thêm dòng Deductions (ghi nợ vào TK 6415/6425/6427)
- Nếu chưa cấu hình → chênh lệch được bỏ qua, PE tạo với số tiền gốc

## Loại bỏ giao dịch (Dismiss)

Giao dịch không liên quan (phí ngân hàng nội bộ, lãi tiền gửi...) có thể nhấn "Dismiss" để ẩn khỏi danh sách đối soát.

## Chạy lại đối soát

Sau khi thay đổi cấu hình trong Bank Statement Settings (ví dụ: bật/tắt matcher, thay đổi dung sai), quay lại Bank Reconcile và nhấn "Chạy lại" để hệ thống áp dụng cấu hình mới cho các giao dịch chưa đối soát.

## Chống trùng lặp

Upload lại cùng file sao kê → hệ thống tự động phát hiện trùng (theo hash ngày + số tiền + tham chiếu + nội dung) → 0 giao dịch mới được tạo. An toàn khi upload nhầm.

## Giao dịch nhiều hóa đơn (Multi-invoice)

Một giao dịch ngân hàng có thể khớp với nhiều hóa đơn. Ví dụ: khách hàng chuyển 1 lần cho 3 hóa đơn → hệ thống gợi ý cả 3 SI với số tiền phân bổ tương ứng. Tối đa 5 hóa đơn mỗi giao dịch (cấu hình trong Settings).
