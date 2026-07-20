---
title: Sổ nhật ký chung (S03a-DN)
order: 6
summary: Sổ kế toán ghi mọi bút toán theo trình tự thời gian, mẫu S03a-DN theo TT99/2025.
---

## Mục đích

**Sổ nhật ký chung (S03a-DN)** liệt kê toàn bộ bút toán đã ghi sổ trong kỳ theo trình tự thời gian, mỗi dòng thể hiện tài khoản, số phát sinh Nợ/Có và tài khoản đối ứng. Đây là sổ kế toán bắt buộc theo Phụ lục IV Thông tư 99/2025/TT-BTC (mẫu S03a-DN), nộp kèm hồ sơ quyết toán thuế hằng năm. Báo cáo chỉ TRA CỨU, không tạo chứng từ.

## Khi nào dùng

- **In sổ định kỳ** (tháng/quý/năm) để lưu trữ và nộp cơ quan thuế.
- **Đối chiếu kiểm toán** — soát toàn bộ phát sinh theo thời gian.
- **Truy vết một nghiệp vụ** — tìm theo ngày, theo số chứng từ.
- **Kiểm tra cân đối** — tổng Phát sinh Nợ phải bằng tổng Phát sinh Có ở dòng cộng cuối.

## Cách thực hiện

1. Mở **Tổng hợp → Sổ nhật ký chung (S03a-DN)**.
2. Nhập bộ lọc: **Công ty** (mặc định công ty hiện hành), **Từ ngày / Đến ngày** (mặc định đầu năm → cuối năm tài chính).
3. Bấm **Chạy báo cáo** → bảng hiển thị các dòng bút toán sắp theo Ngày ghi sổ tăng dần, dòng cuối là "Cộng phát sinh kỳ".
4. Xuất file: bấm **Thực đơn → Tải về** chọn PDF/Excel theo định dạng S03a-DN.

### Các cột chính

| Cột | Ý nghĩa |
|---|---|
| Ngày ghi sổ | Ngày hạch toán chứng từ |
| Số CT | Số hiệu chứng từ (bấm để mở chứng từ gốc) |
| Ngày CT | Ngày của chứng từ gốc |
| Diễn giải | Nội dung nghiệp vụ |
| Đã ghi SC | Đã ghi Sổ Cái — luôn ✓ vì bút toán đã có trên Sổ Cái |
| STT dòng | Số thứ tự dòng trong cùng một bút toán |
| Tài khoản | Tài khoản kế toán của dòng này |
| TK đối ứng | Tài khoản đối ứng của bút toán |
| PS Nợ / PS Có | Số phát sinh bên Nợ / bên Có |

## Định khoản tự động

Không tự định khoản — đây là sổ tra cứu tổng hợp toàn bộ bút toán đã ghi sổ. Không tạo chứng từ mới.

## Tình huống đặc biệt & cảnh báo

- **Chỉ gồm bút toán đã ghi sổ:** sổ lấy dữ liệu từ Sổ Cái (các bút toán đã ghi sổ, chưa bị hủy). Phiếu còn ở trạng thái Nháp KHÔNG xuất hiện.
- **Một chứng từ nhiều dòng:** mỗi chứng từ có thể có nhiều cặp Nợ/Có — cột STT dòng đánh số trong cùng bút toán; chỉ dòng đầu hiển thị Ngày/Số CT/Diễn giải để tránh lặp.
- **Tổng Nợ phải bằng tổng Có:** nếu dòng "Cộng phát sinh kỳ" hai cột lệch nhau là có bút toán lỗi cân đối — kiểm tra ngay (thường do bút toán ngoại tệ chưa quy đổi đúng).
- **Lọc theo tháng riêng:** đặt Từ ngày = đầu tháng, Đến ngày = cuối tháng (VD 01/04/2026 → 30/04/2026).

## Báo cáo liên quan

- [Sổ cái (S03b-DN)](so-cai.md): xem chi tiết phát sinh của TỪNG tài khoản.
- [Sổ chi tiết tài khoản](so-chi-tiet-tai-khoan.md): chi tiết tài khoản kèm đối tượng + bộ phận.
- [Bảng cân đối số phát sinh](trial-balance.md): tổng hợp số dư và phát sinh mọi tài khoản.

## FAQ

**Q: Tổng Phát sinh Nợ khác Tổng Phát sinh Có thì sao?**
**A:** Không nên xảy ra. Nếu có, kiểm tra bút toán lỗi cân đối hoặc bút toán ngoại tệ chưa quy đổi theo đồng tiền gốc của công ty; liên hệ KTT soát xét.

**Q: Sao không thấy phiếu vừa tạo?**
**A:** Sổ chỉ gồm chứng từ đã ghi sổ. Ghi sổ (Submit) phiếu trước, sổ sẽ hiển thị.

**Q: Khác gì Sổ cái?**
**A:** Sổ nhật ký chung ghi MỌI nghiệp vụ theo thời gian (không chia tài khoản). Sổ cái gom theo TỪNG tài khoản, mỗi tài khoản một trang.
