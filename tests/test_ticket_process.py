"""
Testcases for processing ticket list and detail.
"""
import unittest

from app.main.utils import process_response
from tests import MockResponse, cases

class TicketProcessTests(unittest.TestCase):
    """Testcases for ticket list."""
    def setUp(self):
        self.sample_ok = {
            "ticket": cases.generate_ticket(1, cases.STATUSES[0], cases.SOURCES[1])
        }
        self.sample_ok["ticket"]["via"] = cases.VIA_TEMPLATES["email"]

        self.sample_ok_list = {
            "tickets": list()
        }

        for i in range(1, 101):
            self.sample_ok_list["tickets"].append(
                cases.generate_ticket(i, cases.STATUSES[i % 6], cases.SOURCES[i % 3])
            )

        self.resp_ok = MockResponse(self.sample_ok, 200)
        self.resp_ok_list = MockResponse(self.sample_ok_list, 200)
        self.resp_not_found = MockResponse({
            "error": "RecordNotFound",
            "description": "Not found"
        }, 404)
        self.resp_auth_error = MockResponse(cases.ERROR_TEMPLATE["auth"], 401)
        self.resp_rate_exceed = MockResponse(dict(), 429, headers={
            "Retry-After": "120"
        })
        self.resp_service_unavailable = MockResponse(dict(), 503, headers={
            "Retry-After": "1080"
        })
        self.resp_unexpected_error = MockResponse({
            "error": {
                "title": "Title of this error",
                "description": "Description of this error"
            }
        }, 500)

    def test_ok_result(self):
        """Should return 0 for result when response is ok"""
        process_result = process_response(self.resp_ok)
        self.assertEqual(process_result["result"], 0)

    def test_ok_returned_ticket(self):
        """Should return original ticket when response is ok"""
        process_result = process_response(self.resp_ok)
        self.assertEqual(process_result["detail"], self.sample_ok)

    def test_ok_list_result(self):
        """Should return 0 for result when response for list is ok"""
        process_result = process_response(self.resp_ok_list, is_detail=False)
        self.assertEqual(process_result["result"], 0)

    def test_ok_list_returned_tickets(self):
        """Should return original ticket list when response for list is ok"""
        process_result = process_response(self.resp_ok_list, is_detail=False)
        self.assertEqual(process_result["detail"], self.sample_ok_list)

    def test_ok_has_requester(self):
        """Should return requester information when response is ok"""
        process_result = process_response(self.resp_ok)
        self.assertEqual(process_result["detail"]["ticket"]["is_requester_exist"], True)
        self.assertEqual(process_result["detail"]["ticket"]["requester"], "John Doe")

    def test_auth_failure_result(self):
        """Should return 1 for result when response has auth failure"""
        process_result = process_response(self.resp_auth_error)
        self.assertEqual(process_result["result"], 1)

    def test_auth_failure_error(self):
        """Should return error message when response has auth failure"""
        process_result = process_response(self.resp_auth_error)
        self.assertEqual(process_result["error"], "Authentication error")

    def test_rate_exceed_result(self):
        """Should return 2 for result when response has rate exceed error"""
        process_result = process_response(self.resp_rate_exceed)
        self.assertEqual(process_result["result"], 2)

    def test_rate_exceed_retry(self):
        """Should return given retry-after seconds when response has rate exceed error"""
        process_result = process_response(self.resp_rate_exceed)
        self.assertEqual(process_result["retry_after"], 120)

    def test_not_found_result(self):
        """Should return 3 for result when response has not found error"""
        process_result = process_response(self.resp_not_found)
        self.assertEqual(process_result["result"], 3)

    def test_not_found_error(self):
        """Should return error message when response has not found error"""
        process_result = process_response(self.resp_not_found)
        self.assertEqual(process_result["error"], "Not found")

    def test_service_unavailable_result(self):
        """Should return 4 when response has service unavailable error"""
        process_result = process_response(self.resp_service_unavailable)
        self.assertEqual(process_result["result"], 4)

    def test_service_unavailable_retry(self):
        """Should return given retry-after seconds when response has rate exceed error"""
        process_result = process_response(self.resp_service_unavailable)
        self.assertEqual(process_result["retry_after"], 1080)

    def test_unexpected_error_result(self):
        """Should return -1 when response has unexpected error."""
        process_result = process_response(self.resp_unexpected_error)
        self.assertEqual(process_result["result"], -1)
