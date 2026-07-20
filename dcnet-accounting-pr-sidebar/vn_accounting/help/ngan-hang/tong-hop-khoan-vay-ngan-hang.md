---
title: Tổng hợp khoản vay ngân hàng
order: 10
summary: Báo cáo tổng hợp tất cả khoản vay ngân hàng — dư nợ, lịch trả nợ, lãi phải trả.
---

## Mục đích

Báo cáo **Tổng hợp khoản vay ngân hàng** cung cấp cái nhìn tổng quan về tất cả khoản vay của doanh nghiệp: số dư nợ gốc, lãi phải trả, kỳ trả nợ tiếp theo, và tổng nghĩa vụ nợ theo từng ngân hàng.

## Khi nào dùng

- **Định kỳ (cuối tháng/quý):** xem tổng quan tình hình nợ vay.
- **Lập kế hoạch dòng tiền:** biết các khoản trả nợ sắp tới để chuẩn bị tiền.
- **Báo cáo ban giám đốc/hội đồng quản trị:** tình hình nợ vay và chi phí lãi vay.
- **Đàm phán với ngân hàng:** tổng hợp dư nợ để thương thảo khoản vay mới hoặc tái cấp vốn.
- **Kiểm toán:** cung cấp số liệu nợ vay cho kiểm toán viên.

## Cách thực hiện

1. Bấm **Tổng hợp khoản vay ngân hàng** trên menu Ngân hàng → báo cáo mở.
2. Lọc theo: **Công ty**, **Trạng thái** (Đang vay / Đã tất toán / Tất cả), **Ngân hàng** (tùy chọn).
3. Bấm **Refresh** → bảng hiển thị danh sách khoản vay với các cột: Hợp đồng vay, Ngân hàng, Số tiền vay, Dư nợ gốc, Lãi suất, Ngày giải ngân, Ngày đáo hạn, Kỳ trả nợ tới, Lãi phải trả.

## Định khoản tự động

Báo cáo này là báo cáo, không tự định khoản. Các số liệu lấy từ:

| Số liệu | Nguồn |
|---|---|
| Dư nợ gốc | Số dư TK 341 / 342 của từng khoản vay |
| Lãi phải trả | TK 335 (chi phí phải trả) hoặc tính từ lịch trả lãi |
| Chi phí lãi vay lũy kế | TK 635 trong kỳ |

## Tình huống đặc biệt & cảnh báo

- **Dư nợ cuối kỳ không khớp Sổ cái:** Kiểm tra các bút toán trả nợ đã ghi sổ đúng TK chưa. Có thể trả nợ bị ghi nhầm sang TK khác.
- **Lãi phải trả chưa ghi nhận dồn tích:** Cuối kỳ kế toán, nếu có lãi vay phát sinh nhưng chưa đến hạn trả, cần tạo bút toán dồn tích: Nợ 635 / Có 335.
- **Khoản vay sắp đáo hạn (≤ 30 ngày):** Cần chuẩn bị tiền để trả hoặc đàm phán gia hạn với ngân hàng.
- **Vay ngoại tệ:** Số liệu trên báo cáo có thể thay đổi theo tỷ giá nếu chưa đánh giá lại cuối kỳ.

## Báo cáo liên quan

- **Khoản vay ngân hàng**: danh sách chi tiết từng khoản vay.
- **Sổ Tài khoản ngân hàng**: sổ chi tiết TK 112 (theo dõi trả nợ).
- **Dự báo dòng tiền**: kế hoạch dòng tiền (các khoản trả nợ là dòng chi).
- **Báo cáo lãi lỗ**: TK 635 (chi phí lãi vay) trong kỳ.

## FAQ

**Q: Có thể xuất Excel báo cáo này không?**
**A:** Có. Bấm nút "Xuất Excel" trên báo cáo để tải về.

**Q: Có lọc được theo ngân hàng không?**
**A:** Có. Sử dụng bộ lọc "Ngân hàng" để xem khoản vay tại từng ngân hàng.

**Q: Số liệu "Lãi phải trả" có chính xác tuyệt đối không?**
**A:** Số liệu dựa trên lịch trả lãi đã cấu hình và bút toán dồn tích. Nếu chưa cấu hình lịch trả lãi hoặc chưa tạo bút toán dồn tích cuối kỳ, số liệu có thể thấp hơn thực tế.
