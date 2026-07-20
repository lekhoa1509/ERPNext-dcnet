---
title: Dự báo dòng tiền
order: 11
summary: Công cụ dự báo dòng tiền tương lai — tổng hợp thu/chi dự kiến từ hóa đơn, hợp đồng, khoản vay.
---

## Mục đích

**Dự báo dòng tiền** là công cụ giúp doanh nghiệp ước tính dòng tiền trong tương lai dựa trên dữ liệu hiện có: hóa đơn phải thu/phải trả, lịch thanh toán hợp đồng, lịch trả nợ vay, và tiền gửi có kỳ hạn sắp đáo hạn. Giúp ban giám đốc lên kế hoạch tài chính và tránh thiếu hụt tiền mặt.

## Khi nào dùng

- **Hàng tuần/tháng:** lập kế hoạch dòng tiền cho tuần/tháng tới.
- **Trước khi ký hợp đồng lớn:** đánh giá khả năng thanh toán trong tương lai.
- **Khi có biến động lớn:** khoản vay mới, khoản đầu tư lớn, thay đổi chính sách tín dụng.
- **Báo cáo ban giám đốc/hội đồng quản trị:** tình hình tài chính dự kiến.

## Cách thực hiện

1. Bấm **Dự báo dòng tiền** trên menu Ngân hàng → trang Dự báo dòng tiền mở.
2. Chọn **Khoảng thời gian dự báo** (tuần, tháng, quý tới).
3. Hệ thống tự động tổng hợp các nguồn thu/chi dự kiến:
   - **Thu dự kiến**: hóa đơn bán hàng đến hạn, hợp đồng đến kỳ thu tiền, sổ tiền gửi đáo hạn.
   - **Chi dự kiến**: hóa đơn mua hàng đến hạn, lịch trả lương, lịch trả nợ vay, thuế phải nộp.
4. Biểu đồ dòng tiền hiển thị số dư dự kiến theo ngày/tuần/tháng.
5. Điều chỉnh thủ công: thêm các khoản thu/chi chưa có trên hệ thống (dự án mới, chi phí dự kiến).

### Nguồn dữ liệu

| Loại | Nguồn |
|---|---|
| Thu từ khách hàng | Hóa đơn bán hàng (Sales Invoice) đến hạn thanh toán |
| Thu từ hợp đồng | Lịch thu tiền định kỳ trên DCNET Contract |
| Thu từ tiền gửi đáo hạn | Tiền gửi có kỳ hạn đến ngày đáo hạn |
| Chi trả nhà cung cấp | Hóa đơn mua hàng (Purchase Invoice) đến hạn thanh toán |
| Chi lương | Bảng lương dự kiến (theo kỳ lương) |
| Chi trả nợ vay | Lịch trả nợ trên Khoản vay ngân hàng |
| Chi nộp thuế | Thuế phải nộp định kỳ (GTGT hàng tháng, TNDN hàng quý) |

## Định khoản tự động

Dự báo dòng tiền là công cụ kế hoạch, không tạo bút toán. Không ảnh hưởng đến sổ sách kế toán.

## Tình huống đặc biệt & cảnh báo

- **Dự báo chỉ chính xác bằng dữ liệu đầu vào:** Nếu hóa đơn chưa được nhập, hợp đồng chưa cập nhật lịch thanh toán, dự báo sẽ thiếu. Cập nhật dữ liệu đầy đủ trước khi xem dự báo.
- **Thu/chi ngoài dự kiến:** Các khoản đột xuất (phạt, bồi thường, thưởng) cần thêm thủ công vào dự báo.
- **Số dư âm dự kiến:** Nếu biểu đồ báo số dư âm trong tương lai, cần có biện pháp: trì hoãn chi, đẩy nhanh thu, hoặc vay bổ sung.
- **Dung sai:** Dự báo càng xa càng kém chính xác. Dự báo 1-2 tuần có độ chính xác cao; 3-6 tháng chỉ nên dùng làm định hướng.
- **Tỷ giá:** Nếu có giao dịch ngoại tệ, dự báo sử dụng tỷ giá hiện tại — chưa tính biến động tỷ giá tương lai.

## Báo cáo liên quan

- **Thu ngân hàng / Chi ngân hàng**: giao dịch thực tế (đối chiếu dự báo vs thực tế).
- **Báo cáo công nợ**: chi tiết các khoản phải thu/phải trả.
- **Tổng hợp khoản vay ngân hàng**: lịch trả nợ.
- **Tổng hợp tiền gửi có kỳ hạn**: các sổ sắp đáo hạn.

## FAQ

**Q: Dự báo dòng tiền có tự động cập nhật không?**
**A:** Dữ liệu được lấy từ hệ thống tại thời điểm mở trang. Mỗi lần mở trang, hệ thống tổng hợp lại từ dữ liệu mới nhất. Không có cron job chạy nền tự động.

**Q: Có thể xuất báo cáo dự báo dòng tiền không?**
**A:** Có thể xuất dữ liệu ra Excel từ trang dự báo để gửi cho ban giám đốc.

**Q: Làm sao để thêm các khoản thu/chi chưa có trên hệ thống?**
**A:** Sử dụng chức năng "Thêm thủ công" trên trang dự báo để nhập các khoản dự kiến chưa được ghi nhận trong hệ thống (dự án mới, chi phí ước tính).

**Q: Dự báo có bao gồm thuế GTGT không?**
**A:** Có — nếu hóa đơn có thuế, số tiền dự báo là tổng tiền thanh toán (bao gồm VAT).
