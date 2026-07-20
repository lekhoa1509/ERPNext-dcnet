---
title: Hàng hóa, vật tư
order: 4
summary: Danh mục mặt hàng — mã hàng, nhóm, đơn vị tính, kho mặc định, và tài khoản doanh thu/giá vốn qua Giá trị mặc định.
---

## Mục đích

Danh mục **Hàng hóa, vật tư** khai báo mọi mặt hàng doanh nghiệp mua bán, lưu kho hoặc dùng cho sản xuất: hàng hóa (TK 156), nguyên vật liệu (TK 152), công cụ dụng cụ (TK 153), thành phẩm (TK 155), và cả dịch vụ (không quản kho). Mỗi mặt hàng là cơ sở để chứng từ bán hàng / mua hàng / nhập xuất kho tham chiếu.

Thông tin chính của một mặt hàng:

- **Mã hàng / Tên hàng**: định danh dùng trên mọi chứng từ.
- **Nhóm hàng** (Item Group): phân loại phục vụ báo cáo và gán tài khoản theo nhóm.
- **Đơn vị tính** (ĐVT gốc): đơn vị lưu kho chuẩn (cái, kg, m, bộ…).
- **Quản lý tồn kho?** (`Là mặt hàng tồn kho`): bật cho hàng hóa/vật tư có nhập xuất tồn; tắt cho dịch vụ.
- **Là tài sản cố định?**: bật nếu mặt hàng là TSCĐ (liên quan TK 211).
- **Là hàng bán / Là hàng mua**: đánh dấu mặt hàng dùng để bán, để mua.
- **Giá trị mặc định** (`item_defaults`, theo từng công ty): khai **kho mặc định**, **tài khoản doanh thu** (TK 511), **tài khoản giá vốn / chi phí** (TK 632 hoặc 6xx), cùng trung tâm chi phí.

## Khi nào dùng

- **Khi có mặt hàng mới:** nhập về hàng / vật tư mới, hoặc thêm dịch vụ mới để xuất hóa đơn.
- **Khi cần định khoản đúng theo mặt hàng:** gán tài khoản doanh thu / giá vốn mặc định để hóa đơn tự điền đúng tài khoản.
- **Khi quản lý theo lô/seri:** bật theo dõi số lô (hàng có hạn dùng) hoặc số seri (thiết bị) — khai ở thẻ mặt hàng.
- **Khi lập chứng từ bán/mua/kho:** chọn mặt hàng từ danh mục; ĐVT, kho, tài khoản tự điền.

## Cách thực hiện

1. Mở **Hàng hóa, vật tư** trên menu Danh mục → danh sách hiện ra.
2. Bấm **+ Thêm** → nhập **Tên hàng**, chọn **Nhóm hàng**, **Đơn vị tính**.
3. Bật/tắt **Là mặt hàng tồn kho** (tắt cho dịch vụ), **Là hàng bán**, **Là hàng mua** tùy bản chất.
4. Mở mục **Giá trị mặc định** → thêm dòng theo **công ty** và khai:
   - **Kho mặc định** (kho thường nhập/xuất mặt hàng này).
   - **Tài khoản doanh thu** (thường TK 511).
   - **Tài khoản chi phí / giá vốn** (thường TK 632 cho hàng hóa, hoặc 6xx cho dịch vụ).
5. (Tùy chọn) bật theo dõi **số lô** / **số seri** nếu cần.
6. Lưu lại.

## Định khoản tự động

Danh mục mặt hàng **không tự sinh bút toán**, nhưng **Giá trị mặc định** quyết định tài khoản trên chứng từ:

| Trường hợp (chứng từ) | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Bán hàng (hóa đơn bán) | 131 | 511 (theo mặt hàng) + 3331 | TK 511 lấy từ Giá trị mặc định |
| Ghi giá vốn khi xuất bán | 632 (theo mặt hàng) | 156/155 | TK 632 lấy từ Giá trị mặc định |
| Mua hàng nhập kho | 152/153/156 + 1331 | 331 | Kho mặc định gắn TK kho tương ứng |
| Xuất kho dùng sản xuất | 154/627 | 152/153 | Theo nghiệp vụ kho |

Tài khoản mặc định chỉ điền sẵn — kế toán vẫn chỉnh được trên chứng từ.

## Tình huống đặc biệt & cảnh báo

- **Thiếu Giá trị mặc định:** nếu không khai TK doanh thu / giá vốn, chứng từ rơi về tài khoản mặc định của công ty — dễ sai phân loại doanh thu/giá vốn. Nên khai đầy đủ theo nhóm hàng.
- **Đổi `Là mặt hàng tồn kho` sau khi đã phát sinh:** không nên đổi khi mặt hàng đã có nhập/xuất kho — ảnh hưởng cách ghi giá vốn và tồn kho.
- **Dịch vụ:** tắt `Là mặt hàng tồn kho`; chỉ cần TK doanh thu và TK chi phí, không cần kho.
- **Tài sản cố định:** bật `Là tài sản cố định` và gán nhóm tài sản phù hợp; mặt hàng này phục vụ ghi tăng TSCĐ (TK 211), không quản như hàng tồn kho.
- **Đa công ty:** Giá trị mặc định (kho, TK doanh thu, TK giá vốn) khai theo **từng công ty** — kiểm tra đúng công ty.

## Báo cáo liên quan

- **Báo cáo nhập – xuất – tồn**: số lượng và giá trị theo mặt hàng và kho.
- **Sổ chi tiết kho**: phát sinh nhập/xuất của một mặt hàng tại một kho.
- **Báo cáo tuổi kho**: phân tích tồn theo độ tuổi để xử lý hàng chậm luân chuyển.
- **Định mức vật tư (BOM)**: dùng mặt hàng làm thành phần định mức cho sản xuất.

## FAQ

**Q: Khai báo mặt hàng mới có tạo tồn kho/bút toán không?**
**A:** Không. Tồn kho và bút toán chỉ phát sinh khi lập phiếu nhập/xuất hoặc hóa đơn. Khai mặt hàng chỉ tạo dữ liệu nền.

**Q: Tôi để trống tài khoản doanh thu của mặt hàng thì sao?**
**A:** Hóa đơn bán sẽ dùng tài khoản doanh thu mặc định của công ty. Để phân loại doanh thu chính xác theo mặt hàng/nhóm, nên khai TK 511 ở Giá trị mặc định.

**Q: Một mặt hàng dùng ở nhiều kho — khai kho mặc định nào?**
**A:** Khai kho hay dùng nhất làm mặc định để điền sẵn; khi lập chứng từ vẫn chọn kho khác được.

**Q: Hàng theo dõi theo lô/seri khai ở đâu?**
**A:** Bật tùy chọn theo dõi số lô (hàng có hạn dùng) hoặc số seri (theo dõi từng chiếc) ngay trên thẻ mặt hàng; sau đó các phiếu nhập/xuất sẽ yêu cầu nhập lô/seri tương ứng.
