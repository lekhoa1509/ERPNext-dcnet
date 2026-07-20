# Module Pricing - Đặc tả theo Nhật Minh

> **Nguồn:** `/docs/feature/ERP_SPECIFICATION.md` Section 2 (Bước 2-3)
> **Phiên bản:** 1.0.0 | **Giai đoạn:** Bàn giao đợt 1
> **Lưu ý:** File này chỉ ghi lại ĐÚNG những gì có trong spec gốc. Đây là module con của Quản lý Bán hàng, tập trung vào Bảng giá & Chính sách chiết khấu.

---

## Định nghĩa

> Module Pricing quản lý bảng giá niêm yết và chính sách chiết khấu cho cả bán buôn và bán lẻ. Module này là nền tảng cho việc tính giá trong đơn hàng, lệnh xuất, và hóa đơn bán hàng.

---

## I. Bảng giá bán niêm yết (Bán buôn)

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 2 (Lines 57-70)

### Mục đích
Cập nhật giá bán cho từng mặt hàng theo từng thời điểm.

### Màn hình
Bảng giá niêm yết

### Thông tin cần có

#### Thông tin chung:
- Ngày hiệu lực
- Số bảng giá
- Người lập
- Nội dung

#### Thông tin chi tiết:
- Mã hàng hóa
- Tên hàng hóa
- Giá bán
- Ghi chú

### Tính năng
- Đính kèm file quyết định giá

### Bộ phận
Kinh doanh

### Tần suất
Khi có thay đổi

---

## II. Chính sách chiết khấu bán buôn

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 3 (Lines 71-83)

### Mục đích
Cập nhật tỷ lệ chiết khấu cho từng KH theo từng mặt hàng để lên đơn hàng.

### Màn hình
Chính sách chiết khấu bán buôn

### Thông tin cần có

#### Thông tin chung:
- Ngày áp dụng
- Đối tượng
- Nội dung

#### Thông tin chi tiết:
- Mã hàng hóa
- Tên hàng hóa
- Tỷ lệ chiết khấu

### Tính năng
- Đính kèm file

### Bộ phận
Kinh doanh

### Tần suất
Khi có thay đổi

---

## III. Bảng giá bán niêm yết (Bán lẻ)

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 1 (Quy trình Bán lẻ) (Lines 232-238)

### Mục đích
Cập nhật giá bán cho từng mặt hàng theo từng thời điểm.

### Màn hình
Bảng giá niêm yết

### Bộ phận
Kinh doanh

### Tần suất
Khi có thay đổi

### Ghi chú
Sử dụng cùng màn hình với bảng giá bán buôn, phân biệt qua loại bảng giá (Buôn/Lẻ).

---

## IV. Chính sách chiết khấu bán lẻ

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 2 (Quy trình Bán lẻ) (Lines 240-252)

### Mục đích
Cập nhật tỷ lệ chiết khấu cho khách lẻ theo từng mặt hàng.

### Màn hình
Chính sách chiết khấu bán lẻ

### Thông tin cần có

#### Thông tin chung:
- Ngày áp dụng
- Nội dung

#### Thông tin chi tiết:
- Mã hàng hóa
- Tên hàng hóa
- Tỷ lệ chiết khấu

### Tính năng
- Đính kèm file

### Bộ phận
Kinh doanh

### Tần suất
Khi có thay đổi

---

## V. Tích hợp với các module khác

### Tích hợp với Đơn đặt hàng bán (Sales Order)
**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 4 (Lines 86-100)

- Đơn hàng kế thừa dữ liệu từ bảng giá và chính sách chiết khấu
- Nếu không nhập số chính sách chiết khấu thì cho phép tự nhập tay tỷ lệ chiết khấu
- Thông tin chi tiết đơn hàng bao gồm:
  - Số bảng giá
  - Số chính sách chiết khấu
  - % chiết khấu
  - Tiền chiết khấu
  - Đơn giá trước/sau chiết khấu
  - Thành tiền trước/sau chiết khấu

### Tích hợp với Lệnh xuất hàng (Delivery Order)
**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 6 (Lines 110-135)

- Lệnh xuất kế thừa dữ liệu từ đơn hàng (bao gồm thông tin giá và chiết khấu)
- Thông tin chi tiết bao gồm:
  - Đơn giá trước chiết khấu
  - Số chính sách chiết khấu
  - % chiết khấu
  - Tiền chiết khấu
  - Tiền sau chiết khấu

### Tích hợp với Hóa đơn bán buôn (Sales Invoice)
**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 9 (Lines 164-182)

- Tự động lấy ra số bảng giá, số chính sách chiết khấu theo ngày hóa đơn
- Cảnh báo nếu giá bán trên lệnh xuất khác với giá bán trên hóa đơn
- Thông tin chi tiết hóa đơn bao gồm:
  - Số bảng giá bán
  - Đơn giá trước chiết khấu
  - Thành tiền trước chiết khấu
  - Số chính sách chiết khấu
  - % chiết khấu
  - Tiền chiết khấu
  - Thành tiền sau chiết khấu

### Tích hợp với Hóa đơn bán lẻ (POS Invoice)
**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 3 (Quy trình Bán lẻ) (Lines 254-265)

- Thông tin chi tiết hàng hóa bao gồm:
  - Số bảng giá
  - Số chính sách chiết khấu
  - Đơn giá
  - Thành tiền
  - Tiền chiết khấu theo chính sách
  - Tỷ lệ chiết khấu đặc biệt (do nhân viên bán lẻ cấp)
  - Tiền chiết khấu đặc biệt

