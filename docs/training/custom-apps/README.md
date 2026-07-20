# Bộ tài liệu training các chức năng custom — DCNET Flow

> **Phiên bản tài liệu:** 1.0  
> **Cập nhật:** 13/07/2026  
> **Đối tượng:** Người đào tạo, key user, quản trị hệ thống và đội hỗ trợ  
> **Nguyên tắc:** Chỉ mô tả chức năng đã có trong code hoặc đặc tả chính thức.

## 1. Mục đích

Thư mục này là điểm bắt đầu duy nhất khi chuẩn bị đào tạo các phần DCNET phát triển thêm trên Frappe/ERPNext. Tài liệu phân biệt rõ:

- **ERPNext chuẩn:** nghiệp vụ có sẵn, DCNET chỉ cấu hình hoặc hiển thị lại.
- **DCNET mở rộng:** giao diện, kiểm soát hoặc quy trình được DCNET phát triển thêm.
- **Cần xác nhận:** chức năng chưa đủ yêu cầu khách hàng hoặc chưa thể hiện chắc chắn trong code.

## 2. Các guide đã sẵn sàng

| App / module | Nội dung training | Guide | Nguồn chính |
|---|---|---|---|
| `dcnet-crm` | CRM hợp nhất: Lead, Cơ hội, Khách hàng, Liên hệ, Báo giá, Đơn hàng, Hoạt động, Thẻ chăm sóc | [Mở guide CRM](dcnet-crm/USER_GUIDE.md) | `FEATURE_SPECIFICATION.md` mục 3, 4, 13, 14; code `dcnet-crm` |
| `dcnet-migrate` | Import Excel có phân tích, kiểm tra trùng, kế hoạch import và báo cáo lỗi | [Mở guide Migrate](dcnet-migrate/USER_GUIDE.md) | Code `dcnet-migrate`; handoff Import Auto; kế hoạch migration BRAVO |
| `dcnet-permission` | Quản lý user và phân quyền theo phòng ban, module, ma trận quyền chi tiết | [Mở guide Permission](dcnet-permission/USER_GUIDE.md) | `FEATURE_SPECIFICATION.md` mục 12; code `dcnet-permission` |

### 2.1. Bản xuất bản dùng khi training

- **HTML offline:** mở [`html/index.html`](html/index.html). Thư mục chứa trang chủ, ba guide chi tiết, CSS và toàn bộ ảnh SVG nên có thể copy nguyên thư mục sang máy training.
- **Word tổng hợp:** [`word/DCNET-CUSTOM-APPS-TRAINING.docx`](word/DCNET-CUSTOM-APPS-TRAINING.docx).
- **Word từng module:** nằm trong thư mục [`word/`](word/), ảnh giao diện và sơ đồ quy trình đã được nhúng trực tiếp vào từng file `.docx`.

File `export-training.mjs` là trình sinh lại hai thư mục xuất bản từ Markdown. Không sửa trực tiếp HTML/Word nếu thay đổi nội dung lâu dài; cập nhật `USER_GUIDE.md` rồi chạy lại trình export để các định dạng đồng bộ.

### 2.2. Crawl site để lấy screenshot thật

Dùng [prompt crawl website và chụp ảnh thực tế](CRAWL_SCREENSHOT_PROMPT.md) cho browser agent. Prompt có sẵn ma trận màn hình, quy tắc che dữ liệu nhạy cảm, chế độ chỉ đọc, manifest ảnh và bước tái xuất HTML/Word.

## 3. Danh mục custom cần tiếp tục viết guide

| Ưu tiên | App / nhóm custom | Phạm vi quan sát được trong repo | Tài nguyên hình ảnh hiện có | Trạng thái guide |
|---:|---|---|---|---|
| 1 | `dcnet-accounting` | Kế toán Việt Nam, tài sản, CCDC, báo cáo và cấu hình | Nhiều screenshot QA theo persona | Chưa chuẩn hóa thành user guide |
| 1 | `dcnet-einvoice` | Hóa đơn điện tử đa nhà cung cấp, đồng bộ và retry | 5 screenshot QA | Chưa chuẩn hóa thành user guide |
| 1 | `dcnet_htkk` | Lập tờ khai thuế HTKK | Chưa kiểm kê ảnh UAT | Chưa chuẩn hóa thành user guide |
| 2 | `dcnet-banking` | Import sao kê và tự động đối chiếu | Chưa kiểm kê ảnh UAT | Chưa chuẩn hóa thành user guide |
| 2 | `dcnet-contract` | Hợp đồng một lần/định kỳ, lịch thanh toán, dòng tiền | Chưa kiểm kê ảnh UAT | Chưa chuẩn hóa thành user guide |
| 2 | `dcnet-pakd` | Phương án kinh doanh và bảng tính hoa hồng | Chưa kiểm kê ảnh UAT | Chưa chuẩn hóa thành user guide |
| 2 | `dcnet-organization` | Liên kết Công ty, Chi nhánh, Phòng ban, Chức danh | Chưa kiểm kê ảnh UAT | Chưa chuẩn hóa thành user guide |
| 3 | `dcnet-theme` | Theme Desk và điều hướng sidebar theo ngữ cảnh | Không cần guide nghiệp vụ dài | Cần quick guide quản trị |
| 3 | `dcnet_apps` custom | Dashboard, report, barcode, image, fitting, coaching, loyalty, giao vận, workflow diagram… | Phân tán theo module docs | Viết theo STT module, không gom thành một app guide |

