---
title: Kiểm kê kho
order: 4
summary: Biên bản kiểm kê đối chiếu tồn kho thực tế với sổ sách, điều chỉnh chênh lệch thừa/thiếu.
---

## Mục đích

**Biên bản kiểm kê kho** ghi nhận số lượng (và giá trị) hàng tồn kho **thực tế đếm được** so với số liệu trên sổ sách, rồi điều chỉnh chênh lệch. Đây là chứng từ chốt tồn kho định kỳ và là cơ sở pháp lý khi có thừa/thiếu. Khi ghi sổ, biên bản tự cập nhật lại số lượng tồn về đúng thực tế và sinh bút toán điều chỉnh giá trị.

Biên bản có hai mục đích:
- **Tồn đầu kỳ:** khai số dư tồn kho ban đầu khi mới đưa hệ thống vào dùng.
- **Kiểm kê kho:** điều chỉnh tồn kho theo kết quả đếm thực tế trong kỳ.

## Khi nào dùng

- **Khởi tạo hệ thống:** nhập tồn kho đầu kỳ cho từng mặt hàng/kho.
- **Cuối tháng/quý/năm:** kiểm kê định kỳ, đối chiếu sổ với thực tế.
- **Phát hiện chênh lệch:** hỏng, mất, hao hụt, đếm sai → điều chỉnh về số thực.
- **Bàn giao thủ kho:** chốt tồn khi thay người phụ trách kho.

## Cách thực hiện

1. Bấm **Kiểm kê kho** trên menu Kho → danh sách biên bản kiểm kê mở.
2. Bấm **+ Thêm** → biểu mẫu kiểm kê kho mở.
   ![Danh sách biên bản kiểm kê kho](_images/kiem-ke-kho-1.png)
3. Chọn **Mục đích**: Tồn đầu kỳ hoặc Kiểm kê kho.
4. Chọn **Ngày ghi sổ**, **Công ty**.
5. Lấy danh sách tồn hiện tại theo kho (nút lấy mặt hàng theo kho), hoặc thêm thủ công từng dòng.
6. Với mỗi dòng nhập **Số lượng thực tế** (và **Đơn giá** nếu là tồn đầu kỳ). Hệ thống so sánh với số sổ sách và tính **chênh lệch**.
7. Chọn **TK chênh lệch** (mặc định lấy TK điều chỉnh hàng tồn kho của công ty).
8. **Lưu** rồi **Ghi sổ** → tồn kho được điều chỉnh về số thực tế, sinh bút toán chênh lệch.

## Định khoản tự động

Khi ghi sổ, biên bản kiểm kê sinh bút toán điều chỉnh giá trị hàng tồn kho:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Thực tế > sổ sách (thừa) | 152/153/155/156 | 3381 | Tài sản thừa chờ xử lý; sau đó xử lý theo quyết định |
| Thực tế < sổ sách (thiếu) | 1381 | 152/153/155/156 | Tài sản thiếu chờ xử lý |
| Sau khi có quyết định xử lý thiếu | 632 / 1388 / 334 | 1381 | Tính vào giá vốn / quy trách nhiệm bồi thường |
| Sau khi có quyết định xử lý thừa | 3381 | 711 | Ghi nhận thu nhập khác |

Lưu ý: TK chênh lệch hệ thống dùng mặc định là **TK điều chỉnh hàng tồn kho** của công ty (thường là giá vốn 632). Để phản ánh đúng VAS thừa/thiếu chờ xử lý (TK 1381/3381), kế toán nên đổi TK chênh lệch hoặc lập bút toán phân loại lại sau khi ghi sổ.

## Tình huống đặc biệt & cảnh báo

- **Tồn đầu kỳ và kỳ đã khóa sổ:** nếu công ty đã có chứng từ kết chuyển cuối kỳ, biên bản Tồn đầu kỳ có thể bị chặn — cần xử lý kỳ kế toán trước.
- **TK chênh lệch là TK kết quả (632…):** hệ thống yêu cầu TK chênh lệch thuộc nhóm chi phí/thu nhập; với mục đích Tồn đầu kỳ thì cần TK loại tài sản/nguồn vốn.
- **Hàng theo lô/seri:** kiểm kê phải khai đúng lô/seri; chênh lệch số lượng theo từng lô/seri.
- **Chênh lệch lớn:** lập biên bản nghi vấn, đợi quyết định ban giám đốc trước khi kết chuyển vào chi phí.
- **Đếm trong lúc còn nhập/xuất:** nên khóa kho khi kiểm kê để số thực tế và số sổ ở cùng một thời điểm.

## Báo cáo liên quan

- **BC nhập xuất tồn:** cung cấp số tồn sổ sách trước khi kiểm kê.
- **Sổ chi tiết kho:** truy vết bút toán điều chỉnh do kiểm kê sinh ra.
- **Nhập xuất kho:** xử lý tiếp chênh lệch (nếu cần phiếu riêng).

## FAQ

**Q: Kiểm kê kho có tự sửa số lượng tồn không?**
**A:** Có. Khi ghi sổ, biên bản cập nhật tồn kho về đúng số thực tế đã khai và sinh bút toán điều chỉnh giá trị tương ứng.

**Q: Vì sao bút toán chênh lệch lại vào TK 632 chứ không phải 1381/3381?**
**A:** Hệ thống dùng TK điều chỉnh hàng tồn kho mặc định của công ty. Muốn theo đúng VAS (thừa/thiếu chờ xử lý), hãy đổi TK chênh lệch sang 1381/3381 hoặc phân loại lại bằng bút toán sau khi ghi sổ.

**Q: Khai tồn đầu kỳ bằng mục nào?**
**A:** Dùng biên bản kiểm kê kho với mục đích **Tồn đầu kỳ** — nhập số lượng và đơn giá cho từng mặt hàng/kho.

**Q: Kiểm kê xong có in biên bản được không?**
**A:** Có. Biên bản kiểm kê kho có mẫu in để ký xác nhận ba bên (thủ kho, kế toán, ban giám đốc).
