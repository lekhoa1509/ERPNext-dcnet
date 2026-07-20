import json
import os
import re

import frappe
import requests
from frappe import _

from dcnet_migrate.import_auto.services.utils import truncate_text


def analyze_with_ai(doc, summary: dict, hint: dict, schema: dict | None, user_feedback: str | None = None) -> dict | None:
    config = _get_ai_config(doc)
    if not config.api_key or not config.enabled:
        return None

    feedback_note = (user_feedback or "").strip()
    system_prompt = (
        "Bạn là chuyên gia phân tích file Excel kế toán Việt Nam (MISA ERP) để import vào ERPNext v16.\n"
        "Trả về STRICT JSON only — không kèm markdown, không text ngoài JSON.\n"
        "Chỉ dùng fieldname ERPNext có thực. Nếu file không có DocType tương ứng an toàn → safety_status='Error'.\n"
        "Chỉ nhận tối đa 10 sample rows — dùng để nhận diện DocType, header row, field mapping.\n"
        "KHÔNG import dữ liệu. KHÔNG liệt kê toàn bộ records.\n\n"
        "NHẬN DIỆN FILE MISA — ĐẶC TRƯNG CỘT:\n"
        "• Danh sách khách hàng (Customer):\n"
        "  Mã KH/Mã đối tượng → customer_id (unique_key)\n"
        "  Tên KH/Tên đối tượng → customer_name\n"
        "  MST/Mã số thuế → tax_id\n"
        "  Địa chỉ → address_line1 (tạo Address con)\n"
        "  SĐT/Điện thoại → phone (tạo Contact con)\n"
        "  Email → email_id (Contact)\n"
        "  Nhóm KH → customer_group\n"
        "  Loại KH: 'Company'/'Individual' → customer_type\n"
        "• Danh sách nhà cung cấp (Supplier):\n"
        "  Mã NCC → supplier_id (unique_key)\n"
        "  Tên NCC → supplier_name\n"
        "  MST → tax_id\n"
        "  Nhóm NCC → supplier_group\n"
        "• Danh sách hàng hóa (Item):\n"
        "  Mã hàng → item_code (unique_key)\n"
        "  Tên hàng/Tên hàng hóa → item_name\n"
        "  ĐVT/Đơn vị tính → stock_uom\n"
        "  Nhóm hàng/Nhóm VTHH → item_group\n"
        "  Mã vạch → barcode (Item Barcode child)\n"
        "• Danh sách nhân viên (Employee):\n"
        "  Mã NV → employee_number (unique_key)\n"
        "  Tên NV/Họ và tên → employee_name\n"
        "  Phòng ban → department\n"
        "  Chức vụ/Chức danh → designation\n"
        "• Danh sách kho (Warehouse):\n"
        "  Mã kho → warehouse_name (unique_key)\n"
        "  Tên kho → warehouse_name\n"
        "• Hệ thống tài khoản / Danh mục tài khoản (Account) — CÂY TÀI KHOẢN:\n"
        "  QUAN TRỌNG: KHÔNG dùng field 'account_category' — field này KHÔNG TỒN TẠI trong ERPNext.\n"
        "  Số TK/Mã TK → account_number (unique_key)\n"
        "  Tên tài khoản → account_name\n"
        "  Tài khoản cha (parent) → parent_account (format: 'SốTK TênTK - CôngTy', VD: '111 Tiền mặt - DCNET')\n"
        "  Loại (nhóm/chi tiết) → is_group (1 nếu có TK con, 0 nếu TK lá)\n"
        "  Dư Nợ/Dư Có → balance_must_be ('Debit' hoặc 'Credit')\n"
        "  account_type: chỉ dùng 1 trong các giá trị: 'Cash','Bank','Receivable','Payable','Stock','Tax',\n"
        "    'Fixed Asset','Depreciation','Expense Account','Income Account','Equity','Temporary' — hoặc bỏ trống.\n"
        "  KHÔNG import parent accounts trước — ERPNext tự tạo cây từ parent_account field.\n"
        "  Ví dụ row đúng: {account_number:'1111', account_name:'Tiền Việt Nam', parent_account:'111 Tiền mặt - DCNET', is_group:0, balance_must_be:'Debit'}\n\n"
        "QUY TẮC CHUNG:\n"
        "• Bỏ qua hàng tổng cộng: 'Tổng', 'Tổng cộng', 'Cộng', 'Total', dòng header phụ.\n"
        "• Số điện thoại VN: loại bỏ ký tự thừa, chuẩn hóa về 10 số.\n"
        "• Với Customer/Supplier: tạo multi-step — step 1 tạo master, step 2 tạo Address, step 3 tạo Contact.\n"
        "• header_row: MISA thường có 2-4 dòng tiêu đề trước header thực. Header thực = dòng đầu tiên có >3 ô có giá trị cụ thể là tên cột.\n"
        "• unique_key: luôn dùng Mã (Mã KH, Mã NCC, Mã hàng) — KHÔNG dùng tên vì có thể trùng.\n"
        "• ignore_duplicates: true cho tất cả steps để import nhiều lần an toàn.\n"
    )
    if feedback_note:
        system_prompt += (
            "\nNGƯỜI DÙNG CÓ PHẢN HỒI CỤ THỂ CHO FILE NÀY — ưu tiên cao nhất:\n"
            "Áp dụng phản hồi trước, sau đó mới áp dụng các quy tắc chung.\n"
        )

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": truncate_text(
                json.dumps(
                    {
                        "required_json_schema": {
                            "safety_status": "Safe or Error",
                            "target_doctype": "ERPNext DocType name or null",
                            "import_order": "integer order; dependencies first",
                            "confidence": "0-100 number",
                            "sheet_name": "sheet to import",
                            "header_row_number": "1-based header row number",
                            "mappings": [
                                {
                                    "source_column": "Excel header",
                                    "target_field": "ERPNext fieldname",
                                    "default": None,
                                    "transform": "direct or short transform note",
                                }
                            ],
                            "defaults": {"fieldname": "value"},
                            "reason": "Vietnamese reason shown to user",
                        },
                        "context": {
                            "company": doc.company,
                            "hint": hint,
                            "erpnext_schema": schema,
                            "user_feedback": (user_feedback or "").strip() or None,
                        },
                        "workbook_summary": summary,
                    },
                    ensure_ascii=False,
                    default=str,
                ),
                max_length=26000,
            ),
        },
    ]

    response = _chat_completion(config.api_base_url, config.model, config.api_key, messages, int(config.timeout_seconds or 60))
    return _parse_json_response(response)


