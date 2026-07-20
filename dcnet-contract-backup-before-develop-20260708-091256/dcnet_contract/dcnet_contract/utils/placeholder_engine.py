"""Dual-language placeholder engine for DCNet Contract templates.

Supports both English keys ({{customer_name}}) and Vietnamese labels
({{Tên khách hàng}}) resolving to the same value. Provides validation,
typo detection via unidecode normalization, and bilingual guide generation.
"""

import re

from unidecode import unidecode

# ---------------------------------------------------------------------------
# Dual-language placeholder map
# Keys are English identifiers. Each entry has: vi label, source path,
# example value, and display group for the placeholder guide.
# ---------------------------------------------------------------------------
PLACEHOLDER_MAP = {
    # --- Bên A (Khách hàng) ---
    "customer_name": {
        "vi": "Tên khách hàng",
        "source": "contract.customer_name",
        "example": "Công ty TNHH ABC",
        "group": "Bên A (Khách hàng)",
    },
    "customer_address": {
        "vi": "Địa chỉ khách hàng",
        "source": "contract.customer_address",
        "example": "123 Nguyễn Huệ, Q.1, TP.HCM",
        "group": "Bên A (Khách hàng)",
    },
    "customer_phone": {
        "vi": "Số điện thoại KH",
        "source": "contract.customer_phone",
        "example": "028 1234 5678",
        "group": "Bên A (Khách hàng)",
    },
    "customer_fax": {
        "vi": "Số fax KH",
        "source": "contract.customer_fax",
        "example": "028 1234 5679",
        "group": "Bên A (Khách hàng)",
    },
    "customer_tax_id": {
        "vi": "Mã số thuế KH",
        "source": "contract.customer_tax_id",
        "example": "0123456789",
        "group": "Bên A (Khách hàng)",
    },
    "customer_representative": {
        "vi": "Người đại diện KH",
        "source": "contract.customer_representative",
        "example": "Nguyễn Văn A",
        "group": "Bên A (Khách hàng)",
    },
    "customer_representative_title": {
        "vi": "Chức vụ người đại diện KH",
        "source": "contract.customer_representative_title",
        "example": "Giám đốc",
        "group": "Bên A (Khách hàng)",
    },
    "customer_id_number": {
        "vi": "Số CMND/CCCD",
        "source": "contract.customer_id_number",
        "example": "079123456789",
        "group": "Bên A (Khách hàng)",
    },
    "customer_id_date": {
        "vi": "Ngày cấp CMND",
        "source": "contract.customer_id_date",
        "example": "ngày 15 tháng 03 năm 2020",
        "group": "Bên A (Khách hàng)",
    },
    "customer_id_place": {
        "vi": "Nơi cấp CMND",
        "source": "contract.customer_id_place",
        "example": "Cục CS QLHC về TTXH",
        "group": "Bên A (Khách hàng)",
    },
    "customer_dob": {
        "vi": "Ngày sinh KH",
        "source": "contract.customer_dob",
        "example": "ngày 01 tháng 01 năm 1990",
        "group": "Bên A (Khách hàng)",
    },
    "customer_email": {
        "vi": "Email KH",
        "source": "contract.customer_email",
        "example": "contact@abc.com.vn",
        "group": "Bên A (Khách hàng)",
    },
    "customer_bank_account": {
        "vi": "Tài khoản ngân hàng KH",
        "source": "contract.customer_bank_account",
        "example": "1234567890 - Vietcombank",
        "group": "Bên A (Khách hàng)",
    },
    # --- Bên B (Công ty) ---
    "company_name_b": {
        "vi": "Tên Bên B",
        "source": "Company.company_name",
        "example": "Công ty Cổ phần Viễn thông DCNet",
        "group": "Bên B (Công ty)",
    },
    "company_address_b": {
        "vi": "Địa chỉ Bên B",
        "source": "Company.address",
        "example": "456 Lê Lợi, Q.1, TP.HCM",
        "group": "Bên B (Công ty)",
    },
    "company_phone_b": {
        "vi": "Điện thoại Bên B",
        "source": "Company.phone_no",
        "example": "028 9876 5432",
        "group": "Bên B (Công ty)",
    },
    "company_fax_b": {
        "vi": "Fax Bên B",
        "source": "Company.fax",
        "example": "028 9876 5433",
        "group": "Bên B (Công ty)",
    },
    "company_tax_id_b": {
        "vi": "Mã số thuế Bên B",
        "source": "Company.tax_id",
        "example": "0301234567",
        "group": "Bên B (Công ty)",
    },
    "company_representative_b": {
        "vi": "Người đại diện Bên B",
        "source": "contract.company_representative / Company.representative",
        "example": "Trần Văn B",
        "group": "Bên B (Công ty)",
    },
    "company_representative_title_b": {
        "vi": "Chức vụ người đại diện Bên B",
        "source": "contract.company_representative_title / Company.representative_title",
        "example": "Tổng Giám đốc",
        "group": "Bên B (Công ty)",
    },
    "company_bank_account_b": {
        "vi": "Tài khoản ngân hàng Bên B",
        "source": "Bank Account (default, company)",
        "example": "9876543210",
        "group": "Bên B (Công ty)",
    },
    "company_bank_b": {
        "vi": "Ngân hàng Bên B",
        "source": "Bank Account.bank",
        "example": "BIDV - CN Sài Gòn",
        "group": "Bên B (Công ty)",
    },
    # --- Hợp đồng ---
    "contract_number": {
        "vi": "Số hợp đồng",
        "source": "contract.contract_no_external or contract.name",
        "example": "DCNET/2026/001",
        "group": "Hợp đồng",
    },
    "contract_date": {
        "vi": "Ngày ký hợp đồng",
        "source": "contract.contract_date",
        "example": "ngày 15 tháng 04 năm 2026",
        "group": "Hợp đồng",
    },
    "package_term": {
        "vi": "Thời hạn hợp đồng",
        "source": "contract.package_term_months",
        "example": "12",
        "group": "Hợp đồng",
    },
    "acceptance_date": {
        "vi": "Ngày nghiệm thu",
        "source": "contract.acceptance_date",
        "example": "ngày 20 tháng 04 năm 2026",
        "group": "Hợp đồng",
    },
    "end_date": {
        "vi": "Ngày kết thúc",
        "source": "contract.end_date",
        "example": "ngày 19 tháng 04 năm 2027",
        "group": "Hợp đồng",
    },
    # --- Dịch vụ ---
    "service_type": {
        "vi": "Loại dịch vụ",
        "source": "contract.service_type",
        "example": "FTTH DN",
        "group": "Dịch vụ",
    },
    "package_name": {
        "vi": "Tên gói cước",
        "source": "contract.package_name",
        "example": "FTTH-100M",
        "group": "Dịch vụ",
    },
    "installation_address": {
        "vi": "Địa chỉ lắp đặt",
        "source": "contract.installation_address",
        "example": "Tầng 5, Tòa nhà ABC, Q.1, TP.HCM",
        "group": "Dịch vụ",
    },
    "bandwidth": {
        "vi": "Băng thông",
        "source": "contract.bandwidth",
        "example": "100 Mbps",
        "group": "Dịch vụ",
    },
    "point_a": {
        "vi": "Điểm đầu",
        "source": "contract.point_a",
        "example": "POP Nguyễn Huệ",
        "group": "Dịch vụ",
    },
    "point_b": {
        "vi": "Điểm cuối",
        "source": "contract.point_b",
        "example": "Tòa nhà ABC, Q.1",
        "group": "Dịch vụ",
    },
    "sla_restore_hours": {
        "vi": "SLA khắc phục sự cố",
        "source": "contract.sla_restore_hours",
        "example": "4",
        "group": "Dịch vụ",
    },
    # --- Tài chính ---
    "setup_fee": {
        "vi": "Phí lắp đặt",
        "source": "contract.setup_fee",
        "example": "3,000,000",
        "group": "Tài chính",
    },
    "setup_fee_vat": {
        "vi": "VAT phí lắp đặt",
        "source": "setup_fee * 10%",
        "example": "300,000",
        "group": "Tài chính",
    },
    "setup_fee_total": {
        "vi": "Tổng phí lắp đặt",
        "source": "setup_fee * 110%",
        "example": "3,300,000",
        "group": "Tài chính",
    },
    "setup_fee_words": {
        "vi": "Phí lắp đặt bằng chữ",
        "source": "number_to_words(setup_fee_total)",
        "example": "Ba triệu ba trăm nghìn đồng",
        "group": "Tài chính",
    },
    "monthly_fee": {
        "vi": "Phí hàng tháng",
        "source": "contract.unit_price_total",
        "example": "5,000,000",
        "group": "Tài chính",
    },
    "monthly_fee_vat": {
        "vi": "VAT phí hàng tháng",
        "source": "monthly_fee * 10%",
        "example": "500,000",
        "group": "Tài chính",
    },
    "monthly_fee_total": {
        "vi": "Tổng phí hàng tháng",
        "source": "monthly_fee * 110%",
        "example": "5,500,000",
        "group": "Tài chính",
    },
    "monthly_fee_words": {
        "vi": "Phí hàng tháng bằng chữ",
        "source": "number_to_words(monthly_fee_total)",
        "example": "Năm triệu năm trăm nghìn đồng",
        "group": "Tài chính",
    },
    # --- Hạng mục (items table) ---
    "item_stt": {
        "vi": "STT",
        "source": "row index",
        "example": "1",
        "group": "Hạng mục",
    },
    "item_label": {
        "vi": "Tên hạng mục",
        "source": "item.item_label",
        "example": "Dịch vụ Internet FTTH",
        "group": "Hạng mục",
    },
    "item_qty": {
        "vi": "Số lượng",
        "source": "item.qty",
        "example": "1",
        "group": "Hạng mục",
    },
    "item_uom": {
        "vi": "Đơn vị",
        "source": "item.uom",
        "example": "Nos",
        "group": "Hạng mục",
    },
    "item_price": {
        "vi": "Đơn giá",
        "source": "item.unit_price",
        "example": "5,000,000",
        "group": "Hạng mục",
    },
    "item_amount": {
        "vi": "Thành tiền",
        "source": "item.amount_per_period",
        "example": "5,000,000",
        "group": "Hạng mục",
    },
}

