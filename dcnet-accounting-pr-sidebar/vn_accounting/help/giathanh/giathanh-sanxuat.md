---
title: Tính giá thành sản xuất cuối kỳ
section: Giá thành
doctype: null
---

# Tính giá thành sản xuất cuối kỳ

Giá thành sản xuất là tổng chi phí thực tế phát sinh để hoàn thành một đơn vị sản phẩm hoặc dịch vụ trong kỳ. Theo Thông tư 99/2025/TT-BTC, doanh nghiệp sản xuất phải tập hợp và phân bổ chi phí sản xuất (TK 621/622/627) vào giá thành cuối mỗi kỳ.

## Quy trình 6 bước tính giá thành

Sử dụng **Giá thành → Wizard tính giá thành SX** để thực hiện toàn bộ quy trình.

### Bước 1 — Xác định kỳ tính giá thành

Chọn **Công ty** và **Kỳ kế toán** (từ ngày — đến ngày). Thông thường tính theo tháng hoặc quý. Nhấn **Tiếp theo** để hệ thống tổng hợp chi phí.

### Bước 2 — Xem chi phí tập hợp theo đối tượng

Hệ thống hiển thị bảng tổng hợp chi phí thực tế phát sinh theo từng đối tượng tính giá thành:

| Cột | Ý nghĩa |
|-----|---------|
| Đối tượng | Mã sản phẩm / Lệnh sản xuất / Dự án / Trung tâm chi phí |
| Chi phí NVL trực tiếp | Tổng phát sinh TK 621 |
| Chi phí NC trực tiếp | Tổng phát sinh TK 622 |
| Chi phí SXC phân bổ | Tổng phát sinh TK 627 đã phân bổ |
| Tổng chi phí | 621 + 622 + 627 |

Kiểm tra số liệu; nếu thiếu, quay lại nhập bút toán phát sinh trước khi tiếp tục.

### Bước 3 — Nhập thông tin sản phẩm dở dang

Với từng đối tượng, nhập thông tin **sản phẩm dở dang đầu kỳ**, **sản phẩm dở dang cuối kỳ** và **sản lượng hoàn thành**. Chọn **Phương pháp đánh giá SPDD** phù hợp:

| Phương pháp | Khi nào dùng |
|-------------|-------------|
| **Nhập thẳng** | Đã có giá trị SPDD cuối kỳ từ kiểm kê thực tế |
| **Sản lượng tương đương** | Muốn hệ thống tính từ số lượng dở dang và % hoàn thành |
| **Chỉ chi phí NVL trực tiếp** | SPDD chỉ tính NVL; NC và SXC không tính vào SPDD |
| **50% chi phí chế biến** | Quy ước dở dang ở giữa chu kỳ sản xuất (hoàn thành 50%) |

Sau khi nhập, hệ thống tự tính **Giá trị SPDD cuối kỳ** và **Giá thành đơn vị**.

### Bước 4 — Xem lại kết quả tính giá thành

Bảng kết quả hiển thị:

| Chỉ tiêu | Công thức |
|----------|-----------|
| Tổng chi phí | SPDD đầu kỳ + Chi phí phát sinh kỳ |
| Giá trị SPDD cuối kỳ | Tính theo phương pháp đã chọn |
| Tổng giá thành thành phẩm | Tổng chi phí − SPDD cuối kỳ |
| Giá thành đơn vị | Tổng giá thành ÷ Sản lượng hoàn thành |

Kiểm tra kỹ trước khi chuyển sang bước tạo bút toán.

### Bước 5 — Chọn hình thức chuyển giá thành

Hệ thống hỏi **hình thức xử lý giá thành**:

- **Nhập kho thành phẩm (TK 155)**: áp dụng cho doanh nghiệp sản xuất ra thành phẩm nhập kho — hệ thống tạo bút toán Nợ 155 / Có 154 và phiếu nhập kho tương ứng.
- **Kết chuyển thẳng vào giá vốn (TK 632)**: áp dụng cho doanh nghiệp dịch vụ hoặc xây lắp đã bàn giao — hệ thống tạo bút toán Nợ 632 / Có 154.

> **Lưu ý:** Hình thức mặc định được lấy từ **Cài đặt giá thành** do kế toán trưởng cấu hình. Kế toán viên vẫn có thể đổi từng kỳ tại bước này.

### Bước 6 — Xác nhận và tạo bút toán

Nhấn **Tạo bút toán nháp**. Hệ thống tạo 2 bút toán:

1. **Bút toán 1 — Kết chuyển chi phí sang DDSP**: Nợ 154 / Có 621, 622, 627 (theo số thực tế kỳ này)
2. **Bút toán 2 — Chuyển giá thành**: Nợ 155 / Có 154 (hoặc Nợ 632 / Có 154 nếu chọn kết chuyển thẳng)

Hai bút toán ở trạng thái **Nháp**. Kế toán trưởng soát xét và **ghi sổ** thủ công sau khi xác nhận số liệu đúng.

## Xử lý các trường hợp đặc biệt

**Doanh nghiệp có nhiều sản phẩm cùng dùng chung TK 627:**

Cần phân bổ chi phí sản xuất chung trước khi chạy wizard. Vào **Giá thành → Phân bổ chi phí SXC** để chia TK 627 theo tiêu thức phân bổ (NVL, NC, giờ máy...).

**Chi phí phát sinh ngoài kỳ (phát sinh muộn):**

Bổ sung bút toán hạch toán vào đúng kỳ trước khi chạy wizard. Hệ thống lấy số liệu theo ngày phát sinh, không tự điều chỉnh.

**Sản phẩm hỏng, thiệt hại nguyên liệu:**

Nếu có hao hụt nằm trong định mức, không cần điều chỉnh — đã tự động gộp vào TK 621/622/627. Nếu hao hụt vượt định mức, hạch toán sang TK 138 (đòi bồi thường) hoặc TK 811 (chi phí khác) trước khi chạy wizard.

## Câu hỏi thường gặp

**Chạy wizard xong rồi phát hiện sai số liệu chi phí, làm sao sửa?**

Bút toán vẫn đang **Nháp** — xóa 2 bút toán nháp, sửa bút toán chi phí gốc, rồi chạy wizard lại.

**Tháng này không có sản xuất (nhà máy nghỉ), có cần chạy wizard không?**

Không bắt buộc nếu TK 621/622/627 đều bằng 0. Tuy nhiên nên chạy để có bản ghi "0 đồng" và đảm bảo tính liên tục của SPDD đầu/cuối kỳ.

**Giá thành đơn vị âm — tại sao?**

Thường do nhập sai **Sản lượng hoàn thành** (bằng 0 hoặc quá nhỏ so với chi phí). Kiểm tra lại sản lượng thực tế từ phiếu nhập kho hoặc phiếu giao hàng.