**Công thức:** Tiền chiết khấu đặc biệt = (tiền hàng trước chiết khấu - tiền chiết khấu theo chính sách) × tỷ lệ chiết khấu đặc biệt

---

## VI. Quy tắc nghiệp vụ

### 1. Hiệu lực bảng giá
- Bảng giá có ngày hiệu lực xác định
- Hệ thống tự động áp dụng bảng giá đúng theo thời điểm tạo đơn/hóa đơn

### 2. Áp dụng chiết khấu
- Chính sách chiết khấu có ngày áp dụng xác định
- Chiết khấu bán buôn: Theo khách hàng và mặt hàng
- Chiết khấu bán lẻ: Theo mặt hàng (áp dụng cho tất cả khách lẻ)
- Cho phép nhập tay tỷ lệ chiết khấu nếu không chọn chính sách

### 3. Chiết khấu đặc biệt (Bán lẻ)
- Áp dụng trên giá sau khi đã trừ chiết khấu theo chính sách
- Do nhân viên bán lẻ quyết định tại thời điểm bán
- Công thức tính rõ ràng, tránh nhầm lẫn

### 4. Kiểm tra giá
- Cảnh báo khi giá bán trên lệnh xuất khác giá trên hóa đơn
- Đảm bảo tính nhất quán giữa các chứng từ trong quy trình bán hàng

---

## VII. Câu hỏi cần làm rõ

### 1. Phân loại bảng giá
❓ **Hỏi:** Có bao nhiêu loại bảng giá? (VD: Buôn/Lẻ, theo vùng miền, theo kênh bán)
❓ **Hỏi:** Có bảng giá riêng cho từng khách hàng không?

### 2. Lịch sử giá
❓ **Hỏi:** Có cần lưu lịch sử thay đổi bảng giá không?
❓ **Hỏi:** Có báo cáo phân tích dao động giá không?

### 3. Chiết khấu theo số lượng/doanh số
❓ **Hỏi:** Có chiết khấu theo số lượng mua không? (VD: Mua trên 100 sp giảm 5%)
❓ **Hỏi:** Có chiết khấu tích lũy theo doanh số không?

### 4. Chiết khấu kết hợp
❓ **Hỏi:** Có cho phép áp dụng nhiều chính sách chiết khấu cùng lúc không?
❓ **Hỏi:** Thứ tự áp dụng chiết khấu như thế nào? (Nối tiếp hay song song)

### 5. Quyền phê duyệt
❓ **Hỏi:** Bảng giá có cần phê duyệt trước khi áp dụng không?
❓ **Hỏi:** Chính sách chiết khấu có workflow phê duyệt không?

### 6. Giá theo đơn vị tính
❓ **Hỏi:** Có sản phẩm có nhiều đơn vị tính không? (VD: Bán lẻ theo cái, bán buôn theo thùng)
❓ **Hỏi:** Giá có khác nhau theo đơn vị tính không?

### 7. Chiết khấu đặc biệt (Bán lẻ)
❓ **Hỏi:** Ai có quyền cấp chiết khấu đặc biệt? (Nhân viên bán hàng, quản lý?)
❓ **Hỏi:** Có giới hạn tỷ lệ chiết khấu đặc biệt không?
❓ **Hỏi:** Có cần ghi nhận lý do chiết khấu đặc biệt không?

### 8. Tích hợp với kho
❓ **Hỏi:** Giá có khác nhau theo kho không? (VD: Kho trung tâm vs Chi nhánh)

### 9. Giá theo tiền tệ
❓ **Hỏi:** Có nhiều bảng giá theo tiền tệ không? (VND, USD...)
❓ **Hỏi:** Tỷ giá quy đổi lấy từ đâu?

### 10. Import/Export
❓ **Hỏi:** Có cho phép import hàng loạt bảng giá từ Excel không?
❓ **Hỏi:** Có xuất báo cáo so sánh bảng giá giữa các thời điểm không?

---

## VIII. Phạm vi module

### Trong phạm vi (In-scope)
✅ Quản lý bảng giá niêm yết (Buôn/Lẻ)
✅ Quản lý chính sách chiết khấu (Buôn/Lẻ)
✅ Đính kèm file quyết định giá
✅ Tích hợp với Đơn hàng, Lệnh xuất, Hóa đơn
✅ Chiết khấu đặc biệt cho bán lẻ
✅ Cảnh báo giá không khớp

### Ngoài phạm vi (Out-of-scope)
❌ Tính thưởng đạt kế hoạch doanh số (Thuộc module Sales Target)
❌ Hạn mức công nợ (Thuộc module Credit Management)
❌ Quản lý đơn hàng/lệnh xuất/hóa đơn (Thuộc module Sales)
❌ Phân tích giá cạnh tranh (Chưa có trong spec)
❌ Dynamic pricing (Chưa có trong spec)

---

**Tổng kết:**
- **2 chức năng chính:** Bảng giá + Chính sách chiết khấu
- **2 kênh bán:** Buôn + Lẻ
- **4 màn hình:** Bảng giá buôn, Chiết khấu buôn, Bảng giá lẻ (chung), Chiết khấu lẻ
- **Tích hợp:** Đơn hàng, Lệnh xuất, Hóa đơn buôn/lẻ
- **Câu hỏi:** 10 nhóm câu hỏi cần làm rõ với khách hàng
