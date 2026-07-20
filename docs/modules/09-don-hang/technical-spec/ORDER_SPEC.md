# Module Sales Order - Đặc tả theo Nhật Minh

> **Nguồn:** `/docs/feature/ERP_SPECIFICATION.md` Section 2
> **Phiên bản:** 1.0.0 | **Giai đoạn:** Phase 1 - ERP
> **Lưu ý:** File này chỉ ghi lại ĐÚNG những gì có trong spec gốc

---

## Định nghĩa

> Quản lý toàn bộ quy trình bán hàng từ kế hoạch, bảng giá, đơn hàng, xuất kho, hóa đơn đến thu tiền và xử lý trả hàng

**Phạm vi:**
- Bán buôn (Wholesale) - 12 bước
- Bán lẻ (Retail) - 3 bước
- Tích hợp kiểm tra công nợ, hạn mức, tồn kho

---

## Quy trình Bán buôn (12 bước)

**Nguồn:** ERP_SPECIFICATION.md lines 48-227

### Bước 1: Kế hoạch bán hàng theo năm

**Mục đích:** Cập nhật kế hoạch theo năm cho từng KH để tính thưởng doanh số khi đạt kế hoạch năm.

**Chức năng:** Kế hoạch bán hàng

**Bộ phận:** Kinh doanh | **Tần suất:** Theo năm

---

### Bước 2: Bảng giá bán niêm yết

**Mục đích:** Cập nhật giá bán cho từng mặt hàng theo từng thời điểm.

**Màn hình:** Bảng giá niêm yết

**Thông tin cần có:**
- **Thông tin chung:** Ngày hiệu lực, số bảng giá, người lập, nội dung
- **Thông tin chi tiết:** Mã hàng hóa, tên hàng hóa, giá bán, ghi chú

**Tính năng:** Đính kèm file quyết định giá

**Bộ phận:** Kinh doanh | **Tần suất:** Khi có thay đổi

---

### Bước 3: Chính sách chiết khấu bán buôn

**Mục đích:** Cập nhật tỷ lệ chiết khấu cho từng KH theo từng mặt hàng để lên đơn hàng.

**Màn hình:** Chính sách chiết khấu bán buôn

**Thông tin cần có:**
- **Thông tin chung:** Ngày áp dụng, đối tượng, nội dung
- **Thông tin chi tiết:** Mã hàng hóa, tên hàng hóa, tỷ lệ chiết khấu

**Tính năng:** Đính kèm file

**Bộ phận:** Kinh doanh | **Tần suất:** Khi có thay đổi

---

### Bước 4: Đơn đặt hàng bán ⭐ (CORE)

**Mục đích:** Sau khi có nhu cầu từ KH, NVKD lập đơn hàng bán để ghi nhận.

**Cách làm:** Cập nhật đơn đặt hàng dựa trên bảng giá và chính sách chiết khấu đã ban hành.

**Màn hình:** Đơn đặt hàng bán

**Thông tin cần có:**

- **Thông tin chung:**
  - Ngày
  - Số đơn hàng
  - Tiền tệ
  - Khách hàng
  - Địa chỉ
  - Người liên hệ
  - Người lập
  - Điều khoản giao hàng
  - Điều khoản thanh toán
  - Phương thức thanh toán

- **Thông tin chi tiết:**
  - Mã hàng
  - Tên hàng
  - Đơn vị tính
  - Số lượng
  - Đơn giá trước chiết khấu
  - Thành tiền trước chiết khấu
  - Số bảng giá
  - Số chính sách chiết khấu
  - % chiết khấu
  - Tiền chiết khấu
  - Thành tiền sau chiết khấu
  - Ngày dự kiến giao

**Thống nhất:** Nếu không nhập số chính sách chiết khấu thì cho phép tự nhập tay tỷ lệ chiết khấu.

**Bộ phận:** Kinh doanh | **Tần suất:** Hàng ngày

---

### Bước 5: Kiểm tra tồn kho

**Mục đích:** Bộ phận KD kiểm tra tham khảo tồn kho xem còn đủ hàng hóa để xuất kho.

**Cách làm:** Bộ phận KD kiểm tra tồn kho để phản hồi cho KH.

**Bộ phận:** Kinh doanh | **Tần suất:** Hàng ngày

---

### Bước 6: Lệnh xuất hàng

