---
title: Cài đặt PAKD
order: 1
summary: Thiết lập cấu hình phương án kinh doanh (PAKD) — lưu ý đây là mục đặt nhầm trong phân hệ Kho.
---

## Mục đích

**Cài đặt PAKD** là màn hình thiết lập cấu hình cho **phương án kinh doanh (PAKD)** — gồm ngày chốt hàng tháng, mẫu hoa hồng mặc định, các tài khoản kế toán dùng khi đăng hoa hồng cho nhân viên kinh doanh và người giới thiệu ngoài, ngưỡng biên lãi để tô màu thẻ tóm tắt, và cấu hình nhắc duyệt. Đây **không phải** chức năng kho.

> Lưu ý sắp xếp: mục này hiện nằm trong menu **Kho** do lỗi gom nhóm. Về nghiệp vụ, nó thuộc phân hệ **Hợp đồng & PAKD**. Nội dung dưới đây mô tả ngắn để người dùng không nhầm lẫn; nên xem hướng dẫn đầy đủ trong phân hệ PAKD.

## Khi nào dùng

- Khi thiết lập ban đầu cho phân hệ phương án kinh doanh.
- Khi đổi tài khoản kế toán dùng cho hoa hồng nhân viên kinh doanh / hoa hồng người giới thiệu ngoài.
- Khi điều chỉnh ngày chốt tháng, ngưỡng biên lãi, hoặc cấu hình nhắc duyệt.

## Cách thực hiện

1. Mở mục **Cài đặt PAKD** (hiện đang nằm trong menu Kho).
2. Thiết lập các nhóm cấu hình:
   - **Cài đặt chung:** ngày chốt hàng tháng, mẫu hoa hồng mặc định, có dùng phân hệ lương để chi hoa hồng hay không.
   - **Tài khoản kế toán:** các TK chi phí và TK đối ứng cho dịch vụ quản lý, chi phí ngoài, phí GPVT, hoa hồng nhân viên kinh doanh.
   - **Hoa hồng ngoài:** TK chi phí và TK phải trả cho người giới thiệu ngoài, TK thuế TNCN tạm giữ, tỷ lệ TNCN mặc định.
   - **Thẻ tóm tắt & duyệt:** ngưỡng biên lãi (xanh/vàng), tự đăng hoa hồng khi duyệt, khoảng cách tối thiểu giữa hai lần nhắc, mẫu email nhắc duyệt.
3. Lưu.

## Định khoản tự động

**Không tự định khoản** — đây là màn hình cấu hình. Tuy nhiên các tài khoản khai ở đây sẽ được dùng khi phân hệ PAKD đăng bút toán hoa hồng (ví dụ: Nợ 642x chi phí hoa hồng / Có 334 phải trả nhân viên, hoặc TK phải trả người ngoài, kèm TK thuế TNCN tạm giữ). Việc định khoản thực tế xảy ra ở phân hệ PAKD, không phải tại đây.

## Tình huống đặc biệt & cảnh báo

- **Đặt nhầm phân hệ:** mục này thuộc phương án kinh doanh, không liên quan tới kho. Nên chuyển về phân hệ Hợp đồng & PAKD để tránh gây nhầm cho người dùng kho.
- **Thiết lập một lần:** đây là cấu hình dùng chung, chỉ chỉnh khi chính sách thay đổi.
- **Tài khoản phải đúng VAS:** chọn TK chi phí (642x) và TK phải trả (334/338) phù hợp; thuế TNCN tạm giữ vào TK 3335.

## Báo cáo liên quan

- Các chức năng phương án kinh doanh trong phân hệ **Hợp đồng & PAKD**.
- [Lịch sử nhắc duyệt PAKD](lich-su-nhac-duyet-pakd.md): nhật ký nhắc duyệt liên quan tới cấu hình nhắc ở đây.

## FAQ

**Q: Cài đặt PAKD có liên quan gì tới kho không?**
**A:** Không. Đây là cấu hình phương án kinh doanh, bị đặt nhầm vào menu Kho. Chức năng vẫn dùng được, nhưng nên xem nó như một mục của phân hệ Hợp đồng & PAKD.

**Q: Tôi làm kho, có cần đụng tới mục này không?**
**A:** Không cần. Người phụ trách kho có thể bỏ qua; mục này dành cho người thiết lập phương án kinh doanh và kế toán hoa hồng.
