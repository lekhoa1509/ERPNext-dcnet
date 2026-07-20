# Requirements Document

## Introduction

Tính năng **Vận hành quy trình** (process execution / runtime) bổ sung phần "chạy" và "duyệt" cho app `dcnet-process` trong dự án DCNET Flow (Frappe v16 + ERPNext v16). App đã có sẵn phần **thiết kế quy trình** (process builder: `DC Process Template` và các child table Step/Field/Field Condition/Flow Rule/Permission Row/Print Template, service `process_template.py`, trang builder). Phần runtime hiện mới chỉ có khung DocType rỗng (`DC Process Instance`, `DC Process Step Instance`, `DC Process History`) chưa có engine, API hay UI.

Mục tiêu: cho phép người dùng **khởi chạy** một quy trình đã publish, hệ thống tự **điều phối các bước** (resolve người xử lý, đánh giá điều kiện rẽ nhánh, xử lý bước song song), người xử lý thực hiện các **hành động** (đồng ý, từ chối, chuyển tiếp, trả về, comment, đính kèm, thu hồi, chuyển giao, hủy), ghi **lịch sử đầy đủ**, quản lý **deadline/quá hạn** và gửi **thông báo**. Trải nghiệm vận hành (UI/UX) bám sát 100% MISA AMIS Quy Trình.

Tham chiếu nghiệp vụ đối thủ: `docs/competitor-analysis/misa-amis/quy-trinh/ANALYSIS.md`.

### Phạm vi (Scope)
- **Trong phạm vi:** engine thực thi, vòng đời lượt chạy (instance), các hành động xử lý bước, resolve người xử lý, rẽ nhánh điều kiện, bước song song, deadline/quá hạn, lịch sử/audit trail, thông báo (email + desk), inbox "công việc của tôi", danh sách lượt chạy, màn hình khởi chạy & xử lý, dashboard cơ bản, phân quyền runtime.
- **Ngoài phạm vi (giai đoạn này):** chỉnh sửa process builder (đã có), thư viện 500+ template của MISA, ký số WeSign, tính năng AI, mobile app riêng, Open API bên thứ ba.

## Glossary

- **Template / Quy trình:** bản thiết kế (`DC Process Template`) đã publish (status = Active).
- **Instance / Lượt chạy:** một lần thực thi quy trình (`DC Process Instance`).
- **Step Instance / Bước chạy:** trạng thái thực thi của một bước trong lượt chạy (`DC Process Step Instance`).
- **Flow Rule / Luật chuyển bước:** quy tắc xác định bước kế tiếp dựa trên hành động + điều kiện (`DC Process Flow Rule`).
- **Assignee / Người xử lý:** người được phân công xử lý một bước chạy.
- **Requester / Người gửi:** người khởi chạy lượt chạy.
- **Approval step / Bước phê duyệt:** bước có hành động Đồng ý / Từ chối.
- **Execution step / Bước thực hiện:** bước có hành động Chuyển tiếp / Trả về.
- **Recall / Thu hồi:** người gửi rút lại lượt chạy đang xử lý.
- **Reassign / Chuyển giao:** người xử lý giao bước cho người khác.
- **Roles (đã có trong app):** Process Admin, Process Designer, Process User, Process Approver, Process Viewer, System Manager.

## Requirements

### Requirement 1: Khởi chạy quy trình

**User Story:** Là một Process User, tôi muốn khởi chạy một quy trình đã publish bằng cách điền biểu mẫu của bước đầu tiên, để tạo một lượt chạy mới và đưa nó vào luồng xử lý.