**Mục đích:** Sau khi có đơn hàng đến lịch giao hàng, bộ phận KD lập lệnh xuất hàng gửi tới bộ phận kho.

**Cách làm:** Bộ phận Kinh doanh kế thừa dữ liệu từ đơn hàng.

**Màn hình:** Lệnh xuất hàng

**Thông tin cần có:**
- **Thông tin chung:** Ngày đề nghị, Người đề nghị, kho xuất, khách hàng
- **Thông tin chi tiết:** Mã vật tư, tên vật tư, đvt, số lượng, đơn giá trước chiết khấu, thành tiền, số chính sách chiết khấu, % chiết khấu, tiền chiết khấu, tiền sau chiết khấu

**Tính năng cần có:**
- Kế thừa dữ liệu từ đơn hàng bán
- Kiểm tra hạn mức và công nợ quá hạn

**Yêu cầu phân quyền:**
- Phân quyền bộ phận kho không nhìn thấy đơn giá, thành tiền
- Phân quyền bộ phận kho không được sửa lại thông tin khách hàng, mặt hàng, số lượng yêu cầu

**Thống nhất chung:**
- Bộ phận kho cập nhật thông tin thực xuất (mặt hàng, seri, lô, kho, số lượng) để làm cơ sở cho kế toán kế thừa dữ liệu
- Khi kiểm tra điều kiện xuất hàng thì phải hiển thị số dư công nợ thực tế, công nợ dự kiến (bao gồm cả lệnh xuất hàng chưa xuất), số hóa đơn quá hạn

**Bộ phận:** Kinh doanh

---

### Bước 7: Kiểm tra hạn mức công nợ

**Mục đích:** Bộ phận KD kiểm tra hạn mức công nợ của KH.

**Cách làm:** Bộ phận KD kiểm tra hạn mức công nợ. Trường hợp hết hạn mức, bộ phận KD lập lại đơn hàng, hợp đồng gửi lại KH.

**Màn hình:** Hạn mức công nợ

**Thông tin cần có:**
- **Thông tin chung:** Ngày áp dụng, tài khoản công nợ
- **Thông tin chi tiết:** Mã khách hàng, tên khách hàng, giá trị hạn mức

**Tính năng:** Đính kèm file

**Bộ phận:** Kinh doanh | **Tần suất:** Hàng ngày

---

### Bước 8: Kiểm tra công nợ quá hạn

**Mục đích:** Bộ phận KD kiểm tra xem nếu có hóa đơn quá hạn hoặc quá hạn mức không để làm cơ sở cho quyết định có xuất hàng cho KH không.

**Cách làm:** Bộ phận KD thực hiện cập nhật các mặt hàng cần xuất. Khi lưu, phần mềm sẽ thực hiện kiểm tra nếu có hóa đơn quá hạn sẽ hiện cảnh báo.

**Điều kiện xuất hàng hợp lệ:**
1. Khách hàng không có hóa đơn quá hạn
2. Giá trị công nợ hiện tại + giá trị trên các lệnh xuất đã duyệt chưa xuất + giá trị trên lệnh xuất hàng hiện tại không lớn hơn hạn mức công nợ

**Xử lý ngoại lệ:** Nếu không thỏa mãn 2 điều kiện trên thì Kế toán trưởng phải xác nhận thì lệnh xuất mới hợp lệ.

---

### Bước 9: Hóa đơn bán buôn

**Mục đích:** Kế toán thực hiện xuất hóa đơn cho khách.

**Cách làm:** Bộ phận kế toán căn cứ số lượng thực xuất trên lệnh xuất của bộ phận kho để xuất hóa đơn cho KH.

**Màn hình:** Hóa đơn bán buôn

**Thông tin cần có:**

- **Thông tin chung:**
  - Ngày chứng từ
  - Khách hàng
  - Hình thức thanh toán
  - Số hóa đơn
  - Hạn thanh toán
  - Mã tiền tệ
  - Tổng tiền hàng
  - Tổng tiền chiết khấu
  - Tổng tiền thuế
  - Tổng tiền

- **Thông tin chi tiết:**
  - Mã vật tư
  - Tên vật tư
  - Đvt
  - Số đơn hàng
  - Số lệnh xuất hàng
  - Kho hàng
  - Số lượng
  - Số bảng giá bán
  - Đơn giá trước chiết khấu
  - Thành tiền trước chiết khấu
  - Số chính sách chiết khấu
  - % chiết khấu
  - Tiền chiết khấu
  - Thành tiền sau chiết khấu

