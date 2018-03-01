# -*- coding: utf-8 -*-
"""Module for initiating this application.

This module contains create_app() function for crafting the
Flask application object.
"""
from flask import Flask

def create_app(config):
    """Return the crafted Flask application object."""
    app = Flask(__name__)
    app.config.from_object(config)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
