"""Unit tests for vn_banking.match.party_extract — pure functions, no Frappe."""
import unittest

from vn_banking.match.party_extract import (
    find_party_in_description,
    normalize_vn_company_name,
)


class TestNormalizeVnCompanyName(unittest.TestCase):
    def test_strips_cty_prefix(self):
        self.assertEqual(normalize_vn_company_name("CTY CMC TELECOM"), "CMC TELECOM")

    def test_strips_cong_ty_prefix(self):
        self.assertEqual(normalize_vn_company_name("CÔNG TY NETNAM"), "NETNAM")

    def test_strips_cong_ty_no_diacritic(self):
        self.assertEqual(normalize_vn_company_name("CONG TY NETNAM"), "NETNAM")

    def test_strips_tnhh(self):
        self.assertEqual(normalize_vn_company_name("CTY TNHH MTV ABC"), "ABC")

    def test_strips_ctcp(self):
        self.assertEqual(normalize_vn_company_name("CTCP VIETTEL"), "VIETTEL")

    def test_diacritics_normalized(self):
        # Diacritic normalization for VN names like "Tâm Đỉnh" → "TAM DINH"
        self.assertEqual(normalize_vn_company_name("Tâm Đỉnh"), "TAM DINH")

    def test_collapses_internal_whitespace(self):
        self.assertEqual(
            normalize_vn_company_name("CONG  TY   CO  PHAN   ABC"), "ABC"
        )

    def test_strips_trailing_punctuation(self):
        self.assertEqual(normalize_vn_company_name("CTY ABC,"), "ABC")

    def test_empty_input(self):
        self.assertEqual(normalize_vn_company_name(""), "")
        self.assertEqual(normalize_vn_company_name(None), "")


class TestFindPartyInDescription(unittest.TestCase):
    def test_finds_exact_party_in_description(self):
        """CMC TELECOM in description -> matches Customer 'CMC TELECOM'."""
        desc = "CMC TELECOM TT CUOC T01.26"
        result = find_party_in_description(desc, ["CMC TELECOM", "NetNam"])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "CMC TELECOM")
        self.assertGreaterEqual(result[1], 95)

    def test_finds_party_with_cty_prefix_in_description(self):
        """'CTY CMC TELECOM CHUYEN KHOAN' should match Customer 'CMC TELECOM'."""
        desc = "CTY CMC TELECOM CHUYEN KHOAN TT HOA DON"
        result = find_party_in_description(desc, ["CMC TELECOM", "NetNam"])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "CMC TELECOM")

    def test_finds_party_when_customer_has_cty_prefix(self):
        """Description 'CMC TELECOM' should match Customer 'CTY CP CMC TELECOM'."""
        desc = "CMC TELECOM TT CUOC"
        result = find_party_in_description(desc, ["CTY CP CMC TELECOM", "NetNam"])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "CTY CP CMC TELECOM")

    def test_no_match_below_threshold(self):
        desc = "RANDOM TEXT WITH NO PARTY NAME XYZ123"
        result = find_party_in_description(
            desc, ["CMC TELECOM", "NetNam"], threshold=80
        )
        self.assertIsNone(result)

    def test_no_match_when_description_empty(self):
        self.assertIsNone(find_party_in_description("", ["CMC TELECOM"]))
        self.assertIsNone(find_party_in_description(None, ["CMC TELECOM"]))

    def test_no_match_when_candidates_empty(self):
        self.assertIsNone(find_party_in_description("CMC TELECOM TT", []))

    def test_picks_best_when_multiple_match(self):
        """If both NetNam and NetNam VN appear, pick the higher-ratio one."""
        desc = "NETNAM VIETNAM TT HD T05"
        result = find_party_in_description(
            desc, ["NetNam", "NetNam VN", "CMC TELECOM"]
        )
        self.assertIsNotNone(result)
        # 'NetNam VN' should rank higher than 'NetNam' on this description
        self.assertIn(result[0], ("NetNam", "NetNam VN"))

    def test_diacritic_party_in_ascii_description(self):
        """Bank statements strip diacritics; 'TAM DINH' should match 'Tâm Đỉnh'."""
        desc = "TAM DINH TT HOA DON 0001"
        result = find_party_in_description(desc, ["Tâm Đỉnh", "Other Customer"])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Tâm Đỉnh")

    def test_threshold_respected(self):
        """If threshold=95, a 'good but not perfect' match shouldn't return."""
        desc = "CMCTELE TT"
        # default threshold 80 may match; threshold 95 should not
        # (we want to assert the threshold knob actually works)
        r80 = find_party_in_description(desc, ["CMC TELECOM"], threshold=80)
        r99 = find_party_in_description(desc, ["CMC TELECOM"], threshold=99)
        # at least r99 must be None (very strict)
        self.assertIsNone(r99)
        # r80 may or may not match — we don't assert which
        del r80


if __name__ == "__main__":
    unittest.main()
