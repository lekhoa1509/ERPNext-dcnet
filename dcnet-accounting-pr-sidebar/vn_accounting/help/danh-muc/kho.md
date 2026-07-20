---
title: Kho
order: 5
summary: Danh mục kho vật lý gắn với tài khoản hàng tồn kho (152/153/155/156) để ghi đúng giá trị nhập – xuất – tồn.
---

## Mục đích

Danh mục **Kho** khai báo các kho vật lý nơi doanh nghiệp lưu giữ vật tư, hàng hóa, thành phẩm. Mỗi kho có thể gắn một **tài khoản hàng tồn kho** — khi nhập/xuất tại kho, hệ thống ghi giá trị vào đúng tài khoản đó trên Sổ Cái (đồng thời ghi số lượng vào Sổ kho).

Thông tin chính của một kho:

- **Tên kho**: định danh dùng trên phiếu nhập/xuất, hóa đơn.
- **Là kho tổng?** (`Là nhóm`): kho nhóm/cha chỉ để gom; chỉ kho chi tiết (lá) mới nhận nhập/xuất.
- **Tài khoản kho** (`Account`): tài khoản hàng tồn kho gắn với kho (TK 152 nguyên vật liệu, 153 công cụ, 155 thành phẩm, 156 hàng hóa). Nếu để trống, hệ thống dùng tài khoản kho của kho cha hoặc tài khoản tồn kho mặc định của công ty.
- **Công ty**: kho thuộc công ty nào.

> Lưu ý: tài khoản gắn vào kho phải có **loại tài khoản là Kho (Stock)** trong hệ thống tài khoản. Xem [Hệ thống tài khoản](he-thong-tai-khoan.md).

## Khi nào dùng

- **Khi mở kho mới:** thêm kho cho chi nhánh, kho thành phẩm, kho phế liệu, kho hàng gửi bán…
- **Khi cần tách giá trị tồn theo loại:** gán tài khoản 152/153/155/156 khác nhau cho các kho chứa loại hàng khác nhau.
- **Khi lập phiếu nhập/xuất kho, hóa đơn:** chọn kho từ danh mục; tài khoản kho tự áp.
- **Khi báo cáo nhập – xuất – tồn:** lọc theo kho.

## Cách thực hiện

1. Mở **Kho** trên menu Danh mục → danh sách kho hiện ra (dạng cây nếu có kho nhóm).
2. Bấm **+ Thêm** → nhập **Tên kho**, chọn **Công ty**.
3. Để trống `Là nhóm` nếu là kho chi tiết (kho thực tế nhập/xuất).
4. Chọn **Tài khoản kho** (TK 152/153/155/156) tương ứng loại hàng kho chứa. Bảo đảm tài khoản này có loại tài khoản là Kho (Stock).
5. Lưu lại → kho sẵn sàng để chọn trên chứng từ.

## Định khoản tự động

Danh mục kho **không tự sinh bút toán** khi khai báo. Nhưng tài khoản kho quyết định định khoản phía kho trên các phiếu nhập/xuất:

| Trường hợp (chứng từ) | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Nhập kho hàng hóa | 156 (theo kho) | 331 / 111 / 112 | TK kho lấy từ tài khoản kho đã gán |
| Xuất kho bán hàng (giá vốn) | 632 | 156/155 (theo kho) | Giá trị xuất theo phương pháp tính giá |
| Xuất nguyên vật liệu cho sản xuất | 154 / 627 | 152 (theo kho) | |
| Điều chuyển giữa hai kho | 152/156 (kho đến) | 152/156 (kho đi) | Hai kho có thể khác tài khoản |

## Tình huống đặc biệt & cảnh báo

- **Tài khoản kho chưa đặt loại Stock:** nếu gán một tài khoản không phải loại Kho, các phiếu nhập/xuất có thể báo lỗi hoặc ghi sai. Đặt loại tài khoản là Stock trong hệ thống tài khoản trước.
- **Kho để trống tài khoản:** hệ thống sẽ dùng tài khoản kho của kho cha hoặc tài khoản tồn kho mặc định của công ty — kiểm tra để giá trị tồn rơi đúng tài khoản mong muốn.
- **Không nhập/xuất vào kho tổng:** chỉ kho chi tiết (lá) mới nhận giao dịch; kho nhóm chỉ để gom số liệu.
- **Đa công ty:** mỗi kho thuộc một công ty; tài khoản kho cũng thuộc hệ thống tài khoản của công ty đó.
- **Không xóa kho đã có tồn / giao dịch:** kho đã phát sinh nhập/xuất hoặc còn tồn không xóa được; nếu ngừng dùng thì khóa.

## Báo cáo liên quan

- **Báo cáo nhập – xuất – tồn**: số lượng + giá trị theo kho.
- **Sổ chi tiết kho**: phát sinh nhập/xuất của mặt hàng tại một kho.
- **Biên bản kiểm kê kho**: đối chiếu tồn thực tế với sổ sách theo kho.
- **Bảng cân đối số phát sinh**: kiểm tra số dư các tài khoản kho 152/153/155/156.

## FAQ

**Q: Khai báo kho mới có ảnh hưởng số dư kế toán không?**
**A:** Không. Khai kho chỉ tạo dữ liệu nền. Số dư tồn kho chỉ phát sinh khi nhập hàng vào kho qua phiếu nhập kho / hóa đơn mua.

**Q: Tại sao phải gán tài khoản cho kho?**
**A:** Để giá trị nhập/xuất tại kho ghi vào đúng tài khoản hàng tồn kho (ví dụ kho nguyên vật liệu → 152, kho hàng hóa → 156). Nếu nhiều loại hàng tách kho, gán tài khoản khác nhau giúp báo cáo số dư đúng theo từng loại.

**Q: Một công ty nhiều chi nhánh thì khai kho thế nào?**
**A:** Mở mỗi chi nhánh một (hoặc nhiều) kho chi tiết, có thể gom dưới một kho nhóm theo chi nhánh để tổng hợp báo cáo.

**Q: Tôi để trống tài khoản kho thì giá trị tồn ghi vào đâu?**
**A:** Hệ thống dùng tài khoản kho của kho cha, nếu không có thì dùng tài khoản tồn kho mặc định của công ty. Nên gán rõ để tránh nhầm tài khoản.
