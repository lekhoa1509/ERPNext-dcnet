---
section: Kho
title: Tổng quan Kho
summary: Phân hệ Kho quản lý nhập – xuất – tồn vật tư, hàng hóa, công cụ và các báo cáo kho theo VAS TT99/2025.
---

## Mục đích

Phân hệ **Kho** quản lý toàn bộ vòng đời số lượng và giá trị của vật tư – hàng hóa trong doanh nghiệp: nhập kho, xuất kho, điều chuyển giữa các kho, kiểm kê đối chiếu thực tế, theo dõi theo **số lô** và **số seri**, đóng/tháo **gói sản phẩm**, cùng hệ thống báo cáo nhập – xuất – tồn. Mọi nghiệp vụ kho đều ghi đồng thời **Sổ kho** (số lượng) và **Sổ Cái** (giá trị) theo phương pháp tính giá xuất kho đã thiết lập (bình quân gia quyền, nhập trước xuất trước…).

Số dư kho được phản ánh trên các tài khoản hàng tồn kho theo VAS: TK 152 (nguyên vật liệu), TK 153 (công cụ dụng cụ), TK 155 (thành phẩm), TK 156 (hàng hóa), TK 154 (chi phí sản xuất dở dang).

## Khi nào dùng

- Hằng ngày: lập **phiếu nhập xuất kho** khi nhập mua không qua hóa đơn, xuất dùng cho sản xuất, điều chuyển giữa các kho, sản xuất – đóng gói.
- Khi quản lý hàng theo lô/hạn dùng: khai báo **số lô** (hàng có hạn sử dụng) và **số seri** (thiết bị bảo hành, theo dõi từng chiếc).
- Định kỳ/cuối kỳ: lập **biên bản kiểm kê kho**, đối chiếu thực tế với sổ sách, điều chỉnh thừa/thiếu.
- Theo dõi tồn kho: xem **BC nhập xuất tồn**, **Sổ chi tiết kho**, **BC tuổi kho** và **Định mức tồn kho** để lên kế hoạch mua hàng.

## Cách thực hiện

Cấu trúc menu **Kho** gồm 11 mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Cài đặt PAKD | Cấu hình | Thiết lập phương án kinh doanh (xem cảnh báo — đặt nhầm phân hệ) |
| 2 | Nhập xuất kho | Danh sách | Phiếu nhập xuất kho (nhập/xuất/điều chuyển/sản xuất/đóng gói) |
| 3 | Lịch sử nhắc duyệt PAKD | Danh sách | Nhật ký nhắc duyệt phương án kinh doanh (xem cảnh báo — đặt nhầm phân hệ) |
| 4 | Kiểm kê kho | Danh sách | Biên bản kiểm kê, đối chiếu tồn thực tế với sổ sách |
| 5 | Số lô | Danh sách | Quản lý hàng theo lô và hạn sử dụng |
| 6 | Số seri | Danh sách | Quản lý hàng theo từng số seri (bảo hành) |
| 7 | BC nhập xuất tồn | Báo cáo | Tổng hợp tồn đầu – nhập – xuất – tồn cuối theo mặt hàng/kho |
| 8 | BC tuổi kho | Báo cáo | Phân tích tuổi hàng tồn (hàng chậm luân chuyển) |
| 9 | Sổ chi tiết kho | Báo cáo | Sổ chi tiết từng lần nhập/xuất, số dư lũy kế |
| 10 | Định mức tồn kho | Báo cáo | Gợi ý mức tồn kho tối thiểu theo lượng xuất bình quân |
| 11 | Gói sản phẩm | Danh sách | Khai báo combo/bộ sản phẩm bán theo gói |

![Menu Kho](_images/index-1.png)

### Quy trình điển hình

1. **Khai báo danh mục:** khai báo mặt hàng, kho; nếu hàng theo lô/seri thì bật theo dõi lô/seri trên mặt hàng.
2. **Nhập kho:** mua hàng có hóa đơn → nhập qua **phiếu nhập kho** (phân hệ Mua hàng); nhập điều chỉnh/khác → **phiếu nhập xuất kho** loại Nhập kho.
3. **Xuất kho:** bán hàng → **phiếu xuất kho** (phân hệ Bán hàng); xuất dùng nội bộ/sản xuất → **phiếu nhập xuất kho** loại Xuất kho.
4. **Điều chuyển:** chuyển hàng giữa hai kho qua **phiếu nhập xuất kho** loại Điều chuyển kho.
5. **Kiểm kê:** cuối kỳ lập **biên bản kiểm kê kho**, điều chỉnh chênh lệch.
6. **Tra cứu:** xem **BC nhập xuất tồn**, **Sổ chi tiết kho**, **BC tuổi kho**, **Định mức tồn kho** để chốt số và lên kế hoạch.

### Liên kết tới các bài hướng dẫn chi tiết

- **Chứng từ kho:** [Nhập xuất kho](nhap-xuat-kho.md), [Kiểm kê kho](kiem-ke-kho.md).
- **Theo dõi lô/seri:** [Số lô](so-lo.md), [Số seri](so-seri.md).
- **Gói sản phẩm:** [Gói sản phẩm](goi-san-pham.md).
- **Báo cáo:** [BC nhập xuất tồn](bc-nhap-xuat-ton.md), [BC tuổi kho](bc-tuoi-kho.md), [Sổ chi tiết kho](so-chi-tiet-kho.md), [Định mức tồn kho](dinh-muc-ton-kho.md).
- **Cấu hình PAKD (đặt nhầm phân hệ):** [Cài đặt PAKD](cai-dat-pakd.md), [Lịch sử nhắc duyệt PAKD](lich-su-nhac-duyet-pakd.md).

