# DCNET CRM — Vấn đề cần Clarify

> **Ngày cập nhật:** 13/07/2026  
> **Trạng thái:** Chờ khách hàng xác nhận

## Quy ước

| Icon | Ý nghĩa |
|---|---|
| :red_circle: | Critical — block triển khai |
| :orange_circle: | High — ảnh hưởng thiết kế/sprint |
| :yellow_circle: | Medium — có thể tiếp tục phần độc lập |
| :green_circle: | Resolved |

## Tích hợp và đa kênh

| # | Câu hỏi | Priority | Ảnh hưởng | Nguồn |
|---|---|---|---|---|
| CRM-CL-01 | Nguồn ngoài tại 3.7 là `nhanh_vn` hay hệ thống nào khác? Cần schema, auth và quy tắc chống trùng. | :red_circle: | Không thể hoàn thành auto-create Lead | 3.7 |
| CRM-CL-02 | Dùng nhà cung cấp/credential nào cho Zalo OA và Messenger? | :red_circle: | Block giao tiếp đa kênh | 4.3.6 |
| CRM-CL-03 | Cần đồng bộ sàn nào trước và schema từng sàn ra sao? | :red_circle: | Block đồng bộ đơn hàng | 5.12 |

## Chăm sóc và bán lại

| # | Câu hỏi | Priority | Ảnh hưởng | Nguồn |
|---|---|---|---|---|
| CRM-CL-04 | Rule phân nhóm, lịch gửi, nội dung và cơ chế opt-out cho khuyến mãi là gì? | :orange_circle: | Thiết kế scheduler/campaign | 4.3.2 |
| CRM-CL-05 | Rule gợi ý Upsell/Cross-sell và kênh gửi nào được duyệt? | :orange_circle: | Thiết kế recommendation | 4.3.7 |
| CRM-CL-06 | “Resell” bao gồm những trigger/trạng thái/kênh gửi cụ thể nào? | :orange_circle: | Thiết kế hậu mãi | 5.9 |

## Cài đặt và báo cáo

| # | Câu hỏi | Priority | Ảnh hưởng | Nguồn |
|---|---|---|---|---|
| CRM-CL-07 | Có cho tùy chỉnh trạng thái đơn ngoài workflow/docstatus ERPNext không? | :orange_circle: | Data model và workflow | 13.4 |
| CRM-CL-08 | Có cho tùy chỉnh loại hành động nhân viên ngoài danh sách cài sẵn không? | :yellow_circle: | Settings/UI hoạt động | 13.5 |
| CRM-CL-09 | Công thức chính thức cho từng KPI/report, đặc biệt “tỷ lệ chốt” và “hiệu suất”, là gì? | :red_circle: | Không thể nghiệm thu 14.1–14.4 | 14.1–14.4 |
| CRM-CL-10 | “Di tuyến/GPS” có thuộc hợp đồng hay chỉ là tính năng tham khảo? | :yellow_circle: | Kiểm soát scope | Ngoài spec hiện tại |

## Thống kê

| Priority | Số lượng |
|---|---:|
| :red_circle: Critical | 4 |
| :orange_circle: High | 4 |
| :yellow_circle: Medium | 2 |
| **Tổng** | **10** |
