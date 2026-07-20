# Bàn giao công việc CRM ngày 14/07/2026

## Cập nhật ngày 16/07/2026

- **Fix bug: "Tùy chỉnh thông tin tóm tắt" không mở dialog ở trang Khách hàng.**
  - Nguyên nhân thật sự: khối HTML của dialog (`customerSummaryDialogOpen`) bị đặt
    nhầm bên trong `<main v-else-if="route === 'customers'">` (trang danh sách),
    thay vì bên trong `<main v-else-if="route === 'customer-detail'">` (trang chi
    tiết) — nơi nút bấm mở dialog thực sự nằm. Khi xem trang chi tiết, nhánh
    "customers" luôn là `false` nên dialog không bao giờ được tạo ra trong DOM,
    dù state `customerSummaryDialogOpen` vẫn đổi đúng thành `true`. Đây KHÔNG
    phải lỗi framework Vue — đã verify bằng test cô lập (Node + jsdom) trước khi
    sửa. Không liên quan tới nút "Tùy chỉnh cột" (`customerColumnDialogOpen`),
    nút đó vẫn đặt đúng vị trí (chỉ dùng cho trang danh sách).
  - File sửa: `frontend/src/features/customers/template.js` (di chuyển khối
    `.customer-summary-dialog-backdrop` sang đúng `<main>` của trang chi tiết).
  - Checklist Discussion #9 (dòng "Nút tùy chỉnh Thông tin tóm tắt hoạt động")
    trước đó đánh dấu "fixed" nhưng thực tế chưa hoạt động trên trang chi tiết —
    cần cập nhật lại trạng thái QA cho đúng.
