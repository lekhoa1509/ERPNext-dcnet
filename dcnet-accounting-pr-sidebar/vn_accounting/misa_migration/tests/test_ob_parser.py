"""Unit tests for the 9 opening-balance parsers.

Each test feeds a synthetic xlsx-shaped row list (the same shape openpyxl
emits) and asserts the parser produces the documented dict.

Real-data smoke tests run against the on-disk Misa exports when
available — gated by file existence so they skip in CI without the
realdata folder.
"""

from __future__ import annotations

import os
import unittest
from pathlib import Path
from unicodedata import normalize


def _find_realdata_file(name: str) -> Path | None:
    """Locate an OB xlsx in the realdata folder regardless of NFC/NFD
    encoding on the parent directory name."""
    base = Path(
        '/home/long/long/frappe-bench-dcnet/docs/accounting-requirements/realdata'
    )
    if not base.exists():
        return None
    for entry in base.iterdir():
        if '__MACOSX' in entry.name:
            continue
        if 'số dư' in normalize('NFC', entry.name).lower():
            for sub in entry.iterdir():
                if '__MACOSX' in sub.name:
                    continue
                if 'số dư' in normalize('NFC', sub.name).lower():
                    target = sub / name
                    if target.exists():
                        return target
    return None


def _xlsx_rows(p: Path) -> list[tuple]:
    from openpyxl import load_workbook
    wb = load_workbook(str(p), read_only=True, data_only=True)
    rows = list(wb.active.iter_rows(values_only=True))
    wb.close()
    return rows


