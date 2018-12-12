# myApp/module_authorization/__init__.py
from flask import Blueprint

#module_home = Blueprint('home', __name__, url_prefix='/home')
module_home = Blueprint('home', __name__)

from . import controllers
