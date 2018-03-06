"""
Response cases for testcases.
"""

STATUSES = ["open", "closed", "hold", "new", "pending", "solved"]
SOURCES = ["email", "twitter", "facebook"]

TICKET_TEMPLATE = {
    "id": 1,
    "subject": "Sample subject: ",
    "description": "Sample description of this ticket.",
    "status": None,
    "via": None,
}

ERROR_TEMPLATE = {
    "auth": { # with HTTP 401
        "error": "Couldn't authenticate you"
    }
}

VIA_TEMPLATES = {
    "email": {
        "channel": "email",
        "source": {
            "from": {
                "address": "someone@hello.com",
                "name": "John Doe"
            },
            "to": {
                "name": "Support Team",
                "address": "support@harrydrippin.zendesk.com"
            },
            "rel": None
        }
    },
    "twitter": {
        "channel": "twitter",
        "source": {
            "from": {
                "name": "John Doe",
                "profile_url": "twitter.com/hello",
                "username": "hello"
            },
            "to": {
                "name": "Someone: to",
                "profile_url": "twitter.com/world",
                "username": "world"
            },
            "rel": "direct_message"
        }
    },
    "facebook": {
        "channel": "facebook",
        "source": {
            "from": {
                "name": "John Doe",
                "profile_url": "fb.com/hello",
                "facebook_id": "1234321"
            },
            "to": {
                "name": "Someone: to",
                "profile_url": "fb.com/world",
                "facebook_id": "4321234"
            },
            "rel": "message"
        }
    },
    "none": {
        "channel": "whatever",
        "source": {
            "rel": None
        }
    }
}

def generate_ticket(ticket_id, status, via):
    """Generate cases based on templates."""
    result = TICKET_TEMPLATE
    result["id"] = ticket_id
    result["subject"] += str(ticket_id) + ", " + str(status)
    result["status"] = status

    if via in SOURCES:
        result["via"] = VIA_TEMPLATES[via]
    else:
        result["via"] = VIA_TEMPLATES["none"]
    return result