class TestAccountBalanceParser(unittest.TestCase):

    def _synth(self):
        return [
            ('Danh sách Số dư tài khoản', None, None, None, None),
            (None, None, None, None, None),
            ('STT', 'Số tài khoản', 'Tên tài khoản', 'Dư Nợ', 'Dư Có'),
            ('1', '111', 'Tiền mặt', 971401947, 0),
            ('2', '1111', 'Tiền Việt Nam', 971401947, 0),
            ('3', '131', 'Phải thu của khách hàng', 4089355020, 1564004140),
            (None, None, 'Tổng', None, None),
        ]

    def test_synth(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_account_balance
        r = parse_account_balance(self._synth())
        self.assertEqual(len(r), 3)
        self.assertEqual(r[0]['account_number'], '111')
        self.assertEqual(r[0]['account_name'], 'Tiền mặt')
        self.assertEqual(r[0]['dr'], 971401947.0)
        self.assertEqual(r[0]['cr'], 0.0)
        self.assertEqual(r[2]['account_number'], '131')
        self.assertEqual(r[2]['cr'], 1564004140.0)

    def test_real_file(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_account_balance
        p = _find_realdata_file('Danh_sach_so_du_tai_khoan.xlsx')
        if not p:
            self.skipTest('realdata file not found')
        rows = _xlsx_rows(p)
        result = parse_account_balance(rows)
        self.assertGreater(len(result), 5)
        # Verified codes from the file (TK 111, 112)
        accts = [r['account_number'] for r in result]
        self.assertIn('111', accts)
        self.assertIn('112', accts)


class TestBankBalanceParser(unittest.TestCase):

    def _synth(self):
        return [
            ('Danh sách Nhập số dư tài khoản', None, None, None, None, None),
            (None, None, None, None, None, None),
            ('STT', 'Số TK ngân hàng', 'Tên ngân hàng', 'Số tài khoản', 'Dư Nợ', 'Dư Có'),
            ('1', '000008004970', 'SEABANK', '11214', 11339937, 0),
            ('2', '262086313', 'VPBANK', '11218', 38792955, 0),
            (None, None, 'Tổng', None, 50132892, 0),
        ]

    def test_synth(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_bank_balance
        r = parse_bank_balance(self._synth())
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0]['bank_no'], '000008004970')
        self.assertEqual(r[0]['account_number'], '11214')
        self.assertEqual(r[0]['dr'], 11339937.0)

    def test_real_file(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_bank_balance
        p = _find_realdata_file('Danh_sach_nhap_so_du_tai_khoan_ngan_hang.xlsx')
        if not p:
            self.skipTest('realdata file not found')
        result = parse_bank_balance(_xlsx_rows(p))
        self.assertEqual(len(result), 5)  # 5 bank sub-accounts


class TestPartyBalanceParsers(unittest.TestCase):

    def _synth(self, label: str, sample_codes: tuple[str, str]):
        return [
            (f'Danh sách Công nợ {label}', None, None, None, None, None),
            (None, None, None, None, None, None),
            ('STT', 'Số tài khoản', f'Mã {label}', f'Tên {label}', 'Dư Nợ', 'Dư Có'),
            ('1', '131', sample_codes[0], 'CTY A', 35200000, 0),
            ('2', '131', sample_codes[1], 'CTY B', 0, 12345678),
            (None, None, 'Tổng', None, 35200000, 12345678),
        ]

    def test_customer_synth(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_customer_ar
        r = parse_customer_ar(self._synth('khách hàng', ('BIDVCNCT', 'BOE')))
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0]['party_code'], 'BIDVCNCT')
        self.assertEqual(r[1]['cr'], 12345678.0)

    def test_supplier_synth(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_supplier_ap
        r = parse_supplier_ap(self._synth('NCC', ('VIETTEL', '247')))
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0]['party_code'], 'VIETTEL')

    def test_employee_synth(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_employee_advance
        r = parse_employee_advance(self._synth('NV', ('NV02', 'NV03')))
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0]['party_code'], 'NV02')

    def test_real_files(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_customer_ar, parse_supplier_ap, parse_employee_advance
        files_parsers = (
            ('Danh_sach_cong_no_khach_hang.xlsx', parse_customer_ar),
            ('Danh_sach_cong_no_nha_cung_cap.xlsx', parse_supplier_ap),
            ('Danh_sach_cong_no_nhan_vien.xlsx', parse_employee_advance),
        )
        for name, fn in files_parsers:
            with self.subTest(file=name):
                p = _find_realdata_file(name)
                if not p:
                    self.skipTest(f'realdata file not found: {name}')
                r = fn(_xlsx_rows(p))
                self.assertGreater(len(r), 0)
                self.assertIsNotNone(r[0]['party_code'])


class TestInventoryParser(unittest.TestCase):

    def test_synth(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_inventory
        rows = [
            ('Danh sách TỒN KHO VTHH',) + (None,) * 11,
            ('Kho: Tất cả',) + (None,) * 11,
            (None,) * 12,
            ('STT', 'Ngày nhập kho', 'Số phiếu nhập', 'Mã hàng', 'Tên hàng',
             'Nhóm VTHH', 'ĐVT', 'Mã kho', 'Số lượng tồn', 'Đơn giá',
             'Giá trị tồn', 'Số lô'),
            ('1', '2019-12-31', 'OPN', 'CC_MH_70S', 'Máy hàn cáp quang',
             None, 'Cái', 'KHO', 3, 107000000, 321000000, None),
        ]
        r = parse_inventory(rows)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]['item_code'], 'CC_MH_70S')
        self.assertEqual(r[0]['qty'], 3.0)
        self.assertEqual(r[0]['rate'], 107000000.0)
        self.assertEqual(r[0]['amount'], 321000000.0)
        self.assertEqual(r[0]['warehouse'], 'KHO')

    def test_real_file(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_inventory
        p = _find_realdata_file('Danh_sach_ton_kho_vthh.xlsx')
        if not p:
            self.skipTest('realdata file not found')
        r = parse_inventory(_xlsx_rows(p))
        self.assertGreater(len(r), 100)


class TestFixedAssetParser(unittest.TestCase):

    def test_synth(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_fixed_asset
        rows = [
            ('DANH SÁCH TÀI SẢN CỐ ĐỊNH',) + (None,) * 11,
            (None,) * 12,
            ('STT', 'Mã tài sản', 'Tên tài sản', 'Loại tài sản', 'Đơn vị sử dụng',
             'Nguyên giá', 'Giá trị tính KH', 'Hao mòn lũy kế', 'Ngày ghi tăng',
             'Ngày tính KH', 'Thời gian SD (tháng)', 'Thời gian SD còn lại'),
            ('1', 'CC_GHEKLCK8888', 'Ghế massage', 'Thiết bị', 'VP', 40740741,
             40740741, 31272284, '2022-09-12', '2022-09-12', 36, 8),
        ]
        r = parse_fixed_asset(rows)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]['asset_code'], 'CC_GHEKLCK8888')
        self.assertEqual(r[0]['gross_amount'], 40740741.0)
        self.assertEqual(r[0]['accumulated_depreciation'], 31272284.0)
        self.assertEqual(r[0]['useful_life_months'], 36)
        self.assertEqual(r[0]['remaining_useful_life_months'], 8)
        self.assertEqual(r[0]['available_for_use_date'], '2022-09-12')

    def test_real_file(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_fixed_asset
        p = _find_realdata_file('Danh_sach_tai_san_co_dinh_dau_ky.xlsx')
        if not p:
            self.skipTest('realdata file not found')
        r = parse_fixed_asset(_xlsx_rows(p))
        self.assertGreater(len(r), 5)


class TestCcdcParser(unittest.TestCase):

    def test_synth(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_ccdc
        rows = [
            ('DANH SÁCH CÔNG CỤ DỤNG CỤ',) + (None,) * 11,
            (None,) * 12,
            ('STT', 'Mã CCDC', 'Tên CCDC', 'Ngày ghi tăng', 'Số lượng',
             'Giá trị CCDC', 'Giá trị còn lại', 'Số kỳ phân bổ',
             'Số kỳ PB còn lại', 'Số tiền PB hàng kỳ', 'TK chờ phân bổ',
             'Ngừng phân bổ'),
            ('1', 'DT_YEALINK_T19E2', 'ĐT YEALINK', '2021-06-02',
             2, 1400000, 0, 2, 0, 700000, '242', None),
            ('2', 'CC_DGH_5608', 'Đầu ghi hình', '2024-08-24',
             1, 1681818, 488270, 6, 1, 280303, '242', None),
        ]
        r = parse_ccdc(rows)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0]['ccdc_code'], 'DT_YEALINK_T19E2')
        self.assertEqual(r[0]['qty'], 2.0)
        self.assertEqual(r[0]['total_periods'], 2)
        self.assertEqual(r[1]['remaining_periods'], 1)
        self.assertEqual(r[1]['holding_account'], '242')


