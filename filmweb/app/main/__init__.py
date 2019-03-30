from flask import Blueprint

main = Blueprint('main', __name__) #tworzymy blueprint

from . import views

# importujemy wszystkie pliki w tej directory które będą używać blueprinty

