---
title: Đơn mua hàng
order: 1
summary: Lập và theo dõi đơn đặt mua gửi nhà cung cấp — cam kết mua, chưa ghi sổ kế toán.
---

## Mục đích

**Đơn mua hàng** là chứng từ ghi nhận cam kết đặt mua hàng hóa/dịch vụ với nhà cung cấp: mã hàng, số lượng, đơn giá, ngày cần nhận, điều khoản thanh toán. Đây là bước khởi đầu chu trình mua, dùng để theo dõi tiến độ nhận hàng và lập hóa đơn. Đơn mua hàng **không sinh bút toán** — chỉ phục vụ quản lý cam kết và kiểm soát mua.

Menu Mua hàng có hai mục cùng trỏ về đơn mua hàng:

- **Đơn mua hàng**: toàn bộ đơn mua, mọi trạng thái.
- **Đơn mua hàng cần lập hóa đơn**: lọc sẵn các đơn ở trạng thái "Cần lập hóa đơn" / "Cần nhận và lập hóa đơn" (đã nhận hàng nhưng chưa ghi nhận hóa đơn mua hàng) — giúp kế toán theo dõi việc hoàn thiện chứng từ.

## Khi nào dùng

- Khi phòng mua hàng đặt mua hàng/dịch vụ và cần theo dõi đến lúc hàng về + có hóa đơn.
- Khi cần kiểm soát giá mua, số lượng cam kết trước khi nhận hàng.
- Định kỳ: rà soát "Đơn mua hàng cần lập hóa đơn" để đảm bảo mọi đơn đã nhận hàng đều được ghi nhận hóa đơn.

## Cách thực hiện

1. Bấm **Đơn mua hàng** trên menu Mua hàng → danh sách đơn mua hàng.
2. Bấm **+ Thêm** → chọn **Nhà cung cấp**, nhập **Ngày đặt**, thêm dòng hàng (mã hàng, số lượng, đơn giá), chọn **Kho nhận** và **Ngày cần nhận**.
3. (Tùy chọn) chọn **Phòng ban đề xuất** để ghi nhận bộ phận đề nghị mua.
4. **Lưu** → **Ghi sổ/Duyệt** để chuyển đơn sang trạng thái chờ nhận hàng.
5. Khi hàng về: bấm **Tạo > Phiếu nhập kho** để kế thừa dòng hàng. Khi nhận hóa đơn: bấm **Tạo > Hóa đơn mua hàng**.
6. Để theo dõi đơn còn thiếu hóa đơn: mở mục **Đơn mua hàng cần lập hóa đơn**.

## Định khoản tự động

Đơn mua hàng **không tự định khoản** — đây là chứng từ cam kết, không ghi vào Sổ Cái. Bút toán chỉ phát sinh ở bước sau:

- Lập **phiếu nhập kho** → ghi tăng kho (Dr 152/153/156 / Cr 151 hoặc 3388).
- Lập **hóa đơn mua hàng** → ghi công nợ phải trả (Cr 331) và thuế GTGT đầu vào (Dr 1331).

## Tình huống đặc biệt & cảnh báo

- **Đơn mua không khóa giá thực mua:** đơn giá trên đơn mua hàng là dự kiến; giá ghi sổ là giá trên hóa đơn mua hàng. Nếu lệch, kiểm tra điều khoản với NCC.
- **Đơn mua nhiều đợt giao:** một đơn mua có thể tạo nhiều phiếu nhập kho và nhiều hóa đơn mua hàng theo từng đợt. Hệ thống theo dõi phần đã nhận / đã lập hóa đơn theo tỷ lệ.
- **Hủy đơn mua hàng đã có nhập kho/hóa đơn:** phải hủy các chứng từ con (phiếu nhập kho, hóa đơn mua hàng) trước, sau đó mới hủy đơn mua hàng.
- **Phòng ban đề xuất** tự kế thừa xuống hóa đơn mua hàng khi tất cả dòng hàng cùng thuộc một đơn mua (FB-2026-00616).

## Báo cáo liên quan

- [Đơn mua hàng cần lập hóa đơn](index.md) — chính là danh sách này lọc theo trạng thái "cần lập hóa đơn".
- [Hóa đơn mua hàng](hoa-don-mua-hang.md) — bước ghi nhận công nợ và thuế.
- [Nhập kho mua hàng](nhap-kho-mua-hang.md) — bước ghi tăng kho.
- [BC mua hàng](bc-mua-hang.md) — phân tích đơn mua theo NCC/mặt hàng.

## FAQ

**Q: Đơn mua hàng đã duyệt có ghi vào Sổ Cái không?**
**A:** Không. Đơn mua hàng là cam kết mua, không phát sinh nợ phải trả. Công nợ chỉ ghi nhận khi lập hóa đơn mua hàng.

**Q: "Đơn mua hàng cần lập hóa đơn" lấy dữ liệu từ đâu?**
**A:** Cùng bảng đơn mua hàng, lọc theo trạng thái "Cần lập hóa đơn" / "Cần nhận và lập hóa đơn". Đơn nào đã nhận hàng nhưng chưa ghi nhận hóa đơn sẽ hiện ở đây để nhắc kế toán hoàn thiện chứng từ.

**Q: Tạo hóa đơn mua hàng từ đơn mua hàng có lợi gì so với tạo trực tiếp?**
**A:** Kế thừa sẵn dòng hàng, số lượng, đơn giá và phòng ban đề xuất; giảm sai sót nhập tay và tự khớp đơn mua ↔ hóa đơn để báo cáo đúng.