#### Acceptance Criteria
1. WHEN người dùng mở danh sách quy trình THEN hệ thống SHALL chỉ hiển thị các `DC Process Template` có status = "Active" mà người dùng có quyền khởi chạy theo cấu hình phân quyền của template.
2. WHEN người dùng chọn một quy trình để khởi chạy THEN hệ thống SHALL hiển thị biểu mẫu của bước đầu tiên dựng theo `form_schema_json` (đúng field type, thứ tự, bắt buộc, điều kiện hiển thị trường).
3. WHILE người dùng nhập liệu IF một trường bắt buộc còn trống hoặc không đạt validation THEN hệ thống SHALL chặn việc gửi và hiển thị thông báo lỗi tại trường tương ứng.
4. WHEN người dùng gửi biểu mẫu hợp lệ THEN hệ thống SHALL tạo một `DC Process Instance` mới với requester = người dùng hiện tại, process_template + process_version tương ứng, status = "Đang xử lý", submitted_at = thời điểm hiện tại, và lưu dữ liệu form vào `form_data_json`.
5. WHEN một lượt chạy được tạo THEN hệ thống SHALL khởi tạo step instance cho (các) bước kế tiếp theo thiết kế và đặt `current_step` trỏ tới bước đang chờ xử lý.
6. IF template được cấu hình `show_first_step_fields_in_next_steps` = true THEN hệ thống SHALL hiển thị (chỉ đọc) dữ liệu bước đầu ở các bước sau.
7. IF người dùng không có quyền khởi chạy quy trình đã chọn THEN hệ thống SHALL từ chối và trả về lỗi quyền (frappe.PermissionError) với thông báo tiếng Việt.

---

### Requirement 2: Phân giải người xử lý (Assignee Resolution)

**User Story:** Là hệ thống, tôi muốn xác định đúng người xử lý cho mỗi bước theo cấu hình của bước, để công việc đến đúng người.

#### Acceptance Criteria
1. WHEN một step instance được kích hoạt THEN hệ thống SHALL phân giải người xử lý theo `assignee_type` của bước.
2. WHERE assignee_type = "Người dùng tự chọn" THE hệ thống SHALL dùng người xử lý mà người gửi (hoặc người ở bước trước) đã chỉ định khi khởi chạy/chuyển bước.
3. WHERE assignee_type = "Theo role" THE hệ thống SHALL phân công bước cho tất cả người dùng có `assignee_role`, và cho phép bất kỳ ai trong nhóm xử lý.
4. WHERE assignee_type = "Theo phòng ban" THE hệ thống SHALL phân công theo `assignee_department` dựa trên cơ cấu tổ chức ERPNext.
5. WHERE assignee_type = "Trưởng phòng" hoặc "Quản lý trực tiếp" THE hệ thống SHALL lấy người quản lý trực tiếp của người gửi/người liên quan từ dữ liệu HR (Employee → reports_to).
6. WHERE assignee_type = "Theo vị trí/chức danh" THE hệ thống SHALL phân công theo job position/designation đã cấu hình.
7. WHERE assignee_type = "Người thực hiện bước trước" THE hệ thống SHALL gán cho người đã hoàn thành bước liền trước.
8. IF không phân giải được người xử lý nào THEN hệ thống SHALL chuyển lượt chạy sang trạng thái cần can thiệp và thông báo cho Process Admin, KHÔNG đặt bước vào trạng thái "không người xử lý" âm thầm.
9. WHEN người xử lý được phân giải THEN hệ thống SHALL tạo bản ghi giao việc (ToDo/assignment) và gửi thông báo cho từng người xử lý.

---

### Requirement 3: Hành động trên bước phê duyệt (Đồng ý / Từ chối)

**User Story:** Là một Process Approver, tôi muốn xem thông tin và đồng ý hoặc từ chối một bước phê duyệt, để quyết định luồng đi tiếp của quy trình.

#### Acceptance Criteria
1. WHEN người xử lý mở một bước phê duyệt THEN hệ thống SHALL hiển thị dữ liệu form (chỉ đọc với trường không thuộc bước này), hộp comment, vùng đính kèm file, và nút "Đồng ý" + "Từ chối".
2. WHEN người xử lý chọn "Đồng ý" THEN hệ thống SHALL đánh dấu step instance là đã duyệt, ghi history (người xử lý, hành động, thời gian, comment), và chuyển sang bước kế tiếp theo flow rule khớp hành động "Đồng ý".
3. WHEN người xử lý chọn "Từ chối" THEN hệ thống SHALL ghi history và áp dụng flow rule của hành động "Từ chối" (có thể trả về bước trước, hoặc kết thúc với status "Từ chối").
4. IF flow rule yêu cầu comment khi từ chối AND comment trống THEN hệ thống SHALL chặn hành động và yêu cầu nhập lý do.
5. IF người thực hiện hành động không nằm trong danh sách người xử lý của bước THEN hệ thống SHALL từ chối hành động với lỗi quyền.
6. WHEN bước phê duyệt được xử lý THEN hệ thống SHALL cập nhật `current_step` và `status` của lượt chạy tương ứng với bước kế tiếp.