def verify_slot_mapping(doc, summary: dict, target_doctype: str, mappings: list[dict], defaults: dict) -> dict | None:
    """AI second-opinion pass over a slot's deterministic column mapping.

    Master-data slots (see services/slot_import.py) skip AI DocType detection
    entirely — the target DocType is already fixed by the slot the user
    uploaded into. This function does NOT re-decide the DocType; it only asks
    the AI to sanity-check the column->field mapping heuristic_analysis()
    already produced from the fixed IMPORT_COLUMN_MAPPINGS table, catching a
    mismapped or missing column before the row gets marked "Ready" to import.
    Returns None (caller keeps the heuristic result as-is) if AI is not
    configured or the call fails — this is a best-effort extra check, not a
    hard requirement for the slot upload to work.
    """
    config = _get_ai_config(doc)
    if not config.api_key or not config.enabled:
        return None

    system_prompt = (
        "Bạn là chuyên gia kiểm tra lại (QA) mapping cột Excel sang ERPNext DocType.\n"
        "Mapping dưới đây đã được tạo bằng heuristic cố định (không phải bạn tạo) — "
        "DocType đích ĐÃ CỐ ĐỊNH, KHÔNG được đề xuất đổi DocType.\n"
        "Chỉ đánh giá: mapping cột nguồn -> field ERPNext có đúng nghĩa không, "
        "có cột quan trọng nào bị map sai hoặc bị bỏ sót không.\n"
        "Trả về STRICT JSON only — không kèm markdown, không text ngoài JSON.\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": truncate_text(
                json.dumps(
                    {
                        "required_json_schema": {
                            "ok": "true nếu mapping ổn, false nếu có vấn đề cần cảnh báo",
                            "issues": ["Vietnamese: mô tả ngắn từng vấn đề phát hiện được"],
                            "confidence": "0-100 — độ tin tưởng vào đánh giá này",
                        },
                        "target_doctype": target_doctype,
                        "proposed_mappings": mappings,
                        "defaults": defaults,
                        "workbook_summary": summary,
                    },
                    ensure_ascii=False,
                    default=str,
                ),
                max_length=20000,
            ),
        },
    ]

    try:
        response = _chat_completion(
            config.api_base_url, config.model, config.api_key, messages, int(config.timeout_seconds or 60)
        )
        return _parse_json_response(response)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Import Auto Slot Mapping Verify Failed")
        return None


def test_connection(doc) -> dict:
    config = _get_ai_config(doc)
    if not config.api_key:
        frappe.throw(_("AI API key is not configured."))

    response = _chat_completion(
        config.api_base_url,
        config.model,
        config.api_key,
        [
            {"role": "system", "content": "Return only JSON."},
            {"role": "user", "content": "{\"ok\": true}"},
        ],
        int(config.timeout_seconds or 60),
    )
    return {"ok": True, "response": response[:300]}


