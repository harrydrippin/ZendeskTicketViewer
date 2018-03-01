# -*- coding: utf-8 -*-
""" Module for configuration of TicketViewer application.

This module contains some configurations for initiating
TicketViewer application and uses python-dotenv for importing
'.env' file.
"""
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    """Basic Config for overall application."""
    subdomain = os.environ.get("ZENDESK_SUBDOMAIN")
    agent_email = os.environ.get("ZENDESK_AGENT_EMAIL")
    agent_password = os.environ.get("ZENDESK_AGENT_PASSWORD")
