# myApp/module_authorization/__init__.py
from flask import Blueprint

#module_authorization = Blueprint('authorization', __name__, url_prefix='/authorization')
module_authorization = Blueprint('authorization', __name__)

from . import routes