def _chat_completion(base_url: str, model: str, api_key: str, messages: list[dict], timeout: int) -> str:
    try:
        response = requests.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={"model": model, "messages": messages, "temperature": 0.1, "stream": False},
            timeout=timeout,
        )
        response.raise_for_status()
        return _extract_chat_content(response)
    except requests.Timeout:
        frappe.throw(_("AI endpoint timed out. Please try again."))
    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else "unknown"
        frappe.log_error(title="Import Auto HTTP Error", message=f"HTTP {status_code} from AI endpoint")
        frappe.throw(_("AI endpoint returned an error. Check API settings."))
    except (KeyError, IndexError, ValueError):
        frappe.log_error(frappe.get_traceback(), "Import Auto Invalid AI Response")
        frappe.throw(_("AI endpoint returned an invalid response. Check model and streaming settings."))
    except requests.RequestException:
        frappe.log_error(frappe.get_traceback(), "Import Auto Connection Error")
        frappe.throw(_("Could not connect to AI endpoint."))


def _extract_chat_content(response: requests.Response) -> str:
    content_type = response.headers.get("content-type", "")
    text = response.text or ""

    if "text/event-stream" in content_type or text.lstrip().startswith("data:"):
        return _extract_sse_chat_content(text)

    payload = response.json()
    choices = payload.get("choices") or []
    if not choices:
        frappe.throw(_("AI response did not include choices."))

    choice = choices[0]
    message = choice.get("message") or {}
    if message.get("content") is not None:
        return message.get("content") or ""

    delta = choice.get("delta") or {}
    if delta.get("content") is not None:
        return delta.get("content") or ""

    if choice.get("text") is not None:
        return choice.get("text") or ""

    frappe.throw(_("AI response did not include message content."))


def _extract_sse_chat_content(text: str) -> str:
    chunks = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue

        data = line[5:].strip()
        if not data or data == "[DONE]":
            continue

        payload = json.loads(data)
        for choice in payload.get("choices") or []:
            delta = choice.get("delta") or {}
            message = choice.get("message") or {}
            content = delta.get("content") or message.get("content") or choice.get("text")
            if content:
                chunks.append(content)

    if not chunks:
        frappe.throw(_("AI streaming response did not include message content."))

    return "".join(chunks)


def _parse_json_response(content: str) -> dict:
    content = (content or "").strip()
    if not content:
        frappe.throw(_("AI response was empty."))
    if content.startswith("```"):
        content = re.sub(r"^```[a-zA-Z]*\s*", "", content)
        content = re.sub(r"\s*```$", "", content).strip()

    candidates = [content]
    extracted = _extract_json_candidate(content)
    if extracted and extracted not in candidates:
        candidates.append(extracted)

    repaired_candidates = []
    for candidate in candidates:
        repaired = re.sub(r",(\s*[}\]])", r"\1", candidate)
        if repaired != candidate:
            repaired_candidates.append(repaired)
    candidates.extend(repaired_candidates)

    last_error = None
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as exc:
            last_error = exc
            continue

    if last_error:
        raise last_error
    return json.loads(content)


def _extract_json_candidate(content: str) -> str | None:
    """Extract the first balanced JSON object/array from an AI response."""
    start_positions = [pos for pos in (content.find("{"), content.find("[")) if pos != -1]
    if not start_positions:
        return None
    start = min(start_positions)
    opener = content[start]
    closer = "}" if opener == "{" else "]"
    depth = 0
    in_str = False
    escape = False
    for index in range(start, len(content)):
        char = content[index]
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if char == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return content[start:index + 1]
    return content[start:]


def _get_ai_config(doc) -> frappe._dict:
    config = frappe._dict(
        enabled=True,
        api_base_url="",
        model="",
        api_key=None,
        timeout_seconds=60,
    )

    if frappe.db.exists("DocType", "Import Auto Settings"):
        settings = frappe.get_single("Import Auto Settings")
        config.api_base_url = settings.api_base_url or ""
        config.enabled = bool(settings.enabled and config.api_base_url)
        config.model = settings.model or ""
        config.timeout_seconds = settings.timeout_seconds or 60
        config.api_key = settings.get_password("api_key")

    if not config.api_key and doc and doc.meta.has_field("api_key"):
        config.api_key = doc.get_password("api_key")

    if doc:
        if doc.get("api_base_url"):
            config.api_base_url = doc.api_base_url
        if doc.get("model"):
            config.model = doc.model
        if doc.get("timeout_seconds"):
            config.timeout_seconds = doc.timeout_seconds

    config.api_key = (
        config.api_key
        or frappe.conf.get("import_auto_api_key")
        or os.environ.get("IMPORT_AUTO_API_KEY")
    )
    return config
