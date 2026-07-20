# HTKK Module — Product Requirements Document (PRD)

> Source: Google Docs (imported 2026-03-13)
> Module: Kê khai thuế tự động trên ERPNext

---

TÀI LIỆU ĐẶC TẢ SẢN PHẨM (PRD)
MODULE ERPNEXT HTKK


Kê khai thuế tự động trên ERPNext


Phiên bản
	3.1
	Ngày
	Tháng 03/2026
	Trạng thái
	Draft – Revised
	Mật độ
	Internal
	

LỊCH SỬ THAY ĐỔI (CHANGE LOG)[1]
Trang này ghi nhận các thay đổi quan trọng qua từng phiên bản PRD, giúp cả team nắm được luồng phát triển tài liệu.


Phiên bản
	Ngày
	Tác giả
	Nội dung thay đổi chính
	v2.0
	03/2026
	—
	Bản gốc: Tổng quan, Kiến trúc, Doctypes, Tính năng cốt lõi, Univer, Công nghệ.
	v2.1
	03/2026
	—
	Thêm: User Stories, Source of Truth, Bảo mật/Phân quyền, Version Control mẫu, Audit Trail, Edge Cases, Benchmark hiệu năng, Testing strategy, Rủi ro, Lộ trình.
	v2.1 rev1
	03/2026
	—
	Named Ranges thay tọa độ cứng (6.1D, 7.1). Tối ưu storage: File Attachment gzip + HTKK Appendix Row (5.3, 6.3). validate_sync() trước Submit (7.8). Lý do KHBS (7.3.1). Nút Compare dữ liệu gốc (7.9).
	v2.2
	03/2026
	—
	Realtime progress cho background job (6.3). Dọn rác File Attachment auto-save (5.3). Cross-check XSD vs Named Ranges khi Save Template (6.1B).
	v2.3
	03/2026
	—
	Auto-detect Indicators (6.1D, 7.1). Quy trình Hybrid. Review + Sidebar + Re-assign. openpyxl. Trang Change Log.
	v2.4
	03/2026
	—
	Confidence score + heuristic (6.1D). Anchor backup (7.1). Incremental Fingerprint (7.8). Optimistic locking (5.3). KHBS 5 lần + 3 năm (7.3). Rollback + Reconciliation + Alerting (7.10). Phase 0 Spike (17). Success Metrics (18). UI/UX Spec 8 màn hình (8).
	v3.0
	03/2026
	—
	Mapping Rule (6.4). Template Package (6.5). UI/UX 10 màn hình (8).
	v3.1
	03/2026
	—
	Loại bỏ Univer. Từ khai chính: HTML/Tailwind form. Phụ lục: ag-Grid Community. State đơn giản hóa. Cập nhật tech stack và UI/UX.
	

Quy ước: Mỗi lần PRD được cập nhật, người sửa cần thêm một dòng mới vào bảng trên, ghi rõ phiên bản, ngày, tác giả, và tóm tắt thay đổi. Đánh số phiên bản theo quy tắc: thay đổi lớn tăng số chính (v3.0), thay đổi nhỏ tăng số phụ (v2.4).
MỤC LỤC


1.  Tổng quan & Bối cảnh
2.  Mục tiêu sản phẩm
3.  Phạm vi & Giới hạn
4.  Đối tượng sử dụng & User Stories
5.  Kiến trúc hệ thống
6.  Các Doctype cốt lõi
7.  Tính năng & Nghiệp vụ chi tiết
8.  Đặc tả Giao diện (UI/UX Specification)
9.  Bảo mật & Phân quyền
10.  Kiểm soát phiên bản mẫu từ khai
11.  Xử lý lỗi & Edge Cases
12.  Audit Trail & Compliance
13.  Hiệu năng & Khả năng mở rộng
14.  Công nghệ sử dụng
15.  Chiến lược kiểm thử
16.  Rủi ro & Giảm thiểu
17.  Lộ trình triển khai
18.  Chỉ số đo lường thành công
19.  Thuật ngữ
1. Tổng quan & Bối cảnh
Hiện tại, các doanh nghiệp sử dụng ERPNext tại Việt Nam phải thực hiện quy trình kê khai thuế bằng cách xuất dữ liệu từ ERPNext, sau đó nhập lại thủ công vào phần mềm HTKK của Tổng cục Thuế. Quy trình này gây ra nhiều vấn đề:
* Sai sót do nhập liệu thủ công, đặc biệt với các từ khai có hàng trăm chỉ tiêu.
* Mất thời gian đối chiếu giữa ERPNext và HTKK mỗi kỳ thuế.
* Không có nguồn dữ liệu duy nhất (single source of truth) cho số liệu thuế.
* Khó truy vết lịch sử và kiểm toán khi cơ quan thuế yêu cầu giải trình.
Module ERPNext HTKK được xây dựng để nội bộ hóa toàn bộ quy trình này, từ việc trích xuất dữ liệu kế toán, hiển thị giao diện từ khai giống hệt Excel, đến xuất file XML chuẩn nộp trực tiếp cho cơ quan thuế.


2. Mục tiêu sản phẩm
2.1 Mục tiêu chính
STT
	Mục tiêu
	Chỉ số đo lường (KPI)
	1
	Tự động hóa trích xuất dữ liệu thuế từ chứng từ kế toán
	Giảm 90% thời gian nhập liệu thủ công
	2
	Cung cấp giao diện bảng tính giống hệt HTKK gốc
	Độ tương đồng layout > 95%
	3
	Xuất XML chuẩn XSD nộp cơ quan thuế
	100% file XML pass validation
	4
	Đảm bảo toàn vẹn dữ liệu sau khi chốt sổ
	0 trường hợp sai lệch sau Submit
	5
	Hỗ trợ đầy đủ nghiệp vụ từ khai bổ sung (KHBS)
	Xử lý đúng 100% từ khai bổ sung
	

2.2 Mục tiêu phụ
* Giảm phụ thuộc vào phần mềm HTKK của Tổng cục Thuế (chỉ hỗ trợ Windows).
* Tạo nền tảng để xây dựng dashboard báo cáo thuế lịch sử.
* Dễ mở rộng khi Tổng cục Thuế thay đổi mẫu từ khai.


3. Phạm vi & Giới hạn
3.1 Trong phạm vi (In Scope)
* Từ khai thuế GTGT mẫu 01/GTGT (TT80/2021) và các phụ lục liên quan.
* Từ khai thuế TNDN (quyết toán năm) và tạm tính quý.
* Từ khai thuế TNCN (khấu trừ tại nguồn, quyết toán).
* Cơ chế từ khai bổ sung (KHBS) cho tất cả các loại từ khai.
* Xuất XML chuẩn XSD và validate trước khi xuất.
* Giao diện HTML/Tailwind + ag-Grid tích hợp trực tiếp trong ERPNext.


3.2 Ngoài phạm vi (Out of Scope)
* Nộp từ khai điện tử trực tiếp qua cổng thuế (iHTKK/eTax) – chỉ xuất file XML.
* Quản lý chữ ký số và xác thực điện tử.
* Tích hợp với hóa đơn điện tử (e-Invoice) – dữ liệu lấy từ chứng từ kế toán đã ghi nhận.
* Các loại thuế đặc thù (thuế tài nguyên, thuế BVMT) – sẽ bổ sung ở các phase sau.


4. Đối tượng sử dụng & User Stories
4.1 Personas
Persona
	Mô tả
	Nhu cầu chính
	Kế toán thuế
	Thao tác định kỳ hàng tháng/quý
	Lấy dữ liệu nhanh, sửa tay khi cần, xuất XML
	Kế toán trưởng
	Duyệt và phê duyệt từ khai
	Kiểm tra số liệu, so sánh, chốt sổ an toàn
	Developer/Implementer
	Cấu hình mẫu từ khai mới
	Upload schema, map chỉ tiêu, viết hàm
	Quản lý/Giám đốc
	Xem tổng quan nghĩa vụ thuế
	Dashboard, báo cáo lịch sử
	

