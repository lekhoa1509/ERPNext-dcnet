# WAREHOUSE - Spec Summary

> **Nguồn:** ERP_SPECIFICATION.md Section 4 - Quản lý Kho
>
> **Module:** Quản lý Kho hàng
>
> **Mô tả:** Quản lý nhập/xuất/tồn kho theo mã số, kho, lô, vị trí, Serial. Theo dõi nhập/xuất/tồn theo mã vạch. Trừ tồn kho khả dụng (giữ theo đơn hàng). Tạo tem và in tem trên hệ thống.

---

## 1. Quy trình Kho (12 bước)

**Nguồn:** ERP_SPECIFICATION.md Section 4 (lines 457-578)

### Bước 1: Tồn kho đầu kỳ ✅

**Nguồn:** Lines 460-467

**Mục đích:** Cập nhật số lượng, giá trị tồn kho đầu kỳ vào hệ thống.

**Màn hình:** Tồn kho đầu kỳ

**Bộ phận:** Kho | **Tần suất:** Bắt đầu sử dụng Bravo

### Bước 2: Phiếu nhập kho ✅

**Nguồn:** Lines 469-481

**Mục đích:** Ghi nhận hàng hóa nhập kho dựa trên nhu cầu vật tư của các bộ phận khác.

**Màn hình:** Phiếu nhập kho

**Thông tin cần có:**
- **Thông tin chung:** Ngày, số phiếu, người lập, nội dung, nhà cung cấp, tiền tệ, kho
- **Thông tin chi tiết:** Mã vật tư, tên vật tư, số lượng, đơn giá, thành tiền, số lô, seri, số đơn hàng

**Bộ phận:** Kho | **Tần suất:** Hàng ngày

### Bước 3-5: Phiếu nhập mua, Phiếu nhập khẩu, Phiếu xuất kho ✅

**Nguồn:** Lines 483-485

**Ghi chú:** Đã mô tả ở section Mua hàng (Section 3)

### Bước 6: Phiếu xuất CCDC ✅

**Nguồn:** Lines 487-499

**Mục đích:** Ghi nhận CCDC xuất kho dựa trên nhu cầu sử dụng của các bộ phận khác, theo dõi, khai báo phân bổ CCDC hàng tháng.

**Màn hình:** Phiếu xuất CCDC

**Thông tin cần có:**
- **Thông tin chung:** Ngày, số phiếu, người lập, nội dung, kho
- **Thông tin chi tiết:** Mã hàng, tên hàng, số lượng, số tháng phân bổ, tài khoản nợ phân bổ, tài khoản có phân bổ, mã tăng giảm, đơn giá, thành tiền

**Bộ phận:** Kho | **Tần suất:** Khi có phát sinh

### Bước 7: Phiếu điều chuyển kho ✅

**Nguồn:** Lines 501-520

**Mục đích:** Ghi nhận điều chuyển giữa các kho dựa trên yêu cầu điều chuyển kho của các bộ phận khác.

**Màn hình:** Phiếu điều chuyển kho

**Thông tin cần có:**
- **Thông tin chung:** Ngày, số phiếu, người lập, nội dung, kho xuất, kho nhập
- **Thông tin chi tiết:** Mã vật tư, tên vật tư, số lượng, số lô, số seri

**Tính năng:** Kế thừa dữ liệu từ đề nghị xuất kho nội bộ

**Thống nhất chung:**
- Đơn vị có nhu cầu nhận hàng sẽ chủ động làm lệnh xuất kho nội bộ
- Đơn vị xuất sẽ làm phiếu xuất điều chuyển từ kho đơn vị xuất sang kho trung gian
- Đơn vị nhận làm phiếu xuất điều chuyển từ kho trung gian về kho của đơn vị nhận

**Bộ phận:** Kho | **Tần suất:** Khi có phát sinh

### Bước 8: Phiếu điều chuyển vị trí ✅

**Nguồn:** Lines 522-530

**Mục đích:** Ghi nhận điều chuyển vị trí hàng hóa vật tư trong kho.

**Màn hình:** Phiếu điều chuyển vị trí

**Bộ phận:** Kho | **Tần suất:** Khi có phát sinh

### Bước 9: Lệnh kiểm kê ✅

**Nguồn:** Lines 532-540

**Mục đích:** Kế toán gửi yêu cầu kiểm kê cho bộ phận kho.

**Cách làm:** Bộ phận kế toán lập lệnh kiểm kê xuống bộ phận kho. Bộ phận kho dừng hoạt động nhập xuất kho để chốt số tồn kho và tiến hành kiểm kê.

**Màn hình:** Lệnh kiểm kê

**Bộ phận:** Kho | **Tần suất:** Khi có phát sinh

### Bước 10: Kiểm kê ✅

**Nguồn:** Lines 542-554

**Mục đích:** Thực hiện kiểm kê lại vật tư hàng hóa, thành phẩm tại các kho.

**Màn hình:** Phiếu kiểm kê

**Thông tin cần có:**
- **Thông tin chung:** Ngày, số, Nội dung, Kho
- **Chi tiết:** Mã hàng, đơn vị tính, số lượng, lô/lot, serial

**Bộ phận:** Kho | **Tần suất:** Khi có phát sinh

### Bước 11: Phiếu nhập/xuất chênh lệch kiểm kê ✅

