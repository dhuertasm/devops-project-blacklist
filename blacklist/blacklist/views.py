from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required

from .core import adicionar_email, search_email, generate_token


blacklist = Blueprint('blacklist', __name__)


@blacklist.route("/blacklists", methods=['POST'])
@jwt_required()
def agregar_email():
    response, status = adicionar_email(request)
    return response, status

@blacklist.route('/blacklists/<email>', methods=['GET'] )
@jwt_required()
def get_email(email):
    response, status = search_email(email)
    return response, status

@blacklist.route('/blacklists/token', methods=['GET'] )
def token():
    response, status = generate_token()
    return response, status

@blacklist.route('/blacklists/ping', methods=['GET'] )
def root():
    return 'pong'