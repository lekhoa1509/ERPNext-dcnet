# Chức năng Kế toán ERPNext v16 — Theo phần hành

> Ghi chú: "Tự phát triển" = chức năng do tư vấn triển khai xây dựng. "Tùy chỉnh được" = chưa có sẵn, cần cấu hình hoặc phát triển thêm.

---

## 1. Tiền mặt & Tiền gửi ngân hàng

| Chức năng | Mô tả |
|---|---|
| Thu/Chi tiền mặt & TGNH | Phiếu thanh toán, tự động ghi sổ cái |
| Đối chiếu sổ phụ ngân hàng | Công cụ đối chiếu ngân hàng (nhập sao kê, khớp tự động theo số tham chiếu) |
| Kiểm kê quỹ | Tùy chỉnh được |
| Dự báo dòng tiền | Tùy chỉnh được |
| In mẫu chứng từ thu/chi theo thông tư VN | Tùy chỉnh mẫu in |

---

## 2. Mua hàng & Công nợ phải trả

| Chức năng | Mô tả |
|---|---|
| Quy trình mua hàng | Đơn mua → Nhận hàng → Hóa đơn mua → Thanh toán |
| Phân bổ chi phí mua hàng vào giá nhập | Áp dụng cho cả phiếu kho & gia công |
| Ghi nhận chi phí mua hàng vào giá vốn | Gom cước vận chuyển, thuế hải quan vào giá vốn |
| Báo cáo tuổi nợ phải trả | Phân tích công nợ phải trả theo kỳ hạn |
| Đối chiếu công nợ nhà cung cấp | Có sẵn |
| Tạm ứng nhà cung cấp | Thanh toán trước, tự động đối trừ khi có hóa đơn |

---

## 3. Bán hàng & Công nợ phải thu

| Chức năng | Mô tả |
|---|---|
| Quy trình bán hàng | Đơn bán → Giao hàng → Hóa đơn bán → Thu tiền |
| Doanh thu chưa thực hiện | Phân bổ doanh thu tự động theo kỳ |
| Bán hàng tại quầy | Nhanh, hoạt động khi mất mạng |
| Báo cáo tuổi nợ phải thu | Phân tích công nợ phải thu theo kỳ hạn, nhắc nợ tự động |
| Giảm giá / Trả lại hàng bán | Hóa đơn điều chỉnh giảm (ghi có) |
| Chiết khấu thương mại / thanh toán | Quy tắc giá linh hoạt, chiết khấu trên hóa đơn |

---

## 4. Hóa đơn Điện tử

| Chức năng | Mô tả |
|---|---|
| Xuất hóa đơn điện tử | Tự phát triển — kết nối API nhà cung cấp HĐĐT, xuất HĐ trực tiếp từ hóa đơn bán hàng |
| Đồng bộ hóa đơn đầu vào | Tự phát triển — đồng bộ HĐ đầu vào từ NCC HĐĐT qua API, tạo hóa đơn mua hàng nháp |
| Chữ ký số | Tự phát triển — tích hợp với dịch vụ ký số của NCC hóa đơn điện tử |

---

## 5. Kho & Hàng tồn kho

| Chức năng | Mô tả |
|---|---|
| Nhập kho / Xuất kho / Chuyển kho | Phiếu kho đa loại (nhận hàng, xuất sử dụng, chuyển kho, sản xuất) |
| Phương pháp tính giá xuất kho | Chọn riêng theo công ty — nhập trước xuất trước / bình quân gia quyền |
| Giữ chỗ tồn kho | Giữ nguyên vật liệu cho lệnh sản xuất / gia công |
| Truy xuất nguồn gốc lô / số seri | Báo cáo truy xuất ngược – xuôi đầy đủ |
| Xem trước bút toán trước khi ghi sổ | Xem tác động sổ kho & sổ cái trước khi xác nhận |
| Kiểm kê kho hàng | Đối chiếu tồn kho, điều chỉnh chênh lệch |
| Lắp ráp / Tháo dỡ | Phiếu kho loại đóng gói lại |
| Hạch toán tồn kho liên tục & định kỳ | Hỗ trợ cả hai phương pháp |

---

## 6. Tài sản cố định & Công cụ dụng cụ

