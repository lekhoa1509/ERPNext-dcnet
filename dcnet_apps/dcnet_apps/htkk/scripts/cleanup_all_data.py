"""
Script để xóa toàn bộ dữ liệu HTKK trong database.
Chạy: bench --site flow.local execute dcnet_apps.htkk.scripts.cleanup_all_data.run
"""

import frappe


def run():
    """Xóa toàn bộ dữ liệu HTKK để xây dựng lại từ đầu."""

    print("=" * 60)
    print("XÓA TOÀN BỘ DỮ LIỆU HTKK")
    print("=" * 60)

    # Danh sách DocType cần xóa (theo thứ tự: child tables trước)
    doctypes = [
        "HTKK Declaration CT Value",       # Child table
        "HTKK Declaration Adjustment",     # Child table
        "HTKK Declaration",                # Parent (sau khi xóa child)
    ]

    total_deleted = 0

    for doctype in doctypes:
        try:
            # Đếm số record trước khi xóa
            count = frappe.db.count(doctype)
            if count > 0:
                # Xóa trực tiếp qua SQL để nhanh hơn và tránh hooks
                # Using parameterized delete via frappe.db.delete
                frappe.db.delete(doctype)
                print(f"✓ Đã xóa {count} records từ {doctype}")
                total_deleted += count
            else:
                print(f"○ {doctype}: không có dữ liệu")
        except Exception as e:
            print(f"✗ Lỗi khi xóa {doctype}: {str(e)}")

    # Xóa các file đính kèm liên quan
    try:
        attached_files = frappe.get_all(
            "File",
            filters={
                "attached_to_doctype": "HTKK Declaration",
            },
            pluck="name",
        )
        for file_name in attached_files:
            frappe.delete_doc("File", file_name, force=True)
        if attached_files:
            print(f"✓ Đã xóa {len(attached_files)} file đính kèm")
    except Exception as e:
        print(f"✗ Lỗi khi xóa file đính kèm: {str(e)}")

    frappe.db.commit()

    print("=" * 60)
    print(f"HOÀN TẤT: Đã xóa tổng cộng {total_deleted} records")
    print("=" * 60)
