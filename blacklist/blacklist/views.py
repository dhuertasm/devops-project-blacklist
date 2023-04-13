from flask import Blueprint
from flask import request

from .core import adicionar_email


blacklist = Blueprint('blacklist', __name__)


@blacklist.route("/blacklists", methods=['POST'])
def agregar_email():
    response, status = adicionar_email(request)
    return response, status




""" 
@usearios.route("/users/auth", methods=['POST'])
def token_user():
    response, status = autenticar_usuario(request)
    return response, status


@usearios.route("/users/me", methods=['GET'])
def information_user():
    response, status = self_information(request)
    return response, status

@usearios.route('/users/ping', methods=['GET'] )
def root():
    return 'pong'

 """