| Chức năng | Mô tả |
|---|---|
| TSCĐ: ghi tăng / ghi giảm | Quản lý vòng đời tài sản từ mua đến thanh lý |
| Khấu hao TSCĐ | Đường thẳng, số dư giảm dần, số dư giảm dần kép |
| Đa sổ khấu hao | Nhiều sổ tài chính cho các mục đích khác nhau (thuế, quản trị) |
| Điều chuyển TSCĐ | Có sẵn |
| Đánh giá lại TSCĐ | Điều chỉnh giá trị tài sản |
| Kiểm kê TSCĐ | Tùy chỉnh được |
| Sổ theo dõi TSCĐ theo mẫu VN | Tùy chỉnh được |
| CCDC: tăng / giảm / phân bổ / kiểm kê | Tùy chỉnh được (xử lý qua chi phí trả trước hoặc xây phân hệ riêng) |

---

## 7. Giá thành sản xuất

| Chức năng | Mô tả |
|---|---|
| Tính giá thành sản phẩm | Định mức nguyên vật liệu + chi phí lệnh sản xuất |
| Tách giá vốn hàng bán & chi phí dịch vụ | Có sẵn |
| Hạch toán kho theo nhóm mặt hàng | Ghi giá vốn linh hoạt theo nhóm |
| Theo dõi bán thành phẩm qua phiếu công việc | Theo dõi sản phẩm dở dang theo công đoạn |
| Phân bổ chi phí sản xuất chung | Tùy chỉnh được |
| Giá thành công trình xây lắp | Tùy chỉnh được (theo dự án) |
| Gia công nhận vào / gửi ra | Phân hệ gia công hoàn chỉnh |

---

## 8. Tiền lương & Bảo hiểm

| Chức năng | Mô tả |
|---|---|
| Tính lương / Bảng lương | Thành phần lương linh hoạt, công thức tùy chỉnh |
| BHXH / BHYT / BHTN / KPCĐ | Tùy chỉnh công thức theo quy định VN |
| Thuế TNCN lũy tiến | Cấu hình bậc thuế lũy tiến |
| Quản lý làm thêm giờ | Quy tắc duyệt và tính làm thêm giờ |

---

## 9. Tổng hợp & Báo cáo tài chính

| Chức năng | Mô tả |
|---|---|
| Sổ cái | Lọc đa chiều: tài khoản, trung tâm chi phí, dự án, chiều hạch toán |
| Sổ nhật ký chung | Danh sách bút toán điều chỉnh |
| Bảng cân đối số phát sinh | Hợp nhất đa công ty, tự động quy đổi ngoại tệ |
| Bảng cân đối kế toán | Tạo mẫu báo cáo tùy chỉnh không cần lập trình |
| Báo cáo kết quả kinh doanh | Tạo mẫu báo cáo tùy chỉnh không cần lập trình |
| Báo cáo lưu chuyển tiền tệ | Có sẵn |
| Thuyết minh báo cáo tài chính (B09-DN) | Tùy chỉnh được |
| Mẫu BCTC theo TT200 / TT133 | Tùy chỉnh được (qua trình tạo mẫu báo cáo) |
| Kết chuyển cuối kỳ | Bút toán khóa sổ kỳ kế toán |
| Tự động ghi bút toán tồn kho cuối kỳ | Hàng tháng / hàng năm |
| Đánh giá lại tài khoản ngoại tệ cuối kỳ | Có sẵn |
| Chỉ báo Nợ/Có trong tổng hợp sổ cái | Số dư cuối hiển thị rõ bên Nợ hoặc Có |
| Tách cột số hiệu & tên tài khoản khi xuất | Có sẵn |
| Đồng tiền báo cáo theo công ty | Sổ cái lưu song song theo đồng tiền báo cáo |

---

## 10. Ngân sách & Đa công ty

| Chức năng | Mô tả |
|---|---|
| Lập ngân sách | Theo trung tâm chi phí / phòng ban / dự án |
| Kiểm soát chi tiêu | Cảnh báo hoặc chặn khi vượt ngân sách |
| Thực hiện so với kế hoạch | Theo dõi chênh lệch thời gian thực |
| Phân bổ ngân sách theo tháng | Mẫu phân bổ ngân sách |
| Đa công ty trong 1 hệ thống | Nhiều pháp nhân, danh mục dùng chung |
| Giao dịch liên công ty | Bút toán liên công ty, tự động đối ứng |
| Hợp nhất báo cáo tài chính đa công ty | Có sẵn |
| Chiều hạch toán tùy chỉnh | Trung tâm chi phí, dự án, và chiều hạch toán tự tạo |