---

### Requirement 4: Hành động trên bước thực hiện (Chuyển tiếp / Trả về)

**User Story:** Là một Process User được giao bước thực hiện, tôi muốn nhập/bổ sung thông tin rồi chuyển tiếp hoặc trả về, để hoàn thành phần việc của mình.

#### Acceptance Criteria
1. WHEN người xử lý mở một bước thực hiện THEN hệ thống SHALL hiển thị các trường nhập liệu của bước (editable) và nút "Chuyển tiếp" + "Trả về".
2. WHILE nhập liệu IF trường bắt buộc của bước còn trống hoặc sai validation THEN hệ thống SHALL chặn "Chuyển tiếp" và hiển thị lỗi.
3. WHEN người xử lý "Chuyển tiếp" với dữ liệu hợp lệ THEN hệ thống SHALL gộp dữ liệu vào `form_data_json`, ghi history, và chuyển sang bước kế tiếp theo flow rule.
4. WHEN người xử lý "Trả về" THEN hệ thống SHALL chuyển lượt chạy về bước đích theo flow rule (mặc định bước liền trước), đặt status = "Cần bổ sung", và thông báo cho người xử lý bước đó.
5. WHEN một bước hoàn tất là bước cuối (flow rule trỏ tới END_COMPLETED) THEN hệ thống SHALL đặt status = "Đã hoàn tất" và completed_at = thời điểm hiện tại.

---

### Requirement 5: Rẽ nhánh theo điều kiện (Conditional Branching)

**User Story:** Là người thiết kế quy trình, tôi muốn lượt chạy tự động đi đúng nhánh dựa trên dữ liệu đã nhập, để phản ánh đúng nghiệp vụ.

#### Acceptance Criteria
1. WHEN một bước hoàn tất AND flow rule tương ứng có `condition` THEN hệ thống SHALL đánh giá điều kiện dựa trên `form_data_json`.
2. IF điều kiện đúng THEN hệ thống SHALL chuyển tới `target_step`; IF điều kiện sai THEN hệ thống SHALL chuyển tới `fallback_target_step`.
3. WHERE có nhiều flow rule khớp một hành động THE hệ thống SHALL đánh giá theo `order_index` tăng dần và chọn rule khớp đầu tiên.
4. IF không có flow rule nào khớp THEN hệ thống SHALL dừng lượt chạy ở trạng thái lỗi cấu hình và thông báo Process Admin (không tự ý kết thúc).
5. WHERE flow rule trỏ tới các marker đặc biệt "END_COMPLETED" / "END_REJECTED" THE hệ thống SHALL kết thúc lượt chạy với status tương ứng ("Đã hoàn tất" / "Từ chối").

---

### Requirement 6: Bước song song (Parallel Steps)

**User Story:** Là người thiết kế, tôi muốn nhiều bước chạy đồng thời và chỉ tiếp tục khi tất cả hoàn thành, để xử lý song song nhiều bộ phận.

#### Acceptance Criteria
1. WHEN một bước có `is_parallel` = true được kích hoạt THEN hệ thống SHALL khởi tạo đồng thời tất cả các bước song song trong nhóm và phân giải người xử lý cho từng bước.
2. WHILE các bước song song đang chạy THE hệ thống SHALL cho phép các người xử lý xử lý độc lập, không phụ thuộc thứ tự.
3. WHEN tất cả các bước song song trong nhóm hoàn tất THEN hệ thống SHALL áp dụng quy tắc hội tụ (join) và chuyển sang bước kế tiếp.
4. IF bất kỳ bước song song nào bị "Từ chối" THEN hệ thống SHALL áp dụng flow rule từ chối của nhóm song song (mặc định: dừng và đặt status "Từ chối").

---

### Requirement 7: Thu hồi, chuyển giao và hủy lượt chạy

**User Story:** Là người gửi hoặc người xử lý, tôi muốn thu hồi, chuyển giao hoặc hủy lượt chạy khi cần, để xử lý sai sót hoặc thay đổi người phụ trách.

