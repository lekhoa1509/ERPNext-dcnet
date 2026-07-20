import unittest

from dcnet_contract.dcnet_contract.utils.state_machine import ALLOWED, assert_transition


class TestAllowedTransitions(unittest.TestCase):
	def test_draft_to_active(self):
		assert_transition("Draft", "Active")

	def test_active_to_suspended(self):
		assert_transition("Active", "Suspended")

	def test_suspended_to_active(self):
		assert_transition("Suspended", "Active")

	def test_active_to_expired(self):
		assert_transition("Active", "Expired")

	def test_suspended_to_expired(self):
		assert_transition("Suspended", "Expired")

	def test_active_to_cancelled(self):
		assert_transition("Active", "Cancelled")

	def test_suspended_to_cancelled(self):
		assert_transition("Suspended", "Cancelled")

	def test_draft_to_cancelled(self):
		assert_transition("Draft", "Cancelled")


class TestBlockedTransitions(unittest.TestCase):
	def test_cancelled_to_active_blocked(self):
		with self.assertRaises(ValueError):
			assert_transition("Cancelled", "Active")

	def test_expired_to_active_blocked(self):
		with self.assertRaises(ValueError):
			assert_transition("Expired", "Active")

	def test_draft_to_suspended_blocked(self):
		with self.assertRaises(ValueError):
			assert_transition("Draft", "Suspended")

	def test_active_to_draft_blocked(self):
		with self.assertRaises(ValueError):
			assert_transition("Active", "Draft")

	def test_revised_to_active_blocked(self):
		with self.assertRaises(ValueError):
			assert_transition("Revised", "Active")


class TestAllowedDict(unittest.TestCase):
	def test_has_10_transitions(self):
		self.assertEqual(len(ALLOWED), 10)

	def test_active_to_revised(self):
		assert_transition("Active", "Revised")

	def test_cancelled_to_revised(self):
		assert_transition("Cancelled", "Revised")