# Auto-build reverse lookup: Vietnamese label → English key
VI_TO_KEY = {v["vi"]: k for k, v in PLACEHOLDER_MAP.items()}

# Pre-compute normalized (unidecode) lookup for typo detection
_NORMALIZED_VI = {unidecode(v["vi"]).lower(): k for k, v in PLACEHOLDER_MAP.items()}
_NORMALIZED_EN = {unidecode(k).lower(): k for k in PLACEHOLDER_MAP}

# Regex for extracting {{...}} placeholders from HTML/text
_PLACEHOLDER_RE = re.compile(r"\{\{([^}]+)\}\}")


def resolve_placeholder(raw_key: str) -> str | None:
    """Resolve a placeholder key (EN or VI) to its canonical English key.

    Returns None if not found in either language.
    """
    key = raw_key.strip()
    if key in PLACEHOLDER_MAP:
        return key
    if key in VI_TO_KEY:
        return VI_TO_KEY[key]
    return None


def detect_typo(raw_key: str) -> dict | None:
    """Detect if raw_key is a diacritics-stripped version of a known placeholder.

    Uses unidecode normalization: "Ten khach hang" → "ten khach hang"
    matches against normalized "Tên khách hàng" → "ten khach hang".

    Returns {"suggested_key": str, "suggested_vi": str} or None.
    """
    key = raw_key.strip()
    # Skip if it's already a valid key
    if key in PLACEHOLDER_MAP or key in VI_TO_KEY:
        return None

    normalized = unidecode(key).lower()

    # Check against normalized Vietnamese labels
    if normalized in _NORMALIZED_VI:
        en_key = _NORMALIZED_VI[normalized]
        return {"suggested_key": en_key, "suggested_vi": PLACEHOLDER_MAP[en_key]["vi"]}

    # Check against normalized English keys
    if normalized in _NORMALIZED_EN:
        en_key = _NORMALIZED_EN[normalized]
        return {"suggested_key": en_key, "suggested_vi": PLACEHOLDER_MAP[en_key]["vi"]}

    return None


