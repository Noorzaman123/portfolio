"""Main public blueprint."""
from flask import Blueprint

main_bp = Blueprint('main', __name__, template_folder='../../templates/main')

from . import routes  # noqa: F401, E402
