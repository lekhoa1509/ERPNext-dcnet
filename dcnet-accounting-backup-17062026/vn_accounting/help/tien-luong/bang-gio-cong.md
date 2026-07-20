---
title: Bảng giờ công (theo dự án)
order: 2
summary: Ghi nhận giờ làm việc của nhân viên theo từng dự án/công việc để theo dõi chi phí nhân công và làm căn cứ phân bổ.
---

## Mục đích

**Bảng giờ công** ghi nhận số giờ làm việc của nhân viên theo từng dự án, hoạt động hoặc công việc. Mỗi dòng giờ công có **giá vốn** (chi phí nhân công) và tùy chọn **giá trị tính cho khách** (nếu công việc tính phí). Bảng giờ công là căn cứ để theo dõi và phân bổ chi phí nhân công theo dự án — đặc biệt hữu ích cho doanh nghiệp dịch vụ, thi công, tư vấn.

## Khi nào dùng

- Nhân viên làm việc cho nhiều dự án trong kỳ → cần tách giờ công để biết chi phí nhân công mỗi dự án.
- Cần căn cứ định lượng để kế toán phân bổ một phần lương vào TK 154/627 theo dự án.
- Doanh nghiệp tính phí dịch vụ theo giờ → ghi nhận giờ tính phí để lập hóa đơn.

## Cách thực hiện

1. Bấm **Bảng giờ công (theo dự án)** → danh sách bảng giờ công mở ra.
2. Bấm **+ Thêm**: chọn **Nhân viên**, thêm các dòng chi tiết với **Hoạt động/Công việc**, **Dự án**, **Giờ bắt đầu — kết thúc** (hoặc **Số giờ**).
3. Đánh dấu **Tính phí** cho dòng cần tính cho khách; nhập đơn giá giờ công nếu có.
4. Bấm **Lưu** rồi **Duyệt** để chốt.

## Định khoản tự động

Bảng giờ công **không tự sinh bút toán Sổ Cái**. Hệ thống chỉ tính tổng **giá vốn** (chi phí nhân công) và **giá trị tính phí** trên chứng từ. Chi phí lương thực tế chỉ vào Sổ Cái qua bút toán của Bảng lương.

Để đưa chi phí nhân công vào dự án, kế toán dùng một trong hai cách:
- Bút toán phân bổ lương theo tỷ lệ giờ công (Dr 154/627 theo dự án / Cr phần lương 622) — xem phân hệ Giá thành.
- Hoặc cấu hình bút toán lương đã gắn dự án/trung tâm chi phí ngay từ Bảng lương.

## Tình huống đặc biệt & cảnh báo

- **Giờ công ≠ chi phí kế toán.** Đây là một cảnh báo quan trọng theo VAS: lương kỹ sư on-site hạch toán qua Bảng lương (Dr 622 / Cr 334), KHÔNG lấy giá vốn giờ công làm số liệu Sổ Cái. Dùng giờ công làm **bằng chứng tỷ lệ** để chia phân bổ lương, không phải nguồn chi phí trực tiếp.
- **Trùng giờ:** hệ thống cảnh báo nếu một nhân viên có hai dòng giờ công chồng thời gian trong cùng khoảng.
- **Dự án bắt buộc:** nếu mục đích là phân bổ chi phí theo dự án, đảm bảo mỗi dòng đều gắn Dự án; dòng thiếu Dự án sẽ không vào được báo cáo chi phí theo dự án.

## Báo cáo liên quan

- [Bảng lương](bang-luong.md): nguồn chi phí lương thực tế trên Sổ Cái.
- Phân hệ **Giá thành**: tập hợp và phân bổ chi phí nhân công vào dự án (TK 154/627).

## FAQ

**Q: Ghi giờ công xong là chi phí dự án tăng đúng không?**
**A:** Không trực tiếp. Giờ công chỉ ghi nhận thời gian và giá trị; chi phí lương vào dự án qua bút toán lương hoặc bút toán phân bổ. Đừng coi giá vốn giờ công là số đã ghi sổ.

**Q: Vì sao không nên lấy giờ công làm nguồn tính giá vốn 632?**
**A:** Nếu chốt COGS từ giờ công, số tiền có thể lớn hơn chi phí lương thực có trong TK 154, làm TK 154 âm. Luôn lấy chi phí lương thực tế từ Bảng lương làm gốc.

**Q: Giờ tính phí dùng để làm gì?**
**A:** Làm căn cứ lập hóa đơn dịch vụ theo giờ cho khách hàng — thuộc phân hệ Bán hàng, không liên quan tới định khoản chi phí lương.