4.2 User Stories tiêu biểu[2]
ID
	Persona
	User Story
	Tiêu chí chấp nhận
	US-01
	KT thuế
	Bấm một nút để hệ thống tự động điền dữ liệu vào từ khai
	Dữ liệu điền đúng ô, ô tự động màu xanh
	US-02
	KT thuế
	Sửa tay một ô và hệ thống đánh dấu rõ
	Ô chuyển vàng, giá trị gốc lưu audit
	US-03
	KT thuế
	Click phải vào ô để xem chứng từ gốc
	Pop-up hiển thị đúng hóa đơn/bút toán
	US-04
	KT trưởng
	Duyệt từ khai và so sánh với dữ liệu gốc
	Nút Compare và validate_sync khi Submit
	US-05
	Developer
	Thêm mẫu từ khai mới với Auto-detect
	Auto-detect > 80% chỉ tiêu, map xong trong < 30 phút
	US-06
	KT thuế
	Làm từ khai bổ sung với lý do KHBS
	Chênh lệch + lý do tự động đúng
	

5. Kiến trúc hệ thống
5.1 Tổng quan kiến trúc
Hệ thống vận hành theo mô hình Dynamic Template & Spreadsheet Engine, gồm 3 lớp chính:
Lớp
	Thành phần
	Vai trò
	Input
	XSD + XML + XLSX (với Named Ranges)
	Developer upload mẫu, hệ thống parse schema
	Processing
	Whitelist Functions + Query Builder
	Lấy dữ liệu, tính toán chỉ tiêu
	Output
	HTML Form + ag-Grid + XML Generator
	Hiển thị, validate và xuất file
	

5.2 Luồng dữ liệu chính
1. Kế toán tạo HTKK Declaration mới, chọn Template và kỳ thuế.
2. Hệ thống render file XLSX gốc bằng Univer, hiển thị đúng layout.
3. Kế toán bấm “Lấy dữ liệu” – Backend gọi Whitelist Functions. Hệ thống lưu data_hash tại thời điểm này.
4. Dữ liệu được đổ vào Univer theo Named Ranges đã map (tĩnh + động).
5. Kế toán kiểm tra, sửa tay nếu cần. Hệ thống auto-save khi có thay đổi.
6. Kế toán trưởng duyệt (nếu bật workflow). Trước khi Submit, hệ thống chạy validate_sync() kiểm tra dữ liệu gốc.
7. Validate bằng xmlschema, xuất XML để nộp.


5.3 Chiến lược lưu trữ (Storage Strategy)[3]
Hệ thống lưu dữ liệu theo chiến lược phân tầng để tối ưu hiệu năng Frappe và tránh bloat database:
Đầu lưu
	Nội dung
	Hình thức
	Vai trò
	Form State (JSON)
	Toàn bộ state của spreadsheet
	File Attachment (.json.gz)
	Source of Truth – dùng để render và xuất XML
	Child Table (HTKK Indicator Value)
	Chỉ các chỉ tiêu tổng hợp (Fixed Nodes)
	Row-based trong Frappe
	Derived data – phục vụ Report/Dashboard
	HTKK Appendix Row (Doctype riêng)
	Dòng chi tiết phụ lục (Repeatable Nodes)
	Background insert, không render UI
	Truy vấn SQL chi tiết hóa đơn
	

Quy ước Source of Truth
* Khi xuất XML: đọc trực tiếp từ Form State (JSON) (what-you-see-is-what-you-export).
* Child Table và Appendix Row chỉ phục vụ reporting – không bao giờ là nguồn cho XML.
* Sync: Mỗi khi Save hoặc Submit, hệ thống extract chỉ tiêu tổng hợp vào Child Table và insert dòng phụ lục vào HTKK Appendix Row qua background job. Nếu sync thất bại, block Submit.


Tối ưu Auto-save
Thay vì lưu toàn bộ JSON State mỗi 30 giây vào MariaDB (gây bloat và nghẽn băng thông), hệ thống áp dụng cơ chế sau:
* Dirty flag: Chỉ trigger auto-save khi có thay đổi thực sự (không save theo timer cứng).
* File Attachment: Form State được compress (gzip) và lưu như File Attachment thay vì trường Long Text trong MariaDB. Giảm áp lực database, dễ backup.
* Dọn rác tự động: Mỗi lần auto-save tạo file .json.gz mới, hệ thống tự động xóa (unlink + delete record File) bản draft ngay trước đó. Luôn chỉ giữ 1 file state hiện tại cho mỗi Declaration. Tránh ổ cứng VPS bị đầy rác qua nhiều kỳ kê khai.
* Client cache: Khi mất kết nối, Form State được cache tạm trong IndexedDB. Khi kết nối lại, so sánh version và hỏi user chọn giữ bản local hay server.
* Optimistic Locking: Mỗi lần save, client gửi kèm version number. Nếu server phát hiện version client < version server (do tab/người khác đã save trước), trả về conflict và hiển thị cảnh báo “Phiên bản đã cũ, vui lòng tải lại”. Tránh race condition khi 2 tab cùng mở 1 Declaration.
* UI trạng thái: Hiển thị rõ “Đã lưu” / “Đang lưu...” / “Mất kết nối – dữ liệu chưa lưu”.


6. Các Doctype cốt lõi
6.1 HTKK Template Manager
Nơi định nghĩa và cấu hình mẫu từ khai mới khi có sự thay đổi từ Tổng cục Thuế.
A. Tab Thông tin chung
Trường
	Kiểu
	Mô tả
	Tên từ khai
	Data
	Ví dụ: Từ khai GTGT mẫu 01/GTGT
	Mã loại (Target ID)
	Data
	Mã định danh duy nhất
	Phiên bản Thông tư
	Data
	Ví dụ: TT80/2021
	Ngày hiệu lực
	Date
	Ngày áp dụng mẫu
	Ngày hết hiệu lực
	Date
	Ngày ngừng áp dụng
	Trạng thái
	Select
	Draft / Active / Deprecated
	

B. Tab Nền tảng (Foundation)
* Upload file: .xml (mẫu dữ liệu), .xsd (luật kiểm tra), .xlsx (layout gốc từ HTKK – không cần chuẩn bị Named Ranges trước).
* Nút “Parse Schema”: Đọc XSD và XML tạo danh sách Fixed Node và Repeatable Node.
* Nút “Auto-detect Indicators”: Quét file .xlsx bằng Regex, tự động sinh Named Ranges cho Fixed Nodes (xem mục 6.1.D và 7.1).
* Cross-check tự động (khi Save Template): Hệ thống so khớp tập hợp “Node cần điền” từ file .xsd với tập hợp “Named Ranges” từ file .xlsx. Nếu Excel thiếu Named Range cho bất kỳ chỉ tiêu nào trong XSD, hệ thống highlight đỏ và chặn Save cho đến khi Developer bổ sung đầy đủ. Điều này ngăn chặn lỗi mapping thiếu từ sớm, trước khi kế toán sử dụng.


C. Tab Nguồn dữ liệu (Data Sources)
Thay vì cấu hình data source trực tiếp trên Template (gắn cứng, khó tái sử dụng), hệ thống sử dụng HTKK Mapping Rule (mục 6.4) với kiến trúc khớp nối lỏng:
* Tab này hiển thị danh sách Mapping Rules đang áp dụng cho loại từ khai này (read-only, liên kết đến Doctype HTKK Mapping Rule).
* Nút “Xem Rules” mở danh sách Mapping Rules lọc theo loại từ khai.
* Nút “Tạo Custom Rule” cho phép nhân bản Standard Rule để tùy chỉnh cho công ty cụ thể.
* Rules không gắn vào phiên bản Template cụ thể mà neo vào Loại từ khai + Named Range — khi Template mới ra, Rules cũ tự động áp dụng.


D. Tab Giao diện (UI Mapping & Auto-Mapping)[4]
Hệ thống sử dụng quy trình Hybrid: tự động nhận diện chỉ tiêu + Developer duyệt và sửa. Developer upload file .xlsx nguyên bản từ HTKK (không cần chuẩn bị Named Ranges trước).


Bước 1 – Upload file thô: Developer upload thẳng file .xlsx tải từ HTKK/Tổng cục Thuế, chưa có Named Range.
Bước 2 – Nút “Auto-detect Indicators”: Backend (openpyxl) quét toàn bộ sheet bằng heuristic đa tầng:
   * Tầng 1 – Regex: Tìm pattern [29], [30a], [01.1], “Chỉ tiêu 29”.
   * Tầng 2 – Context check: Kiểm tra ô có nằm trong vùng chỉ tiêu của sheet không (loại bỏ false positive như “Điều [29] của Luật...”).
   * Tầng 3 – Neighbor validation: Ô bên phải (hoặc offset cấu hình) phải là input cell (trống, không merge lộn).
   * Tầng 4 – Confidence score: Mỗi match được gán điểm tin cậy 0–1.0.
   * Tự động inject Named Range vào ô target trên memory.
