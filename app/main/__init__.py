"""Module for managing views and errors."""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors