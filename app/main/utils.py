"""Module for access Zendesk API and process data."""
import requests
from requests.auth import HTTPBasicAuth
from config import Config

BASIC_AUTH = HTTPBasicAuth(Config.agent_email, Config.agent_password)

def get_link_base(subdomain):
    """Assemble API link base by subdomain."""
    return Config.link_base.format(subdomain=subdomain)

def fetch_ticket_list():
    """Fetch ticket list from Zendesk API."""
    url = get_link_base(Config.subdomain) + Config.link_tickets
    return requests.get(url, auth=BASIC_AUTH)

def fetch_ticket_details(ticket_id):
    """Fetch specific ticket detail from Zendesk API."""
    url = get_link_base(Config.subdomain) \
            + Config.link_ticket_detail.format(ticket_id=ticket_id)
    return requests.get(url, auth=BASIC_AUTH)

def process_response(response):
    """Extract information from fetched data."""
    detail = response.json()

    if response.status_code == 200:
        return {
            "result": 0,
            "detail": detail
        }
    elif response.status_code == 401:
        return {
            "result": 1,
            "error": "Authentication error"
        }
    elif response.status_code == 429:
        retry_seconds = response.headers["Retry-After"]
        return {
            "result": 2,
            "error": "Rate limit exceeded",
            "retry_after": int(retry_seconds)
        }
    elif response.status_code == 404:
        return {
            "result": 3,
            "error": "Not found"
        }
    elif response.status_code == 503:
        retry_seconds = response.headers["Retry-After"]
        return {
            "result": 4,
            "error": "Service unavailable",
            "retry_after": int(retry_seconds)
        }

    return {
        "result": -1,
        "error": "Unexpected error"
    }
