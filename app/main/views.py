"""Module for processing views on this application.

This module handles ticket list and ticket detail page.
"""
from . import main

@main.route("/", methods=['GET'])
def ticket_list():
    """View handler for ticket list page."""
    return "Ticket List"

@main.route("/detail/<ticket_id>", methods=['GET'])
def ticket_detail(ticket_id):
    """View handler for ticket detail page."""
    return "Requested ticket id is" + str(ticket_id)
