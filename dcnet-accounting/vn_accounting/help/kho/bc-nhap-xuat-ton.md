---
title: BC nhập xuất tồn
order: 7
summary: Báo cáo tổng hợp tồn đầu – nhập – xuất – tồn cuối theo mặt hàng và kho.
---

## Mục đích

**Báo cáo nhập xuất tồn** cho bức tranh tổng quát về biến động hàng tồn kho trong kỳ: với mỗi mặt hàng (theo kho), báo cáo hiển thị **tồn đầu kỳ**, **nhập trong kỳ**, **xuất trong kỳ** và **tồn cuối kỳ** — cả về số lượng lẫn giá trị. Đây là báo cáo kho được dùng nhiều nhất để chốt số và đối chiếu với Sổ Cái các TK 152/153/155/156.

## Khi nào dùng

- Cuối tháng/quý/năm: chốt tồn kho và đối chiếu giá trị tồn với Sổ Cái.
- Theo dõi luân chuyển hàng: mặt hàng nào nhập/xuất nhiều, mặt hàng nào ứ đọng.
- Kiểm tra giá trị tồn theo kho/nhóm hàng phục vụ báo cáo tài chính.
- Đối chiếu trước kiểm kê: lấy số tồn sổ sách để so với thực tế.

## Cách thực hiện

1. Bấm **BC nhập xuất tồn** trên menu Kho → báo cáo mở.
   ![Báo cáo nhập xuất tồn](_images/bc-nhap-xuat-ton-1.png)
2. Nhập bộ lọc:
   - **Công ty** (mặc định công ty đang làm việc).
   - **Từ ngày / Đến ngày** (kỳ báo cáo).
   - **Nhóm hàng**, **Mặt hàng**, **Kho**, **Loại kho** (tùy chọn).
   - Tùy chọn nâng cao: hiện hàng tồn 0, hiện thuộc tính biến thể, kèm dữ liệu tuổi kho.
3. Bấm **Refresh** → bảng hiển thị các cột: **Mặt hàng**, **Tên hàng**, **Nhóm hàng**, **Kho**, **Đơn vị**, **SL tồn đầu / Giá trị tồn đầu**, **SL nhập / Giá trị nhập**, **SL xuất / Giá trị xuất**, **SL tồn cuối / Giá trị tồn cuối**, **Đơn giá bình quân**.
4. Xuất Excel để lưu/đối chiếu nếu cần.

## Định khoản tự động

**Không tự định khoản** — đây là báo cáo tra cứu, chỉ tổng hợp số liệu kho hiện có, không sinh bút toán.

## Tình huống đặc biệt & cảnh báo

- **Giá trị tồn cuối khớp Sổ Cái:** tổng giá trị tồn cuối từng nhóm hàng phải khớp số dư TK 152/153/155/156 tương ứng trên Sổ Cái; lệch là dấu hiệu thiếu bút toán hoặc giá vốn sai.
- **Tồn âm:** nếu một dòng báo tồn cuối âm → có phiếu xuất trước phiếu nhập hoặc sai ngày; cần rà lại theo Sổ chi tiết kho.
- **Đơn giá bình quân:** thay đổi theo phương pháp tính giá; sửa giá nhập sau khi đã xuất làm đơn giá lệch.
- **Lọc khoảng ngày:** tồn đầu kỳ = số dư trước "Từ ngày"; chọn sai mốc làm sai tồn đầu.
- **Báo cáo nền tảng ERP:** đây là báo cáo chuẩn của hệ thống, mô tả theo nghiệp vụ VN; cột và bộ lọc theo bản hiện hành.

## Báo cáo liên quan

- **Sổ chi tiết kho:** xem chi tiết từng lần nhập/xuất tạo nên số tổng hợp.
- **BC tuổi kho:** phân tích hàng tồn lâu ngày.
- **Định mức tồn kho:** gợi ý điểm đặt hàng lại.
- **Bảng cân đối số phát sinh:** đối chiếu số dư các TK hàng tồn kho.

## FAQ

**Q: Tồn đầu kỳ lấy từ đâu?**
**A:** Là số dư tồn kho ngay trước ngày "Từ ngày" của bộ lọc — tổng hợp toàn bộ nhập/xuất trước mốc đó.

**Q: Vì sao giá trị tồn cuối lệch với Sổ Cái?**
**A:** Thường do thiếu bút toán giá vốn, phiếu chưa ghi sổ, hoặc sửa giá nhập sau khi đã xuất. Dùng Sổ chi tiết kho để truy về phiếu gây lệch.

**Q: Báo cáo có hiện hàng tồn bằng 0 không?**
**A:** Mặc định ẩn hàng tồn 0; bật tùy chọn "hiện hàng tồn 0" nếu muốn xem cả mặt hàng đã hết.

**Q: Có thể xem theo từng kho không?**
**A:** Có. Lọc theo **Kho** hoặc **Loại kho**; báo cáo tách dòng theo mặt hàng – kho.