#### Acceptance Criteria
1. WHILE lượt chạy đang ở trạng thái "Đang xử lý"/"Chờ duyệt" IF người thực hiện là requester THEN hệ thống SHALL cho phép "Thu hồi" lượt chạy, đặt status = "Đã hủy" (hoặc về Draft theo cấu hình), ghi history và thông báo các người xử lý hiện tại.
2. WHEN người xử lý hiện tại chọn "Chuyển giao" và chỉ định người mới THEN hệ thống SHALL chuyển assignment của bước cho người mới, ghi history và thông báo người mới.
3. IF người chuyển giao không phải người xử lý hợp lệ của bước THEN hệ thống SHALL từ chối hành động với lỗi quyền.
4. WHEN người có quyền (requester hoặc Process Admin) chọn "Hủy bỏ" THEN hệ thống SHALL đặt status = "Đã hủy", ghi history, và dừng mọi assignment đang mở.
5. WHERE lượt chạy đã ở trạng thái kết thúc ("Đã hoàn tất"/"Từ chối"/"Đã hủy") THE hệ thống SHALL không cho phép thu hồi/chuyển giao/hủy và hiển thị thông báo phù hợp.

---

### Requirement 8: Lịch sử xử lý và audit trail

**User Story:** Là người liên quan, tôi muốn xem lịch sử đầy đủ của lượt chạy, để biết ai đã làm gì, khi nào.

#### Acceptance Criteria
1. WHEN bất kỳ hành động nào (khởi chạy, đồng ý, từ chối, chuyển tiếp, trả về, comment, đính kèm, thu hồi, chuyển giao, hủy) được thực hiện THEN hệ thống SHALL ghi một bản ghi `DC Process History` gồm: bước, người thực hiện, hành động, thời gian, comment, dữ liệu thay đổi (nếu có).
2. WHEN người dùng mở một lượt chạy THEN hệ thống SHALL hiển thị timeline các bước theo thứ tự thời gian, gồm trạng thái mỗi bước (đang xử lý/đã xong/bị trả về/từ chối).
3. THE hệ thống SHALL không cho phép sửa/xóa bản ghi lịch sử bởi người dùng thông thường (chỉ đọc).
4. WHERE người dùng là Process Viewer THE hệ thống SHALL cho phép xem lịch sử nhưng không thực hiện hành động.

---

### Requirement 9: Deadline và quá hạn

**User Story:** Là người quản lý, tôi muốn theo dõi và được cảnh báo khi bước/lượt chạy quá hạn, để thúc đẩy tiến độ.

#### Acceptance Criteria
1. WHERE một bước cấu hình `deadline_type` khác "Không đặt hạn" THE hệ thống SHALL tính hạn xử lý của step instance dựa trên `deadline_value` kể từ thời điểm bước được kích hoạt.
2. WHILE một bước đang chờ xử lý IF quá hạn THEN hệ thống SHALL đánh dấu bước/lượt chạy là "Quá hạn" và gửi thông báo nhắc cho người xử lý (và quản lý nếu cấu hình escalation).
3. WHEN một tác vụ định kỳ (scheduler) chạy THEN hệ thống SHALL quét các step instance đang mở và cập nhật trạng thái quá hạn tương ứng.
4. THE hệ thống SHALL hiển thị chỉ báo trực quan (màu/nhãn) cho các bước/lượt chạy quá hạn trong danh sách và inbox.

---

### Requirement 10: Thông báo (Notifications)

**User Story:** Là người xử lý, tôi muốn được thông báo khi có việc cần làm hoặc trạng thái thay đổi, để xử lý kịp thời.

#### Acceptance Criteria
1. WHEN một bước được phân công cho người xử lý THEN hệ thống SHALL gửi desk notification và email (nếu bật) cho người xử lý kèm liên kết tới bước cần xử lý.
2. WHEN lượt chạy bị trả về, từ chối, hoàn tất, thu hồi hoặc hủy THEN hệ thống SHALL thông báo cho các bên liên quan tương ứng (requester và/hoặc người xử lý).
3. WHERE cấu hình thông báo bị tắt cho một loại sự kiện THE hệ thống SHALL không gửi thông báo loại đó.
4. IF gửi email thất bại THEN hệ thống SHALL vẫn ghi nhận desk notification và log lỗi, không làm gián đoạn luồng xử lý.

