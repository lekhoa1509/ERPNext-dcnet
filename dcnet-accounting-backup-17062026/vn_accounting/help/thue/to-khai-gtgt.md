---
title: Tờ khai thuế GTGT (01/GTGT)
order: 3
summary: Lập tờ khai thuế GTGT mẫu 01/GTGT theo TT80/2021, tự tổng hợp đầu ra/đầu vào và tính số thuế phải nộp.
---

## Mục đích

Báo cáo **Tờ khai thuế GTGT (01/GTGT)** lập tờ khai thuế giá trị gia tăng theo mẫu **01/GTGT (TT80/2021)** cho phương pháp khấu trừ. Hệ thống **tự tổng hợp** thuế đầu ra từ hóa đơn bán hàng và thuế đầu vào từ hóa đơn mua hàng đã ghi sổ trong kỳ, rồi tính số thuế phải nộp hoặc còn được khấu trừ chuyển kỳ sau. Dùng cho kế toán thuế lập tờ khai định kỳ.

## Khi nào dùng

- Cuối tháng (doanh nghiệp kê khai theo tháng) hoặc cuối quý (kê khai theo quý) để lập tờ khai.
- Đối chiếu số thuế GTGT phải nộp trước khi nộp tiền vào ngân sách.
- Kiểm tra thuế đầu vào còn được khấu trừ chuyển sang kỳ sau.
- Rà soát doanh thu chịu thuế theo từng thuế suất.

## Cách thực hiện

1. Bấm **Tờ khai thuế GTGT (01/GTGT)** trên menu Thuế → báo cáo mở.
   ![Tờ khai 01/GTGT](_images/to-khai-gtgt-1.png)
2. Chọn bộ lọc:
   - **Công ty** (mặc định công ty đang làm việc).
   - **Kỳ tính thuế**: chọn **Tháng** hoặc **Quý** — khi đổi, hệ thống tự đặt lại Từ ngày / Đến ngày cho đúng đầu–cuối kỳ.
   - **Từ ngày / Đến ngày**: khoảng kỳ kê khai.
   - **Thuế GTGT đầu vào được KT kỳ trước chuyển sang [30]**: nhập tay số thuế đầu vào còn được khấu trừ từ kỳ trước (nếu có).
3. Bấm **Refresh** → tờ khai hiển thị theo 4 phần A, B, C, D với các chỉ tiêu có mã số trong ngoặc vuông.
4. Đối chiếu các chỉ tiêu, đặc biệt là [34] (phải nộp), [36] (còn phải nộp), [37] (chuyển kỳ sau).

### Cấu trúc tờ khai

| Phần | Chỉ tiêu | Ý nghĩa | Nguồn số liệu |
|---|---|---|---|
| **A** | [21] | Không phát sinh hoạt động mua bán trong kỳ | Đánh dấu thủ công |
| **B** Đầu ra | [22] | HHDV bán ra không phải kê khai tính nộp thuế | Hóa đơn bán, doanh thu |
| | [23] | HHDV bán ra thuế suất 0% | Hóa đơn bán, doanh thu |
| | [24] | HHDV bán ra thuế suất 5% | Hóa đơn bán (thuế 33311) |
| | [25] | HHDV bán ra thuế suất 10% | Hóa đơn bán (thuế 33311) |
| | [26a]/[26b] | Điều chỉnh tăng/giảm kỳ trước | Hóa đơn điều chỉnh/trả hàng |
| | [27] | Tổng doanh thu chịu thuế = [24]+[25] | Tự tính |
| | [28] | Thuế đầu ra của [24]+[25] | Tự tính |
| | [29] | Tổng thuế đầu ra = [28]+[26a]−[26b] | Tự tính |
| **C** Đầu vào | [30] | Thuế đầu vào kỳ trước chuyển sang | **Nhập tay** |
| | [31] | Thuế GTGT mua vào trong nước | Hóa đơn mua (thuế 133) |
| | [32] | Thuế GTGT nhập khẩu | Hóa đơn mua + phiếu kế toán 133/33312 |
| | [33] | Tổng thuế đầu vào khấu trừ = [30]+[31]+[32] | Tự tính |
| **D** Phải nộp | [34] | Thuế GTGT phải nộp = [29]−[33] | Tự tính |
| | [35] | Thuế GTGT đã nộp trong kỳ | Phiếu kế toán nộp thuế (Có 33311) |
| | [36] | Còn phải nộp = [34]−[35] | Tự tính |
| | [37] | Đầu vào khấu trừ chuyển kỳ sau | = max(0, −[34]) |

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ tra cứu và tổng hợp số liệu để lập tờ khai. Các bút toán liên quan đến thuế được sinh từ chứng từ gốc:

