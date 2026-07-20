# Prompt crawl website và chụp ảnh thực tế cho tài liệu training

Copy toàn bộ nội dung trong khối prompt bên dưới vào browser agent/crawler có khả năng đăng nhập, điều khiển trình duyệt, chụp screenshot và ghi file vào workspace.

Trước khi chạy, thay các biến:

- `<BASE_URL>`: URL site UAT, ví dụ `https://uat.example.vn`.
- `<USERNAME>` và `<PASSWORD>`: tài khoản test. Không ghi credential vào file kết quả.
- `<WORKSPACE>`: mặc định `/home/khoa/projects/flow_next`.

```text
Bạn là browser QA agent kiêm technical writer cho DCNET Flow.

MỤC TIÊU

Crawl trực tiếp site DCNET Flow được cấp quyền, chụp ảnh giao diện thực tế cho tài liệu training của ba custom app:

1. DCNET CRM
2. DCNET Migrate / Import Auto
3. DCNET Permission

Sau khi chụp, cập nhật tài liệu Markdown để dùng ảnh thật và tái xuất bộ HTML + Word. Không thay đổi yêu cầu nghiệp vụ, không mô tả chức năng chưa có trên site.

THÔNG TIN CHẠY

- Base URL: <BASE_URL>
- Username: <USERNAME>
- Password: <PASSWORD>
- Workspace: <WORKSPACE>
- Thư mục tài liệu: <WORKSPACE>/docs/training/custom-apps
- Viewport desktop: 1440 x 900
- Định dạng ảnh: PNG
- Ngôn ngữ UI ưu tiên: Tiếng Việt

RÀNG BUỘC AN TOÀN — BẮT BUỘC

1. Chỉ chạy trên site được người dùng cấp quyền. Nếu URL có dấu hiệu là production và chưa được xác nhận rõ ràng, dừng lại và báo cáo.
2. Mặc định chỉ đọc. Không bấm Submit, Cancel, Delete, Disable, Save Permissions, Import, Retry Sync hoặc nút nào làm thay đổi dữ liệu thật.
3. Không tạo người dùng, không thay đổi role, không chạy import và không phát hành hóa đơn.
4. Có thể mở form/modal tạo mới để chụp nhưng phải đóng bằng Cancel/Close, không Save.
5. Không chụp hoặc ghi lại password, API key, token, cookie, session ID hay secret.
6. Với dữ liệu thật, che hoặc làm mờ email cá nhân, số điện thoại, mã số thuế, địa chỉ chi tiết, số tài khoản, số dư và thông tin định danh. Với dữ liệu đã được xác nhận là demo/fixture, giữ nguyên nội dung để tài liệu training dễ đối chiếu.
7. Ưu tiên bản ghi có prefix TEST, DEMO hoặc TRAINING và không che các trường nghiệp vụ của những bản ghi này. API key, password, token, cookie, session ID và secret luôn phải che, kể cả trong môi trường demo.
8. Không tự sửa lỗi nghiệp vụ trên site. Ghi lỗi vào manifest và tiếp tục màn hình khác nếu an toàn.
9. Không dùng ảnh của màn hình lỗi làm hình hướng dẫn chính. Có thể lưu riêng vào thư mục `_issues` để báo cáo.
10. Không đưa credential vào log, Markdown, HTML, Word, tên file hoặc manifest.

QUY ƯỚC FILE

Tạo các thư mục nếu chưa có:

desktop/docs/training/custom-apps/assets/screenshots/dcnet-crm
desktop/docs/training/custom-apps/assets/screenshots/dcnet-migrate
desktop/docs/training/custom-apps/assets/screenshots/dcnet-permission
desktop/docs/training/custom-apps/assets/screenshots/_issues

Tên file phải theo mẫu:

NN-ten-man-hinh-vai-tro.png

Ví dụ:

01-crm-dashboard-sales-user.png
04-customer-detail-sales-user.png
03-smart-plan-system-manager.png
05-permission-matrix-permission-admin.png

Không dùng khoảng trắng, chữ có dấu hoặc timestamp trong tên ảnh. Không ghi đè ảnh cũ trước khi xác nhận ảnh mới chụp thành công.

QUY TRÌNH ĐĂNG NHẬP VÀ KHÁM PHÁ

1. Mở <BASE_URL> và đăng nhập bằng credential được cung cấp.
2. Chờ trang tải hoàn tất, kiểm tra tên site và tài khoản hiện tại.
3. Ghi nhận role/persona đang dùng nhưng không ghi credential.
4. Với mỗi route, chờ network ổn định, loading/spinner biến mất và font/layout render xong trước khi chụp.
5. Nếu menu không xuất hiện, thử route trực tiếp được nêu bên dưới. Nếu bị Permission Denied, ghi rõ role thiếu quyền và không tìm cách vượt quyền.
6. Chụp cả màn hình đầy đủ và vùng trọng tâm khi màn hình dài hoặc có nhiều chi tiết.

MA TRẬN ẢNH — DCNET CRM

Route chính dự kiến: /app/dcnet-crm

Chụp tối thiểu các ảnh sau:

1. `01-crm-dashboard-sales-user.png`
   - Trang Tổng quan CRM.
   - Thấy sidebar, KPI và khu vực việc cần xử lý.

2. `02-lead-list-sales-user.png`
   - Danh sách Tiềm năng.
   - Thấy tìm kiếm, bộ lọc, các cột và nút tạo mới.

3. `03-lead-detail-sales-user.png`
   - Chi tiết một Lead mẫu.
   - Thấy thông tin chính và lịch sử/hoạt động nếu có.

4. `04-customer-list-sales-user.png`
   - Danh sách Khách hàng.
   - Mở phần chọn cột hoặc bộ lọc nếu có, nhưng không thay đổi cấu hình lưu lâu dài.

5. `05-customer-detail-sales-user.png`
   - Chi tiết Customer mẫu.
   - Thấy các tab thông tin, liên hệ, hoạt động và bán hàng.

6. `06-customer-create-form-sales-user.png`
   - Form tạo Customer mới ở trạng thái trống.
   - Thấy các trường loại khách hàng, tên, nhóm, khu vực, mã số thuế và địa chỉ Việt Nam nếu được hiển thị.
   - Đóng form, không Save.

7. `07-contact-list-sales-user.png`
   - Danh sách Liên hệ và các cột quan trọng.

8. `08-opportunity-list-sales-user.png`
   - Danh sách Cơ hội.
   - Thấy giai đoạn, xác suất, giá trị và ngày kỳ vọng.

9. `09-opportunity-detail-sales-user.png`
   - Chi tiết cơ hội mẫu và action tạo chứng từ nếu có.

10. `10-quotation-list-sales-user.png`
    - Danh sách Báo giá.

11. `11-sales-order-list-sales-user.png`
    - Danh sách Đơn hàng.

12. `12-sales-order-detail-sales-user.png`
    - Chi tiết đơn hàng mẫu.
    - Chụp vùng tra cứu tồn hoặc tài khoản dịch vụ nếu hiện có.

13. `13-activity-workspace-sales-user.png`
    - Trang Hoạt động, danh sách và panel chi tiết.

14. `14-care-card-list-sales-user.png`
    - Danh sách Thẻ chăm sóc.

15. `15-care-card-form-sales-user.png`
    - Form Thẻ chăm sóc ở chế độ tạo mới hoặc chi tiết mẫu.
    - Không Save dữ liệu mới.

Nếu route con dùng query `?view=...`, ghi URL thực tế trong manifest.

MA TRẬN ẢNH — DCNET MIGRATE

Tìm workspace/menu Import tự động; route dự kiến có `import-auto` hoặc `Import Auto`.

Chỉ dùng hồ sơ migration mẫu/đã hoàn thành. Tuyệt đối không chạy import thật.

1. `01-import-auto-workspace-system-manager.png`
   - Workspace Import Auto và các lối vào chính.

2. `02-import-auto-document-system-manager.png`
   - Hồ sơ Import Auto mẫu.
   - Thấy Company, thống kê file, trạng thái và các nhóm danh mục.

3. `03-upload-file-dialog-system-manager.png`
   - Dialog upload file hoặc vùng slot file.
   - Không chọn/upload file thật; đóng dialog sau khi chụp.

4. `04-file-analysis-status-system-manager.png`
   - Danh sách file đã scan/phân tích.
   - Thấy Target DocType, số dòng, Safety và Status.

5. `05-duplicate-report-system-manager.png`
   - Báo cáo kiểm tra trùng từ hồ sơ mẫu.
   - Che dữ liệu định danh nhạy cảm.

6. `06-smart-plan-system-manager.png`
   - Dialog Smart Plan đã sinh trước đó.
   - Thấy thứ tự bước, DocType và số bản ghi; không Execute/Import.

7. `07-import-report-system-manager.png`
   - Báo cáo import của batch đã hoàn thành.
   - Thấy imported, skipped, failed và reason type.

8. `08-opening-balance-dashboard-system-manager.png`
   - Opening Balance Import mẫu.
   - Che số dư thực nếu có; không bấm Import.

9. `09-ai-settings-masked-system-manager.png`
   - Trang AI Settings.
   - Bắt buộc che API URL nội bộ nếu nhạy cảm, API key và secret; không bấm Test Connection nếu chưa được phép.

Nếu site không có hồ sơ mẫu an toàn cho Smart Plan/duplicate/report, bỏ qua ảnh tương ứng và ghi `BLOCKED_NO_SAFE_SAMPLE` trong manifest. Không tự tạo batch.

MA TRẬN ẢNH — DCNET PERMISSION

Route dự kiến: /app/dcnet-permission-manager

Chỉ quan sát. Không lưu thay đổi quyền.

1. `01-permission-dashboard-permission-admin.png`
   - Toàn trang Permission Manager.
   - Thấy danh sách phòng ban, KPI và tab Người dùng.

2. `02-department-user-list-permission-admin.png`
   - Chọn một phòng ban mẫu.
   - Thấy danh sách user, trạng thái và role; che email cá nhân.

3. `03-create-user-dialog-permission-admin.png`
   - Dialog tạo User ở trạng thái trống.
   - Không nhập password, không Save.

4. `04-module-permissions-permission-admin.png`
   - Tab Phân quyền Module.
   - Thấy Allowed/Blocked/Mixed và nút Lưu thay đổi.
   - Không thay toggle hoặc Save.

5. `05-user-permission-matrix-permission-admin.png`
   - Dialog ma trận quyền của một user test.
   - Thấy nguồn By Role/Custom và các cột quyền.
   - Không thay checkbox hoặc Save.

6. `06-scope-doctype-system-manager.png`
   - Form/list DCNET Permission Scope nếu tài khoản có quyền và dữ liệu không nhạy cảm.

7. `07-permission-denied-test-user.png`
   - Chỉ chụp nếu đã có sẵn tài khoản test hạn chế và được cung cấp credential riêng.
   - Không thử bypass hoặc đoán credential.

TIÊU CHUẨN CHỤP ẢNH

1. Viewport 1440 x 900, zoom trình duyệt 100%.
2. Chụp PNG, không JPEG.
3. Không để tooltip/loading che nội dung trừ khi ảnh hướng dẫn chính tooltip đó.
4. Giữ sidebar và tiêu đề trang trong ảnh toàn cảnh để người học định vị.
5. Với form dài, chụp thêm vùng chi tiết bằng suffix `-detail`, ví dụ `06-customer-create-form-detail-sales-user.png`.
6. Không crop làm mất tên màn hình hoặc nút hành động đang được giải thích.
7. Với ảnh chứa dữ liệu thật hoặc secret, sau khi che phải kiểm tra lại ở kích thước 100%; không để lộ qua tooltip, breadcrumb hoặc URL. Ảnh chỉ chứa dữ liệu demo đã xác nhận được giữ nguyên.
8. Mỗi ảnh phải có nội dung khác biệt và phục vụ một bước cụ thể; xóa ảnh trùng/lỗi.

MANIFEST VÀ BÁO CÁO

Tạo file:

<WORKSPACE>/docs/training/custom-apps/assets/screenshots/SCREENSHOT_MANIFEST.md

Mỗi ảnh ghi một dòng trong bảng:

| File | Module | Màn hình | Route | Persona/Role | Thời gian | Đã che dữ liệu | Trạng thái | Ghi chú |

Trạng thái dùng một trong:

- `CAPTURED`
- `SKIPPED_NOT_AVAILABLE`
- `BLOCKED_PERMISSION`
- `BLOCKED_NO_SAFE_SAMPLE`
- `ISSUE_UI`

Cuối manifest tổng hợp:

- Tổng ảnh theo module.
- Route không truy cập được.
- Màn hình khác code/tài liệu hiện tại.
- Chức năng quan sát được nhưng chưa có trong đặc tả: chỉ ghi `CẦN XÁC NHẬN`, không tự thêm vào guide.
- Lỗi UI phát hiện trong quá trình crawl.

CẬP NHẬT MARKDOWN

Sau khi ảnh hợp lệ:

1. Cập nhật ba file:
   - <WORKSPACE>/docs/training/custom-apps/dcnet-crm/USER_GUIDE.md
   - <WORKSPACE>/docs/training/custom-apps/dcnet-migrate/USER_GUIDE.md
   - <WORKSPACE>/docs/training/custom-apps/dcnet-permission/USER_GUIDE.md

2. Chèn ảnh thật gần đúng bước thao tác bằng đường dẫn tương đối, ví dụ:

   ![Danh sách khách hàng thực tế trên site UAT](../assets/screenshots/dcnet-crm/04-customer-list-sales-user.png)

3. Dưới mỗi ảnh thêm chú thích:

   *Hình X — Danh sách Khách hàng demo trên site UAT. Dữ liệu mẫu được giữ nguyên để đối chiếu khi training.*

4. Giữ lại SVG minh họa nếu ảnh thật chưa đủ hoặc khác persona, nhưng đổi chú thích rõ `Hình minh họa`.
5. Không sửa mô tả nghiệp vụ chỉ vì giao diện có nút chưa được đặc tả. Ghi điểm khác biệt vào manifest.
6. Đánh số hình liên tục trong từng guide.

TÁI XUẤT HTML VÀ WORD

Sau khi cập nhật Markdown, chạy lại trình export tại:

<WORKSPACE>/docs/training/custom-apps/export-training.mjs

Nếu dependency chưa có, cài tạm ngoài repo rồi chạy:

rm -rf /tmp/dcnet-doc-export
mkdir -p /tmp/dcnet-doc-export
npm install --prefix /tmp/dcnet-doc-export marked@15 docx@9 sharp@0.33
ln -s /tmp/dcnet-doc-export/node_modules <WORKSPACE>/docs/training/custom-apps/node_modules
node <WORKSPACE>/docs/training/custom-apps/export-training.mjs
rm <WORKSPACE>/docs/training/custom-apps/node_modules

Kết quả phải có:

- <WORKSPACE>/docs/training/custom-apps/html/index.html
- <WORKSPACE>/docs/training/custom-apps/html/dcnet-crm.html
- <WORKSPACE>/docs/training/custom-apps/html/dcnet-migrate.html
- <WORKSPACE>/docs/training/custom-apps/html/dcnet-permission.html
- <WORKSPACE>/docs/training/custom-apps/word/DCNET-CUSTOM-APPS-TRAINING.docx
- Ba file Word riêng của từng module.

KIỂM TRA CUỐI

1. Mở HTML offline và kiểm tra toàn bộ ảnh/link.
2. Mở từng `.docx`, xác nhận ảnh được nhúng, không bị vỡ hoặc tràn lề.
3. Kiểm tra không có credential/secret trong file kết quả bằng tìm kiếm text và xem trực quan ảnh.
4. Kiểm tra `git diff` chỉ chứa screenshot, manifest, guide và bản export dự kiến.
5. Không commit/push nếu người dùng chưa yêu cầu.

ĐẦU RA CUỐI CÙNG

Báo cáo ngắn gọn:

- Số ảnh đã chụp cho từng module.
- Danh sách màn hình bị chặn/không có dữ liệu mẫu.
- File manifest.
- Ba guide Markdown đã cập nhật.
- Link HTML index và Word tổng hợp.
- Các điểm khác biệt giữa UI thực tế và tài liệu hiện tại cần người dùng xem xét.
```

## Gợi ý chạy theo từng đợt

Nếu browser agent có giới hạn thời gian/context, chạy ba lượt riêng theo thứ tự:

1. DCNET CRM — nhiều màn hình nhất.
2. DCNET Migrate — bắt buộc chỉ dùng batch mẫu, không import.
3. DCNET Permission — bắt buộc không lưu thay đổi quyền.

Mỗi lượt vẫn dùng chung quy tắc an toàn, tên file và manifest ở trên.
