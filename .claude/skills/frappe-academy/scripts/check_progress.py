"""
Frappe Academy - Learning Progress Checker
==========================================

Check which exercises and modules have been completed in the frappe_learn app.

Usage (inside container):
    bench --site flow.local execute frappe_learn.scripts.check_progress.run

Or if placed in frappe_learn app:
    bench --site flow.local execute frappe_learn.frappe_learn.scripts.check_progress.run

Can also be run standalone for file-system checks:
    python3 check_progress.py --app-path /workspace/development/frappe-bench/apps/frappe_learn
"""

import frappe
import os
import sys


# ============================================================
# Configuration
# ============================================================

APP_NAME = "frappe_learn"
BENCH_PATH = "/workspace/development/frappe-bench"
APP_PATH = os.path.join(BENCH_PATH, "apps", APP_NAME)
MODULE_PATH = os.path.join(APP_PATH, APP_NAME, "library")

# Define what to check for each module
MODULES = {
    "Module 1-2: App Setup": {
        "checks": [
            ("app_installed", "frappe_learn app installed"),
            ("file_exists", "hooks.py exists", f"{APP_PATH}/{APP_NAME}/hooks.py"),
            ("file_exists", "modules.txt exists", f"{APP_PATH}/{APP_NAME}/modules.txt"),
        ]
    },
    "Module 3-4: DocTypes": {
        "checks": [
            ("doctype_exists", "Book DocType", "Book"),
            ("doctype_exists", "Library Member DocType", "Library Member"),
            ("doctype_exists", "Library Transaction DocType", "Library Transaction"),
            ("has_records", "Book has records", "Book"),
            ("has_records", "Library Member has records", "Library Member"),
            ("has_records", "Library Transaction has records", "Library Transaction"),
        ]
    },
    "Module 5: API & Database": {
        "checks": [
            ("file_exists", "api.py exists", f"{MODULE_PATH}/../api.py"),
            ("function_exists", "get_book_availability API", f"{APP_NAME}.{APP_NAME}.api", "get_book_availability"),
            ("function_exists", "search_books API", f"{APP_NAME}.{APP_NAME}.api", "search_books"),
            ("function_exists", "borrow_book API", f"{APP_NAME}.{APP_NAME}.api", "borrow_book"),
            ("function_exists", "get_member_stats API", f"{APP_NAME}.{APP_NAME}.api", "get_member_stats"),
        ]
    },
    "Module 6: Desk UI": {
        "checks": [
            ("file_exists", "Book form JS (book.js)", f"{MODULE_PATH}/doctype/book/book.js"),
            ("file_exists", "Book list JS (book_list.js)", f"{MODULE_PATH}/doctype/book/book_list.js"),
            ("dir_exists", "Overdue Books Report", f"{MODULE_PATH}/report/library_overdue_books"),
            ("file_exists", "Overdue Report .py", f"{MODULE_PATH}/report/library_overdue_books/library_overdue_books.py"),
            ("file_exists", "Overdue Report .js", f"{MODULE_PATH}/report/library_overdue_books/library_overdue_books.js"),
            ("number_card_exists", "Total Books Number Card", "Total Books"),
            ("number_card_exists", "Active Members Number Card", "Active Library Members"),
            ("number_card_exists", "Borrowed Books Number Card", "Books Currently Borrowed"),
            ("workspace_exists", "Library Workspace", "Library"),
        ]
    },
    "Module 7: Advanced": {
        "checks": [
            ("role_exists", "Librarian role", "Librarian"),
            ("role_exists", "Library Member Role", "Library Member Role"),
            ("role_exists", "Library Admin role", "Library Admin"),
            ("dir_exists", "Library Receipt Print Format", f"{MODULE_PATH}/print_format/library_receipt"),
            ("file_exists", "Print Format HTML", f"{MODULE_PATH}/print_format/library_receipt/library_receipt.html"),
            ("file_exists", "Book tests", f"{MODULE_PATH}/doctype/book/test_book.py"),
            ("file_exists", "Book controller", f"{MODULE_PATH}/doctype/book/book.py"),
            ("dir_exists", "Fixtures directory", f"{APP_PATH}/{APP_NAME}/fixtures"),
            ("hooks_has", "Fixtures in hooks.py", "fixtures"),
        ]
    },
    "Module 8: ERPNext (Capstone)": {
        "checks": [
            ("custom_field_exists", "Item rental_available field", "Item", "custom_rental_available"),
            ("custom_field_exists", "Item rental_rate field", "Item", "custom_rental_rate"),
            ("doctype_exists", "Equipment Rental DocType", "Equipment Rental"),
            ("file_exists", "Equipment Rental controller", f"{MODULE_PATH}/doctype/equipment_rental/equipment_rental.py"),
            ("file_exists", "Equipment Rental JS", f"{MODULE_PATH}/doctype/equipment_rental/equipment_rental.js"),
            ("file_exists", "Equipment Rental tests", f"{MODULE_PATH}/doctype/equipment_rental/test_equipment_rental.py"),
            ("dir_exists", "Rental Revenue Report", f"{MODULE_PATH}/report/rental_revenue"),
            ("number_card_exists", "Active Rentals Number Card", "Active Rentals"),
            ("number_card_exists", "Total Revenue Number Card", "Total Rental Revenue"),
        ]
    },
}