| Nghiệp vụ | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Kết chuyển thuế khấu trừ cuối kỳ | 3331 | 1331 | Bù trừ đầu ra với đầu vào |
| Nộp thuế GTGT vào ngân sách | 3331 | 112 | Phiếu kế toán nộp tiền — vào chỉ tiêu [35] |

## Tình huống đặc biệt & cảnh báo

- **Chỉ tiêu [30] phải nhập tay:** số thuế đầu vào còn được khấu trừ kỳ trước (= [37] kỳ trước) không tự kéo sang — kế toán nhập đúng vào ô lọc, nếu bỏ trống hệ thống mặc định 0.
- **[37] chuyển kỳ sau:** chỉ phát sinh khi thuế đầu vào lớn hơn đầu ra (số [34] âm). Khi đó [34] không hiển thị âm như "phải nộp" mà phần dương được đưa vào [37].
- **Tài khoản nhận diện:** đầu ra nhận hóa đơn có tài khoản thuế chứa **"33311"**; đầu vào nhận hóa đơn có tài khoản chứa **"133"**; thuế nhập khẩu nhận thêm phiếu kế toán định khoản Nợ 133 / Có 33312. Mẫu thuế phải trỏ đúng các tài khoản này.
- **Chỉ tính chứng từ đã ghi sổ:** hóa đơn còn nháp không được tổng hợp.
- **[35] thuế đã nộp:** lấy từ vế Có TK 33311 trên phiếu kế toán nộp thuế trong kỳ — đảm bảo đã hạch toán đúng khi nộp tiền.
- **Thời hạn nộp tờ khai (TT80/2021):** theo tháng — chậm nhất ngày 20 tháng sau; theo quý — chậm nhất ngày cuối cùng của tháng đầu quý sau.

## Báo cáo liên quan

- **HĐ GTGT đầu ra**: nguồn thuế đầu ra (chỉ tiêu [22]–[29]).
- **HĐ GTGT đầu vào**: nguồn thuế đầu vào (chỉ tiêu [31]–[32]).
- **Sổ Cái TK 3331 / 1331**: chi tiết phát sinh thuế để truy nguồn từng dòng.
- **Bảng cân đối số phát sinh**: đối chiếu số dư TK 3331, 1331 cuối kỳ.

## FAQ

**Q: Vì sao tờ khai trống dù đã có hóa đơn?**
**A:** Kiểm tra (1) hóa đơn đã ghi sổ chưa, (2) khoảng ngày lọc có bao hóa đơn không, (3) tài khoản thuế trên mẫu thuế có chứa "33311" (đầu ra) / "133" (đầu vào) không.

**Q: Số ở [30] hệ thống có tự điền không?**
**A:** Không. Đây là số thuế đầu vào còn được khấu trừ kỳ trước — kế toán nhập tay vào ô lọc. Lấy đúng bằng chỉ tiêu [37] của tờ khai kỳ liền trước.

**Q: [34] ra số âm nghĩa là gì?**
**A:** Thuế đầu vào lớn hơn đầu ra — không phải nộp thuế, phần chênh được chuyển sang kỳ sau ở chỉ tiêu [37].

**Q: Tờ khai theo thông tư nào?**
**A:** Mẫu 01/GTGT theo TT80/2021 về quản lý thuế. Các tài khoản hạch toán theo VAS TT99/2025 (3331/1331).