---

### Requirement 11: Inbox "Công việc của tôi" và danh sách lượt chạy

**User Story:** Là người dùng, tôi muốn xem các công việc đang chờ tôi và các lượt chạy liên quan, để biết mình cần làm gì.

#### Acceptance Criteria
1. WHEN người dùng mở inbox THEN hệ thống SHALL hiển thị danh sách các bước đang chờ chính người dùng đó xử lý, sắp xếp theo deadline/ngày tạo.
2. THE hệ thống SHALL cung cấp các bộ lọc: theo quy trình, theo trạng thái, theo khoảng thời gian, theo người gửi.
3. WHEN người dùng mở danh sách lượt chạy THEN hệ thống SHALL hiển thị các lượt chạy mà người dùng là requester, người xử lý, hoặc người liên quan (theo phân quyền).
4. WHERE người dùng là Process Admin/System Manager THE hệ thống SHALL cho phép xem tất cả lượt chạy.
5. WHEN người dùng chọn một mục trong inbox/danh sách THEN hệ thống SHALL mở màn hình xử lý/chi tiết tương ứng.

---

### Requirement 12: Phân quyền runtime

**User Story:** Là quản trị, tôi muốn quyền truy cập runtime tuân theo vai trò, để bảo mật dữ liệu quy trình.

#### Acceptance Criteria
1. THE hệ thống SHALL chỉ cho phép người dùng có một trong các role {System Manager, Process Admin, Process Designer, Process User, Process Approver, Process Viewer} truy cập tính năng runtime.
2. WHERE người dùng là Process Viewer THE hệ thống SHALL chỉ cho phép xem (read-only), không khởi chạy/không xử lý.
3. WHEN người dùng cố thực hiện một hành động trên bước mà họ không phải người xử lý hợp lệ THEN hệ thống SHALL từ chối với frappe.PermissionError và thông báo tiếng Việt.
4. THE mọi endpoint API runtime SHALL kiểm tra quyền trước khi thực thi (không tin tưởng dữ liệu client).

---

### Requirement 13: UI/UX vận hành theo phong cách MISA

**User Story:** Là người dùng, tôi muốn giao diện vận hành quen thuộc như MISA AMIS Quy Trình, để dễ sử dụng.

#### Acceptance Criteria
1. THE màn hình khởi chạy SHALL render biểu mẫu bước đầu theo schema (radio/dropdown/table/date/file/textarea...) với bố cục giống MISA.
2. THE màn hình xử lý task SHALL hiển thị: thông tin lượt chạy, các bước thực hiện (timeline dọc bên trái), form bước hiện tại ở giữa, panel comment/đính kèm/người liên quan bên phải — tương ứng layout MISA.
3. THE timeline các bước SHALL thể hiện trạng thái từng bước bằng số thứ tự + nhãn trạng thái (đang xử lý/đã duyệt/bị trả về...).
4. THE nút hành động (Đồng ý/Từ chối/Chuyển tiếp/Trả về...) SHALL hiển thị phù hợp theo loại bước và quyền của người xử lý.
5. THE toàn bộ nhãn, thông báo và nội dung hiển thị SHALL bằng tiếng Việt.
6. THE giao diện SHALL hoạt động tốt trên desktop và responsive ở mức cơ bản trên màn hình hẹp.

---

### Requirement 14: Dashboard theo dõi

**User Story:** Là lãnh đạo/QA, tôi muốn xem tổng quan tình hình thực hiện quy trình, để phát hiện điểm nghẽn.

#### Acceptance Criteria
1. WHEN người dùng có quyền mở dashboard THEN hệ thống SHALL hiển thị số liệu tổng quan: số lượt chạy theo trạng thái, số bước quá hạn, số lượt chạy đang chờ duyệt.
2. THE dashboard SHALL cho phép lọc theo quy trình và khoảng thời gian.
3. WHERE người dùng không có quyền xem toàn bộ THE dashboard SHALL chỉ tính trên dữ liệu người dùng được phép xem.