> Danh mục trên là kiểm kê code, không phải cam kết phạm vi hợp đồng. Trước khi viết từng guide phải map lại đặc tả khách hàng và đánh dấu nội dung cần clarify.

### 3.1. Chi tiết các vùng custom trong app dùng chung `dcnet_apps`

| Vùng code | Nội dung cần đưa vào training | Cách đóng gói tài liệu |
|---|---|---|
| `dcnet_dashboard` | Dashboard và KPI custom | Guide module 02 và các báo cáo liên quan |
| `dcnet_report` | Báo cáo DCNET | Guide theo từng báo cáo/module nghiệp vụ |
| `barcode_management` | Quản lý/in mã vạch | Guide Sản phẩm/Kho |
| `dcnet_image_management` | Cập nhật và quản lý ảnh hàng hóa | Guide Sản phẩm/Mua hàng |
| `purchase_order` | Mở rộng Purchase Order | Guide module 05 Mua hàng |
| `sales_order` | Mở rộng Sales Order | Guide module 09/12 Bán hàng |
| `sales_invoice` | Mở rộng Sales Invoice | Guide bán hàng và kế toán bán |
| `stock` | Mở rộng nghiệp vụ kho | Guide module 07 Kho hàng |
| `einvoice` | Thành phần HĐĐT cũ/trong app dùng chung | Phải phân biệt với app riêng `dcnet-einvoice` trước training |
| `htkk` | Thành phần HTKK cũ/trong app dùng chung | Phải phân biệt với app riêng `dcnet_htkk` trước training |
| `crm` | Thành phần CRM cũ/trong app dùng chung | Guide chính dùng app riêng `dcnet-crm`; ghi rõ phần còn được gọi lại |
| `workflow_diagram` | Sơ đồ quy trình trên Workspace | Quick guide cho key user/quản trị |
| `workspace_sidebar` | Sidebar và điều hướng custom | Quick guide định hướng giao diện |
| `mobile_push` | Thông báo push | Guide quản trị và xử lý sự cố |
| `migration_install` | Hỗ trợ chuyển đổi/cài đặt | Runbook kỹ thuật, không đào tạo end user |
| `dcnet_ecommerce` | Kết nối/e-commerce custom | Guide riêng sau khi scope tích hợp được khách xác nhận |

Các thư mục kỹ thuật như `fixtures`, `patches`, `setup`, `translations`, `utils`, `public` không phải menu nghiệp vụ độc lập; chỉ đưa vào runbook quản trị khi có thao tác vận hành tương ứng.

## 4. Quy ước hình ảnh

1. Ảnh thật phải lấy từ site UAT, dùng dữ liệu mẫu và che email, số điện thoại, mã số thuế hoặc số tài khoản nhạy cảm.
2. Tên file: `{step}-{screen}-{variant}.png`, ví dụ `03-customer-detail-sales-user.png`.
3. Ảnh mô phỏng dùng SVG và phải có dòng **“Hình minh họa — không phải ảnh production”**.
4. Mỗi ảnh trong guide phải có chú thích nêu rõ người dùng cần nhìn vào đâu.
5. Khi UI thay đổi, cập nhật cả ảnh, chú thích và ngày phiên bản tài liệu.

## 5. Checklist trước buổi training

- [ ] Chốt persona tham dự và quyền của từng tài khoản mẫu.
- [ ] Chuẩn bị dữ liệu mẫu không chứa thông tin thật.
- [ ] Chạy thử toàn bộ kịch bản trên site UAT.
- [ ] Thay ảnh minh họa bằng screenshot UAT nếu môi trường đã sẵn sàng.
- [ ] Kiểm tra tên nút và menu đúng phiên bản đang triển khai.
- [ ] Chuẩn bị kịch bản lỗi có kiểm soát và cách khôi phục.
- [ ] Ghi lại câu hỏi chưa có trong đặc tả để xác nhận với khách hàng.

## 6. Cấu trúc chuẩn cho guide tiếp theo

Mỗi app/module tạo thư mục riêng với `USER_GUIDE.md` và `assets/`. Guide tối thiểu gồm: phạm vi, đối tượng/quyền, truy cập, sơ đồ quy trình, thao tác từng bước, kiểm soát dữ liệu, bài thực hành, xử lý lỗi, FAQ, thuật ngữ và nguồn đối chiếu.