class TestPrepaidExpenseParser(unittest.TestCase):

    def test_synth(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import parse_prepaid_expense
        rows = [
            ('Danh sách chi phí trả trước',) + (None,) * 9,
            (None,) * 10,
            ('STT', 'Mã CP trả trước', 'Tên CP trả trước', 'Ngày ghi nhận',
             'Số tiền', 'Số tiền còn lại', 'Số kỳ phân bổ',
             'Số kỳ phân bổ còn lại', 'Số tiền PB hàng kỳ', 'Tài khoản chờ phân bổ'),
            ('1', 'CPTTK_205VIETTELHC', 'Thuê HTHCC', '2024-11-01',
             738000, 246000, 3, 1, 246000, '242'),
        ]
        r = parse_prepaid_expense(rows)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]['prepaid_code'], 'CPTTK_205VIETTELHC')
        self.assertEqual(r[0]['total_amount'], 738000.0)
        self.assertEqual(r[0]['remaining_amount'], 246000.0)
        self.assertEqual(r[0]['total_periods'], 3)
        self.assertEqual(r[0]['remaining_periods'], 1)
        self.assertEqual(r[0]['per_period_amount'], 246000.0)


class TestDetectFileType(unittest.TestCase):

    def _cases(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import detect_file_type
        return detect_file_type, [
            ('Danh sách Số dư tài khoản', 'OB Account Balance'),
            ('Danh sách Nhập số dư tài khoản ngân hàng', 'OB Bank Balance'),
            ('Danh sách Công nợ khách hàng', 'OB Customer AR'),
            ('Danh sách Công nợ nhà cung cấp', 'OB Supplier AP'),
            ('Danh sách Công nợ nhân viên', 'OB Employee Advance'),
            ('Danh sách TỒN KHO VTHH', 'OB Inventory'),
            ('DANH SÁCH TÀI SẢN CỐ ĐỊNH', 'OB Fixed Asset'),
            ('DANH SÁCH CÔNG CỤ DỤNG CỤ', 'OB CCDC'),
            ('Danh sách chi phí trả trước', 'OB Prepaid Expense'),
        ]

    def test_each_title_resolves(self):
        detect, cases = self._cases()
        for title, expected in cases:
            self.assertEqual(detect(title), expected,
                             f'{title!r} -> expected {expected!r}')

    def test_unknown_returns_none(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import detect_file_type
        self.assertIsNone(detect_file_type(None))
        self.assertIsNone(detect_file_type(''))
        self.assertIsNone(detect_file_type('Random voucher'))


class TestRegistry(unittest.TestCase):

    def test_all_9_parsers_registered(self):
        from vn_accounting.misa_migration.parsers.opening_balance_parser \
            import PARSER_BY_FILE_TYPE
        self.assertEqual(len(PARSER_BY_FILE_TYPE), 9)
        for v in PARSER_BY_FILE_TYPE.values():
            self.assertTrue(callable(v))


if __name__ == '__main__':
    unittest.main()
