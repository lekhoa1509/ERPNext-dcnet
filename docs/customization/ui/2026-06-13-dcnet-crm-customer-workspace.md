# DCNET CRM Customer Workspace

## Overview

Tạo màn hình danh sách Khách hàng riêng trong `dcnet_crm`, sử dụng dữ liệu và
permission chuẩn của ERPNext.

Nguồn yêu cầu: `docs/feature/FEATURE_SPECIFICATION.md` Sections 4.1, 4.2 và
4.4.

## Requirements

- Danh sách khách hàng có tìm kiếm, phân trang và import Excel.
- Cho phép chọn tiêu chí lọc theo các trường Customer hiện có.
- Nút Hoạt động và Bộ lọc ẩn/hiện độc lập panel tương ứng; bảng tự mở rộng
  theo phần diện tích còn lại.
- Panel Hoạt động dùng cùng dữ liệu `ToDo` và `Event` với tab Hoạt động trong
  hồ sơ khách hàng.
- Panel Mua hàng hiển thị chung Báo giá, Đơn hàng và Hóa đơn của khách hàng,
  sắp theo ngày mới nhất.
- Panel Liên hệ hiển thị Contact được liên kết với Customer qua `Dynamic Link`.
- Không hiển thị thêm thẻ tóm tắt khách hàng trong panel lịch sử.
- Menu giao diện ở tiêu đề không hiển thị hai giao diện dự báo AI từ hệ thống
  tham khảo.
- `Khách hàng của tôi` lọc theo `Customer.account_manager` bằng user hiện tại.
- Giao diện Đối tác/CTV và nhóm tôi chỉ hiển thị ở trạng thái chưa cấu hình,
  không tự suy đoán Customer Group hoặc mô hình nhóm nhân viên.
- Nút bánh răng mở panel Tùy chỉnh cột có tìm kiếm, danh sách trường, danh
  sách đã chọn, Xóa tất cả, Mặc định, Hủy và Lưu.
- Thay đổi cột chỉ áp dụng khi bấm Lưu và được lưu trên trình duyệt.
- Hiển thị chi tiết theo ba tab: Hoạt động, Mua hàng và Liên hệ.
- Panel ba tab dùng đúng hai hàng layout (thanh tab và vùng nội dung), không
  giữ hàng tiêu đề cũ làm co hoặc cắt ô nhập bình luận.
- Cho phép thêm bình luận, mở hồ sơ, tạo công việc và tạo đơn hàng.
- Click mã hoặc tên khách hàng mở hồ sơ chi tiết ngay trong `dcnet_crm`, không
  chuyển sang Customer Form.
- Hồ sơ chi tiết gồm thông tin tóm tắt, liên hệ, hoạt động, bán hàng, tệp đính
  kèm và các empty state cho phân hệ chưa có dữ liệu.
- Tab Thông tin chi tiết hiển thị dữ liệu Customer, liên hệ chính và địa chỉ
  hóa đơn trong cùng màn hình.
- Nút Sửa bật chế độ chỉnh sửa trực tiếp; Hủy khôi phục dữ liệu ban đầu và Lưu
  cập nhật các DocType chuẩn mà không chuyển sang Customer Form.
- Tab Liên hệ hiển thị dạng bảng, có phân trang, thêm đầy đủ, thêm nhanh, sửa
  trực tiếp và chọn Contact đã tồn tại để liên kết với Customer.
- Tab Hoạt động hiển thị bảng nhiệm vụ, lịch hẹn và cuộc gọi; hỗ trợ thêm/sửa,
  trạng thái, hạn hoàn thành, thời gian kết thúc, người thực hiện và phân trang.
- Tab Bán hàng hiển thị Đơn hàng, Trả lại hàng bán, Cơ hội, Báo giá, Hóa đơn,
  Hàng hóa đã mua và empty state Đại lý/Công ty con theo bố cục hai cột.
- Không triển khai panel AI của hệ thống tham khảo vì không thuộc đặc tả.

## Implementation

- `dcnet-crm/frontend/src/main.js`: Customer workspace, toolbar, table, filter,
  pagination và detail tabs.
- `dcnet-crm/frontend/src/styles.css`: layout ba panel và responsive states.
- `dcnet-crm/dcnet_crm/api.py`: API chi tiết và cập nhật Customer, Contact,
  Address cùng dữ liệu Sales Order và timeline theo permission.
- `dcnet-crm/dcnet_crm/public/dist/crm.bundle.js`: bundle đã build.

## Technical Notes

