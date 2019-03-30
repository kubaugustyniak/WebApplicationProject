from flask import Blueprint

auth = Blueprint('auth', __name__) #tworzymy blueprint

from . import views