# ============================================================
# Check Functions
# ============================================================

def check_app_installed(app_name):
    """Check if an app is installed."""
    try:
        installed_apps = frappe.get_installed_apps()
        return app_name in installed_apps
    except Exception:
        return False


def check_file_exists(path):
    """Check if a file exists."""
    # Normalize path
    path = os.path.normpath(path)
    return os.path.isfile(path)


def check_dir_exists(path):
    """Check if a directory exists."""
    path = os.path.normpath(path)
    return os.path.isdir(path)


def check_doctype_exists(doctype_name):
    """Check if a DocType exists in the database."""
    try:
        return bool(frappe.db.exists("DocType", doctype_name))
    except Exception:
        return False


def check_has_records(doctype_name):
    """Check if a DocType has at least one record."""
    try:
        count = frappe.db.count(doctype_name)
        return count > 0
    except Exception:
        return False


def check_function_exists(module_path, function_name):
    """Check if a Python function exists and is importable."""
    try:
        module = frappe.get_module(module_path)
        return hasattr(module, function_name)
    except Exception:
        return False


def check_number_card_exists(name):
    """Check if a Number Card exists."""
    try:
        return bool(frappe.db.exists("Number Card", name))
    except Exception:
        return False


def check_workspace_exists(name):
    """Check if a Workspace exists."""
    try:
        return bool(frappe.db.exists("Workspace", name))
    except Exception:
        return False


def check_role_exists(name):
    """Check if a Role exists."""
    try:
        return bool(frappe.db.exists("Role", name))
    except Exception:
        return False


def check_custom_field_exists(doctype, fieldname):
    """Check if a Custom Field exists on a DocType."""
    try:
        cf_name = f"{doctype}-{fieldname}"
        return bool(frappe.db.exists("Custom Field", cf_name))
    except Exception:
        return False


def check_hooks_has(keyword):
    """Check if hooks.py contains a specific keyword."""
    hooks_path = os.path.join(APP_PATH, APP_NAME, "hooks.py")
    try:
        with open(hooks_path, "r") as f:
            content = f.read()
        return keyword in content
    except Exception:
        return False


# ============================================================
# Runner
# ============================================================

def run_check(check_type, label, *args):
    """Run a single check and return (passed, label, details)."""
    try:
        if check_type == "app_installed":
            passed = check_app_installed(APP_NAME)
        elif check_type == "file_exists":
            passed = check_file_exists(args[0])
        elif check_type == "dir_exists":
            passed = check_dir_exists(args[0])
        elif check_type == "doctype_exists":
            passed = check_doctype_exists(args[0])
        elif check_type == "has_records":
            passed = check_has_records(args[0])
        elif check_type == "function_exists":
            passed = check_function_exists(args[0], args[1])
        elif check_type == "number_card_exists":
            passed = check_number_card_exists(args[0])
        elif check_type == "workspace_exists":
            passed = check_workspace_exists(args[0])
        elif check_type == "role_exists":
            passed = check_role_exists(args[0])
        elif check_type == "custom_field_exists":
            passed = check_custom_field_exists(args[0], args[1])
        elif check_type == "hooks_has":
            passed = check_hooks_has(args[0])
        else:
            return False, label, f"Unknown check type: {check_type}"

        return passed, label, ""
    except Exception as e:
        return False, label, str(e)


