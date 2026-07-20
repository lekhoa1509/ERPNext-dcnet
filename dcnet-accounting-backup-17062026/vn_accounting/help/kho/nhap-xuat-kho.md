---
title: Nhập xuất kho
order: 2
summary: Phiếu nhập xuất kho dùng cho nhập, xuất, điều chuyển, sản xuất và đóng gói vật tư hàng hóa.
---

## Mục đích

**Phiếu nhập xuất kho** là chứng từ ghi nhận biến động số lượng và giá trị hàng tồn kho không gắn trực tiếp với hóa đơn mua/bán. Một phiếu có một **mục đích** quyết định cách hệ thống hạch toán:

| Mục đích | Diễn giải nghiệp vụ |
|---|---|
| Nhập kho | Nhập hàng vào một kho (chỉ có kho đến) — nhập khác, nhập điều chỉnh, nhập lại |
| Xuất kho | Xuất hàng khỏi một kho (chỉ có kho đi) — xuất dùng, xuất hủy |
| Điều chuyển kho | Chuyển hàng từ kho đi sang kho đến (có cả hai kho) |
| Sản xuất | Tiêu hao nguyên vật liệu để tạo thành phẩm theo định mức |
| Tiêu hao cho sản xuất | Xuất nguyên vật liệu phục vụ một lệnh sản xuất |
| Đóng gói | Tháo một mặt hàng thành nhiều mặt hàng khác (hoặc ngược lại) |

## Khi nào dùng

- Nhập hàng vào kho không qua hóa đơn mua hàng (hàng mẫu, nhập lại hàng trả, nhập điều chỉnh).
- Xuất vật tư/công cụ cho sản xuất hoặc dùng nội bộ.
- Điều chuyển hàng giữa các kho/chi nhánh.
- Sản xuất – tạo thành phẩm từ nguyên vật liệu theo định mức.
- Đóng gói/tháo gói: gộp nhiều linh kiện thành một bộ hoặc tách bộ thành linh kiện.

## Cách thực hiện

1. Bấm **Nhập xuất kho** trên menu Kho → danh sách phiếu nhập xuất kho mở.
2. Bấm **+ Thêm** → biểu mẫu phiếu nhập xuất kho mở.
   ![Danh sách phiếu nhập xuất kho](_images/nhap-xuat-kho-1.png)
3. Chọn **Loại phiếu** (mục đích): Nhập kho / Xuất kho / Điều chuyển kho / Sản xuất / Đóng gói.
4. Chọn **Ngày ghi sổ**, **Công ty**.
5. Trong bảng mặt hàng, thêm từng dòng:
   - **Kho đi** (xuất/điều chuyển), **Kho đến** (nhập/điều chuyển).
   - **Mặt hàng**, **Số lượng**, **Đơn giá** (giá nhập nếu nhập kho; với xuất kho hệ thống tự lấy theo phương pháp tính giá).
   - Nếu mặt hàng theo lô/seri: khai **số lô**/**số seri** tương ứng.
6. (Tùy chọn) Chọn **TK chênh lệch** nếu là nhập/xuất điều chỉnh.
7. **Lưu** rồi **Gửi/Ghi sổ** → hệ thống cập nhật Sổ kho và Sổ Cái.

## Định khoản tự động

Khi ghi sổ, phiếu nhập xuất kho sinh bút toán theo mục đích (phương pháp kê khai thường xuyên):

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Nhập kho (nhập khác) | 152/153/156 | TK chênh lệch (vd 632/642) hoặc 331 | Tăng tồn kho |
| Xuất kho cho sản xuất | 621/627 | 152/153 | Theo định mức sản xuất |
| Xuất kho dùng cho bán hàng/quản lý | 641/642 | 152/153 | Bộ phận sử dụng |
| Điều chuyển kho | 152/156 (kho đến) | 152/156 (kho đi) | Cùng TK, khác kho — không đổi tổng tồn |
| Sản xuất — tiêu hao NVL | 154 | 152 | Kết chuyển chi phí NVL vào dở dang |
| Sản xuất — nhập thành phẩm | 155 | 154 | Nhập thành phẩm từ chi phí dở dang |
| Đóng gói | TK mặt hàng đầu ra | TK mặt hàng đầu vào | Giá trị bảo toàn (chênh do chi phí gia công ghi vào TK chênh lệch) |

Đối với **điều chuyển kho** trong cùng một tài khoản kho, hệ thống chỉ cập nhật Sổ kho theo kho; giá trị trên Sổ Cái không đổi nếu hai kho cùng dùng một TK hàng tồn.

## Tình huống đặc biệt & cảnh báo

- **Tồn âm:** xuất quá tồn → hệ thống chặn hoặc cảnh báo tùy thiết lập kho. Không để tồn âm vì làm sai giá vốn.
- **Hàng theo lô có hạn dùng:** khi xuất, ưu tiên xuất lô hết hạn trước; lô đã quá hạn không nên cho xuất bán.
- **Hàng theo seri:** mỗi seri chỉ tồn ở một kho tại một thời điểm; xuất seri đã xuất rồi sẽ báo lỗi.
- **Sửa phiếu đã ghi sổ:** không sửa trực tiếp. Hủy phiếu → tạo phiếu mới. Hủy phiếu sản xuất/đóng gói có thể vướng ràng buộc lô/seri đã sinh.
- **TK chênh lệch nhập/xuất điều chỉnh:** nếu không khai, hệ thống lấy TK điều chỉnh hàng tồn kho mặc định của công ty (thường là TK giá vốn 632).
- **Sản xuất cần định mức:** phiếu Sản xuất nên gắn với lệnh sản xuất/định mức để tự sinh dòng tiêu hao và thành phẩm.

## Báo cáo liên quan

- **Sổ chi tiết kho:** truy vết từng dòng nhập/xuất của phiếu.
- **BC nhập xuất tồn:** tổng hợp ảnh hưởng của phiếu tới tồn kho.
- **Kiểm kê kho:** đối chiếu sổ với thực tế sau các phiếu nhập/xuất.
- **Số lô / Số seri:** tra cứu lô/seri được phiếu sinh ra hoặc tiêu thụ.

## FAQ

**Q: Khác nhau giữa phiếu nhập xuất kho và phiếu nhập kho / phiếu xuất kho của Mua – Bán?**
**A:** Phiếu nhập kho (Mua hàng) và phiếu xuất kho (Bán hàng) gắn với hóa đơn và đối tác. Phiếu nhập xuất kho dùng cho nghiệp vụ kho nội bộ: xuất dùng, điều chuyển, sản xuất, đóng gói, nhập/xuất điều chỉnh.

**Q: Điều chuyển kho có làm thay đổi giá vốn không?**
**A:** Không, nếu hai kho cùng dùng một tài khoản hàng tồn kho — chỉ chuyển số lượng giữa kho. Tổng giá trị tồn của công ty không đổi.

**Q: Phiếu sản xuất tự tính giá thành phẩm thế nào?**
**A:** Giá thành = tổng giá trị nguyên vật liệu tiêu hao (+ chi phí gia công nếu khai). Hệ thống kết chuyển NVL vào TK 154 rồi nhập thành phẩm TK 155 theo giá thành đó.

**Q: Lỡ xuất nhầm kho thì sao?**
**A:** Hủy phiếu rồi lập lại với kho đúng. Nếu phiếu đã sinh lô/seri, cần kiểm tra ràng buộc trước khi hủy.
