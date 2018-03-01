"""Module for processing possible errors.

This module handles 403, 404, and 500 error.
Each function returns appropriate template HTML file to user.
"""
from flask import render_template
from . import main

@main.app_errorhandler(403)
def forbidden(error):
    """Error handler for 403 Forbidden."""
    return render_template('403.html'), 403

@main.app_errorhandler(404)
def page_not_found(error):
    """Error handler for 404 Not Found."""
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(error):
    """Error handler for 500 Internal Server Error"""
    return render_template('500.html'), 500
