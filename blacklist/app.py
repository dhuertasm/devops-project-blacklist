import os
from flask import Flask
from models import db
from flask_cors import CORS
from flask import request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from core import adicionar_email, search_email, generate_token

application = Flask(__name__)

username = os.getenv('DB_USER', '')
password = os.getenv('DB_PASSWORD', '')
dbname = os.getenv('DB_NAME', '')
hostname = os.getenv('DB_HOST', '')
# url_posgres = f'postgresql://{username}:{password}@{hostname}:5432/{dbname}'
url_posgres = os.getenv('DATABASE_URL', 'postgresql://postgres_admin:K38xBUh8&Xfg@moria-devops.c7qi4hgepkrl.us-east-1.rds.amazonaws.com:5432/moria_blacklists')

application.config['SQLALCHEMY_DATABASE_URI'] = url_posgres
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JWT_SECRET_KEY'] = 'frase-secreta'
application.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(application)

db.init_app(application)

with application.app_context():
    db.create_all()

app_context = application.app_context()
app_context.push()
cors = CORS(application)


@application.route("/blacklists", methods=['POST'])
@jwt_required()
def agregar_email():
    response, status = adicionar_email(request)
    return response, status

@application.route('/blacklists/<email>', methods=['GET'] )
@jwt_required()
def get_email(email):
    response, status = search_email(email)
    return response, status

@application.route('/blacklists/token', methods=['GET'] )
def token():
    response, status = generate_token()
    return response, status

@application.route('/blacklists/ping', methods=['GET'] )
def root():
    return 'pong'


