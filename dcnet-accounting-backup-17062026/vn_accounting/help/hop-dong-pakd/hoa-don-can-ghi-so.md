---
title: Hóa đơn cần ghi sổ
order: 3
summary: Danh sách công việc — hóa đơn nháp gắn hợp đồng do hệ thống tự sinh khi đến kỳ, chờ kế toán ghi sổ (duyệt) rồi xuất hóa đơn VAT.
---

## Mục đích

**Hóa đơn cần ghi sổ** là danh sách công việc cho kế toán: liệt kê các **hóa đơn bán hàng còn ở dạng nháp** (chưa ghi sổ) được hệ thống tự sinh từ lịch của hợp đồng khi thuê bao đến kỳ. Kế toán mở báo cáo này để rà soát + **ghi sổ** (duyệt) — sau đó mới xuất hóa đơn VAT chính thức.

Báo cáo chỉ hiện hóa đơn **gắn một hợp đồng**; hóa đơn nháp lẻ ngoài hợp đồng nằm ở danh sách hóa đơn bán hàng thông thường. Cột **"Chờ ghi sổ (ngày)"** tính sẵn để ưu tiên ghi sổ hóa đơn tồn nháp lâu nhất trước.

## Khi nào dùng

- Hằng ngày: rà các hóa đơn nháp mới sinh để ghi sổ kịp thời.
- Khi cần biết hóa đơn nào tồn nháp lâu (sắp trễ kỳ thuế).
- Lọc theo một hợp đồng hoặc một khách hàng cụ thể.

## Cách thực hiện

1. Mở **Hóa đơn cần ghi sổ** từ menu Hợp đồng & PAKD.
2. Bộ lọc:
   - **Hợp đồng**: chỉ xem hóa đơn nháp của một hợp đồng.
   - **Khách hàng**: chỉ xem hóa đơn nháp của một khách.
3. Đọc cột **"Chờ ghi sổ (ngày)"** — số ngày kể từ khi hóa đơn nháp được tạo. Ưu tiên dòng lâu nhất.
4. Bấm vào số hóa đơn để mở chứng từ gốc → kiểm tra số liệu → **Ghi sổ** (duyệt). Sau khi ghi sổ, hóa đơn rời khỏi báo cáo này và doanh thu + thuế GTGT được ghi nhận.

## Định khoản tự động

Báo cáo này **không tự định khoản** — chỉ là danh sách tra cứu/worklist. Định khoản phát sinh khi kế toán **ghi sổ hóa đơn bán hàng** (ngoài báo cáo này), với hình mẫu: Nợ TK 131 (phải thu khách) / Có TK 511 (doanh thu) + Có TK 3331 (thuế GTGT đầu ra).

## Tình huống đặc biệt & cảnh báo

- **Chỉ hiện hóa đơn nháp gắn hợp đồng:** điều kiện là hóa đơn chưa ghi sổ và có trường hợp đồng. Hóa đơn lẻ không gắn hợp đồng không hiện ở đây.
- **Ghi sổ rồi mới xuất hóa đơn VAT:** quy trình là rà → ghi sổ trong hệ thống → phát hành hóa đơn điện tử chính thức.
- **Tồn nháp lâu = rủi ro trễ kỳ thuế:** cột số ngày chờ giúp tránh bỏ sót hóa đơn cuối kỳ.

## Báo cáo liên quan

- [Hóa đơn quá hạn cần đôn thúc](hoa-don-qua-han-don-thuc.md): hóa đơn đã ghi sổ nhưng khách chưa trả.
- [Công nợ theo hợp đồng](cong-no-theo-hop-dong.md) và [Kỳ thu tiền quá hạn](ky-thu-tien-qua-han.md): theo dõi công nợ.
- [Danh sách hợp đồng](danh-sach-hop-dong.md): nguồn sinh ra lịch hóa đơn.

## FAQ

**Q: Vì sao có hóa đơn nháp mà tôi không tạo?**
**A:** Hệ thống tự sinh hóa đơn nháp từ lịch của hợp đồng khi đến kỳ thu tiền. Kế toán chỉ cần rà và ghi sổ.

**Q: Ghi sổ hóa đơn từ đâu — ngay trên báo cáo này được không?**
**A:** Bấm vào số hóa đơn để mở chứng từ gốc rồi ghi sổ tại đó. Báo cáo này dùng để tra cứu và ưu tiên, không phải nơi duyệt trực tiếp.

**Q: Báo cáo này có dữ liệu cho công ty DCNET không?**
**A:** Có — hiện đang có các hóa đơn nháp gắn hợp đồng chờ ghi sổ.
