"""
Testcases for extracting requester.
"""
import unittest

from app.main.utils import extract_requester
from tests import cases

class ExtractRequesterTests(unittest.TestCase):
    """Testcases for ticket list."""
    def setUp(self):
        ticket = cases.TICKET_TEMPLATE

        self.email = ticket.copy()
        self.email["via"] = cases.VIA_TEMPLATES["email"]

        self.twitter = ticket.copy()
        self.twitter["via"] = cases.VIA_TEMPLATES["twitter"]

        self.facebook = ticket.copy()
        self.facebook["via"] = cases.VIA_TEMPLATES["facebook"]

        self.none = ticket.copy()
        self.none["via"] = cases.VIA_TEMPLATES["none"]

    def test_email_requester(self):
        """Should extract requester from via-email ticket."""
        is_exist, requester = extract_requester(self.email)
        self.assertEqual(is_exist, True)
        self.assertEqual(requester, "John Doe")

    def test_twitter_requester(self):
        """Should extract requester from via-twitter ticket."""
        is_exist, requester = extract_requester(self.twitter)
        self.assertEqual(is_exist, True)
        self.assertEqual(requester, "John Doe")

    def test_facebook_requester(self):
        """Should extract requester from via-facebook ticket."""
        is_exist, requester = extract_requester(self.facebook)
        self.assertEqual(is_exist, True)
        self.assertEqual(requester, "John Doe")

    def test_no_requester(self):
        """Should discover that no requester is in ticket."""
        is_exist, requester = extract_requester(self.none)
        self.assertEqual(is_exist, False)
        self.assertEqual(requester, str())