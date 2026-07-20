"""Unit tests for UX gap fixes — filename auto-detect + auto-submit
+ persistence + mark_reviewed promotion.

UX Gap 1 (batch persistence) is JS-only; verified via Playwright in
parent session. This file covers the Python-side gaps:
  * Gap 2: detect_file_type_from_name() classifier
  * Gap 3: post_batch(auto_submit=True) wraps submit_phase_4_drafts
  * Gap 4: mark_reviewed promotes New → Ready
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch


class TestDetectFileTypeFromName(unittest.TestCase):
    """detect_file_type_from_name maps Misa SDK filenames → file_type."""

    def _detect(self, name):
        from vn_accounting.misa_migration.api.upload import (
            detect_file_type_from_name,
        )
        return detect_file_type_from_name(name)

    def test_empty_returns_unknown(self):
        self.assertEqual(self._detect(""), "Unknown")
        self.assertEqual(self._detect(None), "Unknown")
        self.assertEqual(self._detect("   "), "Unknown")

    # --- Phase 4 transactions

    def test_nkc_so_nhat_ky_chung(self):
        self.assertEqual(self._detect("So_nhat_ky_chung_2025.xlsx"), "NKC")
        self.assertEqual(self._detect("So_nhat_ky_chung_01-2026.xlsx"), "NKC")

    def test_bang_ke_ban_ra(self):
        self.assertEqual(
            self._detect("Bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_ban_ra_2025.xlsx"),
            "Bang ke BR",
        )

    def test_bang_ke_mua_vao(self):
        self.assertEqual(
            self._detect("Bang_ke_hoa_don_chung_tu_hang_hoa_dich_vu_mua_vao 01-2026.xlsx"),
            "Bang ke MV",
        )

    # --- Phase 0 opening balances (the 9 OB files)

    def test_ob_account_balance(self):
        self.assertEqual(
            self._detect("Danh_sach_so_du_tai_khoan.xlsx"),
            "OB Account Balance",
        )

    def test_ob_bank_balance(self):
        """More specific 'ngan_hang' pattern wins over generic 'so_du_tai_khoan'."""
        self.assertEqual(
            self._detect("Danh_sach_nhap_so_du_tai_khoan_ngan_hang.xlsx"),
            "OB Bank Balance",
        )

    def test_ob_customer_ar(self):
        self.assertEqual(
            self._detect("Danh_sach_cong_no_khach_hang.xlsx"),
            "OB Customer AR",
        )

    def test_ob_supplier_ap(self):
        self.assertEqual(
            self._detect("Danh_sach_cong_no_nha_cung_cap.xlsx"),
            "OB Supplier AP",
        )

    def test_ob_employee_advance(self):
        self.assertEqual(
            self._detect("Danh_sach_cong_no_nhan_vien.xlsx"),
            "OB Employee Advance",
        )

    def test_ob_prepaid_expense(self):
        self.assertEqual(
            self._detect("Danh_sach_chi_phi_tra_truoc_dau_ky.xlsx"),
            "OB Prepaid Expense",
        )

    def test_ob_inventory(self):
        self.assertEqual(
            self._detect("Danh_sach_ton_kho_vthh.xlsx"),
            "OB Inventory",
        )

    def test_ob_fixed_asset(self):
        self.assertEqual(
            self._detect("Danh_sach_tai_san_co_dinh_dau_ky.xlsx"),
            "OB Fixed Asset",
        )

    def test_ob_ccdc(self):
        self.assertEqual(
            self._detect("Danh_sach_cong_cu_dung_cu_dau_ky.xlsx"),
            "OB CCDC",
        )

    # --- Phase 3 master entities

    def test_customer_master(self):
        self.assertEqual(
            self._detect("Danh_sach_khach_hang.xlsx"),
            "Customer",
        )

    def test_supplier_master(self):
        self.assertEqual(
            self._detect("Danh_sach_nha_cung_cap.xlsx"),
            "Supplier",
        )

    def test_item_master(self):
        self.assertEqual(
            self._detect("Danh_sach_hang_hoa_dich_vu.xlsx"),
            "Item",
        )

    def test_employee_master(self):
        self.assertEqual(
            self._detect("Danh_sach_nhan_vien.xlsx"),
            "Employee",
        )

    # --- Phase 2 Chart of Accounts

    def test_chart_of_accounts(self):
        self.assertEqual(
            self._detect("Danh_sach_he_thong_tai_khoan_.xlsx"),
            "Account",
        )

    # --- Phase 1 reference masters

    def test_bank_master(self):
        self.assertEqual(self._detect("Danh_sach_ngan_hang.xlsx"), "Bank")

    def test_uom_master(self):
        self.assertEqual(self._detect("Danh_sach_don_vi_tinh.xlsx"), "UOM")

    def test_warehouse_master(self):
        self.assertEqual(self._detect("Danh_sach_kho.xlsx"), "Warehouse")

    def test_department_master(self):
        self.assertEqual(
            self._detect("Danh_sach_co_cau_to_chuc.xlsx"),
            "Department",
        )

    def test_project_master(self):
        self.assertEqual(
            self._detect("Danh_sach_cong_trinh.xlsx"),
            "Project",
        )

    # --- Defensive cases

    def test_with_path_prefix(self):
        self.assertEqual(
            self._detect("/private/files/abc/Danh_sach_cong_no_khach_hang.xlsx"),
            "OB Customer AR",
        )

    def test_with_random_suffix(self):
        # Misa sometimes appends date/version suffix to filenames
        self.assertEqual(
            self._detect("Danh_sach_so_du_tai_khoan_2025-12-31.xlsx"),
            "OB Account Balance",
        )

    def test_case_insensitive(self):
        self.assertEqual(
            self._detect("DANH_SACH_CONG_NO_KHACH_HANG.XLSX"),
            "OB Customer AR",
        )

    def test_unknown_filename_returns_unknown(self):
        self.assertEqual(self._detect("random_file.xlsx"), "Unknown")
        self.assertEqual(self._detect("invoice.csv"), "Unknown")


class TestPostBatchAutoSubmit(unittest.TestCase):
    """post_batch(auto_submit=True) calls submit_phase_4_drafts after
    Phase 0+4 inserts complete."""

    def _setup_mocks(self, mock_frappe, status_history, batch_company="DCNET TEST"):
        """Common mock setup. status_history tracks state transitions."""
        # frappe.get_doc returns a mock with status reflecting most recent
        # transition. Initial status = REVIEWED.
        batch_mock = MagicMock()
        batch_mock.status = "REVIEWED"
        batch_mock.company = batch_company
        batch_mock.name = "MM-X"

        def get_doc(dt, name):
            if dt == "Misa Migration Batch":
                return batch_mock
            return MagicMock()

        mock_frappe.get_doc.side_effect = get_doc
        mock_frappe.db.get_value.return_value = batch_company
        mock_frappe.defaults.get_global_default.return_value = batch_company
        mock_frappe.db.commit = MagicMock()
        mock_frappe.publish_realtime = MagicMock()
        mock_frappe.log_error = MagicMock()
        return batch_mock

    def test_auto_submit_true_calls_submit_phase_4_drafts(self):
        from vn_accounting.misa_migration.jobs import post_job

        history: list[str] = []
        with patch.object(post_job, "frappe") as mock_frappe, \
             patch.object(post_job, "run_post", return_value={}), \
             patch.object(post_job, "run_phase_0_post", return_value={}), \
             patch.object(post_job, "run_phase_4_post", return_value={"by_target_doctype": {}}), \
             patch.object(post_job, "submit_phase_4_drafts") as mock_submit, \
             patch.object(post_job, "st") as mock_st, \
             patch("vn_accounting.misa_migration.context.set_active_company") as mock_set, \
             patch("vn_accounting.misa_migration.context.clear_active_company") as mock_clear:
            self._setup_mocks(mock_frappe, history)
            # st.lock_for_batch must be a context manager
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            mock_st.transition = MagicMock()
            mock_st.REVIEWED = "REVIEWED"
            mock_st.POSTING = "POSTING"
            mock_st.POSTED = "POSTED"
            mock_st.STUCK = "STUCK"
            mock_submit.return_value = {
                "submitted": {"Journal Entry": 1}, "failed": {},
                "total_submitted": 1, "total_failed": 0,
                "elapsed_seconds": 0.5,
            }

            result = post_job.post_batch("MM-X", auto_submit=True)

        # submit_phase_4_drafts was invoked with batch_name + company
        mock_submit.assert_called_once_with(
            batch_name="MM-X", company="DCNET TEST",
        )
        # Active company was pinned during the submit pass
        mock_set.assert_called_once_with("DCNET TEST")
        mock_clear.assert_called_once()
        # Result includes submit summary under __submit__ key
        self.assertEqual(
            result["summary"].get("__submit__"),
            {"submitted": {"Journal Entry": 1}, "failed": {},
             "total_submitted": 1, "total_failed": 0, "elapsed_seconds": 0.5},
        )

    def test_auto_submit_false_skips_submit(self):
        from vn_accounting.misa_migration.jobs import post_job

        with patch.object(post_job, "frappe") as mock_frappe, \
             patch.object(post_job, "run_post", return_value={}), \
             patch.object(post_job, "run_phase_0_post", return_value={}), \
             patch.object(post_job, "run_phase_4_post", return_value={"by_target_doctype": {}}), \
             patch.object(post_job, "submit_phase_4_drafts") as mock_submit, \
             patch.object(post_job, "st") as mock_st:
            self._setup_mocks(mock_frappe, [])
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            mock_st.transition = MagicMock()
            mock_st.REVIEWED = "REVIEWED"
            mock_st.POSTING = "POSTING"
            mock_st.POSTED = "POSTED"
            mock_st.STUCK = "STUCK"

            post_job.post_batch("MM-X", auto_submit=False)

        mock_submit.assert_not_called()

    def test_default_is_auto_submit_true(self):
        """Verify the default kwarg value."""
        import inspect
        from vn_accounting.misa_migration.jobs import post_job
        sig = inspect.signature(post_job.post_batch)
        self.assertEqual(sig.parameters["auto_submit"].default, True)


class TestAttachFileAutoDetect(unittest.TestCase):
    """attach_file uses detect_file_type_from_name when caller passes
    'Unknown' or omits file_type."""

    def test_attach_with_unknown_filetype_triggers_autodetect(self):
        from vn_accounting.misa_migration.api import upload as up

        with patch.object(up, "frappe") as mock_frappe, \
             patch.object(up, "st") as mock_st:
            batch_mock = MagicMock()
            batch_mock.status = "UPLOADED"
            batch_mock.files = []
            mock_frappe.get_doc.return_value = batch_mock
            mock_frappe.db.commit = MagicMock()
            mock_st.DRAFT = "DRAFT"
            mock_st.UPLOADED = "UPLOADED"
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None

            # Mock _serialize to skip the second get_doc round trip
            with patch.object(up, "_serialize", return_value={}):
                up.attach_file(
                    batch_name="MM-X",
                    file_url="/private/files/Danh_sach_so_du_tai_khoan.xlsx",
                    file_type="Unknown",
                )

        # The append should have set file_type to OB Account Balance
        # (auto-detected from filename)
        batch_mock.append.assert_called_once()
        call_args = batch_mock.append.call_args
        # call_args.args[0] = "files", call_args.args[1] = payload dict
        payload = call_args.args[1]
        self.assertEqual(payload["file_type"], "OB Account Balance")

    def test_attach_with_explicit_filetype_skips_autodetect(self):
        """Operator-set file_type wins over auto-detect."""
        from vn_accounting.misa_migration.api import upload as up

        with patch.object(up, "frappe") as mock_frappe, \
             patch.object(up, "st") as mock_st:
            batch_mock = MagicMock()
            batch_mock.status = "UPLOADED"
            batch_mock.files = []
            mock_frappe.get_doc.return_value = batch_mock
            mock_frappe.db.commit = MagicMock()
            mock_st.DRAFT = "DRAFT"
            mock_st.UPLOADED = "UPLOADED"
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None

            with patch.object(up, "_serialize", return_value={}):
                up.attach_file(
                    batch_name="MM-X",
                    file_url="/private/files/Danh_sach_so_du_tai_khoan.xlsx",
                    file_type="NKC",   # operator override
                )

        call_args = batch_mock.append.call_args
        payload = call_args.args[1]
        # NKC explicit wins, NOT OB Account Balance auto-detected
        self.assertEqual(payload["file_type"], "NKC")


class TestMarkReviewedPromoteNewToReady(unittest.TestCase):
    """UX Gap 4: mark_reviewed bulk-promotes status='New' → 'Ready' so
    Phase 0+4 orchestrators (which filter status='Ready') actually post.
    """

    def test_promotes_new_rows_to_ready(self):
        from vn_accounting.misa_migration.api import review as r

        with patch.object(r, "frappe") as mock_frappe, \
             patch.object(r, "st") as mock_st:
            # Batch is PARSED; 0 Invalid rows
            mock_frappe.db.get_value.return_value = "PARSED"
            mock_frappe.db.count.return_value = 0  # n_invalid
            # frappe.db.count for ready rows count call after UPDATE → 100
            counts: list[int] = [0, 100]
            mock_frappe.db.count.side_effect = counts
            mock_frappe.db.sql = MagicMock()
            mock_frappe.db.commit = MagicMock()
            batch_mock = MagicMock()
            mock_frappe.get_doc.return_value = batch_mock
            mock_st.PARSED = "PARSED"
            mock_st.REVIEWED = "REVIEWED"
            mock_st.lock_for_batch.return_value.__enter__ = lambda s: None
            mock_st.lock_for_batch.return_value.__exit__ = lambda s, *a: None
            mock_st.transition = MagicMock()

            result = r.mark_reviewed(batch_name="MM-X")

        # SQL UPDATE was executed to promote New → Ready
        mock_frappe.db.sql.assert_called_once()
        sql_call = mock_frappe.db.sql.call_args
        sql_text = sql_call.args[0]
        self.assertIn("UPDATE", sql_text)
        self.assertIn("status='Ready'", sql_text)
        self.assertIn("status='New'", sql_text)
        # Result reports Ready count
        self.assertEqual(result["status"], "REVIEWED")
        self.assertEqual(result["ready_rows"], 100)

    def test_blocks_when_invalid_rows_present(self):
        from vn_accounting.misa_migration.api import review as r

        with patch.object(r, "frappe") as mock_frappe, \
             patch.object(r, "st") as mock_st:
            mock_frappe.db.get_value.return_value = "PARSED"
            mock_frappe.db.count.return_value = 5  # 5 Invalid rows
            mock_frappe.throw.side_effect = Exception("vn_accounting throw")
            mock_st.PARSED = "PARSED"

            with self.assertRaises(Exception):
                r.mark_reviewed(batch_name="MM-X")

            # Promotion SQL must NOT have run when Invalid exists
            mock_frappe.db.sql.assert_not_called()


if __name__ == "__main__":
    unittest.main()