**Nguồn:** Lines 556-568

**Mục đích:** Dựa trên số liệu tồn kho theo kiểm kê thực tế và số liệu tồn kho trên hệ thống, chương trình sẽ tạo phiếu nhập/xuất xử lý phần chênh lệch.

**Màn hình:** Phiếu xuất chênh lệch kiểm kê

**Thông tin cần có:**
- **Thông tin chung:** Ngày, số phiếu, người lập, nội dung, khách hàng, kho
- **Thông tin chi tiết:** Mã vật tư, tên vật tư, số lượng, đơn giá, thành tiền, số lô, seri

**Bộ phận:** Kế toán | **Tần suất:** Khi có phát sinh

### Bước 12: Tính giá vốn hàng xuất ✅

**Nguồn:** Lines 570-578

**Mục đích:** Thực hiện tính và áp giá vốn vào các phiếu xuất.

**Phương pháp:** Trung bình tháng

**Bộ phận:** Kế toán

---

## 2. Danh mục liên quan

**Nguồn:** ERP_SPECIFICATION.md Section 4 (lines 582-612)

### Danh mục kho ✅

**Nguồn:** Lines 584-586

**Thông tin:** Mã kho, tên kho, nút tích xác định có cho phép xuất âm kho hay không.

### Danh mục lô hàng hóa ✅

**Nguồn:** Lines 588-596

**Mục đích:** Khai báo thông tin lô hàng hóa.

**Cách làm:** Trước khi thực hiện lập phiếu nhập thì thủ kho khai báo thông tin lô hàng hóa để khi làm phiếu nhập chọn được lô.

**Thông tin cần có:**
- **Thông tin chung:** Ngày, mã lô hàng
- **Thông tin chi tiết:** Mã vật tư, tên vật tư

### In tem mã vạch ✅

**Nguồn:** Lines 598-612

**Mục đích:** In tem để dán lên hàng hóa.

**Thông tin cần có:**
- **Thông tin chung:** Ngày, loại tem (tem tự tạo/tem của nhà cung cấp), người lập, số lô vật tư, nước sản xuất, nhà cung cấp, địa chỉ nhà cung cấp, đơn vị nhập khẩu, địa chỉ, điện thoại
- **Thông tin chi tiết:** Mã vật tư, tên vật tư, đvt, số seri, mã vạch, số lượng tem in

**Tính năng:**
- Giá trị mã vạch được quy ước như sau:
  - Đối với loại tem tự in: Mã vạch = `mã vật tư + ;; + số lô`
  - Đối với loại tem của nhà cung cấp: Mã vạch = `số seri`
- Kế thừa mặt hàng, seri từ phiếu nhập khẩu

---

## 3. Quy trình đặc biệt

**Nguồn:** ERP_SPECIFICATION.md Section 4 (lines 616-640)

### Xuất nội bộ giữa các cửa hàng ✅

**Nguồn:** Lines 618-623

**Quy trình:**
1. Nhân viên phụ trách điều phối hàng hóa thực hiện lập lệnh xuất hàng
2. Cửa hàng xuất làm phiếu xuất điều chuyển kho (Kho xuất: kho ký gửi, Kho nhập: kho ký gửi)
3. Trưởng cửa hàng xuất duyệt phiếu xuất để xác nhận lượng xuất
4. Trưởng cửa hàng nhận duyệt phiếu xuất để xác nhận lượng nhập

### Quy trình hàng ký gửi (Thăng Long TM ↔ Nhật Minh) ✅

**Nguồn:** Lines 625-640

**Nhập xuất hàng ký gửi:**
1. Tại khay Thăng Long làm phiếu xuất điều chuyển kho từ kho tổng sang kho ký gửi
2. Tại khay Nhật Minh làm phiếu nhập kho vào ký gửi tại cửa hàng

**Mua bán giữa Nhật Minh và Thăng Long TM:**
1. Nhật Minh tổng hợp số lượng thực tế bán cho KH để gửi Thăng Long làm căn cứ xuất hóa đơn
2. Thăng Long xuất hóa đơn từ kho hàng ký gửi cho Nhật Minh
3. Nhật Minh lập phiếu nhập mua đưa vào kho xuất hóa đơn

**Bán hàng tại Nhật Minh:**
1. Bán hàng cho KH từ kho xuất hóa đơn để ghi nhận tăng doanh thu, công nợ
2. Xuất kho hàng ký gửi để giảm lượng tồn kho
3. Lập phiếu nhập mua đưa vào kho xuất hóa đơn để cuối tháng tính được giá vốn

---

## 4. Tính năng đặc biệt

**Nguồn:** ERP_SPECIFICATION.md Section 1 (lines 32-35)

### Theo dõi nhập/xuất/tồn ✅

- Nhập/xuất theo mã số, kho, lô, vị trí, Serial
- Theo dõi nhập/xuất/tồn theo mã vạch
- Trừ tồn kho khả dụng (giữ theo đơn hàng)

### Chức năng tạo tem, in tem trên hệ thống ✅

- Hỗ trợ 2 loại tem: Tem tự tạo, Tem của nhà cung cấp
- Quy ước mã vạch theo loại tem
- Kế thừa dữ liệu từ phiếu nhập khẩu

---

**© 2025 DCNET Corporation**
**Last Updated:** 14/01/2026