Bước 3 – Giao diện Review: Sau khi quét xong:
   * hệ thống render giao diện lên màn hình.
   * Sidebar bên phải liệt kê toàn bộ chỉ tiêu đã nhận diện, màu theo confidence: xanh (> 0.9), vàng (0.7–0.9), đỏ (< 0.7).
   * Batch review mode: Developer duyệt nhanh các chỉ tiêu vàng/đỏ theo nhóm thay vì click từng ô.
   * Click vào dòng trên Sidebar → Univer tự động focus (“nhảy đến”) ô đó để Developer kiểm tra bằng mắt.
   * Chỉ tiêu chưa match được (do merge cell phức tạp) được highlight vàng trên Sidebar.
Bước 4 – Manual Override: Nếu thuật toán nhận diện sai, Developer click chuột phải vào ô đúng trên Univer → Chọn “Re-assign Named Range” → Chọn chỉ tiêu từ dropdown → Mapping cập nhật ngay.
Bước 5 – Vùng lặp thủ công: Riêng Phụ lục có dòng lặp động (Repeatable Range): Developer bôi đen vùng phụ lục trên Univer và gắn tên thủ công (VD: APPENDIX_01_RANGE). Thuật toán không auto-detect phần này vì layout phụ lục quá nhiều biến thể.
Bước 6 – Lưu Template: Cross-check XSD vs Named Ranges (mục 6.1.B), chốt Named Ranges vào file .xlsx và lưu làm bản gốc.


Độ chính xác dự kiến
Thuật toán dò tìm ô trống kế bên text chỉ tiêu sẽ đúng khoảng 80–90% với các từ khai tiêu chuẩn. 10–20% sai sót thường rơi vào bảng biểu lồng ghép/merge cell phức tạp. Vì vậy, bước Review (3) và Manual Override (4) là chốt chặn an toàn bắt buộc, không được bỏ qua.


E. Tab Khởi tạo & Nhân bản
Duplicate Template cũ, giữ mapping hàm và Named Ranges đã được duyệt. Developer chỉ cần upload file .xlsx mới và chạy lại Auto-detect nếu có thay đổi layout.


6.2 HTKK Declaration
Nơi kế toán thao tác hàng tháng/quý. Tuân thủ lifecycle Frappe với bổ sung workflow duyệt và validate_sync.
A. Header
Trường
	Kiểu
	Mô tả
	Công ty
	Link (Company)
	Công ty kê khai
	Mẫu từ khai
	Link (HTKK Template)
	Tự động chọn theo kỳ thuế
	Kỳ thuế
	Select + Date Range
	Tháng/Quý/Năm
	Loại từ khai
	Select
	Lần đầu / Bổ sung (Lần 1, 2...)
	Từ khai gốc
	Link (HTKK Declaration)
	Chỉ hiển khi Bổ sung
	data_hash
	Data (hidden)
	Hash dữ liệu kế toán lúc Lấy dữ liệu
	Trạng thái
	Workflow State
	Draft → Pending → Submitted → Cancelled
	

B. Body (Spreadsheet Workspace)
* Render toàn màn hình bằng Univer. Giao diện y hệt HTKK gốc.
* Màu sắc ô: Xanh (tự động), Vàng (sửa tay), Xám (read-only/công thức).
* Auto-save: Dirty-flag based, lưu dạng File Attachment (xem mục 5.3).


C. Lưu trữ dữ liệu chỉ tiêu
Phân tầng theo độ chi tiết để tránh giới hạn Child Table của Frappe (chậm khi > 1.000 dòng):
* Child Table (HTKK Indicator Value): Chỉ lưu chỉ tiêu tổng hợp của từ khai chính (khoảng 50–100 dòng). Render bình thường trên Frappe form.
* HTKK Appendix Row (Doctype riêng): Lưu hàng nghìn dòng hóa đơn phụ lục. Insert bằng background job (frappe.enqueue), tuyệt đối không render trên form UI. Liên kết với Declaration qua trường Link.


D. Lifecycle & Trạng thái
1. Draft: Kế toán làm việc, lấy dữ liệu, sửa tay.
2. Pending Approval: Gửi duyệt. Hệ thống lưu data_hash tại thời điểm này.
3. Submitted: Trước khi Submit, hệ thống chạy validate_sync() (xem mục 7.8). Khóa toàn bộ.
4. Cancelled: Chỉ khi chưa xuất XML hoặc có quyền đặc biệt.


6.3 HTKK Appendix Row (Mới)[5]
Doctype riêng lưu dòng chi tiết phụ lục, tách biệt khỏi Child Table chính:
Trường
	Kiểu
	Mô tả
	declaration
	Link (HTKK Declaration)
	Liên kết về từ khai cha
	appendix_code
	Data
	Mã phụ lục (VD: PL01_1_GTGT)
	row_index
	Int
	Số thứ tự dòng
	data_json
	Long Text
	JSON chứa toàn bộ cột của dòng
	Dữ liệu được insert bằng frappe.enqueue (background), không render trên UI. Phục vụ truy vấn SQL khi cần báo cáo chi tiết hóa đơn.


Realtime Progress cho Background Job
Vì background job có thể mất vài giây đến vài chục giây với hàng nghìn dòng, cần phản hồi UI rõ ràng để kế toán không vội bấm “Xuất XML” hoặc tắt trình duyệt:
* Sử dụng frappe.publish_realtime để Backend bắn tiến độ (progress %) về frontend qua WebSocket.
* Frontend hiển thị thanh progress bar và lock các nút thao tác (Xuất XML, Submit, Lấy lại dữ liệu) cho đến khi job trả về trạng thái completed.
* Nếu job thất bại: hiển thị thông báo lỗi cụ thể, cho phép Retry.


6.4 HTKK Mapping Rule — Động cơ Ánh xạ Thuế Đa phương thức (Mới)
Doctype trung tâm thay thế việc cấu hình data source trực tiếp trên Template. Mỗi Rule định nghĩa cách lấy dữ liệu cho một chỉ tiêu, với kiến trúc khớp nối lỏng (loose coupling).
Nguyên lý Khớp nối lỏng
Rule không gắn vào phiên bản Template cụ thể (VD: TT80), mà chỉ neo vào 2 yếu tố: Loại từ khai (VD: 01/GTGT) + Mã chỉ tiêu đích (Named Range, VD: CHI_TIEU_29). Khi Tổng cục Thuế ra mẫu Excel mới mà Named Range không đổi, toàn bộ Rules cũ tự động áp dụng mà không cần cấu hình lại.
Cấu trúc Doctype
Trường
	Kiểu
	Mô tả
	declaration_type
	Data
	Loại từ khai (VD: 01/GTGT, 03/TNDN)
	target_named_range
	Data
	Mã chỉ tiêu đích (VD: CHI_TIEU_29)
	rule_type
	Select
	Standard (gốc, không sửa) / Custom (ghi đè)
	source_type
	Select
	condition_builder / sql_builder / python_whitelist
	condition_config
	JSON
	Cấu hình Condition Builder (Doctype, Filters, Aggregate)
	sql_query
	Code
	Câu SQL đã sanitize (chỉ SELECT, whitelist tables)
	whitelist_function
	Data
	Tên hàm Python (VD: custom_app.htkk.api.get_vat_allocation)
	company
	Link (Company)
	Null = áp dụng tất cả, hoặc chỉ định công ty cụ thể
	priority
	Int
	Độ ưu tiên (Custom > Standard)
	is_active
	Check
	Bật/tắt rule
	Đa phương thức lấy dữ liệu (3 cấp độ)
Cấp độ
	Source Type
	Đối tượng
	Mô tả
	No-code
	Condition Builder
	Kế toán
	UI trực quan: chọn Doctype, Filters, Sum field. Hệ thống dịch ra query.
	Low-code
	SQL Builder
	Admin/Implementer
	Viết SQL (chỉ SELECT, sanitized, whitelist tables, timeout 10s, max 10k rows).
	Pro-code
	Python Whitelist
	Developer
	Gọi hàm @whitelist_for_htkk cho nghiệp vụ phân bổ phức tạp.
	Cơ chế Gốc + Ghi đè (Base + Override)