## Định khoản tự động

Các nghiệp vụ kho sinh bút toán tự động khi **ghi sổ** chứng từ (đối với doanh nghiệp hạch toán hàng tồn kho theo phương pháp kê khai thường xuyên):

| Nghiệp vụ | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Nhập kho vật tư/hàng hóa | 152/153/156 | 331 / 154 / 111 / 112 | Theo nguồn nhập (mua chịu / nhập từ sản xuất / mua tiền mặt) |
| Xuất kho dùng cho sản xuất | 621/627 | 152/153 | Xuất nguyên vật liệu, công cụ cho sản xuất |
| Xuất kho bán hàng | 632 | 155/156 | Giá vốn hàng bán; đi kèm phiếu xuất kho |
| Xuất kho chi phí quản lý/bán hàng | 641/642 | 152/153 | Xuất dùng cho bộ phận bán hàng/quản lý |
| Điều chuyển giữa hai kho | 152/153/156 (kho đến) | 152/153/156 (kho đi) | Cùng nhóm TK, khác kho — tổng số dư không đổi |
| Kiểm kê phát hiện thừa | 152/153/156 | 3381 | Tài sản thừa chờ xử lý |
| Kiểm kê phát hiện thiếu | 1381 | 152/153/156 | Tài sản thiếu chờ xử lý |

Tài khoản cụ thể lấy từ thiết lập của từng mặt hàng và từng kho; doanh nghiệp xem và chỉnh sửa trong **Danh mục** (mặt hàng, kho) — không cố định trong mã nguồn.

## Tình huống đặc biệt & cảnh báo

- **Hai mục PAKD đặt nhầm phân hệ:** mục **Cài đặt PAKD** và **Lịch sử nhắc duyệt PAKD** thuộc về phương án kinh doanh (phân hệ Hợp đồng & PAKD), KHÔNG liên quan tới kho. Chúng xuất hiện trong menu Kho do lỗi sắp xếp — nên chuyển sang đúng phân hệ. Xem chi tiết trong từng bài.
- **Kê khai thường xuyên vs kiểm kê định kỳ:** các bút toán ở trên áp dụng cho phương pháp kê khai thường xuyên. Doanh nghiệp dùng kiểm kê định kỳ sẽ định khoản qua TK 611 — cần thiết lập riêng.
- **Tồn kho âm:** nếu xuất quá tồn, hệ thống có thể chặn hoặc cảnh báo tùy thiết lập; tránh để tồn âm vì làm sai giá vốn.
- **Giá xuất kho:** giá trị xuất kho tính theo phương pháp đã chọn (bình quân, nhập trước xuất trước). Sửa giá nhập sau khi đã xuất có thể làm lệch giá vốn — cần ghi sổ lại theo thứ tự thời gian.
- **Hàng theo lô/seri:** khi mặt hàng bật theo dõi lô/seri, mọi phiếu nhập/xuất bắt buộc khai lô/seri tương ứng, nếu không sẽ báo lỗi khi ghi sổ.

## Báo cáo liên quan

- **BC nhập xuất tồn:** bức tranh tổng quát tồn đầu – nhập – xuất – tồn cuối.
- **Sổ chi tiết kho:** truy vết từng lần nhập/xuất của một mặt hàng.
- **BC tuổi kho:** phát hiện hàng chậm luân chuyển, ứ đọng vốn.
- **Định mức tồn kho:** cảnh báo điểm đặt hàng lại.
- **Bảng cân đối số phát sinh:** kiểm tra số dư các TK 152/153/155/156 cuối kỳ.

## FAQ

**Q: Tạo phiếu nhập/xuất kho ở đâu?**
**A:** Nhập/xuất gắn với mua bán đi qua phân hệ Mua hàng (phiếu nhập kho) và Bán hàng (phiếu xuất kho). Các nghiệp vụ kho nội bộ (xuất dùng, điều chuyển, sản xuất, đóng gói) lập tại mục **Nhập xuất kho** → "+ Thêm".

**Q: Vì sao trong menu Kho lại có Cài đặt PAKD và Lịch sử nhắc duyệt PAKD?**
**A:** Đây là lỗi sắp xếp menu. Hai mục này thuộc phương án kinh doanh (PAKD), không phải kho. Chức năng vẫn dùng được nhưng nên được chuyển về đúng phân hệ.

**Q: Kho có tự động ghi sổ giá vốn không?**
**A:** Có. Với phương pháp kê khai thường xuyên, mỗi phiếu nhập/xuất khi ghi sổ đều ghi đồng thời Sổ kho (số lượng) và Sổ Cái (giá trị) — không phải định khoản thủ công cho giá vốn.

**Q: Báo cáo kho có giữ menu ở phân hệ Kho khi mở chứng từ gốc không?**
**A:** Có. Bấm vào dòng trên báo cáo để mở chứng từ; hệ thống giữ menu ở phân hệ hiện hành.
