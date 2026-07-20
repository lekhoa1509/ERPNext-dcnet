---
title: Định mức vật tư (BOM)
order: 7
summary: Định mức nguyên vật liệu cho một đơn vị thành phẩm — cơ sở tính giá thành và xuất kho sản xuất.
---

## Mục đích

**Định mức vật tư** (BOM — Bill of Materials) khai báo công thức sản xuất: để làm ra **một đơn vị thành phẩm** cần những nguyên vật liệu / bán thành phẩm nào và với số lượng bao nhiêu. Đây là dữ liệu nền cho doanh nghiệp **sản xuất**, làm cơ sở để:

- Tính **giá thành** sản phẩm (chi phí nguyên vật liệu định mức).
- Xuất kho nguyên vật liệu theo định mức khi sản xuất.
- Lập kế hoạch mua hàng theo nhu cầu sản xuất.

Thông tin chính của một định mức:

- **Thành phẩm** (`item`): mặt hàng được sản xuất ra.
- **Số lượng sản xuất** (`quantity`) và **đơn vị tính**: định mức tính cho bao nhiêu đơn vị thành phẩm.
- **Danh sách nguyên vật liệu** (`items`): từng vật tư thành phần + số lượng định mức + tỷ lệ hao hụt (nếu có).
- **Có công đoạn?** (`with_operations`): bật nếu tính thêm chi phí nhân công / máy theo công đoạn (Routing).
- **Cách lấy đơn giá vật tư** (`rm_cost_as_per`): theo Giá vốn (Valuation Rate), Giá mua gần nhất (Last Purchase Rate), hoặc Bảng giá (Price List).
- **Đang áp dụng / Mặc định** (`is_active`, `is_default`): định mức có hiệu lực và là định mức mặc định khi một thành phẩm có nhiều phiên bản định mức.

## Khi nào dùng

- **Doanh nghiệp sản xuất:** khai định mức cho từng thành phẩm trước khi chạy lệnh sản xuất / tính giá thành.
- **Khi đổi công thức:** sản phẩm thay đổi nguyên liệu / tỷ lệ → tạo phiên bản định mức mới và đặt làm mặc định.
- **Khi tính giá thành:** định mức cung cấp chi phí nguyên vật liệu chuẩn cho một đơn vị thành phẩm.
- **Khi lập kế hoạch mua hàng:** từ nhu cầu sản xuất và định mức, hệ thống tính lượng vật tư cần mua.

## Cách thực hiện

1. Mở **Định mức vật tư** trên menu Danh mục → danh sách định mức hiện ra.
2. Bấm **+ Thêm** → chọn **Thành phẩm**, nhập **Số lượng sản xuất** (thường 1) và **đơn vị tính**.
3. Tại bảng **Nguyên vật liệu**, thêm từng dòng: chọn vật tư thành phần, nhập **số lượng định mức** cho lượng thành phẩm đã khai.
4. Chọn **Cách lấy đơn giá vật tư** (thường theo Giá vốn) → hệ thống tính chi phí nguyên vật liệu định mức.
5. (Tùy chọn) bật **Có công đoạn** và khai Routing nếu cần cộng chi phí nhân công / máy.
6. Đặt **Đang áp dụng** = có; nếu thành phẩm có nhiều định mức, đặt một định mức **Mặc định**.
7. Lưu và duyệt (`Đã duyệt`) để định mức có hiệu lực dùng trong sản xuất / giá thành.

## Định khoản tự động

Bản thân định mức vật tư **không tự sinh bút toán** — nó chỉ là công thức. Bút toán phát sinh khi **dùng định mức** để sản xuất:

| Trường hợp (chứng từ dựa trên định mức) | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Xuất nguyên vật liệu cho sản xuất | 154 | 152 | Số lượng xuất theo định mức × số lượng sản xuất |
| Tập hợp chi phí nhân công / sản xuất chung | 154 | 622 / 627 | Nếu định mức có công đoạn |
| Nhập kho thành phẩm hoàn thành | 155 | 154 | Giá thành = chi phí tập hợp trong 154 |

Định mức chỉ quyết định **lượng vật tư và chi phí định mức** — giá trị thực tế lấy theo phương pháp tính giá kho và chi phí thực tế tập hợp.

## Tình huống đặc biệt & cảnh báo

- **Định mức chưa duyệt không dùng được:** chỉ định mức `Đang áp dụng` (và đã duyệt) mới được tham chiếu trong sản xuất / tính giá thành.
- **Nhiều phiên bản định mức:** một thành phẩm có thể có nhiều định mức (đổi công thức theo thời kỳ); đặt đúng định mức **Mặc định** để hệ thống chọn tự động.
- **Tỷ lệ hao hụt:** khai hao hụt trong dòng vật tư để định mức phản ánh đúng lượng tiêu hao thực tế (mép cắt, hao dầu…).
- **Bán thành phẩm lồng nhau:** một thành phẩm có thể dùng bán thành phẩm (cũng có định mức riêng) làm nguyên liệu — khai định mức nhiều cấp.
- **Đơn giá vật tư biến động:** chi phí định mức phụ thuộc cách lấy đơn giá (giá vốn / giá mua gần nhất / bảng giá); chọn cách phù hợp để giá thành sát thực tế.

## Báo cáo liên quan

- **Báo cáo giá thành sản xuất**: tổng hợp chi phí và giá thành theo định mức.
- **Báo cáo nhập – xuất – tồn**: theo dõi vật tư tiêu hao và thành phẩm nhập kho.
- **Hàng hóa, vật tư**: định mức tham chiếu các mặt hàng thành phần và thành phẩm. Xem [Hàng hóa, vật tư](hang-hoa-vat-tu.md).

## FAQ

**Q: Khai định mức có làm xuất kho nguyên vật liệu không?**
**A:** Không. Định mức chỉ là công thức. Xuất kho và bút toán chỉ phát sinh khi chạy lệnh sản xuất / lập phiếu xuất kho dựa trên định mức.

**Q: Một sản phẩm đổi công thức giữa năm thì làm sao?**
**A:** Tạo một định mức mới với công thức mới, đặt làm Mặc định và để định mức cũ ở trạng thái không áp dụng. Các lệnh sản xuất cũ giữ định mức cũ; lệnh mới dùng định mức mới.

**Q: Định mức tính cho 1 sản phẩm hay cho cả lô?**
**A:** Tùy bạn khai số lượng sản xuất. Thường khai cho 1 đơn vị thành phẩm để dễ nhân lên theo sản lượng; khai theo lô cũng được nếu vật tư khó chia nhỏ.

**Q: Doanh nghiệp thương mại (không sản xuất) có cần định mức không?**
**A:** Không. Định mức vật tư chỉ dành cho doanh nghiệp có hoạt động sản xuất / gia công cần tính giá thành.