def extract_placeholders_from_html(html: str) -> list[str]:
    """Extract all {{...}} placeholder raw keys from HTML content."""
    return _PLACEHOLDER_RE.findall(html)


def validate_template_placeholders(
    html_content: str,
    previous_version_placeholders: list[str] | None = None,
) -> list[dict]:
    """Validate all placeholders in HTML template content.

    Returns list of dicts with keys: key, status, suggestion, context_line.
    Status: matched | typo | unknown | removed
    """
    raw_keys = extract_placeholders_from_html(html_content)
    results = []
    seen_keys = set()

    for raw in raw_keys:
        raw = raw.strip()
        resolved = resolve_placeholder(raw)
        if resolved:
            seen_keys.add(resolved)
            results.append({
                "key": resolved,
                "raw": raw,
                "status": "matched",
                "suggestion": None,
            })
            continue

        typo = detect_typo(raw)
        if typo:
            seen_keys.add(typo["suggested_key"])
            results.append({
                "key": raw,
                "raw": raw,
                "status": "typo",
                "suggestion": typo["suggested_vi"],
                "suggested_key": typo["suggested_key"],
            })
            continue

        results.append({
            "key": raw,
            "raw": raw,
            "status": "unknown",
            "suggestion": None,
        })

    # Check for removed placeholders vs previous version
    if previous_version_placeholders:
        for prev_key in previous_version_placeholders:
            canonical = resolve_placeholder(prev_key)
            check_key = canonical or prev_key
            if check_key not in seen_keys:
                results.append({
                    "key": check_key,
                    "raw": check_key,
                    "status": "removed",
                    "suggestion": None,
                })

    return results


