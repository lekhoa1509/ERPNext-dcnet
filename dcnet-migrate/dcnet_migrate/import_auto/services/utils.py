import hashlib
import os
from pathlib import Path

import frappe
from frappe import _


EXCEL_EXTENSIONS = {".xlsx", ".xls", ".csv"}
FINGERPRINT_CHUNK_SIZE = 1024 * 1024


def _candidate_paths(raw: Path) -> list[Path]:
    if raw.is_absolute():
        return [raw]
    return [
        Path(frappe.get_site_path()) / raw,
        Path.cwd() / raw,
        Path(frappe.get_app_path("dcnet_migrate")).parents[1] / raw,
        Path(frappe.get_app_path("dcnet_migrate")).parents[2] / raw,
    ]


def _resolve_existing_path(path_text: str) -> Path:
    raw = Path(os.path.expandvars(os.path.expanduser(path_text)))
    candidates = _candidate_paths(raw)
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    checked = "\n".join(str(candidate) for candidate in candidates)
    frappe.throw(_("Path not found. Checked:\n{0}").format(checked))


def resolve_folder_path(folder_path: str) -> str:
    """Resolve a folder path (must be a directory). Kept for backward compatibility."""
    if not folder_path:
        frappe.throw(_("Folder Import is required."))
    resolved = _resolve_existing_path(folder_path)
    if not resolved.is_dir():
        frappe.throw(_("Expected a folder, got a file: {0}").format(resolved))
    return str(resolved)


def resolve_input_path(input_path: str) -> Path:
    """Resolve a path that may be either a folder or an Excel file."""
    if not input_path:
        frappe.throw(_("Đường dẫn nhập là bắt buộc."))
    return _resolve_existing_path(input_path)


def parse_file_patterns(file_pattern: str | None) -> list[str]:
    patterns = [part.strip() for part in (file_pattern or "*.xlsx,*.xls").split(",")]
    return [pattern for pattern in patterns if pattern]


def _is_valid_excel(file_path: Path) -> bool:
    if file_path.name.startswith("~$"):
        return False
    return file_path.suffix.lower() in EXCEL_EXTENSIONS


def _split_input_entries(input_path: str) -> list[str]:
    """Split a free-form input into multiple path entries.

    Accepts newline- and semicolon-separated paths so users can paste
    a folder, a single file, or a list of files. Commas are NOT used as
    separators because filenames/folders may contain commas.
    """
    if not input_path:
        return []
    normalized = input_path.replace("\r", "\n").replace(";", "\n")
    entries = []
    for line in normalized.split("\n"):
        text = line.strip()
        if text:
            entries.append(text)
    return entries


def scan_excel_files(folder_path: str, file_pattern: str | None, recursive: bool = True) -> list[str]:
    """Discover Excel files from any of: a folder, a single file, or a list of files.

    The ``folder_path`` argument keeps its name for backward compatibility but
    now also accepts:
      - an absolute/relative path to a single ``.xlsx``/``.xls`` file
      - a newline- or semicolon-separated list of file/folder paths
      - a folder path (original behavior, ``file_pattern`` applies)
    """
    entries = _split_input_entries(folder_path or "")
    if not entries:
        frappe.throw(_("Đường dẫn nhập là bắt buộc."))

    patterns = parse_file_patterns(file_pattern)
    files: list[Path] = []
    for entry in entries:
        resolved = resolve_input_path(entry)
        if resolved.is_dir():
            for pattern in patterns:
                matches = resolved.rglob(pattern) if recursive else resolved.glob(pattern)
                files.extend(matches)
        elif resolved.is_file():
            if not _is_valid_excel(resolved):
                frappe.throw(
                    _("Tệp không phải Excel hoặc CSV (.xlsx/.xls/.csv): {0}").format(resolved)
                )
            files.append(resolved)
        else:
            frappe.throw(_("Đường dẫn không hợp lệ: {0}").format(resolved))

    unique_files: list[str] = []
    seen: set[str] = set()
    for file_path in sorted(files):
        if not _is_valid_excel(file_path):
            continue
        resolved_str = str(file_path.resolve())
        if resolved_str in seen:
            continue
        unique_files.append(resolved_str)
        seen.add(resolved_str)
    return unique_files


def file_sha256(file_path: str) -> str:
    digest = hashlib.sha256()
    with open(file_path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_fingerprint(file_path: str) -> str:
    """Return a fast content fingerprint for cache invalidation.

    Full SHA256 over multi-GB Excel files makes every scan expensive. For the
    import workflow we only need a stable "changed or not" key, so combine
    file metadata with first/last chunks.
    """
    path = Path(file_path)
    stat = path.stat()
    digest = hashlib.sha256()
    digest.update(str(stat.st_size).encode())
    digest.update(str(stat.st_mtime_ns).encode())

    with path.open("rb") as handle:
        first = handle.read(FINGERPRINT_CHUNK_SIZE)
        digest.update(first)
        if stat.st_size > FINGERPRINT_CHUNK_SIZE:
            handle.seek(max(stat.st_size - FINGERPRINT_CHUNK_SIZE, 0))
            digest.update(handle.read(FINGERPRINT_CHUNK_SIZE))

    return f"fp:{digest.hexdigest()}"


GROUP_LINK_CONFIG: dict[str, dict] = {
    "Customer Group": {
        "label_field": "customer_group_name",
        "parent_field": "parent_customer_group",
        "root": "All Customer Groups",
    },
    "Supplier Group": {
        "label_field": "supplier_group_name",
        "parent_field": "parent_supplier_group",
        "root": "All Supplier Groups",
    },
    "Item Group": {
        "label_field": "item_group_name",
        "parent_field": "parent_item_group",
        "root": "All Item Groups",
    },
    "Territory": {
        "label_field": "territory_name",
        "parent_field": "parent_territory",
        "root": "All Territories",
    },
}


def normalize_key(value) -> str:
    text = frappe.as_unicode(value or "").strip().lower()
    replacements = {
        "_": " ",
        "-": " ",
        "\u00a0": " ",
        "/": " ",
        ",": " ",
        ".": " ",
        "(": " ",
        ")": " ",
        "%": " ",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return " ".join(text.split())


def truncate_text(value: str | None, max_length: int = 6000) -> str:
    text = frappe.as_unicode(value or "")
    if len(text) <= max_length:
        return text
    return text[:max_length] + "\n...[truncated]"
