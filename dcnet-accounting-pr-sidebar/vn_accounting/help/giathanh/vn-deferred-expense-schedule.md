---
title: Lịch phân bổ chi phí trả trước (TK 242)
order: 4
summary: Lập lịch phân bổ chi phí chờ phân bổ (TK 242) ra nhiều kỳ và tự sinh bút toán Dr chi phí / Cr 242 từng kỳ.
---

## Mục đích

Một số chi phí trả trước phục vụ nhiều kỳ — tiền thuê nhà trả trước nhiều tháng, công cụ dụng cụ phân bổ dần, bảo hiểm trả trước, chi phí sửa chữa lớn... Theo VAS TT99/2025, các khoản này hạch toán vào **TK 242 — Chi phí chờ phân bổ** (TT99 đổi tên từ "Chi phí trả trước" và bỏ TK 142), sau đó phân bổ dần vào chi phí từng kỳ.

**Lịch phân bổ chi phí trả trước** giúp:
- Khai báo tổng số tiền chờ phân bổ và khoảng thời gian phân bổ.
- Tự chia thành các kỳ (theo tháng / quý / ngày / một lần).
- Mỗi kỳ tự sinh bút toán **Dr chi phí (6xx) / Cr 242** và đánh dấu kỳ đã phân bổ.

Dùng cho kế toán tổng hợp.

## Khi nào dùng

- Thuê văn phòng / nhà xưởng trả trước cho nhiều tháng.
- Bảo hiểm tài sản, bảo hiểm hàng hóa trả trước theo năm.
- Chi phí công cụ dụng cụ, sửa chữa lớn cần phân bổ dần.
- Bất kỳ chi phí trả trước nào đã ghi Nợ TK 242 và cần phân bổ tự động qua nhiều kỳ.

## Cách thực hiện

**Cách 1 — Tạo trực tiếp:**
1. Vào **Giá thành → Lịch phân bổ CP trả trước (242)** → **+ Thêm**.
2. Chọn **Công ty**, **Ngày bắt đầu**, **Ngày kết thúc**, nhập **Tổng số tiền chờ phân bổ**.
3. Chọn **TK chi phí chờ phân bổ** (mặc định 242) và **TK chi phí sẽ ghi nhận** (TK 6xx tương ứng: 6427 chi phí dịch vụ mua ngoài, 6423 đồ dùng văn phòng, 627/641/642 tùy bản chất).
4. Chọn **Phương pháp phân bổ**: Theo tháng / Theo quý / Theo ngày / Một lần.
5. Bấm **Sinh lịch tự động** → hệ thống chia tổng số tiền thành các dòng kỳ (kỳ cuối nhận phần dư để tổng khớp tuyệt đối).
6. Bấm **Ghi sổ** → lịch chuyển sang trạng thái **Hoạt động**.
7. Mỗi kỳ đến hạn: mở lịch → bấm phân bổ kỳ đó (hoặc dùng "Phân bổ tất cả kỳ đến hạn") → hệ thống sinh và ghi sổ bút toán cho kỳ.

**Cách 2 — Tạo từ hóa đơn mua hàng:** trên hóa đơn mua hàng đã ghi sổ, dùng nút tạo lịch phân bổ → hệ thống tự gắn nhà cung cấp + hóa đơn nguồn, sinh lịch và ghi sổ ngay.

## Định khoản tự động

| Bước | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Ghi nhận chi phí trả trước ban đầu (làm thủ công hoặc từ hóa đơn mua) | **242** | 331 / 111 / 112 | Đây là bước nhập liệu trước, không do lịch sinh |
| Phân bổ từng kỳ (lịch tự sinh) | **TK chi phí 6xx** (vd 6427/627/641/642) | **242** | Mỗi kỳ một bút toán, số tiền = phần phân bổ của kỳ |

> Bút toán phân bổ kỳ giữ tham chiếu tới nhà cung cấp + hóa đơn nguồn (nếu lịch tạo từ hóa đơn mua hàng) để truy vết. Hủy lịch → các bút toán đã sinh tự hủy.

## Tình huống đặc biệt & cảnh báo

- **Phải bấm "Sinh lịch tự động" trước khi ghi sổ** — không có dòng kỳ thì hệ thống chặn ghi sổ.
- **Tổng các kỳ phải khớp tổng số tiền** (sai lệch > 1 đồng sẽ bị chặn) — hệ thống tự dồn phần dư vào kỳ cuối nên thường luôn khớp.
- **Chỉ sinh lịch khi đang ở trạng thái Nháp** — đã ghi sổ thì không sinh lại; muốn đổi phải hủy.
- **TK chi phí chờ phân bổ và TK chi phí ghi nhận phải là TK chi tiết, cùng công ty** — không dùng TK tổng (TK cha).
- Khi phân bổ hết, lịch tự chuyển trạng thái **Hoàn thành**.
- Phân hệ này khác với **công cụ dụng cụ (CCDC)** nếu đơn vị dùng module CCDC riêng — lịch 242 phù hợp cho chi phí trả trước nói chung.

## Báo cáo liên quan

- [Sổ Cái] TK 242: theo dõi số dư chi phí chờ phân bổ còn lại.
- [Dự án — Giá thành](project-costing-tinh-gia-thanh.md): nếu chi phí trả trước cần phân bổ vào công trình.

## FAQ

**Q: TT99/2025 còn TK 142 không?**
**A:** Không. TT99/2025 bỏ TK 142, gộp toàn bộ chi phí trả trước vào TK 242 (đổi tên thành "Chi phí chờ phân bổ"). Lịch này mặc định dùng TK 242.

**Q: Nếu phân bổ thiếu một kỳ thì sao?**
**A:** Dùng "Phân bổ tất cả kỳ đến hạn" — hệ thống quét mọi kỳ chưa phân bổ có ngày kết thúc ≤ ngày hiện tại và sinh bút toán cho từng kỳ.

**Q: Đã phân bổ một kỳ rồi có phân bổ lại được không?**
**A:** Không. Kỳ đã phân bổ bị khóa. Nếu sai, hủy bút toán kỳ đó rồi xử lý lại.