* Standard Rule (Gốc): Bộ quy tắc mặc định do nhà cung cấp đóng gói (chuẩn TT200/133). Kế toán chỉ xem, không sửa. Đảm bảo 80% khách hàng “cắm là chạy”.
* Custom Rule (Ghi đè): Kế toán nhân bản Standard Rule để tự sửa điều kiện lọc (VD: trỏ vào tài khoản con đặc thù), hoặc tạo Rule mới hoàn toàn.
* Thứ tự thực thi: Custom Rule (company-specific) → Custom Rule (global) → Standard Rule → Không có rule → ô để trống (highlight vàng, nhập tay).
* Khi nhà cung cấp update Standard Rule (vì Thuế thay đổi): Custom Rule không bị ghi đè, nhưng hệ thống hiển thị cảnh báo “Standard Rule đã cập nhật, Custom Rule có thể cần review”.


6.5 Template Package Distribution (Mới)
Đóng gói toàn bộ tài nguyên của một mẫu từ khai thành một khối thống nhất để phân phối nhanh cho nhiều công ty/site.
Export Package
Trên HTKK Template Manager, nút “Export Package” tự động gom:
* Meta-data của Template (tên, mã, phiên bản, ngày hiệu lực).
* File đính kèm: .xlsx (đã chốt Named Ranges), .xml, .xsd.
* Bộ Standard Rules đi kèm (HTKK Mapping Rule với rule_type = Standard).
* Nén thành file .htkktpl (zip + metadata header).
Import Package
Tại ERPNext của khách hàng, upload file .htkktpl:
* Hệ thống kiểm tra version compatibility (phiên bản HTKK module của site phải >= phiên bản trong package).
* Tự động khôi phục Template + files + Standard Rules mà không cần chạy lại Auto-detect.
* Custom Rules của khách hàng (nếu có) không bị ghi đè.
* Hiển thị báo cáo import: số Rules mới, số Rules cập nhật, số conflicts.
Định dạng file .htkktpl
Thành phần
	Mô tả
	manifest.json
	Metadata: tên, version, ngày, min_module_version, checksum
	template.json
	Cấu hình Template Manager (serialize)
	rules/*.json
	Từng Standard Rule (mỗi file 1 rule)
	files/
	Thư mục chứa .xlsx, .xml, .xsd
	

7. Tính năng & Nghiệp vụ chi tiết
7.1 Mapping bằng Named Ranges – Quy trình Hybrid[6]
Thay vì yêu cầu Developer chuẩn bị Named Ranges thủ công trên Excel (tốn thời gian và dễ sót), hệ thống tự động hóa bước này với quy trình Hybrid (Tự động + Duyệt):


Quy trình chuẩn bị file & Mapping
1. Lấy file .xlsx gốc từ HTKK hoặc website Tổng cục Thuế. Không cần thao tác gì thêm trên Excel.
2. Tạo HTKK Template mới, upload file .xlsx cùng .xml và .xsd.
3. Nhấn “Auto-detect Indicators”. Backend (openpyxl) quét file và tự động sinh Named Ranges cho các Fixed Nodes bằng Regex + dò ô trống.
4. Developer dùng màn hình Review trên Univer để đối chiếu lướt qua các ô đã map. Sửa lại bằng Re-assign Named Range nếu thuật toán dò sai (thường ở các ô merge phức tạp).
5. Định nghĩa thủ công Vùng lặp (Repeatable Range): Bôi đen vùng phụ lục trên Univer, gắn tên (VD: APPENDIX_01_RANGE). Thuật toán không auto-detect phần này.
6. Nhấn “Lưu Template”. Hệ thống cross-check XSD vs Named Ranges, chốt vào file .xlsx và lưu bản gốc.


So sánh quy trình cũ vs mới


	Quy trình cũ (Thủ công)
	Quy trình mới (Hybrid)
	Developer effort
	Mở Excel, tạo 50–100 Named Ranges tay
	Bấm 1 nút, duyệt + sửa 10–20% sai
	Thời gian
	1–2 giờ/mẫu
	15–30 phút/mẫu
	Độ chính xác
	100% (nếu không sót)
	80–90% auto + review thủ công
	Rủi ro
	Dễ sót Named Range
	Chốt chặn bằng cross-check XSD
	

Runtime: Resolve Named Range + Anchor Backup
Lưu ý kỹ thuật: Named Ranges trong Excel không tự động dịch chuyển khi insert row phía trên range. Do đó, khi Tổng cục Thuế ra mẫu mới có thay đổi layout, Developer cần tạo Template mới (Duplicate + chạy lại Auto-detect).
Để tăng độ tin cậy runtime, hệ thống lưu cả Named Range và Anchor text làm backup:
* Primary: Resolve Named Range → tọa độ ô.
* Fallback: Nếu Named Range resolve thất bại (file bị sửa ngoài hệ thống), dùng Anchor text (“Chỉ tiêu [29]”) + offset để định vị lại.
* Nếu cả hai cách đều resolve khác nhau: cảnh báo Developer kiểm tra Template.


7.2 Lấy dữ liệu tự động
Từ khai chính (Fixed Nodes)
Dữ liệu được điền vào ô thông qua Named Range. VD: Chỉ tiêu [29] map với Named Range “CHI_TIEU_29”, hệ thống resolve ra tọa độ thực tế và điền giá trị.
Phụ lục (Repeatable Nodes)
Backend trả về mảng JSON. ag-Grid hiển thị Rows tại Vùng lặp đã định nghĩa, đẩy dòng phía dưới xuống. Công thức SUM tự động mở rộng range.


7.3 Từ khai bổ sung & KHBS
Nghiệp vụ cốt lõi và phức tạp nhất của module:
1. User chọn “Từ khai bổ sung”, hệ thống copy snapshot từ khai gốc (đã Submit).
2. Kế toán sửa số liệu trên lưới hiện tại.
3. Hệ thống tự động so sánh và phát hiện chênh lệch.
4. Với mỗi chỉ tiêu chênh lệch, hiển thị pop-up yêu cầu kế toán chọn lý do (xem 7.3.1).
5. Tự động điền Phụ lục 01/KHBS với số chênh lệch + lý do.
6. Tính tiền chậm nộp dựa trên số ngày và lãi suất.


7.3.1 Giao diện Map Lý do KHBS[7]
Khi phát hiện chênh lệch, hệ thống hiển thị modal với:
* Danh sách chỉ tiêu thay đổi, giá trị cũ/mới, số chênh lệch.
* Dropdown chọn lý do từ bộ mã chuẩn (sai hóa đơn, sót chứng từ, điều chỉnh giá, khác...).
* Cho phép nhập tự do nếu chọn “Khác” (không bắt buộc chọn từ danh sách đóng).
* Kết quả được tự động điền vào cột “Lý do điều chỉnh” trong Phụ lục 01/KHBS.


Quy tắc chuỗi bổ sung[8]
* Bổ sung lần N so sánh với từ khai gần nhất đã Submit (gốc hoặc N-1).
* Nếu N-1 bị Cancel, tự động tìm bản Submit gần nhất còn hiệu lực.
* Không cho tạo lần N+1 nếu N chưa Submit.
* Giới hạn cứng: Tối đa 5 lần bổ sung cho một kỳ thuế. Vượt quá → yêu cầu liên hệ cơ quan thuế.
* Giới hạn thời gian: Không cho bổ sung nếu đã quá 3 năm kể từ kỳ thuế gốc (theo quy định Luật Quản lý thuế).


7.4 Real-time Calculation
* Công thức có sẵn trong .xlsx được Giao diện render tính tổng tức thời (VD: [40] = [29] - [30]).
* Insert Rows cho phụ lục: SUM tự động mở rộng range.


7.5 Drill-down (Truy xuất nguồn)
Click chuột phải ô số liệu tự động → “Xem chứng từ gốc” → Pop-up danh sách Hóa đơn/Bút toán. Click dòng để mở chứng từ gốc.


7.6 Data Lock (Chốt sổ)
Khi Submit:
* Vô hiệu hóa sửa ô và nút “Lấy lại dữ liệu”.
* Ghi SHA-256 hash của Form State vào Doctype.
* XML xuất ra trùng khớp 100% với dữ liệu lưu.


7.7 Kiểm tra & Kết xuất XML
1. Validate: xmlschema đối soát dữ liệu.
2. Hiển thị lỗi: Highlight đỏ ô không hợp lệ, kèm thông báo cụ thể.
3. Đóng gói XML: Vòng lặp cho Phụ lục, trả file tải xuống.


7.8 Validate Sync – Kiểm tra dữ liệu gốc trước Submit (Mới)[9]
Vấn đề: Sau khi kế toán gửi duyệt (Pending Approval), chứng từ kế toán gốc trong ERPNext có thể bị sửa/hủy. Kế toán trưởng Submit mà không biết dữ liệu đã lệch.
Giải pháp: Cơ chế validate_sync() với Incremental Fingerprint chạy tự động trước Submit:
1. Lúc “Lấy dữ liệu”, hệ thống tính signature riêng cho từng chứng từ (hash của invoice_id + grand_total + modified). Lưu toàn bộ {invoice_id: signature} vào trường data_fingerprint.
2. Khi Submit, hệ thống tính lại signature cho từng chứng từ và so sánh với bản đã lưu.
3. Nếu khác: Hiển thị cảnh báo cụ thể từng chứng từ (VD: “Hóa đơn INV-2024-001 đã bị sửa lúc 14:30”). User chọn: (a) Quay về Draft lấy lại dữ liệu, hoặc (b) Vẫn Submit (ghi nhận rủi ro trong Audit Log).
4. Nếu khớp: Submit bình thường.
Lợi ích so với hash toàn bộ dataset: Thông báo cụ thể chứng từ nào thay đổi (không chỉ “dữ liệu đã lệch” chung chung). Hiệu năng tốt với 10k+ chứng từ.
Lưu ý: Không freeze chứng từ gốc. Chỉ cảnh báo và để user quyết định.


7.9 So sánh với dữ liệu gốc (Compare with Initial Data)[10]
Nút “So sánh với dữ liệu gốc” trên toolbar, dành cho kế toán trưởng khi duyệt:
* Highlight các ô đã bị kế toán sửa khác so với dữ liệu tự động ban đầu.
* Tooltip hiển thị giá trị gốc (từ hàm) vs giá trị hiện tại (sau sửa tay).
* Giúp kế toán trưởng nhanh chóng phát hiện sửa đổi bất thường trước khi phê duyệt.


7.10 Tính năng bổ trợ (Mới)[11]
A. Rollback (Quay lại bản trước)
Mỗi lần Save, hệ thống lưu snapshot Form State với version number. Nút “Quay lại bản trước” cho phép kế toán chọn version cần restore từ danh sách (hiển thị thời gian, user, số ô thay đổi). Giữ tối đa 10 snapshot gần nhất, cũ hơn tự động dọn.
B. Data Reconciliation (So khớp XML đã nộp)
Cho phép import file XML đã nộp cơ quan thuế vào hệ thống để so sánh với dữ liệu trên ERPNext. Hiển thị báo cáo chênh lệch (nếu có) giữa số liệu ERPNext và XML thực tế đã nộp. Hữu ích khi kiểm toán hoặc cơ quan thuế yêu cầu giải trình.
C. Cảnh báo Deadline nộp thuế
Hệ thống tự động cảnh báo (email + notification trong ERPNext) khi gần hạn nộp từ khai. Cấu hình được số ngày cảnh báo trước hạn (mặc định: 7 ngày và 3 ngày). Hiển thị trạng thái các kỳ chưa nộp trên Dashboard.


8. Đặc tả Giao diện (UI/UX Specification)
Mục này mô tả chi tiết layout, thành phần, và hành vi của từng màn hình. File wireframe tương tác (React) được đính kèm PRD để xem trực quan: htkk_wireframes.jsx (8 màn hình).
8.1 Màn hình: Danh sách Từ khai (Declaration List)
Vùng
	Vị trí
	Nội dung
	Header
	Trên cùng
	Tiêu đề “HTKK Declaration” + nút “Tạo từ khai mới” (góc phải)
	Alert bar
	Dưới header
	Cảnh báo deadline nộp thuế (nền vàng, icon ⚠️, đếm ngược ngày)
	Table
	Body
	Cột: Mã | Loại từ khai | Kỳ thuế | Công ty | Trạng thái (badge màu) | Nút Mở
	Filters
	Trên table
	Lọc theo: Công ty, Kỳ, Trạng thái, Loại
	Trạng thái badge: Draft (xanh dương nhạt), Chờ duyệt (vàng), Đã chốt (xanh lá), Đã hủy (đỏ). Click dòng → mở Declaration Workspace.


8.2 Màn hình: Declaration Workspace (Màn hình chính)
Layout full-screen, chia 5 vùng từ trên xuống:
Vùng
	Chiều cao
	Nội dung chi tiết
	1. Header Bar
	~70px
	Trái: Nút quay lại + Mã Declaration + Status badge + Thông tin (loại, kỳ, công ty). Phải: Trạng thái save (đã lưu / đang lưu / mất kết nối)
	2. Action Toolbar
	~40px
	Trái: Lấy dữ liệu | Lấy lại | So sánh DL gốc | Quay lại bản trước. Phải: Validate | Gửi duyệt/Phê duyệt | Xuất XML
	3. Warning Bar
	~35px (tùy)
	Hiển thị khi validate_sync phát hiện lệch. Nền đỏ nhạt, tên chứng từ cụ thể, 2 nút: Quay về Draft / Vẫn Submit
	4. Color Legend
	~25px
	4 ô màu mẫu: Xanh (tự động) | Vàng (sửa tay) | Xám (read-only) | Đỏ (lỗi validation)
	5. Spreadsheet
	Flex (chiếm hết)
	Giao diện render toàn màn hình. Sheet tabs ở đáy: Từ khai | PL01-1 | PL01-2 | PL01-KHBS
	6. Progress Bar
	~25px (đáy)
	Chỉ hiển khi background job đang chạy. Thanh progress + % + mô tả (VD: 2,340/5,000 dòng)
	

Thay đổi theo trạng thái
Trạng thái
	Toolbar
	Spreadsheet
	Đặc biệt
	Draft
	Tất cả nút hoạt động trừ Xuất XML
	Cho phép sửa ô xanh/vàng
	Progress bar hiển thị khi insert phụ lục
	Pending Approval
	Chỉ Phê duyệt + So sánh DL gốc
	Read-only
	Warning bar nếu validate_sync lệch
	Submitted
	Chỉ Xuất XML
	Read-only toàn bộ
	Hiển thị hash SHA-256
	Cancelled
	Không nút nào
	Read-only + mờ nhạt
	Banner đỏ “Đã hủy”
	

Context Menu (Click chuột phải trên ô)
* Ô dữ liệu tự động (xanh): “Xem chứng từ gốc” → mở Drill-down Popup.
* Ô bất kỳ: “Sao chép giá trị”.
* Khi đang ở chế độ So sánh: Tooltip hiển thị “Giá trị gốc: X | Hiện tại: Y” trên các ô vàng.


8.3 Màn hình: Auto-detect Review
Layout chia 2 cột:
Vùng
	Vị trí
	Nội dung
	Header
	Trên cùng
	Tên Template + số chỉ tiêu quét được + Nút: Chạy lại | Lưu Template
	Summary bar
	Dưới header
	3 badge: X xanh (chắc chắn) | Y vàng (cần duyệt) | Z đỏ (có thể sai) | Cross-check XSD status
	Cột trái (70%)
	Body
	Preview HTML form của tờ khai. Click ô được highlight khi chọn từ Sidebar
	Sidebar phải (30%)
	Body
	Danh sách chỉ tiêu: Mã | Ô target | Confidence % | Màu viền trái theo confidence
	

Sidebar chi tiết
* Mỗi dòng: Viền trái màu (xanh/vàng/đỏ) + Mã chỉ tiêu [XX] + Confidence XX% + Tên chỉ tiêu + Ô target.
* Filter tabs: “Tất cả” | “Cần duyệt (Y)” – batch review cho chỉ tiêu vàng/đỏ.
* Click dòng → giao diện focus ô tương ứng (scroll + highlight).
* Dòng có confidence < 0.7: nền hồng nhạt, hiển thị icon cảnh báo.
* Context menu trên Univer: “Re-assign Named Range” → dropdown chọn chỉ tiêu.


8.4 Màn hình: KHBS Lý do Modal
Modal overlay (620px rộng, centered), xuất hiện khi tạo từ khai bổ sung và phát hiện chênh lệch:
Vùng
	Nội dung
	Header
	Tiêu đề “Giải trình KHBS” + thông tin bổ sung lần mấy + nút đóng
	Bảng chênh lệch
	Cột: Chỉ tiêu (mã + tên) | Giá trị cũ | Giá trị mới | Chênh lệch (xanh/đỏ) | Dropdown lý do
	Dropdown lý do
	5 mã chuẩn: Sai hóa đơn | Sót chứng từ | Điều chỉnh giá | Sai thuế suất | Khác (nhập tay)
	Tiền chậm nộp
	Box vàng: Công thức = Số tiền chênh lệch × 0.03%/ngày × Số ngày
	Footer
	Nút Hủy | Nút Xác nhận & Điền vào PL 01/KHBS
	

8.5 Màn hình: Drill-down Popup
Modal overlay (580px), xuất hiện khi click phải ô tự động → “Xem chứng từ gốc”:
* Header: Icon 🔍 + “Chứng từ gốc — Chỉ tiêu [XX]” + Tên chỉ tiêu + Tổng giá trị.
* Danh sách: Mỗi dòng = Mã hóa đơn (link xanh, underline, click mở ERPNext) + Ngày + Đối tác + Số tiền + VAT.
* Footer: Tổng số hóa đơn + hướng dẫn click.


8.6 Màn hình: Template Manager
Giao diện Frappe standard với 4 tab:
Tab
	Nội dung chính
	Thông tin chung
	Form fields: Tên, Mã, Thông tư, Ngày hiệu lực/hết, Trạng thái
	Nền tảng
	3 upload boxes (XML/XSD/XLSX) + 2 nút: Parse Schema | Auto-detect Indicators + Kết quả cross-check
	Nguồn dữ liệu
	Bảng Whitelist Functions (tên hàm, nhóm chỉ tiêu) + Query Builder config (JSON)
	Giao diện & Mapping
	Chuyển sang màn hình Auto-detect Review (8.3) khi click
	

8.7 Color System & Typography
Màu sắc ô Spreadsheet
Loại ô
	Nền
	Viền
	Hex
	Dữ liệu tự động
	Xanh nhạt
	Xanh #2E86C1
	#EBF5FB
	Đã sửa thủ công
	Vàng nhạt
	Vàng #F39C12
	#FEF9E7
	Read-only / Công thức
	Xám nhạt
	Xám #95A5A6
	#F4F6F7
	Lỗi validation
	Đỏ nhạt
	Đỏ #E74C3C
	#FDEDEC
	So sánh (highlight ô khác)
	Tím nhạt
	Tím #8E44AD
	#F5EEF8
	

Status Badge
Trạng thái
	Nền
	Text
	Font
	Draft
	#EBF5FB
	#2E86C1
	11px bold, border-radius 12px
	Chờ duyệt
	#FEF9E7
	#F39C12
	11px bold, border-radius 12px
	Đã chốt
	#EAFAF1
	#27AE60
	11px bold, border-radius 12px
	Đã hủy
	#FDEDEC
	#E74C3C
	11px bold, border-radius 12px
	

Confidence Score (Auto-detect)
Mức
	Màu
	Label
	Hành động
	> 0.9
	Xanh #27AE60
	Chắc chắn
	Tự động chấp nhận, Developer lướt qua
	0.7 – 0.9
	Vàng #F39C12
	Cần duyệt
	Developer kiểm tra, sửa nếu cần
	< 0.7
	Đỏ #E74C3C
	Có thể sai
	Bắt buộc Developer xác nhận/sửa
	

Typography
* Font chính: IBM Plex Sans (hoặc system font fallback).
* Tiêu đề màn hình: 15–18px, bold, #2C3E50.
* Body text: 12–13px, regular, #2C3E50.
* Muted text: 11px, #7F8C8D.
* Spreadsheet cell: 12px, mono-space cho số, right-align.


8.8 Rendering Engine — Hybrid HTML + ag-Grid
Lý do thay đổi từ Univer sang HTML + ag-Grid
File .xlsx gốc của HTKK có merge cell cực kỳ phức tạp (header 3–4 dòng merge lộn xộn, ô chỉ tiêu merge ngang dọc không đều). Spreadsheet engine (Univer/Handsontable) render xấu hoặc phải hack thêm cột giả. Trong khi đó, bản chất từ khai chính là một form có cấu trúc cố định, còn phụ lục mới là bảng dữ liệu lặp thực sự.
Thành phần
	Công nghệ
	Lý do
	Từ khai chính
	HTML/Tailwind CSS
	Layout cố định, pixel-perfect giống bản giấy, dễ color-code từng ô, responsive
	Phụ lục (hóa đơn)
	ag-Grid Community
	Dữ liệu dạng bảng lặp (100–10k dòng), cần sort/filter/virtual scroll
	Tabs chuyển
	Vue component tabs
	Từ khai | PL01-1 | PL01-2 | KHBS
	Công thức tổng
	JavaScript computed
	Tính tức thời khi ô thay đổi (VD: [40] = [29] - [30])
	

HTML Form cho từ khai chính
* Mỗi chỉ tiêu là một input field với id = Named Range code (VD: id='CHI_TIEU_29').
* Layout dùng Tailwind grid/flex tái hiện đúng bố cục từ khai gốc.
* Color-code: class 'bg-blue-50' (tự động), 'bg-yellow-50' (sửa tay), 'bg-gray-100' (read-only), 'bg-red-50' (lỗi).
* Ô read-only (công thức): Dùng computed property, update tức thời khi input thay đổi.
* Click phải ô tự động: Context menu “Xem chứng từ gốc”.


ag-Grid cho phụ lục
* ag-Grid Community (MIT, miễn phí). Virtual scroll cho 10k+ dòng.
* Cột định nghĩa theo cấu trúc phụ lục (từ XSD parsed_nodes).
* Footer row: Tự động tính tổng các cột số.
* Row editable: Kế toán có thể sửa trực tiếp dòng hóa đơn.


Licensing
HTML/Tailwind CSS: MIT. ag-Grid Community: MIT. Không có license trả phí.


Tích hợp kỹ thuật
* Embed trong Frappe Custom Page qua Vue 3.
* Giao tiếp Backend qua frappe.call.
* Context menu: Click phải ô trên HTML form → custom dropdown.


8.9 Màn hình: Mapping Rule Manager
Giao diện quản lý HTKK Mapping Rule, trung tâm điều khiển cách lấy dữ liệu cho mọi chỉ tiêu trên mọi loại từ khai.
A. Danh sách Rules (List View)
Vùng
	Nội dung
	Header
	Tiêu đề “HTKK Mapping Rule” + Filter: Loại từ khai | Source Type | Rule Type | Công ty
	Toolbar
	Nút: Tạo Rule mới | Nhân bản Standard Rule
	Table
	Cột: Chỉ tiêu đích | Loại TK | Source Type (badge màu) | Rule Type (Standard/Custom) | Công ty | Active
	Badge màu Source
	Condition Builder = xanh lá | SQL Builder = cam | Python = tím
	

B. Form Rule chi tiết
Vùng
	Nội dung
	Header
	Mã rule + badge Standard/Custom + toggle Active/Inactive
	Section 1: Đích
	Loại từ khai (dropdown) + Named Range đích (autocomplete từ danh sách XSD)
	Section 2: Nguồn
	Radio chọn Source Type, nội dung thay đổi theo lựa chọn (xem bên dưới)
	Section 3: Phạm vi
	Công ty (null = tất cả) + Priority (số)
	Footer
	Nút Lưu | Test Rule (chạy thử với kỳ mẫu, hiển kết quả) | Xem Standard gốc (nếu là Custom)
	

C. Source Type UI — thay đổi theo lựa chọn
Source Type
	Giao diện hiển thị
	Condition Builder (No-code)
	3 dropdown liên tiếp: (1) Doctype nguồn (VD: Sales Invoice) → (2) Bộ lọc điều kiện: trường + toán tử + giá trị, nút + để thêm điều kiện → (3) Aggregate: Sum/Count/Avg của trường nào. Kế toán không cần viết code.
	SQL Builder (Low-code)
	Code editor với syntax highlighting SQL. Banner cảnh báo: “Chỉ SELECT, timeout 10s, max 10k rows”. Nút “Run Preview” chạy thử và hiển thị kết quả bên dưới.
	Python Whitelist (Pro-code)
	Input tên hàm (autocomplete từ danh sách @whitelist_for_htkk). Hiển thị docstring của hàm + params. Nút “Test” chạy với kỳ mẫu.
	

D. Trải nghiệm Base + Override
* Standard Rule: Form read-only, nền xám nhạt. Nút duy nhất: “Nhân bản thành Custom Rule”.
* Custom Rule: Form editable bình thường. Banner trên cùng: “Ghi đè Standard Rule [tên]” với link xem bản gốc.
* Khi Standard Rule được cập nhật (qua import package): Custom Rule hiển thị badge vàng “Standard đã update, cần review” với nút “Xem thay đổi” (side-by-side diff).
* Ơ màn hình Declaration Workspace, tab Data Sources hiển thị danh sách rules đang áp dụng với badge Standard/Custom và source type màu.


8.10 Màn hình: Template Package Manager
Giao diện xuất/nhập gói Template để phân phối nhanh.
A. Export Package (trên Template Manager)
Vùng
	Nội dung
	Nút trigger
	Nút “Export Package” trên toolbar của HTKK Template Manager (bên cạnh Duplicate)
	Preview modal
	Hiển thị danh sách sẽ đóng gói: Template meta + 3 files + N Standard Rules. Checkbox chọn/bỏ từng rule.
	Progress
	Thanh progress “Đang đóng gói...” + tải file .htkktpl về máy khi xong
	

B. Import Package (màn hình riêng)
Vùng
	Nội dung
	Header
	Tiêu đề “Import Template Package” + Vùng kéo thả file .htkktpl
	Step 1: Upload
	Kéo thả hoặc chọn file. Hệ thống đọc manifest.json, hiển thị: Tên template, version, ngày tạo, số rules
	Step 2: Compatibility
	Kiểm tra version module. Xanh = OK. Đỏ = “Module version quá cũ, cần nâng cấp”
	Step 3: Conflict check
	Bảng: Rule name | Status (Mới / Cập nhật / Conflict). Conflict = Custom Rule đã tồn tại, hiển thị radio: Giữ Custom / Ghi đè
	Step 4: Import
	Nút “Import” + progress bar. Báo cáo kết quả: X mới, Y cập nhật, Z bỏ qua
	

C. Visual Design
* File .htkktpl: Icon tùy chỉnh (hộp quà / package), màu tím để phân biệt với các file khác.
* Import wizard: Dạng step-by-step (1 → 2 → 3 → 4), mỗi step hiển thị rõ kết quả trước khi next.
* Conflict highlight: Dòng conflict nền vàng, radio chọn rõ ràng.


9. Bảo mật & Phân quyền[12]
9.1 Ma trận phân quyền
Quyền
	KT thuế
	KT trưởng
	Developer
	Admin
	Tạo Declaration
	✓
	✓
	✗
	✓
	Lấy dữ liệu
	✓
	✓
	✗
	✓
	Sửa tay ô
	✓
	✓
	✗
	✓
	Gửi duyệt
	✓
	✓
	✗
	✓
	Phê duyệt / Submit
	✗
	✓
	✗
	✓
	Cancel
	✗
	✓ (có đk)
	✗
	✓
	Xuất XML
	✓
	✓
	✗
	✓
	Tạo/Sửa Template
	✗
	✗
	✓
	✓
	Cấu hình Whitelist Fn
	✗
	✗
	✓
	✓
	

9.2 Bảo mật dữ liệu
* Không raw SQL/Python eval trên UI. Mọi truy vấn qua Whitelist Functions hoặc Query Builder.
* Whitelist Functions: decorator @whitelist_for_htkk + kiểm tra quyền user.
* Form State: compress (gzip) + hash integrity check khi lưu.


10. Kiểm soát phiên bản mẫu từ khai
Khi Tổng cục Thuế thay đổi mẫu giữa năm:
1. Mỗi Template có ngày hiệu lực / hết hiệu lực.
2. Tạo Declaration: hệ thống tự chọn Template Active phù hợp kỳ thuế.
3. Không tìm thấy Template: cảnh báo, không cho tạo.
Chuyển giao: Mẫu cũ Deprecated nhưng vẫn cho phép tạo bổ sung cho kỳ đã qua. Template chỉ khóa hoàn toàn khi không còn kỳ cần bổ sung.


11. Xử lý lỗi & Edge Cases[13]
Tình huống
	Xử lý
	Hàm lấy dữ liệu timeout/exception
	Thông báo lỗi, cho Retry. Không để Univer nửa chừng.
	Submit nhưng sync Child Table thất bại
	Block Submit, yêu cầu thử lại.
	XSD validation thất bại
	Highlight đỏ ô lỗi, danh sách chi tiết.
	File XLSX không có Named Ranges
	Cảnh báo Developer, liệt kê chỉ tiêu chưa map.
	XSD yêu cầu chỉ tiêu nhưng XLSX thiếu Named Range
	Cross-check tự động chặn Save, highlight đỏ.
	Background job insert phụ lục chưa xong
	Lock nút thao tác + progress bar qua WebSocket.
	Mất kết nối giữa chừng
	IndexedDB cache + hiển thị trạng thái offline.
	Từ khai bổ sung mà gốc đã Cancel
	Tìm bản Submit gần nhất còn hiệu lực.
	2 người mở cùng Declaration
	Người thứ 2 read-only + cảnh báo.
	Dữ liệu gốc thay đổi sau Pending Approval
	validate_sync() cảnh báo khi Submit (mục 7.8).
	

12. Audit Trail & Compliance[14]
Với tính chất pháp lý của từ khai thuế, cần log chi tiết hơn Frappe Version Log. Tuy nhiên, để tránh log noise (ghi nhận mỗi keystroke), hệ thống log theo sự kiện (event-based):
12.1 HTKK Audit Log
Trường
	Mô tả
	declaration
	Link đến HTKK Declaration
	action
	fetch_data / save / manual_edit / submit / cancel / export_xml / validate_sync_warning
	user
	Ai thực hiện
	timestamp
	Ngày giờ
	changes_diff
	JSON diff: danh sách ô thay đổi so với lần Save trước (cell_ref, old, new)
	reason
	Lý do sửa (bắt buộc với manual_edit)
	state_hash
	SHA-256 của Form State (chỉ ghi khi Save/Submit)
	

12.2 Thời điểm ghi log
* fetch_data: Khi bấm “Lấy dữ liệu”. Ghi nhận data_hash.
* save: Mỗi lần auto-save hoặc Save thủ công. Ghi snapshot diff (danh sách ô thay đổi so với lần save trước).
* manual_edit: Ghi riêng khi user sửa tay ô đã có dữ liệu tự động. Bắt buộc nhập lý do.
* submit / cancel / export_xml: Ghi state_hash đầy đủ.
* validate_sync_warning: Ghi khi Submit phát hiện dữ liệu gốc đã lệch.


12.3 Báo cáo kiểm toán
* Lịch sử thay đổi của một Declaration, lọc theo user/thời gian.
* Đối chiếu hai bản Declaration (lần đầu vs bổ sung).
* XML Export Log: ai, lúc nào, hash file.


13. Hiệu năng & Khả năng mở rộng
13.1 Benchmark yêu cầu
Chỉ số
	Mục tiêu
	Ghi chú
	Render giao diện
	< 3s
	File .xlsx chuẩn Tổng cục Thuế
	Lấy dữ liệu
	< 5s
	1.000 hóa đơn
	Insert 5.000 dòng
	< 10s
	Không giật UI
	Xuất XML
	< 3s
	Bao gồm validate
	Auto-save
	< 1s
	Không block UI, gzip file attachment
	

13.2 Tối ưu
* ag-Grid: Virtual rendering, lazy load tabs, viewport rendering.
* Backend: Cache kết quả hàm trong phiên. HTKK Appendix Row insert bằng background job.
* Storage: Form State lưu File Attachment (gzip), không đổ vào Long Text MariaDB.


14. Công nghệ sử dụng[15]
Thành phần
	Công nghệ
	Ghi chú
	Framework
	Frappe Framework
	Python Backend + Jinja
	Frontend
	Vue 3
	Frappe UI / Custom Page
	Từ khai chính
	HTML/Tailwind CSS
	Form cố định, pixel-perfect layout giống HTKK
	Phụ lục (bảng)
	ag-Grid Community (MIT)
	Virtual scroll, sort/filter, 10k+ rows
	XML Build/Parse
	lxml
	Native C binding
	XML Validate
	xmlschema
	Chuẩn XSD
	Auto-detect
	openpyxl
	Regex quét chỉ tiêu, inject Named Ranges
	Lưu trữ State
	File Attachment (gzip)
	Thay vì Long Text MariaDB
	Lưu trữ Reporting
	Child Table + HTKK Appendix Row
	Phân tầng theo độ chi tiết
	

15. Chiến lược kiểm thử[16]
15.1 Unit Test
* Whitelist Functions: Từng hàm với dữ liệu mẫu.
* Query Builder: Verify SQL an toàn.
* Named Range Resolver: Resolve đúng tọa độ từ tên.
* Auto-detect Indicators: Độ chính xác Regex trên 5+ mẫu từ khai chuẩn (target > 80%).
* XML Generator: Output pass XSD.
* validate_sync(): Phát hiện đúng khi dữ liệu gốc thay đổi.


15.2 Integration Test
* End-to-end: Tạo → Lấy dữ liệu → Sửa tay → Submit → XML.
* KHBS: Gốc → Submit → Bổ sung → Lý do → Verify.
* validate_sync: Sửa chứng từ gốc sau Pending → Verify cảnh báo.
* Version: Chuyển giữa hai Template.


15.3 Parallel Validation (Gold Standard)
Cùng dữ liệu đầu vào, so XML output của module với HTKK gốc. Mục tiêu: 100% match giá trị (cho phép khác whitespace).


15.4 Performance Test
* Load: 5.000 dòng phụ lục trên 4GB RAM.
* Concurrent: 10 user, 10 Declaration.
* Storage: Verify gzip file attachment < 500KB cho từ khai trung bình.


16. Rủi ro & Giảm thiểu[17]
Rủi ro
	Mức độ
	Giảm thiểu
	Univer thay đổi license
	TB
	Abstract layer. Dữ liệu độc lập engine.
	Thuế thay mẫu gấp
	Cao
	Named Ranges + Duplicate Template nhanh.
	Hiệu năng dữ liệu lớn
	TB
	Benchmark sớm. Lazy load + background insert.
	Sai lệch Univer vs Child Table
	Cao
	Source of truth rõ. Block Submit khi sync fail.
	Bảo mật Backend Functions
	Cao
	Whitelist + decorator + kiểm tra quyền.
	User sửa tay nhầm
	Thấp
	Highlight vàng + lý do + Compare button.
	Dữ liệu gốc lệch sau duyệt
	Cao
	validate_sync() trước Submit.
	Bloat database do auto-save
	TB
	Gzip File Attachment + dirty-flag + dọn rác tự động.
	

17. Lộ trình triển khai[18]
Phase
	Nội dung
	Thời gian
	Go/No-go gate
	Phase 0: Spike
	Validate HTML render + Auto-detect accuracy trên 3 mẫu thực
	2 tuần
	Accuracy > 85% hoặc pivot
	Phase 1: MVP
	1 mẫu GTGT, 1 công ty, Mapping Rule (Condition Builder), end-to-end
	6 tuần
	Xuất XML đúng với dữ liệu thực
	Phase 2: Hardening
	KHBS + validate_sync + Audit log + SQL/Python source types
	4 tuần
	Security audit pass
	Phase 3: Scale
	Multi-template + Multi-company + Template Package + Base+Override
	4 tuần
	5 công ty, 3 mẫu, import .htkktpl OK
	Phase 4: Polish
	Alerting, Dashboard, Performance tuning, Parallel Test, UAT
	4 tuần
	< 3s mọi operation
	Tổng: 20 tuần. Mỗi phase có go/no-go gate rõ ràng. Nếu Phase 0 Spike thất bại (Univer không render được file HTKK hoặc auto-detect quá kém), pivot sớm trước khi đầu tư nhiều.


18. Chỉ số đo lường thành công (Success Metrics)[19]
18.1 Business Metrics
Metric
	Mô tả
	Target
	Time-to-declare
	Từ lúc tạo Declaration đến Submit
	< 30 phút
	Error-rate
	% từ khai bị cơ quan thuế reject
	< 1%
	Manual-correction-rate
	% ô bị sửa tay so với tổng ô tự động
	< 5%
	

18.2 Technical Metrics
Metric
	Mô tả
	Target
	Auto-detect Precision
	TP / (TP + FP) – trong số ô auto-detect, bao nhiêu đúng
	> 85%
	Auto-detect Recall
	TP / (TP + FN) – bao nhiêu chỉ tiêu được tìm thấy
	> 90%
	Sync false-positive
	% validate_sync báo động nhầm
	< 2%
	Render time
	Thời gian Univer load file
	< 3s
	XML export time
	Bao gồm validate
	< 3s
	

18.3 Adoption Metrics
Metric
	Mô tả
	Target
	Active users
	Số KTT sử dụng liên tục > 3 tháng
	80% KTT công ty triển khai
	Declarations/month
	Số từ khai tạo thành công mỗi tháng
	Theo số kỳ thuế thực tế
	HTKK bypass rate
	% kỳ vẫn phải dùng HTKK gốc
	< 5% sau 6 tháng
	

19. Thuật ngữ
Thuật ngữ
	Định nghĩa
	HTKK
	Hỗ trợ kê khai – Phần mềm Tổng cục Thuế VN
	KHBS
	Khai bổ sung – Từ khai điều chỉnh sau nộp lần đầu
	XSD
	XML Schema Definition – Luật kiểm tra XML
	Univer
	Engine bảng tính mã nguồn mở
	Named Range
	Vùng được đặt tên trong Excel, dùng thay tọa độ cứng
	Auto-detect Indicators
	Thuật toán Regex quét file Excel tự sinh Named Ranges
	Fixed Node
	Chỉ tiêu tĩnh (1 giá trị)
	Repeatable Node
	Chỉ tiêu động (nhiều dòng)
	Whitelist Function
	Hàm Backend đăng ký an toàn
	Mapping Rule
	Quy tắc ánh xạ dữ liệu cho chỉ tiêu, khớp nối lỏng
	Condition Builder
	Giao diện no-code cấu hình lấy dữ liệu cho Kế toán
	Standard Rule
	Rule mặc định do nhà cung cấp, không sửa
	Custom Rule
	Rule ghi đè do khách hàng tự tạo
	.htkktpl
	File đóng gói Template + Rules + files để phân phối
	validate_sync()
	Hàm kiểm tra dữ liệu gốc còn khớp không trước Submit
	data_hash
	SHA-256 của dataset kế toán tại thời điểm lấy dữ liệu
	Drill-down
	Truy xuất nguồn gốc con số đến chứng từ
	

— Hết tài liệu —
________________
[1][v2.3] Thêm mới: Trang Change Log.
[2][v2.1] Thêm mới: User Stories, Personas, tiêu chí chấp nhận.
[3][v2.1] Thêm mới. [v2.1-rev1] File Attachment gzip. [v2.2] Dọn rác. [v2.4] Thêm Optimistic Locking.
[4][v2.1-rev1] Named Ranges. [v2.2] Cross-check XSD. [v2.3] Auto-detect Hybrid. [v2.4] Thêm confidence score + heuristic đa tầng + batch review.
[5][v2.1-rev1] Thêm HTKK Appendix Row tách khỏi Child Table. [v2.2] Thêm Realtime Progress qua WebSocket.
[6][v2.3] Quy trình Hybrid. [v2.4] Sửa Named Ranges runtime + Anchor backup. Thêm so sánh quy trình.
[7][v2.1-rev1] Thêm mới: Giao diện Map Lý do KHBS với dropdown mã chuẩn + nhập tự do.
[8][v2.4] Thêm mới: Giới hạn 5 lần bổ sung + 3 năm.
[9][v2.1-rev1] Thêm validate_sync() với data_hash. [v2.4] Nâng cấp Incremental Fingerprint (hash từng chứng từ).
[10][v2.1-rev1] Thêm mới: Nút So sánh với dữ liệu gốc cho kế toán trưởng duyệt.
[11][v2.4] Thêm mới: Rollback, Data Reconciliation, Cảnh báo deadline.
[12][v2.1] Thêm mới: Ma trận phân quyền 4 role.
[13][v2.1] Thêm mới. [v2.2] Thêm edge case: XSD thiếu Named Range, Background job chưa xong, Dữ liệu gốc lệch sau Pending.
[14][v2.1] Thêm mới. [v2.1-rev1] Chuyển sang event-based logging thay vì log từng keystroke.
[15][v2.1] Thêm mới. [v2.3] Cập nhật: openpyxl, Auto-detect Indicators.
[16][v2.1] Thêm mới. [v2.3] Thêm: auto-detect accuracy test, validate_sync test.
[17][v2.1] Thêm mới. [v2.2] Thêm: bloat auto-save, dữ liệu gốc lệch. [v2.3] Cập nhật Named Ranges risk.
[18][v2.1] Thêm mới. [v2.3] Auto-detect. [v2.4] Chuyển sang Risk-driven với Phase 0 Spike + go/no-go gates.
[19][v2.4] Thêm mới: Business, Technical, Adoption metrics.