- **Thông tin chi tiết lô, seri:**
  - Số lô
  - Số seri
  - Số lượng

**Tính năng cần có:**
- Kế thừa dữ liệu từ lệnh xuất hàng
- Tự động lấy ra số bảng giá, số chính sách chiết khấu theo ngày hóa đơn
- Cảnh báo nếu giá bán trên lệnh xuất khác với giá bán trên hóa đơn

**Bộ phận:** Kế toán | **Tần suất:** Hàng ngày

---

### Bước 10: Lệnh nhập hàng trả lại

**Mục đích:** Kinh doanh thực hiện yêu cầu kho nhập hàng trả lại nếu có hàng bán bị trả lại.

**Cách làm:** Bộ phận Kinh doanh kế thừa dữ liệu từ hóa đơn bán hàng để lập lệnh nhập hàng trả lại.

**Màn hình:** Lệnh nhập hàng

**Thông tin cần có:**
- **Thông tin chung:** Ngày đề nghị, Người đề nghị, kho nhập, khách hàng
- **Thông tin chi tiết:** Mã vật tư, tên vật tư, đvt, số lượng, đơn giá, thành tiền
- **Thông tin chi tiết:** Mã lô, số seri, kho, số lượng

**Tính năng:** Kế thừa dữ liệu từ hóa đơn

**Thống nhất chung:** Bộ phận kho cập nhật thông tin thực nhập (mã hàng, mã lô, số seri, số lượng) để làm cơ sở cho kế toán kế thừa sang phiếu hàng bán trả lại.

**Bộ phận:** Kinh doanh | **Tần suất:** Khi có phát sinh

---

### Bước 11: Hàng bán bị trả lại

**Mục đích:** Bộ phận kế toán kế thừa danh sách mặt hàng, seri, số lô từ lệnh nhập hàng trả lại để ghi nhận hàng bán bị trả lại.

**Màn hình:** Hàng bán bị trả lại

**Thông tin cần có:**
- **Thông tin chung:** Ngày, Số phiếu, Thông tin khách hàng, Lý do
- **Thông tin chi tiết:** Mã hàng, Tên hàng, đơn vị tính, số lượng, kho nhập, ngày dự kiến giao, số đơn hàng, số hóa đơn, ghi chú
- **Thông tin chi tiết lô, seri:** số lô, số seri, số lượng

**Tính năng cần có:**
- Kế thừa dữ liệu từ đề nghị nhập hàng trả lại
- Kiểm tra nếu seri nhập không tồn tại trên hóa đơn bán hàng của KH trả lại thì cảnh báo

**Bộ phận:** Kế toán | **Tần suất:** Khi có phát sinh

---

### Bước 12: Tính thưởng đạt kế hoạch doanh số

**Mục đích:** Dùng cho bộ phận kế toán tính toán, ghi nhận lại chương trình chiết khấu, khuyến mại KH được hưởng làm căn cứ thu tiền từ KH.

**Cách làm:** Thực hiện chức năng tính CKKM, công nợ KH thanh toán ghi nhận tại báo có, phiếu thu tiền mặt.

**Bộ phận:** Kế toán | **Tần suất:** Khi có phát sinh

---

## Quy trình Bán lẻ (3 bước)

**Nguồn:** ERP_SPECIFICATION.md lines 230-267

### Bước 1: Bảng giá bán niêm yết (Bán lẻ)

**Mục đích:** Cập nhật giá bán cho từng mặt hàng theo từng thời điểm.

**Màn hình:** Bảng giá niêm yết

**Bộ phận:** Kinh doanh | **Tần suất:** Khi có thay đổi

---

### Bước 2: Chính sách chiết khấu bán lẻ

**Mục đích:** Cập nhật tỷ lệ chiết khấu cho khách lẻ theo từng mặt hàng.

**Màn hình:** Chính sách chiết khấu bán lẻ

**Thông tin cần có:**
- **Thông tin chung:** Ngày áp dụng, nội dung
- **Thông tin chi tiết:** Mã hàng hóa, tên hàng hóa, tỷ lệ chiết khấu

**Tính năng:** Đính kèm file

