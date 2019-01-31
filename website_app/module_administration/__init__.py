# myApp/module_administration/__init__.py
from flask import Blueprint
from . import routes

module_administration = Blueprint('admin', __name__, url_prefix='/admin')
#module_administration = Blueprint('admin', __name__)
