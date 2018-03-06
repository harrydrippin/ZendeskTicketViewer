"""Module for processing views on this application.

This module handles ticket list and ticket detail page.
"""
from flask import render_template

from config import Config
from app.main.utils import fetch_ticket_list, fetch_ticket_details
from . import main, utils

STATUS_COLOR = {
    "open": "danger",
    "pending": "info",
    "new": "warning",
    "hold": "dark",
    "solved": "secondary",
    "closed": "light"
}

STATUS_BADGE = {
    "open": "O",
    "pending": "P",
    "new": "P",
    "hold": "H",
    "solved": "S",
    "closed": "C"
}

def error_handler(result_code, resp):
    """Common error handler for view handlers."""
    if result_code == 1:
        return render_template(
            "error.html", error=resp["error"]
        )
    elif result_code == 2:
        return render_template(
            "rate_exceed.html", seconds=resp["retry_after"]
        )
    elif result_code == 3:
        return render_template(
            "not_found.html"
        )
    elif result_code == 4:
        return render_template(
            "service_unavailable.html", seconds=resp["retry_after"]
        )
    else:
        return render_template(
            "error.html", error=resp["error"]
        )

@main.route("/", methods=['GET'])
def ticket_list():
    """View handler for ticket list page."""
    resp = utils.process_response(fetch_ticket_list(), False)
    result_code = resp["result"]

    if result_code == 0:
        detail = resp["detail"]

        for ticket in detail["tickets"]:
            ticket["link"] = "/detail/" + str(ticket["id"])

        return render_template(
            "index.html",
            total_count=detail["count"],
            page_count=len(detail["tickets"]),
            agent_email=Config.agent_email,
            tickets=detail["tickets"],
            badge_code=STATUS_BADGE,
            badge_color=STATUS_COLOR
        )
    
    return error_handler(result_code, resp)

@main.route("/detail/<ticket_id>", methods=['GET'])
def ticket_detail(ticket_id):
    """View handler for ticket detail page."""
    resp = utils.process_response(fetch_ticket_details(ticket_id), True)
    result_code = resp["result"]

    if result_code == 0:
        ticket = resp["detail"]["ticket"]

        return render_template(
            "detail.html",
            subject=ticket["subject"],
            status=ticket["status"].capitalize(),
            description=ticket["description"].replace("\n", "<br>"),
            is_requester_exist=ticket["is_requester_exist"],
            requester=ticket["requester"]
        )

    return error_handler(result_code, resp)