**Bộ phận:** Kinh doanh | **Tần suất:** Khi có thay đổi

---

### Bước 3: Hóa đơn bán lẻ

**Mục đích:** Nhân viên bán hàng tại cửa hàng thực hiện lập phiếu bán hàng cho KH.

**Màn hình:** Hóa đơn bán lẻ

**Thông tin cần có:**

- **Thông tin chung:**
  - Ngày
  - Số chứng từ
  - Số điện thoại KH
  - Doanh số lũy kế
  - Nhân viên kinh doanh
  - Kho
  - Khách hàng
  - Địa chỉ
  - Diễn giải
  - Tiền hàng
  - Tiền chiết khấu
  - Tổng tiền
  - Trả lại khách
  - Tiền thanh toán
  - Tab thẻ thanh toán
  - Loại thuế
  - Thuế suất
  - Tiền thuế
  - Yêu cầu xuất hóa đơn điện tử (Không lấy hóa đơn, phát hành hóa đơn sau, phát hành hóa đơn ngay)

- **Thông tin chi tiết hàng hóa:**
  - Mã hàng
  - Tên vật tư hàng hóa
  - Đvt
  - Số bảng giá
  - Số chính sách chiết khấu
  - Đơn giá
  - Thành tiền
  - Tiền chiết khấu theo chính sách
  - Tỷ lệ chiết khấu đặc biệt
  - Tiền chiết khấu đặc biệt

- **Thông tin chi tiết lô, seri:**
  - Số lô
  - Số seri
  - Số lượng

**Công thức:** Tiền chiết khấu đặc biệt = (tiền hàng trước chiết khấu - tiền chiết khấu theo chính sách) × tỷ lệ chiết khấu đặc biệt

**Bộ phận:** Cửa hàng | **Tần suất:** Hàng ngày

---

## Danh mục liên quan

**Nguồn:** ERP_SPECIFICATION.md lines 271-296

### Danh mục đối tượng (Khách hàng)

**Mô tả:** Dùng để khai báo danh mục các đối tượng như: nhà cung cấp, khách hàng, đối tượng nội bộ.

**Thông tin chung:**
- Mã đối tượng
- Tên đối tượng
- Loại đối tượng
- Địa chỉ
- Mã số thuế
- Người đại diện
- Điện thoại
- Email
- Nhóm đối tượng
- Thông tin tài khoản ngân hàng
- Phương thức thanh toán
- Kỳ hạn thanh toán

---

### Danh mục vật tư hàng hóa

**Thông tin chung:**
- Mã hàng
- Tên hàng hóa
- Đơn vị tính
- Macro
- Location
- Product group
- Color
- Category
- Phân loại doanh số
- Product type
- Statis factor
- Nhóm 1-6

**Thông tin đơn vị tính quy đổi:**
- Đơn vị tính
- Hệ số quy đổi

**Tính năng:**
- **Theo dõi lô:** Phần mềm kiểm tra được thông tin nhập xuất tồn kho theo từng mã lô. Yêu cầu: Trên tất cả các màn hình nhập dữ liệu (tồn kho đầu kỳ, phiếu nhập, phiếu xuất...), người sử dụng đều phải cập nhật thông tin mã lô tương ứng với vật tư cần theo dõi.

---

### Kế hoạch doanh số năm

**Mục đích:** Dùng để nhập giá trị doanh số tiêu thụ theo kế hoạch của từng KH.

**Thông tin chung:**
- Ngày áp dụng
- Khách hàng
- Tổng doanh số

**Thông tin chi tiết:**
- Chủng loại
- % doanh số
- Tiền doanh số

**Tính năng:** Đính kèm file

---

## Tổng kết

**Tổng số bước:** 18 bước
- Quy trình Bán buôn: 12 bước
- Quy trình Bán lẻ: 3 bước
- Danh mục liên quan: 3 danh mục

**Core features:**
- Đơn đặt hàng bán (Bước 4) - Trung tâm của quy trình
- Kiểm tra công nợ tự động (Bước 7, 8)
- Tích hợp kho (Bước 5, 6, 10, 11)
- Tính toán chiết khấu đa cấp (Bước 2, 3, 9)
- Phân quyền bộ phận (Kho, Kế toán, Kinh doanh)

---

**Nguồn:** ERP_SPECIFICATION.md Section 2 (lines 46-298)
