"""
Testcases for this application.
"""
class MockResponse:
    """Mock object for requests response."""
    def __init__(self, json_data, status_code, headers=dict()):
        self.json_data = json_data
        self.status_code = status_code
        self.headers = headers

    def json(self):
        """Returns JSON data."""
        return self.json_data