- Dữ liệu danh sách dùng `frappe.get_list`, không bỏ qua user permission.
- Trường tùy chọn được kiểm tra qua metadata trước khi query.
- Contact được tìm qua `Dynamic Link`, sau đó lọc lại bằng `frappe.get_list`.
- Email và điện thoại Contact được cập nhật qua child tables chuẩn
  `Contact Email` và `Contact Phone`.
- Contact mới hoặc Contact được chọn được gắn Customer bằng `Dynamic Link`.
- Nhiệm vụ dùng `ToDo`; lịch hẹn và cuộc gọi dùng `Event` cùng participant
  Customer/User để giữ đúng mô hình dữ liệu Frappe.
- Đơn hàng dùng `Sales Order`; trả hàng và hóa đơn được tách bằng
  `Sales Invoice.is_return`; hàng đã mua được tổng hợp từ hóa đơn đã submit.
- API cập nhật kiểm tra quyền `write` riêng cho Customer, Contact và Address.
- Sales Order chỉ lấy chứng từ chưa hủy (`docstatus < 2`).

## Contact List Extension

- Trang `contacts` dùng cùng bố cục danh sách ba panel với Customer.
- Cột dữ liệu lấy từ DocType chuẩn `Contact`, gồm mã liên hệ, xưng hô, họ tên,
  chức danh, điện thoại, email và tổ chức khi field tồn tại.
- Nút Hoạt động và Bộ lọc có trạng thái active riêng, ẩn/hiện độc lập.
- Khi đóng một panel, bảng chiếm phần diện tích vừa giải phóng; khi đóng cả
  hai panel, bảng chiếm toàn bộ chiều ngang workspace.

## Opportunity List Extension

- Trang Cơ hội dùng layout danh sách ba panel đồng nhất với Customer/Contact.
- Dữ liệu lấy từ DocType chuẩn `Opportunity`.
- Panel bên phải gồm Hoạt động, Khách hàng, Liên hệ và Hàng hóa.
- Hàng hóa lấy từ child table chuẩn `Opportunity Item`.
- Có tìm kiếm, phân trang, import Excel, filter và nút ẩn/hiện panel.
- Nút Thêm mở form toàn trang trong CRM, không chuyển sang Opportunity Form.
- Form lưu Customer, Contact, tên, loại, tỷ lệ, giai đoạn, ngày kỳ vọng,
  Territory, Company, Opportunity Item và mô tả bằng DocType chuẩn.
- Form được neo theo vùng nội dung của Desk để giữ nguyên native sidebar và
  không bị cắt nhãn khi mở từ danh sách Cơ hội.
- Nguồn gốc dùng trường chuẩn `Opportunity.utm_source`.
- `after_install` và `after_migrate` tự tạo các Custom Field đã được duyệt:
  địa chỉ giao hàng, dùng chung, mã cơ hội, đối tác/CTV giới thiệu và điểm
  lắp đặt A-End/Z-End trên `Opportunity Item`.
- Mã cơ hội được đồng bộ từ `Opportunity.name` sau khi insert.
- Tùy chọn tự tăng số lượng khi chọn trùng hoạt động ngay trên bảng hàng hóa.

## Deployment

```bash
cd /workspace/dcnet-crm
npm run build
cd /workspace/development/frappe-bench
bench --site flow.local migrate
bench --site flow.local clear-cache
bench restart
```

## Future Updates

Các trường doanh số, công nợ, điểm thưởng, tài liệu và lịch chăm sóc sẽ chỉ bổ
sung khi mapping DocType/field tương ứng được duyệt theo specification.

## Troubleshooting

- Hard reload trình duyệt nếu bundle cũ còn cache.
- Kiểm tra `dcnet_crm` trong `bench --site flow.local list-apps`.
- Kiểm tra Workspace Sidebar `CRM` có `app = dcnet_crm`.

## Verification Checklist

- [x] Frontend build thành công.
- [x] Python compile thành công.
- [x] API danh sách trả `tax_id` và phân trang.
- [x] API chi tiết trả timeline, đơn hàng và liên hệ.
- [x] API chi tiết trả liên hệ chính, địa chỉ hóa đơn và quyền chỉnh sửa.
- [x] Chỉnh sửa Customer/Contact/Address thực hiện ngay trong hồ sơ CRM.
- [x] Thêm, sửa và chọn liên hệ thực hiện trong tab Liên hệ, không mở Contact Form.
- [x] Tạo/sửa Nhiệm vụ, Lịch hẹn và Cuộc gọi ngay trong tab Hoạt động.
- [x] Hoàn thiện menu và dữ liệu tab Bán hàng theo chứng từ ERPNext chuẩn.
- [x] Form Cơ hội đúng bố cục hai cột và tự tạo/lưu các Custom Field đặc thù.
- [x] `bench migrate`, clear cache và restart thành công.