def generate_placeholder_guide_html(placeholder_keys: list[str]) -> str:
    """Generate bilingual HTML table showing placeholder info grouped by category."""
    # Group by category
    groups: dict[str, list[str]] = {}
    for key in placeholder_keys:
        if key not in PLACEHOLDER_MAP:
            continue
        info = PLACEHOLDER_MAP[key]
        group = info["group"]
        groups.setdefault(group, []).append(key)

    # Render HTML table
    rows = []
    for group_name in [
        "Bên A (Khách hàng)", "Bên B (Công ty)", "Hợp đồng",
        "Dịch vụ", "Tài chính", "Hạng mục",
    ]:
        keys_in_group = groups.get(group_name, [])
        if not keys_in_group:
            continue
        rows.append(
            f'<tr><td colspan="5" style="background:#e8e8e8;font-weight:bold;">'
            f"{group_name}</td></tr>"
        )
        for key in keys_in_group:
            info = PLACEHOLDER_MAP[key]
            rows.append(
                f"<tr>"
                f"<td><code>{{{{{key}}}}}</code></td>"
                f"<td><code>{{{{{info['vi']}}}}}</code></td>"
                f"<td>{info['source']}</td>"
                f"<td>{info['example']}</td>"
                f"</tr>"
            )

    header = (
        "<table class='table table-bordered table-sm'>"
        "<thead><tr>"
        "<th>Key (EN)</th><th>Label (VI)</th>"
        "<th>Source</th><th>Example</th>"
        "</tr></thead><tbody>"
    )
    return header + "\n".join(rows) + "</tbody></table>"