def run():
    """Check Frappe Academy learning progress and print a formatted report."""
    print("")
    print("=" * 70)
    print("  FRAPPE ACADEMY - LEARNING PROGRESS REPORT")
    print("  Báo cáo tiến độ học tập Frappe Academy")
    print("=" * 70)
    print("")

    total_checks = 0
    total_passed = 0
    module_results = {}

    for module_name, module_config in MODULES.items():
        checks = module_config["checks"]
        module_passed = 0
        module_total = len(checks)
        results = []

        for check_def in checks:
            check_type = check_def[0]
            label = check_def[1]
            args = check_def[2:]

            passed, label, error = run_check(check_type, label, *args)
            results.append((passed, label, error))

            if passed:
                module_passed += 1
                total_passed += 1
            total_checks += 1

        module_results[module_name] = {
            "passed": module_passed,
            "total": module_total,
            "results": results
        }

    # Print results
    for module_name, data in module_results.items():
        passed = data["passed"]
        total = data["total"]
        pct = int(passed / total * 100) if total > 0 else 0

        # Module header
        if passed == total:
            status = "DONE"
        elif passed > 0:
            status = "IN PROGRESS"
        else:
            status = "NOT STARTED"

        print(f"--- {module_name} [{status}] ({passed}/{total} = {pct}%) ---")

        for check_passed, label, error in data["results"]:
            icon = "[x]" if check_passed else "[ ]"
            err_msg = f"  ({error})" if error else ""
            print(f"  {icon} {label}{err_msg}")

        print("")

    # Summary
    pct_total = int(total_passed / total_checks * 100) if total_checks > 0 else 0

    print("=" * 70)
    print(f"  OVERALL PROGRESS: {total_passed}/{total_checks} checks passed ({pct_total}%)")
    print("")

    # Progress bar
    bar_width = 50
    filled = int(bar_width * pct_total / 100)
    bar = "#" * filled + "-" * (bar_width - filled)
    print(f"  [{bar}] {pct_total}%")
    print("")

    # Completion status
    if pct_total == 100:
        print("  CONGRATULATIONS! You have completed all modules!")
        print("  CHÚC MỪNG! Bạn đã hoàn thành tất cả các module!")
    elif pct_total >= 75:
        print("  Almost there! Just a few more exercises to complete.")
        print("  Sắp xong rồi! Chỉ còn vài bài tập nữa.")
    elif pct_total >= 50:
        print("  Good progress! Keep going!")
        print("  Tiến độ tốt! Tiếp tục nào!")
    elif pct_total >= 25:
        print("  Getting started. Work through the exercises step by step.")
        print("  Đã bắt đầu. Làm từng bài tập theo thứ tự.")
    else:
        print("  Just starting out. Begin with Module 1-2: App Setup.")
        print("  Mới bắt đầu. Hãy bắt đầu với Module 1-2: Thiết lập App.")

    print("")
    print("=" * 70)

    return {
        "total_checks": total_checks,
        "total_passed": total_passed,
        "percentage": pct_total,
        "modules": {
            name: {"passed": d["passed"], "total": d["total"]}
            for name, d in module_results.items()
        }
    }


# Allow standalone execution for file-system-only checks
if __name__ == "__main__":
    # Parse --app-path argument
    if "--app-path" in sys.argv:
        idx = sys.argv.index("--app-path")
        if idx + 1 < len(sys.argv):
            APP_PATH = sys.argv[idx + 1]
            MODULE_PATH = os.path.join(APP_PATH, APP_NAME, "library")

    print("Running file-system checks only (no database checks)...")
    print(f"App path: {APP_PATH}")
    print("")

    # Only run file/dir checks
    for module_name, module_config in MODULES.items():
        print(f"--- {module_name} ---")
        for check_def in module_config["checks"]:
            check_type = check_def[0]
            label = check_def[1]
            args = check_def[2:]

            if check_type in ("file_exists", "dir_exists"):
                passed = check_file_exists(args[0]) if check_type == "file_exists" else check_dir_exists(args[0])
                icon = "[x]" if passed else "[ ]"
                print(f"  {icon} {label}")
            else:
                print(f"  [?] {label} (requires database - skipped)")
        print("")