- **Feature mới (ngoài checklist Discussion #9): thêm tab "Tổng quan" ở trang
  chi tiết Khách hàng**, đặt làm tab mặc định/đầu tiên. Nội dung: 4 thẻ chỉ số
  (Số lượng đơn hàng, Giá trị đơn hàng, Công nợ, Chu kỳ mua hàng — chu kỳ mua
  hàng tự tính từ khoảng cách trung bình giữa các `Sales Order.transaction_date`,
  không có sẵn ở backend), danh sách "Hàng hóa đã mua", panel "Hoạt động" và
  panel "Nội dung trao đổi" (đọc/gửi y hệt tab Trao đổi hiện có). Toàn bộ dùng
  dữ liệu thật đã có sẵn từ `get_customer_workspace`, không có phần AI (theo yêu
  cầu). File sửa: `frontend/src/features/customers/{template.js,composable.js}`,
  `frontend/src/styles.css`. ⚠️ Feature này do khách yêu cầu trực tiếp trong
  phiên làm việc, chưa có trong `FEATURE_SPECIFICATION.md` — cần ghi nhận vào
  `CUSTOM_REQUIREMENTS.md`/SPEC_MAPPING của module Khách hàng nếu có.

## Nhánh làm việc

- Repository: `dcnet-cloud/dcnet-crm`
- Branch: `fix/discussion-9-crm-feedback-14072026`
- Pull Request chung: [PR #12 — Apply Discussion #9 feedback by sidebar module](https://github.com/dcnet-cloud/dcnet-crm/pull/12)
- PR merge vào `develop`; lịch sử commit đã được dựng lại ngày 16/07/2026 để BA kiểm tra theo từng mục sidebar.

## Các commit đã tách

| Commit | Nhóm thay đổi | Nội dung chính |
|---|---|---|
| `26607da` | Dùng chung | API, router, quyền, nhật ký, attachment và style dùng chung cho Discussion #9 |
| `63ed878` | Bàn làm việc | Dashboard vừa khung nhìn |
| `c122ecc` | Tiềm năng | Danh sách, chi tiết, bộ lọc, popup hoạt động và các feedback UI |
| `435e6fc` | Liên hệ | Form nhập tay chức danh/phòng ban, detail MISA và panel liên quan |
| `a305228` | Khách hàng | Detail, tóm tắt tùy chỉnh và panel Hoạt động/Mua hàng/Liên hệ |
| `6a6432c` | Cơ hội | Panel dữ liệu Cơ hội/Khách hàng và bốn tab liên quan |
| `daf2528` | Báo giá | Action chi tiết và điều hướng nội bộ CRM |
| `ed870af` | Đơn hàng | Vòng đời đề nghị ghi, trạng thái, Account, in theo mẫu và liên kết khách hàng |
| `0ce537f` | Tài khoản | Liên kết và cập nhật Account theo quyền |
| `0e6491f` | Hoạt động | Điều hướng nhiệm vụ/lịch hẹn/cuộc gọi về workspace Hoạt động |
| `7fe47cd` | Kiểm thử | Test hồi quy API cho các luồng Discussion #9 |
| `ef68041` | Bundle build | Bundle production build lại từ toàn bộ source ở trên |

## Trạng thái Pull Request

- PR: [#12](https://github.com/dcnet-cloud/dcnet-crm/pull/12)
- Base: `develop`
- Head: `fix/discussion-9-crm-feedback-14072026`
- Trạng thái: `OPEN`, merge state `CLEAN`.
- Git Flow Guard: `SUCCESS`.
- Static checks: `SUCCESS`.
- Discord PR Notify: `SUCCESS`.
- Frappe tests trên GitHub Actions: `SKIPPED`; bộ backend test đã chạy local ngày 15/07/2026 và đạt `39/39`.
- PR chưa có review decision; chờ chị P manual QA theo từng mục sidebar.

## Kết quả đã làm

- Tiềm năng có bộ lọc và layout chi tiết theo mẫu MISA; giữ active menu khi mở chi tiết.
- Tiềm năng không tự tạo dữ liệu Liên hệ ngoài luồng chuyển đổi được cho phép.
- Ghi chú và Trao đổi đã tách nghiệp vụ:
  - Ghi chú dùng `Comment`.
  - Trao đổi dùng `Communication`.
- Thêm nhiệm vụ, lịch hẹn và cuộc gọi bằng popup; bản ghi mở trong trang Hoạt động CRM.
- Tài liệu đính kèm có Thêm liên kết/Thêm tệp; URL thiếu scheme tự thêm `https://`; icon phân biệt link và ảnh/tệp.
- Liên hệ và Khách hàng dùng layout chi tiết MISA; các sửa đổi chung từ Tiềm năng được áp dụng đồng bộ.
- Danh sách Liên hệ dùng đúng hai tab panel phải `Hoạt động / Mua hàng`: panel chỉ đọc dữ liệu, không tạo ghi chú tại danh sách; ghi chú `Comment` và công việc của liên hệ được gom theo thời gian ở Hoạt động; Báo giá, Cơ hội, Đơn hàng và Hóa đơn liên quan được hiển thị ở Mua hàng và mở đúng chứng từ khi bấm.
- Danh sách Khách hàng đã sửa panel phải `Hoạt động / Mua hàng / Liên hệ` bị co nội dung do còn thừa một hàng grid từ UI cũ; tab Hoạt động chỉ đọc dữ liệu, không tạo ghi chú trực tiếp tại danh sách.
- Danh sách Cơ hội giữ layout panel riêng (thao tác, tab và nội dung), tránh khoảng trắng lớn sau khi đồng bộ layout Khách hàng; tab Hoạt động chỉ đọc dữ liệu, không có ô nhập/gửi ghi chú tại danh sách.
- Form sửa Khách hàng đã tách đúng **Lĩnh vực** và **Ngành nghề** (không còn hai dòng cùng nhãn), đồng thời đổi các trường phân loại từ text sang dropdown lấy dữ liệu chuẩn của ERPNext/metadata Customer.
- Chức danh và Phòng ban của Liên hệ cho phép nhập tay.
- Báo giá, Cơ hội và Đơn hàng điều hướng trong CRM; chỉ Hóa đơn được phép sang Accounting và phải kiểm tra quyền.
- Dòng hàng Đơn hàng hiển thị Account phù hợp khi account đã tồn tại.
- Dashboard co giãn theo khung nhìn.
- Bộ lọc không còn nút “Xem thêm”; chỉ nội dung thực sự có điều hướng mới dùng màu xanh.
- Empty-state icon được tăng kích thước đồng bộ.
- Nút “Sinh đơn hàng” dùng màu theme hệ thống.
- Tab Trao đổi được làm lại dạng luồng bình luận và chiếm toàn bộ chiều rộng nội dung.
- Trạng thái Đơn hàng được suy ra từ `docstatus`, trạng thái chuẩn, tỷ lệ đã xuất hóa đơn và tỷ lệ đã giao:
  - Đơn chưa submit hiển thị `Đơn nháp`.
  - Đơn đã xuất hóa đơn đủ nhưng chưa giao hiển thị `Đã ghi` và `Chờ giao hàng`.
  - Không ghi đè các custom field cũ vào database; đây là trạng thái hiển thị theo dữ liệu chuẩn ERPNext.
- In Đơn hàng dùng chung kho mẫu Word của `dcnet-contract`:
  - Nút `In` mở popup để chọn mẫu, xem trước, tải Word hoặc in.
  - Đã bỏ icon tải Word riêng trên tiêu đề.
  - Mẫu được điền bằng dữ liệu Sales Order tại thời điểm người dùng chọn.
  - Thẻ khách hàng trên chi tiết đơn mở đúng trang Khách hàng trong CRM.

## Tài liệu kiểm tra

- Checklist tổng hợp Discussion #9: `docs/DISCUSSION_9_FEEDBACK_CHECKLIST.html`
- Nguồn feedback: <https://github.com/dcnet-cloud/dcnet-crm/discussions/9>

## Kiểm thử đã chạy

- Frontend ngày 16/07/2026: `npm test`, `npm run build`, `git diff --check` đều thành công.
- Python ngày 16/07/2026: `python3 -m py_compile` thành công với API, hooks, install, sales order events và test module.
- Backend gần nhất ngày 15/07/2026: `bench --site flow.local run-tests --app dcnet_crm --module dcnet_crm.tests.test_api --test-category integration` — `39/39` test passed. Chưa chạy lại ngày 16/07 vì devcontainer không tồn tại trên máy hiện tại.
- In đơn hàng: đã kiểm tra danh sách 14 mẫu thật từ `dcnet-contract`; xem trước mẫu `HD Dich vu Vien thong` có mã đơn, khách hàng và không còn placeholder; tạo DOCX theo mẫu đã chọn thành công.
- Đã chạy `bench --site flow.local clear-cache` sau thay đổi cuối.

## Việc cần làm tiếp ngày 17/07/2026

1. Checkout branch và cập nhật code:

   ```bash
   git fetch origin
   git switch fix/discussion-9-crm-feedback-14072026
   git pull --ff-only origin fix/discussion-9-crm-feedback-14072026
   ```

2. Manual QA theo `docs/DISCUSSION_9_FEEDBACK_CHECKLIST.html`, ưu tiên:
   - Ghi chú không xuất hiện trong Trao đổi và ngược lại.
   - Tạo nhiệm vụ/lịch hẹn/cuộc gọi rồi mở tại workspace Hoạt động.
   - Link Cơ hội/Báo giá/Đơn hàng ở lại CRM; Hóa đơn kiểm tra quyền trước khi mở Accounting.
   - Upload file và thêm URL không có scheme ở Tiềm năng, Liên hệ, Khách hàng.
   - Kiểm tra responsive Dashboard và các trang danh sách ở độ phân giải 1366px/1920px.
3. Rà lại quyền bằng một user Sales không phải Administrator.
4. Chỉ sửa các lỗi phát hiện trong checklist; thêm test hồi quy tương ứng.
5. Cập nhật kết quả QA trực tiếp vào checklist PR #12 theo từng mục sidebar.
6. Chỉ merge PR vào `develop` sau khi người phụ trách xác nhận hoàn tất.

## Lưu ý worktree

- `dcnet_crm/workspace_sidebar/crm.json` còn thay đổi cục bộ có sẵn và không được đưa vào các commit feedback để tránh ghi đè phần việc khác.
- Không reset hoặc checkout bỏ thay đổi file trên nếu chưa xác nhận với người đang phụ trách.
